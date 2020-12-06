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


class TagFilter(django_filters.rest_framework.FilterSet):
	name = django_filters.CharFilter(lookup_expr='icontains')
	color = django_filters.CharFilter(lookup_expr='icontains')
	emoji = django_filters.CharFilter(lookup_expr='icontains')

	class Meta:
		model = Tag
		fields = ['name', 'color', 'emoji']


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
	tag = django_filters.ModelMultipleChoiceFilter(
		queryset=Tag.objects.all(), field_name='es_document__tag',
		label='Tag', help_text="Filter collections by tags of its documents"
		)

	class Meta:
		model = Collection
		fields = ['title', 'created_by',
		'public', 'annotations',
		'annotations__category', 'tag', 'deleted', 'lemma_id']


class LemmaFilter(django_filters.rest_framework.FilterSet):
        CHOICES_TASK = (
                (0, 'Keiner Aufgabe zugewiesen'),
                (1, 'Bereits Aufgabe zugewiesen'),
                (2, 'Kein User zugewiesen')
                )

        CHOICES_COLLECTION = (
                (0, 'Collection zugewiesen'),
                (1, 'Keiner Collection zugewiesen')
                )
        org = django_filters.CharFilter(lookup_expr='icontains')
        norm = django_filters.CharFilter(lookup_expr='icontains')
        count__gt = django_filters.NumberFilter(field_name='count', lookup_expr='gt')
        count__lt = django_filters.NumberFilter(field_name='count', lookup_expr='lt')
        has__norm = django_filters.BooleanFilter(field_name='norm', lookup_expr='isnull', exclude=False)
        # has__lemma = django_filters.BooleanFilter(field_name='has_lemma', method='check_task')
        task = django_filters.ChoiceFilter(label='tasks', method='check_task', choices=CHOICES_TASK)
        collection = django_filters.ChoiceFilter(label='Collections', method='check_collection', choices=CHOICES_COLLECTION)

        def check_collection(self, queryset, name, value):
            val = int(value)
            blocked = Collection.objects.exclude(lemma_id = None).values_list('lemma_id', flat = True).distinct()

            if val == 1:
                return Lemma.objects.exclude(id__in = blocked)
            else:
                return Lemma.objects.filter(id__in = blocked)

        def check_task(self, queryset, name, value):
            val = int(value)
            blocked = Edit_of_article.objects.exclude(lemma = None).values_list('lemma', flat = True).distinct()
            if val == 0:
                return Lemma.objects.exclude(id__in = blocked)
            elif val == 1:
                return Lemma.objects.filter(id__in = blocked)
            blocked = Edit_of_article.objects.exclude(lemma = None, user = None).values_list('lemma', flat = True).distinct()
            return Lemma.objects.exclude(id__in = blocked)
        
        has__simplex = django_filters.BooleanFilter(field_name='simplex', lookup_expr='isnull')
        class Meta:
            model = Lemma
            fields = ['org', 'norm', 'filename', 'count', 'simplex', 'task']


class EditOfArticleFilter(django_filters.rest_framework.FilterSet):
        user = django_filters.CharFilter(field_name = 'user__username', lookup_expr='icontains')
        lemma = django_filters.CharFilter(field_name = 'lemma__org', lookup_expr = 'icontains')
        date = django_filters.DateFilter(field_name = 'deadline', lookup_expr = 'exact')

        class Meta:
            model = Edit_of_article
            fields = ['deadline', 'step', 'status', 'last_edited', 'current', 'user', 'lemma', 'finished_date']
