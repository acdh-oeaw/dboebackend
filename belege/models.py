import xml.etree.ElementTree as ET
from django_jsonform.models.fields import ArrayField
from django.db import models
from belege.fields import XMLField
from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import extract_fulltext, get_xmlid
from acdh_xml_pyutils.xml import NSMAP


POS_CHOICES = (
    ("Subst", "Subst"),
    ("Interj", "Interj"),
    ("Verb", "Verb"),
    ("Adj", "Adj"),
)

LANG_CHOICES = (("bar", "bar"), ("de", "de"))

RESP_OPTIONS = (("O", "O"), ("B", "B"))


def set_extra(self, **kwargs):
    self.extra = kwargs
    return self


models.Field.set_extra = set_extra


class Facsimile(models.Model):
    """
    A facsimile
    """

    file_name = models.CharField(
        max_length=250, unique=True, verbose_name="Dateiname", help_text="whatever"
    )

    @classmethod
    def get_base_url(cls):
        return "https://some-iiif-url/"

    @property
    def facs_url(self):
        return f"{self.get_base_url}{self.file_name}"

    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name = "Faksimile"
        verbose_name_plural = "Faksimiles"
        ordering = ["file_name"]


class BundesLand(models.Model):
    """
    A federal state (Bundesland) in Austria.
    """

    sigle = models.CharField(
        default="1", max_length=20, verbose_name="Sigle", help_text="whatever"
    )
    abbr = models.CharField(default="OÖ", max_length=50, verbose_name="Kürzel")
    name = models.CharField(default="", max_length=50, verbose_name="Name")
    geonames = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="GeoNames URL",
        help_text="Link to corresponding GeoNames entry",
    )
    coordinates = models.JSONField(
        blank=True,
        null=True,
        verbose_name="Koordinaten",
    )

    def __str__(self):
        if self.name:
            return f"{self.name} ({self.sigle})"
        else:
            return f"{self.abbr} ({self.sigle})"

    class Meta:
        verbose_name = "Bundesland"
        verbose_name_plural = "Bundesländer"
        ordering = ["name"]


class GRegion(models.Model):
    """
    A geographical greater region (Großregion) in Austria.
    """

    sigle = models.CharField(default="5.4", max_length=20, verbose_name="Sigle")
    abbr = models.CharField(default="Mühlv.", max_length=50, verbose_name="Kürzel")
    name = models.CharField(default="", max_length=50, verbose_name="Name")
    bundesland = models.ForeignKey(
        "Bundesland",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Bundesland",
    )
    geonames = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="GeoNames URL",
        help_text="Link to corresponding GeoNames entry",
    )
    coordinates = models.JSONField(
        blank=True,
        null=True,
        verbose_name="Koordinaten",
    )

    def __str__(self):
        if self.name:
            return f"{self.name} ({self.sigle})"
        else:
            return f"{self.abbr} ({self.sigle})"

    class Meta:
        verbose_name = "Großregion"
        verbose_name_plural = "Großregionen"
        ordering = ["name"]


class KRegion(models.Model):
    """
    A small region (Kleinregion) in Austria.
    """

    sigle = models.CharField(default="1", max_length=20, verbose_name="Sigle")
    abbr = models.CharField(
        default="swestl.uMühlv.", max_length=50, verbose_name="Kürzel"
    )
    name = models.CharField(default="", max_length=50, verbose_name="Name")
    bundesland = models.ForeignKey(
        "Bundesland",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Bundesland",
    )
    gregion = models.ForeignKey(
        "GRegion",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Großregion",
    )
    geonames = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="GeoNames URL",
        help_text="Link to corresponding GeoNames entry",
    )
    coordinates = models.JSONField(
        blank=True,
        null=True,
        verbose_name="Koordinaten",
    )

    def __str__(self):
        if self.name:
            return f"{self.name} ({self.sigle})"
        else:
            return f"{self.abbr} ({self.sigle})"

    class Meta:
        verbose_name = "Kleinregion"
        verbose_name_plural = "Kleinregionen"
        ordering = ["name"]


