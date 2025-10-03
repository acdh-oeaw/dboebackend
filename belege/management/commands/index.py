import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from tqdm import tqdm

from belege.models import Beleg

beleg_json_dir = os.path.join(settings.MEDIA_ROOT, "belege")
os.makedirs(beleg_json_dir, exist_ok=True)


class Command(BaseCommand):
    help = "indexing Belege"

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch-size",
            type=int,
            default=5000,
            help="Number of records per JSON batch file (default: 5000)",
        )

    def handle(self, *args, **options):
        cur_nr = 0
        total = Beleg.objects.count()
        batch_size = options.get("batch_size") or 5000
        if batch_size <= 0:
            raise ValueError("batch-size must be a positive integer")
        cur_nr + 1  # used for file numbering
        batch = []
        # Iterate lazily over all Beleg instances
        for x in tqdm(Beleg.objects.iterator(), total=total):
            cur_nr += 1
            # Collect the processed Typesense object
            try:
                batch.append(x.create_typesense_object())
            except Exception as e:
                print(f"failed to serialize {x} due to {e}")
                continue

            # If we reached the batch size, flush to disk
            if len(batch) >= batch_size:
                out_file = f"belege_{cur_nr:05}.json"
                save_path = os.path.join(beleg_json_dir, out_file)
                with open(save_path, "w", encoding="utf-8") as fp:
                    json.dump(batch, fp, ensure_ascii=False)
                print(f"wrote {len(batch)} records to {save_path}")
                cur_nr += 1
                batch = []

        # Flush remaining records (if any)
        if batch:
            out_file = f"belege_{cur_nr:05}.json"
            save_path = os.path.join(beleg_json_dir, out_file)

            with open(save_path, "w", encoding="utf-8") as fp:
                json.dump(batch, fp, ensure_ascii=False)
            print(f"wrote final {len(batch)} records to {save_path}")
        print("done (all batches written)")
