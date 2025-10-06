import xml.etree.ElementTree as ET

from acdh_tei_pyutils.tei import TeiReader
from django.core.management.base import BaseCommand
from tqdm import tqdm

from belege.models import (
    Beleg,
    BundesLand,
    GeoRelationBundesland,
    GeoRelationGregion,
    GeoRelationKregion,
    GeoRelationOrt,
    GRegion,
    KRegion,
    Ort,
)

namespaces = {"tei": "http://www.tei-c.org/ns/1.0"}


class Command(BaseCommand):
    help = "updates all Beleg-Zettel"

    def handle(self, *args, **options):
        mapping = {
            "Kleinregion": [GeoRelationKregion, KRegion],
            "Großregion": [GeoRelationGregion, GRegion],
            "Bundesland": [GeoRelationBundesland, BundesLand],
            "Ort": [GeoRelationOrt, Ort],
        }
        total = Beleg.objects.count()
        for item in tqdm(Beleg.objects.iterator(), total=total):
            doc = TeiReader(ET.tostring(item.orig_xml).decode("utf-8"))
            try:
                for x in doc.any_xpath(".//tei:usg"):
                    try:
                        corresp = x.attrib["corresp"]
                    except KeyError:
                        corresp = None
                    try:
                        y = x.xpath(".//tei:place", namespaces=namespaces)[-1]
                    except IndexError:
                        continue
                    place_type = y.attrib["type"]
                    try:
                        place_sigle = y.xpath(
                            "./tei:idno/text()", namespaces=namespaces
                        )[0]
                    except IndexError:
                        continue
                    if place_type in mapping.keys():
                        geo_model, place_model = mapping[place_type]
                        place_obj = place_model.objects.get(sigle=place_sigle)
                        geo_model.objects.get_or_create(
                            beleg=item, ort=place_obj, corresp=corresp
                        )
            except Exception as e:
                print(f"Error in {item}: {e}")
        print("done")
