import requests
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from tqdm import tqdm

from belege.models import Beleg


class Command(BaseCommand):
    help = "imports facs"

    def handle(self, *args, **options):
        facs_source = "https://raw.githubusercontent.com/lapis-project/dboe2arche/refs/heads/main/facs.json"
        print(f"fetching data from {facs_source}")
        data = requests.get(facs_source).json()
        print(f"processing {len(data)} entries")
        for key, value in tqdm(data.items(), total=len(data)):
            try:
                item = Beleg.objects.get(dboe_id=key)
            except ObjectDoesNotExist:
                print(f"{key} does not exist")
                continue
            item.scan = value
            item.save(trigger_index=False)
        print(f"done, updated {len(data)} Belege")
