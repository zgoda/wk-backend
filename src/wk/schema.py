from __future__ import annotations

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

    @classmethod
    def get_instance(cls) -> UserSchema:
        return cls()


class EventSchema(Schema):
    user = fields.Nested(
        UserSchema, only=['display_name', 'is_active', 'name', 'email'], dump_only=True,
    )
    created_millis = fields.Int(data_key='created', dump_only=True)
    name = fields.Str(required=True)
    date_millis = fields.Int(data_key='date', required=True)
    length = fields.Int(required=True)
    location = fields.Str(required=True)
    virtual = fields.Bool(default=False)
    public = fields.Bool(default=True)
    description = fields.Str()

    @classmethod
    def get_instance(cls) -> EventSchema:
        return cls()