class Ort(models.Model):
    """
    A location/place (Ort) in the DBOE annotation system.
    """

    sigle = models.CharField(default="1", max_length=20, verbose_name="Sigle")
    name = models.CharField(default="", max_length=250, verbose_name="Name")
    bundesland = models.ForeignKey(
        "Bundesland",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Bundesland",
    )
    gregion = models.ForeignKey(
        "GRegion",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Großregion",
    )
    kregion = models.ForeignKey(
        "KRegion",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Kleinregion",
    )
    geonames = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="GeoNames URL",
        help_text="Link to corresponding GeoNames entry",
    )
    coordinates = models.JSONField(
        blank=True,
        null=True,
        verbose_name="Koordinaten",
    )

    def __str__(self):
        if self.name:
            return f"{self.name} ({self.sigle})"
        else:
            return f"{self.sigle}"

    class Meta:
        verbose_name = "Ort"
        verbose_name_plural = "Orte"
        ordering = ["name"]


class ZusatzLemma(models.Model):
    """
    Django model representing a tei:re node extracted a tei:cit node.
    """

    dboe_id = models.CharField(
        primary_key=True,
        max_length=250,
        verbose_name="DBÖ ID",
        help_text="e.g. tu-10130.56",
    )
    citation = models.ForeignKey(
        "Citation",
        verbose_name="Citation",
        on_delete=models.CASCADE,
        related_name="zusatz_lemma",
    )
    number = models.PositiveIntegerField(default=1, verbose_name="Order number")
    orig_xml = XMLField(
        verbose_name="XML Node", help_text="tei:form[@type='lautung'] node"
    )
    form_orth = models.CharField(
        blank=True, null=True, max_length=250, verbose_name="Lemma"
    ).set_extra(xpath="./tei:form/tei:orth", node_type="text")
    pos = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        verbose_name="POS",
        choices=POS_CHOICES,
    ).set_extra(xpath="./tei:gramGrp/tei:pos", node_type="text")
    gram = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        verbose_name="Grammatik",
        choices=POS_CHOICES,
    ).set_extra(xpath="./tei:gramGrp/tei:gram", node_type="text")

    class Meta:
        verbose_name = "Zusatzlemma"
        verbose_name_plural = "Zusatzlemmata"
        ordering = ["citation", "number"]

    def __str__(self):
        if self.form_orth:
            return f"{self.form_orth}"
        else:
            return f"{self.dboe_id}"

    def save(self, *args, **kwargs):
        if self.orig_xml is not None:
            try:
                doc = TeiReader(self.orig_xml)
            except AttributeError:
                doc = TeiReader(ET.tostring(self.orig_xml).decode("utf-8"))
            for field in self._meta.fields:
                if (
                    hasattr(field, "extra")
                    and "xpath" in field.extra
                    and isinstance(field, (models.CharField, models.TextField))
                    and not getattr(self, field.name)
                ):
                    xpath_expr = field.extra["xpath"]
                    try:
                        nodes = doc.any_xpath(xpath_expr)[0]
                    except IndexError:
                        continue
                    try:
                        value = extract_fulltext(nodes)
                    except AttributeError:
                        value = nodes
                    setattr(self, field.name, value)
        super().save(*args, **kwargs)


