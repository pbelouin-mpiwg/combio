from django.contrib import admin
from django.contrib.sites.models import Site

admin.site.unregister(Site)

from combio_app import models


@admin.register(models.Record)
class RecordAdmin(admin.ModelAdmin):
    fields = ("id", "transcript", "metadata", "collection")
    readonly_fields = ("id",)
    list_display = ("id", "title", "collection", "metadata", "transcript")
    list_display_links = ("metadata",)
    search_fields = ("metadata",)


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    fields = ("id", "name")
    readonly_fields = ("id",)
    list_display = ("id", "name")
    list_display_links = ("name",)
    search_fields = ("name",)


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    fields = ("id", "name", "domain")
    readonly_fields = ("id",)
    list_display = ("id", "name", "domain")
    list_display_links = ("name",)
    search_fields = ("name", "domain")
