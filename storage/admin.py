import logging

import requests
from django.contrib import admin

from storage.models import Box, Image, Order, Storage
from geo.models import Location

logger = logging.getLogger(__file__)


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    def response_add(self, request, obj):
        try:
            Location.save_location(obj.address)
        except requests.ConnectionError:
            logger.warning(
                'Connection error. Location for storage %s was not saved',
                obj
            )
        return super().response_add(request, obj)

    def response_change(self, request, obj):
        try:
            Location.save_location(obj.address)
        except requests.ConnectionError:
            logger.warning(
                'Connection error. Location for storage %s was not saved',
                obj
            )
        return super().response_change(request, obj)


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'box', 'start_order', 'end_order']
