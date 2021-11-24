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
