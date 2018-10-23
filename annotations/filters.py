from django.db import models
from rest_framework import filters
import django_filters
from django_filters.rest_framework import FilterSet
from .models import *


class CategoryFilter(django_filters.rest_framework.FilterSet):
	name = django_filters.CharFilter(lookup_expr='icontains')

	class Meta:
		model = Category
		fields = ['name', ]


class AnnotationFilter(django_filters.rest_framework.FilterSet):
	title = django_filters.CharFilter(lookup_expr='icontains')
	description = django_filters.CharFilter(lookup_expr='icontains')

	class Meta:
		model = Annotation
		fields = ['title', 'description',
		'collection', 'category', 'created_by', 'public']

