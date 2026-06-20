from flask import Flask
from flask_login import LoginManager
from pydantic import ValidationError
from werkzeug.exceptions import Forbidden, Unauthorized

import models
from config.constants import SECRET_KEY, SQLALCHEMY_DATABASE_URI
from config.database import db
from modules.auth import register_login_manager
from utils import handle_forbidden, handle_unauthorized, handle_validation_errors

from .routes import register_routes


def create_app(config_name: str = "default") -> Flask:
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    login_manager = LoginManager()

    app.register_error_handler(ValidationError, handle_validation_errors)

    @app.errorhandler(Unauthorized)
    def _unauthorized(e):
        return handle_unauthorized()

    @app.errorhandler(Forbidden)
    def _forbidden(e):
        return handle_forbidden()

    app.config["SECRET_KEY"] = SECRET_KEY

    if config_name == "testing":
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

    db.init_app(app)
    login_manager.init_app(app)

    register_login_manager(login_manager)
    register_routes(app)

    return app
