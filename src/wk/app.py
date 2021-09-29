import os
import tempfile

from flask import Flask, Response, jsonify
from werkzeug.utils import import_string

from . import api, auth, cli, ext
from .db import database


def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__.split('.')[0])
    configure_app(app, testing)
    with app.app_context():
        configure_database(app)
        configure_extensions(app)
        configure_blueprints(app)
        configure_cli(app)
        configure_error_handlers(app)
    return app


def configure_app(app: Flask, testing: bool) -> None:
    app.config['TESTING'] = testing
    # default config
    app.config.from_object(import_string('wk.config.Config')())
    # dev overrides
    if app.config['ENV'] == 'development':
        app.config.from_object(import_string('wk.config.DevConfig')())
    # test overrides
    if app.testing:
        app.config.from_object(import_string('wk.config.TestConfig')())
    # finally overrides from file passed in env
    config_from_env = os.getenv('WK_CONFIG')
    if config_from_env:
        app.config.from_envvar(config_from_env)


def configure_database(app: Flask) -> None:
    if app.testing:
        tmp_dir = tempfile.mkdtemp()
        db_name = os.path.join(tmp_dir, 'db.sqlite')
    else:
        db_name = os.getenv('DB_NAME')
    kw = {
        'pragmas': {
            'journal_mode': 'wal',
            'cache_size': -1 * 64000,
            'foreign_keys': 1,
            'ignore_check_constraints': 0,
        }
    }
    if db_name is None:
        db_name = ':memory:'
        kw = {}
    database.init(db_name, **kw)

    def db_connect():
        database.connect(reuse_if_open=True)
    app.before_request(db_connect)

    def db_close(_):
        if not database.is_closed():
            database.close()
    app.teardown_request(db_close)


def configure_extensions(app: Flask) -> None:
    ext.jwt.init_app(app)


def configure_blueprints(app: Flask) -> None:
    app.register_blueprint(api.bp, url_prefix='/v1/api')
    app.register_blueprint(auth.bp, url_prefix='/v1/auth')


def configure_cli(app: Flask) -> None:
    app.cli.add_command(cli.db_cli)


def configure_error_handlers(app: Flask) -> None:

    @app.errorhandler(400)
    @app.errorhandler(422)
    def bad_request_error(err) -> Response:
        headers = err.data.get('headers', None)
        messages = err.data.get('messages', ['Invalid request.'])
        if headers:
            return jsonify({'errors': messages}), err.code, headers
        else:
            return jsonify({'errors': messages}), err.code
