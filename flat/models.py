from django.db import models

from belege.models import Beleg


class BelegFlatten(models.Model):
    # Basic identifiers
    id = models.CharField(max_length=1000, verbose_name="ID", primary_key=True)
    dboe_id = models.ForeignKey(Beleg, on_delete=models.CASCADE, verbose_name="Beleg")
    nr = models.CharField(max_length=1000, blank=True, null=True, verbose_name="NR")
    hl = models.CharField(max_length=1000, blank=True, null=True, verbose_name="HL")
    nl = models.CharField(max_length=1000, blank=True, null=True, verbose_name="NL")
    pos = models.CharField(max_length=1000, blank=True, null=True, verbose_name="POS")

    # Bedeutung/Lautung and Bedeutung/Kontext
    bd_lt_star = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="BD/LT*"
    )
    bd_kt_star = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="BD/KT*"
    )

    # Lautung (LT) series with Teuthonista and Grammar
    lt1_teuthonista = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="LT1 Teuthonista"
    )
    gram_lt1 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="GRAM/LT1"
    )
    lt2_teuthonista = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="LT2 Teuthonista"
    )
    gram_lt2 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="GRAM/LT2"
    )
    lt3_teuthonista = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="LT3 Teuthonista"
    )
    gram_lt3 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="GRAM/LT3"
    )
    lt4_teuthonista = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="LT4 Teuthonista"
    )
    gram_lt4 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="GRAM/LT4"
    )
    lt5_teuthonista = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="LT5 Teuthonista"
    )
    gram_lt5 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="GRAM/LT5"
    )
    lt6_teuthonista = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="LT6 Teuthonista"
    )
    gram_lt6 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="GRAM/LT6"
    )
    lt7_teuthonista = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="LT7 Teuthonista"
    )
    gram_lt7 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="GRAM/LT7"
    )
    lt8_teuthonista = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="LT8 Teuthonista"
    )
    gram_lt8 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="GRAM/LT8"
    )
    lt9_teuthonista = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="LT9 Teuthonista"
    )
    gram_lt9 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="GRAM/LT9"
    )

    # Anmerkung Lautung
    anm_lt_star = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="ANM/LT*"
    )

    # Kontext (KT) series with additional fields
    kt1 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Kontext 1"
    )
    kl_kt1 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="KL/KT1"
    )
    zl1_kt1 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Zusatzlemma 1/KT1"
    )
    zl2_kt1 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Zusatzlemma 2/KT1"
    )

    kt2 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Kontext 2"
    )
    kl_kt2 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="KL/KT2"
    )
    zl1_kt2 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Zusatzlemma 1/KT2"
    )
    zl2_kt2 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Zusatzlemma 2/KT2"
    )

    kt3 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Kontext 3"
    )
    kl_kt3 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="KL/KT3"
    )
    zl1_kt3 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Zusatzlemma 1/KT3"
    )
    zl2_kt3 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Zusatzlemma 2/KT3"
    )

    kt4 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Kontext 4"
    )
    kl_kt4 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="KL/KT4"
    )
    zl1_kt4 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Zusatzlemma 1/KT4"
    )
    zl2_kt4 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Zusatzlemma 2/KT4"
    )

    kt5 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Kontext 5"
    )
    kl_kt5 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="KL/KT5"
    )
    zl1_kt5 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Zusatzlemma 1/KT5"
    )
    zl2_kt5 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Zusatzlemma 2/KT5"
    )

    kt6 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Kontext 6"
    )
    kl_kt6 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="KL/KT6"
    )
    zl1_kt6 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Zusatzlemma 1/KT6"
    )
    zl2_kt6 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Zusatzlemma 2/KT6"
    )

    kt7 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Kontext 7"
    )
    kl_kt7 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="KL/KT7"
    )
    zl1_kt7 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Zusatzlemma 1/KT7"
    )
    zl2_kt7 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Zusatzlemma 2/KT7"
    )

    kt8 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Kontext 8"
    )
    kl_kt8 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="KL/KT8"
    )
    zl1_kt8 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Zusatzlemma 1/KT8"
    )
    zl2_kt8 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Zusatzlemma 2/KT8"
    )

    # Wortbedeutung
    wbd = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Wortbedeutung"
    )
    wbd_kt_star = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Wortbedeutung/KT*"
    )

    # Ort Lautung
    ort_lt_star = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Ort/LT*"
    )

    # Leitwort (LW) series
    lw1 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Leitwort 1"
    )
    lw2 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Leitwort 2"
    )
    lw3 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Leitwort 3"
    )
    lw4 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Leitwort 4"
    )
    lw5 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Leitwort 5"
    )
    lw6 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Leitwort 6"
    )
    lw7 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Leitwort 7"
    )
    lw8 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Leitwort 8"
    )

    # Bedeutung/Anmerkung/Datenverweis/Ort für Leitwort
    bd_lw_star = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Bedeutung/LW*"
    )
    anm_lw_star = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Anmerkung/LW*"
    )
    dv_lw_star = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Datenverweis/LW*"
    )
    ort_lw_star = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Ort/LW*"
    )

    # Zusatzlemma
    zusatzlemma = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Zusatzlemma"
    )

    # Verweis/Anmerkung/Datenverweis für Kontext
    vrw_kt_star = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Verweis/KT*"
    )
    anm_kt_star = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Anmerkung/KT*"
    )
    dv_kt_star = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Datenverweis/KT*"
    )

    # Kontext/Lautung combinations
    kt_lt1 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Kontext/LT1"
    )
    kl_kt_lt1 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="KL/Kontext/LT1"
    )
    bd_kt_lt1 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Bedeutung/Kontext/LT1"
    )
    wbd_kt_lt1 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Wortbedeutung/Kontext/LT1"
    )
    zl1_kt_lt1 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Zusatzlemma 1/Kontext/LT1"
    )
    zl2_kt_lt1 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Zusatzlemma 2/Kontext/LT1"
    )
    note_kt_lt1 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Note/Kontext/LT1"
    )

    kt_lt2 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Kontext/LT2"
    )
    kl_kt_lt2 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="KL/Kontext/LT2"
    )
    bd_kt_lt2 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Bedeutung/Kontext/LT2"
    )
    wbd_kt_lt2 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Wortbedeutung/Kontext/LT2"
    )
    zl1_kt_lt2 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Zusatzlemma 1/Kontext/LT2"
    )
    zl2_kt_lt2 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Zusatzlemma 2/Kontext/LT2"
    )
    note_kt_lt2 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Note/Kontext/LT2"
    )

    # Kontext/Leitwort combination
    kt_lw1 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Kontext/LW1"
    )
    kl_kt_lw1 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="KL/Kontext/LW1"
    )
    bd_kt_lw1 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Bedeutung/Kontext/LW1"
    )
    wbd_kt_lw1 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Wortbedeutung/Kontext/LW1"
    )
    zl1_kt_lw1 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Zusatzlemma 1/Kontext/LW1"
    )
    zl2_kt_lw1 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Zusatzlemma 2/Kontext/LW1"
    )
    note_kt_lw1 = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Note/Kontext/LW1"
    )

    # Verweis
    verweis = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Verweis"
    )

    def __str__(self):
        return self.id
