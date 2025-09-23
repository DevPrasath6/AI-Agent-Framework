"""Aggregate OpenVINO bench JSON into a CSV file for historical tracking.

This script reads a JSON file produced by `openvino_bench.py` (with keys
`stats` and `times`) and appends a row to `benchmarks/results.csv` with
selected metrics.

Example:
    python bench\aggregate_results.py --json bench_output\result.json --openvino false --model-path ""
"""
from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def row_from_json(data: dict[str, Any], matrix_openvino: str, model_path: str) -> dict:
    stats = data.get("stats", {})
    return {
        "ts": datetime.utcnow().isoformat() + "Z",
        "matrix_openvino": matrix_openvino,
        "model_path": model_path or "",
        "count": stats.get("count", ""),
        "mean_s": stats.get("mean_s", ""),
        "median_s": stats.get("median_s", ""),
        "p90_s": stats.get("p90_s", ""),
        "min_s": stats.get("min_s", ""),
        "max_s": stats.get("max_s", ""),
    }


def append_csv(path: Path, row: dict[str, Any]):
    header = ["ts", "matrix_openvino", "model_path", "count", "mean_s", "median_s", "p90_s", "min_s", "max_s"]
    exists = path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=header)
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", required=True, help="Path to bench JSON produced by openvino_bench.py")
    parser.add_argument("--openvino", required=True, help="Matrix value for openvino (true/false)")
    parser.add_argument("--model-path", default="", help="Model path used for the run (if any)")
    parser.add_argument("--out", default="benchmarks/results.csv", help="CSV file to append results to")
    args = parser.parse_args()

    p = Path(args.json)
    if not p.exists():
        raise SystemExit(f"Input JSON not found: {p}")

    with p.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    row = row_from_json(data, args.openvino, args.model_path)
    out_path = Path(args.out)
    append_csv(out_path, row)
    print(f"Appended results to {out_path}")


if __name__ == "__main__":
    main()
