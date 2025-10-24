from typing import Iterable

from django.db.models.query import QuerySet


def transform_record(raw: dict) -> dict:
    out = {}
    for key, v in raw.items():
        # Normalize QuerySets explicitly
        if isinstance(v, QuerySet):
            v = list(v)
        # Some Django related managers may appear (e.g. ManyRelatedManager);
        # catch generic iterables except strings/bytes
        elif (
            not isinstance(v, (str, bytes, list, dict))
            and hasattr(v, "__iter__")
            and not isinstance(v, Iterable)  # narrow - safety; Iterable imported
        ):
            # Fallback path (likely not hit often)
            try:
                v = list(v)  # type: ignore[arg-type]
            except Exception:
                pass

        if key == "id":
            # Keep primary key as-is (string)
            out[key] = str(v)
        elif v in ("", None, []):
            out[key] = []
        elif hasattr(v, "exists") and callable(getattr(v, "exists")) and not v.exists():
            out[key] = []
        elif isinstance(v, list):
            # Coerce every element to string for Typesense
            out[key] = [str(x) for x in v if x not in (None, "")]
        else:
            out[key] = [str(v)]
    return out
