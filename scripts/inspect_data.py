"""CLI entry point: inspect the raw Telco CSV and save a JSON report.

Usage (from the project root):

    uv run python scripts/inspect_data.py
"""
from __future__ import annotations

from pathlib import Path

from telco_churn.dataset import inspect, write_report

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT_ROOT / "data" / "raw" / "telco.csv"
DESTINATION = PROJECT_ROOT / "reports" / "data_overview.json"


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Source CSV not found: {SOURCE}")
    report = inspect(SOURCE)
    write_report(report, DESTINATION)
    print(f"Wrote {DESTINATION}")
    print(f"  rows    : {report['dataset']['shape']['rows']}")
    print(f"  columns : {report['dataset']['shape']['columns']}")
    print(f"  target  : {report['target']['counts']}")
    print(f"  sha256  : {report['source']['sha256']}")


if __name__ == "__main__":
    main()
