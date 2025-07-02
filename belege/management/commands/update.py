from tqdm import tqdm
from django.core.management.base import BaseCommand
from belege.models import Beleg


class Command(BaseCommand):
    help = "saves all Beleg-Zettel"

    def handle(self, *args, **options):
        total = Beleg.objects.count()
        for x in tqdm(Beleg.objects.iterator(), total=total):
            try:
                x.save(
                    add_citations=True,
                    add_places=True,
                    add_lautungen=True,
                    add_sense=True,
                )
            except Exception as e:
                print(f"failed to save {x} due to {e}")
                x.import_issue = True
                x.save()
        print("done")
