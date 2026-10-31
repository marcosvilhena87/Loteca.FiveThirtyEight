import json
from audits.rsssf.ingest_sources import parse_page,ingest
def test_dates_and_split():
 s="<pre>[Dec 7]\nMilan      1-0  Roma\n[Jan 11]\nBologna    0-2  Milan</pre>"
 rows,kind,w=parse_page(s,2002,True,"Italy","https://www.rsssf.org/tablesi/ital03.html")
 assert [r["date"] for r in rows]==["2002-12-07","2003-01-11"]
 assert kind=="dated_round_lines"
def test_duplicates_are_not_added():
 rows,kind,w=parse_page("<pre>[Oct 5]\nFlamengo  2-3  São Paulo\nFlamengo  2-3  São Paulo</pre>",2002,False,"BR","url")
 assert len(rows)==1 and any(x["reason"]=="duplicate_row" for x in w)
def test_integrity_offline(tmp_path):
 folder=tmp_path/"local";folder.mkdir()
 (folder/"source.html").write_text("<pre>[Oct 5]\nFlamengo  2-3  São Paulo</pre>",encoding="utf-8")
 spec={"id":"local","url":"https://www.rsssfbrasil.com/tablesae/br2002.htm","year":2002,"competition":"BR","expected_matches":2}
 x=ingest(spec,tmp_path,offline=True)
 assert x["integrity"]=="review" and "expected_count_mismatch" in x["issues"]
 assert x["sha256"] and (folder/"matches.csv").exists()
def test_unsupported():
 rows,kind,w=parse_page("<p>classification only</p>",2002,False,"BR","url")
 assert not rows and kind=="unsupported"
