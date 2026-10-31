"""Extrator conservador de partidas internacionais RSSSF, sem promoção automática."""
import csv
import re
import urllib.request
from datetime import date
from html import unescape
from pathlib import Path

MONTHS={m:i for i,m in enumerate(("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"),1)}
MONTHS.update({"June":6,"July":7})
EURO_DATE=re.compile(r"\[\s*([A-Za-z]{3})\s+(\d{1,2})\s*\]")
EURO_RESULT=re.compile(r"^\s*(.{2,}?)\s{2,}(\d{1,2})\s*[-–]\s*(\d{1,2})\s+(.+?)\s*$")
FIFA_RESULT=re.compile(r"^\s*(\d{1,2})-\s*(\d{1,2})-(\d{2})\s+(.+?)\s{2,}(.+?)\s{2,}(\d{1,2})-(\d{1,2})\s+(.+?)\s*$")

def parse_europe(text,competition,season_end,url):
    # Only first-tier league section. Cups and lower divisions must not leak in.
    first={"La Liga":"Primera Divisi","Premier League":"Premier League","Serie A Italia":"Serie A"}[competition]
    lines=text.splitlines()
    began=False;day=None;round_seen=False
    for lineno,raw in enumerate(lines,1):
        line=unescape(raw).strip()
        if not began:
            if first.lower() in line.lower():began=True
            continue
        if any(x in line.lower() for x in ("segunda división","championship","serie b","fa cup","coppa italia","league cup")):break
        if re.search(r"\bRound\s+\d+\b",line,re.I):round_seen=True
        m=EURO_DATE.search(line)
        if m and m[1].title() in MONTHS:
            month=MONTHS[m[1].title()]
            year=season_end-1 if month>=7 else season_end
            try:day=date(year,month,int(m[2])).isoformat()
            except ValueError:day=None
            continue
        score=EURO_RESULT.match(raw)
        if not (score and day and round_seen):continue
        home,g1,g2,away=score.groups()
        if not re.search(r"[A-Za-z]",home+away):continue
        yield dict(home=home.strip(),away=away.strip(),goals_home=int(g1),goals_away=int(g2),
                   date=day,competition=competition,category="PRINCIPAL",url=url,line=lineno,year=season_end)

def parse_fifa(text,year,url):
    for lineno,line in enumerate(text.splitlines(),1):
        m=FIFA_RESULT.match(line)
        if not m:continue
        d,mo,yy,venue,home,g1,g2,away=m.groups()
        if int(yy)!=year%100:continue
        try:when=date(year,int(mo),int(d)).isoformat()
        except ValueError:continue
        yield dict(home=home.strip(),away=away.strip(),goals_home=int(g1),goals_away=int(g2),date=when,
                   competition="Mundial de Clubes FIFA",category="PRINCIPAL",url=url,line=lineno,year=year)

def parse_page(text,entry):
    if entry["parser"]=="rsssf_round":
        return list(parse_europe(text,entry["competition"],int(entry["reference_year"]),entry["url"]))
    if entry["parser"]=="rsssf_fifa_dated":
        return list(parse_fifa(text,int(entry["reference_year"]),entry["url"]))
    return []

def run(manifest,out):
    with open(manifest,encoding="utf-8",newline="") as f: entries=list(csv.DictReader(f,delimiter=";"))
    refs=[];audit=[]
    for entry in entries:
        row=dict(entry);row["parsed_games"]=0
        if entry["status"]!="PAGE_VERIFIED_UNPARSED" or not entry["url"]:
            audit.append(row);continue
        try:
            req=urllib.request.Request(entry["url"],headers={"User-Agent":"LotecaAuditResearch/1.0"})
            with urllib.request.urlopen(req,timeout=20) as response:
                raw=response.read()
            text=unescape(re.sub(r"<[^>]*>","",re.sub(r"(?i)<br\s*/?>","\n",raw.decode("utf-8",errors="replace"))))
            got=parse_page(text,entry)
            row["parsed_games"]=len(got)
            row["status"]="PARSED_NEEDS_REVIEW" if got else "NO_MATCHES_PARSED"
            refs+=got
        except Exception as e: row["status"]="FETCH_OR_PARSE_ERROR";row["error"]=str(e)[:150]
        audit.append(row)
    Path(out).mkdir(parents=True,exist_ok=True)
    for filename,records in (("international_matches.csv",refs),("international_source_audit.csv",audit)):
        if records:
            with (Path(out)/filename).open("w",encoding="utf-8",newline="") as f:
                w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in records for k in r)),delimiter=";");w.writeheader();w.writerows(records)
    return audit

if __name__=="__main__":
    import sys,json
    print(json.dumps(run(sys.argv[1],sys.argv[2]),ensure_ascii=False))
