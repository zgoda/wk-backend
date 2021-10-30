from datetime import datetime, time

import factory
from factory.base import Factory, FactoryOptions, OptionDefault
from wk.db import database, User, Event

factory.Faker._DEFAULT_LOCALE = "pl_PL"

DEFAULT_PASSWORD = "password"


class PeeweeOptions(FactoryOptions):
    def _build_default_options(self):
        return super()._build_default_options() + [
            OptionDefault("database", None, inherit=True),
        ]


class PeeweeModelFactory(Factory):
    _options_class = PeeweeOptions

    class Meta:
        abstract = True

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        """Create an instance of the model, and save it to the database."""
        return target_class.create(**kwargs)


class UserFactory(PeeweeModelFactory):
    email = factory.Faker("email")
    password = DEFAULT_PASSWORD
    name = factory.Sequence(lambda n: f"user-{n}")

    class Meta:
        model = User
        database = database


class EventFactory(PeeweeModelFactory):
    name = factory.Sequence(lambda n: f"event-{n}")
    date = factory.Faker("date_this_decade", before_today=False, after_today=True)
    date_millis = factory.LazyAttribute(
        lambda o: datetime.combine(o.date, time()).timestamp() * 1000
    )
    location = factory.Faker("city")
    user = factory.SubFactory(UserFactory)
    length = factory.Faker("pyint", min_value=18, max_value=33)

    class Meta:
        model = Event
        database = database

    class Params:
        with_archived = factory.Trait(
            date=factory.Faker("date_this_decade", before_today=True, after_today=True)
        )
