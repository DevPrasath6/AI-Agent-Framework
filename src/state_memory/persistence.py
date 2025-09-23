"""
Persistence shim used for local testing.

This writes simple JSON-lines files under a `.data` directory. In a
real deployment you would replace this with Postgres/MinIO clients.
"""

import json
from pathlib import Path
from typing import Any, Dict

_DATA_DIR = Path(".data")
_DATA_DIR.mkdir(exist_ok=True)


def save_record(table: str, obj: Dict[str, Any]) -> Dict[str, Any]:
    """Save a record to a JSON-lines file and return the saved object.

    Args:
            table: Logical table/collection name
            obj: Dictionary representing the record

    Returns:
            The saved object (with generated id if not present)
    """
    file_path = _DATA_DIR / f"{table}.jsonl"

    # Ensure record has an id
    if "id" not in obj:
        # Simple incremental id based on file length
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                obj_id = len(lines) + 1
        except FileNotFoundError:
            obj_id = 1
        obj["id"] = obj_id

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, default=str) + "\n")

    return obj


def read_records(table: str) -> list:
    """Read all records from a logical table."""
    file_path = _DATA_DIR / f"{table}.jsonl"
    records = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    records.append(json.loads(line))
                except Exception:
                    continue
    except FileNotFoundError:
        return []

    return records
