from marshmallow import Schema, fields


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class RegisterSchema(LoginSchema):
    name = fields.Str()


class UserSchema(Schema):
    email = fields.Email(required=True)
    name = fields.Str()
    is_active = fields.Bool(data_key='isActive')
    display_name = fields.Str(data_key='displayName')
    created_millis = fields.Int(data_key='created')


class EventSchema(Schema):
    user = fields.Nested(
        UserSchema, only=('display_name', 'is_active', 'name', 'email'),
        dump_only=True,
    )
    created_millis = fields.Int(data_key='created', dump_only=True)
    name = fields.Str(required=True)
    date_millis = fields.Int(data_key='date', required=True)
    length = fields.Int(required=True)
    location = fields.Str(required=True)
    virtual = fields.Bool(default=False)
    public = fields.Bool(default=True)
    description = fields.Str()


# schema instances
login_schema = LoginSchema()
register_schema = RegisterSchema()
user_schema = UserSchema()
event_schema = EventSchema()
