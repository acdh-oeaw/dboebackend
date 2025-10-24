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
            default=1000,
            help="Number of records per JSON batch file (default: 1000)",
        )
        parser.add_argument(
            "--dump",
            action="store_true",
            default=False,
            help="Write batch files to disk (default: False)",
        )

    def handle(self, *args, **options):
        cur_nr = 0
        total = Beleg.objects.count()
        batch_size = options.get("batch_size") or 5000
        dump_to_file = options.get("dump", False)
        if batch_size <= 0:
            raise ValueError("batch-size must be a positive integer")
        batch = []
        for x in tqdm(Beleg.objects.iterator(), total=total):
            cur_nr += 1
            try:
                batch.append(x.sanitize_representation())
            except Exception as e:
                print(f"failed to serialize {x} due to {e}")
                continue
            if len(batch) >= batch_size:
                if dump_to_file:
                    out_file = f"belege_{cur_nr:05}.json"
                    save_path = os.path.join(beleg_json_dir, out_file)
                    with open(save_path, "w", encoding="utf-8") as fp:
                        json.dump(batch, fp, ensure_ascii=False)
                    print(f"wrote {len(batch)} records to {save_path}")
                batch = []

        # Flush remaining records (if any)
        if batch:
            if dump_to_file:
                out_file = f"belege_{cur_nr:05}.json"
                save_path = os.path.join(beleg_json_dir, out_file)
                with open(save_path, "w", encoding="utf-8") as fp:
                    json.dump(batch, fp, ensure_ascii=False)
                print(f"wrote final {len(batch)} records to {save_path}")
        print("done (all batches written)")
