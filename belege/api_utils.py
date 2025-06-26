from django_filters import rest_framework as filters
from django_filters import UnknownFieldBehavior
from django.forms import TextInput
from django.db import models


CHAR_LOOKUP_CHOICES = [
    ("icontains", "Contains"),
    ("iexact", "Equals"),
    ("istartswith", "Starts with"),
    ("iendswith", "Ends with"),
]


def get_filterset_for_model(model_class):
    """Returns a FilterSet class for the given model_class."""

    class DynamicFilterSet(filters.FilterSet):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in (
                self._meta.model._meta.fields + self._meta.model._meta.many_to_many
            ):
                field_name = field.name
                if isinstance(
                    field, (models.CharField, models.TextField, models.BooleanField)
                ):
                    self.filters[f"{field_name}__icontains"] = filters.CharFilter(
                        field_name=field_name,
                        lookup_expr="icontains",
                        label=f"{field.verbose_name} contains",
                        help_text=field.help_text,
                    )
                elif isinstance(field, (models.ForeignKey, models.ManyToManyField)):
                    self.filters[field_name] = filters.ModelChoiceFilter(
                        field_name=field_name,
                        queryset=field.related_model.objects.all(),
                        label=field.verbose_name,
                        help_text=f"Enter ID for {field.verbose_name}",
                        widget=TextInput(
                            attrs={
                                "placeholder": "Enter ID",
                            }
                        ),
                    )

        class Meta:
            model = model_class
            fields = "__all__"
            unknown_field_behavior = UnknownFieldBehavior.IGNORE

    return DynamicFilterSet
