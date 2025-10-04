import json
import os

import typesense
from django.conf import settings
from django.core.management.base import BaseCommand
from tqdm import tqdm
from typesense.exceptions import ObjectAlreadyExists

from belege.models import Beleg
from belege.search_utils import belege_schema

beleg_json_dir = os.path.join(settings.MEDIA_ROOT, "belege")
os.makedirs(beleg_json_dir, exist_ok=True)

COLLECTION_NAME = "dboe_belege"
TYPESENSE_API_KEY = os.environ.get("TYPESENSE_API_KEY", "xyz")
TYPESENSE_TIMEOUT = os.environ.get("TYPESENSE_TIMEOUT", "120")
TYPESENSE_HOST = os.environ.get("TYPESENSE_HOST", "localhost")
TYPESENSE_PORT = os.environ.get("TYPESENSE_PORT", "8108")
TYPESENSE_PROTOCOL = os.environ.get("TYPESENSE_PROTOCOL", "http")
client = typesense.Client(
    {
        "nodes": [
            {
                "host": TYPESENSE_HOST,
                "port": TYPESENSE_PORT,
                "protocol": TYPESENSE_PROTOCOL,
            }
        ],
        "api_key": TYPESENSE_API_KEY,
        "connection_timeout_seconds": int(TYPESENSE_TIMEOUT),
    }
)


class Command(BaseCommand):
    help = "indexing Belege"

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch-size",
            type=int,
            default=5000,
            help="Number of records per JSON batch file (default: 5000)",
        )
        parser.add_argument(
            "--dump",
            action="store_true",
            default=False,
            help="Write batch files to disk (default: False)",
        )

    def handle(self, *args, **options):
        try:
            client.collections.create(belege_schema)
        except ObjectAlreadyExists:
            print("Collection already exists, skipping creation.")

        cur_nr = 0
        total = Beleg.objects.count()
        batch_size = options.get("batch_size") or 5000
        dump_to_file = options.get("dump", False)
        if batch_size <= 0:
            raise ValueError("batch-size must be a positive integer")
        cur_nr + 1  # used for file numbering
        batch = []
        for x in tqdm(Beleg.objects.iterator(), total=total):
            cur_nr += 1
            try:
                batch.append(x.create_typesense_object())
            except Exception as e:
                print(f"failed to serialize {x} due to {e}")
                continue

            # If we reached the batch size, flush to disk
            if len(batch) >= batch_size:
                if dump_to_file:
                    out_file = f"belege_{cur_nr:05}.json"
                    save_path = os.path.join(beleg_json_dir, out_file)
                    with open(save_path, "w", encoding="utf-8") as fp:
                        json.dump(batch, fp, ensure_ascii=False)
                    print(f"wrote {len(batch)} records to {save_path}")
                update = client.collections[COLLECTION_NAME].documents.import_(
                    batch, {"return_json": True, "action": "upsert"}
                )
                errors = [r for r in update if not r["success"]]
                if errors:
                    print(f"{len(errors)} documents failed to import")
                    for err in errors:
                        print(err)
                else:
                    print(f"All good updating batch {cur_nr:05}")
                cur_nr += 1
                batch = []

        # Flush remaining records (if any)
        if batch:
            if dump_to_file:
                out_file = f"belege_{cur_nr:05}.json"
                save_path = os.path.join(beleg_json_dir, out_file)

                with open(save_path, "w", encoding="utf-8") as fp:
                    json.dump(batch, fp, ensure_ascii=False)
                print(f"wrote final {len(batch)} records to {save_path}")
            update = client.collections[COLLECTION_NAME].documents.import_(
                batch, {"return_json": True, "action": "upsert"}
            )
            errors = [r for r in update if not r["success"]]
            if errors:
                print(f"{len(errors)} documents failed to import")
                for err in errors:
                    print(err)
            else:
                print(f"All good updating batch {cur_nr:05}")
        print("done (all batches written)")
