"""Diagnóstico conservador das partidas Caixa sem candidato RSSSF."""
import argparse,csv,json
from collections import Counter
from pathlib import Path
from datetime import timedelta
from difflib import SequenceMatcher
from audits.rsssf.reconcile_auto import read,norm,date,canon,run
def classify(c,source,aliases):
 d=date(c.get("data_jogo")); h=canon(c["equipe_1"],d,aliases); a=canon(c["equipe_2"],d,aliases)
 if not d:return "sem_data_caixa",[],0
 if h=="AMBIGUOUS" or a=="AMBIGUOUS":return "alias_ambiguo",[],0
 same_teams=[];near=[]
 for m in source:
  md=date(m.get("date"))
  if not md:continue
  mh=canon(m["home"],md,aliases);ma=canon(m["away"],md,aliases)
  def close(x,y,i,j):
   if x and y and x!="AMBIGUOUS" and y!="AMBIGUOUS":return x==y
   return SequenceMatcher(None,norm(i),norm(j)).ratio()>=.82
  if not(close(h,mh,c["equipe_1"],m["home"]) and close(a,ma,c["equipe_2"],m["away"])):continue
  delta=abs((d-md).days)
  score=str(c["gols_1"])==str(m["home_goals"]) and str(c["gols_2"])==str(m["away_goals"])
  if delta<=14:same_teams.append((m,delta,score))
  if delta<=1:near.append((m,delta,score))
 if any(x[2] and x[1]>1 for x in same_teams):
  label="divergencia_data_possivel"
 elif any(not x[2] for x in near):
  label="divergencia_placar_possivel"
 elif not h or not a:label="alias_ausente_ou_nao_coberto"
 else:label="competicao_ausente_ou_fonte_incompleta"
 selected=sorted(same_teams,key=lambda x:(x[1],not x[2]))[:5]
 candidates=[{"date":x[0]["date"],"home":x[0]["home"],"away":x[0]["away"],"score":x[0]["home_goals"]+"-"+x[0]["away_goals"],"source":x[0]["source_url"],"days_gap":x[1]} for x in selected]
 return label,candidates,len(same_teams)
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--archive",required=True);p.add_argument("--caixa",required=True);p.add_argument("--aliases",required=True)
 a=p.parse_args();root=Path(a.archive);aliases=read(a.aliases,",")
 reports=json.loads((root/"integrity_report.json").read_text(encoding="utf-8"))
 sources=[]
 for report in reports:
  path=root/report["id"]/"matches.csv"
  if path.exists():sources.extend(x for x in read(path) if x.get("result_type","played")=="played")
 caixa=[x for x in read(a.caixa) if 32<=int(x["concurso"])<=50]
 match_results=run(caixa,sources,aliases)
 items=[]
 for c,m in zip(caixa,match_results):
  if m["status"]!="sem_candidato":continue
  label,suggestions,n=classify(c,sources,aliases)
  items.append({"concurso":c["concurso"],"jogo":c["jogo"],"data_caixa":c["data_jogo"],
    "mandante_caixa":c["equipe_1"],"visitante_caixa":c["equipe_2"],
    "placar_caixa":str(c["gols_1"])+"-"+str(c["gols_2"]),"categoria_provisoria":label,
    "candidatos_proximos":n,"evidencias_json":json.dumps(suggestions,ensure_ascii=False),"aprovado_elo":"nao"})
 out=root/"diagnostico_sem_candidato_0032_0050.csv"
 with out.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(items[0]) if items else ["concurso","jogo"],delimiter=";");w.writeheader();w.writerows(items)
 result={"total":len(items),"categorias":dict(Counter(x["categoria_provisoria"] for x in items)),"aprovados_elo":0}
 (root/"diagnostico_sem_candidato_resumo.json").write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding="utf-8")
 print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
