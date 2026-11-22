"""Recompute the three site CSVs from BTS parquet and compare. Run: python3 verify_site_csv.py"""
import duckdb,csv,os
HERE=os.path.dirname(os.path.abspath(__file__))
B=os.environ.get("BTS_PARQUET","bts/bts_202[345]_*.parquet")  # BTS On-Time monthly files as parquet
S=os.path.join(HERE,"..","data-site")+"/"
g=f"read_parquet('{B}')"
def num(s): return None if s=='' else float(s)
CANC="round(100*sum(case when Year>=2024 then Cancelled end)/sum(case when Year>=2024 then 1 end),2)"
tot=0
# airports (Origin)
m={x[0]:x for x in duckdb.sql(f"select Origin,count(ArrDel15),round(100*sum(ArrDel15)/count(ArrDel15),2),{CANC} from {g} group by 1").fetchall()}
rows=list(csv.DictReader(open(S+'delayguard-airport-delay-rates.csv'))); ap=[r['airport_code'] for r in rows]
bad=[r['airport_code'] for r in rows if (int(r['flights_delay_window']),float(r['delay_rate_pct']),num(r['cancel_rate_pct']))!=(m[r['airport_code']][1],m[r['airport_code']][2],m[r['airport_code']][3])]
print('airport rows',len(rows),'mismatch',bad)
# airlines
names={'Delta Air Lines':'DL','United Airlines':'UA','Southwest Airlines':'WN','Alaska Airlines':'AS','Allegiant Air':'G4','American Airlines':'AA','JetBlue Airways':'B6','Frontier Airlines':'F9','Spirit Airlines':'NK','Hawaiian Airlines':'HA'}
m={x[0]:x for x in duckdb.sql(f"select Reporting_Airline,count(ArrDel15),round(100*sum(ArrDel15)/count(ArrDel15),2),{CANC} from {g} group by 1").fetchall()}
rows=list(csv.DictReader(open(S+'delayguard-airline-delay-cancellation-rates.csv')))
bad=[r['airline'] for r in rows if (int(r['flights_delay_window']),float(r['delay_rate_pct']),num(r['cancel_rate_pct']))!=tuple(m[names[r['airline']]][1:])]
print('airline rows',len(rows),'mismatch',bad)
# time patterns: origin in the 39 airports
apl="("+",".join(f"'{a}'" for a in ap)+")"
h=f"{g} where Origin in {apl}"
def hl(i): return f"{i%12 or 12} {'AM' if i<12 else 'PM'}"
exp={}
for hr,n,d in duckdb.sql(f"select CRSDepTime//100,count(ArrDel15),round(100*sum(ArrDel15)/count(ArrDel15),2) from {h} group by 1").fetchall():
    exp[('scheduled_hour',hl(hr))]=(n,d,None)
dn=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
for dw,n,d in duckdb.sql(f"select DayOfWeek,count(ArrDel15),round(100*sum(ArrDel15)/count(ArrDel15),2) from {h} group by 1").fetchall(): exp[('weekday',dn[dw-1])]=(n,d,None)
mn=['January','February','March','April','May','June','July','August','September','October','November','December']
for mo,n,d,c in duckdb.sql(f"select Month,count(ArrDel15),round(100*sum(ArrDel15)/count(ArrDel15),2),round(100*sum(case when Year>=2024 then Cancelled end)/sum(case when Year>=2024 then 1 end),2) from {h} group by 1").fetchall(): exp[('month',mn[mo-1])]=(n,d,c)
bad=[];k=0
for r in csv.DictReader(open(S+'delayguard-time-patterns.csv')):
    k+=1;e=exp.get((r['dimension'],r['value']))
    if e!=(int(r['flights']),float(r['delay_rate_pct']),num(r['cancel_rate_pct'])): bad.append((r['dimension'],r['value'],e,r['flights'],r['delay_rate_pct'],r['cancel_rate_pct']))
print('time rows',k,'mismatch',len(bad));[print(b) for b in bad[:10]]
