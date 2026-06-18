from http import HTTPStatus

from flask import jsonify


def http_response(
    message: str = "",
    *,
    code: str,
    status: HTTPStatus | int = HTTPStatus.OK,
    key: str = "message",
    **kwargs,
):
    body = {**kwargs} if message == "" else {**kwargs, key: message}

    return jsonify({**body, "code": code}), int(status)
