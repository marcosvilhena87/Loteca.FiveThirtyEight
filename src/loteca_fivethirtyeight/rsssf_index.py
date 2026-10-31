"""Indexação conservadora RSSSF 2002-2026.
Gera candidatos, valida URLs e prioriza séries que aparecem em temporadas da Loteca.
Nunca promove URL candidata a evidência confirmada sem extração e matching.
"""
import argparse
import csv
import datetime as dt
import json
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path
from loteca_fivethirtyeight.rsssf_match import load_loteca, parse_date

SERIES = {
    "Brasileiro Serie A": "https://www.rsssfbrasil.com/tablesae/br{year}.htm",
    "Brasileiro Serie B": "https://www.rsssfbrasil.com/tablesae/br2{year}.htm",
    "Brasileiro Serie C": "https://www.rsssfbrasil.com/tablesae/br3{year}.htm",
    "Copa do Brasil": "https://www.rsssfbrasil.com/tablesae/cbr{year}.htm",
    "Carioca Serie A": "https://www.rsssfbrasil.com/tablesr/rj{year}.htm",
    "Paulista Serie A1": "https://www.rsssfbrasil.com/tablessz/sp{year}.htm",
    "Mineiro": "https://www.rsssfbrasil.com/tablesfq/mg{year}.htm",
    "Gaucho": "https://www.rsssfbrasil.com/tablesr/rs{year}.htm",
}
CATEGORIES = {k: "PRINCIPAL" for k in SERIES}
def proposals(root: Path):
    years=Counter()
    for file in sorted(root.glob("Loteca_*.csv")):
        for g in load_loteca(file):
            date=parse_date(g.get("data_jogo","")) or parse_date(g.get("data_apuracao",""))
            if date: years[date.year]+=1
    for year in range(2002,2027):
        if year not in years: continue
        for competition,pattern in SERIES.items():
            yield {"competition":competition,"year":year,"category":CATEGORIES[competition],
                   "url":pattern.format(year=year),"year_loteca_games":years[year],
                   "status":"CANDIDATE_NOT_VERIFIED"}
def verify_url(url):
    req=urllib.request.Request(url,headers={"User-Agent":"LotecaResearchAudit/1.0"},method="GET")
    try:
        with urllib.request.urlopen(req,timeout=12) as res:
            body=res.read(131072)
            return res.status==200 and len(body)>300 and b"404 Not Found" not in body and b"Page Not Found" not in body
    except (urllib.error.URLError, TimeoutError, OSError): return False

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--verify",action="store_true")
    args=p.parse_args()
    rows=list(proposals(args.source))
    if args.verify:
        for row in rows:
            row["status"]="URL_REACHABLE_UNREVIEWED" if verify_url(row["url"]) else "URL_UNAVAILABLE"
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=";");w.writeheader();w.writerows(rows)
    print(json.dumps({"candidates":len(rows),"years":len(set(r["year"] for r in rows)),
                       "statuses":dict(Counter(r["status"] for r in rows))},ensure_ascii=False))
if __name__=="__main__":main()
