from webargs import fields

login_args = {
    'email': fields.Email(required=True),
    'password': fields.Str(required=True),
}
