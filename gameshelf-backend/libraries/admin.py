from django.contrib import admin

from .models import LibraryItem

@admin.register(LibraryItem)
class LibraryAdmin(admin.ModelAdmin):
    pass


