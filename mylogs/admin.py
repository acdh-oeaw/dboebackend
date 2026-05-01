from django.contrib import admin

from mylogs.models import LogEntry


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ["beleg", "username", "created_at"]
    list_filter = ["username"]
    autocomplete_fields = ["beleg"]
