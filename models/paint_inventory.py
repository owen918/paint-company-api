from db import db
from models.color import ColorModel
from sqlalchemy import Enum

class PaintInventoryModel(db.Model):
    __tablename__ = "paint_inventory"

    color = db.Column(db.Enum(ColorModel), primary_key=True)
    quantity = db.Column(db.Integer, unique=False, nullable=False)