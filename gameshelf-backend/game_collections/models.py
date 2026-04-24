from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from shared.models import SoftDeleteModel
from django.db.models.functions import Lower


class Item(SoftDeleteModel):
    class Type(models.TextChoices):
        PHYSICAL = 'P', 'Physical'
        DIGITAL = 'D', 'Digital'

    type = models.CharField(max_length=1, choices=Type, default=Type.DIGITAL)
    
    platform = models.ForeignKey(
        'classifications.Platform',
        on_delete=models.CASCADE
    )
    
    is_private = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

class Collection(SoftDeleteModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='collections',
        on_delete=models.CASCADE,
    )

    name = models.CharField(max_length=100, default='My Collection')
    
    is_private = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('name'),
                'user',
                condition=models.Q(deleted_at__isnull=True),
                name='unique_collection_name_per_user_ci'
            )
        ]


class CollectionItem(Item):
    is_private = models.BooleanField(default=False)

    collection = models.ForeignKey(
        Collection,
        related_name='items',
        on_delete=models.CASCADE,
    )
    
    game = models.ForeignKey(
        'games.Game',
        related_name='collection_items',
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['collection', 'game', 'type'],
                condition=models.Q(deleted_at__isnull=True),
                name='unique_game_per_collection_and_type'
            )
        ]


class Wishlist(SoftDeleteModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='wishlist',
        on_delete=models.CASCADE,
    )
    
    name = models.CharField(max_length=100, default='My Wishlist')
    
    is_private = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

class WishListItem(Item):
    priority = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5,
    )
    
    annotation = models.CharField(max_length=100, null=True, blank=True)
    
    is_private = models.BooleanField(default=False)

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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['wishlist', 'game', 'type'],
                condition=models.Q(deleted_at__isnull=True),
                name='unique_game_per_wishlist_and_type'
            )
        ]