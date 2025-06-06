from django.db import models
from belege.fields import XMLField

POS_CHOICES = (
    ("Subst", "Subst"),
    ("Interj", "Interj"),
    ("Verb", "Verb"),
    ("Adj", "Adj"),
)


def set_extra(self, **kwargs):
    self.extra = kwargs
    return self


class BelegSimple(models.Model):
    dboe_id = models.CharField(
        primary_key=True, max_length=250, verbose_name="DBÖ ID", help_text="The DBÖ ID"
    )
    orig_xml = XMLField(blank=True, null=True, verbose_name="original tei-xml entry")
    xeno_data = models.TextField(
        blank=True, null=True, verbose_name="legacy transkription?"
    )
    hauptlemma = models.CharField(
        blank=True, null=True, max_length=250, verbose_name="Hauptlemma"
    ).set_extra(xpath=".//tei:form[@type='hauptlemma'][1]/tei:orth", node_type="text")
    nebenlemma = models.CharField(
        blank=True, null=True, max_length=250, verbose_name="Nebenlemma"
    ).set_extra(xpath=".//tei:form[@type='nebenlemma']/tei:orth", node_type="text")
    pos = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        verbose_name="POS",
        choices=POS_CHOICES,
    ).set_extra(xpath=".//tei:gramGrp/tei:pos", node_type="text")

    def __str__(self):
        return f"{self.dboe_id}"
