from django.db import models


class Classification(models.Model):
    name = models.TextField(unique=True)
    description = models.TextField(max_length=160)

    def __str__(self):
        return f'PK="{self.pk}", name="{self.name}", description="{self.description}"'


class Edition(Classification):
    pass

class Region(Classification):
    acronym = models.CharField(max_length=2)
    icon = models.ImageField(upload_to='regions', default='regions/default.png', null=True, blank=True)

class Genre(Classification):
    pass


class Developer(Classification):
    pass


class Publisher(Classification):
    pass


class Platform(Classification):
    pass
