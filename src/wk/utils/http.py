from flask import Response, jsonify


def error_response(payload: dict, code: int = 400) -> Response:
    resp = jsonify(payload)
    resp.status_code = code
    return resp
