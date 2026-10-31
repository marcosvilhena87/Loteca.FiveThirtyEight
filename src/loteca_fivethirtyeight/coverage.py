"""Gera cadastro de cobertura integral sem inventar validações externas.

Baixa os 13 CSVs da fonte original, preserva todos os jogos e suas origens.
Somente revisões verificadas (arquivo separado) podem determinar confirmado/rejeitado.
"""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from .external_audit import fetch_csvs, read_records, parse_date

FIELDS = ["concurso", "jogo", "data_jogo", "mandante", "visitante",
          "placar_csv", "sorteio", "estado", "competicao", "categoria",
          "fonte_oficial", "status_placar", "decisao_elo", "motivo", "arquivo_origem"]
REQUIRED_REVIEW = {"concurso", "jogo", "estado", "competicao", "categoria",
                   "fonte_oficial", "status_placar", "revisor", "justificativa"}
STATUSES = {"confirmado", "rejeitado", "pendente"}

def reviews_from(path):
    if not path:
        return {}
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        if not REQUIRED_REVIEW.issubset(reader.fieldnames or []):
            raise ValueError("Revisões sem colunas obrigatórias")
        reviews = {}
        for row in reader:
            key = (row["concurso"].strip(), row["jogo"].strip())
            if key in reviews or not all(key):
                raise ValueError(f"Revisão duplicada ou inválida: {key}")
            state = row["estado"].strip().lower()
            if state not in STATUSES:
                raise ValueError(f"Estado inválido: {state}")
            if state != "pendente" and not (row["revisor"].strip() and
                    row["justificativa"].strip() and row["fonte_oficial"].startswith("https://")
                    and row["competicao"].strip() and row["categoria"].strip()):
                raise ValueError(f"Revisão não fundamentada: {key}")
            reviews[key] = row
    return reviews

def generate(source_cache, out, review_file=None):
    rows = read_records(fetch_csvs(Path(source_cache)))
    reviews = reviews_from(review_file)
    ids = Counter((r["concurso"].strip(), r["jogo"].strip()) for r in rows)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    counts = Counter()
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, delimiter=";")
        writer.writeheader()
        for r in rows:
            key = (r["concurso"].strip(), r["jogo"].strip())
            rev = reviews.get(key, {})
            try:
                date = parse_date(r["data_jogo"])
            except (ValueError, TypeError):
                date = ""
            state = rev.get("estado", "pendente").strip().lower()
            reason = rev.get("justificativa", "sem revisão oficial externa")
            if ids[key] > 1:
                state, reason = "pendente", "duplicidade na chave concurso+jogo"
            if not date:
                state, reason = "pendente", "data de jogo inválida"
            # Estado confirmado significa apenas evidência revisada; NÃO libera Elo.
            record = dict(concurso=key[0], jogo=key[1], data_jogo=date,
                mandante=r["equipe_1"], visitante=r["equipe_2"],
                placar_csv=f'{r["gols_1"]}-{r["gols_2"]}', sorteio=r["sorteio"],
                estado=state, competicao=rev.get("competicao", ""),
                categoria=rev.get("categoria", ""),
                fonte_oficial=rev.get("fonte_oficial", ""),
                status_placar=rev.get("status_placar", ""),
                decisao_elo="bloquear", motivo=reason,
                arquivo_origem=r["_file"])
            writer.writerow(record)
            counts[state] += 1
    missing = set(reviews) - set(ids)
    if missing:
        raise ValueError(f"Revisões sem jogo na fonte: {sorted(missing)[:10]}")
    report = {"total": len(rows), "estados": dict(counts), "duplicidades": sum(v-1 for v in ids.values()),
              "fonte": "marcosvilhena87/Loteca/dados",
              "alerta": "Nenhum jogo liberado ao Elo automaticamente"}
    out.with_suffix(".json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", default="data/cache_loteca")
    parser.add_argument("--output", default="reports/cobertura_integral.csv")
    parser.add_argument("--reviews")
    a = parser.parse_args()
    print(json.dumps(generate(a.cache, a.output, a.reviews), ensure_ascii=False))
if __name__ == "__main__":
    main()
