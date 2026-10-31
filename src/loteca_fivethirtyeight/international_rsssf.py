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
EURO_RESULT=re.compile(r"^\s*(.{2,}?)\s+(\d{1,2})\s*[-–]\s*(\d{1,2})\s+(.+?)\s*$")
FIFA_RESULT=re.compile(r"^\s*(\d{1,2})-\s*(\d{1,2})-(\d{2})\s+(.+?)\s{2,}(.+?)\s{2,}(\d{1,2})-(\d{1,2})\s+(.+?)\s*$")

def parse_europe(text,competition,season_end,url):
    # Only first-tier league section. Cups and lower divisions must not leak in.
    first={"La Liga":"Primera Divisi","Premier League":"Premier League","Serie A Italia":"Serie A"}[competition]
    lines=text.splitlines()
    began=False;day=None;round_seen=False;round_no=None;per_round={};seen=set()
    for lineno,raw in enumerate(lines,1):
        line=unescape(raw).strip()
        if not began:
            if first.lower() in line.lower():began=True
            continue
        if round_seen and re.search(r"^(?:Copa del Rey|Cup Tournaments|FA Cup|Coppa Italia|Segunda Divisi|Championship|Serie B)\b",line,re.I):break
        round_match=re.search(r"^Round\s+(\d+)\b",line,re.I)
        if round_match:
            round_no=int(round_match[1]);round_seen=True
            if round_no>38 or (round_no==1 and len(per_round)>=38):break
        m=EURO_DATE.search(line)
        if m and m[1].title() in MONTHS:
            month=MONTHS[m[1].title()]
            year=season_end-1 if month>=7 else season_end
            try:day=date(year,month,int(m[2])).isoformat()
            except ValueError:day=None
            if not round_match:continue
        score=EURO_RESULT.match(raw)
        if not (score and round_seen and round_no is not None and 1<=round_no<=38):continue
        home,g1,g2,away=score.groups()
        # RSSSF pode registrar jogos abandonados e comentários com placares internos.
        if "[" in home or "]" in home or re.search(r"\babd\b",home,re.I):continue
        away=re.split(r"\s{2,}|\s+\[",away,maxsplit=1)[0].strip()
        if not re.search(r"[A-Za-z]",home+away):continue
        if per_round.get(round_no,0)>=10:continue
        match_key=(round_no,home.strip(),away.strip())
        if match_key in seen:continue
        seen.add(match_key);per_round[round_no]=per_round.get(round_no,0)+1
        yield dict(home=home.strip(),away=away.strip(),goals_home=int(g1),goals_away=int(g2),
                   date=day or "",round=round_no,competition=competition,category="PRINCIPAL",url=url,line=lineno,year=season_end)

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
            charset=response.headers.get_content_charset() or "utf-8"
            try: decoded=raw.decode(charset)
            except (UnicodeDecodeError,LookupError): decoded=raw.decode("latin-1")
            text=unescape(re.sub(r"<[^>]*>","",re.sub(r"(?i)<br\s*/?>","\n",decoded)))
            got=parse_page(text,entry)
            row["parsed_games"]=len(got)
            row["missing_dates"]=sum(not r["date"] for r in got)
            row["unique_fixtures"]=len({(r["home"],r["away"]) for r in got})
            expected=380 if entry["competition"] in ("La Liga","Premier League","Serie A Italia") else None
            if expected:
                from collections import Counter
                n=Counter(int(r["round"]) for r in got if r.get("round"))
                row["underfull_rounds"]=",".join(f"{i}:{n[i]}" for i in range(1,39) if n[i]!=10)
            row["status"]=("COUNT_MISMATCH_QUARANTINE" if expected is not None and (len(got)!=expected or row["missing_dates"] or row["unique_fixtures"]!=expected) else "PARSED_NEEDS_REVIEW") if got else "NO_MATCHES_PARSED"
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
