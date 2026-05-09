import factory
from django.contrib.auth import get_user_model
from faker import Faker
from libraries.models import Library, LibraryItem

from tests.factories.classifications import PlatformFactory
from tests.factories.games import GameFactory

fake = Faker()
User = get_user_model()


# -------------------------
# USER
# -------------------------
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda o: f'{o.username}@test.com')
    password = factory.PostGenerationMethodCall('set_password', 'password123')


# -------------------------
# LIBRARY
# -------------------------
class LibraryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Library
        django_get_or_create = ('user',)

    user = factory.SubFactory(UserFactory)
    is_private = False

    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        if not create:
            return


class LibraryItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LibraryItem

    library = factory.SubFactory(LibraryFactory)
    game = factory.SubFactory(GameFactory)
    platform = factory.SubFactory(PlatformFactory)

    status = LibraryItem.Status.PLANNING
    is_private = False
    hours_played = factory.LazyFunction(
        lambda: fake.pydecimal(left_digits=2, right_digits=1, positive=True)
    )

    @factory.post_generation
    def attach_platform(self, create, extracted, **kwargs):
        if not create:
            return
        self.game.platforms.add(self.platform)