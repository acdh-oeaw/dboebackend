from django.core.management.base import BaseCommand
from tqdm import tqdm

from belege.models import Beleg


class Command(BaseCommand):
    help = "updates all Beleg-Zettel"

    def handle(self, *args, **options):
        total = Beleg.objects.count()
        for x in tqdm(Beleg.objects.iterator(), total=total):
            try:
                x.save(
                    add_citations=False,
                    add_places=False,
                    add_lautungen=False,
                    add_sense=False,
                    add_anmkerung_laut=False,
                    add_lehnwort=False,
                )
            except Exception as e:
                print(f"failed to save {x} due to {e}")
                x.import_issue = True
                x.save()
        print("done")
