from typing import Iterable

from django.db.models.query import QuerySet

belege_schema = {
    "name": "dboe_belege",
    "fields": [
        {"name": "id", "type": "string"},  # primary key
        {"name": "hl", "type": "string[]", "facet": True, "optional": True},
        {"name": "nl", "type": "string[]", "facet": True, "optional": True},
        {"name": "qu", "type": "string[]", "facet": True, "optional": True},
        {"name": "bibl", "type": "string[]", "facet": True, "optional": True},
        {"name": "pos", "type": "string[]", "facet": True, "optional": True},
        {"name": "archivzeile", "type": "string[]", "optional": True},
        {"name": "nr", "type": "string[]", "facet": True, "optional": True},
        {"name": "verweis", "type": "string[]", "optional": True},
        {"name": "page", "type": "string[]", "optional": True, "facet": True},
        {"name": "etym", "type": "string[]", "optional": True},
        {"name": "a", "type": "string[]", "optional": True},
        {"name": "lw1", "type": "string[]", "optional": True},
        {"name": "lw2", "type": "string[]", "optional": True},
        {"name": "lw3", "type": "string[]", "optional": True},
        {"name": "lw4", "type": "string[]", "optional": True},
        {"name": "lw5", "type": "string[]", "optional": True},
        {"name": "lw6", "type": "string[]", "optional": True},
        {"name": "lw7", "type": "string[]", "optional": True},
        {"name": "lw8", "type": "string[]", "optional": True},
        # Star / slash normalized array fields
        {"name": "anm_lt_star", "type": "string[]", "optional": True},
        {"name": "anm_kt_star", "type": "string[]", "optional": True},
        {"name": "bd_kt_star", "type": "string[]", "optional": True},
        {"name": "wbd_kt_star", "type": "string[]", "optional": True},
        {"name": "vrw_kt_star", "type": "string[]", "optional": True},
        {"name": "dv_kt_star", "type": "string[]", "optional": True},
        {"name": "bd_lw_star", "type": "string[]", "optional": True},
        {"name": "bd_kt_lt1", "type": "string[]", "optional": True},
        {"name": "kt_lt1", "type": "string[]", "optional": True},
        {"name": "zl1_kt_lt1", "type": "string[]", "optional": True},
        {"name": "zl2_kt_lt1", "type": "string[]", "optional": True},
        {"name": "bd_kt_lt2", "type": "string[]", "optional": True},
        {"name": "kt_lt2", "type": "string[]", "optional": True},
        {"name": "zl1_kt_lt2", "type": "string[]", "optional": True},
        {"name": "zl2_kt_lt2", "type": "string[]", "optional": True},
        {"name": "anm_lw_star", "type": "string[]", "optional": True},
        {"name": "bd_lt_star", "type": "string[]", "optional": True},
        {"name": ".*", "type": "auto"},
    ],
}


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


def normalize_value(value):
    """Convert list values to strings, handle None values."""
    if value is None:
        return ""
    if isinstance(value, list):
        if not value:
            return ""
        # For single item lists, return the first item
        if len(value) == 1:
            return str(value[0]) if value[0] is not None else ""
        # For multiple items, join with separator
        return " | ".join(str(v) for v in value if v is not None)
    return str(value)
