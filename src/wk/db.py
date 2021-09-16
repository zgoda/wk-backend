from passlib.context import CryptContext
from peewee import CharField, Model as PeeweeModel, SqliteDatabase, TextField

pwd_context = CryptContext(schemes=['argon2'])


def generate_password_hash(password: str) -> str:  # pragma: nocover
    return pwd_context.hash(password)


def check_password_hash(stored: str, password: str) -> bool:  # pragma: nocover
    return pwd_context.verify(password, stored)


database = SqliteDatabase(None)


class Model(PeeweeModel):

    class Meta:
        database = database


class User(Model):
    email = CharField(max_length=200, primary_key=True)
    password = TextField()

    class Meta:
        table_name = 'users'

    def set_password(self, password: str) -> None:  # pragma: nocover
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)


models = [User]
