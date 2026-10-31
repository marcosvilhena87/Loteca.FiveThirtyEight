from dataclasses import replace

from loteca_fivethirtyeight.audit import audit_matches, canonical_team
from loteca_fivethirtyeight.importer import load_csv, COLUMNS


def fixture(concurso=1, jogo=1, equipe="SAO  CAETANO/SP", sorteio="Não"):
    row = [str(concurso), "segunda-feira, 18/02/2002", str(jogo), "2",
           equipe, "FLAMENGO/RJ", "1", "domingo, 17/02/2002", "1", "caixa", sorteio]
    return load_csv(";".join(COLUMNS) + "\n" + ";".join(row) + "\n")[0]


def test_format_aliases_without_merging_unrelated_teams():
    assert canonical_team("SAO  CAETANO/SP") == canonical_team("SAO CAETANO/SP")
    assert canonical_team("S. PAULO/SP") != canonical_team("SAO PAULO/SP")
    assert canonical_team("PALMEIRAS B/SP") != canonical_team("PALMEIRAS/SP")


def test_contest_coverage_duplicates_and_special_flags():
    a = fixture()
    b = fixture(concurso=3, jogo=2, equipe="SAO CAETANO/SP", sorteio="SIM")
    report = audit_matches([a, a, b])
    assert report["duplicatas_chave"] == 1
    assert report["concursos_faltantes_no_intervalo"] == [2]
    assert report["concursos_incompletos"]["1"] == list(range(2, 15))
    assert report["nao_adequados_para_elo_por_sorteio"] == 1
    assert len(report["grupos_grafias_equivalentes"]) == 1
    assert report["pronto_para_treinar_elo"] is False
