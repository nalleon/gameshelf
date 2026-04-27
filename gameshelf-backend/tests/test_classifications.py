import pytest
from django.utils import timezone

from classifications.models import PlatformSlugAlias
from tests.factories.classifications import GenreFactory, PlatformFactory, RegionFactory


@pytest.mark.django_db
def test_slug_is_generated():
    genre = GenreFactory(name='Action RPG')

    assert genre.slug == 'action-rpg'


@pytest.mark.django_db
def test_slug_is_stable():
    genre = GenreFactory(name='Action RPG')

    genre.name = 'Action RPG Updated'
    genre.save()

    assert genre.slug == 'action-rpg-updated'


@pytest.mark.django_db
def test_genre_str():
    genre = GenreFactory(name='Action RPG')

    assert str(genre) == f'PK="{genre.pk}", name="Action RPG", slug="action-rpg"'


@pytest.mark.django_db
def test_genre_str_contains_fields():
    genre = GenreFactory(name='Action RPG')

    s = str(genre)

    assert str(genre.pk) in s
    assert 'Action RPG' in s
    assert genre.slug in s

#Revisar
@pytest.mark.django_db
def test_slug_uniqueness_increment():
    g1 = GenreFactory(name='Action RPG')
    g2 = GenreFactory(name='Action RPG 2') 

    g2.slug = g1.slug
    g2.save()

    assert g2.slug == 'action-rpg-2'


@pytest.mark.django_db
def test_genre_acronym_generated():
    genre = GenreFactory(name='Action Role Playing')

    assert genre.acronym == 'ARP'


@pytest.mark.django_db
def test_region_acronym_generated_from_name():
    region = RegionFactory(name='north_america', acronym='')

    assert region.acronym == 'NA'


@pytest.mark.django_db
def test_region_acronym_fallback():
    region = RegionFactory(name='Spain', acronym='')

    assert region.acronym == 'SP'


@pytest.mark.django_db
def test_platform_aliases_created():
    platform = PlatformFactory(name='PlayStation 5')

    aliases = PlatformSlugAlias.objects.filter(platform=platform)

    slugs = {a.slug for a in aliases}

    assert 'playstation5' in slugs
    assert 'ps5' in slugs or 'p5' in slugs


@pytest.mark.django_db
def test_unique_name_ignores_soft_deleted():
    genre1 = GenreFactory(name='Strategy')

    genre1.deleted_at = timezone.now()
    genre1.save()

    genre2 = GenreFactory(name='Strategy')

    assert genre2.pk is not None


@pytest.mark.django_db
def test_slug_updates_when_name_changes():
    genre = GenreFactory(name='Action')

    genre.name = 'Action RPG'
    genre.save()

    assert genre.slug == 'action-rpg'


@pytest.mark.django_db
def test_platform_aliases_are_replaced():
    platform = PlatformFactory(name='PlayStation 4')

    # initial_aliases = platform.slug_aliases.count()

    platform.name = 'PlayStation 5'
    platform.save()

    assert platform.slug_aliases.filter(deleted_at__isnull=True).count() > 0


@pytest.mark.django_db
def test_platform_slug_alias_str():
    platform = PlatformFactory(name='PlayStation 5')

    alias = platform.slug_aliases.first()

    assert str(alias) == (
        f'PK="{alias.pk}", slug="{alias.slug}", platform="{platform.name} - {platform.pk}"'
    )


@pytest.mark.django_db
def test_platform_slug_alias_str_contains_data():
    platform = PlatformFactory(name='PlayStation 5')

    alias = platform.slug_aliases.first()
    s = str(alias)

    assert str(alias.pk) in s
    assert alias.slug in s
    assert platform.name in s


@pytest.mark.django_db
def test_aliases_platform_aliases_are_replaced():
    platform = PlatformFactory(name='PlayStation 5')

    old_ids = set(platform.slug_aliases.values_list('id', flat=True))

    platform.name = 'PlayStation 6'
    platform.save()

    old_aliases = PlatformSlugAlias.all_objects.filter(id__in=old_ids)

    assert old_aliases.count() > 0
    assert all(a.deleted_at is not None for a in old_aliases)

    assert platform.slug_aliases.filter(slug='playstation6').exists()


@pytest.mark.django_db
def test_platform_aliases_do_not_duplicate():
    platform = PlatformFactory(name='PlayStation 5')

    aliases = list(platform.slug_aliases.all())

    assert len(aliases) == len(set(a.slug for a in aliases))
