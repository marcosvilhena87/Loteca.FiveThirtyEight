"""Auditoria externa, conservadora e reproduzível, dos jogos históricos da Loteca.

Uso: python -m loteca538.external_audit --output reports/auditoria
Para pesquisas reais configure SERPER_API_KEY (Google via Serper).
Sem chave, gera fila de revisão e links de busca; NUNCA confirma jogos offline.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import time
import unicodedata
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

SOURCE = "https://raw.githubusercontent.com/marcosvilhena87/Loteca/main/dados/"
HEADERS = {"User-Agent": "Loteca538-auditoria/1.0 (research; respect rate limits)"}
FIELDS = ("concurso", "jogo", "data_jogo", "equipe_1", "equipe_2",
          "gols_1", "gols_2", "resultado_placar", "sorteio")
OUTPUT_FIELDS = ("chave", "concurso", "jogo", "data_iso", "mandante", "visitante",
                 "placar", "classificacao", "competicao", "equipe_principal",
                 "elegivel_elo", "confianca", "evidencia_url", "evidencia_titulo",
                 "motivo", "risco", "consulta_url", "fonte_csv")
BASE_MARKERS = re.compile(r"\b(SUB[\s-]?(?:15|17|18|19|20|21|23)|U[\s-]?(?:15|17|18|19|20|21|23)|JUNIOR(?:ES)?|COPINHA|BASE)\b", re.I)
FEMALE_MARKERS = re.compile(r"\b(FEMININ[OA]|WOMEN|LADIES)\b", re.I)
OTHER_MARKERS = re.compile(r"\b(FUTSAL|BEACH SOCCER|FUTEBOL DE AREIA)\b", re.I)
RESERVE_MARKERS = re.compile(r"\b(RESERVAS?|EQUIPE B|TEAM B|SEGUNDA EQUIPE)\b", re.I)
FRIENDLY_MARKERS = re.compile(r"\b(AMISTOS[OA]|FRIENDLY|FRIENDLIES)\b", re.I)
COMP_MARKERS = re.compile(
    r"(CAMPEONATO [A-ZÁÉÍÓÚÃÕÇ /-]+|COPA [A-ZÁÉÍÓÚÃÕÇ /-]+|"
    r"BRASILEIR[ÃA]O(?: [A-ZÁÉÍÓÚÃÕÇ /-]+)?|S[ÉE]RIE [A-D]|"
    r"LIBERTADORES|SUL.AMERICANA|TORNEIO RIO.S[ÃA]O PAULO)", re.I
)
LOWER_PRIORITY = {"principal_confirmada": 0, "excluida_confirmada": 0}

def fold(value: str) -> str:
    value = unicodedata.normalize("NFKD", str(value or ""))
    return re.sub(r"\s+", " ", "".join(c for c in value if not unicodedata.combining(c)).upper()).strip()

def parse_date(value: str) -> str:
    value = (value or "").strip()
    m = re.search(r"(\d{2})/(\d{2})/(\d{4})", value)
    if not m:
        raise ValueError("data não reconhecida")
    return datetime.strptime(m.group(0), "%d/%m/%Y").date().isoformat()

def fetch_csvs(cache: Path, remote: bool = True) -> list[Path]:
    cache.mkdir(parents=True, exist_ok=True)
    files = []
    for start in range(1, 1301, 100):
        name = f"Loteca_{start:04d}-{start+99:04d}.csv"
        path = cache / name
        if remote and not path.exists():
            req = Request(SOURCE + name, headers=HEADERS)
            with urlopen(req, timeout=35) as response:
                body = response.read()
            path.write_bytes(body)
        if not path.exists():
            raise FileNotFoundError(f"Falta CSV: {path}")
        files.append(path)
    return files

def read_records(files: list[Path]) -> list[dict]:
    records = []
    for path in files:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, delimiter=";")
            if not set(FIELDS).issubset(set(reader.fieldnames or [])):
                raise ValueError(f"Colunas obrigatórias ausentes: {path}")
            for row_number, row in enumerate(reader, 2):
                row["_file"] = path.name
                row["_line"] = row_number
                records.append(row)
    return records

def search_query(row: dict) -> str:
    return (f'"{row["equipe_1"]}" "{row["equipe_2"]}" '
            f'{row["data_jogo"][-4:]} futebol competição placar')

def serper_search(query: str, key: str, retries: int = 2) -> list[dict]:
    payload = json.dumps({"q": query, "gl": "br", "hl": "pt-br", "num": 8}).encode()
    req = Request("https://google.serper.dev/search", data=payload,
                  headers={"Content-Type": "application/json", "X-API-KEY": key,
                           **HEADERS}, method="POST")
    for retry in range(retries + 1):
        try:
            with urlopen(req, timeout=25) as response:
                data = json.load(response)
            return data.get("organic", [])
        except HTTPError as exc:
            if exc.code not in (429, 500, 502, 503) or retry == retries:
                raise
        except (TimeoutError, URLError):
            if retry == retries:
                raise
        time.sleep(2 ** retry)
    return []

def name_tokens(raw: str) -> list[str]:
    # Remove a UF, mas não transforma "BOTAFOGO/SP" em "BOTAFOGO/RJ".
    name = fold(raw).split("/")[0].strip()
    return [t for t in re.findall(r"[A-Z0-9]+", name)
            if len(t) >= 3 and t not in {"ESPORTE", "CLUBE", "FUTEBOL", "SPORT", "CLUB", "ASSOCIACAO"}]

def evidence_match(row: dict, item: dict, date_iso: str) -> bool:
    """O resultado da busca não é prova: exige times, data e placar no mesmo resultado.
    A confirmação esportiva final exige também fonte e competição identificadas.
    """
    title = str(item.get("title") or "")
    snippet = str(item.get("snippet") or "")
    body = fold(title + " " + snippet)
    sides = [name_tokens(row["equipe_1"]), name_tokens(row["equipe_2"])]
    if not all(any(token in body for token in tokens) for tokens in sides):
        return False
    d = datetime.fromisoformat(date_iso)
    date_variants = (d.strftime("%d/%m/%Y"), d.strftime("%d-%m-%Y"),
                     d.strftime("%Y-%m-%d"), f"{d.day} DE {fold(d.strftime('%B'))} DE {d.year}")
    if not any(fold(variant) in body for variant in date_variants):
        return False
    g1, g2 = row["gols_1"].strip(), row["gols_2"].strip()
    if not (g1.isdigit() and g2.isdigit()):
        return False
    return bool(re.search(rf"(?<!\d){g1}\s*[-X×:]\s*{g2}(?!\d)", body)
                or re.search(rf"(?<!\d){g2}\s*[-X×:]\s*{g1}(?!\d)", body))

def classify(row: dict, results: list[dict] | None = None) -> dict:
    d = parse_date(row["data_jogo"])
    query = search_query(row)
    query_url = "https://www.google.com/search?" + urlencode({"q": query})
    base = {
        "chave": f'{row["concurso"]}:{row["jogo"]}', "concurso": row["concurso"],
        "jogo": row["jogo"], "data_iso": d, "mandante": row["equipe_1"],
        "visitante": row["equipe_2"],
        "placar": f'{row["gols_1"]}-{row["gols_2"]}',
        "classificacao": "pendente", "competicao": "", "equipe_principal": "indeterminado",
        "elegivel_elo": "nao", "confianca": "nenhuma", "evidencia_url": "",
        "evidencia_titulo": "", "motivo": "sem evidência externa suficiente",
        "risco": "alto", "consulta_url": query_url, "fonte_csv": row["_file"]
    }
    if fold(row.get("sorteio", "")) in ("SIM", "S", "YES") or "SORTEIO" in fold(row.get("resultado_placar", "")):
        base.update(classificacao="sorteio", motivo="resultado lotérico por sorteio; requer verificação da realização esportiva", risco="critico")
        return base

    candidates = []
    for item in (results or []):
        link = str(item.get("link") or "")
        if not link.startswith("https://"):
            continue
        if not evidence_match(row, item, d):
            continue
        blob = fold(f'{item.get("title", "")} {item.get("snippet", "")}')
        comp_match = COMP_MARKERS.search(blob)
        if not comp_match:
            continue
        competition = comp_match.group(0).strip()
        if OTHER_MARKERS.search(blob):
            classification, reason = "excluida_confirmada", "outra modalidade"
        elif FEMALE_MARKERS.search(blob):
            classification, reason = "excluida_confirmada", "futebol feminino"
        elif BASE_MARKERS.search(blob):
            classification, reason = "excluida_confirmada", "categoria de base"
        elif RESERVE_MARKERS.search(blob):
            classification, reason = "excluida_confirmada", "equipe B/reserva"
        elif FRIENDLY_MARKERS.search(blob):
            classification, reason = "amistoso", "amistoso separado do Elo oficial"
        else:
            # Não é lícito inferir principal só porque não há marcador de base.
            classification, reason = "categoria_indeterminada", "competição identificada, categoria principal não comprovada"
        candidates.append((classification, reason, competition, link, str(item.get("title", ""))))
    if not candidates:
        base["motivo"] = "nenhum resultado externo apresentou simultaneamente clubes, data, placar e competição"
        return base
    # Não aceitar fontes conflitantes. Confirmação automática de exclusão exige
    # ao menos duas evidências independentes (domínios distintos).
    from urllib.parse import urlparse
    excluded = [c for c in candidates if c[0] == "excluida_confirmada"]
    domains = {urlparse(c[3]).netloc.lower().removeprefix("www.") for c in excluded}
    if len(domains) >= 2 and len({c[1] for c in excluded}) == 1 and not any(c[0] == "categoria_indeterminada" for c in candidates):
        selected = excluded[0]
        base.update(classificacao="excluida_confirmada", competicao=selected[2],
                    equipe_principal="nao", confianca="media", evidencia_url=selected[3],
                    evidencia_titulo=selected[4], motivo=selected[1], risco="baixo")
    else:
        selected = candidates[0]
        base.update(classificacao="revisao_externa", competicao=selected[2],
                    evidencia_url=selected[3], evidencia_titulo=selected[4],
                    motivo="correspondência externa encontrada; categoria e fontes precisam de revisão",
                    confianca="baixa", risco="alto")
    return base

def audit(records: list[dict], key: str = "", pause: float = 1.0, max_searches: int = 0) -> list[dict]:
    output = []
    seen = Counter((r["concurso"].strip(), r["jogo"].strip()) for r in records)
    used = 0
    cache = {}
    for row in records:
        try:
            query = search_query(row)
            results = []
            if key and (max_searches <= 0 or used < max_searches):
                if query not in cache:
                    cache[query] = serper_search(query, key)
                    used += 1
                    if pause:
                        time.sleep(pause)
                results = cache[query]
            result = classify(row, results)
        except (ValueError, KeyError) as exc:
            result = {field: "" for field in OUTPUT_FIELDS}
            result.update(chave=f'{row.get("concurso")}:{row.get("jogo")}',
                          concurso=row.get("concurso", ""), jogo=row.get("jogo", ""),
                          classificacao="erro_dados", motivo=str(exc), risco="critico",
                          elegivel_elo="nao", fonte_csv=row["_file"])
        if seen[(row["concurso"].strip(), row["jogo"].strip())] > 1:
            result.update(classificacao="duplicidade", risco="critico",
                          elegivel_elo="nao", motivo="chave concurso+jogo repetida")
        if result["classificacao"] == "pendente" and not key:
            result["motivo"] = "pesquisa externa não executada (SERPER_API_KEY ausente)"
        if result["classificacao"] == "pendente" and key and max_searches and used >= max_searches:
            result["motivo"] += "; verificar se o limite de buscas foi atingido"
        output.append(result)
    return output

def write_reports(records: list[dict], outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    priority = {"critico": 0, "alto": 1, "medio": 2, "baixo": 3}
    records.sort(key=lambda r: (priority.get(r["risco"], 4), int(r["concurso"] or 0),
                                int(r["jogo"] or 0)))
    for name, rows in (("auditoria_completa.csv", records),
                       ("excecoes.csv", [r for r in records if r["risco"] in ("critico", "alto")])):
        with (outdir / name).open("w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS, delimiter=";", extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
    counts = Counter(r["classificacao"] for r in records)
    risks = Counter(r["risco"] for r in records)
    summary = {"total": len(records), "classificacoes": dict(counts), "riscos": dict(risks),
               "elegiveis_elo": sum(r["elegivel_elo"] == "sim" for r in records),
               "regra": "sem evidencia externa inequívoca, não liberar para Elo"}
    (outdir / "resumo.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    md = ["# Auditoria externa da Loteca", "", f"Registros: **{len(records)}**",
          f"Elegíveis automaticamente ao Elo: **{summary['elegiveis_elo']}**",
          "", "## Classificação", ""]
    md += [f"- {key}: {val}" for key, val in sorted(counts.items())]
    md += ["", "## Risco", ""]
    md += [f"- {key}: {val}" for key, val in sorted(risks.items())]
    md += ["", "## Observações", "",
           "Uma busca não confirma automaticamente a utilização de equipes principais.",
           "Resultados por sorteio são bloqueados; confrontos sem evidência permanecem pendentes.",
           "A exclusão automática exige concordância de dois domínios externos independentes.",
           "Verifique manualmente partidas com conflito de categoria, placar e competição.",
           ""]
    (outdir / "RELATORIO.md").write_text("\n".join(md), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=Path("data/raw/loteca"))
    parser.add_argument("--offline", action="store_true", help="não baixar CSVs; usar cache")
    parser.add_argument("--output", type=Path, default=Path("reports/auditoria_externa"))
    parser.add_argument("--pause", type=float, default=1.0)
    parser.add_argument("--max-searches", type=int, default=0, help="0=sem limite")
    args = parser.parse_args()
    rows = read_records(fetch_csvs(args.cache, remote=not args.offline))
    reports = audit(rows, os.getenv("SERPER_API_KEY", ""), args.pause, args.max_searches)
    write_reports(reports, args.output)
    print(json.dumps({"registros": len(reports), "saida": str(args.output),
                      "status": dict(Counter(r["classificacao"] for r in reports))},
                     ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
