from loteca_fivethirtyeight.club_identity import Club,resolve,same_club
R=[Club("BRA-RJ-BOTAFOGO","BRA","RJ","BOTAFOGO",1900,2100),Club("BRA-SP-BOTAFOGO","BRA","SP","BOTAFOGO",1900,2100),Club("BRA-SP-SAO-PAULO","BRA","SP","S PAULO",1900,2100),Club("BRA-SP-SAO-PAULO","BRA","SP","SAO PAULO",1900,2100)]
def test_region(): assert resolve("BOTAFOGO/SP",2020,R)=="BRA-SP-BOTAFOGO"
def test_ambiguous(): assert resolve("BOTAFOGO",2020,R) is None
def test_alias(): assert same_club("S. PAULO/SP","SAO PAULO/SP",2020,R)
def test_not_cross_region(): assert not same_club("BOTAFOGO/SP","BOTAFOGO/RJ",2020,R)
def test_validity():
    entries=[Club("X","BRA","SP","EXEMPLO",2002,2010)]
    assert resolve("EXEMPLO/SP",2011,entries) is None
