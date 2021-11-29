from flask import url_for


def test_get_fail_notfound(client):
    url = url_for("api.event_item", event_id=1)
    rv = client.get(url)
    assert rv.status_code == 404


def test_get_ok(client, event_factory):
    event = event_factory()
    url = url_for("api.event_item", event_id=event.id)
    rv = client.get(url)
    assert rv.status_code == 200
    assert "item" in rv.json
    assert rv.json["item"]["name"] == event.name


def test_patch_fail_notfound(client, login, user_factory):
    data = {
        "name": "Some event",
        "date": 100000000,
        "length": 20,
        "location": "everywhere",
    }
    email = "test@example.com"
    password = "pass"
    name = "test name"
    user_factory(email=email, password=password, name=name)
    url = url_for("api.event_item", event_id=1)
    tokens = login(client, email, password)
    headers = {"X-CSRF-TOKEN": tokens.csrf_access_token}
    rv = client.patch(url, json=data, headers=headers)
    assert rv.status_code == 404


def test_patch_fail_notallowed(client, login, user_factory, event_factory):
    data = {
        "name": "Some event",
        "date": 100000000,
        "length": 20,
        "location": "everywhere",
    }
    email = "test@example.com"
    password = "pass"
    name = "test name"
    user_factory(email=email, password=password, name=name)
    event = event_factory()
    url = url_for("api.event_item", event_id=event.id)
    tokens = login(client, email, password)
    headers = {"X-CSRF-TOKEN": tokens.csrf_access_token}
    rv = client.patch(url, json=data, headers=headers)
    assert rv.status_code == 403


def test_patch_ok(client, login, user_factory, event_factory):
    data = {
        "name": "Some event",
        "date": 100000000,
        "length": 20,
        "location": "everywhere",
    }
    email = "test@example.com"
    password = "pass"
    name = "test name"
    user = user_factory(email=email, password=password, name=name)
    event = event_factory(user=user)
    url = url_for("api.event_item", event_id=event.id)
    tokens = login(client, email, password)
    headers = {"X-CSRF-TOKEN": tokens.csrf_access_token}
    rv = client.patch(url, json=data, headers=headers)
    assert rv.status_code == 200
    assert rv.json["item"]["location"] == data["location"]
