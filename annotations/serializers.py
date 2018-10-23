# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
	collections = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='collection-detail')
	annotations = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='annotation-detail')

	class Meta:
		model = User
		fields = [
			'url', 'username',
			'collections', 'annotations'
			]


class CategorySerializer(serializers.HyperlinkedModelSerializer):
	annotations = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='annotation-detail')

	class Meta:
		model = Category
		fields = [
			'url', 'name',
			'notation', 'note',
			'annotations'
			]


class Es_documentSerializer(serializers.HyperlinkedModelSerializer):
	in_collections = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='collection-detail')

	class Meta:
		model = Es_document
		fields = [
			'url', 'es_id',
			'index', 'version',
			'in_collections'
			]

	def create(self, validated_data):
		es_id, created = Es_document.objects.get_or_create(
			es_id=validated_data.get('es_id', None),
			defaults={'es_id': validated_data.get('es_id', None)})
		return es_id


class CollectionSerializer(serializers.HyperlinkedModelSerializer):
	created_by = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')
	annotations = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='annotation-detail')

	class Meta:
		model = Collection
		fields = [
			'url', 'title', 'description',
			'created_by', 'es_document',
			'public', 'comment',
			'annotations',
			'created', 'modified'
			]


class AnnotationSerializer(serializers.HyperlinkedModelSerializer):
	created_by = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')

	class Meta:
		model = Annotation
		fields = [
			'url', 'collection',
			'title', 'description',
			'category', 'public',
			'created_by', 'created',
			'modified'
			]