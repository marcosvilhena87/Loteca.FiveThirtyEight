"""Auditoria por confronto e por participante da fonte RSSSF, sem aprovar Elo."""
import csv
from collections import Counter,defaultdict
from pathlib import Path
from .club_identity import clean

def audit_league(games, league, alias_rows):
    names=defaultdict(set)
    for r in alias_rows:
        if r["competition"]==league:
            names[clean(r["alias"])].add(r["club_id"])
    fixtures=set();teams=Counter();home=Counter();away=Counter();issues=[]
    for g in games:
        pair=[names.get(clean(g[side]),set()) for side in ("home","away")]
        if any(len(x)!=1 for x in pair):
            issues.append((g,"ALIAS_UNRESOLVED_OR_AMBIGUOUS"));continue
        a,b=[next(iter(x)) for x in pair]
        key=(a,b)
        if a==b or key in fixtures:
            issues.append((g,"DUPLICATE_OR_SELF_FIXTURE"));continue
        fixtures.add(key);home[a]+=1;away[b]+=1;teams[a]+=1;teams[b]+=1
        if not g.get("date"):issues.append((g,"MISSING_DATE"))
    members=set(home)|set(away)
    for t in sorted(members):
        if home[t]!=19 or away[t]!=19:
            issues.append(({"home":t,"away":"","date":""},f"HOME_AWAY_COUNT_{home[t]}_{away[t]}"))
    if len(fixtures)!=380 or len(members)!=20:
        issues.append(({"home":"","away":"","date":""},f"LEAGUE_COUNT_{len(fixtures)}_TEAMS_{len(members)}"))
    return {"competition":league,"raw_records":len(games),"unique_fixtures":len(fixtures),
            "teams":len(members),"issue_count":len(issues),"status":"STRUCTURE_OK_NEEDS_EXTERNAL_REVIEW" if not issues else "QUARANTINE_STRUCTURAL"},issues

def export_audit(refs,scope,out):
    stats=[];errors=[]
    for league in ("La Liga","Premier League","Serie A Italia"):
        summary,issues=audit_league([x for x in refs if x["competition"]==league],league,scope)
        stats.append(summary)
        errors += [{"competition":league,"home":g.get("home",""),"away":g.get("away",""),
                    "date":g.get("date",""),"reason":reason} for g,reason in issues]
    Path(out).mkdir(parents=True,exist_ok=True)
    for filename,records,fields in (
        ("league_integrity_summary.csv",stats,["competition","raw_records","unique_fixtures","teams","issue_count","status"]),
        ("league_integrity_issues.csv",errors,["competition","home","away","date","reason"])):
        with (Path(out)/filename).open("w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,delimiter=";",fieldnames=fields);w.writeheader();w.writerows(records)
    return stats
if __name__=="__main__":
    import sys,json
    def read(p):
        with open(p,encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f,delimiter=";"))
    print(json.dumps(export_audit(read(sys.argv[1]),read(sys.argv[2]),sys.argv[3]),ensure_ascii=False))
