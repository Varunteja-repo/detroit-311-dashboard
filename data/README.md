# Data

The CSV isn't committed. It's built from public data and can be recreated with one command:

```bash
python3 scripts/prepare_data.py
```

## Source

- **Dataset:** [Improve Detroit Issues](https://data.detroitmi.gov/datasets/detroitmi::improve-detroit-issues/about), City of Detroit Open Data Portal. Improve Detroit is the City's 311 system (SeeClickFix), and DoIT administers it.
- **Pulled from:** the dataset's [ArcGIS feature service](https://services2.arcgis.com/qvkbeam7Wirps6zC/arcgis/rest/services/improve_detroit/FeatureServer/0), filtered to requests created in 2025. The full export covers every year and is too large to commit.
- **Downloaded:** October 1, 2026. The City updates records daily as requests close, so a later pull will drift slightly.
- **Output:** `improve_detroit_2025.csv`, 93,981 rows, 12 columns, 13.9 MB.

| Column | Notes |
|---|---|
| `issue_id` | Unique request ID |
| `request_type` | 57 categories in 2025, e.g. "Tall Grass and Weeds" |
| `status` | Closed, Archived, Acknowledged, Open |
| `report_method` | `direct` (Improve Detroit app or website), phone, walk-in, email, … |
| `created_at`, `acknowledged_at`, `closed_at` | UTC, as stored by the City's service |
| `num_days_to_close` | Blank while a request is open |
| `council_district` | 1–7, blank when unassigned |
| `neighborhood`, `latitude`, `longitude` | Location of the request |

## Cleaning rules

Both dashboards apply the same rules. The row filter happens in the script; the derived fields are calculated fields in the workbook, so the logic is visible where it's used.

| # | Rule | Where |
|---|---|---|
| 1 | Keep requests created in 2025 (Jan 1 to Dec 31, UTC) | `prepare_data.py` query |
| 2 | Blank council district becomes "Unassigned" | `District` calculated field |
| 3 | `Is Internal` is TRUE when the request type contains "ONLY" (staff-entered work orders); the dashboard filter defaults to FALSE | `Is Internal` calculated field |
| 4 | `num_days_to_close` stays blank for open requests. Filling it with 0 would make the City look faster than it is | `prepare_data.py` keeps nulls |
| 5 | Days to Acknowledge = hours between `created_at` and `acknowledged_at`, divided by 24 | `Days to Acknowledge` calculated field |
| 6 | Map only: drop points outside latitude 42.25 to 42.46, longitude -83.29 to -82.91 | Map sheet filter |

## Validation

After cleaning: 93,981 requests, 91,172 closed (97.0%), median 5 days to close. These match a direct count query against the City's feature service. The full set of numbers each dashboard has to reproduce is in [`docs/reference_numbers.md`](../docs/reference_numbers.md).

## Data quality findings

- **No council district:** 4,937 requests (5.3%). Grouped as "Unassigned" rather than dropped.
- **Staff-entered work orders:** 25,084 requests (26.7%) have "ONLY" in the request type, e.g. "DPW - Debris Removal - DPW USE ONLY". They behave differently from resident requests: 30% are closed the day they're entered (vs. 10% of resident requests), while debris-removal orders take a median of 21 days. Mixing them in distorts resident-facing metrics, so the dashboard shows resident requests by default, and the Is Internal filter adds them back.
- **Missing or bad coordinates:** 8,455 requests (9.0%) have no coordinates. Another 125 have latitude and longitude swapped (latitude around -83, longitude around 42). Both groups are left off the map but kept in every other chart.
- **Open requests:** 2,809 requests had no close date when the data was pulled. Every closed request has `num_days_to_close`, and no open request does.
- **Skewed close times:** 386 requests took 200+ days to close (the longest took 589), so the average is 12.3 days against a 5-day median. The dashboard leads with the median.
