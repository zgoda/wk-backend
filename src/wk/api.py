from flask import Blueprint, Response, current_app, jsonify
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from webargs.flaskparser import use_args

from .db import Event, User
from .schema import event_schema, user_schema
from .utils.http import error_response
from .utils.views import get_page

bp = Blueprint("api", __name__)


class UserItemResource(MethodView):
    @jwt_required()
    @use_args(user_schema)
    def post(self, args, email) -> Response:
        try:
            user = User.get_by_id(email)
        except User.DoesNotExist:
            return error_response({"message": "user not found"}, code=404)
        if email != get_jwt_identity():
            return error_response({"message": "not allowed"}, code=403)
        user.name = args.get("name")
        user.save()
        return jsonify({"message": "user data changed", "user": user_schema.dump(user)})


class EventCollectionResource(MethodView):
    def get(self) -> Response:
        page = get_page()
        q = Event.select().order_by(Event.date.desc())
        q = q.paginate(page, current_app.config["PAGE_SIZE"])
        return jsonify({"events": event_schema.dump(q, many=True)})

    @jwt_required()
    @use_args(event_schema)
    def post(self, args) -> Response:
        email = get_jwt_identity()
        e = Event.create(user_id=email, **args)
        resp = jsonify({"message": "Event created", "event": event_schema.dump(e)})
        resp.status_code = 201
        return resp


# register routes
bp.add_url_rule(
    "/user/<email>",
    endpoint="user_item",
    view_func=UserItemResource.as_view("user_item"),
)
bp.add_url_rule(
    "/events",
    endpoint="event_collection",
    view_func=EventCollectionResource.as_view("event_collection"),
)
