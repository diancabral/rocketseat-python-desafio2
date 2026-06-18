from flask import Flask

from modules.health import bp as health_bp


def register_routes(app: Flask):
    app.register_blueprint(health_bp)
