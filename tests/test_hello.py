from flask import url_for


def test_hello(client):
    url = url_for("api.hello")
    rv = client.get(url)
    assert rv.status_code == 200
    assert rv.json["message"] == "hello"
