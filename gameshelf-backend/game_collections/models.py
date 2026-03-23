from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from shared.models import SoftDeleteModel


class Item(SoftDeleteModel):
    class Type(models.TextChoices):
        PHYSICAL = 'P', 'Physical'
        DIGITAL = 'D', 'Digital'

    type = models.CharField(max_length=1, choices=Type, default=Type.DIGITAL)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

class Collection(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='collections',
        on_delete=models.CASCADE,
    )

    name = models.CharField(max_length=100, default='My Collection')
    created_at = models.DateTimeField(auto_now_add=True)
    

class CollectionItem(Item): 
    collection = models.ForeignKey(
        Collection,
        related_name='items',
        on_delete=models.CASCADE,
    )
    
    game = models.ForeignKey(
        'games.Game',
        related_name='collection_items',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )


class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='wishlists',
        on_delete=models.CASCADE,
    )

    name = models.CharField(max_length=100, default='My Wishlist')
    created_at = models.DateTimeField(auto_now_add=True)

class WishListItem(Item):
    priority = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5,
    )
    
    annotation = models.CharField(max_length=100, null=True, blank=True)

    game = models.ForeignKey(
        'games.Game',
        related_name='wishlist_items',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    
    wishlist = models.ForeignKey(
        Wishlist,
        related_name='items',
        on_delete=models.CASCADE,
    )

