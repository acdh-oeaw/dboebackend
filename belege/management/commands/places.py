import os
from csae_pyutils import load_json

from django.core.management.base import BaseCommand
from belege.models import BundesLand, GRegion, KRegion, Ort


class Command(BaseCommand):
    help = "imports places"

    def handle(self, *args, **options):
        data = load_json(os.path.join("data", "places.json"))
        print("Processing Bundesländer")
        for key, value in data.items():
            if len(key) == 7:
                item, _ = BundesLand.objects.get_or_create(
                    sigle=value["Bundesland"]["idno"], abbr=value["Bundesland"]["label"]
                )
        print("Processing Großregionen")
        for key, value in data.items():
            if len(key) == 9:
                item, _ = GRegion.objects.get_or_create(
                    sigle=value["Großregion"]["idno"], abbr=value["Großregion"]["label"]
                )
                try:
                    bl = BundesLand.objects.get(sigle=value["Bundesland"]["idno"])
                except BundesLand.DoesNotExist:
                    continue
                item.bundesland = bl
                item.save()
        print("Processing Kleinregionen")
        for key, value in data.items():
            if len(key) == 10:
                try:
                    item, _ = KRegion.objects.get_or_create(
                        sigle=value["Kleinregion"]["idno"],
                        abbr=value["Kleinregion"]["label"],
                    )
                except Exception as e:
                    print(
                        f'Error creating KRegion: {e} {value["Kleinregion"]["label"]}'
                    )
                    continue
                try:
                    bl = BundesLand.objects.get(sigle=value["Bundesland"]["idno"])
                except BundesLand.DoesNotExist:
                    bl = None
                try:
                    gregion = GRegion.objects.get(sigle=value["Großregion"]["idno"])
                except GRegion.DoesNotExist:
                    gregion = None
                item.gregion = gregion
                item.bundesland = bl
                item.save()
        print("Processing Orte")
        for key, value in data.items():
            if len(key) > 10:
                item, _ = Ort.objects.get_or_create(
                    sigle=value["Ort"]["idno"], name=value["Ort"]["label"]
                )
                try:
                    bl = BundesLand.objects.get(sigle=value["Bundesland"]["idno"])
                except BundesLand.DoesNotExist:
                    bl = None
                try:
                    gregion = GRegion.objects.get(sigle=value["Großregion"]["idno"])
                except GRegion.DoesNotExist:
                    gregion = None
                try:
                    kregion = KRegion.objects.get(sigle=value["Kleinregion"]["idno"])
                except KRegion.DoesNotExist:
                    kregion = None
                item.gregion = gregion
                item.kregion = kregion
                item.bundesland = bl
                item.save()

        print("done")
