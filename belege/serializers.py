from rest_framework import serializers
from belege.models import Citation, Lautung, Beleg


def get_serializer_for_model(model_class, field_to_serialize="__all__"):

    class DynamicSerlizer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = model_class
            fields = field_to_serialize

    return DynamicSerlizer


class BelegSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="belege-elastic-search-detail")
    hl = serializers.CharField(source="hauptlemma", required=False)
    nl = serializers.CharField(source="nebenlemma", required=False)
    id = serializers.CharField(source="dboe_id", required=False)
    qu = serializers.CharField(source="quelle", required=False)
    sigle1 = serializers.CharField(source="ort.sigle", required=False)

    class Meta:
        model = Beleg
        fields = [
            "url",
            "id",
            "hl",
            "nl",
            "qu",
            "sigle1",
            "bibl",
            "pos",
            "archivzeile",
        ]

    def get_locationcenter(self, instance):
        return instance.dboe_id[-1] if instance.dboe_id else None

    def get_locationcenter_quq(self, instance):
        return "48.033199664024224,13.996338548539455"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        for x in instance.lautungen.all():
            gram_key = f"GRAM/LT{x.number}"
            ret[gram_key] = [x.pron_gram]
            teut_key = f"LT{x.number}_teuthonista"
            ret[teut_key] = [x.pron]

        for x in instance.lehnwoerter.all():
            number = x.number
            ret[f"LW{number}"] = x.pron

        ret["ANM/KT*"] = []
        ret["BD/KT*"] = []
        for x in instance.citations.all():
            ret["BD/KT*"].append(f"{x.definition} ›KT {x.number}")
            ret[f"KT{x.number}"] = [x.quote_text]
            for y in x.zusatz_lemma.all():
                ret[f"ZL{y.number}/KT{x.number}"] = [
                    f"{y.form_orth}||{y.pos}||{y.gram}"
                ]

            if x.note_anmerkung_b:
                ret["ANM/KT*"].append(f"O: {x.note_anmerkung_o} ›KT{x.number}")
            if x.note_anmerkung_b:
                ret["ANM/KT*"].append(f"B: {x.note_anmerkung_b} ›KT{x.number}")

        ret["BD/LT*"] = []
        for x in instance.bedeutungen.all():
            if x.note_anmerkung_o:
                ret["BD/LT*"].append(
                    f"{x.definition}ANMO: {x.note_anmerkung_o} ›LT{x.number}"
                )
            else:
                ret["BD/LT*"].append(f"{x.definition} ›LT{x.number}")
        try:
            ret["Gemeinde1"] = [f"{instance.ort.sigle} {instance.ort.name}"]
        except AttributeError:
            ret["Gemeinde1"] = []
        try:
            ret["Kleinregion1"] = [
                f"{instance.ort.kregion.sigle} {instance.ort.kregion.abbr}"
            ]
        except AttributeError:
            ret["Kleinregion1"] = []
        try:
            ret["Großregion1"] = [
                f"{instance.ort.gregion.sigle} {instance.ort.gregion.abbr}"
            ]
        except AttributeError:
            ret["Großregion1"] = []
        try:
            ret["Bundesland1"] = [
                f"{instance.ort.bundesland.sigle} {instance.ort.bundesland.abbr}"
            ]
        except AttributeError:
            ret["Bundesland1"] = []

        for i, x in enumerate(instance.zitierweise, start=1):
            ret[f"ZW{i}"] = [x]

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
