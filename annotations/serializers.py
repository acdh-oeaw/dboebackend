# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
	collections_created = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='collection-detail')
	collections_curated = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='collection-detail')
	annotations_created = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='annotation-detail')

	class Meta:
		model = User
		fields = [
			'url', 'username',
			'date_joined',
			'collections_created',
			'collections_curated',
			'annotations_created'
			]


class CategorySerializer(serializers.HyperlinkedModelSerializer):
	annotations = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='annotation-detail')

	class Meta:
		model = Category
		fields = [
			'url', 'name',
			'description',
			'note', 'notation',
			'annotations'
			]


class TagSerializer(serializers.HyperlinkedModelSerializer):
	es_documents = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='es_document-detail')

	class Meta:
		model = Tag
		fields = [
			'url', 'name',
			'color',
			'emoji', 'meta',
			'es_documents'
			]

	def create(self, validated_data):
		name, created = Tag.objects.get_or_create(
			name=validated_data.get('name', None),
			defaults={'name': validated_data.get('name', None)})
		return name


class Es_documentSerializer(serializers.HyperlinkedModelSerializer):
	in_collections = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='collection-detail')

	class Meta:
		model = Es_document
		fields = [
			'url', 'es_id',
			'index', 'version',
			'tag',
			'in_collections'
			]

	def create(self, validated_data):
		es_id, created = Es_document.objects.get_or_create(
			es_id=validated_data.get('es_id', None),
			defaults={'es_id': validated_data.get('es_id', None)})
		return es_id


class CollectionSerializer(serializers.HyperlinkedModelSerializer):
	#created_by = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')
	created_by = serializers.StringRelatedField()
	annotations = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='annotation-detail')
	tags = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='tag-detail')

	class Meta:
		model = Collection
		fields = [
			'url', 'title', 'description',
			'es_document', 'comment',
			'annotations',
			'created_by', 'curator',
			'public',
			'created', 'modified',
			'tags'
			]


class AnnotationSerializer(serializers.HyperlinkedModelSerializer):
	#created_by = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')
	created_by = serializers.StringRelatedField()

	class Meta:
		model = Annotation
		fields = [
			'url', 'collection',
			'title', 'description',
			'category', 'created_by',
			'created', 'modified'
			]