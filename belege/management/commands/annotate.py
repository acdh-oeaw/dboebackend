from django.core.management.base import BaseCommand

from belege.models import Citation


class Command(BaseCommand):
    help = "import coordinates for places"

    def handle(self, *args, **options):
        items = Citation.objects.all()
        print(items.count())
