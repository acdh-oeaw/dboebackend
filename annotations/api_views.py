from rest_framework import viewsets
from rest_framework import pagination, generics, filters
import django_filters
from .serializers import *
from .models import *
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Text, Date, Search, MultiSearch
import requests
from django.shortcuts import render
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from elasticsearch_dsl import Q
from .filters import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})


class LargeResultsSetPagination(pagination.PageNumberPagination):
	page_size = 25
	page_size_query_param = 'page_size'
	max_page_size = 10000


class UserViewSet(viewsets.ModelViewSet):
	"""
	get:
	Return a list of all the existing users.

	post:
    Create a new user instance.

	"""
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer
	pagination_class = LargeResultsSetPagination
	# authentication_classes = (TokenAuthentication, )
	filter_backends = (DjangoFilterBackend,)
	filter_fields = ('username', 'collections')


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
	#filter_fields = ('name', )


class Es_documentViewSet(viewsets.ModelViewSet):
	"""
	get:
	Return a list of all the existing documents.

	post:
    Create a new document instance.
    
	"""
	queryset = Es_document.objects.all()
	serializer_class = Es_documentSerializer
	pagination_class = LargeResultsSetPagination
	# authentication_classes = (TokenAuthentication, )
	filter_backends = (DjangoFilterBackend,)
	# make a custom filter with exact match for es_id
	filter_fields = ('es_id', 'index', 'version', 'in_collections')


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
	# authentication_classes = (TokenAuthentication, )
	filter_backends = (DjangoFilterBackend,)
	filter_fields = ('title', 'created_by', 'public')


	def perform_create(self, serializer):
		serializer.save(created_by=self.request.user)


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
	q = request.GET.get('q')
	if q:
		my_query = Q("multi_match", query=q, fields=['*'])
		search = Search(using=client, index="dboe").query(my_query)		
		count = search.count()
		results = search[0:count].execute()
		results = results.to_dict()
	else:
		results = None
	return Response({'results': results})