from django.contrib import admin
from shared.admin import SoftDeleteAdmin

from .models import LibraryItem

@admin.register(LibraryItem)
class LibraryAdmin(SoftDeleteAdmin):
    pass


