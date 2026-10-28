"""Lightweight repository checks that use only Python's standard library.

This checks local documentation links, not scientific model validity.
Run from the repository root with: python scripts/check_repository.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTML_LINK = re.compile(r"\b(?:href|src)\s*=\s*(['\"])(.*?)\1", re.IGNORECASE)


def _is_external_or_fragment(target: str) -> bool:
    target = target.strip()
    if not target or target.startswith("#") or target.startswith("//"):
        return True
    parsed = urlparse(target)
    return bool(parsed.scheme or parsed.netloc)


def extract_local_links(markdown: str) -> list[str]:
    """Extract local Markdown and HTML href/src targets from a text file."""
    found: list[str] = []
    for match in MARKDOWN_LINK.finditer(markdown):
        target = match.group(1).strip()
        if target.startswith("<") and ">" in target:
            target = target[1 : target.index(">")]
        else:
            # Markdown permits an optional title after the destination.
            target = target.split(maxsplit=1)[0] if target else ""
        if not _is_external_or_fragment(target):
            found.append(target)

    for match in HTML_LINK.finditer(markdown):
        target = match.group(2).strip()
        if not _is_external_or_fragment(target):
            found.append(target)
    return found


def check_local_links(root: Path = ROOT) -> list[str]:
    """Return broken or unsafe local-link descriptions across Markdown files."""
    root = root.resolve()
    problems: list[str] = []

    for markdown_file in sorted(root.rglob("*.md")):
        try:
            text = markdown_file.read_text(encoding="utf-8")
            relative_name = markdown_file.relative_to(root)
        except (OSError, UnicodeError, ValueError) as exc:
            problems.append(f"{markdown_file}: cannot read file ({exc})")
            continue

        for target in extract_local_links(text):
            path_part = unquote(urlparse(target).path)
            if not path_part:
                continue

            candidate = (markdown_file.parent / path_part).resolve()
            try:
                candidate.relative_to(root)
            except ValueError:
                problems.append(
                    f"{relative_name}: link escapes repository root: {target}"
                )
                continue

            if not candidate.exists():
                problems.append(
                    f"{relative_name}: missing local target: {target}"
                )
    return problems


def main() -> int:
    problems = check_local_links()
    if problems:
        print("Repository integrity check failed:")
        for problem in problems:
            print(f" - {problem}")
        return 1

    count = len(list(ROOT.rglob("*.md")))
    print(f"Repository integrity check passed ({count} Markdown files checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
