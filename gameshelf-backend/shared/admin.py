from django.contrib import admin
from .softdelete_filters import SoftDeletedFilter


@admin.action(description='Restore selected items')
def restore_items(modeladmin, request, queryset):
    """
    Restore soft-deleted items by setting deleted_at to None
    """
    queryset.update(deleted_at=None)


@admin.action(description='Permanently delete selected items (hard delete)')
def hard_delete_items(modeladmin, request, queryset):
    """
    Permanently delete records from the database
    """
    for obj in queryset:
        obj.hard_delete()


class SoftDeleteAdmin(admin.ModelAdmin):
    """
    Base admin class for models using SoftDeleteModel
    """

    list_filter = (SoftDeletedFilter,)
    actions = [restore_items, hard_delete_items]

    def get_queryset(self, request):
        """
        Show both active and deleted records in Django admin
        """
        return self.model.all_objects.all()