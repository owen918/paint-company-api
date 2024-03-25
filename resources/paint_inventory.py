from models import PaintInventoryModel, PaintStatusModel
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import PaintInventorySchema, PaintInventoryUpdateSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("paint_inventory", __name__, description="Operations on Paint Inventory")

@blp.route("/paint/inventory")
class PaintInventoryList(MethodView):
    @blp.response(200, PaintInventorySchema(many=True))
    def get(self):
        return PaintInventoryModel.query.all()

    @blp.arguments(PaintInventorySchema)
    @blp.response(201, PaintInventorySchema)
    def post(self, paint_inventory_data):
        '''
        if there is no status record when creating a inventory record, create status record along with inventory record,
        otherwise, return error
        '''
        paint_inventory = PaintInventoryModel(**paint_inventory_data)
        paint_status = PaintStatusModel.query.get(paint_inventory_data["color"])
        if paint_status.status != "out_of_stock":
            return abort(500, message="There is a inventory record related to this paint, try modifying inventory record.")
        else:
            if paint_inventory_data["quantity"] <= 0:
                paint_status = PaintStatusModel(color=paint_inventory_data["color"], status="out_of_stock")
            elif paint_inventory_data["quantity"] <= 20:
                paint_status = PaintStatusModel(color=paint_inventory_data["color"], status="running_low")
            else:
                paint_status = PaintStatusModel(color=paint_inventory_data["color"], status="available")
        try:
            db.session.add(paint_inventory)
            db.session.add(paint_status)
            db.session.commit()
        except SQLAlchemyError:
            return abort(500, message="An error occurred while inserting a paint inventory record")
        
        return paint_inventory

@blp.route("/paint/inventory/<string:color_name>")
class PaintInventory(MethodView):
    @blp.response(200, PaintInventorySchema)
    def get(self, color_name):
        paint_inventory = PaintInventoryModel.query.get_or_404(color_name)
        return paint_inventory
    
    @blp.arguments(PaintInventoryUpdateSchema)
    @blp.response(200, PaintInventorySchema)
    def put(self, paint_inventory_data, color_name):

        paint_inventory = PaintInventoryModel.query.get(color_name)
        paint_status = PaintStatusModel.query.get(color_name)

        quantity = paint_inventory_data["quantity"]
        status = ""
        if quantity <= 0:
            status = "out_of_stock"
        elif quantity <= 20:
            status = "running_low"
        else:
            status = "available"

        if paint_inventory and paint_status: # if inventory and status of the color_name paint exists
            paint_status.status = status
            paint_inventory.quantity = quantity
        
        else: # otherwise, we create a new inventory record for the color_name paint
            paint_inventory = PaintInventoryModel(color=color_name, **paint_inventory_data)
            paint_status = PaintStatusModel(color=color_name, status=status)
        
        db.session.add(paint_inventory)
        db.session.add(paint_status)
        db.session.commit()

        return paint_inventory
    
    def delete(self, color_name):
        paint_inventory = PaintInventoryModel.query.get_or_404(color_name)
        db.session.delete(paint_inventory)
        db.session.commit()
        return {"message": "Paint Inventory Record Deleted"}