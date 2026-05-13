from rest_framework import serializers

from bibls.models import BibliographicItem, BibliographicType


class BibliographicTypeSerializer(serializers.HyperlinkedModelSerializer):
    label = serializers.ReadOnlyField(source="view_label")

    class Meta:
        model = BibliographicType
        fields = ["url", "label", "main_type", "sub_type", "specification"]


class BibliographicItemSerializer(serializers.HyperlinkedModelSerializer):
    bibl_type = BibliographicTypeSerializer(read_only=True)
    bibl_type_id = serializers.PrimaryKeyRelatedField(
        source="bibl_type", queryset=BibliographicType.objects.all(), write_only=True
    )

    class Meta:
        model = BibliographicItem
        fields = "__all__"
