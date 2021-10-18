import collections
import os

import pytest
from flask import url_for
from pytest_factoryboy import register

from wk.app import create_app
from wk.db import database, models

from .factories import EventFactory, UserFactory

register(UserFactory)
register(EventFactory)


def fake_gen_password_hash(password):
    return password


def fake_check_password_hash(stored, password):
    return stored == password


Tokens = collections.namedtuple(
    "Tokens",
    ["csrf_access_token", "csrf_refresh_token", "access_token", "refresh_token"],
)


@pytest.fixture(scope="session", autouse=True)
def faker_session_locale():
    return ["pl_PL"]


def _cookie_from_response(response, cookie_name):
    cookie_headers = response.headers.getlist("Set-Cookie")
    for header in cookie_headers:
        attributes = header.split(";")
        if cookie_name in attributes[0]:
            cookie = {}
            for attr in attributes:
                split = attr.split("=")
                cookie[split[0].strip().lower()] = split[1] if len(split) > 1 else True
            return cookie
    return None


@pytest.fixture()
def login():
    def _login(client, email, password):
        url = url_for("auth.login")
        rv = client.post(url, json={"email": email, "password": password})
        return Tokens(
            csrf_access_token=_cookie_from_response(rv, "csrf_access_token"),
            csrf_refresh_token=_cookie_from_response(rv, "csrf_refresh_token"),
            access_token=_cookie_from_response(rv, "access_token"),
            refresh_token=_cookie_from_response(rv, "refresh_token"),
        )

    return _login


@pytest.fixture()
def app(mocker):
    mocker.patch("wk.db.generate_password_hash", fake_gen_password_hash)
    mocker.patch("wk.db.check_password_hash", fake_check_password_hash)
    os.environ["FLASK_ENV"] = "test"
    mocker.patch.dict(
        "os.environ",
        {"WK_SECRET_KEY": "very secret", "WK_JWT_SECRET_KEY": "another very secret"},
    )
    app = create_app(testing=True)
    with app.app_context():
        database.create_tables(models)
        yield app
        database.drop_tables(models)
