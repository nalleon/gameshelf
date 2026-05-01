import factory
from django.contrib.auth import get_user_model
from faker import Faker

from games.models import FavoriteItem, Game, Media, Review
from tests.factories.classifications import (
    DeveloperFactory,
    GenreFactory,
    PlatformFactory,
    PublisherFactory,
    RegionFactory,
)

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
# GAME
# -------------------------
class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game

    igdb_id = factory.Sequence(lambda n: n + 10000)
    title = factory.Sequence(lambda n: f'Game {n}')
    description = factory.LazyFunction(lambda: fake.text(max_nb_chars=200))

    cover_default = factory.LazyFunction(lambda: fake.image_url())
    cover_detail = factory.LazyFunction(lambda: fake.image_url())

    released_at = factory.LazyFunction(
        lambda: fake.date_between(start_date='-10y', end_date='today')
    )

    parent_game_igdb = None

    region = factory.SubFactory(RegionFactory)

    age_rating = 'TBA'
    mature_content = True

    @factory.post_generation
    def platforms(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for platform in extracted:
                self.platforms.add(platform)
        else:
            self.platforms.add(PlatformFactory())

    @factory.post_generation
    def genres(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for genre in extracted:
                self.genres.add(genre)
        else:
            self.genres.add(GenreFactory())

    @factory.post_generation
    def developers(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for dev in extracted:
                self.developers.add(dev)
        else:
            self.developers.add(DeveloperFactory())

    @factory.post_generation
    def publishers(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for pub in extracted:
                self.publishers.add(pub)
        else:
            self.publishers.add(PublisherFactory())


# -------------------------
# REVIEW
# -------------------------
class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    content = factory.LazyFunction(lambda: fake.text(max_nb_chars=300))
    recommend = factory.LazyFunction(lambda: fake.boolean())

    game = factory.SubFactory(GameFactory)
    author = factory.SubFactory(UserFactory)


# -------------------------
# MEDIA
# -------------------------
class MediaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Media

    review = factory.SubFactory(ReviewFactory)

    # evita problemas con ImageField en tests
    image = factory.django.ImageField(color='blue')


# -------------------------
# FAVORITE ITEM
# -------------------------
class FavoriteItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FavoriteItem

    game = factory.SubFactory(GameFactory)
    user = factory.SubFactory(UserFactory)

    order = factory.Sequence(lambda n: n)
