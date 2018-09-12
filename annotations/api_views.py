from rest_framework import viewsets
from rest_framework import pagination
from .serializers import *
from .models import *
from django.contrib.auth.models import User


class LargeResultsSetPagination(pagination.PageNumberPagination):
	page_size = 25
	page_size_query_param = 'page_size'
	max_page_size = 10000


class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer
	pagination_class = LargeResultsSetPagination


class CategoryViewSet(viewsets.ModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	pagination_class = LargeResultsSetPagination


class Es_documentViewSet(viewsets.ModelViewSet):
	queryset = Es_document.objects.all()
	serializer_class = Es_documentSerializer
	pagination_class = LargeResultsSetPagination


class CollectionViewSet(viewsets.ModelViewSet):
	queryset = Collection.objects.all()
	serializer_class = CollectionSerializer
	pagination_class = LargeResultsSetPagination


	def perform_create(self, serializer):
		serializer.save(created_by=self.request.user)


class AnnotationViewSet(viewsets.ModelViewSet):
	queryset = Annotation.objects.all()
	serializer_class = AnnotationSerializer
	pagination_class = LargeResultsSetPagination


	def perform_create(self, serializer):
		serializer.save(created_by=self.request.user)