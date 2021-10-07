from flask.cli import AppGroup

from .db import database, models

db_cli = AppGroup('db', help='Database operations')


@db_cli.command('init', help='Initialise empty database')
def init_db():
    database.create_tables(models)


@db_cli.command('clear', help='Drop all database objects')
def clear_db():
    database.drop_tables(models)


@db_cli.command('recreate', help='Recreate database objects from scratch')
def recreate_db():
    database.drop_tables(models)
    database.create_tables(models)
