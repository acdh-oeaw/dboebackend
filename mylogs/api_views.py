from rest_framework import mixins, viewsets

from mylogs.models import LogEntry
from mylogs.serializers import LogEntrySerializer


class LogEntryViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer
    http_method_names = ["get", "post"]
