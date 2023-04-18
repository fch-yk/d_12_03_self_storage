from django.contrib import admin

from storage.models import Storage, Image, Box


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    pass


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass


