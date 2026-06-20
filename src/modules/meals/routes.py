from http import HTTPStatus
from typing import cast
from uuid import UUID

from flask import Blueprint, Response, request
from flask_login import current_user, login_required
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from config.constants import API_PREFIX
from config.database import db
from models import Meals, User
from modules.users.utils import http_response_user_not_found
from utils import handle_forbidden, http_response

from .constants import MEAL_STATUS_CODE
from .schemas import CreateMealBody, EditMealBody
from .utils import (
    http_response_meal_not_found,
    is_current_user,
    is_current_user_or_admin,
)

api = Blueprint("meals", __name__, url_prefix=f"{API_PREFIX}/v1/meals")


@api.route("/", methods=["POST"])
@login_required
def create_meal():
    payload = CreateMealBody.model_validate(request.get_json())

    new_meal = Meals()

    user = cast(User, current_user)

    new_meal.name = payload.name
    new_meal.description = payload.description
    new_meal.is_diet = payload.is_diet
    new_meal.user_id = user.uuid

    db.session.add(new_meal)
    db.session.commit()

    return http_response(
        "Refeição criada com sucesso", code=MEAL_STATUS_CODE.MEAL_CREATED
    )


@api.route("/<uuid:meal_id>", methods=["GET"])
@login_required
def view_meal(meal_id: UUID):
    meal = db.session.get(Meals, meal_id)

    if meal is None:
        return http_response_meal_not_found(meal_id)

    if not is_current_user_or_admin(meal.user_id):
        return handle_forbidden()

    return http_response(
        **{
            "uuid": meal.uuid,
            "name": meal.name,
            "description": meal.description,
            "is_diet": meal.is_diet,
            "created_at": meal.created_at,
            "updated_at": meal.updated_at,
            "user": {
                "uuid": meal.user.uuid,
                "username": meal.user.username,
                "email": meal.user.email,
            },
        }
    )


@api.route("/<uuid:meal_id>", methods=["PATCH"])
@login_required
def edit_meal(meal_id: UUID):
    meal = db.session.get(Meals, meal_id)

    if meal is None:
        return http_response_meal_not_found(meal_id)

    if not is_current_user_or_admin(meal.user_id):
        return handle_forbidden()

    payload = EditMealBody.model_validate(request.get_json())

    if payload.name is not None:
        meal.name = payload.name

    if payload.description is not None:
        meal.description = payload.description

    if payload.is_diet is not None:
        meal.is_diet = payload.is_diet

    if db.session.is_modified(meal):
        db.session.commit()
        return http_response(
            "Refeição editada com sucesso", code=MEAL_STATUS_CODE.MEAL_UPDATED
        )
    else:
        db.session.rollback()
        return http_response(
            "Nenhum campo foi alterado", code=MEAL_STATUS_CODE.MEAL_NOT_UPDATED
        )


@api.route("/<uuid:meal_id>", methods=["DELETE"])
@login_required
def delete_meal(meal_id: UUID):
    meal = db.session.get(Meals, meal_id)

    if meal is None:
        return http_response_meal_not_found(meal_id)

    if not is_current_user_or_admin(meal.user_id):
        return handle_forbidden()

    db.session.delete(meal)
    db.session.commit()

    return http_response(
        "Refeição deletada com sucesso", code=MEAL_STATUS_CODE.MEAL_DELETED
    )


@api.route("/user/<uuid:user_id>", methods=["GET"])
@login_required
def list_user_meals(user_id: UUID):

    if not is_current_user_or_admin(user_id):
        return handle_forbidden()

    if not is_current_user(user_id):
        if db.session.get(User, user_id) is None:
            return http_response_user_not_found(user_id)

    meals_list = db.session.scalars(
        select(Meals).options(selectinload(Meals.user)).where(Meals.user_id == user_id)
    ).all()

    if not meals_list:
        return http_response(meals=[], status=HTTPStatus.NO_CONTENT)

    return http_response(
        meals=[
            {
                "uuid": meal.uuid,
                "name": meal.name,
                "description": meal.description,
                "is_diet": meal.is_diet,
                "created_at": meal.created_at,
                "updated_at": meal.updated_at,
                "user": {
                    "uuid": meal.user.uuid,
                    "username": meal.user.username,
                    "email": meal.user.email,
                },
            }
            for meal in meals_list
        ]
    )
