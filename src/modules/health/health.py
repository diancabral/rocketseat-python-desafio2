from flask import Blueprint

from config.constants import API_PREFIX
from utils import response

bp = Blueprint("health", __name__, url_prefix=f"{API_PREFIX}/health")


@bp.route("/", methods=["GET"])
def health():
    return response("ok", key="status")
