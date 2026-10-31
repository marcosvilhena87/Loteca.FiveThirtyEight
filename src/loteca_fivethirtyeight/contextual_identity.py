"""Resolução contextual *não promocional*: uma fonte externa precisa provar a partida inteira.
Sem adversário identificado, data e placar exatos, não há resolução.
"""
import csv
import datetime as dt
from collections import defaultdict
from pathlib import Path
from .club_identity import clean, resolve
from .rsssf_match import parse_date

def contextual_candidates(games, references, registry):
    """Retorna auditoria individual: ID sugerido ou quarentena. Nunca altera o registro."""
    by_date=defaultdict(list)
    for ref in references:
        try: day=dt.date.fromisoformat(ref["date"])
        except (KeyError,ValueError,TypeError): continue
        if ref.get("category")!="PRINCIPAL" or not ref.get("competition") or not ref.get("url"):continue
        by_date[day].append(ref)
    for g in games:
        day=parse_date(g.get("data_jogo",""))
        year=day.year if day else None
        home_id=resolve(g["equipe_1"],year,registry) if year else None
        away_id=resolve(g["equipe_2"],year,registry) if year else None
        possibilities=[]
        if day and ((home_id is None) != (away_id is None)):
            for ref in by_date[day]:
                if (int(g["gols_1"]),int(g["gols_2"]))!=(int(ref["goals_home"]),int(ref["goals_away"])):continue
                ref_known=ref["away"] if home_id is None else ref["home"]
                known_id=away_id if home_id is None else home_id
                if resolve(ref_known,year,registry)!=known_id:continue
                ref_missing=ref["home"] if home_id is None else ref["away"]
                # Igualdade do nome-base é apenas uma *proposta*, nunca criação de identidade.
                lot_missing=g["equipe_1"] if home_id is None else g["equipe_2"]
                if clean(lot_missing.split("/")[0])!=clean(ref_missing.split("/")[0]):continue
                proposed=resolve(ref_missing,year,registry)
                if proposed and proposed != known_id:
                    possibilities.append((proposed,ref))
        unique={v[0] for v in possibilities}
        status="CANDIDATO_CONTEXTO_REVISAR" if len(unique)==1 else ("AMBIGUO_CONTEXTO" if len(unique)>1 else "QUARENTENA")
        evidence=possibilities[0][1] if status=="CANDIDATO_CONTEXTO_REVISAR" else {}
        yield {"concurso":g.get("concurso",""),"jogo":g.get("jogo",""),
               "data_jogo":g.get("data_jogo",""),"equipe_1":g["equipe_1"],"equipe_2":g["equipe_2"],
               "gols_1":g["gols_1"],"gols_2":g["gols_2"],
               "home_club_id":home_id or "","away_club_id":away_id or "",
               "candidate_id":next(iter(unique)) if len(unique)==1 else "",
               "status":status,"competition":evidence.get("competition",""),
               "source_url":evidence.get("url",""),"source_line":evidence.get("line",""),
               "matching_sources":len(possibilities)}

def export_contextual(games,references,registry,destination):
    rows=list(contextual_candidates(games,references,registry))
    Path(destination).parent.mkdir(parents=True,exist_ok=True)
    with Path(destination).open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=";");w.writeheader();w.writerows(rows)
    from collections import Counter
    return dict(Counter(r["status"] for r in rows))
