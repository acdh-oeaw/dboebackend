from tqdm import tqdm
from django.core.management.base import BaseCommand

from belege.models import Beleg, Facsimile


class Command(BaseCommand):
    help = "extract facsimile info from beleg-xml"

    def handle(self, *args, **options):
        total = Beleg.objects.count()
        for item in tqdm(Beleg.objects.iterator(), total=total):
            doc = item.orig_xml
            try:
                file_name = doc.xpath("@facs")[0]
            except (IndexError, AttributeError):
                continue
            for x in file_name.split():
                facs, _ = Facsimile.objects.get_or_create(file_name=x)
                item.facsimile.add(facs)
        print("done")
