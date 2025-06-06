from django.contrib import admin
from belege.models import Beleg
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
