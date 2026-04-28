import factory
from factory import fuzzy

from games.models import FavoriteItem, Game, Media, Review


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game
        django_get_or_create = ('title', 'released_at', 'region')

    igdb_id = factory.Sequence(lambda n: 1000 + n)
    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('paragraph')
    cover_default = factory.Faker('image_url')
    cover_detail = factory.Faker('image_url')
    released_at = factory.Faker('date_object')

    parent_game_igdb = None
    region = factory.SubFactory('apps.classifications.factories.RegionFactory')

    age_rating = fuzzy.FuzzyChoice(['E', 'T', 'M', 'PEGI 12', 'PEGI 18'])
    mature_content = factory.Faker('boolean')

    @factory.post_generation
    def platforms(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for platform in extracted:
                self.platforms.add(platform)

    @factory.post_generation
    def genres(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for genre in extracted:
                self.genres.add(genre)

    @factory.post_generation
    def developers(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for developer in extracted:
                self.developers.add(developer)

    @factory.post_generation
    def publishers(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for publisher in extracted:
                self.publishers.add(publisher)


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    content = factory.Faker('text')
    recommend = factory.Faker('boolean')
    game = factory.SubFactory(GameFactory)
    author = factory.SubFactory('apps.users.factories.UserFactory')


class MediaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Media

    review = factory.SubFactory(ReviewFactory)
    image = factory.django.ImageField(color='blue')


class FavoriteItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FavoriteItem

    game = factory.SubFactory(GameFactory)
    user = factory.SubFactory('apps.users.factories.UserFactory')
    order = factory.Sequence(lambda n: n)
