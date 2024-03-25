from db import db
from models.color import ColorModel
from models.status import StatusModel
from sqlalchemy import Enum

class PaintStatusModel(db.Model):
    __tablename__ = "paint_status"

    color = db.Column(db.Enum(ColorModel), primary_key=True)
    status = db.Column(db.Enum(StatusModel), nullable=False)