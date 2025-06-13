from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from belege.api_utils import get_filterset_for_model
from belege.serializers import get_serializer_for_model
from belege.models import BundesLand, GRegion, KRegion, Ort, Beleg, Citation


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20


class CustomViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPagination

    def get_serializer_class(self):
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


class CitationViewSet(CustomViewSet):
    queryset = Citation.objects.all()
    filterset_class = get_filterset_for_model(Citation)
