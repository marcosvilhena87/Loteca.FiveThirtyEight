"""Cross-check Loteca records against season-scoped official fixture exports.

Official fixtures must be supplied as CSV from federation/conference records with
provenance URL; no invented fixtures, no implicit category approval.
"""
import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from .external_audit import fetch_csvs, read_records, parse_date
from .identity import resolve, write_alias_report, resolve_rows

FIXTURE_FIELDS = ("temporada", "data_iso", "mandante_id", "visitante_id",
                  "gols_mandante", "gols_visitante", "competicao", "categoria",
                  "fonte_tabela_url", "fonte_sumula_url")
OUT_FIELDS = ("concurso", "jogo", "data_iso", "mandante", "visitante",
              "competicao", "categoria", "status_tabela", "status_sumula",
              "fonte_tabela_url", "fonte_sumula_url", "motivo", "elegivel_elo")

def read_official(folder: Path) -> list[dict]:
    result = []
    for path in sorted(folder.glob("*.csv")):
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, delimiter=";")
            if not set(FIXTURE_FIELDS).issubset(reader.fieldnames or []):
                raise ValueError(f"Schema inválido: {path}")
            for row in reader:
                if not row["fonte_tabela_url"].startswith("https://"):
                    raise ValueError(f"Proveniência oficial ausente: {path}")
                if row["fonte_sumula_url"] and not row["fonte_sumula_url"].startswith("https://"):
                    raise ValueError(f"URL súmula inválida: {path}")
                datetime.fromisoformat(row["data_iso"])
                result.append(row)
    return result

def cross_check(records: list[dict], fixtures: list[dict]) -> list[dict]:
    idx = defaultdict(list)
    for f in fixtures:
        idx[(f["temporada"], f["data_iso"], f["mandante_id"], f["visitante_id"])].append(f)
    output = []
    for r in records:
        result = {x: "" for x in OUT_FIELDS}
        result.update(concurso=r["concurso"], jogo=r["jogo"], mandante=r["equipe_1"],
                      visitante=r["equipe_2"], elegivel_elo="nao")
        try:
            date = parse_date(r["data_jogo"])
        except ValueError:
            result.update(status_tabela="sem_data", status_sumula="pendente",
                          motivo="ausência de data de jogo / possível sorteio")
            output.append(result)
            continue
        result["data_iso"] = date
        a, b = resolve(r["equipe_1"]), resolve(r["equipe_2"])
        if not a.club_id or not b.club_id:
            result.update(status_tabela="alias_pendente", status_sumula="pendente",
                          motivo="um ou dois IDs canônicos ainda não validados")
            output.append(result)
            continue
        matches = idx.get((date[:4], date, a.club_id, b.club_id), [])
        if len(matches) != 1:
            result.update(status_tabela="sem_correspondencia" if not matches else "ambiguo",
                          status_sumula="pendente",
                          motivo="nenhuma ou múltiplas tabelas oficiais coincidentes")
            output.append(result)
            continue
        f = matches[0]
        result.update(competicao=f["competicao"], categoria=f["categoria"],
                      fonte_tabela_url=f["fonte_tabela_url"],
                      fonte_sumula_url=f["fonte_sumula_url"],
                      status_tabela="confronto_identificado",
                      status_sumula="url_informada_nao_verificada" if f["fonte_sumula_url"] else "sumula_nao_localizada")
        if f["gols_mandante"] != r["gols_1"] or f["gols_visitante"] != r["gols_2"]:
            result.update(status_tabela="placar_divergente",
                          motivo="resultado lotérico difere da tabela da competição")
        elif r.get("sorteio", "").strip().upper() == "SIM":
            result["motivo"] = "resultado lotérico por sorteio"
        elif a.squad != "principal" or b.squad != "principal" or f["categoria"].strip().lower() not in ("principal masculino",):
            result["motivo"] = "categoria diferente ou não comprovada"
        else:
            result["motivo"] = "tabela encontrada; conferir autenticidade da fonte e súmula"
        # A URL da súmula sozinha não atesta seu conteúdo; aprovação manual necessária.
        output.append(result)
    return output

def write_queue(rows: list[dict], folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    partitions = {
        "conferencia_tabelas.csv": rows,
        "fila_sumulas_ausentes.csv": [r for r in rows if r["status_sumula"] in ("pendente", "sumula_nao_localizada")],
        "fila_sumulas_nao_verificadas.csv": [r for r in rows if r["status_sumula"] == "url_informada_nao_verificada"],
        "fila_divergencias.csv": [r for r in rows if r["status_tabela"] in ("placar_divergente", "ambiguo", "alias_pendente", "sem_data")]
    }
    for name, items in partitions.items():
        with (folder / name).open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=OUT_FIELDS, delimiter=";")
            writer.writeheader()
            writer.writerows(items)
    counts = Counter(r["status_tabela"] for r in rows)
    (folder / "resumo_tabelas.json").write_text(json.dumps({
        "registros": len(rows), "status_tabela": dict(counts),
        "sumulas_ausentes": len(partitions["fila_sumulas_ausentes.csv"]),
        "sumulas_urls_nao_verificadas": len(partitions["fila_sumulas_nao_verificadas.csv"]),
        "elegiveis_elo": 0, "politica": "nenhuma URL ou tabela isolada libera o Elo"
    }, ensure_ascii=False, indent=2), encoding="utf-8")

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--fixtures", type=Path, default=Path("data/official_fixtures"))
    p.add_argument("--cache", type=Path, default=Path("data/raw/loteca"))
    p.add_argument("--offline", action="store_true")
    p.add_argument("--output", type=Path, default=Path("reports/conferencia_oficial"))
    args = p.parse_args()
    rows = read_records(fetch_csvs(args.cache, remote=not args.offline))
    fixtures = read_official(args.fixtures) if args.fixtures.exists() else []
    write_queue(cross_check(rows, fixtures), args.output)
    write_alias_report(resolve_rows(rows), args.output / "aliases_por_partida.csv")
    print(f"Auditados {len(rows)} registros, usando {len(fixtures)} partidas de tabelas oficiais cadastradas.")

if __name__ == "__main__":
    main()
