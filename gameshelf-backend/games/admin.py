from django.contrib import admin

from .models import Game, Review, Media, FavoriteItem


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    pass

@admin.register(FavoriteItem)
class FavoriteItemAdmin(admin.ModelAdmin):
    pass

