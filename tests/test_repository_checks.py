from pathlib import Path

from scripts.check_repository import check_local_links, extract_local_links


def test_extracts_markdown_and_html_local_links() -> None:
    text = """
    [Guide](docs/guide.md)
    ![Banner](<assets/banner.svg> "Project banner")
    <img src="assets/icon.svg" alt="icon">
    [External](https://example.com/docs)
    [Section](#section)
    """
    assert extract_local_links(text) == [
        "docs/guide.md",
        "assets/banner.svg",
        "assets/icon.svg",
    ]


def test_validates_local_links_and_ignores_external_links(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "README.md").write_text(
        "[Guide](docs/guide.md) and [External](https://example.com)",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "guide.md").write_text("# Guide", encoding="utf-8")
    assert check_local_links(tmp_path) == []


def test_reports_missing_local_targets(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text(
        "[Missing](docs/not-there.md)", encoding="utf-8"
    )
    problems = check_local_links(tmp_path)
    assert len(problems) == 1
    assert "missing local target" in problems[0]


def test_rejects_links_that_escape_repository_root(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text(
        "[Outside](../../outside.md)", encoding="utf-8"
    )
    problems = check_local_links(tmp_path)
    assert len(problems) == 1
    assert "escapes repository root" in problems[0]
