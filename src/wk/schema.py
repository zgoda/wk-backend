from marshmallow import Schema, fields


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class RegisterSchema(LoginSchema):
    name = fields.Str()


class UserSchema(Schema):
    email = fields.Email(required=True)
    name = fields.Str()


user_schema = UserSchema()
