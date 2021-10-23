from __future__ import annotations

from datetime import datetime
from enum import Enum, unique
from typing import Optional

from passlib.context import CryptContext
from peewee import BooleanField, CharField, DateTimeField, ForeignKeyField, IntegerField
from peewee import Model as PeeweeModel
from peewee import SqliteDatabase, TextField

pwd_context = CryptContext(schemes=["argon2"])


def generate_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def check_password_hash(stored: str, password: str) -> bool:
    return pwd_context.verify(password, stored)


def current_timestamp_millis() -> int:
    return int(datetime.utcnow().timestamp() * 1000)


database = SqliteDatabase(None)


class Model(PeeweeModel):
    class Meta:
        database = database


class User(Model):
    email = CharField(max_length=200, primary_key=True)
    password = TextField()
    name = CharField(max_length=200, index=True)
    is_active = BooleanField(default=True, index=True)
    created = DateTimeField(default=datetime.utcnow, index=True)
    created_millis = IntegerField(default=current_timestamp_millis)

    class Meta:
        table_name = "users"

    @property
    def display_name(self) -> str:
        if self.is_active:
            return self.name
        return "inactive user"

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    @classmethod
    def get_active(cls, email: str) -> Optional[User]:
        try:
            return cls.get((cls.email == email) & (cls.is_active == True))  # noqa: E712
        except cls.DoesNotExist:
            return None


class Event(Model):
    user = ForeignKeyField(User, backref="events")
    created = DateTimeField(default=datetime.utcnow, index=True)
    created_millis = IntegerField(default=current_timestamp_millis)
    name = CharField(max_length=200)
    date = DateTimeField(index=True)
    date_millis = IntegerField()
    length = IntegerField()
    location = CharField(max_length=200)
    virtual = BooleanField(default=False)
    public = BooleanField(default=True)
    description = TextField(null=True)

    class Meta:
        indexes = ((("virtual", "public"), False),)


@unique
class ParticipantRole(Enum):
    OWNER = "owner"
    GUEST = "guest"
    SUPPORT = "support"


class Participation(Model):
    user = ForeignKeyField(User, backref="participations")
    event = ForeignKeyField(Event, backref="participants")
    role = CharField(max_length=100, index=True)
    description = TextField(null=True)


class ParticipationAsset(Model):
    participation = ForeignKeyField(Participation, backref="assets")
    asset_type = CharField(max_length=100)
    url = TextField()
    created = DateTimeField(default=datetime.utcnow, index=True)
    created_millis = IntegerField(default=current_timestamp_millis)
    description = TextField(null=True)


models = [User, Event, Participation, ParticipationAsset]
