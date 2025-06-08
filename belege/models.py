import xml.etree.ElementTree as ET
from django.db import models
from belege.fields import XMLField
from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import extract_fulltext, get_xmlid


POS_CHOICES = (
    ("Subst", "Subst"),
    ("Interj", "Interj"),
    ("Verb", "Verb"),
    ("Adj", "Adj"),
)


def set_extra(self, **kwargs):
    self.extra = kwargs
    return self


models.Field.set_extra = set_extra


class Citation(models.Model):
    """
    Django model representing a citation extracted from TEI XML documents.
    This model stores individual citations that belong to a Beleg (tei:entry/tei:cit).
    Each citation contains metadata, original XML content, and extracted text fields
    that are automatically populated from the TEI XML using XPath expressions.
    Attributes:
        dboe_id (CharField): Primary key identifier for the citation (e.g., "tu-10130.56")
        beleg (ForeignKey): Reference to the parent Beleg instance
        number (PositiveIntegerField): Order number for sorting citations within a Beleg
        orig_xml (XMLField): Original TEI citation node in XML format
        quote_text (TextField): Plain text content extracted from TEI quote element
        definition (TextField): Definition text extracted from TEI definition element
    The model automatically extracts text content from XML fields during save operations
    using XPath expressions defined in field metadata. Fields with 'extra' attributes
    containing 'xpath' keys will be populated by querying the orig_xml content.
    Meta:
        verbose_name: "Zitat"
        verbose_name_plural: "Zitate"
        ordering: ["beleg", "number"]
    """

    dboe_id = models.CharField(
        primary_key=True,
        max_length=250,
        verbose_name="DBÖ ID",
        help_text="e.g. tu-10130.56",
    )
    beleg = models.ForeignKey(
        "Beleg",
        verbose_name="Beleg",
        on_delete=models.CASCADE,
        related_name="citations",
    )
    number = models.PositiveIntegerField(default=1, verbose_name="order number")
    orig_xml = XMLField(verbose_name="original tei-cit node")
    quote_text = models.TextField(
        blank=True, null=True, verbose_name="plain text"
    ).set_extra(xpath="./tei:quote", node_type="text")
    definition = models.TextField(
        blank=True, null=True, verbose_name="definition"
    ).set_extra(xpath="./tei:def", node_type="text")

    class Meta:
        verbose_name = "Zitat"
        verbose_name_plural = "Zitate"
        ordering = ["beleg", "number"]

    def save(self, *args, **kwargs):
        if self.orig_xml:
            try:
                doc = TeiReader(self.orig_xml)
            except AttributeError:
                doc = TeiReader(ET.tostring(self.orig_xml).decode("utf-8"))
            for field in self._meta.fields:
                if hasattr(field, "extra") and "xpath" in field.extra:
                    xpath_expr = field.extra["xpath"]
                    try:
                        nodes = doc.any_xpath(xpath_expr)[0]
                    except IndexError:
                        continue
                    value = extract_fulltext(nodes)
                    setattr(self, field.name, value)
        super().save(*args, **kwargs)


class Beleg(models.Model):
    """
    Django model representing a Beleg entry from the DBÖ (Dictionary of Bavarian Dialects in Austria) database.
    This model stores linguistic evidence with metadata extracted from TEI-XML documents. It automatically
    populates fields from XML using XPath expressions and can create related Citation objects.
    """

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
    archivzeile = models.CharField(
        blank=True, null=True, max_length=250, verbose_name="Archivzeile"
    ).set_extra(xpath=".//tei:ref[@type='archiv']", node_type="text")
    quelle = models.CharField(
        blank=True, null=True, max_length=250, verbose_name="Quelle"
    ).set_extra(xpath=".//tei:ref[@type='quelle']", node_type="text")
    quelle_bearbeitet = models.CharField(
        blank=True, null=True, max_length=250, verbose_name="Quelle bearbeitet"
    ).set_extra(xpath=".//tei:ref[@type='quelleBearbeitet']", node_type="text")
    bibl = models.CharField(
        blank=True, null=True, max_length=250, verbose_name="Literatur"
    ).set_extra(xpath=".//tei:ref[@type='bibl']/tei:bibl", node_type="text")
    pos = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        verbose_name="POS",
        choices=POS_CHOICES,
    ).set_extra(xpath=".//tei:gramGrp/tei:pos", node_type="text")
    import_issue = models.BooleanField(
        default=False,
        verbose_name="Import issue",
        help_text="Set to True if there was an issue during import",
    )

    class Meta:
        verbose_name = "Beleg"
        verbose_name_plural = "Belege"
        ordering = ["dboe_id"]

    def __str__(self):
        if self.hauptlemma:
            return f"{self.dboe_id} ({self.hauptlemma})"
        return f"{self.dboe_id}"

    def save(self, add_citations=False, *args, **kwargs):
        """
        Save the model instance with optional XML processing and citation extraction.
        This method extends the default save behavior by:
        1. Parsing the orig_xml field using TeiReader if present
        2. Extracting values from XML nodes using XPath expressions defined in field metadata
        3. Optionally creating Citation objects from XML citation elements
        Args:
            add_citations (bool, optional): If True, extracts and creates Citation objects
                from tei:cit elements found in the XML. Defaults to False.
            *args: Variable length argument list passed to parent save method.
            **kwargs: Arbitrary keyword arguments passed to parent save method.
        Returns:
            None
        Notes:
            - Fields with 'xpath' in their extra metadata will have their values
              automatically populated from the corresponding XML nodes
            - When add_citations is True, Citation objects are created with
              extracted dboe_id, number, and original XML content
            - Uses get_or_create to avoid duplicate Citation entries
        """

        if self.orig_xml:
            try:
                doc = TeiReader(self.orig_xml)
            except AttributeError:
                doc = TeiReader(ET.tostring(self.orig_xml).decode("utf-8"))
            for field in self._meta.fields:
                if hasattr(field, "extra") and "xpath" in field.extra:
                    if self.orig_xml:
                        xpath_expr = field.extra["xpath"]
                        try:
                            nodes = doc.any_xpath(xpath_expr)[0]
                        except IndexError:
                            continue
                        value = extract_fulltext(nodes)
                        if isinstance(field, models.CharField):
                            if field.max_length and len(value) > field.max_length:
                                value = value[: field.max_length]
                                self.import_issue = True
                        if isinstance(field, (models.CharField, models.TextField)):
                            value = value.strip()
                        setattr(self, field.name, value)
        if self.orig_xml and add_citations:
            items = doc.any_xpath("./tei:cit")
            for item in items:
                xml_id = get_xmlid(item)
                number = item.attrib["n"]
                orig_xml = ET.tostring(item, encoding="unicode")
                try:
                    item = Citation.objects.get(dboe_id=xml_id)
                except Citation.DoesNotExist:
                    item = Citation(dboe_id=xml_id, beleg=self, number=number, orig_xml=orig_xml)
                try:
                    item.save()
                except Exception as e:
                    print(f"Error saving citation {xml_id}: {e}")
        super().save(*args, **kwargs)
