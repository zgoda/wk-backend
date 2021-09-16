from flask.cli import AppGroup

from .db import database, models

db_cli = AppGroup('db')


@db_cli.command('init', help='Initialise empty database')
def init_db():
    database.create_tables(models)
