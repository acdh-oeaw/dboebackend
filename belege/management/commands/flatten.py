from django.core.management.base import BaseCommand
from tqdm import tqdm

from belege.models import Beleg


class Command(BaseCommand):
    help = "creates flattend Beleg instances"

    def handle(self, *args, **options):
        total = Beleg.objects.count()
        for x in tqdm(Beleg.objects.iterator(), total=total):
            if x.flatten_beleg.all():
                continue
            try:
                x.create_beleg_flatten_copy()
            except Exception as e:
                print(f"failed to created flattend object from {x} due to {e}")
        print("done")
