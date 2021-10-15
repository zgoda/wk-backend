import factory
from factory.base import Factory, FactoryOptions, OptionDefault
from wk.db import database, User

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
