from http import HTTPStatus

from bcrypt import checkpw
from flask import Blueprint, request
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import select

from config.constants import API_PREFIX
from config.database import db
from models import User
from utils import http_response

from .constants import AUTH_STATUS_CODE
from .schemas import AuthLoginBody

api = Blueprint("auth", __name__, url_prefix=f"{API_PREFIX}/v1/auth")


@api.route("/login/", methods=["POST"])
def login():
    payload = AuthLoginBody.model_validate(request.get_json())

    username = payload.username
    password = payload.password

    user = db.session.scalar(select(User).where(User.username == username))

    if user and checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        login_user(user)
        return http_response(code=AUTH_STATUS_CODE.AUTH_LOGIN_SUCCESS)
    else:
        return http_response(
            code=AUTH_STATUS_CODE.AUTH_LOGIN_ERROR,
            status=HTTPStatus.UNAUTHORIZED,
        )


@api.route("/logout/", methods=["GET"])
@login_required
def logout():
    logout_user()
    return http_response(code=AUTH_STATUS_CODE.AUTH_LOGOFF_SUCCESS)
