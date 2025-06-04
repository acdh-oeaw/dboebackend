from rest_framework import viewsets
from rest_framework import pagination, filters
from .serializers import (
    UserListSerializer,
    UserSerializer,
    CategorySerializer,
    CollectionListSerializer,
    TagSerializer,
    LemmaSerializer,
    EditOfArticleSerializer,
    AutorArtikelSerializer,
    Es_documentSerializer,
    CollectionSerializer,
    AnnotationSerializer,
    TagListSerializer,
    EditOfArticleStSerializer,
    EditOfArticleLemmaSerializer,
    EditOfArticleUserSerializer,
    Es_documentSerializerForScans,
    Es_documentSerializerForCache,
    Es_documentListSerializer
)
from .models import (
    Tag,
    Category,
    Es_document,
    Collection,
    Autor_Artikel,
    Edit_of_article,
    Lemma,
    Annotation,
)
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from django.conf import settings
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from elasticsearch_dsl import Q
from .filters import (
    CategoryFilter,
    CollectionFilter,
    TagFilter,
    LemmaFilter,
    UserFilter,
    EditOfArticleFilter,
    AnnotationFilter,
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import DjangoObjectPermissions
from dboeannotation.metadata import PROJECT_METADATA as PM
from copy import deepcopy
from rest_framework import status
import json


# AnonymousUser can view objects if granted 'view' permission


class DjangoObjectPermissionsOrAnonReadOnly(DjangoObjectPermissions):
    authenticated_users_only = False


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data["token"])
        return Response({"token": token.key, "id": token.user_id})


class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 10000


class UserViewSet(viewsets.ModelViewSet):
    """
    get:
    Return a list of all the existing users.

    post:
    Create a new user instance.

    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    pagination_class = LargeResultsSetPagination
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend,)
    filter_class = UserFilter

    def get_serializer_class(self):
        if self.action == "list":
            return UserListSerializer
        return UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
        get:
        Return a list of all the existing categories.

        post:
    Create a new category instance.

    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LargeResultsSetPagination
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend,)
    filter_class = CategoryFilter


class TagViewSet(viewsets.ModelViewSet):
    """
        get:
        Return a list of all tags.

        post:
    Create a new tag instance.

    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = LargeResultsSetPagination
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend,)
    filter_class = TagFilter

    def get_serializer_class(self):
        if self.action == "list":
            return TagListSerializer
        return TagSerializer


class LemmaViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        queryset = Lemma.objects.all()
        parameter = self.request.query_params.get("has_collection", None)
        editor_para = self.request.query_params.get("has_editor", None)
        if parameter is not None and editor_para is None:
            queryset = Lemma.objects.exclude(
                id__in=Collection.objects.exclude(lemma_id__isnull=True)
            )
        elif parameter is None and editor_para is not None:
            queryset = Lemma.objects.exclude(
                id__in=Edit_of_article.objects.filter(lemma__isnull=False)
            )
        return queryset

    queryset = Lemma.objects.all()
    serializer_class = LemmaSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = LemmaFilter


class EditOfArticleViewSet(viewsets.ModelViewSet):
    queryset = Edit_of_article.objects.all()
    serializer_class = EditOfArticleSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = EditOfArticleFilter

    def get_serializer_class(self):
        parameter = self.request.query_params.get("reporting")
        if parameter is None:
            return EditOfArticleSerializer
        elif parameter == "0":
            return EditOfArticleStSerializer
        elif parameter == "1":
            return EditOfArticleLemmaSerializer
        elif parameter == "2":
            return EditOfArticleUserSerializer


class AutorArtikelViewSet(viewsets.ModelViewSet):
    queryset = Autor_Artikel.objects.all()
    serializer_class = AutorArtikelSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = (DjangoFilterBackend,)


