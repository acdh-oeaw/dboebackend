from django.db import models
from belege.fields import XMLField


class BelegSimple(models.Model):
    dboe_id = models.CharField(
        blank=True, null=True, max_length=250, verbose_name="DBÖ ID", help_text="The DBÖ ID"
    )
    simple_xml = XMLField(blank=True, null=True, verbose_name="simplified XML")

    def __str__(self):
        return f"{self.dboe_id}"
