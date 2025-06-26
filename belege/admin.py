from django.contrib import admin
from django.db import models

from belege.models import Beleg, Citation, BundesLand, GRegion, KRegion, Ort, Facsimile


@admin.register(Facsimile)
class FacsimileAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in Facsimile._meta.fields
        if isinstance(field, (models.CharField, models.TextField, models.ForeignKey))
    ]
    search_fields = [
        field.name
        for field in Facsimile._meta.fields
        if isinstance(field, (models.CharField, models.TextField))
    ]
    search_fields = ["file_name"]
    ordering = ["file_name"]
    list_per_page = 20


@admin.register(Beleg)
class BelegAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in Beleg._meta.fields
        if isinstance(field, (models.CharField, models.TextField, models.ForeignKey))
    ]
    search_fields = [
        field.name
        for field in Beleg._meta.fields
        if isinstance(field, (models.CharField, models.TextField))
    ]
    search_fields = ["dboe_id", "hauptlemma"]
    list_filter = ["import_issue", "pos"]
    ordering = ["dboe_id"]
    autocomplete_fields = ["ort", "facsimile"]
    list_per_page = 20


@admin.register(Citation)
class CitationAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in Citation._meta.fields
        if isinstance(
            field, (models.CharField, models.TextField, models.PositiveIntegerField)
        )
    ]
    search_fields = [
        field.name
        for field in Citation._meta.fields
        if isinstance(field, (models.CharField, models.TextField))
    ]
    ordering = ["beleg", "number"]
    autocomplete_fields = ["beleg"]
    list_per_page = 20


@admin.register(BundesLand)
class BundesLandAdmin(admin.ModelAdmin):
    list_display = ["sigle", "abbr", "name", "geonames"]
    search_fields = ["sigle", "abbr", "name"]
    ordering = ["name"]


@admin.register(GRegion)
class GRegionAdmin(admin.ModelAdmin):
    list_display = ["sigle", "abbr", "name", "bundesland"]
    search_fields = ["sigle", "abbr", "name"]
    ordering = ["name"]
    list_filter = ["bundesland"]


@admin.register(KRegion)
class KRegionAdmin(admin.ModelAdmin):
    list_display = ["sigle", "abbr", "name", "bundesland", "gregion", "geonames"]
    search_fields = ["sigle", "abbr", "name"]
    autocomplete_fields = ["bundesland", "gregion"]
    ordering = ["name"]
    list_filter = ["bundesland", "gregion"]


@admin.register(Ort)
class OrtAdmin(admin.ModelAdmin):
    list_display = ["sigle", "name", "bundesland", "gregion", "kregion", "geonames"]
    search_fields = ["sigle", "name"]
    autocomplete_fields = ["bundesland", "gregion", "kregion"]
    ordering = ["name"]
