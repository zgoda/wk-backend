from flask import url_for


def test_user_modify(client, login, user_factory):
    email = "test@example.com"
    password = "pass"
    name = "test name"
    user_factory(email=email, password=password, name=name)
    tokens = login(client, email, password)
    headers = {"X-CSRF-TOKEN": tokens.csrf_access_token}
    url = url_for("api.user_item", email=email)
    data = {"name": "My Fancy Name"}
    rv = client.patch(url, json=data, headers=headers)
    assert rv.status_code == 200
    assert rv.json["user"]["name"] == data["name"]


def test_user_modify_fail_notfound(client, login, user_factory):
    email = "test@example.com"
    another_email = "another@example.com"
    password = "pass"
    user_factory(email=email, password=password)
    tokens = login(client, email, password)
    headers = {"X-CSRF-TOKEN": tokens.csrf_access_token}
    url = url_for("api.user_item", email=another_email)
    data = {"name": "My Fancy Name"}
    rv = client.patch(url, json=data, headers=headers)
    assert rv.status_code == 404


def test_user_modify_fail_notallowed(client, login, user_factory):
    email = "test@example.com"
    another_email = "another@example.com"
    password = "pass"
    user_factory(email=email, password=password)
    user_factory(email=another_email, password=password)
    tokens = login(client, email, password)
    headers = {"X-CSRF-TOKEN": tokens.csrf_access_token}
    url = url_for("api.user_item", email=another_email)
    data = {"name": "My Fancy Name"}
    rv = client.patch(url, json=data, headers=headers)
    assert rv.status_code == 403
