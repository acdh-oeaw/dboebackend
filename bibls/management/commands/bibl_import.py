import os

import pandas as pd
from django.core.management.base import BaseCommand
from tqdm import tqdm

from bibls.models import BibliographicItem, BibliographicType


class Command(BaseCommand):
    help = "import bibls from dbo_sources.csv"

    def handle(self, *args, **options):
        df = pd.read_csv(os.path.join("bibls", "data", "dbo_sources.csv")).fillna("")

        additional_types = [
            {
                "main_type": "Erhebung",
                "sub_type": "große_Fragebögen",
                "specification": "",
            },
            {
                "main_type": "Erhebung",
                "sub_type": "Ergänzungsfragebögen",
                "specification": "",
            },
            {"main_type": "Erhebung", "sub_type": "Kundfahrten", "specification": ""},
            {
                "main_type": "Erhebung",
                "sub_type": "Fragebucherhebungen",
                "specification": "",
            },
            {
                "main_type": "Sonstige",
                "sub_type": "Sonstige",
                "specification": "Sonstige",
            },
        ]

        for x in additional_types:
            BibliographicType.objects.get_or_create(**x)

        for i, row in tqdm(df.iterrows(), total=len(df)):
            bibl_type, _ = BibliographicType.objects.get_or_create(
                main_type=row["Quelle_Typ"],
                sub_type=row["Quelle_Subtyp"],
                specification=row["Quelle_Spezifikation"],
            )
            try:
                bibl_item, _ = BibliographicItem.objects.get_or_create(
                    sigle=row["ID"],
                    short_title=row["Kürzel"],
                    full_title=row["Titel"],
                    bibl_type=bibl_type,
                )
            except Exception as e:
                print(row["ID"], e)
                break
            bibl_item.year = row["Jahr"]
            bibl_item.volume = row["Band"]
            bibl_item.author_last_name = row["Autor - Nachname"]
            bibl_item.author_first_name = row["Vorname"]
            bibl_item.place = row["Ort"]
            bibl_item.publisher = row["Verlag"]
            bibl_item.comment = row["Kommentar"]
            bibl_item.internal_node = row["Anmerkung"]
            try:
                bibl_item.save()
            except Exception as e:
                print(row["ID"], e)
                break
