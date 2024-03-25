from db import db

class OrderModel(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    items = db.relationship("OrderItemModel", back_populates="orders", lazy="dynamic", cascade="all, delete")