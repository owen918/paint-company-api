from models import OrderModel, OrderItemModel, PaintInventoryModel, PaintStatusModel
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import OrderSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("orders", __name__, description="Operations on Orders")

@blp.route("/paint/order")
class OrderList(MethodView):
    @blp.response(200, OrderSchema(many=True))
    def get(self):
        return OrderModel.query.all()

    @blp.arguments(OrderSchema)
    @blp.response(201, OrderSchema)
    def post(self, order_data):
        order = OrderModel()
        for item in order_data["items"]:
            new_item = OrderItemModel(color=item["color"], quantity=item["quantity"])
            order.items.append(new_item)

            # Update color inventory and status
            paint_inventory = PaintInventoryModel.query.get(item["color"])
            paint_status = PaintStatusModel.query.get(item["color"])

            if paint_inventory and paint_status:
                paint_inventory.quantity -= item["quantity"]
                if paint_inventory.quantity <= 0:
                    paint_status.status = "out_of_stock"
                elif paint_inventory.quantity <= 20:
                    paint_status.status = "running_low"
                else:
                    paint_status.status = "available"
                
                db.session.add(paint_inventory)
                db.session.add(paint_status)

            
        try:
            db.session.add(order)
            db.session.commit()
        except SQLAlchemyError:
            return abort(500, message="An error occurred while inserting a paint order record")
        
        return order

@blp.route("/paint/order/<int:order_id>")
class Order(MethodView):
    @blp.response(200, OrderSchema)
    def get(self, order_id):
        order = OrderModel.query.get_or_404(order_id)
        return order
    
    def delete(self, order_id):
        paint_inventory = OrderModel.query.get_or_404(order_id)
        db.session.delete(paint_inventory)
        db.session.commit()
        return {"message": "Paint Order Record Deleted"}