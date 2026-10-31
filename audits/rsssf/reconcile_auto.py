"""Gerador conservador de candidatos Caixa x RSSSF (CSV previamente extraído)."""
import argparse,csv,json,re,unicodedata
from datetime import datetime
from difflib import SequenceMatcher

def norm(x):
 x=unicodedata.normalize("NFKD",str(x or ""))
 x="".join(c for c in x if not unicodedata.combining(c)).upper()
 return " ".join(re.sub(r"[^A-Z0-9]+"," ",x).split())

def date(x):
 m=re.search(r"\d{2}/\d{2}/\d{4}",str(x or ""))
 if m:return datetime.strptime(m.group(),"%d/%m/%Y").date()
 try:return datetime.fromisoformat(str(x)).date()
 except ValueError:return None

def canon(name,day,aliases):
 matches=set()
 for a in aliases:
  if norm(a["alias"])!=norm(name):continue
  if a.get("valid_from") and day and day.isoformat()<a["valid_from"]:continue
  if a.get("valid_to") and day and day.isoformat()>a["valid_to"]:continue
  matches.add(a["canonical_id"])
 if len(matches)>1:return "AMBIGUOUS"
 return next(iter(matches)) if matches else ""

def matches(c,r,aliases):
 if str(c.get("sorteio","")).upper()=="SIM":return []
 d=date(c.get("data_jogo"))
 if not d:return []
 ch=canon(c["equipe_1"],d,aliases);ca=canon(c["equipe_2"],d,aliases)
 if "AMBIGUOUS" in (ch,ca):return []
 result=[]
 for m in r:
  md=date(m["date"])
  if not md or abs((d-md).days)>1:continue
  if str(c["gols_1"])!=str(m["home_goals"]) or str(c["gols_2"])!=str(m["away_goals"]):continue
  mh=canon(m["home"],md,aliases);ma=canon(m["away"],md,aliases)
  if ch and mh and ch!=mh:continue
  if ca and ma and ca!=ma:continue
  hs=1.0 if ch and mh and ch==mh else SequenceMatcher(None,norm(c["equipe_1"]),norm(m["home"])).ratio()
  av=1.0 if ca and ma and ca==ma else SequenceMatcher(None,norm(c["equipe_2"]),norm(m["away"])).ratio()
  if min(hs,av)<.65:continue
  result.append({"competition":m["competition"],"rsssf_date":md.isoformat(),"rsssf_score":str(m["home_goals"])+"-"+str(m["away_goals"]),"source_url":m["source_url"],"home":m["home"],"away":m["away"],"similarity":round((hs+av)/2,4),"date_gap":abs((d-md).days)})
 return sorted(result,key=lambda x:(-x["similarity"],x["date_gap"]))

def read(path,sep=";"):
 with open(path,encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f,delimiter=sep))

def run(caixa,rsssf,aliases):
 out=[]
 for c in caixa:
  cand=matches(c,rsssf,aliases)
  status="sorteio_bloqueado" if str(c.get("sorteio","")).upper()=="SIM" else ("sem_candidato" if not cand else ("candidato_unico_revisao" if len(cand)==1 else "multiplos_candidatos_revisao"))
  out.append({"concurso":c["concurso"],"jogo":c["jogo"],"status":status,"candidate_count":len(cand),"candidates_json":json.dumps(cand,ensure_ascii=False),"review_required":"sim","elo_eligible":"nao"})
 return out

def main():
 p=argparse.ArgumentParser()
 for key in ("caixa","rsssf","aliases","out"):p.add_argument("--"+key,required=True)
 a=p.parse_args();data=run(read(a.caixa),read(a.rsssf),read(a.aliases,","))
 with open(a.out,"w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]),delimiter=";");w.writeheader();w.writerows(data)
 print(json.dumps({"rows":len(data),"statuses":{k:sum(v["status"]==k for v in data) for k in set(v["status"] for v in data)}}))
if __name__=="__main__":main()
