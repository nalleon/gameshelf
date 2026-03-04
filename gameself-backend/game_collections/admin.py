from django.contrib import admin

from .models import CollectionItem, WishListItem

@admin.register(CollectionItem)
class CollectionItemAdmin(admin.ModelAdmin):
    pass

@admin.register(WishListItem)
class WishListItemAdmin(admin.ModelAdmin):
    pass

