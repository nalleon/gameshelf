from django.conf import settings
from django.db import models
from shared.models import SoftDeleteModel
from django.utils.text import slugify

class Game(SoftDeleteModel):
    title = models.CharField()
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    cover_default = models.URLField(null=True, blank=True)
    cover_detail = models.URLField(null=True, blank=True)

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
    
    age_rating = models.CharField(max_length=10, blank=True, null=True, default='TBA')
    mature_content = models.BooleanField(default=True)

    def __str__(self):
        return f'Game(id={self.pk}, title="{self.title}", slug="{self.slug}", released_at="{self.released_at}", rating="{self.region} - {self.age_rating}", mature_content="{self.mature_content}"'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            
            slug = base_slug
            if Game.objects.filter(slug=slug).exists():
                year = self.released_at.year if self.released_at else ''
                slug_candidate = f"{base_slug}-{year}" if year else base_slug

                counter = 1
                slug = slug_candidate
                while Game.objects.filter(slug=slug).exists():
                    slug = f"{slug_candidate}-{counter}"
                    counter += 1

            self.slug = slug

        super().save(*args, **kwargs)
        
    class Meta:
        unique_together = ['title', 'released_at', 'edition', 'region']

    
class Review(SoftDeleteModel):
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


class Media(SoftDeleteModel):
    image = models.ImageField(
        upload_to='reviews/', default='reviews/default.png', null=True, blank=True
    )
    review = models.ForeignKey('games.Review', related_name='medias', on_delete=models.CASCADE)

    def __str__(self):
        return f'Media(id={self.pk}, image="{self.content}", review="{self.review}")'


class FavoriteItem(SoftDeleteModel):
    game = models.ForeignKey('games.Game', related_name='favorites', on_delete=models.CASCADE)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='favorites', on_delete=models.CASCADE
    )

    def __str__(self):
        return f'FavoriteItem(id={self.pk}, game="{self.game}", user="{self.user}")'
