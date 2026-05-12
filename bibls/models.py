from django.db import models

BIBL_MAIN_TYPE = (
    ("Literatur", "Literatur"),
    ("Erhebung", "Erhebung"),
    ("Sonstige", "Sonstige"),
)

BIBL_SUB_TYPE = (
    ("Fachliteratur", "Fachliteratur"),
    ("Journalit.Text", "Journalistischer Text"),
    ("Literar.Text", "Literarischer Text"),
    ("große_Fragebögen", "große Fragebögen"),
    ("Ergänzungsfragebögen", "Ergänzungsfragebögen"),
    ("Kundfahrten", "Kundfahrten"),
    ("Fragebucherhebungen", "Fragebucherhebungen"),
)

BIBL_SPECIFICATION = (
    ("Dissertation", "Dissertation"),
    ("Gedichte", "Gedicht"),
    ("Lexikon", "Lexikon"),
    ("Lieder", "Lied"),
    ("Prosa", "Prosa"),
    ("Wiss.Zeitschrift", "Wissenschaftliche Zeitschrift"),
    ("Wiss.Zeitschriftenartikel", "Wissenschaftlicher Zeitschriftenartikel"),
    ("Wörterbuch", "Wörterbuch"),
    ("Zeitung", "Zeitung"),
    ("Sonstige", "Sonstige"),
)


class BibliographicType(models.Model):
    main_type = models.CharField(
        max_length=50, choices=BIBL_MAIN_TYPE, verbose_name="Quelle Type"
    )
    sub_type = models.CharField(
        max_length=50,
        choices=BIBL_SUB_TYPE,
        blank=True,
        null=True,
        verbose_name="Quelle Subtype",
    )
    specification = models.CharField(
        max_length=50,
        choices=BIBL_SPECIFICATION,
        blank=True,
        null=True,
        verbose_name="Quelle Spezifikation",
    )

    class Meta:
        verbose_name = "Art der Quelle"
        verbose_name_plural = "Arten der Quellen"
        ordering = ["main_type", "sub_type", "specification"]

    def __str__(self):
        if self.sub_type and self.specification:
            return " >> ".join([self.main_type, self.sub_type, self.specification])
        elif self.sub_type:
            return " >> ".join([self.main_type, self.sub_type])
        else:
            return self.main_type


class BibliographicItem(models.Model):
    sigle = models.CharField(
        primary_key=True,
        max_length=50,
        verbose_name="Sigle",
        help_text="Sigle (ID). Darf nur einmal verwendet werden",
    )
    short_title = models.CharField(
        max_length=100, verbose_name="Kürzel", help_text="Kurztitel"
    )
    full_title = models.CharField(
        max_length=500, verbose_name="Titel", help_text="Volltitel"
    )
    bibl_type = models.ForeignKey(
        "BibliographicType", verbose_name="Art der Quelle", on_delete=models.CASCADE
    )
    year = models.CharField(max_length=50, verbose_name="Jahr", blank=True, null=True)
    volume = models.CharField(
        max_length=100,
        verbose_name="Band",
        help_text="Angabe zum Band, z.B: 'Band 1: Italienisch–Deutsch' oder '[I. Heft] 2., verm. Aufl.'",
        blank=True,
        null=True,
    )
    author_last_name = models.CharField(
        max_length=150,
        verbose_name="Autor (Nachname)",
        help_text="Bei mehreren Autor*Innen: 'Benecke/Müller/Zarncke'",
        blank=True,
        null=True,
    )
    author_first_name = models.CharField(
        max_length=100,
        verbose_name="Autor (Vorname)",
        help_text="Bei mehreren Autor*Innen 'Georg Friedrich/Wilhelm/Friedrich'",
        blank=True,
        null=True,
    )
    place = models.CharField(
        max_length=100,
        verbose_name="Ort",
        help_text="Bei mehreren Orten: 'Innsbruck / München'",
        blank=True,
        null=True,
    )
    publisher = models.CharField(
        max_length=200,
        verbose_name="Verlag",
        help_text="Verlag, z.B: 'De Gruyter' oder 'Dissertationen der Universität Wien'",
        blank=True,
        null=True,
    )
    comment = models.TextField(verbose_name="Kommentar", blank=True, null=True)
    in_zotero = models.BooleanField(
        default=False,
        verbose_name="Zotero Eintrag vorhanden?",
        help_text="Wird automatisch gesetzt",
    )
    zotero_key = models.URLField(
        max_length=150,
        verbose_name="Zotero URL",
        help_text="z.B. 'https://www.zotero.org/groups/12345/dboe/items/AWYHCEMA'",
        blank=True,
        null=True,
    )
    internal_node = models.TextField(
        verbose_name="interne Anmerkung", blank=True, null=True
    )

    class Meta:
        verbose_name = "Bibliographische Angabe"
        verbose_name_plural = "Bibliographische Angaben"
        ordering = ["sigle"]

    def __str__(self):
        return self.short_title

    def save(self, *args, **kwargs):
        if self.zotero_key is not None:
            self.in_zotero = True
        super().save(*args, **kwargs)
