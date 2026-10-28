import json
from pathlib import Path

from scripts.check_data_files import check_json_file


def test_accepts_object_json(tmp_path: Path) -> None:
    path = tmp_path / "pubchem_cache.json"
    path.write_text(json.dumps({"Example": {"formula": "H2O"}}), encoding="utf-8")
    assert check_json_file(path) == []


def test_rejects_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "smiles_repairs.json"
    path.write_text("{not json", encoding="utf-8")
    assert "cannot parse JSON" in check_json_file(path)[0]


def test_rejects_non_object_top_level(tmp_path: Path) -> None:
    path = tmp_path / "pubchem_cache.json"
    path.write_text("[]", encoding="utf-8")
    assert "top-level JSON value must be an object" in check_json_file(path)[0]


def test_rejects_empty_repair_values(tmp_path: Path) -> None:
    path = tmp_path / "smiles_repairs.json"
    path.write_text(json.dumps({"Example": ""}), encoding="utf-8")
    assert "non-empty string" in check_json_file(path)[0]
