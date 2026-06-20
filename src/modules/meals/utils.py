from http import HTTPStatus
from typing import cast
from uuid import UUID

from flask_login import current_user

from models import User
from modules.meals.constants import MEAL_STATUS_CODE
from utils import http_response


def http_response_meal_not_found(meal_id: UUID):
    return http_response(
        f"A refeição '{meal_id}' não existe.",
        code=MEAL_STATUS_CODE.MEAL_NOT_FOUND,
        status=HTTPStatus.NOT_FOUND,
    )


def is_current_user_or_admin(user_id: UUID):
    user = cast(User, current_user)

    return user_id == user.uuid or user.role == "admin"


def is_current_user(user_id: UUID):
    user = cast(User, current_user)

    return user_id == user.uuid
