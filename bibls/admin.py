from django.contrib import admin

from bibls.models import BibliographicItem, BibliographicType


@admin.register(BibliographicType)
class BibliographicTypeAdmin(admin.ModelAdmin):
    list_display = ["main_type", "sub_type", "specification"]
    list_filter = ["main_type"]


@admin.register(BibliographicItem)
class BibliographicItemAdmin(admin.ModelAdmin):
    list_display = ["sigle", "short_title", "place", "bibl_type"]
    search_fields = ["short_title"]
    list_filter = ["bibl_type", "place"]
