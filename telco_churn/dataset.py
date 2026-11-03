"""Inspection helpers for the Telco churn dataset.

This module only *reads* the source CSV and reports facts about it.
It does not clean, impute, split, or train anything (TP01 scope).
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import sys
from pathlib import Path

import pandas as pd

TARGET_COLUMN = "Churn"
ID_COLUMN = "customerID"


def sha256_of(path: Path) -> str:
    """Return the hex SHA-256 digest of a file's bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def empty_or_whitespace_counts(df: pd.DataFrame) -> dict[str, int]:
    """Count cells that are empty or whitespace-only *strings*.

    Distinct from ``isna()``: a cell containing " " is not NaN.
    """
    result: dict[str, int] = {}
    for col in df.columns:
        s = df[col].astype("string")
        stripped = s.str.strip()
        count = int((stripped.eq("") & s.notna()).sum())
        result[col] = count
    return result


def inspect(source: Path) -> dict:
    """Build a machine-readable inspection report for ``source``."""
    df = pd.read_csv(source)

    target_counts = df[TARGET_COLUMN].value_counts(dropna=False)
    target_proportions = df[TARGET_COLUMN].value_counts(
        dropna=False, normalize=True
    ).round(4)

    report = {
        "source": {
            "path": str(source),
            "size_bytes": source.stat().st_size,
            "sha256": sha256_of(source),
        },
        "environment": {
            "python_version": sys.version,
            "python_implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "pandas_version": importlib.metadata.version("pandas"),
        },
        "dataset": {
            "shape": {"rows": int(df.shape[0]), "columns": int(df.shape[1])},
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        },
        "target": {
            "column": TARGET_COLUMN,
            "counts": {str(k): int(v) for k, v in target_counts.items()},
            "proportions": {str(k): float(v) for k, v in target_proportions.items()},
        },
        "identifier": {
            "column": ID_COLUMN,
            "duplicate_count": int(df[ID_COLUMN].duplicated().sum()),
            "unique_count": int(df[ID_COLUMN].nunique(dropna=False)),
        },
        "missing_values": {
            "isna_counts": {col: int(v) for col, v in df.isna().sum().items()},
            "empty_or_whitespace_counts": empty_or_whitespace_counts(df),
        },
    }
    return report


def write_report(report: dict, destination: Path) -> None:
    """Write the report to ``destination`` as pretty-printed JSON."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
