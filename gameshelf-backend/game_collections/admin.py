from django.contrib import admin

from .models import CollectionItem, WishListItem
from shared.admin import SoftDeleteAdmin

@admin.register(CollectionItem)
class CollectionItemAdmin(SoftDeleteAdmin):
    pass

@admin.register(WishListItem)
class WishListItemAdmin(SoftDeleteAdmin):
    pass

