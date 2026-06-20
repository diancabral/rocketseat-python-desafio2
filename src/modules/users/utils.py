from http import HTTPStatus
from uuid import UUID

from utils import http_response

from .constants import USER_STATUS_CODE


def http_response_user_not_found(user_id: UUID):
    return http_response(
        f"O usuário '{user_id}' não existe.",
        code=USER_STATUS_CODE.USER_NOT_FOUND,
        status=HTTPStatus.NOT_FOUND,
    )
