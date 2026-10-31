from loteca_fivethirtyeight.identity import resolve, resolve_rows

def test_aliases_equal():
    assert resolve("S. PAULO/SP").club_id == resolve("SAO PAULO/SP").club_id
    assert resolve("VASCO/RJ").club_id == resolve("VASCO DA GAMA/RJ").club_id

def test_state_is_identity():
    ids = {resolve(x).club_id for x in ("BOTAFOGO/RJ", "BOTAFOGO/SP", "BOTAFOGO/PB")}
    assert len(ids) == 3

def test_reserve_is_separate():
    assert resolve("PALMEIRAS B/SP").club_id != resolve("PALMEIRAS/SP").club_id
    assert resolve("PALMEIRAS-B/SP").squad == "B"
    assert resolve("SAO PAULO B/SP").squad == "B"

def test_juniors_are_not_always_base():
    assert resolve("BOCA JUNIOR/SE").squad == "principal"

def test_sub20():
    a = resolve("FLUMINENSE/RJ/Sub 20")
    b = resolve("CRUZEIRO/MG - SUB 20")
    assert a.squad == "SUB20"
    assert b.squad == "SUB20"

def test_unknown_is_not_auto_assigned():
    assert resolve("CLUBE SEM CADASTRO/RS").club_id == ""
    assert resolve("CLUBE SEM CADASTRO/RS").status == "revisar_identidade"

def test_identity_block():
    d = resolve_rows([{"concurso":"393","jogo":"1", "equipe_1":"FLUMINENSE/RJ/Sub 20", "equipe_2":"CRUZEIRO/MG - SUB 20"}])
    assert d[0]["bloqueio_categoria"] == "sim"
