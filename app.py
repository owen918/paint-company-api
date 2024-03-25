from flask import Flask
from flask_smorest import Api
from resources.paint_inventory import blp as PaintInventoryBlueprint
from resources.paint_status import blp as PaintStatusBlueprint
from resources.order import blp as OrderBlueprint
from resources.order_item import blp as OrderItemBlueprint
import models
import os
from db import db
from flask_migrate import Migrate

def create_app(db_url=None):

    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Paint Company REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    api = Api(app)
    api.register_blueprint(PaintInventoryBlueprint)
    api.register_blueprint(PaintStatusBlueprint)
    api.register_blueprint(OrderBlueprint)
    api.register_blueprint(OrderItemBlueprint)


    return app