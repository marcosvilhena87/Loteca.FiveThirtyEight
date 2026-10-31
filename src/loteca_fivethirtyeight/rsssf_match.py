"""Matcher auditável RSSSF: sem correspondência baseada apenas em placar."""
from __future__ import annotations
import argparse
import csv
import datetime as dt
import json
import re
import unicodedata
import urllib.request
from collections import defaultdict
from pathlib import Path
from html import unescape

ALIASES = {
 "S PAULO": "SAO PAULO", "SAO PAULO FC":"SAO PAULO",
 "SAO CAETANO":"SAO CAETANO", "AD SAO CAETANO":"SAO CAETANO",
 "P DESPORTOS":"PORTUGUESA", "PORTUGUESA DE DESPORTOS":"PORTUGUESA",
 "VASCO":"VASCO DA GAMA", "CR VASCO DA GAMA":"VASCO DA GAMA",
 "ETTI JUNDIAI":"JUNDIAI", "JUNDIAI FC":"JUNDIAI",
 "ATHLETICO":"ATLETICO PR", "ATLETICO PARANAENSE":"ATLETICO PR",
 "ATLETICO PR":"ATLETICO PR", "ATLETICO MG":"ATLETICO MG",
 "CR FLAMENGO":"FLAMENGO", "SC CORINTHIANS PAULISTA":"CORINTHIANS",
 "SE PALMEIRAS":"PALMEIRAS", "SANTOS FC":"SANTOS",
 "AA PONTE PRETA":"PONTE PRETA", "FLUMINENSE FC":"FLUMINENSE",
 "AMERICANO FC":"AMERICANO", "BANGU AC":"BANGU",
}
STATES = {"AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MG","MS","MT","PA","PB","PE","PI","PR","RJ","RN","RO","RR","RS","SC","SE","SP","TO"}
DATE_RE = re.compile(r"(\d{2})/(\d{2})/(\d{4})")
MATCH_RE = re.compile(r"^\s*([\wÀ-ÿ ./'()–-]+?)\s+(\d{1,2})\s*[-–]\s*(\d{1,2})\s+([\wÀ-ÿ ./'()–-]+?)\s*$")

def normalize(name: str) -> str:
    name = unicodedata.normalize("NFKD", name.upper())
    name = "".join(c for c in name if not unicodedata.combining(c))
    name = re.sub(r"/(?:%s)$" % "|".join(sorted(STATES)), "", name.strip())
    name = re.sub(r"[^A-Z0-9]+", " ", name).strip()
    return ALIASES.get(name, name)

def parse_date(value: str):
    match = DATE_RE.search(value or "")
    if not match:
        return None
    try:
        return dt.date(int(match[3]), int(match[2]), int(match[1]))
    except ValueError:
        return None

