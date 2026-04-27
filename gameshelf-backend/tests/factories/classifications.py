import factory
from faker import Faker

from classifications.models import (
    Edition, Region, Genre, Developer, Publisher, Platform
)

fake = Faker()


class EditionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Edition

    name = factory.Sequence(lambda n: f'Edition {n}')
    description = factory.LazyFunction(lambda: fake.text(max_nb_chars=160))


class RegionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Region

    name = factory.Sequence(lambda n: f'Region {n}')
    igdb_id = factory.Sequence(lambda n: n + 1000)
    rating_organization = factory.Iterator(
        ['PEGI', 'ESRB', 'CERO', 'USK', 'GRAC', 'CLASS_IND', 'ACB', 'IARC']
    )
    acronym = '' 


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre

    name = factory.Sequence(lambda n: f'Action Adventure {n}')
    acronym = None


class DeveloperFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Developer

    name = factory.Sequence(lambda n: f'Dev Studio {n}')


class PublisherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Publisher

    name = factory.Sequence(lambda n: f'Publisher {n}')


class PlatformFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Platform

    name = factory.Sequence(lambda n: f'PlayStation {n}')