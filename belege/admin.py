from django.contrib import admin
from django.db import models

from belege.models import (
    Annotation,
    Beleg,
    Citation,
    Lautung,
    LehnWort,
    Sense,
    ZusatzLemma,
)


@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ["kontext", "tool", "created_at", "updated_at"]
    search_fields = ["kontext__dboe_id", "tool"]
    autocomplete_fields = ["kontext"]
    ordering = ["kontext", "created_at"]
    list_per_page = 20


@admin.register(LehnWort)
class LehnWortAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in LehnWort._meta.fields
        if isinstance(
            field,
            (
                models.CharField,
                models.TextField,
                models.ForeignKey,
                models.PositiveIntegerField,
            ),
        )
    ]
    autocomplete_fields = ["beleg"]
    ordering = ["beleg", "number"]
    list_per_page = 20


@admin.register(ZusatzLemma)
class ZusatzLemmaAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in ZusatzLemma._meta.fields
        if isinstance(
            field,
            (
                models.CharField,
                models.TextField,
                models.ForeignKey,
                models.PositiveIntegerField,
            ),
        )
    ]
    search_fields = [
        field.name
        for field in ZusatzLemma._meta.fields
        if isinstance(field, (models.CharField, models.TextField))
    ]
    autocomplete_fields = ["citation"]
    ordering = ["citation", "number"]
    list_per_page = 20


@admin.register(Sense)
class SenseAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in Sense._meta.fields
        if isinstance(
            field,
            (
                models.CharField,
                models.TextField,
                models.ForeignKey,
                models.PositiveIntegerField,
            ),
        )
    ]
    search_fields = [
        field.name
        for field in Sense._meta.fields
        if isinstance(field, (models.CharField, models.TextField))
    ]
    autocomplete_fields = ["beleg"]
    ordering = ["beleg", "number"]
    list_per_page = 20


@admin.register(Lautung)
class LautungAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in Lautung._meta.fields
        if isinstance(
            field,
            (
                models.CharField,
                models.TextField,
                models.ForeignKey,
                models.PositiveIntegerField,
            ),
        )
    ]
    search_fields = [
        field.name
        for field in Lautung._meta.fields
        if isinstance(field, (models.CharField, models.TextField))
    ]
    autocomplete_fields = ["beleg"]
    ordering = ["beleg", "number"]
    list_per_page = 20


@admin.register(Beleg)
class BelegAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in Beleg._meta.fields
        if isinstance(
            field,
            (
                models.CharField,
                models.TextField,
                models.ForeignKey,
                models.PositiveIntegerField,
                models.BooleanField,
            ),
        )
    ]
    search_fields = [
        field.name
        for field in Beleg._meta.fields
        if isinstance(field, (models.CharField, models.TextField))
    ]
    list_filter = [
        "import_issue",
        "pos",
        "has_internal_comment",
    ]
    ordering = ["dboe_id"]
    autocomplete_fields = ["tag", "collection"]
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
    ] + ["beleg__dboe_id"]
    ordering = ["beleg", "number"]
    autocomplete_fields = ["beleg"]
    list_per_page = 20
