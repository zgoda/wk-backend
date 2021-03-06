from datetime import date
from marshmallow import Schema, fields, post_load


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class RegisterSchema(LoginSchema):
    name = fields.Str()


class UserSchema(Schema):
    email = fields.Email(dump_only=True)
    name = fields.Str()
    is_active = fields.Bool(data_key="isActive", dump_only=True)
    display_name = fields.Str(data_key="displayName", dump_only=True)
    created_millis = fields.Int(data_key="created", dump_only=True)


class EventSchema(Schema):
    id = fields.Int(data_key="eventId", dump_only=True)  # noqa: A003
    user = fields.Nested(
        UserSchema,
        only=("display_name", "is_active", "name", "email"),
        dump_only=True,
    )
    created_millis = fields.Int(data_key="created", dump_only=True)
    name = fields.Str(required=True)
    date_millis = fields.Int(data_key="date", required=True)
    length = fields.Int(required=True)
    location = fields.Str(required=True)
    virtual = fields.Bool(load_default=False)
    public = fields.Bool(load_default=True)
    description = fields.Str()

    @post_load()
    def date_from_millis(self, data, **kwargs):
        data["date"] = date.fromtimestamp(data["date_millis"] / 1000)
        return data


# schema instances
login_schema = LoginSchema()
register_schema = RegisterSchema()
user_schema = UserSchema()
event_schema = EventSchema()
