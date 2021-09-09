import pytest
from flask import Response
from werkzeug.utils import cached_property

from wk.app import create_app


class TestResponse(Response):

    @cached_property
    def text(self):
        if self.mimetype.startswith('text'):
            return self.data.decode(self.charset)
        return self.data


@pytest.fixture()
def app():
    app = create_app(testing=True)
    app.response_class = TestResponse
    with app.app_context():
        yield app
