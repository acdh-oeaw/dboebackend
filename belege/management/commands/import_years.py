import json
import os

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from tqdm import tqdm

from belege.models import Beleg


class Command(BaseCommand):
    help = "imports places"

    def handle(self, *args, **options):
        with open(os.path.join("data", "years.json"), "r", encoding="utf-8") as fp:
            data = json.load(fp)

        for key, value in tqdm(data.items(), total=len(data)):
            try:
                item = Beleg.objects.get(dboe_id=key)
            except ObjectDoesNotExist:
                print(f"{key} does not exist")
                continue
            if item.year:
                continue
            item.year = value
            item.save()
        print(f"done, updated {len(data)} Belege")
