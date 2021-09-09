import os

from flask import Flask, Response, jsonify
from werkzeug.utils import import_string

from . import errors, api


def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__.split('.')[0])
    configure_app(app, testing)
    with app.app_context():
        configure_blueprints(app)
        configure_error_handlers(app)
    return app


def configure_app(app: Flask, testing: bool) -> None:
    app.config['TESTING'] = testing
    # default config
    app.config.from_object(import_string('wk.config.Config')())
    # test overrides
    if app.testing:
        app.config.from_object(import_string('wk.config.TestConfig')())
    # finally overrides from file passed in env
    config_from_env = os.getenv('WK_CONFIG')
    if config_from_env:
        app.config.from_envvar(config_from_env)


def configure_blueprints(app: Flask) -> None:
    app.register_blueprint(api.bp, url_prefix='/api/v1')


def configure_error_handlers(app: Flask) -> None:

    @app.errorhandler(errors.AuthError)
    def auth_error(ex: errors.AuthError) -> Response:
        resp = jsonify(ex.error)
        resp.status_code = ex.status_code
        return resp