class Es_documentViewSet(viewsets.ModelViewSet):
    """
    get:
    Return a list of all the existing documents.

    post:
    Create a new document instance.

    patch:
    Update only certain fields

    """

    queryset = Es_document.objects.all()
    serializer_class = Es_documentSerializer
    pagination_class = LargeResultsSetPagination
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend,)
    # make a custom filter with exact match for es_id

    # es_id__starts_with = django_filters.CharFilter(lookup_expr='istartswith', field_name="es_id")
    filter_fields = ("es_id", "index", "version", "in_collections", "tag")

    # filter_class = Es_Document_es_id_filter
    def get_queryset(self):
        qs = super().get_queryset()
        es = str(self.request.query_params.get("es_id__startswith")).lower()
        print("es", es)
        if isinstance(es, str) and len(es) > 1 and es != "none":
            return qs.filter(es_id__istartswith=es)
        if bool(self.request.query_params.get("cache_only")) is True:
            return qs.exclude(xml="")
        return qs

    def get_serializer_class(self):
        es = str(self.request.query_params.get("es_id__startswith")).lower()
        if isinstance(es, str) and len(es) > 1 and es != "none":
            return Es_documentSerializerForScans
        if bool(self.request.query_params.get("cache_only")) is True:
            return Es_documentSerializerForCache
        return Es_documentSerializer

    def create(self, request, *args, **kwargs):
        many = True if isinstance(self.request.data, list) else False
        if not many:
            return super().create(request, *args, **kwargs)
        else:
            serializer = Es_documentListSerializer(
                data=request.data, context={"request": request}, many=True
            )
            if serializer.is_valid():
                # 	print('is valido')
                serializer.save()
                # 	print('we created something...', serializer)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                # 	print('is not valido')
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

    def partial_update(self, request, *args, **kwargs):

        allowed_props = {"xml", "xml_error_message"}
        if request.data.keys() <= allowed_props:
            es_document = self.get_object()
            serializer = Es_documentSerializer(
                es_document,
                data=request.data,
                context={"request": request},
                partial=True,
            )
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"detail": serializer.errors}, status=status.HTTP_409_CONFLICT
                )
        else:
            return Response(
                {"detail": f"Allowed properties are {str(allowed_props)}"},
                status=status.HTTP_409_CONFLICT,
            )

    def put(self, request):
        es_documents_data = request.data
        for es_document_item in es_documents_data:
            try:
                es_document = Es_document.objects.get(es_id=es_document_item["es_id"])
            except Es_document.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = self.serializer_class(
                es_document,
                data=es_document_item,
                context={"request": request},
                partial=True,
            )
            if serializer.is_valid():
                serializer.save()

        return Response(status=status.HTTP_200_OK)


class CollectionViewSet(viewsets.ModelViewSet):
    """
        get:
        Return a list of all the existing collection.

        post:
    Create a new collection instance.

    """

    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    pagination_class = LargeResultsSetPagination
    # permission_classes = (DjangoObjectPermissionsOrAnonReadOnly, )
    # permission_classes = (IsAuthenticatedOrAnonReadOnly)
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    # filter_fields = ('title', 'created_by', 'public', 'annotations')
    filter_class = CollectionFilter

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return CollectionListSerializer
        return CollectionSerializer


class AnnotationViewSet(viewsets.ModelViewSet):
    """
        get:
        Return a list of all the existing annotations.

        post:
    Create a new annotation instance.

    """

    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (DjangoObjectPermissionsOrAnonReadOnly,)
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend,)
    filter_class = AnnotationFilter

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


@api_view()
def dboe_query(request):
    """
    The endpoint to query external elasticsearch index;
    the query matches all fields

    """
    client = Elasticsearch(settings.ES_DBOE)
    q = request.GET.get("q")
    if q:
        my_query = Q("multi_match", query=q, fields=["*"])
        search = Search(using=client, index="dboe").query(my_query)
        count = search.count()
        results = search[0:count].execute()
        results = results.to_dict()
    else:
        results = None
    return Response({"results": results})


#################################################################
#                    project info view                          #
#################################################################


@api_view()
def project_info(request):
    """
    returns a dict providing metadata about the current project
    """

    info_dict = deepcopy(PM)
    info_dict["base_tech"] = "django rest framework"
    return Response(info_dict)


@api_view()
def version_info(request):
    """
    returns a software version
    """
    info_dict = None
    with open("version.json") as version_file:
        info_dict = json.load(version_file)
    return Response(info_dict)
