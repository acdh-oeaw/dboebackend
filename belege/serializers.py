from rest_framework import serializers
from belege.models import Citation, Lautung, Beleg


def get_serializer_for_model(model_class, field_to_serialize="__all__"):

    class DynamicSerlizer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = model_class
            fields = field_to_serialize

    return DynamicSerlizer


class BelegSerializer(serializers.HyperlinkedModelSerializer):
    hl = serializers.CharField(source="hauptlemma", required=False)
    id = serializers.CharField(source="dboe_id", required=False)
    qu = serializers.CharField(source="quelle", required=False)
    sigle1 = serializers.CharField(source="ort.sigle", required=False)
    locationcenter = serializers.SerializerMethodField(required=False)
    locationcenter_quq = serializers.SerializerMethodField(required=False)
    bundesland1 = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Beleg
        fields = [
            "url",
            "id",
            "hl",
            "qu",
            "sigle1",
            "locationcenter",
            "locationcenter_quq",
            "bundesland1",
            "bibl",
        ]

    def get_locationcenter(self, instance):
        return instance.dboe_id[-1] if instance.dboe_id else None

    def get_locationcenter_quq(self, instance):
        return "48.033199664024224,13.996338548539455"

    def get_bundesland1(self, instance):
        try:
            return f"{instance.ort.bundesland.sigle} {instance.ort.bundesland.abbr}"
        except AttributeError:
            return ""

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        for x in instance.lautungen.all():
            gram_key = f"GRAM/LT{x.number}"
            ret[gram_key] = x.pron_gram
            teut_key = f"LT{x.number}_teuthonista"
            ret[teut_key] = x.pron

        ret["BD/LT*"] = []
        for x in instance.bedeutungen.all():
            ret["BD/LT*"].append(x.definition)

        return ret


class CitationSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="citation-detail", lookup_field="dboe_id"
    )
    id = serializers.CharField(source="dboe_id", read_only=False)
    beleg_id = serializers.CharField(source="beleg.dboe_id", read_only=True)
    orig_xml = serializers.CharField(read_only=True)

    class Meta:
        model = Citation
        fields = "__all__"


class LautungSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="lautung-detail", lookup_field="dboe_id"
    )
    id = serializers.CharField(source="dboe_id", read_only=False)
    beleg_id = serializers.CharField(source="beleg.dboe_id", read_only=True)
    orig_xml = serializers.CharField(read_only=True)

    class Meta:
        model = Lautung
        fields = "__all__"