class Citation(models.Model):
    """
    Django model representing a citation (Kontext) extracted from TEI XML documents.
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
    quote_lang = models.CharField(
        max_length=3,
        choices=LANG_CHOICES,
        blank=True,
        null=True,
        verbose_name="Sprache (Kontext)",
    ).set_extra(xpath="./tei:quote/@xml:lang", node_type="attribute")
    quote_text = models.TextField(
        blank=True, null=True, verbose_name="plain text"
    ).set_extra(xpath="./tei:quote", node_type="text")
    quote_gram = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="Grammatik",
        help_text="whatever",
    ).set_extra(xpath="./tei:quote/tei:seg[@type='gram']", node_type="text")
    p_ref = models.CharField(
        blank=True,
        null=True,
        verbose_name="Pronunciation reference",
        help_text="whatever",
    ).set_extra(xpath="./tei:quote/tei:pRef", node_type="text")
    definition = models.TextField(
        blank=True, null=True, verbose_name="definition"
    ).set_extra(xpath="./tei:def", node_type="text")
    definition_lang = models.CharField(
        max_length=3,
        choices=LANG_CHOICES,
        blank=True,
        null=True,
        verbose_name="Sprache (Definition)",
    ).set_extra(xpath="./tei:def/@xml:lang", node_type="attribute")
    interpration = models.TextField(
        blank=True,
        null=True,
        verbose_name="interpretation",
        help_text="Summarizes a specific interpretative annotation which can be linked to a span of text",
    ).set_extra(xpath="./tei:interp", node_type="text")
    note_anmerkung_o = models.TextField(
        blank=True,
        null=True,
        verbose_name="Anmerkung: O",
        help_text="Whatever",
    ).set_extra(xpath="./tei:note[@type='anmerkung' and @resp='O']", node_type="text")
    note_anmerkung_b = models.TextField(
        blank=True,
        null=True,
        verbose_name="Anmerkung: B",
        help_text="Whatever",
    ).set_extra(xpath="./tei:note[@type='anmerkung' and @resp='B']", node_type="text")
    fragebogen_nummer = models.TextField(
        blank=True,
        null=True,
        verbose_name="Fragebogen Nummer",
        help_text="Whatever",
    ).set_extra(xpath="./tei:ref[@type='fragebogenNummer']", node_type="text")

    class Meta:
        verbose_name = "Kontext"
        verbose_name_plural = "Kontexte"
        ordering = ["beleg", "number"]

    def save(self, add_zusatzlemma=False, *args, **kwargs):
        if self.orig_xml is not None:
            try:
                doc = TeiReader(self.orig_xml)
            except AttributeError:
                doc = TeiReader(ET.tostring(self.orig_xml).decode("utf-8"))
            for field in self._meta.fields:
                if (
                    hasattr(field, "extra")
                    and "xpath" in field.extra
                    and isinstance(field, (models.CharField, models.TextField))
                    and not getattr(self, field.name)
                ):
                    xpath_expr = field.extra["xpath"]
                    try:
                        nodes = doc.any_xpath(xpath_expr)[0]
                    except IndexError:
                        continue
                    try:
                        value = extract_fulltext(nodes)
                    except AttributeError:
                        value = nodes
                    setattr(self, field.name, value)
        if self.orig_xml is not None and add_zusatzlemma:
            items = doc.any_xpath("./tei:re")
            for number, item in enumerate(items, start=1):
                xml_id = get_xmlid(item)
                orig_xml = ET.tostring(item, encoding="unicode")
                try:
                    item = ZusatzLemma.objects.get(dboe_id=xml_id)
                except ZusatzLemma.DoesNotExist:
                    item = ZusatzLemma(
                        dboe_id=xml_id, citation=self, number=number, orig_xml=orig_xml
                    )
                try:
                    item.save()
                except Exception as e:
                    print(f"Error saving ZusatzLemma {xml_id}: {e}")
        super().save(*args, **kwargs)


class Lautung(models.Model):
    """
    Django model representing a tei:form[@type="lautung"] node.
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
        related_name="lautungen",
    )
    number = models.PositiveIntegerField(default=1, verbose_name="Order number")
    orig_xml = XMLField(
        verbose_name="XML Node", help_text="tei:form[@type='lautung'] node"
    )
    pron = models.CharField(
        blank=True, null=True, max_length=250, verbose_name="Pronunciation"
    ).set_extra(xpath="./tei:pron", node_type="text")
    pron_lang = models.CharField(
        max_length=3,
        choices=LANG_CHOICES,
        blank=True,
        null=True,
        verbose_name="Sprache (Pronunciation)",
    ).set_extra(xpath="./tei:pron/@xml:lang", node_type="attribute")
    pron_gram = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        verbose_name="Grammatik",
        help_text="whatever",
    ).set_extra(xpath="./tei:gramGrp/tei:gram", node_type="text")

    class Meta:
        verbose_name = "Lautung"
        verbose_name_plural = "Lautungen"
        ordering = ["beleg", "number"]

    def __str__(self):
        return f"{self.pron} ({self.beleg})"

    def save(self, *args, **kwargs):
        if self.orig_xml is not None:
            try:
                doc = TeiReader(self.orig_xml)
            except AttributeError:
                doc = TeiReader(ET.tostring(self.orig_xml).decode("utf-8"))
            for field in self._meta.fields:
                if (
                    hasattr(field, "extra")
                    and "xpath" in field.extra
                    and isinstance(field, (models.CharField, models.TextField))
                    and not getattr(self, field.name)
                ):
                    xpath_expr = field.extra["xpath"]
                    try:
                        nodes = doc.any_xpath(xpath_expr)[0]
                    except IndexError:
                        continue
                    try:
                        value = extract_fulltext(nodes)
                    except AttributeError:
                        value = nodes
                    setattr(self, field.name, value)
        super().save(*args, **kwargs)


