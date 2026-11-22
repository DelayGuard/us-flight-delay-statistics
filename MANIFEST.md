# MANIFEST

Built 2026-11-13 from BTS On-Time Performance monthly files (2023-01..2025-12). rows = data rows excluding header.

| file | rows | sha256 |
|---|---:|---|
| data-site/delayguard-airline-delay-cancellation-rates.csv | 10 | f62e25343ae6eeeea851822d8ac4672795eb512f4f0db45f49b2440302a98f09 |
| data-site/delayguard-airport-delay-rates.csv | 39 | fdef73fb0ecc4a7d29438d85e95f6621e8ce94049bd21efdc6ded9c01d0ff46e |
| data-site/delayguard-time-patterns.csv | 40 | 48f355e6406b231c534104f77dae0b304280d71831397f6f77272ef79d918c2e |
| tables/thanksgiving_week_by_airport.csv | 39 | 4e6fbd5d3ddc7a630bee63e7eac42bd52c12252ca2c34164821cf5f94139b9f7 |
| tables/thanksgiving_week_by_day.csv | 24 | b60218d66416ce0d8f70a63144432f7b949d1959113f6662e63b0d31fe994262 |
| tables/thanksgiving_week_by_year.csv | 3 | 483e035cd3aaa84fc367acce78a20d167dc77522bc22ba87432d81f96ced692b |
| tables/winter_cancellations_by_airport.csv | 39 | aa3cf24f0d293f1487bf6c8e3f807ed754c9b055310d2e3838309353947e3e13 |
| tables/winter_cancellations_by_month.csv | 9 | 3d110de6b9a489c768965ddc31c80af8a87991eaa9a6c4aee6a69526ef143d34 |
| scripts/build_tables.py | - | acb40c9bd5f80b72b64809907f566bfc722a4ce99e8a4a9ae0e01e724e61ed29 |
| scripts/verify_site_csv.py | - | 892beb0ecef7368a915af1d3638aeb5a3854db38d3d0ea0045954a8dc6f12e86 |

## Recomputation checks (2026-11-13)
- Parquet 2023-2025: 20,928,579 rows; 14,080,680 in 2024-25 with 199,191 cancelled (1.41%); delay 21.23% (4,371,303/20,588,134).
- airline CSV: 10/10 rows match recompute (flights, delay, cancel).
- airport CSV: 39/39 flights and delay rates match; cancel rate matches the 22 filled rows, blank on 17 (BWI MDW DAL SAN DCA AUS STL HOU CVG IAD SNA OAK BUR SAT SMF ONT SJC) by site choice.
- time-patterns CSV: 36/40 rows match; 4 rows differ slightly from recompute (12 AM 26,906 vs 27,088; 1 AM 3,493 vs 3,544; 10 PM 451,165 vs 451,174; 11 PM 153,485 vs 153,890; delay rates within 0.06 pt). Site file shipped as-is; cause not found.
- tables/: thanksgiving 2025 window and Jan 2024 winter row re-derived independently with pandas; both equal.
