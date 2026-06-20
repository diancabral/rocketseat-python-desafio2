from http import HTTPStatus

from modules.auth.constants import AUTH_STATUS_CODE

from .http_response import http_response


def handle_unauthorized():
    return http_response(
        code=AUTH_STATUS_CODE.UNAUTHORIZED, status=HTTPStatus.UNAUTHORIZED
    )


def handle_forbidden():
    return http_response(code=AUTH_STATUS_CODE.FORBIDDEN, status=HTTPStatus.FORBIDDEN)
