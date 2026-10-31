from loteca_fivethirtyeight.external_audit import classify, evidence_match, parse_date, write_reports

def row(**kwargs):
    d = dict(concurso="1201", jogo="3", data_jogo="sábado, 05/07/2025", equipe_1="ITUANO/SP", equipe_2="RETRO BRASIL/PE", gols_1="2", gols_2="0", resultado_placar="1", sorteio="Não", _file="Loteca_1201-1300.csv")
    d.update(kwargs)
    return d

def test_date():
    assert parse_date("domingo, 17/02/2002") == "2002-02-17"

def test_without_evidence_blocked():
    r = classify(row())
    assert r["classificacao"] == "pendente"
    assert r["elegivel_elo"] == "nao"

def test_sorteio_critical():
    r = classify(row(sorteio="Sim"))
    assert r["risco"] == "critico"
    assert r["elegivel_elo"] == "nao"

def test_bad_search_does_not_approve():
    item = {"title": "Ituano 2-0 Retro Serie C", "snippet": "", "link": "https://example.com"}
    assert not evidence_match(row(), item, "2025-07-05")
    assert classify(row(), [item])["classificacao"] == "pendente"

def test_search_never_automatically_approves_main_team():
    item = {"title": "Ituano 2-0 Retro Série C 05/07/2025", "snippet": "", "link": "https://example.com"}
    r = classify(row(), [item])
    assert r["elegivel_elo"] == "nao"
    assert r["classificacao"] == "revisao_externa"

def test_reports(tmp_path):
    write_reports([classify(row())], tmp_path)
    assert (tmp_path / "excecoes.csv").exists()
    assert (tmp_path / "resumo.json").exists()
