from django.core.management.base import BaseCommand
from tqdm import tqdm

from belege.models import Beleg


class Command(BaseCommand):
    help = "saves all Beleg objects"

    def handle(self, *args, **options):
        total = Beleg.objects.count()
        for x in tqdm(Beleg.objects.iterator(), total=total):
            try:
                x.save(trigger_index=False)
            except Exception as e:
                print(f"failed to save {x} due to {e}")
                x.import_issue = True
                x.save()
        print("done")
