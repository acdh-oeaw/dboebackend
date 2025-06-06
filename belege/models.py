from django.db import models
from belege.fields import XMLField


class BelegSimple(models.Model):
    dboe_id = models.CharField(
        primary_key=True, max_length=250, verbose_name="DBÖ ID", help_text="The DBÖ ID"
    )
    orig_xml = XMLField(blank=True, null=True, verbose_name="original tei-xml entry")
    xeno_data = models.TextField(blank=True, null=True, verbose_name="legacy transkription?")
    hauptlemma = models.TextField(blank=True, null=True, max_length=20, verbose_name="Hauptlemma")

    def __str__(self):
        return f"{self.dboe_id}"
