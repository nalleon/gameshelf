import re

from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.text import slugify

from shared.models import SoftDeleteModel


class Classification(SoftDeleteModel):
    name = models.CharField()
    slug = models.SlugField()
    description = models.TextField(max_length=160)

    def __str__(self):
        return f'PK="{self.pk}", name="{self.name}", slug="{self.slug}" description="{self.description}"'

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['slug'],
                condition=Q(deleted_at__isnull=True),
                name='%(app_label)s_%(class)s_unique_active_slug',
            ),
            models.UniqueConstraint(
                fields=['name'],
                condition=Q(deleted_at__isnull=True),
                name='%(app_label)s_%(class)s_unique_active_name',
            ),
        ]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Edition(Classification):
    pass


class Region(Classification):
    description = None
    acronym = models.CharField(max_length=2)
    icon = models.ImageField(
        upload_to='regions/', default='regions/default.png', null=True, blank=True
    )


class Genre(Classification):
    acronym = models.CharField(max_length=10, null=True, blank=True)

    def generate_acronym(self):
        words = self.name.split()
        return ''.join(word[0].upper() for word in words if word)

    def save(self, *args, **kwargs):
        new_slug = slugify(self.name)
        if self.slug != new_slug:
            self.slug = new_slug

        if not self.acronym:
            self.acronym = self.generate_acronym()

        super().save(*args, **kwargs)


class Developer(Classification):
    pass


class Publisher(Classification):
    pass


class Platform(Classification):
    def generate_aliases(self):
        name = self.name.lower()

        aliases = set()

        compact = re.sub(r'[\s\-]+', '', name)
        aliases.add(compact)

        words = re.split(r'[\s\-]+', name)
        acronym = ''.join(word[0] for word in words if word)
        aliases.add(acronym)

        number_match = re.search(r'\d+', name)
        if number_match:
            number = number_match.group()
            if words:
                aliases.add(words[0][0] + number)

        return aliases


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        aliases = self.generate_aliases()

        self.slug_aliases.filter(deleted_at__isnull=True).update(deleted_at=timezone.now())

        for alias in aliases:
            PlatformSlugAlias.objects.get_or_create(
                platform=self,
                slug=alias,
            )


class PlatformSlugAlias(SoftDeleteModel):
    platform = models.ForeignKey(
        'Platform',
        on_delete=models.CASCADE,
        related_name='slug_aliases',
    )

    slug = models.SlugField()

    def __str__(self):
        return f'PK="{self.pk}", slug="{self.slug}", platform="{self.platform.name} - {self.platform.pk}"'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['slug'],
                condition=Q(deleted_at__isnull=True),
                name='%(app_label)s_%(class)s_unique_active_slug',
            )
        ]
