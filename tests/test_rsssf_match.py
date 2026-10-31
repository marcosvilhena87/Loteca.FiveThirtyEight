from loteca_fivethirtyeight.rsssf_match import match_all

def game(**kwargs):
    x=dict(concurso="1",jogo="1",data_jogo="domingo, 17/02/2002",
           equipe_1="SANTOS/SP",equipe_2="SAO  CAETANO/SP",
           gols_1="2",gols_2="1",sorteio="Não")
    x.update(kwargs);return x

def source(**kwargs):
    x=dict(date="2002-02-17",home="Santos",away="São Caetano",
           home_goals="2",away_goals="1",competition="Rio-São Paulo 2002",
           source_url="https://www.rsssf.org/tablesr/riospl02.html")
    x.update(kwargs);return x

def test_exact_match_and_no_elo():
    x=match_all([game()],[source()])[0]
    assert x["estado"]=="confirmado"
    assert x["elo_liberado"]=="nao"

def test_strict_fields_and_unknown_alias():
    for change in [dict(date="2002-02-18"),dict(home="Flamengo"),
                   dict(home_goals="3"),dict(competition="")]:
        assert match_all([game()],[source(**change)])[0]["estado"]=="pendente"
    assert match_all([game(equipe_1="BOTAFOGO/SP")],[source()])[0]["estado"]=="pendente"

def test_lottery_draw_blocks_approval():
    assert match_all([game(sorteio="SIM")],[source()])[0]["estado"]=="pendente"

def test_conflict_and_duplicate():
    a,b=source(),source(competition="Outro torneio")
    assert "multiplas" in match_all([game()],[a,b])[0]["motivo"]
    assert all(x["estado"]=="pendente" for x in match_all([game(),game()],[a]))

def test_no_swap_of_home_away():
    assert match_all([game()],[source(home="São Caetano",away="Santos")])[0]["estado"]=="pendente"

def test_categorias_excecao():
    assert match_all([game(equipe_1="CLUBE NAO MAPEADO")],[source()])[0]["categoria_excecao"] == "alias_ausente"
    assert match_all([game()],[source(home="Palmeiras")])[0]["categoria_excecao"] == "fora_escopo"
    assert match_all([game()],[source(home_goals="3")])[0]["categoria_excecao"] == "divergencia_placar"
    assert match_all([game()],[source(date="2002-02-18")])[0]["categoria_excecao"] == "divergencia_data"
    assert match_all([game()],[source(),source(competition="Outro torneio")])[0]["categoria_excecao"] == "conflito_fontes"
    assert match_all([game()],[source(),source(source_url="https://rsssf.org/alternativa")])[0]["estado"] == "confirmado"

def test_sem_inventar_divergencia_por_encontros_distintos():
    rec = match_all([game()],[source(date="2002-02-19",home_goals="9")])[0]
    assert rec["categoria_excecao"] == "revisao_humana"
