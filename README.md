# dbt-description-extractor
Bulk-extract dbt model and column descriptions from manifest.json into a CSV.
 # dbt Description Extractor

Pull every model and column description out of your dbt project in one go. The script reads dbt's `manifest.json` and writes all descriptions to a single CSV.

Use it to seed a data dictionary, feed dashboard info-buttons, or audit what's documented, without copying descriptions out of YAML files by hand.

## Prerequisites

- A dbt project with descriptions already written in your `schema.yml` files
- dbt installed and able to run from your project folder
- Python 3.7 or later (no extra packages needed)

## Usage

**1. Generate the manifest.** From your dbt project folder, run:

```bash
dbt docs generate
```

This writes `manifest.json` to the `target/` folder. `dbt parse` also produces it and is faster if you only need the descriptions.

**2. Run the script.** Save `extract_from_manifest.py` in your dbt project folder, next to `dbt_project.yml`, and run:

```bash
python extract_from_manifest.py
```

The script prints a summary when it finishes:

```
Extracted 21 description rows -> descriptions_from_manifest.csv
```

## Output

`descriptions_from_manifest.csv` has one row per model and one per column:

| model_name | column_name | description |
|---|---|---|
| stg_customers | | One row per customer who has signed up for the gym membership system. |
| stg_customers | customer_id | Unique identifier for each customer. Primary key. |

A blank `column_name` means the row is the model's own description.

## Good to know

- Only models are included. Seeds, sources and tests are skipped.
- Models and columns without a description are skipped, so the CSV lists only what's documented.
- `manifest.json` is a snapshot from the last time dbt ran. Re-run both steps after you change any descriptions.
- To change the input or output location, edit `MANIFEST_PATH` and `OUTPUT_CSV` at the top of the script.

## Keeping it up to date

A one-off run works well for smaller projects. If the CSV feeds something people rely on, run both steps in CI on every merge so it never goes stale.

## About

Built by [NeenOpal](https://www.neenopal.com). Read the full walkthrough: [How To Bulk-Extract Descriptions From dbt](https://www.neenopal.com/blog/bulk-extract-dbt-descriptions).
