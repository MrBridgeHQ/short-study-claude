#!/usr/bin/env python3
"""
analyze.py - deterministic numbers engine for the short-study skill.

Subcommands: compare | correlate | distribute
Reads CSV or JSON (file or stdin). Writes JSON to stdout.
All floats rounded to 3 decimal places.
Standard library only.

Standard-deviation note: this script uses statistics.pstdev (population σ)
throughout. The study treats the dataset it was given as the complete
population of interest; std is reported as a context/spread figure, not as
an inferential statistic, so dividing by N (not N-1) is appropriate.
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from collections import defaultdict
from typing import Any


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _round(value: float) -> float:
    return round(value, 3)


def _die(msg: str) -> None:
    """Print error to stderr and exit non-zero."""
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


def _load(path: str) -> list[dict]:
    """Load rows from a CSV or JSON file (or stdin when path=='-')."""
    if path == "-":
        # Read JSON from stdin
        try:
            raw = sys.stdin.read()
            rows = json.loads(raw)
        except json.JSONDecodeError as exc:
            _die(f"stdin is not valid JSON: {exc}")
        if not isinstance(rows, list):
            _die("stdin JSON must be a list of objects")
        return rows

    try:
        with open(path, newline="", encoding="utf-8") as fh:
            if path.endswith(".json"):
                rows = json.load(fh)
                if not isinstance(rows, list):
                    _die(f"{path}: JSON must be a list of objects")
                return rows
            else:
                # Treat as CSV
                reader = csv.DictReader(fh)
                return [dict(row) for row in reader]
    except FileNotFoundError:
        _die(f"File not found: {path}")
    except json.JSONDecodeError as exc:
        _die(f"{path} is not valid JSON: {exc}")


def _require_col(rows: list[dict], col: str) -> None:
    """Exit with error if col is missing from any row."""
    for i, row in enumerate(rows):
        if col not in row:
            _die(f"Column '{col}' not found in row {i}: {list(row.keys())}")


def _to_float(value: Any, col: str, row_idx: int) -> float:
    """Convert value to float or die with a clear message."""
    try:
        return float(value)
    except (TypeError, ValueError):
        _die(
            f"Non-numeric value '{value}' in column '{col}' at row {row_idx}"
        )


def _rank_avg(data: list[float]) -> list[float]:
    """Return average ranks for data (handles ties)."""
    n = len(data)
    sorted_indexed = sorted(range(n), key=lambda i: data[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j < n - 1 and data[sorted_indexed[j + 1]] == data[sorted_indexed[i]]:
            j += 1
        avg_rank = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[sorted_indexed[k]] = avg_rank
        i = j + 1
    return ranks


# ---------------------------------------------------------------------------
# Operations
# ---------------------------------------------------------------------------

def op_compare(rows: list[dict], group_col: str, value_col: str) -> dict:
    if not rows:
        _die("Input dataset is empty")
    _require_col(rows, group_col)
    _require_col(rows, value_col)

    # Group values
    groups: dict[str, list[float]] = defaultdict(list)
    for idx, row in enumerate(rows):
        val = _to_float(row[value_col], value_col, idx)
        groups[str(row[group_col])].append(val)

    group_stats = []
    for label in sorted(groups.keys()):
        vals = groups[label]
        group_stats.append({
            "label": label,
            "n": len(vals),
            "mean": _round(statistics.mean(vals)),
            "median": _round(statistics.median(vals)),
            "std": _round(statistics.pstdev(vals)),  # population σ - see module docstring
            "min": _round(min(vals)),
            "max": _round(max(vals)),
        })

    chart_series = [
        {"label": g["label"], "value": g["mean"]} for g in group_stats
    ]

    return {
        "operation": "compare",
        "n": len(rows),
        "value_col": value_col,
        "group_col": group_col,
        "groups": group_stats,
        "chart": {
            "type": "bar",
            "x": group_col,
            "y": f"mean {value_col}",
            "series": chart_series,
        },
    }


def op_correlate(rows: list[dict], x_col: str, y_col: str) -> dict:
    if not rows:
        _die("Input dataset is empty")
    _require_col(rows, x_col)
    _require_col(rows, y_col)

    x_vals: list[float] = []
    y_vals: list[float] = []
    for idx, row in enumerate(rows):
        x_vals.append(_to_float(row[x_col], x_col, idx))
        y_vals.append(_to_float(row[y_col], y_col, idx))

    if len(x_vals) < 2:
        _die("Need at least 2 data points for correlation")

    try:
        pearson = _round(statistics.correlation(x_vals, y_vals))

        rx = _rank_avg(x_vals)
        ry = _rank_avg(y_vals)
        spearman = _round(statistics.correlation(rx, ry))
    except statistics.StatisticsError as exc:
        _die(f"Correlation requires non-constant columns: {exc}")

    points = [[x, y] for x, y in zip(x_vals, y_vals)]

    return {
        "operation": "correlate",
        "n": len(rows),
        "x_col": x_col,
        "y_col": y_col,
        "pearson": pearson,
        "spearman": spearman,
        "chart": {
            "type": "scatter",
            "x": x_col,
            "y": y_col,
            "points": points,
        },
    }


def op_distribute(
    rows: list[dict], by_col: str, value_col: str | None
) -> dict:
    if not rows:
        _die("Input dataset is empty")
    _require_col(rows, by_col)
    if value_col is not None:
        _require_col(rows, value_col)

    n = len(rows)
    groups: dict[str, list] = defaultdict(list)
    for idx, row in enumerate(rows):
        label = str(row[by_col])
        if value_col is not None:
            groups[label].append(_to_float(row[value_col], value_col, idx))
        else:
            groups[label].append(None)

    categories = []
    for label in sorted(groups.keys()):
        items = groups[label]
        count = len(items)
        proportion = _round(count / n)
        cat: dict = {"label": label, "count": count, "proportion": proportion}
        if value_col is not None:
            float_vals = [v for v in items if v is not None]
            cat["mean_value"] = _round(statistics.mean(float_vals))
        categories.append(cat)

    if value_col is not None:
        chart_y = f"mean {value_col}"
        chart_series = [
            {"label": c["label"], "value": c["mean_value"]} for c in categories
        ]
    else:
        chart_y = "count"
        chart_series = [
            {"label": c["label"], "value": c["count"]} for c in categories
        ]

    result: dict = {
        "operation": "distribute",
        "n": n,
        "by_col": by_col,
    }
    if value_col is not None:
        result["value_col"] = value_col
    result["categories"] = categories
    result["chart"] = {
        "type": "bar",
        "x": by_col,
        "y": chart_y,
        "series": chart_series,
    }
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Deterministic numbers engine for short-study skill."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # compare
    p_compare = sub.add_parser("compare", help="Compare groups on a numeric value")
    p_compare.add_argument("--input", required=True, metavar="PATH|'-'")
    p_compare.add_argument("--group-col", required=True)
    p_compare.add_argument("--value-col", required=True)

    # correlate
    p_correlate = sub.add_parser("correlate", help="Pearson + Spearman correlation")
    p_correlate.add_argument("--input", required=True, metavar="PATH|'-'")
    p_correlate.add_argument("--x-col", required=True)
    p_correlate.add_argument("--y-col", required=True)

    # distribute
    p_distribute = sub.add_parser("distribute", help="Distribution by category")
    p_distribute.add_argument("--input", required=True, metavar="PATH|'-'")
    p_distribute.add_argument("--by-col", required=True)
    p_distribute.add_argument("--value-col", default=None)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    rows = _load(args.input)

    if args.command == "compare":
        result = op_compare(rows, args.group_col, args.value_col)
    elif args.command == "correlate":
        result = op_correlate(rows, args.x_col, args.y_col)
    elif args.command == "distribute":
        result = op_distribute(rows, args.by_col, args.value_col)
    else:
        _die(f"Unknown command: {args.command}")

    print(json.dumps(result))


if __name__ == "__main__":
    main()
