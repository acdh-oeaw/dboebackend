from django.db import models
from django.forms import TextInput
from django_filters import UnknownFieldBehavior
from django_filters import rest_framework as filters

CHAR_LOOKUP_CHOICES = [
    ("icontains", "Contains"),
    ("iexact", "Equals"),
    ("istartswith", "Starts with"),
    ("iendswith", "Ends with"),
]


def filter_by_ids(queryset, name, value):
    values = value.split(",")
    return queryset.filter(dboe_id__in=values)


def get_filterset_for_model(model_class):
    """Returns a FilterSet class for the given model_class."""

    class DynamicFilterSet(filters.FilterSet):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            if hasattr(self._meta.model, "dboe_id"):
                self.filters["ids"] = filters.CharFilter(
                    method=filter_by_ids,
                    label="DBOE IDs",
                    help_text="Enter comma-separated DBOE IDs",
                )

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
