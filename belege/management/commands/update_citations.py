from tqdm import tqdm
from django.core.management.base import BaseCommand
from belege.models import Citation


class Command(BaseCommand):
    help = "saves all Citation-Objects"

    def handle(self, *args, **options):
        total = Citation.objects.count()
        for x in tqdm(Citation.objects.iterator(), total=total):
            try:
                x.save(add_zusatzlemma=True)
            except Exception as e:
                print(f"failed to save {x} due to {e}")
                continue
        print("done")
