"""Separate first/second legs of RSSSF Brazilian 2002 knockout ties."""
import re
from datetime import date
from audits.rsssf.ingest_sources import Page,MONTHS

TIE=re.compile(r"^\s*(?P<a>.+?)\s{2,}(?P<h1>\d+)-(?P<a1>\d+)\s+(?P<h2>\d+)-(?P<a2>\d+)\s{2,}(?P<b>.+?)\s*$")
DATES=re.compile(r"^\s*\[(?P<m1>[A-Za-z]{3})\s+(?P<d1>\d{1,2})\s+and\s+(?:(?P<m2>[A-Za-z]{3})\s+)?(?P<d2>\d{1,2})\]\s*$",re.I)
PHASE={"Quarterfinals":"quarterfinal","Semi-finals":"semifinal","Finals":"final"}
def extract_knockouts(html_text,competition,url,year=2002):
 p=Page();p.feed(html_text);text=p.text()
 phase=None;dates=None;rows=[];warnings=[];seen=set()
 for lineno,line in enumerate(text.splitlines(),1):
  s=line.strip()
  if s in PHASE:
   phase=PHASE[s];dates=None;continue
  if phase is None:continue
  if s in ("First Leg","Second Leg") or s.startswith("are prometed") or "are the 2002 Brazilian" in s:
   if s=="First Leg":phase=None
   continue
  d=DATES.match(s)
  if d:
   m1,d1,m2,d2=d["m1"],int(d["d1"]),d["m2"] or d["m1"],int(d["d2"])
   try:dates=(date(year,MONTHS[m1.title()],d1).isoformat(),date(year,MONTHS[m2.title()],d2).isoformat())
   except (ValueError,KeyError):dates=None;warnings.append({"line":lineno,"issue":"invalid_leg_dates"})
   continue
  m=TIE.match(line)
  if not m:continue
  if dates is None:
   warnings.append({"line":lineno,"issue":"tie_without_dates"});continue
  a,b=m["a"].strip(),m["b"].strip()
  if not(2<=len(a)<=60 and 2<=len(b)<=60):continue
  # RSSSF gives both scores from first-listed club's perspective;
  # the second leg reverses home team and goals.
  for leg,dt,home,away,hg,ag in (
   ("ida",dates[0],a,b,m["h1"],m["a1"]),
   ("volta",dates[1],b,a,m["a2"],m["h2"])):
   key=(dt,home,away,phase)
   if key in seen:warnings.append({"line":lineno,"issue":"duplicate_leg","leg":leg});continue
   seen.add(key)
   rows.append({"date":dt,"home":home,"away":away,"home_goals":hg,"away_goals":ag,
     "competition":competition,"source_url":url,"source_line":lineno,"phase":phase,
     "leg":leg,"result_type":"played","round":""})
 return rows,warnings
