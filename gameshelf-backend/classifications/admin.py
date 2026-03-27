from django.contrib import admin
from shared.admin import SoftDeleteAdmin
from .models import Edition, Region, Genre, Developer, Publisher, Platform


@admin.register(Edition)
class EditionAdmin(SoftDeleteAdmin):
    pass

@admin.register(Region)
class RegionAdmin(SoftDeleteAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(SoftDeleteAdmin):
    pass


@admin.register(Developer)
class DeveloperAdmin(SoftDeleteAdmin):
    pass


@admin.register(Publisher)
class PublisherAdmin(SoftDeleteAdmin):
    pass


@admin.register(Platform)
class PlatformAdmin(SoftDeleteAdmin):
    pass