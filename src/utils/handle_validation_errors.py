from http import HTTPStatus

from pydantic import ValidationError

from .http_response import http_response


def handle_validation_errors(exc: ValidationError):
    errors: list[dict[str, str]] = []
    for err in exc.errors(include_url=False):
        loc = err.get("loc", ())
        field = ".".join(str(x) for x in loc if x != "body")
        errors.append(
            {"field": field or "root", "message": err["msg"], "type": err["type"]}
        )
    return http_response(
        errors=errors, status=HTTPStatus.UNPROCESSABLE_ENTITY, code="VALIDATION_ERROR"
    )
