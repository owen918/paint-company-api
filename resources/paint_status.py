from models import PaintStatusModel
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import PaintStatusSchema, PaintStatusUpdateSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("paint_status", __name__, description="Operations on Paint Status")

@blp.route("/paint/status")
class PaintStatusList(MethodView):
    @blp.response(200, PaintStatusSchema(many=True))
    def get(self):
        return PaintStatusModel.query.all()

    # @blp.arguments(PaintStatusSchema)
    # @blp.response(201, PaintStatusSchema)
    # def post(self, paint_status_data):
    #     paint_status = PaintStatusModel(**paint_status_data)
    #     try:
    #         db.session.add(paint_status)
    #         db.session.commit()
    #     except SQLAlchemyError:
    #         return abort(500, message="An error occurred while inserting a paint status")
        
    #     return paint_status

@blp.route("/paint/status/<string:color_name>")
class PaintStatus(MethodView):
    @blp.response(200, PaintStatusSchema)
    def get(self, color_name):
        color = PaintStatusModel.query.get_or_404(color_name)
        return color
    
    @blp.arguments(PaintStatusUpdateSchema)
    @blp.response(200, PaintStatusSchema)
    def put(self, paint_status_data, color_name):
        paint_status = PaintStatusModel.query.get(color_name)
        if paint_status: # if the status of the color_name paint exists
            paint_status.status = paint_status_data["status"]
        else: # otherwise, we create a new status for the color_name paint
            item = PaintStatusModel(color=color_name, **paint_status_data)
        
        db.session.add(paint_status)
        db.session.commit()

        return paint_status
    
    def delete(self, color_name):
        paint_status = PaintStatusModel.query.get_or_404(color_name)
        db.session.delete(paint_status)
        db.session.commit()
        return {"message": "Paint Status Deleted"}