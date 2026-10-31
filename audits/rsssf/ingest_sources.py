"""RSSSF ingestão reproduzível: fetch, snapshot, formatos, extração e QA."""
from __future__ import annotations
import argparse,csv,hashlib,json,re,time,urllib.request,urllib.error
from collections import Counter
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
MONTHS={m:i for i,m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(),1)}
DATE=re.compile(r"^\s*\[?\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2})(?:\s*,?\s*(\d{4}))?\s*\]?\s*$",re.I)
DATE_REV=re.compile(r"^\s*\[?\s*(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(?:\s+(\d{4}))?\s*\]?\s*$",re.I)
SCORE=re.compile(r"^\s*(?P<home>.+?)\s+(?P<hg>\d{1,2})\s*[-:]\s*(?P<ag>\d{1,2})\s+(?P<away>[^;\[\]]+?)\s*$")
class Page(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.parts=[]
 def handle_data(self,data):self.parts.append(data)
 def handle_starttag(self,tag,attrs):
  if tag in ("br","p","pre","tr","div","h1","h2","h3"):self.parts.append("\n")
 def text(self):return "".join(self.parts)
def decode(raw):
 for encoding in ("utf-8","windows-1252","latin-1"):
  try:return raw.decode(encoding)
  except UnicodeDecodeError:pass
 return raw.decode("latin-1",errors="replace")
def format_kind(text):
 n=sum(bool(DATE.match(s) or DATE_REV.match(s)) for s in text.splitlines())
 scores=sum(bool(SCORE.match(s)) for s in text.splitlines())
 if n and scores:return "dated_round_lines"
 if scores:return "score_lines_without_recognized_dates"
 return "unsupported"
def parse_page(html_text,year,split,competition,url):
 p=Page();p.feed(html_text);txt=p.text()
 current=None;rows=[];warnings=[];dedup=set()
 for no,line in enumerate(txt.splitlines(),1):
  stripped=line.strip()
  d=DATE.match(stripped);rev=DATE_REV.match(stripped)
  if d or rev:
   if d:month,day,explicit=d.groups()
   else:day,month,explicit=rev.groups()
   mo=MONTHS[month.title()]
   yr=int(explicit) if explicit else int(year)+(int(bool(split and mo<7)))
   try:current=date(yr,mo,int(day))
   except ValueError:current=None;warnings.append({"line":no,"reason":"invalid_date"})
   continue
  m=SCORE.match(re.sub(r"\s+\[[^\]]+\]\s*$","",line))
  if not m:continue
  if current is None:
   warnings.append({"line":no,"reason":"score_without_date"})
   continue
  home=m["home"].strip();away=m["away"].strip()
  # Avoid score summaries (league standings, totals) and malformed lines.
  if not(2<=len(home)<=65 and 2<=len(away)<=65):continue
  if home[0].isdigit() or away[0].isdigit():continue
  key=(str(current),home.casefold(),away.casefold(),m["hg"],m["ag"])
  if key in dedup:
   warnings.append({"line":no,"reason":"duplicate_row"})
   continue
  dedup.add(key)
  rows.append({"date":str(current),"home":home,"away":away,
      "home_goals":m["hg"],"away_goals":m["ag"],"competition":competition,
      "source_url":url,"source_line":no})
 return rows,format_kind(txt),warnings
def extract_league_rounds(html_text,year,competition,url,expected_rounds,per_round):
 p=Page();p.feed(html_text);text=p.text()
 first=re.search(r"(?m)^\s*Round 1\s*$",text)
 if not first:return [],"unsupported",[{"reason":"missing_first_round"}],{}
 text=text[first.start():]
 text=re.sub(r"(?m)^(\s*Round \d+)\s+(\[[A-Za-z]{3} \d+\])\s*$",r"\1\n\2",text)
 blocks=re.split(r"(?m)^\s*Round (\d+)\s*$",text)
 rows=[];warnings=[];counts={};seen=set()
 for i in range(1,len(blocks)-1,2):
  n=int(blocks[i])
  if not 1<=n<=expected_rounds:break
  if n in counts:
   warnings.append({"reason":"repeated_round","round":n});break
  section=blocks[i+1]
  if n==expected_rounds:
   section=section.split("Final Table:",1)[0]
   section=re.split(r"(?im)^\s*(?:Final Table:|Second Level|Second Division|Segunda|Coppa Italia|Copa del Rey|Cup Competition|Promotion|Relegation Playoff)\b",section)[0]
  extracted,_,problems=parse_page(section,year,True,competition,url)
  if expected_rounds==34 and n==12 and re.search(r"(?im)^\s*Como\s+awd\s+Udinese\b",section):
   extracted.append({"date":"2002-12-18","home":"Como","away":"Udinese","home_goals":"0","away_goals":"2","competition":competition,"source_url":url,"source_line":0,"result_type":"administrative_award"})
  counts[n]=len(extracted)
  warnings.extend({**w,"round":n} for w in problems)
  for x in extracted:
   x["round"]=n
   key=(x["date"],x["home"].casefold(),x["away"].casefold())
   if key in seen:warnings.append({"reason":"duplicate_fixture","round":n})
   else:seen.add(key);rows.append(x)
  if n==expected_rounds:break
 if len(counts)!=expected_rounds:warnings.append({"reason":"missing_rounds","found":len(counts),"expected":expected_rounds})
 for n in range(1,expected_rounds+1):
  if counts.get(n)!=per_round:warnings.append({"reason":"round_count_mismatch","round":n,"actual":counts.get(n,0),"expected":per_round})
 return rows,"league_rounds",warnings,counts

def fetch(url,timeout=25):
 p=urlparse(url)
 if p.scheme!="https" or p.hostname not in ("www.rsssf.org","rsssf.org","www.rsssfbrasil.com","rsssfbrasil.com","mail.rsssfbrasil.com"):
  raise ValueError("URL não autorizada")
 req=urllib.request.Request(url,headers={"User-Agent":"Loteca-Historical-Audit/0.1 (research archive)","Accept":"text/html"})
 with urllib.request.urlopen(req,timeout=timeout) as resp:
  payload=resp.read(8_000_001)
  if len(payload)>8_000_000:raise ValueError("HTML maior que 8 MB")
  return payload
def ingest(spec,archive,offline=False):
 name=spec["id"];folder=Path(archive)/name;folder.mkdir(parents=True,exist_ok=True)
 path=folder/"source.html";status="reused_archive"
 if not offline:
  try:
   raw=fetch(spec["url"]);path.write_bytes(raw);status="downloaded"
  except (OSError,ValueError,urllib.error.URLError) as e:
   if not path.exists():return {"id":name,"status":"download_error","error":str(e),"url":spec["url"],"rows":0}
   status="fallback_archive"
 if not path.exists():return {"id":name,"status":"missing_archive","rows":0,"url":spec["url"]}
 raw=path.read_bytes();sha=hashlib.sha256(raw).hexdigest()
 if spec.get("rounds"):
  rows,kind,warnings,round_counts=extract_league_rounds(decode(raw),spec["year"],spec["competition"],spec["url"],spec["rounds"],spec["matches_per_round"])
 else:
  raw_text=decode(raw)
  if spec["id"] in ("br2002_a","br2002_b"):
   raw_text=raw_text.split("Quarterfinals",1)[0]
  rows,kind,warnings=parse_page(raw_text,spec["year"],spec.get("season_split",False),spec["competition"],spec["url"])
  round_counts={}
 if spec["id"] in ("br2002_a","br2002_b"):
  from audits.rsssf.extract_knockouts import extract_knockouts
  knockout,kw=extract_knockouts(decode(raw),spec["competition"],spec["url"],spec["year"])
  rows.extend(knockout)
  warnings.extend(kw)
 expected=spec.get("expected_matches")
 issues=[]
 if not rows:issues.append("zero_matches")
 if expected is not None and len(rows)!=expected:issues.append("expected_count_mismatch")
 if kind not in ("dated_round_lines","league_rounds"):issues.append("format_unsupported_or_incomplete")
 if any(w.get("reason") in ("missing_rounds","round_count_mismatch","repeated_round","duplicate_fixture") for w in warnings):issues.append("round_integrity_failure")
 if len({(x["date"],x["home"],x["away"]) for x in rows})!=len(rows):issues.append("duplicate_fixture")
 dates=[x["date"] for x in rows]
 if spec.get("date_start") and any(x<spec["date_start"] for x in dates):issues.append("date_before_range")
 if spec.get("date_end") and any(x>spec["date_end"] for x in dates):issues.append("date_after_range")
 rec={"id":name,"url":spec["url"],"status":status,"sha256":sha,"bytes":len(raw),
   "format":kind,"rows":len(rows),"expected_matches":expected,"issues":issues,
   "round_counts":round_counts,"warnings":warnings[:100],"integrity":"pass" if not issues else "review"}
 (folder/"metadata.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding="utf-8")
 with (folder/"matches.csv").open("w",newline="",encoding="utf-8") as fp:
  writer=csv.DictWriter(fp,fieldnames=["date","home","away","home_goals","away_goals","competition","source_url","source_line","round","result_type","phase","leg"],delimiter=";")
  writer.writeheader();writer.writerows([{**r,"round":r.get("round",""),"result_type":r.get("result_type","played"),"phase":r.get("phase","league"),"leg":r.get("leg","")} for r in rows])
 return rec
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--manifest",required=True);ap.add_argument("--archive",default="data/rsssf_archive")
 ap.add_argument("--offline",action="store_true")
 args=ap.parse_args()
 entries=json.loads(Path(args.manifest).read_text(encoding="utf-8"))
 reports=[]
 for spec in entries:
  reports.append(ingest(spec,args.archive,args.offline))
  time.sleep(0 if args.offline else .75)
 base=Path(args.archive);base.mkdir(parents=True,exist_ok=True)
 (base/"integrity_report.json").write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({"sources":len(reports),"integrity_pass":sum(x.get("integrity")=="pass" for x in reports),
    "total_extracted":sum(x.get("rows",0) for x in reports),"failed":sum(x.get("status") in ("download_error","missing_archive") for x in reports)}))
if __name__=="__main__":main()
