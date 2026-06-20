from uuid import UUID

from flask_login import LoginManager

from config.database import db
from models import User
from utils import handle_unauthorized, http_response


def register_login_manager(login_manager: LoginManager):
    @login_manager.user_loader
    def _load_user(user_id):
        return db.session.get(User, UUID(user_id))

    @login_manager.unauthorized_handler
    def _unauthorized():
        return handle_unauthorized()
