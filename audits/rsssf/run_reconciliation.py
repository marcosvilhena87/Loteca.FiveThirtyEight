"""Concilia snapshot da Caixa com todas as partidas RSSSF extraídas e gera métricas."""
import argparse,csv,json
from pathlib import Path
from collections import Counter
from audits.rsssf.reconcile_auto import read,run
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--archive",required=True);p.add_argument("--caixa",required=True);p.add_argument("--aliases",required=True)
 a=p.parse_args();root=Path(a.archive);reports=json.loads((root/"integrity_report.json").read_text())
 matches=[];source_summary=[]
 for record in reports:
  path=root/record["id"]/"matches.csv"
  if path.exists():matches.extend(x for x in read(path) if x.get("result_type","played")=="played")
  source_summary.append({"source":record["id"],"integrity":record.get("integrity","error"),"rows":record.get("rows",0),"issues":record.get("issues",[])})
 caixa=[r for r in read(a.caixa) if 32<=int(r["concurso"])<=50]
 candidates=run(caixa,matches,read(a.aliases,","))
 with (root/"caixa_0032_0050_candidates.csv").open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(candidates[0]),delimiter=";");w.writeheader();w.writerows(candidates)
 summary={"caixa_rows":len(caixa),"rsssf_rows":len(matches),"statuses":dict(Counter(r["status"] for r in candidates)),"sources":source_summary,"elo_approved":0}
 (root/"conciliation_summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding="utf-8")
 print(json.dumps(summary,ensure_ascii=False))
if __name__=="__main__":main()
