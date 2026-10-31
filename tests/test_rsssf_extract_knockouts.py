from audits.rsssf.extract_knockouts import extract_knockouts
def test_reverses_second_leg():
 s="<pre>Quarterfinals\n[Nov 24 and 27]\nFluminense     3-0   0-2  São Caetano\n</pre>"
 x,w=extract_knockouts(s,"A","url")
 assert [(a["date"],a["home"],a["away"],a["home_goals"],a["away_goals"],a["leg"]) for a in x]==[
 ("2002-11-24","Fluminense","São Caetano","3","0","ida"),
 ("2002-11-27","São Caetano","Fluminense","2","0","volta")]
def test_dates_cross_month_and_finals():
 s="<pre>Finals\n[Nov 30 and Dec 7]\nFortaleza       2-0   1-4  Criciúma\n</pre>"
 x,_=extract_knockouts(s,"B","url")
 assert len(x)==2 and x[1]["date"]=="2002-12-07" and (x[1]["home"],x[1]["home_goals"],x[1]["away_goals"])==("Criciúma","4","1")
def test_no_date_no_inference():
 x,w=extract_knockouts("<pre>Quarterfinals\nSantos  3-1  2-1  São Paulo</pre>","A","url")
 assert not x and w
