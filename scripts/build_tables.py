"""Builds thanksgiving_week_by_day.csv, thanksgiving_week_by_airport.csv, winter_cancellations_by_month.csv,
winter_cancellations_by_airport.csv from BTS parquet 2023-01..2025-12. Airports = the 39 in the site airport CSV (Origin)."""
import duckdb,csv,datetime,os
HERE=os.path.dirname(os.path.abspath(__file__))
BTS=os.environ.get("BTS_PARQUET","bts/bts_202[345]_*.parquet")  # BTS On-Time monthly files as parquet
OUT=os.path.join(HERE,"..","tables")+"/"
g=f"read_parquet('{BTS}')"
ap="("+",".join("'%s'"%r['airport_code'] for r in csv.DictReader(open(os.path.join(HERE,'..','data-site','delayguard-airport-delay-rates.csv'))))+")"
def thx(y):
    d=datetime.date(y,11,1); d+=datetime.timedelta((3-d.weekday())%7+21); return d
T={y:thx(y) for y in (2023,2024,2025)}; print(T)
vals=",".join(f"({y},DATE '{d}')" for y,d in T.items())
duckdb.sql(f"create view t as select * from (values {vals}) v(yr,thx)")
duckdb.sql(f"""create view f as select cast(FlightDate as date) fd,Origin,Cancelled,Diverted,ArrDel15,CancellationCode,Year,Month from {g} where Origin in {ap}""")
R="count(*) scheduled_flights, cast(sum(Cancelled) as bigint) cancelled, round(100*sum(Cancelled)/count(*),2) cancel_rate_pct, count(ArrDel15) flights_with_arrival_status, round(100*sum(ArrDel15)/count(ArrDel15),2) delay_rate_pct"
def w(name,sql):
    duckdb.sql(f"copy ({sql}) to '{OUT}{name}' (header,delimiter ',')")
import os;os.makedirs(OUT,exist_ok=True)
# window: Saturday before Thanksgiving week start (thx-5 = Saturday)? use Mon before (thx-3) .. Mon after (thx+4)
J="from f join t on f.fd between t.thx-3 and t.thx+4"
w("thanksgiving_week_by_day.csv",f"""select yr as year, strftime(fd,'%Y-%m-%d') flight_date, strftime(fd,'%A') weekday, cast(fd-thx as int) days_from_thanksgiving, {R} {J} group by yr,fd,thx order by yr,fd""")
w("thanksgiving_week_by_airport.csv",f"""select Origin airport_code, {R} {J} group by 1 order by scheduled_flights desc""")
w("thanksgiving_week_by_year.csv",f"""select yr as year, strftime(thx,'%Y-%m-%d') thanksgiving_date, {R} {J} group by yr,thx order by 1""")
w("winter_cancellations_by_month.csv",f"""select Year as year, Month as month, {R},
 cast(sum(case when CancellationCode='A' then 1 else 0 end) as bigint) cancelled_carrier_A,
 cast(sum(case when CancellationCode='B' then 1 else 0 end) as bigint) cancelled_weather_B,
 cast(sum(case when CancellationCode='C' then 1 else 0 end) as bigint) cancelled_nas_C,
 cast(sum(case when CancellationCode='D' then 1 else 0 end) as bigint) cancelled_security_D
 from f where Month in (12,1,2) group by 1,2 order by 1,2""")
w("winter_cancellations_by_airport.csv",f"""select Origin airport_code, count(*) scheduled_flights, cast(sum(Cancelled) as bigint) cancelled, round(100*sum(Cancelled)/count(*),2) cancel_rate_pct,
 cast(sum(case when CancellationCode='B' then 1 else 0 end) as bigint) cancelled_weather_B
 from f where Month in (12,1,2) and Year in (2024,2025) group by 1 order by cancel_rate_pct desc""")
