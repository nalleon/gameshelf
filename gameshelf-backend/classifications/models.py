import re

from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.text import slugify
from django.db import IntegrityError

from shared.models import SoftDeleteModel


class Classification(SoftDeleteModel):
    name = models.CharField(unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'PK="{self.pk}", name="{self.name}", slug="{self.slug}"'

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
    description = models.TextField(max_length=160)


class Region(Classification):
    acronym = models.CharField(max_length=2)
    igdb_id = models.IntegerField(unique=True)
    rating_organization = models.CharField(
        max_length=20,
        choices=[
            ('PEGI', 'PEGI'),
            ('ESRB', 'ESRB'),
            ('CERO', 'CERO'),
            ('USK', 'USK'),
            ('GRAC', 'GRAC'),
            ('CLASS_IND', 'CLASS_IND'),
            ('ACB', 'ACB'),
            ('IARC', 'IARC') 
        ],
        blank=True,
        null=True
    )
    
    def save(self, *args, **kwargs):
        if not self.acronym:
            name_upper = self.name.upper()
            if '_' in name_upper:
                parts = name_upper.split('_')
                self.acronym = ''.join(part[0] for part in parts)
            else:
                self.acronym = self.name[:2].upper()
        super().save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        aliases = self.generate_aliases()

        self.slug_aliases.filter(deleted_at__isnull=True).update(
            deleted_at=timezone.now()
        )

        for alias in aliases:
            try:
                PlatformSlugAlias.objects.get_or_create(
                    platform=self,
                    slug=alias,
                )
            except IntegrityError:
                continue

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
