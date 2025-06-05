from django.db import models
from django import forms
import xml.etree.ElementTree as ET

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class XMLWidget(forms.widgets.Textarea):
    def format_value(self, value):
        if isinstance(value, ET.Element):
            return ET.tostring(value, encoding='unicode')
        return value


class XMLField(models.Field):
    description = _("XML Data")

    def db_type(self, connection):
        """
        Returns the database column data type for this field.
        For PostgreSQL, we want to use the native 'xml' type.
        """
        return 'xml'

    def to_python(self, value):
        """
        Convert the input value into the correct Python data type.
        This method is called by deserialization and during form cleaning.
        """
        if value is None:
            return value

        # If it's already a parsed element or string, return as-is or process accordingly.
        if isinstance(value, ET.Element):
            return value

        # Assume the value is a string and try parsing it.
        try:
            return ET.fromstring(value)
        except ET.ParseError:
            # Optionally, you might want to raise a validation error instead.
            raise ValidationError(_("Invalid XML data."))

    def get_db_prep_value(self, value, connection, prepared=False):
        """
        Prepare the value for storage into the database.
        Convert the Python XML data (an ElementTree Element) into a string.
        """
        if value is None:
            return value

        # If the value is an Element, convert it to a string.
        if isinstance(value, ET.Element):
            return ET.tostring(value, encoding='unicode')

        # If it's already a string, you might want to do a simple validation check.
        try:
            ET.fromstring(value)
        except ET.ParseError:
            raise ValidationError(_("Invalid XML data."))
        return value

    def from_db_value(self, value, expression, connection):
        """
        Convert a value as returned by the database to a Python object.
        This method is invoked when Django retrieves a value from the database.
        """
        if value is None:
            return value

        try:
            return ET.fromstring(value)
        except ET.ParseError:
            raise ValidationError(_("Invalid XML data in database."))

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.CharField,
            'widget': XMLWidget,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)

    # def value_to_string(self, obj):
    #     """
    #     Convert the value for serialization.
    #     """
    #     value = self.value_from_object(obj)
    #     if isinstance(value, ET.Element):
    #         return ET.tostring(value, encoding='unicode')
    #     return value
