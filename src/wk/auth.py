from typing import Mapping

from flask import Blueprint, Response, jsonify
from webargs.flaskparser import use_args

from . import schema

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['POST'])
def register() -> Response:
    return jsonify({'message': 'User registration'})


@bp.route('/login', methods=['POST'])
@use_args(schema.login_args)
def login(args: Mapping[str, str]) -> Response:
    return jsonify({'message': 'User login'})


@bp.route('/logout', methods=['POST'])
def logout() -> Response:
    return jsonify({'message': 'User logout'})


@bp.route('/refresh', methods=['POST'])
def refresh() -> Response:
    return jsonify({'message': 'User logout'})
