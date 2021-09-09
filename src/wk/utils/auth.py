from functools import wraps
from typing import Callable

import requests
from flask import current_app, g, request
from jose import jwt

from ..errors import AuthError


def get_token() -> str:
    auth = request.headers.get('Authorization')
    if not auth:
        raise AuthError({
            'code': 'auth_header_missing',
            'description': 'Authorization header is expected',
        }, 401)
    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Bearer type token is expected',
        }, 401)
    if len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not present',
        }, 401)
    if len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token',
        }, 401)
    return parts[1]


def check_scope(scope: str) -> bool:
    token = get_token()
    unverified_claims = jwt.get_unverified_claims(token)
    claims_scope = unverified_claims.get('scope')
    if claims_scope:
        token_scopes = claims_scope['scope'].split()
        for ts in token_scopes:
            if ts == scope:
                return True
    return False


def require_auth(f: Callable) -> Callable:

    @wraps(f)
    def decorated(*args, **kw):
        c = current_app.config
        token = get_token()
        resp = requests.get(c['AUTH0_JWKS_URI'])
        jwks = resp.json()
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
        if rsa_key:
            try:
                g.user = jwt.decode(
                    token, rsa_key,
                    algorithms=c['AUTH0_ALGORITHMS'],
                    audience=c['AUTH0_AUDIENCE'],
                    issuer=c['AUTH0_ISSUER']
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({
                    'code': 'token_expired',
                    'description': 'Authentication token expired',
                }, 401)
            except jwt.JWTClaimsError:
                raise AuthError({
                    'code': 'invalid_header',
                    'description': 'Unable to parse authentication token',
                }, 401)
            return f(*args, **kw)
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to find appropriate key',
        }, 401)

    return decorated
