from loteca_fivethirtyeight.club_identity import Club,resolve,same_club
R=[Club("BRA-RJ-BOTAFOGO","BRA","RJ","BOTAFOGO",1900,2100),Club("BRA-SP-BOTAFOGO","BRA","SP","BOTAFOGO",1900,2100),Club("BRA-SP-SAO-PAULO","BRA","SP","S PAULO",1900,2100),Club("BRA-SP-SAO-PAULO","BRA","SP","SAO PAULO",1900,2100)]
def test_region(): assert resolve("BOTAFOGO/SP",2020,R)=="BRA-SP-BOTAFOGO"
def test_ambiguous(): assert resolve("BOTAFOGO",2020,R) is None
def test_alias(): assert same_club("S. PAULO/SP","SAO PAULO/SP",2020,R)
def test_not_cross_region(): assert not same_club("BOTAFOGO/SP","BOTAFOGO/RJ",2020,R)
def test_validity():
    entries=[Club("X","BRA","SP","EXEMPLO",2002,2010)]
    assert resolve("EXEMPLO/SP",2011,entries) is None

def test_matcher_uses_canonical_ids():
    from loteca_fivethirtyeight.rsssf_match import match_games
    game={"concurso":"1","jogo":"1","equipe_1":"S. PAULO/SP","equipe_2":"BOTAFOGO/SP","gols_1":"2","gols_2":"0","data_jogo":"17/02/2002"}
    ref={"home":"SAO PAULO/SP","away":"BOTAFOGO/SP","goals_home":2,"goals_away":0,"date":"2002-02-17","year":2002,"competition":"TEST","url":"https://rsssfbrasil.com/test","category":"PRINCIPAL"}
    result=next(match_games([game],[ref],registry=R))
    assert result["status_rsssf"]=="CONFIRMADO_PRINCIPAL"
    assert result["home_club_id"]=="BRA-SP-SAO-PAULO"

def test_matcher_quarantines_ambiguous_name():
    from loteca_fivethirtyeight.rsssf_match import match_games
    game={"equipe_1":"BOTAFOGO","equipe_2":"S. PAULO/SP","gols_1":"1","gols_2":"1","data_jogo":"17/02/2002"}
    result=next(match_games([game],[],registry=R))
    assert result["status_rsssf"]=="ALIAS_NAO_RESOLVIDO"
