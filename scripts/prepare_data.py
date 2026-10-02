"""Pull 2025 Improve Detroit issues from the City of Detroit's ArcGIS feature
service and write the CSV the dashboards are built on.

Row and column rules from the build guide are applied here: requests created in
2025, the 12 columns the dashboards use, and blank num_days_to_close left blank
for open requests. The derived fields (District, Is Internal, Is Closed, Days to
Acknowledge, Detroit map bounds) are built inside each BI tool, so the logic is
visible in the workbook. This script also writes docs/reference_numbers.md, the
totals each tool has to reproduce.

Usage: python3 scripts/prepare_data.py
"""

import json
import ssl
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

import pandas as pd

try:  # python.org builds on macOS ship without CA certificates
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

SERVICE = (
    "https://services2.arcgis.com/qvkbeam7Wirps6zC/arcgis/rest/services/"
    "improve_detroit/FeatureServer/0/query"
)
# The service stores dates in UTC, so the 2025 window is in UTC too.
WHERE = (
    "created_at >= TIMESTAMP '2025-01-01 00:00:00' "
    "AND created_at < TIMESTAMP '2026-01-01 00:00:00'"
)
FIELDS = [
    "issue_id", "request_type", "status", "report_method", "created_at",
    "acknowledged_at", "closed_at", "num_days_to_close", "council_district",
    "neighborhood", "latitude", "longitude",
]
DATE_FIELDS = ["created_at", "acknowledged_at", "closed_at"]
PAGE_SIZE = 1000  # the layer's maxRecordCount

# Detroit bounding box from the build guide, used to filter the map only.
LAT_RANGE = (42.25, 42.46)
LON_RANGE = (-83.29, -82.91)

ROOT = Path(__file__).resolve().parent.parent
OUT_CSV = ROOT / "data" / "improve_detroit_2025.csv"
OUT_REF = ROOT / "docs" / "reference_numbers.md"


def query(params):
    url = SERVICE + "?" + urllib.parse.urlencode({"where": WHERE, "f": "json", **params})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=120, context=SSL_CONTEXT) as resp:
                data = json.load(resp)
            if "error" in data:
                raise RuntimeError(data["error"])
            return data
        except Exception:
            if attempt == 4:
                raise
            time.sleep(2 ** attempt)


def fetch():
    total = query({"returnCountOnly": "true"})["count"]

    def page(offset):
        data = query({
            "outFields": ",".join(FIELDS + ["ObjectId"]),
            "orderByFields": "ObjectId",
            "resultOffset": offset,
            "resultRecordCount": PAGE_SIZE,
            "returnGeometry": "false",
        })
        return [f["attributes"] for f in data["features"]]

    with ThreadPoolExecutor(max_workers=6) as pool:
        rows = [row for rows in pool.map(page, range(0, total, PAGE_SIZE)) for row in rows]

    df = pd.DataFrame(rows).drop_duplicates("ObjectId")
    if len(df) != total:
        raise RuntimeError(f"expected {total} rows, got {len(df)}; rerun the script")
    return df[FIELDS]


def clean(df):
    df = df.copy()
    df["issue_id"] = df["issue_id"].astype("int64")
    for col in DATE_FIELDS:
        df[col] = pd.to_datetime(df[col], unit="ms", utc=True).dt.tz_localize(None)
    # Whole-day values are written without a trailing ".0". Open requests stay
    # blank: filling them with 0 would make the City look faster than it is.
    days = df["num_days_to_close"]
    if (days.dropna() % 1 == 0).all():
        df["num_days_to_close"] = days.astype("Int64")
    df["council_district"] = df["council_district"].replace("", None)
    return df.sort_values(["created_at", "issue_id"]).reset_index(drop=True)


def derive(df):
    """The guide's derived fields, mirrored here only to compute reference numbers."""
    out = df.copy()
    out["district"] = ("District " + out["council_district"]).fillna("Unassigned")
    out["is_internal"] = out["request_type"].str.upper().str.contains("ONLY", na=False)
    out["is_closed"] = out["closed_at"].notna()
    # DATEDIFF('hour', ...) counts hour boundaries crossed, so floor both ends.
    hours = (out["acknowledged_at"].dt.floor("h") - out["created_at"].dt.floor("h"))
    out["days_to_ack"] = hours.dt.total_seconds() / 3600 / 24
    out["month"] = out["created_at"].dt.month
    out["in_detroit"] = (
        out["latitude"].between(*LAT_RANGE) & out["longitude"].between(*LON_RANGE)
    )
    return out


