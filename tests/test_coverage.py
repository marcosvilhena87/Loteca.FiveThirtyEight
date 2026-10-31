import csv
import pytest
from loteca_fivethirtyeight.coverage import reviews_from

def test_review_requires_evidence(tmp_path):
    p = tmp_path / "reviews.csv"
    p.write_text("concurso;jogo;estado;competicao;categoria;fonte_oficial;status_placar;revisor;justificativa\n1;1;confirmado;;;;;;\n", encoding="utf-8")
    with pytest.raises(ValueError, match="não fundamentada"):
        reviews_from(p)

def test_review_duplicate(tmp_path):
    p = tmp_path / "reviews.csv"
    header = "concurso;jogo;estado;competicao;categoria;fonte_oficial;status_placar;revisor;justificativa\n"
    row = "1;1;pendente;;;;;;\n"
    p.write_text(header+row+row, encoding="utf-8")
    with pytest.raises(ValueError, match="duplicada"):
        reviews_from(p)
