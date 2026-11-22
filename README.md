# US flight delay and cancellation statistics, 2023-2025 (DelayGuard open data)

Aggregated US domestic flight statistics from the U.S. Bureau of Transportation Statistics (BTS) On-Time Reporting Carrier On-Time Performance data. These are the same files DelayGuard publishes at https://www.delayguard.ai/data, plus a Thanksgiving-week table and a winter cancellation table. Background and write-ups: https://www.delayguard.ai/research

DOI: [10.5281/zenodo.24445333](https://doi.org/10.5281/zenodo.24445333) (all versions). Also on [Kaggle](https://www.kaggle.com/datasets/delayguard/us-flight-delay-and-cancellation-stats-2023-2025) and [GitHub](https://github.com/DelayGuard/us-flight-delay-statistics).

## Files
| path | what |
|---|---|
| data-site/delayguard-airline-delay-cancellation-rates.csv | 10 airlines: flights, delay rate, cancellation rate |
| data-site/delayguard-airport-delay-rates.csv | 39 airports (by origin): flights, delay rate, cancellation rate (cancellation blank for 17 airports, as on the site) |
| data-site/delayguard-time-patterns.csv | delay rate by scheduled departure hour, weekday and month across the 39 airports |
| tables/thanksgiving_week_by_day.csv | per day, Monday before to Monday after Thanksgiving, 2023-2025 |
| tables/thanksgiving_week_by_year.csv | the same window summed per year |
| tables/thanksgiving_week_by_airport.csv | the same window per airport, 3 years pooled |
| tables/winter_cancellations_by_month.csv | Dec, Jan, Feb by year, with BTS cancellation-cause counts |
| tables/winter_cancellations_by_airport.csv | Dec-Feb 2024-2025 pooled, per airport |
| scripts/ | Python that rebuilds and checks the tables from the BTS files |
| MANIFEST.md | row counts and sha256 for every file |

## Source and method
- Source: BTS On-Time Reporting Carrier On-Time Performance, https://www.transportation.gov/data (monthly files from https://transtats.bts.gov). US domestic flights by reporting carriers, Jan 2023 to Dec 2025 (20,928,579 scheduled flights).
- A flight is **delayed** if it arrived 15 or more minutes after schedule (BTS ArrDel15 = 1). Delay rate = delayed / flights with an arrival status (cancelled flights and diverted flights without an arrival time are excluded from the denominator).
- **Cancellation rate** = cancelled / scheduled flights. On data-site files the cancellation window is 2024-2025 only; delay windows are Jan 2023 to Dec 2025. Each file's window columns say so.
- Airports are counted by origin. The airport and time-pattern files cover the 39 airports listed in the airport file.
- Tables in tables/ use the same 39 origin airports and 2023-2025. Thanksgiving = 4th Thursday of November (23 Nov 2023, 28 Nov 2024, 27 Nov 2025). Cancellation causes are BTS codes: A carrier, B weather, C national air system, D security.
- Everything is observed history. There are no model outputs, forecasts or accuracy figures.

## Notes
- Thanksgiving 2025 cancellations (2.06% for the window) were far above 2023 (0.09%) and 2024 (0.14%); the spike is on Sat 29 Nov 2025 (8.23%). The data does not explain why; do not read it as a trend.
- BTS figures can be revised. Rates are descriptive, not a guide to any single flight.

## Rebuild
Download the BTS On-Time Performance monthly files for 2023-2025, save them as parquet, and point `BTS_PARQUET` at them:

```
pip install duckdb
BTS_PARQUET='bts/bts_202[345]_*.parquet' python3 scripts/verify_site_csv.py
BTS_PARQUET='bts/bts_202[345]_*.parquet' python3 scripts/build_tables.py
```

## License and citation
CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), full text in LICENSE. Underlying data is from BTS (U.S. government work). Cite as:

> DelayGuard. US flight delay and cancellation statistics, 2023-2025 (from BTS On-Time Performance data). https://www.delayguard.ai/data. DOI: https://doi.org/10.5281/zenodo.24445333

Data page: https://www.delayguard.ai/data | Research: https://www.delayguard.ai/research
