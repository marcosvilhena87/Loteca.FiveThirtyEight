"""Extrator RSSSF para tabelas por rodada. Requer HTML arquivado da fonte."""
import csv,re,argparse,html
from datetime import date
from html.parser import HTMLParser
class Plain(HTMLParser):
 def __init__(self): super().__init__();self.a=[]
 def handle_data(self,s): self.a.append(s)
 def handle_starttag(self,t,attrs):
  if t in ("br","p","pre","div","tr","h1","h2"):self.a.append("\n")
 def text(self):return html.unescape("".join(self.a))
months={n:i for i,n in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(),1)}
dr=re.compile(r"^\s*\[?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2})\]?\s*$",re.I)
mr=re.compile(r"^\s*(.+?)\s{2,}(\d{1,2})\s*[-:]\s*(\d{1,2})\s{2,}(.+?)\s*$")
def extract(s,base_year,season_split,competition,url):
 current=None;result=[];seen=set()
 for line in s.splitlines():
  d=dr.match(line)
  if d:
   month=months[d[1].title()];year=base_year+(1 if season_split and month<7 else 0)
   try:current=date(year,month,int(d[2])).isoformat()
   except ValueError:current=None
   continue
  m=mr.match(line)
  if current and m:
   home,hg,ag,away=m.groups()
   if len(home)>55 or len(away)>55 or home.strip().startswith("["):continue
   row=(current,home.strip(),away.strip(),hg,ag,competition,url)
   if row not in seen:result.append(row);seen.add(row)
 return result
def main():
 p=argparse.ArgumentParser()
 for n in ("html","competition","source-url","out"):p.add_argument("--"+n,required=True)
 p.add_argument("--year",type=int,required=True);p.add_argument("--season-split",action="store_true")
 a=p.parse_args();parser=Plain();parser.feed(open(a.html,encoding="utf-8",errors="replace").read())
 rows=extract(parser.text(),a.year,a.season_split,a.competition,a.source_url)
 with open(a.out,"w",newline="",encoding="utf-8-sig") as f:
  w=csv.writer(f,delimiter=";");w.writerow(["date","home","away","home_goals","away_goals","competition","source_url"]);w.writerows(rows)
 print("extracted",len(rows))
if __name__=="__main__":main()
