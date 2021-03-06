import pytest
from flask import url_for

from . import days_from_now_millis


@pytest.mark.options(PAGE_SIZE=2)
def test_get_paginated(client, config, event_factory):
    event_factory.create_batch(5)
    url = url_for("api.event_collection")
    rv = client.get(url)
    assert rv.status_code == 200
    assert len(rv.json["collection"]) <= config["PAGE_SIZE"]
    assert "pagination" in rv.json


@pytest.mark.options(PAGE_SIZE=2)
def test_get_paginated_archive(client, config, event_factory):
    event_factory.create_batch(5, with_archived=True)
    url = url_for("api.event_collection", current="n")
    rv = client.get(url)
    assert rv.status_code == 200
    assert len(rv.json["collection"]) <= config["PAGE_SIZE"]
    assert rv.json["pagination"]["numPages"] == 3


@pytest.mark.options(PAGE_SIZE=2)
def test_get_paginated_last_page(client, event_factory):
    event_factory.create_batch(5)
    url = url_for("api.event_collection", page=3)
    rv = client.get(url)
    assert rv.status_code == 200
    assert len(rv.json["collection"]) == 1


@pytest.mark.options(PAGE_SIZE=2)
def test_get_paginated_past_lastpage(client, event_factory):
    event_factory.create_batch(5)
    url = url_for("api.event_collection", page=4)
    rv = client.get(url)
    assert rv.status_code == 200
    assert len(rv.json["collection"]) == 0


@pytest.mark.options(PAGE_SIZE=2)
def test_get_paginated_wrong_page(client, event_factory):
    event_factory.create_batch(5)
    url = url_for("api.event_collection", page="invalid")
    rv = client.get(url)
    assert rv.status_code == 200
    assert len(rv.json["collection"]) == 2


def test_create_event(client, login, user_factory):
    email = "test@example.com"
    password = "pass"
    user_factory(email=email, password=password)
    tokens = login(client, email, password)
    headers = {"X-CSRF-TOKEN": tokens.csrf_access_token}
    url = url_for("api.event_collection")
    data = {
        "name": "event name",
        "location": "Brok",
        "date": days_from_now_millis(16),
        "length": 20,
    }
    rv = client.post(url, json=data, headers=headers)
    assert rv.status_code == 201
    assert "item" in rv.json
