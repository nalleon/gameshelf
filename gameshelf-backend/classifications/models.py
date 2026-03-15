from django.db import models
from django.utils.text import slugify
from shared.models import SoftDeleteModel
from django.db.models import Q

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
    icon = models.ImageField(upload_to='regions/', default='regions/default.png', null=True, blank=True)



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
    pass

class PlatformSlugAlias(SoftDeleteModel):
    platform = models.ForeignKey(
        Platform,
        on_delete=models.CASCADE,
        related_name='slug_aliases'
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug