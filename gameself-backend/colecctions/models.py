from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Item(models.Model):
    class Type(models.TextChoices):
        PHYSICAL = 'P', 'Physical'
        DIGITAL = 'D', 'Digital'

    type = models.CharField(max_length=1, choices=Type, default=Type.DIGITAL)

    game = models.ForeignKey(
        'games.Game',
        related_name='collections',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    region = models.ForeignKey(
        'classifications.Region',
        related_name='regions',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    edition = models.ForeignKey(
        'classifications.Edition',
        related_name='editions',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='wishlist', on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Item(id={self.pk}, created_at="{self.created_at}"'


class CollectionItem(Item):
    pass


class WishListItem(Item):
    DEFAULT_PRIORITY = 5

    priority = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=DEFAULT_PRIORITY,
    )

    annotation = models.CharField(max_length=100)

    def __str__(self):
        return f'WishListItem(id={self.pk})'
