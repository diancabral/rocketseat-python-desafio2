from flask import Blueprint, request
from flask_login import login_required

from config.constants import API_PREFIX
from config.database import db
from models import Meals
from utils import http_response

from .constants import MEAL_STATUS_CODE
from .schemas import CreateMealBody

api = Blueprint("meals", __name__, url_prefix=f"{API_PREFIX}/v1/meals")


@api.route("/", methods=["POST"])
@login_required
def list_meals():
    payload = CreateMealBody.model_validate(request.get_json())

    username = payload.username

    new_meal = Meals()

    new_meal.name = payload.username

    db.session.add(new_meal)
    db.session.commit()

    return http_response(
        "Refeição criada com sucesso!", code=MEAL_STATUS_CODE.MEAL_CREATED
    )
