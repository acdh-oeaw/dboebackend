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
	get:
	Return a list of all the existing users.

	post:
    Create a new user instance.

	"""
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer
	pagination_class = LargeResultsSetPagination


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


	def perform_create(self, serializer):
		serializer.save(created_by=self.request.user)