from rest_framework import serializers
from belege.models import Ort


class OrtSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ort
        fields = "__all__"


def get_serializer_for_model(model_class, field_to_serialize="__all__"):

    class DynamicSerlizer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = model_class
            fields = field_to_serialize

    return DynamicSerlizer
