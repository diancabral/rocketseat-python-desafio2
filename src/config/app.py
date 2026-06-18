from flask import Flask

from config.constants import SECRET_KEY, SQLALCHEMY_DATABASE_URI
from config.database import db


def create_app(config_name: str = "default") -> Flask:
    app = Flask(__name__)

    app.config["SECRET_KEY"] = SECRET_KEY

    if config_name == "testing":
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

    db.init_app(app)

    import models
    from routes import register_routes

    register_routes(app)

    return app
