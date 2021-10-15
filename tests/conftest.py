import os

import pytest
from flask import Response
from pytest_factoryboy import register
from werkzeug.utils import cached_property

from wk.app import create_app
from wk.db import database, models

from .factories import UserFactory

register(UserFactory)


class TestResponse(Response):
    @cached_property
    def text(self):
        if self.mimetype.startswith("text"):
            return self.data.decode(self.charset)
        return self.data


def fake_gen_password_hash(password):
    return password


def fake_check_password_hash(stored, password):
    return stored == password


@pytest.fixture(scope="session", autouse=True)
def faker_session_locale():
    return ["pl_PL"]


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
    app.response_class = TestResponse
    with app.app_context():
        database.create_tables(models)
        yield app
        database.drop_tables(models)
