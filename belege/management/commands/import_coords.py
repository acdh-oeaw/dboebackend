import json
from pathlib import Path
from tqdm import tqdm
from django.core.management.base import BaseCommand

from django.conf import settings
from belege.models import BundesLand, GRegion, KRegion, Ort


class Command(BaseCommand):
    help = "import coordinates for places"

    def handle(self, *args, **options):

        data_dir = Path(settings.MEDIA_ROOT) / "geojson"
        mapping = {
            "bundesland.json": BundesLand,
            "gregion.json": GRegion,
            "kregion.json": KRegion,
            "ort.json": Ort,
        }
        for key, value in mapping.items():
            with open(data_dir / key, encoding="utf-8") as f:
                data = json.load(f)
            print(f"processing {value._meta.verbose_name_plural}")
            for x in tqdm(data["features"]):
                props = x["properties"]
                sigle = props["sigle"]
                coords = x["geometry"]["coordinates"]
                try:
                    abbr = props["Name"]
                except KeyError:
                    abbr = props["name"]
                try:
                    name = props["NAME_D"]
                    if not name:
                        name = props["name"]
                except KeyError:
                    name = None
                cur_item, _ = value.objects.get_or_create(sigle=sigle)
                cur_item.abbr = abbr
                cur_item.coordinates = coords
                if name:
                    cur_item.name = name
                cur_item.save()
        print("done")
