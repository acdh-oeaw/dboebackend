from rest_framework import mixins, viewsets

from belege.api_utils import get_filterset_for_model
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
    filterset_fields = filterset_class = get_filterset_for_model(
        LogEntry, fields=["beleg"]
    )
    http_method_names = ["get", "post"]
