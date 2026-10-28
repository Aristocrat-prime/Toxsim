"""Check the syntax and basic shape of tracked project JSON data.

This deliberately does not infer chemical identity, toxicity, or pharmacokinetic
validity from a record. Run from the repository root:
    python scripts/check_data_files.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILES = ("pubchem_cache.json", "smiles_repairs.json")


def check_json_file(path: Path) -> list[str]:
    problems: list[str] = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        return [f"{path.name}: file is missing"]
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"{path.name}: cannot parse JSON ({exc})"]

    if not isinstance(data, dict):
        return [f"{path.name}: top-level JSON value must be an object"]

    for key, value in data.items():
        if not isinstance(key, str) or not key.strip():
            problems.append(f"{path.name}: keys must be non-empty strings")
            continue
        if path.name == "smiles_repairs.json":
            if not isinstance(value, str) or not value.strip():
                problems.append(
                    f"{path.name}: repair for {key!r} must be a non-empty string"
                )
        elif not isinstance(value, dict):
            problems.append(
                f"{path.name}: record for {key!r} must be a JSON object"
            )

    return problems


def main() -> int:
    problems: list[str] = []
    for filename in DATA_FILES:
        problems.extend(check_json_file(ROOT / filename))

    if problems:
        print("Data-file integrity check failed:")
        for problem in problems:
            print(f" - {problem}")
        return 1

    print(f"Data-file integrity check passed ({len(DATA_FILES)} JSON files).")
    print("Note: JSON integrity does not validate scientific accuracy or identity.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
