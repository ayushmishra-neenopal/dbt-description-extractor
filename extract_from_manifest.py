"""
Bulk-extract model & column descriptions from dbt's manifest.json.
Run this AFTER `dbt docs generate` (or `dbt parse`) has produced target/manifest.json.

Usage:
    python extract_from_manifest.py
"""

import json
import csv
from pathlib import Path

MANIFEST_PATH = Path("target/manifest.json")
OUTPUT_CSV = Path("extract_descriptions_from_manifest.csv")


def main():
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(
            f"{MANIFEST_PATH} not found. Run `dbt docs generate` or `dbt parse` first."
        )

    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)

    rows = []
    for node in manifest["nodes"].values():
        if node.get("resource_type") != "model":
            continue

        model_name = node["name"]
        model_description = node.get("description", "")

        # model-level row (column_name left blank)
        if model_description:
            rows.append([model_name, "", model_description])

        # column-level rows
        for col_name, col in node.get("columns", {}).items():
            if col.get("description"):
                rows.append([model_name, col_name, col["description"]])

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["model_name", "column_name", "description"])
        writer.writerows(rows)

    print(f"Extracted {len(rows)} description rows -> {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
