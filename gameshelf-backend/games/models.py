from django.conf import settings
from django.db import models


class Game(models.Model):
    title = models.CharField()
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)

    cover = models.ImageField(
        upload_to='games/covers/', default='games/covers/default.png', null=True, blank=True
    )

    released_at = models.DateField()

    platforms = models.ManyToManyField('classifications.Platform', related_name='games')
    genres = models.ManyToManyField('classifications.Genre', related_name='games')
    developers = models.ManyToManyField('classifications.Developer', related_name='games')
    publishers = models.ManyToManyField('classifications.Publisher', related_name='games')
    
    edition = models.ForeignKey(
        'classifications.Edition',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    
    region = models.ForeignKey(
        'classifications.Region',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    
    def __str__(self):
        return f'Game(id={self.pk}, title="{self.title}", slug="{self.slug}", released_at="{self.released_at}"'

    class Meta:
        unique_together = ['title', 'released_at', 'edition', 'region']


class Review(models.Model):
    content = models.TextField()

    recommend = models.BooleanField()

    game = models.ForeignKey('games.Game', related_name='reviews', on_delete=models.CASCADE)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='reviews', on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f'Review(id={self.pk}, '
            f'content="{self.content}", '
            f'game="{self.game}", '
            f'author="{self.author}"'
        )


class Media(models.Model):
    image = models.ImageField(
        upload_to='reviews/', default='reviews/default.png', null=True, blank=True
    )
    review = models.ForeignKey('games.Review', related_name='medias', on_delete=models.CASCADE)

    def __str__(self):
        return f'Media(id={self.pk}, image="{self.content}", review="{self.review}")'


class FavoriteItem(models.Model):
    game = models.ForeignKey('games.Game', related_name='favorites', on_delete=models.CASCADE)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='favorites', on_delete=models.CASCADE
    )

    def __str__(self):
        return f'FavoriteItem(id={self.pk}, game="{self.game}", user="{self.user}")'