def load_loteca(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        for record in csv.DictReader(f, delimiter=";"):
            yield record

def parse_rsssf_text(text: str, *, competition: str, url: str, year: int, category: str = "PRINCIPAL"):
    """Aceita tabelas RSSSF em formato texto: cabeçalho [Feb 17] e partidas A 2-1 B.
    Confrontos sem data permanecem sem data: não presumir rodada/dia.
    """
    current = None
    month_map = {m:i for i,m in enumerate(("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"),1)}
    for line_no,line in enumerate(text.splitlines(),1):
        date_match = re.search(r"\[\s*([A-Za-z]{3})\s+(\d{1,2})\s*\]",line)
        if date_match and date_match[1].title() in month_map:
            month,day=month_map[date_match[1].title()],int(date_match[2])
            try: current=dt.date(year,month,day)
            except ValueError: current=None
            continue
        match = MATCH_RE.match(line)
        if match:
            home,ga,gb,away = match.groups()
            yield {"home":home, "away":away,"goals_home":int(ga),"goals_away":int(gb),
                   "date":current.isoformat() if current else "","competition":competition,
                   "category":category,"url":url,"line":line_no,"year":year}

def html_to_text(html: str) -> str:
    html=re.sub(r"<(?:br|/p|/div)\b[^>]*>", "\n", html, flags=re.I)
    html=re.sub(r"<[^>]+>", "", html)
    return unescape(html)

def download_catalog(manifest: Path, destination: Path):
    """Manifest CSV: competition;year;category;url. Apenas fontes autorizadas RSSSF."""
    destination.mkdir(parents=True,exist_ok=True)
    with manifest.open(encoding="utf-8-sig",newline="") as f:
        entries=list(csv.DictReader(f,delimiter=";"))
    rows=[]
    for i,entry in enumerate(entries):
        url=entry["url"]
        if not re.fullmatch(r"https://(?:www\.)?(?:rsssfbrasil\.com|rsssf\.org)/[^\s]+", url):
            raise ValueError("URL fora dos domínios RSSSF: "+url)
        req=urllib.request.Request(url,headers={"User-Agent":"LotecaResearchAudit/1.0 (educational)"})
        with urllib.request.urlopen(req,timeout=30) as response:
            data=response.read().decode(response.headers.get_content_charset() or "utf-8",errors="replace")
        text=html_to_text(data)
        rows.extend(parse_rsssf_text(text,competition=entry["competition"],url=url,year=int(entry["year"]),category=entry.get("category","PRINCIPAL")))
    path=destination/"rsssf_catalog.csv"
    if rows:
        with path.open("w",encoding="utf-8",newline="") as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    return len(rows)

def match_games(games, references, max_days=3):
    index=defaultdict(list)
    for r in references:
        key=(normalize(r["home"]),normalize(r["away"]),int(r["goals_home"]),int(r["goals_away"]))
        index[key].append(r)
    for game in games:
        original=dict(game)
        home,away=normalize(game["equipe_1"]),normalize(game["equipe_2"])
        goals=(int(game["gols_1"]),int(game["gols_2"]))
        day=parse_date(game.get("data_jogo",""))
        candidates=[]
        for ref in index.get((home,away,*goals),[]):
            try: refdate=dt.date.fromisoformat(ref["date"]) if ref.get("date") else None
            except ValueError: refdate=None
            if day and refdate:
                delta=abs((refdate-day).days)
                if delta>max_days: continue
            else: delta=None
            # Filtro anual obrigatório, mesmo quando a data exata está ausente.
            year=day.year if day else parse_date(game.get("data_apuracao",""))
            year=year.year if isinstance(year,dt.date) else None
            if year is not None and abs(year-int(ref["year"]))>1:continue
            candidates.append((delta,ref))
        candidates.sort(key=lambda x:(x[0] is None,x[0] if x[0] is not None else 999,x[1]["url"]))
        unique={(r["url"],r["competition"],r.get("date",""),r["home"],r["away"]) for _,r in candidates}
        if not candidates: status="PENDENTE_RSSSF"
        elif len(unique)>1: status="AMBIGUO"
        elif candidates[0][0] is None: status="REVISAO_DATA"
        elif candidates[0][1].get("category","PRINCIPAL").upper()!="PRINCIPAL":status="OUTRA_CATEGORIA"
        else:status="CONFIRMADO_PRINCIPAL"
        best=candidates[0][1] if candidates else {}
        original.update({"status_rsssf":status,"competition_rsssf":best.get("competition",""),
                         "category_rsssf":best.get("category",""),"date_rsssf":best.get("date",""),
                         "url_rsssf":best.get("url",""),"reference_line":best.get("line",""),
                         "candidates":len(unique)})
        yield original

def cli():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True,help="pasta dos 13 CSVs")
    p.add_argument("--catalog",type=Path,required=True,help="RSSSF catalog.csv")
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--days",type=int,default=3)
    args=p.parse_args()
    games=[g for path in sorted(args.source.glob("Loteca_*.csv")) for g in load_loteca(path)]
    with args.catalog.open(encoding="utf-8-sig",newline="") as f: refs=list(csv.DictReader(f))
    result=list(match_games(games,refs,args.days))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(result[0].keys()),delimiter=";");w.writeheader();w.writerows(result)
    from collections import Counter
    print(json.dumps({"total":len(result),"status":dict(Counter(x["status_rsssf"] for x in result))},ensure_ascii=False))

if __name__=="__main__":cli()
