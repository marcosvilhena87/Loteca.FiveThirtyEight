from loteca_fivethirtyeight.rsssf_match import normalize,parse_date,parse_rsssf_text,match_games

def sample():
    return {"concurso":"1","jogo":"1","equipe_1":"FLAMENGO/RJ","equipe_2":"S. PAULO/SP","gols_1":"2","gols_2":"4","data_jogo":"domingo, 17/02/2002"}

def reference(date="2002-02-17", category="PRINCIPAL"):
    return {"home":"Flamengo","away":"São Paulo","goals_home":"2","goals_away":"4","date":date,"year":"2002","competition":"Rio-Sao Paulo","url":"https://www.rsssfbrasil.com/tablesr/rjsp2002.htm","category":category}

def test_alias(): assert normalize("S. PAULO/SP")==normalize("São Paulo")
def test_date(): assert parse_date("domingo, 17/02/2002").isoformat()=="2002-02-17"
def test_match(): assert next(match_games([sample()],[reference()]))["status_rsssf"]=="CONFIRMADO_PRINCIPAL"
def test_out_of_window(): assert next(match_games([sample()],[reference("2002-03-17")]))["status_rsssf"]=="PENDENTE_RSSSF"
def test_category(): assert next(match_games([sample()],[reference(category="SUB20")]))["status_rsssf"]=="OUTRA_CATEGORIA"
def test_ambiguity(): assert next(match_games([sample()],[reference(),reference("2002-02-18")]))["status_rsssf"]=="AMBIGUO"
def test_missing_date(): 
    game=sample();game["data_jogo"]=""
    assert next(match_games([game],[reference()]))["status_rsssf"]=="REVISAO_DATA"
def test_parser():
    src="Round 6\n[Feb 17]\nFlamengo       2-4  São Paulo\n"
    data=list(parse_rsssf_text(src,competition="Rio-Sao Paulo",url="https://rsssfbrasil.com",year=2002))
    assert len(data)==1 and data[0]["date"]=="2002-02-17"
