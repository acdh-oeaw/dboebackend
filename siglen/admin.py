from django.contrib import admin

from siglen.models import BelegSigle, Sigle


class BundeslandFilter(admin.SimpleListFilter):
    title = "Bundesland"
    parameter_name = "bl"

    def lookups(self, request, model_admin):
        return [
            (sigle.pk, str(sigle))
            for sigle in Sigle.objects.filter(kind="bl").order_by("sigle")
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(bl=self.value())
        return queryset


class GrossRegionFilter(admin.SimpleListFilter):
    title = "Großregion"
    parameter_name = "gr"

    def lookups(self, request, model_admin):
        return [
            (sigle.pk, str(sigle))
            for sigle in Sigle.objects.filter(kind="gr").order_by("sigle")
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(gr=self.value())
        return queryset


@admin.register(Sigle)
class SigleAdmin(admin.ModelAdmin):
    list_display = ["sigle", "name", "orig_names", "bl", "gr", "kr", "geonames", "kind"]
    search_fields = ["name", "sigle"]
    list_filter = ["kind", BundeslandFilter, GrossRegionFilter]
    autocomplete_fields = ["bl", "gr", "kr"]
    ordering = ["sigle"]
    list_per_page = 50


@admin.register(BelegSigle)
class BelegSigleAdmin(admin.ModelAdmin):
    list_display = ["beleg", "sigle", "corresp", "resp"]
    search_fields = ["beleg__dboe_id", "sigle__name", "sigle__sigle"]
    autocomplete_fields = ["beleg", "sigle"]
    ordering = ["sigle"]
    list_per_page = 50
