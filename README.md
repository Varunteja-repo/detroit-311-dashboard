# Detroit 311 Service Request Dashboard

**Where and when does Detroit's 311 system fall behind?**

Detroiters filed 93,981 service requests through Improve Detroit, the City's 311 system, in 2025. 97% were closed, with a median of 5 days to close. This dashboard shows where and when that slows down, built in Tableau Public from the City of Detroit's open data. A Power BI version is in progress.

> **In progress:** the Tableau Public dashboard is being built. Its link and a screenshot will be added here once it's published.

## Findings

These are for resident requests, the dashboard's default view. 25,084 staff-entered "USE ONLY" work orders are excluded, and the Is Internal filter adds them back.

1. **Summer surge.** Resident requests peak in July at 9,054, 2.7× December (3,415).
2. **Close times lag the surge.** Median days to close more than doubles, from 4 days in March–May to 9 in August, a month after volume peaks, then falls to 2 in December.
3. **The slowest high-volume work has long tails.** Among request types with 2,000+ requests, Investigate Blocked Basin Street (2,545) has the longest average close time: 46 days, against a 15-day median. Next are DPW DR Coordinator (2,604; average 32, median 10) and Request Recycling Cart (7,180; average 19, median 10).

## What's in the dashboard

- **KPI row:** total requests, closure rate, median days to close, % of closed requests that took over 30 days
- **Monthly trend:** request volume as bars and median days to close as a line, on a dual axis
- **Top 10 request types** by volume, colored by median days to close
- **Council districts** ranked by median days to close. Click a district to filter every other chart.
- **Density map** of request locations
- **Filters:** request type, council district, and Is Internal (default: residents only)

The dashboard leads with the median, not the average. Close times are skewed: 386 requests took 200+ days, which pulls the average (12.3 days) to more than twice the median (5).

## Data and cleaning

Source: [Improve Detroit Issues](https://data.detroitmi.gov/datasets/detroitmi::improve-detroit-issues/about), City of Detroit Open Data Portal. Data was pulled October 1, 2026 from the City's ArcGIS feature service.

[`scripts/prepare_data.py`](scripts/prepare_data.py) pulls the 2025 requests and writes the CSV the dashboard uses. The cleaning rules, the data-quality issues found, and how each was handled are in [`data/README.md`](data/README.md). The CSV itself isn't committed; run the script to rebuild it.

## Validation

The cleaned data matches a direct count from the City's feature service: 93,981 requests, 91,172 closed, median 5 days to close with every request included. [`docs/reference_numbers.md`](docs/reference_numbers.md) lists every number the dashboard has to reproduce, for both the resident-only and the all-requests views.

## Repository layout

```
detroit-311-dashboard/
├── README.md
├── scripts/prepare_data.py         pulls and cleans the 2025 data
├── data/README.md                  source, download date, cleaning rules, data quality
└── docs/reference_numbers.md       numbers the dashboards must reproduce
```
