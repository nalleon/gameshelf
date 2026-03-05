from django.db import models
from django.utils.text import slugify

class Classification(models.Model):
    name = models.CharField(unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=160)

    def __str__(self):
        return f'PK="{self.pk}", name="{self.name}", slug="{self.clean_fieldsslug}" description="{self.description}"'
    
    class Meta:
        abstract = True
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Edition(Classification):
    pass

class Region(Classification):
    description = None
    acronym = models.CharField(max_length=2)
    icon = models.ImageField(upload_to='regions/', default='regions/default.png', null=True, blank=True)

class Genre(Classification):
    pass


class Developer(Classification):
    pass


class Publisher(Classification):
    pass


class Platform(Classification):
    pass

class PlatformSlugAlias(models.Model):
    platform = models.ForeignKey(
        Platform,
        on_delete=models.CASCADE,
        related_name='slug_aliases'
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug