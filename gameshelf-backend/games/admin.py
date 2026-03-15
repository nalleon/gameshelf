from django.contrib import admin

from .models import Game, Review, Media, FavoriteItem
from shared.admin import SoftDeleteAdmin


@admin.register(Game)
class GameAdmin(SoftDeleteAdmin):
    pass

@admin.register(Review)
class ReviewAdmin(SoftDeleteAdmin):
    pass

@admin.register(Media)
class MediaAdmin(SoftDeleteAdmin):
    pass

@admin.register(FavoriteItem)
class FavoriteItemAdmin(SoftDeleteAdmin):
    pass

