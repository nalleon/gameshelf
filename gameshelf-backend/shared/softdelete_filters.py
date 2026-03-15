from django.contrib import admin


class SoftDeletedFilter(admin.SimpleListFilter):
    title = 'deleted status'
    parameter_name = 'deleted'

    def lookups(self, request, model_admin):
        return (
            ('active', 'Active'),
            ('deleted', 'Deleted'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'deleted':
            return queryset.filter(deleted_at__isnull=False)

        if self.value() == 'active':
            return queryset.filter(deleted_at__isnull=True)

        return queryset