from django.contrib import admin
from belege.models import Beleg, Citation
from django.db import models


@admin.register(Beleg)
class BelegAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in Beleg._meta.fields
        if isinstance(field, (models.CharField, models.TextField))
    ]
    search_fields = [
        field.name
        for field in Beleg._meta.fields
        if isinstance(field, (models.CharField, models.TextField))
    ]
    search_fields = ['dboe_id', 'hauptlemma']  # Fields to search in autocomplete
    ordering = ['dboe_id']


@admin.register(Citation)
class CitationAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in Citation._meta.fields
        if isinstance(field, (models.CharField, models.TextField, models.PositiveIntegerField))
    ]
    search_fields = [
        field.name
        for field in Citation._meta.fields
        if isinstance(field, (models.CharField, models.TextField))
    ]
    ordering = ["beleg", "number"]
    autocomplete_fields = ['beleg']  # Enable autocomplete for beleg field
