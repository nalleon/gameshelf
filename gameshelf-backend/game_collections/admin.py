from django.contrib import admin

from .models import CollectionItem, WishListItem, Collection, Wishlist
from shared.admin import SoftDeleteAdmin

@admin.register(Collection)
class CollectionAdmin(SoftDeleteAdmin):
    pass
@admin.register(CollectionItem)
class CollectionItemAdmin(SoftDeleteAdmin):
    pass

@admin.register(Wishlist)
class WishlistAdmin(SoftDeleteAdmin):
    pass

@admin.register(WishListItem)
class WishListItemAdmin(SoftDeleteAdmin):
    pass

