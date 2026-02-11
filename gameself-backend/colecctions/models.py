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
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True



class CollectionItem(Item):
    game = models.ForeignKey(
        'games.Game',
        related_name='collection_items',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='collection',
        on_delete=models.CASCADE,
    )



class WishListItem(Item):
    priority = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5,
    )
    
    annotation = models.CharField(max_length=100)

    game = models.ForeignKey(
        'games.Game',
        related_name='wishlist_items',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='wishlist',
        on_delete=models.CASCADE,
    )

