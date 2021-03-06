import datetime
from typing import Mapping, Union

from flask import Blueprint, Response, current_app, jsonify
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from webargs import fields
from webargs.flaskparser import use_args

from .db import Event, User
from .schema import event_schema, user_schema
from .utils.http import error_response
from .utils.pagination import Pagination

bp = Blueprint("api", __name__)


class UserItemResource(MethodView):
    @jwt_required()
    @use_args(user_schema)
    def patch(self, args, email) -> Response:
        try:
            user = User.get(
                (User.email == email) & (User.is_active == True)  # noqa: E712
            )
        except User.DoesNotExist:
            return error_response({"message": "user not found"}, code=404)
        if email != get_jwt_identity():
            return error_response({"message": "not allowed"}, code=403)
        user.name = args.get("name")
        user.save()
        return jsonify({"message": "user data changed", "user": user_schema.dump(user)})


class EventCollectionResource(MethodView):
    @use_args({"current": fields.Bool(load_default="y")}, location="query")
    def get(self, args) -> Response:
        if args["current"]:
            q = Event.select().where(Event.date >= datetime.date.today())
        else:
            q = Event.select()
        q.order_by(Event.date)
        pagination = Pagination(q, page_size=current_app.config["PAGE_SIZE"])
        return jsonify(
            {
                "collection": event_schema.dump(pagination.items, many=True),
                "pagination": pagination.serialize_meta(),
            }
        )

    @jwt_required()
    @use_args(event_schema)
    def post(self, args) -> Response:
        email = get_jwt_identity()
        user = User.get_active(email)
        e = Event.create(user=user, **args)
        resp = jsonify({"message": "event created", "item": event_schema.dump(e)})
        resp.status_code = 201
        return resp


class EventItemResource(MethodView):
    def get(self, event_id: int) -> Response:
        event = Event.get_or_none(Event.id == event_id)
        if event is None:
            return error_response({"message": "Event does not exist"}, 404)
        return jsonify({"item": event_schema.dump(event)})

    @jwt_required()
    @use_args(event_schema)
    def patch(
        self, args: Mapping[str, Union[str, int, bool]], event_id: int
    ) -> Response:
        event = Event.get_or_none(Event.id == event_id)
        if event is None:
            return error_response({"message": "Event does not exist"}, 404)
        if event.user.email != get_jwt_identity():
            return error_response({"message": "not allowed"}, code=403)
        q = Event.update(**args).where(Event.id == event.id)
        q.execute()
        event = Event.get_by_id(event_id)
        return jsonify({"item": event_schema.dump(event)})


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
bp.add_url_rule(
    "/event/<int:event_id>",
    endpoint="event_item",
    view_func=EventItemResource.as_view("event_item"),
)
