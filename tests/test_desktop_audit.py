import json

from toxsim.data_audit import audit_data


def test_audit_reports_aggregate_field_coverage(tmp_path):
    source = tmp_path / "records.json"
    source.write_text(
        json.dumps({
            "record-a": {"formula": "X2", "mw": 12.0, "source": "example"},
            "record-b": {"formula": "Y", "structure": "example"},
            "invalid-record": None,
        }),
        encoding="utf-8",
    )
    result = audit_data(source)
    assert result["ok"] is True
    assert result["record_count"] == 3
    assert result["object_records"] == 2
    assert result["malformed_records"] == 1
    assert result["field_coverage"]["formula"] == 2
    assert result["field_coverage"]["mw"] == 1
    assert result["field_coverage"]["source"] == 1
    assert "record-a" not in str(result)


def test_audit_reports_invalid_json(tmp_path):
    source = tmp_path / "broken.json"
    source.write_text("{not json", encoding="utf-8")
    result = audit_data(source)
    assert result["ok"] is False
    assert "Invalid JSON" in result["error"]


def test_audit_reports_missing_file(tmp_path):
    result = audit_data(tmp_path / "missing.json")
    assert result["ok"] is False
    assert result["error"]
