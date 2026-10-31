"""Audit the 26-club single round-robin in Brazil's first two 2002 divisions."""
import csv,json,unicodedata,re
from collections import Counter,defaultdict
from itertools import combinations
from pathlib import Path
from audits.rsssf.ingest_sources import Page
def normal(name):
 x=unicodedata.normalize("NFKD",name).encode("ascii","ignore").decode().casefold()
 return re.sub(r"[^a-z0-9]+"," ",x).strip()
def audit(path,expected_teams=26):
 with open(path,encoding="utf-8-sig",newline="") as f:allrows=list(csv.DictReader(f,delimiter=";"))
 regular=[r for r in allrows if r.get("phase")=="league"]
 by_pair=defaultdict(list);by_team=Counter()
 for r in regular:
  h,a=normal(r["home"]),normal(r["away"])
  by_pair[tuple(sorted((h,a)))].append(r)
  by_team[h]+=1;by_team[a]+=1
 duplicates={str(pair):[{"date":r["date"],"home":r["home"],"away":r["away"],"score":r["home_goals"]+"-"+r["away_goals"],"source_line":r.get("source_line")} for r in vals] for pair,vals in by_pair.items() if len(vals)>1}
 # Unknown team aliases produce false gaps: diagnostics, not automatic mutations
 return {"regular_rows":len(regular),"unique_unordered_fixtures":len(by_pair),"expected":expected_teams*(expected_teams-1)//2,"duplicate_pairs":duplicates,"club_appearances":dict(sorted(by_team.items())),"distinct_names":len(by_team),"counts_unequal_25":{t:n for t,n in by_team.items() if n!=25},"phase_counts":dict(Counter(r.get("phase") for r in allrows))}
def main():
 import argparse
 p=argparse.ArgumentParser();p.add_argument("--archive",required=True);args=p.parse_args()
 summary={}
 for name in ("br2002_a","br2002_b"):
  summary[name]=audit(Path(args.archive)/name/"matches.csv")
 out=Path(args.archive)/"brazil_2002_fixture_audit.json"
 out.write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
 for k,v in summary.items():
  print("ROUND_ROBIN_AUDIT",k,json.dumps(v,ensure_ascii=False))
  if v["regular_rows"]!=325 or v["unique_unordered_fixtures"]!=325 or v["distinct_names"]!=26 or v["counts_unequal_25"] or v["duplicate_pairs"] or v["phase_counts"]!={"league":325,"quarterfinal":8,"semifinal":4,"final":2}:
   raise SystemExit("Brazilian historical fixture integrity failed for "+k)
if __name__=="__main__":main()
