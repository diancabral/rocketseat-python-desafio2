from http import HTTPStatus
from typing import cast

from bcrypt import gensalt, hashpw
from flask import Blueprint, request
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError

from config.constants import API_PREFIX
from config.database import db
from models import User
from utils import http_response

from .constants import USER_STATUS_CODE
from .schemas import CreateUserBody

api = Blueprint("users", __name__, url_prefix=f"{API_PREFIX}/v1/users/")


@api.route("/", methods=["POST"])
def create_user():
    payload = CreateUserBody.model_validate(request.get_json())

    username = payload.username

    try:
        hash_password = hashpw(payload.password.encode("utf-8"), gensalt())

        new_user = User()

        new_user.username = payload.username
        new_user.email = payload.email
        new_user.password = hash_password.decode("ascii")
        new_user.role = "user"

        db.session.add(new_user)
        db.session.commit()

        return http_response(
            "Usuário criado com sucesso!", code=USER_STATUS_CODE.USER_CREATED
        )
    except IntegrityError as e:
        db.session.rollback()
        return http_response(
            f"O nome de usuário '{username}' já existe.",
            code=USER_STATUS_CODE.USER_ALREADY_EXISTS,
            status=HTTPStatus.CONFLICT,
        )


@api.route("/me/", methods=["GET"])
@login_required
def get_current_user():
    user = cast(User, current_user)

    return http_response(
        **{
            "uuid": user.uuid,
            "username": user.username,
            "email": user.email,
            "role": user.role,
        }
    )
