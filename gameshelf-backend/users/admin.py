from django.contrib import admin

from .models import Profile
from shared.admin import SoftDeleteAdmin


@admin.register(Profile)
class ProfileAdmin(SoftDeleteAdmin):
    pass

