from loteca_fivethirtyeight.international_rsssf import parse_europe,parse_fifa
def test_premier_league_and_no_cup_leak():
    text="Premier League\nRound 38\n[May 25]\nLiverpool               1-1 Crystal Palace\nFA Cup\n[May 25]\nChelsea                 0-1 Everton"
    rows=list(parse_europe(text,"Premier League",2025,"https://rsssf.org/tablese/eng2025.html"))
    assert len(rows)==1 and rows[0]["date"]=="2025-05-25"
def test_spanish_classico():
    text="Primera División\nRound 35\n[May 11]\nBarcelona                4-3 Madrid"
    rows=list(parse_europe(text,"La Liga",2025,"https://rsssf.org/tabless/span2025.html"))
    assert len(rows)==1 and rows[0]["goals_home"]==4
def test_fifa_date():
    text="20- 6-25 Philadelphia    Flamengo          3-1 Chelsea"
    rows=list(parse_fifa(text,2025,"https://rsssf.org/tablesf/fifa-wcc2025.html"))
    assert len(rows)==1 and rows[0]["date"]=="2025-06-20"

def test_single_space_after_long_team_name():
    text="Premier League\nRound 2\n[Aug 25]\nWolverhampton 2-6 Chelsea"
    rows=list(parse_europe(text,"Premier League",2025,"https://rsssf.org/tablese/eng2025.html"))
    assert len(rows)==1
    assert rows[0]["home"]=="Wolverhampton"
    assert rows[0]["goals_home"]==2
