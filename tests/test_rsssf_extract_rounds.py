from audits.rsssf.extract_rounds import extract
def test_brazil():
 text="[Oct 5]\nFlamengo       2-3  São Paulo\nBotafogo       1-1  São Caetano\n"
 x=extract(text,2002,False,"Serie A","https://www.rsssfbrasil.com/tablesae/br2002.htm")
 assert len(x)==2 and x[0][:5]==("2002-10-05","Flamengo","São Paulo","2","3")
def test_season_split():
 x=extract("[Jan 19]\nVasco da Gama  1-0  América",2002,True,"Rio","url")
 assert len(x)==1 and x[0][0]=="2003-01-19"
