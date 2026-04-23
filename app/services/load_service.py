from __future__ import annotations

import csv
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"


def _write_csv(rows: list[dict], file_path: Path) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        file_path.write_text("", encoding="utf-8")
        return

    fieldnames = list(rows[0].keys())
    with file_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class LoadService:
    def export_raw(self, object_name: str, rows: list[dict]) -> str:
        file_path = RAW_DIR / f"{object_name}.csv"
        _write_csv(rows, file_path)
        return str(file_path)

    def export_processed(self, object_name: str, rows: list[dict]) -> str:
        file_path = PROCESSED_DIR / f"{object_name}.csv"
        _write_csv(rows, file_path)
        return str(file_path)

