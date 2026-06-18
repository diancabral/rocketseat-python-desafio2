from http import HTTPStatus

from bcrypt import gensalt, hashpw
from flask import Blueprint, request
from sqlalchemy import select

from config.constants import API_PREFIX
from config.database import db
from models import User
from utils import http_response

from .constants import USER_STATUS_CODE
from .schemas import CreateUserBody

api = Blueprint("users", __name__, url_prefix=f"{API_PREFIX}/v1/users")


def username_available(username: str):
    user = db.session.scalar(select(User).where(User.username == username))
    return user is None


@api.route("/", methods=["POST"])
def create_user():
    payload = CreateUserBody.model_validate(request.get_json())

    username = payload.username

    if username_available(username):
        hash_password = hashpw(payload.password.encode("utf-8"), gensalt())

        new_user = User()

        new_user.username = username
        new_user.password = hash_password.decode("ascii")
        new_user.role = "user"

        db.session.add(new_user)
        db.session.commit()

        return http_response(
            "Usuário criado com sucesso!", code=USER_STATUS_CODE.USER_CREATED
        )
    else:
        return http_response(
            f"O nome de usuário '{username}' já existe.",
            code=USER_STATUS_CODE.USER_ALREADY_EXISTS,
            status=HTTPStatus.CONFLICT,
        )
