import re

from django.db import IntegrityError, models
from django.db.models import Q
from django.utils.text import slugify

from shared.models import SoftDeleteModel


class Classification(SoftDeleteModel):
    name = models.CharField()
    slug = models.SlugField()

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
        if not self.slug:
            base_slug = slugify(self.name)

            base_slug = base_slug.replace('(', '').replace(')', '')

            slug = base_slug
            counter = 1

            Model = self.__class__

            while Model.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1

            self.slug = slug
            
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
            ('IARC', 'IARC'),
        ],
        blank=True,
        null=True,
    )

class Genre(Classification):
    acronym = models.CharField(max_length=10, null=True, blank=True)


class Developer(Classification):
    pass


class Publisher(Classification):
    pass


class Platform(Classification):
    pass



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
