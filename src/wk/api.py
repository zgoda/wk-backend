from flask import Blueprint, Response, jsonify

bp = Blueprint('api', __name__)


@bp.route('/hello')
def hello() -> Response:
    return jsonify({'message': 'hello'})
