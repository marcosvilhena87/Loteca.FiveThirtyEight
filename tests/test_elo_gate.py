import csv
from loteca_fivethirtyeight.elo_gate import assess, export_approved
import pytest

def valid_row():
    return dict(concurso="1202", jogo="1", mandante="FLAMENGO/RJ",
        visitante="SAO PAULO/SP", data_jogo="2025-07-12",
        competicao="Campeonato Brasileiro Série A 2025",
        categoria="oficial_profissional", fonte_oficial="https://www.cbf.com.br/jogo",
        tipo_evidencia_oficial="pagina_oficial_partida",
        status_placar="oficial_confirmado", decisao_elo="liberar",
        observacoes="mandante 2-0 visitante, confrontado com CBF")
def test_fail_closed():
    row=valid_row()
    assert assess(row)[0]
    for k in ("categoria","decisao_elo","fonte_oficial","tipo_evidencia_oficial",
              "status_placar","competicao","data_jogo","mandante","observacoes"):
        broken=row.copy(); broken[k]=""
        assert not assess(broken)[0], k
def test_export_and_duplicate(tmp_path):
    path=tmp_path/"e.csv"; dest=tmp_path/"out.csv"; row=valid_row()
    with path.open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(row),delimiter=";")
        writer.writeheader();writer.writerow(row)
    assert export_approved(path,dest)==1
    with path.open("a",newline="") as f:
        csv.DictWriter(f,fieldnames=list(row),delimiter=";").writerow(row)
    with pytest.raises(ValueError,match="duplicada"):
        export_approved(path,dest)
