"""Auditoria de evidência de cada candidato, sem promoção automática ao Elo.

Saídas: audit_candidates.csv, audit_summary.json.
A vinculação excepcional 0048/01 é respaldada por fontes independentes e não
altera a data no snapshot RSSSF. Requer aprovação documental humana.
"""
import argparse,csv,json
from collections import Counter
from pathlib import Path
from audits.rsssf.reconcile_auto import read,run,canon,canon_source,date,norm

SOURCES_VASCO=[
 "https://www.netvasco.com.br/news/noticias07/9957.shtml",
 "https://www.bolanaarea.com/estaduais_rj_2003.htm",
 "https://mprais.netvasco.com.br/vasco/2003rj.html",
]
def audit_row(c,candidates,sources,aliases):
 key=(int(c["concurso"]),int(c["jogo"]))
 out={"concurso":c["concurso"],"jogo":c["jogo"],"data_caixa":date(c.get("data_jogo")).isoformat() if date(c.get("data_jogo")) else "",
  "home_caixa":c["equipe_1"],"away_caixa":c["equipe_2"],"score_caixa":str(c["gols_1"])+"-"+str(c["gols_2"]),
  "status":"", "canonical_home":"","canonical_away":"","source_url":"","source_date":"","source_score":"",
  "competition":"","evidence_urls_json":"[]","reason":"","elo_eligible":"nao"}
 if str(c.get("sorteio","")).upper()=="SIM":
  out["status"]="sorteio_bloqueado";out["reason"]="Sorteio não corresponde a resultado disputado";return out
 d=date(c.get("data_jogo"));h=canon(c["equipe_1"],d,aliases);a=canon(c["equipe_2"],d,aliases)
 out["canonical_home"]=h;out["canonical_away"]=a
 if key==(48,1):
  # A correção é independente da lista de candidatos (limite normal ±1 dia)
  possible=[x for x in sources if x["competition"]=="Campeonato Carioca 2003" and
   x["date"]=="2003-01-16" and x["home_goals"]=="1" and x["away_goals"]=="0" and
   norm(x["home"])=="VASCO DA GAMA" and norm(x["away"]) in ("AMERICA","AM RICA")]
  if len(possible)==1 and d and d.isoformat()=="2003-01-18" and h=="BR_RJ_VASCO" and a=="BR_RJ_AMERICA":
   m=possible[0];out.update(status="data_rsssf_divergente_documentada",source_url=m["source_url"],
    source_date=m["date"],source_score="1-0",competition=m["competition"],
    evidence_urls_json=json.dumps([m["source_url"]]+SOURCES_VASCO),reason="Caixa 18/01/2003; RSSSF 16/01/2003; fontes independentes confirmam 18/01; manter RSSSF sem alteração")
  else:out.update(status="divergencia_sem_confirmacao",reason="Exceção não corresponde exatamente à fonte esperada; revisar")
  return out
 if len(candidates)!=1:
  out["status"]="sem_candidato" if not candidates else "multiplos_candidatos"
  out["reason"]="Nenhum vínculo único identificado sob as regras atuais";return out
 candidate=candidates[0]
 possible=[m for m in sources if m["source_url"]==candidate["source_url"] and m["date"]==candidate["rsssf_date"] and
  m["competition"]==candidate["competition"] and m["home"]==candidate["home"] and m["away"]==candidate["away"] and
  str(m["home_goals"])+"-"+str(m["away_goals"])==candidate["rsssf_score"]]
 if len(possible)!=1:
  out.update(status="fonte_nao_univoca",reason="Não foi possível identificar uma única linha original");return out
 m=possible[0];md=date(m["date"])
 sh=canon_source(m["home"],md,aliases,m["competition"]);sa=canon_source(m["away"],md,aliases,m["competition"])
 out.update(source_url=m["source_url"],source_date=m["date"],source_score=candidate["rsssf_score"],
  competition=m["competition"],evidence_urls_json=json.dumps([m["source_url"]]))
 if not h or not a or h=="AMBIGUOUS" or a=="AMBIGUOUS" or not sh or not sa or sh=="AMBIGUOUS" or sa=="AMBIGUOUS":
  out.update(status="identidade_incompleta",reason="Falta ID canônico inequívoco em pelo menos um clube");return out
 if h!=sh or a!=sa:
  out.update(status="identidade_divergente",reason="IDs canônicos não coincidem");return out
 if out["data_caixa"]!=m["date"]:
  out.update(status="data_divergente",reason="Data RSSSF difere da data Caixa; requer fontes independentes");return out
 if out["score_caixa"]!=out["source_score"]:
  out.update(status="placar_divergente",reason="Placares diferentes");return out
 out["status"]="evidencia_estrita_para_revisao"
 out["reason"]="Identidade, data, placar, competição e linha RSSSF coincidem; homologação humana ainda necessária"
 return out
def main():
 p=argparse.ArgumentParser()
 for key in ("archive","caixa","aliases"):p.add_argument("--"+key,required=True)
 a=p.parse_args();root=Path(a.archive);reports=json.loads((root/"integrity_report.json").read_text())
 sources=[]
 for r in reports:
  pth=root/r["id"]/"matches.csv"
  if r.get("integrity")=="pass" and pth.exists():
   sources.extend(m for m in read(pth) if m.get("result_type","played")=="played")
 caixa=[c for c in read(a.caixa) if 32<=int(c["concurso"])<=50]
 aliases=read(a.aliases,",")
 rows=run(caixa,sources,aliases)
 audited=[audit_row(c,json.loads(r["candidates_json"]),sources,aliases) for c,r in zip(caixa,rows)]
 with (root/"audit_candidates.csv").open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(audited[0]),delimiter=";");w.writeheader();w.writerows(audited)
 summary={"caixa_total":len(caixa),"statuses":dict(Counter(x["status"] for x in audited)),
   "eligible_for_elo":0,"manual_approval_required":True,"special_case":"0048/01"}
 (root/"audit_summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding="utf-8")
 print("STRICT_AUDIT",json.dumps(summary,ensure_ascii=False))
if __name__=="__main__":main()
