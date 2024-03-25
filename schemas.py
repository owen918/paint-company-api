from marshmallow import Schema, fields
from models import ColorModel
from models import StatusModel

class PaintStatusSchema(Schema):
    color = fields.Enum(ColorModel, required=True)
    status = fields.Enum(StatusModel, required=True)

class PaintStatusUpdateSchema(Schema):
    status = fields.Enum(StatusModel, required=True)


class PaintInventorySchema(Schema):
    color = fields.Enum(ColorModel, required=True)
    quantity = fields.Int(required=True)

class PaintInventoryUpdateSchema(Schema):
    quantity = fields.Int(required=True)

class PlainOrderItemSchema(Schema):
    id = fields.Int(dump_only=True)
    color = fields.Enum(ColorModel, required=True)
    quantity = fields.Int(required=True)

class PlainOrderSchema(Schema):
    id = fields.Int(dump_only=True)

class OrderItemSchema(PlainOrderItemSchema):
    order_id = fields.Int(required=True, load_only=True)
    orders = fields.Nested(PlainOrderSchema(), dump_only=True)

class OrderSchema(PlainOrderSchema):
    items = fields.List(fields.Nested(PlainOrderItemSchema()))

class OrderItemUpdateSchema(Schema):
    color = fields.Enum(ColorModel)
    quantity = fields.Int()
    order_id = fields.Int()