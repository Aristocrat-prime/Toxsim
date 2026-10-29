"""Desktop data-quality console for the tracked Toxsim JSON cache.

This module audits file readability and metadata coverage only. It deliberately
does not execute simulation, mixture, dose, injury, or lethality calculations.
"""
from __future__ import annotations

import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA = ROOT / "pubchem_cache.json"
METADATA_FIELDS = ("formula", "mw", "type", "structure", "cid", "source")


def audit_data(path: str | Path = DEFAULT_DATA) -> dict[str, Any]:
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
    field_coverage = {
        field: sum(1 for record in records if record.get(field) not in (None, "", [], {}))
        for field in METADATA_FIELDS
    }
    return {
        "ok": True,
        "path": str(source),
        "record_count": len(payload),
        "object_records": len(records),
        "malformed_records": len(payload) - len(records),
        "field_coverage": field_coverage,
        "bytes": len(raw.encode("utf-8")),
    }


class DataReviewApp:
    """Small standard-library desktop interface for repository data checks."""

    def __init__(self, root: tk.Tk, data_path: str | Path = DEFAULT_DATA) -> None:
        self.root = root
        self.data_path = Path(data_path)
        self.root.title("Toxsim | Data Review Console")
        self.root.geometry("820x590")
        self.root.minsize(680, 480)
        self.root.configure(bg="#101820")

        style = ttk.Style(root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background="#101820")
        style.configure("TLabel", background="#101820", foreground="#e8eef2")
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), foreground="#f3f6f8")
        style.configure("Sub.TLabel", font=("Segoe UI", 10), foreground="#aab8c2")
        style.configure("Treeview", background="#17232d", fieldbackground="#17232d",
                        foreground="#e8eef2", rowheight=30, borderwidth=0)
        style.configure("Treeview.Heading", background="#263846", foreground="#ffffff",
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#235b68")])

        outer = ttk.Frame(root, padding=24)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="TOXSIM / DATA REVIEW", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            outer,
            text="Local repository check · read-only · no simulation execution",
            style="Sub.TLabel",
        ).pack(anchor="w", pady=(5, 20))

        self.status = ttk.Label(outer, text="Ready to inspect the tracked JSON file.")
        self.status.pack(anchor="w", pady=(0, 12))
        self.metrics = ttk.Treeview(outer, columns=("metric", "value"), show="headings", height=8)
        self.metrics.heading("metric", text="CHECK")
        self.metrics.heading("value", text="RESULT")
        self.metrics.column("metric", width=420, anchor="w")
        self.metrics.column("value", width=230, anchor="w")
        self.metrics.pack(fill="both", expand=True)

        bottom = ttk.Frame(outer)
        bottom.pack(fill="x", pady=(16, 0))
        ttk.Button(bottom, text="Refresh audit", command=self.refresh).pack(side="left")
        ttk.Button(bottom, text="Show data path", command=self.show_path).pack(side="left", padx=8)
        ttk.Label(
            outer,
            text=(
                "This console reports file integrity and metadata coverage only. "
                "It does not calculate doses, mixtures, toxicity, injury, or lethality."
            ),
            style="Sub.TLabel",
            wraplength=740,
        ).pack(anchor="w", pady=(16, 0))
        self.refresh()

    def refresh(self) -> None:
        result = audit_data(self.data_path)
        self.metrics.delete(*self.metrics.get_children())
        if not result["ok"]:
            self.status.configure(text="DATA CHECK FAILED")
            self.metrics.insert("", "end", values=("File check", "Failed"))
            self.metrics.insert("", "end", values=("Details", result["error"]))
            return

        self.status.configure(text="DATA FILE READABLE · aggregate checks complete")
        rows = [
            ("JSON file", "Valid"),
            ("File size", f'{result["bytes"]:,} bytes'),
            ("Records in file", str(result["record_count"])),
            ("Record objects", str(result["object_records"])),
            ("Non-object records", str(result["malformed_records"])),
        ]
        rows.extend(
            (f"Records with {field}", f'{count} / {result["object_records"]}')
            for field, count in result["field_coverage"].items()
        )
        for row in rows:
            self.metrics.insert("", "end", values=row)

    def show_path(self) -> None:
        messagebox.showinfo("Tracked data file", str(self.data_path), parent=self.root)


def main() -> int:
    root = tk.Tk()
    DataReviewApp(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
