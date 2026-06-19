from flask import Flask

from modules import auth_api, health_api, users_api


def register_routes(app: Flask):
    app.register_blueprint(auth_api)
    app.register_blueprint(health_api)
    app.register_blueprint(users_api)
