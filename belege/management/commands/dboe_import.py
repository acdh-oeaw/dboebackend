import glob
import lxml.etree as ET
from tqdm import tqdm
from django.core.management.base import BaseCommand
from belege.models import BelegSimple

from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import get_xmlid


class Command(BaseCommand):
    help = "imports dboe xmls"

    def handle(self, *args, **options):
        files = glob.glob("/home/csae8092/repos/dboe/legacy-data/orig-files/*xml")

        for x in tqdm(files):
            doc = TeiReader(x)
            items = doc.any_xpath(".//tei:entry")
            for entry in items:
                xml_id = get_xmlid(entry)
                node_as_text = ET.tostring(entry, encoding='unicode')
                BelegSimple.objects.create(dboe_id=xml_id, simple_xml=node_as_text)
