import glob
import lxml.etree as ET
import os
from tqdm import tqdm
from django.core.management.base import BaseCommand
from belege.models import Beleg

from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import get_xmlid


class Command(BaseCommand):
    help = "imports dboe xmls"

    def handle(self, *args, **options):
        files = sorted(glob.glob("/home/csae8092/repos/dboe/legacy-data/orig-files/d178_*.xml"))
        for f, x in enumerate(files, start=1):
            print(f"{f}/{len(files)} files")
            fname = os.path.split(x)[-1]
            doc = TeiReader(x)
            items = doc.any_xpath(".//tei:entry")
            xenos = doc.any_xpath(".//tei:xenoData")
            print(f"processing {len(items)} entries from {fname}")
            for i, entry in tqdm(enumerate(items), total=len(items)):
                xml_id = get_xmlid(entry)
                node_as_text = ET.tostring(entry, encoding='unicode')
                beleg, _ = Beleg.objects.get_or_create(dboe_id=xml_id)
                beleg.orig_xml = node_as_text
                try:
                    beleg.xeno_data = xenos[i].text
                except IndexError:
                    beleg.xeno_data = "NO MATCHING ENTRY FOUND: HANSI4EVER"
                    beleg.import_issue = True
                beleg.save(add_citations=True)
