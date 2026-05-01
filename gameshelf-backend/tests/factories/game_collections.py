import factory
from django.contrib.auth import get_user_model
from faker import Faker

from game_collections.models import Collection, CollectionItem, Wishlist, WishListItem
from tests.factories.classifications import PlatformFactory
from tests.factories.games import GameFactory

fake = Faker()
User = get_user_model()


# -------------------------
# USER (si no tienes uno global reutilizable)
# -------------------------
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda o: f'{o.username}@test.com')
    password = factory.PostGenerationMethodCall('set_password', 'password123')


# -------------------------
# COLLECTION
# -------------------------
class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collection

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f'Collection {n}')
    is_private = False

    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        if not create:
            return


# -------------------------
# COLLECTION ITEM
# -------------------------
class CollectionItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CollectionItem

    collection = factory.SubFactory(CollectionFactory)
    game = factory.SubFactory(GameFactory)
    platform = factory.SubFactory(PlatformFactory)

    type = CollectionItem.Type.DIGITAL
    is_private = False


# -------------------------
# WISHLIST
# -------------------------
class WishlistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Wishlist

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f'Wishlist {n}')
    is_private = False


# -------------------------
# WISHLIST ITEM
# -------------------------
class WishListItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WishListItem

    wishlist = factory.SubFactory(WishlistFactory)
    game = factory.SubFactory(GameFactory)

    platform = factory.SubFactory(PlatformFactory)

    type = WishListItem.Type.DIGITAL

    priority = factory.LazyFunction(lambda: fake.random_int(min=1, max=10))
    annotation = factory.LazyFunction(lambda: fake.sentence(nb_words=6))

    is_private = False
