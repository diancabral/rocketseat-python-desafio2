from http import HTTPStatus

from flask import Blueprint

from config.constants import API_PREFIX
from utils import http_response

from .constants import HEALTH_STATUS_CODE

api = Blueprint("health", __name__, url_prefix=f"{API_PREFIX}/health")


@api.route("/", methods=["GET"])
def health():
    return http_response(code=HEALTH_STATUS_CODE.OK)
