from webargs import fields

login_args = {
    'username': fields.Str(required=True),
    'password': fields.Str(required=True),
}
