from rest_framework import serializers

from bibls.models import BibliographicItem, BibliographicType


class BibliographicItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BibliographicItem
        fields = "__all__"
        depth = 1


class BibliographicTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BibliographicType
        fields = "__all__"
