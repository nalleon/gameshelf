from django.conf import settings
from django.db import models


class LibraryItem(models.Model):
    class Status(models.TextChoices):
        COMPLETED = 'Completed'
        PLAYING = 'Physical'
        PAUSED = 'Paused'
        DROPPED = 'Dropped'
        PLANNING = 'Planning'

    status = models.CharField(choices=Status, default=Status.PLANNING)

    game = models.ForeignKey(
        'games.Game',
        related_name='in_library',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    hours_played = models.DecimalField(decimal_places=1, max_digits=6, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='wishlist', on_delete=models.CASCADE
    )

    def __str__(self):
        return f'LibraryItem(id={self.pk}, created_at="{self.created_at}"'
