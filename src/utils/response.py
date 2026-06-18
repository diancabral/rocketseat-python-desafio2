from flask import jsonify


def response(message: str, code=200, *, key: str = "message", **kwargs):
    return jsonify({f"{key}": message, **kwargs}), code