def kpis(d):
    closed = int(d["is_closed"].sum())
    over_30 = int((d["is_closed"] & (d["num_days_to_close"] > 30)).sum())
    return {
        "Total Requests": f"{len(d):,}",
        "Closed Requests": f"{closed:,}",
        "Closure Rate": f"{closed / len(d):.1%}",
        "Median Days to Close": f"{d['num_days_to_close'].median():.1f}",
        "% Closed Over 30 Days": f"{over_30 / closed:.1%}",
        "Median Days to Ack": f"{d['days_to_ack'].median():.1f}",
    }


def md_table(frame):
    header = "| " + " | ".join(frame.columns) + " |"
    rule = "|" + "|".join("---" for _ in frame.columns) + "|"
    body = ["| " + " | ".join(str(v) for v in row) + " |" for row in frame.itertuples(index=False)]
    return "\n".join([header, rule, *body])


def by_group(d, key):
    g = d.groupby(key)
    return pd.DataFrame({
        key: list(g.groups),
        "Requests": g.size().values,
        "Closed": g["is_closed"].sum().values,
        "Median days to close": g["num_days_to_close"].median().round(1).values,
        "Avg days to close": g["num_days_to_close"].mean().round(1).values,
    })


def reference(df):
    d = derive(df)
    external = d[~d["is_internal"]]
    sections = [f"# Reference numbers\n\nComputed by `scripts/prepare_data.py` from the City's feature "
                f"service on {date.today():%B %-d, %Y} (requests created in 2025, UTC). "
                "Both dashboards should reproduce these; small drifts are normal because "
                "the City updates records as requests close."]

    kpi = pd.DataFrame({
        "Measure": list(kpis(d)),
        "All requests (Is Internal = All)": list(kpis(d).values()),
        "Resident requests (Is Internal = False)": list(kpis(external).values()),
    })
    sections.append("## KPI cards\n\n" + md_table(kpi))

    months = by_group(d, "month").rename(columns={"month": "Month"})
    months["Month"] = pd.to_datetime(months["Month"], format="%m").dt.strftime("%b")
    sections.append("## By month (all requests)\n\n" + md_table(months))

    for label, frame in [("all requests", d), ("Is Internal = False", external)]:
        top = by_group(frame, "request_type").nlargest(10, "Requests")
        top = top.rename(columns={"request_type": "Request type"})
        sections.append(f"## Top 10 request types ({label})\n\n" + md_table(top))

        districts = by_group(frame, "district").sort_values("Median days to close", ascending=False)
        districts = districts.rename(columns={"district": "District"})
        sections.append(f"## Council districts ({label})\n\n" + md_table(districts))

    methods = d["report_method"].value_counts(dropna=False)
    channel = pd.DataFrame({
        "Report method": methods.index.astype(str),
        "Requests": methods.values,
        "Share": (methods.values / len(d) * 100).round(1).astype(str) + "%",
    })
    sections.append("## Channel\n\n" + md_table(channel))

    unassigned = int(d["council_district"].isna().sum())
    no_close_days = int((d["is_closed"] & d["num_days_to_close"].isna()).sum())
    open_with_days = int((~d["is_closed"] & d["num_days_to_close"].notna()).sum())
    quality = pd.DataFrame({
        "Check": [
            "No council district",
            "Internal requests (request type contains ONLY)",
            "Outside the Detroit map bounds or missing coordinates",
            "Closed but no num_days_to_close",
            "Open but has num_days_to_close",
        ],
        "Requests": [
            f"{unassigned:,} ({unassigned / len(d):.1%})",
            f"{int(d['is_internal'].sum()):,}",
            f"{int((~d['in_detroit']).sum()):,}",
            f"{no_close_days:,}",
            f"{open_with_days:,}",
        ],
    })
    sections.append("## Data quality\n\n" + md_table(quality))
    return "\n\n".join(sections) + "\n"


def main():
    df = clean(fetch())
    OUT_CSV.parent.mkdir(exist_ok=True)
    df.to_csv(OUT_CSV, index=False, date_format="%Y-%m-%d %H:%M:%S")
    OUT_REF.parent.mkdir(exist_ok=True)
    OUT_REF.write_text(reference(df))
    print(f"Wrote {len(df):,} rows to {OUT_CSV.relative_to(ROOT)} "
          f"({OUT_CSV.stat().st_size / 1e6:.1f} MB) and {OUT_REF.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
