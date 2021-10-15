import pytest
from flask import url_for


@pytest.mark.parametrize(
    "input_data",
    [
        {"email": "testuser@example.com", "password": "somepassword"},
        {
            "email": "testuser@example.com",
            "password": "somepassword",
            "name": "User Name",
        },
    ],
    ids=["minimal", "full-data"],
)
def test_register(client, input_data):
    url = url_for("auth.register")
    rv = client.post(url, json=input_data)
    assert rv.status_code == 201
    assert "user" in rv.json


def test_register_fail_duplicate_user(client, user_factory):
    url = url_for("auth.register")
    input_data = {"email": "testuser@example.com", "password": "somepassword"}
    user_factory(email=input_data["email"])
    rv = client.post(url, json=input_data)
    assert rv.status_code == 400
    assert "user already registered" in rv.json["message"]


def test_register_fail_incomplete_data(client):
    url = url_for("auth.register")
    input_data = {"name": "User Name", "password": "somepassword"}
    rv = client.post(url, json=input_data)
    assert rv.status_code == 422


def test_login(client, user_factory):
    email = "user@example.com"
    password = "pass"
    user_factory(email=email, password=password)
    url = url_for("auth.login")
    input_data = {"email": email, "password": password}
    rv = client.post(url, json=input_data)
    assert rv.status_code == 200
    assert "user" in rv.json


def test_login_fail_bad_credentials(client, user_factory):
    email = "user@example.com"
    password = "pass"
    user_factory(email=email, password=password)
    url = url_for("auth.login")
    input_data = {"email": email, "password": "wrong"}
    rv = client.post(url, json=input_data)
    assert rv.status_code == 400
    assert "wrong credentials" in rv.json["message"]


def test_login_fail_user_not_found(client):
    email = "user@example.com"
    password = "pass"
    url = url_for("auth.login")
    input_data = {"email": email, "password": password}
    rv = client.post(url, json=input_data)
    assert rv.status_code == 400
    assert "wrong credentials" in rv.json["message"]
