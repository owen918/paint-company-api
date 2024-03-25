from models import OrderItemModel
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import OrderItemSchema, OrderItemUpdateSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("order_items", __name__, description="Operations on Order Items")

@blp.route("/paint/order/item")
class OrderItemList(MethodView):
    @blp.response(200, OrderItemSchema(many=True))
    def get(self):
        return OrderItemModel.query.all()

    @blp.arguments(OrderItemSchema)
    @blp.response(201, OrderItemSchema)
    def post(self, order_item_data):
        order_item = OrderItemModel(**order_item_data)
        try:
            db.session.add(order_item)
            db.session.commit()
        except SQLAlchemyError:
            return abort(500, message="An error occurred while inserting a paint order item")
        
        return order_item

@blp.route("/paint/order/item/<int:item_id>")
class OrderItem(MethodView):
    @blp.response(200, OrderItemSchema)
    def get(self, item_id):
        item = OrderItemModel.query.get_or_404(item_id)
        return item

    @blp.arguments(OrderItemUpdateSchema)
    @blp.response(200, OrderItemSchema)
    def put(self, item_update_data, item_id):
        item = OrderItemModel.query.get_or_404(item_id)
        if item:
            item.color = item_update_data["color"]
            item.quantity = item_update_data["quantity"]
            item.store_id = item_update_data["store_id"]
        else:
            item = OrderItemModel(id=item_id, **item_update_data)
        
        db.session.add(item)
        db.session.commit()

        return item
    
    def delete(self, item_id):
        item = OrderItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Paint Order Item Deleted"}