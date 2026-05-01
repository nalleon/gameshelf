import re

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import Classification, Genre, Platform, PlatformSlugAlias, Region


def generate_genre_acronym(name: str) -> str:
    name = name.strip()

    words = re.findall(r'[a-z0-9]+', name.lower())

    if len(words) > 1:
        return ''.join(w[0] for w in words).upper()

    word = words[0]

    if len(word) <= 4:
        return word[:3].ljust(3, word[-1]).upper()

    return word[:3].upper()


def generate_aliases(name: str) -> set:
    name = name.lower()

    aliases = set()

    compact = re.sub(r'[^a-z0-9]+', '', name)
    aliases.add(compact)

    words = re.findall(r'[a-z0-9]+', name)

    acronym = ''.join(word[0] for word in words if word)
    aliases.add(acronym)

    number_match = re.search(r'\d+', name)
    if number_match:
        number = number_match.group()
        if words:
            aliases.add(words[0][0] + number)

    return aliases


@receiver(pre_save, sender=Classification)
def set_slug(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.name)
        slug = base_slug

        counter = 1
        Model = sender

        while Model.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1

        instance.slug = slug


@receiver(post_save, sender=Platform)
def create_platform_aliases(sender, instance, created, **kwargs):
    if not created:
        return

    aliases = generate_aliases(instance.name)

    existing = set(
        PlatformSlugAlias.objects.filter(slug__in=aliases).values_list('slug', flat=True)
    )

    new_aliases = [
        PlatformSlugAlias(platform=instance, slug=alias)
        for alias in aliases
        if alias not in existing
    ]

    PlatformSlugAlias.objects.bulk_create(new_aliases)


@receiver(post_save, sender=Region)
def set_region_acronym(sender, instance, created, **kwargs):
    if instance.acronym:
        return

    name_upper = instance.name.upper()

    if '_' in name_upper:
        parts = name_upper.split('_')
        acronym = ''.join(p[0] for p in parts if p)
    else:
        acronym = name_upper[:2]

    Region.objects.filter(pk=instance.pk).update(acronym=acronym)



@receiver(post_save, sender=Genre)
def set_genre_acronym(sender, instance, created, **kwargs):
    if instance.acronym:
        return

    acronym = generate_genre_acronym(instance.name)

    Genre.objects.filter(pk=instance.pk).update(
        acronym=acronym
    )