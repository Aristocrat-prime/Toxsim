"""JSON file integrity and aggregate metadata coverage checks."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

METADATA_FIELDS = ("formula", "mw", "type", "structure", "cid", "source")


def audit_data(path: str | Path) -> dict[str, Any]:
    """Return aggregate file and metadata checks without exposing record values."""
    source = Path(path)
    try:
        raw = source.read_text(encoding="utf-8")
    except OSError as exc:
        return {"ok": False, "path": str(source), "error": str(exc)}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "path": str(source),
            "error": f"Invalid JSON at line {exc.lineno}, column {exc.colno}.",
        }
    if not isinstance(payload, dict):
        return {"ok": False, "path": str(source), "error": "Expected a JSON object containing records."}

    records = [record for record in payload.values() if isinstance(record, dict)]
    coverage = {
        field: sum(1 for record in records if record.get(field) not in (None, "", [], {}))
        for field in METADATA_FIELDS
    }
    return {
        "ok": True,
        "path": str(source),
        "record_count": len(payload),
        "object_records": len(records),
        "malformed_records": len(payload) - len(records),
        "field_coverage": coverage,
        "bytes": len(raw.encode("utf-8")),
    }
