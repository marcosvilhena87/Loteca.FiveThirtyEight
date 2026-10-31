"""Testes unitários sem acesso à internet."""
from dataclasses import replace

import pytest

from loteca_fivethirtyeight import importer as imp

HEADER = ";".join(imp.COLUMNS)
LINE = "1;segunda-feira, 18/02/2002;1;2;FLAMENGO/RJ;S. PAULO/SP;4;domingo, 17/02/2002;2;caixa;Não"


def test_dates_and_teams():
    assert imp.parse_brazilian_date("segunda-feira, 18/02/2002") == "2002-02-18"
    assert imp.normalize_team("  São   Paulo/SP ") == "SAO PAULO/SP"
    assert imp.normalize_team("S. PAULO/SP") == "S PAULO/SP"


def test_row_and_outcome():
    match = imp.load_csv(HEADER + "\n" + LINE + "\n", "fixture.csv")[0]
    assert match.resultado_placar == "2"
    assert match.data_jogo == "2002-02-17"
    assert not match.sorteio_indicado
    assert match.equipe_1_id == "FLAMENGO/RJ"


def test_mismatched_score():
    invalid = LINE.replace(";4;domingo", ";1;domingo")
    with pytest.raises(imp.ImportValidationError, match="diverge"):
        imp.load_csv(HEADER + "\n" + invalid, "fixture.csv")


@pytest.mark.parametrize("edit", [
    lambda line: line.replace("18/02/2002", "31/02/2002"),
    lambda line: line.replace(";1;2;FLAMENGO", ";15;2;FLAMENGO"),
    lambda line: line.replace(";2;caixa;Não", ";3;caixa;Não"),
    lambda line: line.replace("17/02/2002", "19/02/2002"),
])
def test_invalid_values(edit):
    with pytest.raises(imp.ImportValidationError):
        imp.load_csv(HEADER + "\n" + edit(LINE))


def test_bad_header():
    with pytest.raises(imp.ImportValidationError, match="cabeçalho"):
        imp.load_csv("outro;cabecalho\n1;2")


def test_identical_duplicates_and_report(tmp_path, monkeypatch):
    monkeypatch.setattr(imp, "FILENAMES", ("a.csv", "b.csv"))
    for name in imp.FILENAMES:
        (tmp_path / name).write_text(HEADER + "\n" + LINE + "\n", encoding="utf-8")
    matches, report = imp.import_all(tmp_path)
    assert len(matches) == 1
    assert report["duplicatas_identicas_removidas"] == 1
    assert report["concursos_com_menos_de_14_jogos"] == [1]
    out = tmp_path / "output.csv"
    imp.write_csv(matches, out)
    assert "FLAMENGO/RJ" in out.read_text(encoding="utf-8")


def test_conflicting_duplicate(tmp_path, monkeypatch):
    monkeypatch.setattr(imp, "FILENAMES", ("a.csv", "b.csv"))
    (tmp_path / "a.csv").write_text(HEADER + "\n" + LINE, encoding="utf-8")
    (tmp_path / "b.csv").write_text(HEADER + "\n" + LINE.replace("FLAMENGO/RJ", "VASCO/RJ"), encoding="utf-8")
    with pytest.raises(imp.ImportValidationError, match="duplicata conflitante"):
        imp.import_all(tmp_path)


def test_special_flag():
    match = imp.load_csv(HEADER + "\n" + LINE.replace(";Não", ";Sim"))[0]
    assert match.sorteio_indicado


def test_missing_source(tmp_path, monkeypatch):
    monkeypatch.setattr(imp, "FILENAMES", ("ausente.csv",))
    with pytest.raises(FileNotFoundError):
        imp.import_all(tmp_path)
