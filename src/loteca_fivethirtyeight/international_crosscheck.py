"""Cruzamento estrito por competição, identidades das DUAS equipes, data e placar.
Resultado é fila de revisão, nunca certificação nem atualização automática Elo."""
import csv
from collections import defaultdict
from pathlib import Path
from .club_identity import clean
from .rsssf_match import parse_date,load_loteca

def match_context(games,refs,scope,source_status):
    lookup=defaultdict(set)
    for row in scope:
        for y in range(int(row["since"]),int(row["until"])+1):
            lookup[(row["competition"],clean(row["alias"]),y)].add(row["club_id"])
    index=defaultdict(list)
    for r in refs:
        if not r.get("date"):continue
        index[(r["date"],int(r["goals_home"]),int(r["goals_away"]))].append(r)
    for g in games:
        date=parse_date(g.get("data_jogo",""))
        if not date:continue
        key=(date.isoformat(),int(g["gols_1"]),int(g["gols_2"]))
        candidates=[]
        for r in index[key]:
            tournament=r["competition"];yr=date.year
            a=lookup[(tournament,clean(g["equipe_1"]),yr)] & lookup[(tournament,clean(r["home"]),yr)]
            b=lookup[(tournament,clean(g["equipe_2"]),yr)] & lookup[(tournament,clean(r["away"]),yr)]
            if len(a)!=1 or len(b)!=1:continue
            x,y=next(iter(a)),next(iter(b))
            if x==y:continue
            candidates.append((x,y,r))
        distinct={(x,y,r["competition"],r["url"]) for x,y,r in candidates}
        if len(distinct)!=1:continue
        x,y,r=candidates[0]
        status="REVIEW_ONLY_SOURCE_COUNT_MISMATCH" if source_status.get(r["competition"])!="PARSED_NEEDS_REVIEW" else "REVIEW_ONLY_UNVERIFIED_ALIAS"
        yield {"concurso":g.get("concurso",""),"jogo":g.get("jogo",""),"date":date.isoformat(),
               "home_caixa":g["equipe_1"],"away_caixa":g["equipe_2"],"score":str(g["gols_1"])+"-"+str(g["gols_2"]),
               "home_club_id_candidate":x,"away_club_id_candidate":y,
               "competition":r["competition"],"url":r["url"],"line":r.get("line",""),"status":status}

def cli():
    import sys,json
    src,catalog,alias,source_audit,out=sys.argv[1:]
    games=[g for p in sorted(Path(src).glob("Loteca_*.csv")) for g in load_loteca(p)]
    def read(path):
        with open(path,encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f,delimiter=";"))
    rows=read(catalog) if Path(catalog).exists() else []
    scope=read(alias);audit={r["competition"]:r["status"] for r in read(source_audit)}
    results=list(match_context(games,rows,scope,audit))
    Path(out).parent.mkdir(parents=True,exist_ok=True)
    with open(out,"w",encoding="utf-8",newline="") as f:
        fields=["concurso","jogo","date","home_caixa","away_caixa","score","home_club_id_candidate","away_club_id_candidate","competition","url","line","status"]
        w=csv.DictWriter(f,delimiter=";",fieldnames=fields);w.writeheader();w.writerows(results)
    print(json.dumps({"review_candidates":len(results),"statuses":{s:sum(x["status"]==s for x in results) for s in set(x["status"] for x in results)}}))
if __name__=="__main__":cli()
