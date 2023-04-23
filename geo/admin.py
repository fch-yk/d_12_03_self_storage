from django.contrib import admin

from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'changed_at', ]
    readonly_fields = ['id', 'changed_at', ]
