from rest_framework import serializers

from mylogs.models import LogEntry


class LogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntry
        fields = ["id", "beleg", "created_at", "username", "payload"]
        read_only_fields = ["id", "created_at", "payload"]
