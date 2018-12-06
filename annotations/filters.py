from django.db import models
from rest_framework import filters
import django_filters
from django_filters.rest_framework import FilterSet
from .models import *
from django.contrib.auth.models import User


class UserFilter(django_filters.rest_framework.FilterSet):
	username = django_filters.CharFilter(lookup_expr='icontains')

	class Meta:
		model = User
		fields = ['username', ]


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
		'collection', 'category', 'created_by']


class CollectionFilter(django_filters.rest_framework.FilterSet):
	title = django_filters.CharFilter(lookup_expr='icontains')
	annotations__category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        label='Annotation category',
        help_text="Search collections by category of its annotations")	

	class Meta:
		model = Collection
		fields = ['title', 'created_by', 'public', 'annotations', 'annotations__category']
