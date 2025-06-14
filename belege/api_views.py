from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from belege.api_utils import get_filterset_for_model
from belege.serializers import get_serializer_for_model, CitationSerializer
from belege.models import BundesLand, GRegion, KRegion, Ort, Beleg, Citation


class CustomPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 20
    page_size_query_param = "page_size"


class CustomViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.serializer_class:
            return self.serializer_class
        else:
            return get_serializer_for_model(self.queryset.model)


class BundesLandViewSet(CustomViewSet):
    queryset = BundesLand.objects.all()
    filterset_class = get_filterset_for_model(BundesLand)


class GRegionViewSet(CustomViewSet):
    queryset = GRegion.objects.all()
    filterset_class = get_filterset_for_model(GRegion)


class KRegionViewSet(CustomViewSet):
    queryset = KRegion.objects.all()
    filterset_class = get_filterset_for_model(KRegion)


class OrtViewSet(CustomViewSet):
    queryset = Ort.objects.all()
    filterset_class = get_filterset_for_model(Ort)


class BelegViewSet(CustomViewSet):
    queryset = Beleg.objects.all()
    filterset_class = get_filterset_for_model(Beleg)


class CitationViewSet(viewsets.ModelViewSet):
    page_size = 10
    max_page_size = 20
    page_size_query_param = "page_size"
    pagination_class = CustomPagination
    queryset = Citation.objects.all()
    filterset_class = get_filterset_for_model(Citation)
    serializer_class = CitationSerializer
    lookup_field = "dboe_id"
    lookup_value_regex = r'[^/]+'  # the default regex does not work with dboe_ids due to e.g. `.`
