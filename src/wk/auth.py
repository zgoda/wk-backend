from typing import Mapping

from flask import Blueprint, Response, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity, jwt_required,
    set_refresh_cookies, unset_jwt_cookies,
)
from peewee import IntegrityError
from webargs.flaskparser import use_args

from . import db
from .schema import login_schema, register_schema, user_schema
from .utils.http import error_response

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['POST'])
@use_args(register_schema)
def register(args: Mapping[str, str]) -> Response:
    email = args['email']
    name = args.get('name')
    if not name:
        name = email.split('@')[0]
    try:
        with db.database.atomic():
            user = db.User.create(
                email=email,
                name=name,
                password=db.generate_password_hash(args['password']),
            )
        refresh_token = create_refresh_token(identity=user.email)
        resp = jsonify({
            'message': f'user {user.name} created',
            'access_token': create_access_token(identity=user.email),
            'user': user_schema.dump(user)
        })
        resp.status_code = 201
        set_refresh_cookies(resp, refresh_token)
        return resp
    except IntegrityError:
        return error_response({'message': 'user already registered'})


@bp.route('/login', methods=['POST'])
@use_args(login_schema)
def login(args: Mapping[str, str]) -> Response:
    user = db.User.get_or_none(db.User.email == args['email'])
    if user and user.check_password(args['password']):
        refresh_token = create_refresh_token(identity=user.email)
        resp = jsonify({
            'message': f'logged in as {user.name}',
            'access_token': create_access_token(identity=user.email),
            'user': user_schema.dump(user)
        })
        set_refresh_cookies(resp, refresh_token)
        return resp
    return error_response({'message': 'wrong credentials'})


@bp.route('/logout', methods=['POST'])
@jwt_required(refresh=True)
def logout() -> Response:
    resp = jsonify({'message': 'user logged out'})
    unset_jwt_cookies(resp)
    return resp


@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh() -> Response:
    identity = get_jwt_identity()
    refresh_token = create_refresh_token(identity=identity)
    resp = jsonify({'access_token': create_access_token(identity=identity)})
    set_refresh_cookies(resp, refresh_token)
    return resp
