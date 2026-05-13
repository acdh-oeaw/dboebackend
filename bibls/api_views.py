from django.conf import settings
from django.db import reset_queries
from rest_framework import viewsets

from belege.api_views import CustomPagination
from belege.query_utils import log_query_count
from bibls.models import BibliographicItem, BibliographicType
from bibls.serializers import BibliographicItemSerializer, BibliographicTypeSerializer


class BibliographicItemViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    queryset = BibliographicItem.objects.select_related("bibl_type")
    serializer_class = BibliographicItemSerializer

    def list(self, request, *args, **kwargs):
        reset_queries()
        response = super().list(request, *args, **kwargs)
        if settings.DEBUG:
            log_query_count(full_log=False)
        return response


class BibliographicTypeViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    queryset = BibliographicType.objects.all()
    serializer_class = BibliographicTypeSerializer