class LehnWort(models.Model):
    """
    Django model representing a tei:form[@type="lautung"] node.
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
        related_name="lehnwoerter",
    )
    number = models.PositiveIntegerField(default=1, verbose_name="Order number")
    orig_xml = XMLField(
        verbose_name="XML Node", help_text="tei:form[@type='lehnwort'] node"
    )
    pron = models.CharField(
        blank=True, null=True, max_length=250, verbose_name="Pronunciation"
    ).set_extra(xpath="./tei:pron", node_type="text")
    pron_lang = models.CharField(
        max_length=3,
        choices=LANG_CHOICES,
        blank=True,
        null=True,
        verbose_name="Sprache (Pronunciation)",
    ).set_extra(xpath="./tei:pron/@xml:lang", node_type="attribute")
    pron_gram = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        verbose_name="Grammatik",
        help_text="whatever",
    ).set_extra(xpath="./tei:gramGrp/tei:gram", node_type="text")

    class Meta:
        verbose_name = "Lehnwort"
        verbose_name_plural = "Lehnwörter"
        ordering = ["beleg", "number"]

    def __str__(self):
        return f"{self.pron} ({self.beleg})"

    def save(self, *args, **kwargs):
        if self.orig_xml is not None:
            try:
                doc = TeiReader(self.orig_xml)
            except AttributeError:
                doc = TeiReader(ET.tostring(self.orig_xml).decode("utf-8"))
            for field in self._meta.fields:
                if (
                    hasattr(field, "extra")
                    and "xpath" in field.extra
                    and isinstance(field, (models.CharField, models.TextField))
                    and not getattr(self, field.name)
                ):
                    xpath_expr = field.extra["xpath"]
                    try:
                        nodes = doc.any_xpath(xpath_expr)[0]
                    except IndexError:
                        continue
                    try:
                        value = extract_fulltext(nodes)
                    except AttributeError:
                        value = nodes
                    setattr(self, field.name, value)
        super().save(*args, **kwargs)


class AnmerkungLautung(models.Model):
    """Django model representing a tei:note related to a Lautung object"""

    dboe_id = models.CharField(
        primary_key=True,
        max_length=250,
        verbose_name="DBÖ ID",
        help_text="Kombination of the Beleg-ID and the @n",
    )
    beleg = models.ForeignKey(
        "Beleg",
        verbose_name="Beleg",
        on_delete=models.CASCADE,
        related_name="note_lautung",
    )
    number = models.PositiveIntegerField(default=1, verbose_name="Order number")
    resp = models.CharField(
        choices=RESP_OPTIONS,
        max_length=1,
        default="O",
        verbose_name="Responsible (O/B)",
        help_text="whatever",
    )
    corresp_to = models.CharField(
        blank=True, null=True, max_length=20, verbose_name="Korrespondiert zu"
    )
    content = models.TextField(blank=True, null=True, verbose_name="Anmerkung")
    p_ref = ArrayField(
        models.TextField(blank=True, null=True),
        blank=True,
        default=list,
        verbose_name="Pronunciation reference",
        help_text="Iindicates a reference to the pronunciation(s) of the headword",
    )

    class Meta:
        verbose_name = "Anmerkung (Lautung)"
        verbose_name_plural = "Anmerkungen (Lautung)"
        ordering = ["beleg", "number"]

    def __str__(self):
        return f"{self.dboe_id}"


class Sense(models.Model):
    """
    Django model representing a tei:sense node.
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
        related_name="bedeutungen",
    )
    number = models.PositiveIntegerField(default=1, verbose_name="Order number")
    orig_xml = XMLField(verbose_name="XML Node", help_text="tei:sense node")
    definition = models.TextField(
        blank=True, null=True, verbose_name="definition"
    ).set_extra(xpath="./tei:def", node_type="text")
    corresp_to = models.CharField(
        blank=True, null=True, max_length=20, verbose_name="Korrespondiert zu"
    ).set_extra(xpath="./@corresp", node_type="attribute")
    definition_lang = models.CharField(
        max_length=3,
        choices=LANG_CHOICES,
        blank=True,
        null=True,
        verbose_name="Sprache (Definition)",
    ).set_extra(xpath="./tei:def/@xml:lang", node_type="attribute")
    note_anmerkung_o = models.TextField(
        blank=True,
        null=True,
        verbose_name="Anmerkung: O",
        help_text="Whatever",
    ).set_extra(xpath="./tei:note[@type='anmerkung' and @resp='O']", node_type="text")
    note_anmerkung_b = models.TextField(
        blank=True,
        null=True,
        verbose_name="Anmerkung: B",
        help_text="Whatever",
    ).set_extra(xpath="./tei:note[@type='anmerkung' and @resp='B']", node_type="text")

    class Meta:
        verbose_name = "Bedeutung"
        verbose_name_plural = "Bedeutungen"
        ordering = ["beleg", "number"]

    def __str__(self):
        return f"{self.definition[:25]} ... ({self.beleg})"

    def save(self, *args, **kwargs):
        if self.orig_xml is not None:
            try:
                doc = TeiReader(self.orig_xml)
            except AttributeError:
                doc = TeiReader(ET.tostring(self.orig_xml).decode("utf-8"))
            for field in self._meta.fields:
                if (
                    hasattr(field, "extra")
                    and "xpath" in field.extra
                    and isinstance(field, (models.CharField, models.TextField))
                    and not getattr(self, field.name)
                ):
                    xpath_expr = field.extra["xpath"]
                    try:
                        nodes = doc.any_xpath(xpath_expr)[0]
                    except IndexError:
                        continue
                    try:
                        value = extract_fulltext(nodes)
                    except AttributeError:
                        value = nodes
                    setattr(self, field.name, value)
        super().save(*args, **kwargs)


