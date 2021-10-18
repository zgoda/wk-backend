import pytest
from flask import url_for


@pytest.mark.options(PAGE_SIZE=2)
def test_get_paginated(client, config, event_factory):
    event_factory.create_batch(5)
    url = url_for("api.event_collection")
    rv = client.get(url)
    assert rv.status_code == 200
    assert len(rv.json["events"]) <= config["PAGE_SIZE"]


@pytest.mark.options(PAGE_SIZE=2)
def test_get_paginated_last_page(client, event_factory):
    event_factory.create_batch(5)
    url = url_for("api.event_collection", page=3)
    rv = client.get(url)
    assert rv.status_code == 200
    assert len(rv.json["events"]) == 1


@pytest.mark.options(PAGE_SIZE=2)
def test_get_paginated_past_lastpage(client, event_factory):
    event_factory.create_batch(5)
    url = url_for("api.event_collection", page=4)
    rv = client.get(url)
    assert rv.status_code == 200
    assert len(rv.json["events"]) == 0
