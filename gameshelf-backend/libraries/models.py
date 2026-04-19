from django.conf import settings
from django.db import models

from shared.models import SoftDeleteModel

class Library(SoftDeleteModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='library',
        on_delete=models.CASCADE
    )

    is_private = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user}'s Library ({'Private' if self.is_private else 'Public'})"

class LibraryItem(SoftDeleteModel):
    class Status(models.TextChoices):
        COMPLETED = 'CMP', 'Completed'
        PLAYING = 'PLY', 'Playing'
        PAUSED = 'PSD', 'Paused'
        DROPPED = 'DRP', 'Dropped'
        PLANNING = 'PLN', 'Planning'

    library = models.ForeignKey(
        Library,
        related_name='items',
        on_delete=models.CASCADE
    )

    game = models.ForeignKey(
        'games.Game',
        related_name='library_items',
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=3,
        choices=Status.choices,
        default=Status.PLANNING
    )

    is_private = models.BooleanField(default=False)

    hours_played = models.DecimalField(
        decimal_places=1,
        max_digits=6,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['library', 'game'],
                condition=models.Q(deleted_at__isnull=True),
                name='unique_game_per_library'
            )
        ]