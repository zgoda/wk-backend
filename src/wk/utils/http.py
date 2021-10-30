from typing import Any, Mapping

from flask import Response, jsonify


def error_response(payload: Mapping[str, Any], code: int = 400) -> Response:
    resp = jsonify(payload)
    resp.status_code = code
    return resp
