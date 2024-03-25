from db import db
from models.color import ColorModel
from sqlalchemy import Enum

class OrderItemModel(db.Model):
    __tablename__ = "order_item"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), unique=False, nullable=False)
    orders = db.relationship("OrderModel", back_populates="items")
    color = db.Column(db.Enum(ColorModel), unique=False, nullable=False)
    quantity= db.Column(db.Integer, unique=False, nullable=False)
