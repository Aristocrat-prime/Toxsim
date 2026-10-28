from pathlib import Path

import toxsim


ROOT = Path(__file__).resolve().parents[1]


def test_package_exposes_version():
    assert toxsim.__version__ == "0.1.0"


def test_core_project_documents_exist():
    assert (ROOT / "README.md").is_file()
    assert (ROOT / "docs" / "implementation-status.md").is_file()
    assert (ROOT / "docs" / "data-policy.md").is_file()


def test_data_files_are_not_misrepresented_as_present():
    # The README in data/ explains which data files still need to be supplied.
    assert (ROOT / "data" / "README.md").is_file()
