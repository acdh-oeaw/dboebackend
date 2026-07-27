import json

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from mylogs.models import LogEntry


@extend_schema_field(serializers.JSONField)
class TextBackedJSONField(serializers.JSONField):
    def to_representation(self, value):
        if value in (None, ""):
            return None
        if isinstance(value, (dict, list, int, float, bool)):
            return value
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            return value


class LogEntrySerializer(serializers.ModelSerializer):
    payload = TextBackedJSONField(read_only=True)

    class Meta:
        model = LogEntry
        fields = ["id", "beleg", "created_at", "username", "payload"]
        read_only_fields = ["id", "created_at", "payload"]
