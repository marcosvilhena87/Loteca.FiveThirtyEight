from loteca_fivethirtyeight.official_fixtures import cross_check, write_queue

def sample():
    return {"concurso":"1", "jogo":"1", "equipe_1":"FLAMENGO/RJ", "equipe_2":"S. PAULO/SP",
            "data_jogo":"domingo, 17/02/2002", "gols_1":"2", "gols_2":"4", "sorteio":"Não"}

def fixture(**kwargs):
    d = {"temporada":"2002", "data_iso":"2002-02-17", "mandante_id":"flamengo_rj:principal",
         "visitante_id":"sao_paulo_sp:principal", "gols_mandante":"2",
         "gols_visitante":"4", "competicao":"Torneio Rio-São Paulo",
         "categoria":"principal masculino", "fonte_tabela_url":"https://example.org/fixture",
         "fonte_sumula_url":""}
    d.update(kwargs)
    return d

def test_no_official_records_stays_pending():
    r = cross_check([sample()], [])[0]
    assert r["status_tabela"] == "sem_correspondencia"
    assert r["elegivel_elo"] == "nao"

def test_official_fixture_without_sumula_goes_to_queue(tmp_path):
    r = cross_check([sample()], [fixture()])[0]
    assert r["status_tabela"] == "confronto_identificado"
    assert r["status_sumula"] == "sumula_nao_localizada"
    assert r["elegivel_elo"] == "nao"
    write_queue([r], tmp_path)
    assert "1;1;" in (tmp_path / "fila_sumulas_ausentes.csv").read_text(encoding="utf-8-sig")

def test_conflicting_score_blocked():
    r = cross_check([sample()], [fixture(gols_mandante="1")])[0]
    assert r["status_tabela"] == "placar_divergente"

def test_duplicate_official_entries_ambiguous():
    r = cross_check([sample()], [fixture(), fixture()])[0]
    assert r["status_tabela"] == "ambiguo"

def test_date_missing_pending():
    a = sample()
    a["data_jogo"] = ""
    assert cross_check([a], []) [0]["status_sumula"] == "pendente"
