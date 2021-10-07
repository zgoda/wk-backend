from flask import Blueprint, Response, current_app, jsonify
from flask.views import MethodView
from webargs.flaskparser import use_args

from .db import Event
from .schema import event_schema
from .utils.views import get_page

bp = Blueprint('api', __name__)


class EventCollection(MethodView):

    def get(self) -> Response:
        page = get_page()
        q = Event.select().order_by(Event.date.desc())
        q = q.paginate(page, current_app.config['PAGE_SIZE'])
        return jsonify({'events': event_schema.dump(q, many=True)})

    @use_args(event_schema)
    def post(self, args) -> Response:
        pass


# register routes
bp.add_url_rule(
    '/events', endpoint='event_collection',
    view_func=EventCollection.as_view('event_collection'),
)
