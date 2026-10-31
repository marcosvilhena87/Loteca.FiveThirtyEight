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
from .club_identity import resolve, read_registry

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
MATCH_RE = re.compile(r"^\s*(.+?)\s{2,}(\d{1,2})\s*[-–]\s*(\d{1,2})\s+(.+?)\s*$")
MONTH_RE = re.compile(r"\[\s*([A-Za-z]{3})\s+(\d{1,2})\s*\]")
SCORE_RE = re.compile(r"^\s*(.+?)\s+(\d{1,2})\s*[-–]\s*(\d{1,2})\s+(.+?)\s*$")


def state_code(name: str):
    m = re.search(r"/([A-Z]{2})$", name.strip().upper())
    return m[1] if m and m[1] in STATES else None

AMBIGUOUS_NAMES = {"AMERICA", "BOTAFOGO", "FLUMINENSE", "ATLETICO", "NACIONAL", "RIO BRANCO", "OPERARIO", "JUVENTUS", "PORTUGUESA"}

def compatible_identity(source: str, reference: str) -> bool:
    a, b = state_code(source), state_code(reference)
    if a and b and a != b:
        return False
    if normalize(source) in AMBIGUOUS_NAMES and (not a or not b):
        return False
    return True

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
    """Lê linhas RSSSF pré-formatadas; recusa linhas de classificação e comentários.
    Suporta [Feb 17], [Dec 31], placares A   2-4  B e nomes com /UF.
    Não inventa datas: ausência de cabeçalho gera data vazia.
    """
    current = None
    months = {m:i for i,m in enumerate(("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"),1)}
    for line_no, line in enumerate(text.splitlines(), 1):
        dm = MONTH_RE.search(line)
        if dm and dm[1].title() in months:
            try: current = dt.date(year, months[dm[1].title()], int(dm[2]))
            except ValueError: current = None
            continue
        m = SCORE_RE.match(line)
        if not m: continue
        home, ga, gb, away = m.groups()
        home, away = home.strip(), re.split(r"\s+\[played\b", away.strip(), flags=re.I)[0].strip()
        if home.startswith("[") or away.startswith("[") or not re.search(r"[A-Za-zÀ-ÿ]",home) or not re.search(r"[A-Za-zÀ-ÿ]",away):
            continue
        yield {"home":home,"away":away,"goals_home":int(ga),"goals_away":int(gb),
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

def match_games(games, references, max_days=3, registry=None):
    index=defaultdict(list)
    for r in references:
        year=int(r["year"])
        ids=(resolve(r["home"],year,registry),resolve(r["away"],year,registry)) if registry is not None else (None,None)
        key=(*ids,int(r["goals_home"]),int(r["goals_away"])) if registry is not None else (normalize(r["home"]),normalize(r["away"]),int(r["goals_home"]),int(r["goals_away"]))
        index[key].append(r)
    for game in games:
        original=dict(game)
        home,away=normalize(game["equipe_1"]),normalize(game["equipe_2"])
        goals=(int(game["gols_1"]),int(game["gols_2"]))
        day=parse_date(game.get("data_jogo",""))
        year_date=day or parse_date(game.get("data_apuracao",""))
        game_year=year_date.year if year_date else None
        ids=(resolve(game["equipe_1"],game_year,registry),resolve(game["equipe_2"],game_year,registry)) if registry is not None and game_year else (None,None)
        unresolved=registry is not None and (not game_year or None in ids)
        original["home_club_id"]=ids[0] or ""
        original["away_club_id"]=ids[1] or ""
        candidates=[]
        key=(*ids,*goals) if registry is not None else (home,away,*goals)
        for ref in ([] if unresolved else index.get(key,[])):
            if registry is None and (not compatible_identity(game["equipe_1"],ref["home"]) or not compatible_identity(game["equipe_2"],ref["away"])):
                continue
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
        if unresolved: status="ALIAS_NAO_RESOLVIDO"
        elif not candidates: status="PENDENTE_RSSSF"
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
    p.add_argument("--registry",type=Path)
    p.add_argument("--alias-review",type=Path)
    args=p.parse_args()
    games=[g for path in sorted(args.source.glob("Loteca_*.csv")) for g in load_loteca(path)]
    with args.catalog.open(encoding="utf-8-sig",newline="") as f: refs=list(csv.DictReader(f))
    registry=read_registry(args.registry) if args.registry else None
    result=list(match_games(games,refs,args.days,registry))
    if args.alias_review:
        args.alias_review.parent.mkdir(parents=True,exist_ok=True)
        review=defaultdict(lambda: {"count":0,"examples":[]})
        for game,row in zip(games,result):
            if row["status_rsssf"]!="ALIAS_NAO_RESOLVIDO":continue
            year_date=parse_date(game.get("data_jogo","")) or parse_date(game.get("data_apuracao",""))
            for side,field in (("home","equipe_1"),("away","equipe_2")):
                if not row[side+"_club_id"]:
                    key=(game[field],year_date.year if year_date else "")
                    review[key]["count"]+=1
                    if len(review[key]["examples"])<3:review[key]["examples"].append(str(game["concurso"])+"/"+str(game["jogo"]))
        with args.alias_review.open("w",encoding="utf-8",newline="") as f:
            w=csv.writer(f,delimiter=";");w.writerow(["alias_original","ano","ocorrencias","exemplos_concurso_jogo","status"])
            for (alias,year),info in sorted(review.items(),key=lambda x:(-x[1]["count"],x[0])):
                w.writerow([alias,year,info["count"],",".join(info["examples"]),"REVISAO_MANUAL"])
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(result[0].keys()),delimiter=";");w.writeheader();w.writerows(result)
    from collections import Counter
    print(json.dumps({"total":len(result),"status":dict(Counter(x["status_rsssf"] for x in result))},ensure_ascii=False))

if __name__=="__main__":cli()