class Beleg(models.Model):
    """
    A Beleg entry from the DBÖ (Dictionary of Bavarian Dialects in Austria) database.
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
    ).set_extra(xpath="./tei:form[@type='hauptlemma'][1]/tei:orth", node_type="text")
    nebenlemma = models.CharField(
        blank=True, null=True, max_length=250, verbose_name="Nebenlemma"
    ).set_extra(xpath="./tei:form[@type='nebenlemma']/tei:orth", node_type="text")
    archivzeile = models.CharField(
        blank=True, null=True, max_length=250, verbose_name="Archivzeile"
    ).set_extra(xpath="./tei:ref[@type='archiv']", node_type="text")
    quelle = models.CharField(
        blank=True, null=True, max_length=250, verbose_name="Quelle"
    ).set_extra(xpath="./tei:ref[@type='quelle']", node_type="text")
    quelle_page = models.CharField(
        blank=True, null=True, max_length=250, verbose_name="Seite"
    ).set_extra(
        xpath="./tei:ref[@type='quelle']/tei:ref[@type='seite']", node_type="text"
    )
    quelle_bearbeitet = models.CharField(
        blank=True, null=True, max_length=250, verbose_name="Quelle bearbeitet"
    ).set_extra(xpath="./tei:ref[@type='quelleBearbeitet']", node_type="text")
    bibl = models.CharField(
        blank=True, null=True, max_length=250, verbose_name="Literatur"
    ).set_extra(xpath="./tei:ref[@type='bibl']/tei:bibl", node_type="text")
    zitierweise = ArrayField(
        models.CharField(blank=True, max_length=250, null=True),
        blank=True,
        default=list,
        verbose_name="Zitierweise",
        help_text="whatever",
    ).set_extra(xpath="./tei:ref[@type='zitiereweise']/tei:bibl", node_type="list")
    pos = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        verbose_name="POS",
        choices=POS_CHOICES,
    ).set_extra(xpath="./tei:gramGrp/tei:pos", node_type="text")
    ort = models.ForeignKey(
        "Ort",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Ort",
    ).set_extra(xpath="./tei:place[@type='Ort']/tei:idno", node_type="text")
    ref_type_dbo = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        verbose_name="Verweis (ref/@type='dbo')",
    ).set_extra(xpath=".//tei:ref[@type='dbo']", node_type="text")
    ref_type_sni = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        verbose_name="Verweis (ref/@type='sni')",
    ).set_extra(xpath="./tei:ref[@type='sni']", node_type="text")
    xr_type_verweise_o = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        verbose_name="Verweis (xr/@type='verweise' and @resp='O')",
    ).set_extra(xpath="./tei:xr[@type='verweise' and @resp='O']", node_type="text")
    xr_type_verweise_b = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        verbose_name="Verweis (xr/@type='verweise' and @resp='B')",
    ).set_extra(xpath="./tei:xr[@type='verweise' and @resp='B']", node_type="text")
    fragebogen_nummer = models.TextField(
        blank=True,
        null=True,
        verbose_name="Fragebogen Nummer",
        help_text="Whatever",
    ).set_extra(xpath="./tei:ref[@type='fragebogenNummer']", node_type="text")
    etym = ArrayField(
        models.TextField(blank=True, null=True),
        blank=True,
        default=list,
        verbose_name="Etymologie",
        help_text="whatever",
    ).set_extra(xpath="./tei:etym", node_type="list")
    note_notabene = ArrayField(
        models.TextField(blank=True, null=True),
        blank=True,
        default=list,
        verbose_name="Notabene",
        help_text="whatever",
    ).set_extra(xpath="./tei:note[@type='notabene']", node_type="list")
    note_diverse = ArrayField(
        models.TextField(blank=True, null=True),
        blank=True,
        default=list,
        verbose_name="Anmerkung (diverse)",
        help_text="whatever",
    ).set_extra(xpath="./tei:note[@type='diverse']", node_type="list")
    facsimile = models.ManyToManyField(
        "Facsimile",
        blank=True,
        verbose_name="Faksimiles",
        help_text="whatever",
        related_name="belege",
    )
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

    def save(
        self,
        add_citations=False,
        add_places=False,
        add_lautungen=False,
        add_sense=False,
        add_anmkerung_laut=False,
        add_lehnwort=False,
        *args,
        **kwargs,
    ):
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

        if self.orig_xml is not None:
            self.import_issue = False
            try:
                doc = TeiReader(self.orig_xml)
            except AttributeError:
                doc = TeiReader(ET.tostring(self.orig_xml).decode("utf-8"))
            for field in self._meta.fields:
                if (
                    hasattr(field, "extra")
                    and "xpath" in field.extra
                    and isinstance(field, (models.CharField, models.TextField))
                    and not getattr(self, field.name)
                ):
                    if self.orig_xml is not None:
                        xpath_expr = field.extra["xpath"]
                        try:
                            nodes = doc.any_xpath(xpath_expr)[0]
                        except IndexError:
                            continue
                        try:
                            value = extract_fulltext(nodes)
                        except AttributeError:
                            value = nodes
                        if isinstance(field, models.CharField):
                            if field.max_length and len(value) > field.max_length:
                                value = value[: field.max_length]
                                self.import_issue = True
                        if isinstance(field, (models.CharField, models.TextField)):
                            value = value.strip()
                        setattr(self, field.name, value)
                if isinstance(field, ArrayField) and not getattr(self, field.name):
                    xpath_expr = field.extra["xpath"]
                    try:
                        nodes = doc.any_xpath(xpath_expr)
                    except IndexError:
                        continue
                    values = []
                    for node in nodes:
                        try:
                            value = extract_fulltext(node)
                        except AttributeError:
                            value = node
                        if isinstance(value, str):
                            value = value.strip()
                        values.append(value)
                    setattr(self, field.name, values)
        if self.orig_xml is not None and add_anmkerung_laut:
            items = doc.any_xpath(
                "./tei:note[@type='anmerkung' and @resp and @corresp]"
            )
            for i, item in enumerate(items, start=1):

                try:
                    number = item.attrib["number"]
                except KeyError:
                    number = i
                dboe_id = f"{self.dboe_id}_{number:0>2}"
                item_object, _ = AnmerkungLautung.objects.get_or_create(
                    dboe_id=dboe_id, beleg=self
                )
                item_object.number = number
                item_object.corresp_to = item.attrib["corresp"]
                item_object.resp = item.attrib["resp"]
                item_object.content = extract_fulltext(item)
                p_refs = []
                for x in item.xpath(".//tei:pRef", namespaces=NSMAP):
                    p_refs.append(extract_fulltext(x))
                item_object.p_ref = p_refs
                try:
                    item_object.save()
                except Exception as e:
                    print(f"Error saving AnmerkungLautung {dboe_id}: {e}")
        if self.orig_xml is not None and add_citations:
            items = doc.any_xpath("./tei:cit")
            for item in items:
                xml_id = get_xmlid(item)
                number = item.attrib["n"]
                orig_xml = ET.tostring(item, encoding="unicode")
                try:
                    item = Citation.objects.get(dboe_id=xml_id)
                except Citation.DoesNotExist:
                    item = Citation(
                        dboe_id=xml_id, beleg=self, number=number, orig_xml=orig_xml
                    )
                try:
                    item.save()
                except Exception as e:
                    print(f"Error saving citation {xml_id}: {e}")
        if self.orig_xml is not None and add_lautungen:
            items = doc.any_xpath("./tei:form[@type='lautung']")
            for item in items:
                xml_id = get_xmlid(item)
                try:
                    number = item.attrib["n"]
                except KeyError:
                    number = 1
                orig_xml = ET.tostring(item, encoding="unicode")
                try:
                    item = Lautung.objects.get(dboe_id=xml_id)
                except Lautung.DoesNotExist:
                    item = Lautung(
                        dboe_id=xml_id, beleg=self, number=number, orig_xml=orig_xml
                    )
                try:
                    item.save()
                except Exception as e:
                    print(f"Error saving lautung {xml_id}: {e}")
        if self.orig_xml is not None and add_lehnwort:
            items = doc.any_xpath("./tei:form[@type='lehnwort']")
            for item in items:
                xml_id = get_xmlid(item)
                try:
                    number = item.attrib["n"]
                except KeyError:
                    number = 1
                orig_xml = ET.tostring(item, encoding="unicode")
                try:
                    item = LehnWort.objects.get(dboe_id=xml_id)
                except LehnWort.DoesNotExist:
                    item = LehnWort(
                        dboe_id=xml_id, beleg=self, number=number, orig_xml=orig_xml
                    )
                try:
                    item.save()
                except Exception as e:
                    print(f"Error saving LehnWort {xml_id}: {e}")
        if self.orig_xml is not None and add_sense:
            items = doc.any_xpath("./tei:sense")
            for i, item in enumerate(items, start=1):
                xml_id = get_xmlid(item)
                number = i
                orig_xml = ET.tostring(item, encoding="unicode")
                try:
                    item = Sense.objects.get(dboe_id=xml_id)
                except Sense.DoesNotExist:
                    item = Sense(
                        dboe_id=xml_id, beleg=self, number=number, orig_xml=orig_xml
                    )
                try:
                    item.save()
                except Exception as e:
                    print(f"Error saving sense {xml_id}: {e}")
        if self.orig_xml is not None and add_places:
            xpath = self._meta.get_field("ort").extra.get("xpath", None)
            try:
                sigle = doc.any_xpath(xpath)[0].text
                try:
                    ort = Ort.objects.get(sigle=sigle)
                    self.ort = ort
                except Ort.DoesNotExist:
                    print(f"Ort with sigle {sigle} does not exist")
                    pass
            except IndexError:
                pass
        super().save(*args, **kwargs)
