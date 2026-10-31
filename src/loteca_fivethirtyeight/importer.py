"""Importação determinística dos CSVs históricos públicos da Loteca.

Usa apenas a biblioteca padrão. Não presume que todos os concursos tenham 14 jogos
ou que o último arquivo esteja completo. Linhas sorteadas são sinalizadas, não
excluídas silenciosamente.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import unicodedata
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

SOURCE_REPO = "marcosvilhena87/Loteca"
SOURCE_BRANCH = "main"
FILENAMES = tuple(
    f"Loteca_{start:04d}-{start + 99:04d}.csv"
    for start in range(1, 1301, 100)
)
COLUMNS = (
    "concurso", "data_apuracao", "jogo", "gols_1", "equipe_1",
    "equipe_2", "gols_2", "data_jogo", "resultado_placar", "fonte", "sorteio",
)
DATE_PATTERN = re.compile(r"^(?:(?:[^,]+),\s*)?(\d{2})/(\d{2})/(\d{4})$")
CLUB_WHITESPACE = re.compile(r"\s+")


class ImportValidationError(ValueError):
    """Falha de validação com origem e número de linha."""


@dataclass(frozen=True)
class Match:
    concurso: int
    jogo: int
    data_apuracao: str
    data_jogo: str
    equipe_1: str
    equipe_2: str
    equipe_1_id: str
    equipe_2_id: str
    gols_1: int
    gols_2: int
    resultado_placar: str
    fonte: str
    sorteio: str
    sorteio_indicado: bool


def parse_brazilian_date(value: str) -> str:
    """Converte 'segunda-feira, 18/02/2002' ou '18/02/2002' em ISO."""
    match = DATE_PATTERN.fullmatch(value.strip())
    if not match:
        raise ValueError(f"data brasileira inválida: {value!r}")
    day, month, year = map(int, match.groups())
    return date(year, month, day).isoformat()


def normalize_team(value: str) -> str:
    """ID estável: remove acentos, pontuação e espaços repetidos; preserva UF."""
    normalized = unicodedata.normalize("NFKD", value.upper().strip())
    normalized = "".join(c for c in normalized if not unicodedata.combining(c))
    normalized = re.sub(r"[^A-Z0-9/]+", " ", normalized)
    normalized = CLUB_WHITESPACE.sub(" ", normalized).strip()
    if not normalized:
        raise ValueError("equipe vazia")
    return normalized


def _positive_int(value: str, label: str, minimum: int = 0) -> int:
    number = int(value.strip())
    if number < minimum:
        raise ValueError(f"{label} deve ser >= {minimum}")
    return number


def parse_row(row: dict[str, str], source: str, line: int) -> Match:
    """Valida um jogo, inclusive compatibilidade resultado/placar."""
    try:
        if None in row or any(row.get(col) is None for col in COLUMNS):
            raise ValueError("quantidade de colunas incorreta")
        concurso = _positive_int(row["concurso"], "concurso", 1)
        jogo = _positive_int(row["jogo"], "jogo", 1)
        if jogo > 14:
            raise ValueError("jogo deve estar entre 1 e 14")
        g1 = _positive_int(row["gols_1"], "gols_1")
        g2 = _positive_int(row["gols_2"], "gols_2")
        result = row["resultado_placar"].strip().upper()
        if result not in {"1", "X", "2"}:
            raise ValueError(f"resultado inválido: {result!r}")
        expected = "1" if g1 > g2 else "2" if g1 < g2 else "X"
        if result != expected:
            raise ValueError(f"resultado {result} diverge do placar {g1}x{g2} (esperado {expected})")
        team1, team2 = row["equipe_1"].strip(), row["equipe_2"].strip()
        team1_id, team2_id = normalize_team(team1), normalize_team(team2)
        if team1_id == team2_id:
            raise ValueError("equipes iguais na mesma partida")
        apuracao = parse_brazilian_date(row["data_apuracao"])
        game_date = parse_brazilian_date(row["data_jogo"])
        if game_date > apuracao:
            raise ValueError("data do jogo posterior à apuração")
        sorteio = row["sorteio"].strip()
        status = unicodedata.normalize("NFKD", sorteio).encode("ascii", "ignore").decode().casefold()
        # 'Não Demonstrado' não significa 'Sim': preservar texto original.
        indicado = status not in {"", "nao", "nao demonstrado"}
        return Match(
            concurso, jogo, apuracao, game_date, team1, team2,
            team1_id, team2_id, g1, g2, result, row["fonte"].strip(),
            sorteio, indicado,
        )
    except (ValueError, TypeError, OverflowError) as exc:
        raise ImportValidationError(f"{source}:{line}: {exc}") from exc


def load_csv(text: str, source: str = "<memoria>") -> list[Match]:
    reader = csv.DictReader(io.StringIO(text.lstrip("\ufeff")), delimiter=";")
    if reader.fieldnames is None or tuple(reader.fieldnames) != COLUMNS:
        raise ImportValidationError(f"{source}: cabeçalho inesperado: {reader.fieldnames}")
    result = []
    for line, row in enumerate(reader, 2):
        if not any(value and value.strip() for value in row.values() if isinstance(value, str)):
            continue
        result.append(parse_row(row, source, line))
    return result


def fetch_csv(filename: str, timeout: int = 30) -> str:
    if filename not in FILENAMES:
        raise ValueError("nome de arquivo fora da lista esperada")
    url = f"https://raw.githubusercontent.com/{SOURCE_REPO}/{SOURCE_BRANCH}/dados/{filename}"
    request = Request(url, headers={"User-Agent": "Loteca-FiveThirtyEight-importer/0.1"})
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8-sig")


def import_all(local_dir: Path | None = None) -> tuple[list[Match], dict]:
    """Importa 13 CSVs locais ou remotos; duplicatas idênticas são removidas.

    Falha em duplicatas conflitantes, resultados inconsistentes e arquivos ausentes.
    """
    matches: dict[tuple[int, int], Match] = {}
    duplicates = 0
    for filename in FILENAMES:
        if local_dir is None:
            content = fetch_csv(filename)
        else:
            content = (local_dir / filename).read_text(encoding="utf-8-sig")
        for match in load_csv(content, filename):
            key = (match.concurso, match.jogo)
            if key in matches:
                if matches[key] != match:
                    raise ImportValidationError(f"{filename}: duplicata conflitante concurso/jogo {key}")
                duplicates += 1
            else:
                matches[key] = match
    ordered = sorted(matches.values(), key=lambda m: (m.concurso, m.jogo))
    counts: dict[int, int] = {}
    for match in ordered:
        counts[match.concurso] = counts.get(match.concurso, 0) + 1
    report = {
        "arquivos": len(FILENAMES),
        "jogos": len(ordered),
        "concursos": len(counts),
        "duplicatas_identicas_removidas": duplicates,
        "concursos_com_menos_de_14_jogos": sorted(k for k, v in counts.items() if v < 14),
        "jogos_com_sorteio_indicado": sum(m.sorteio_indicado for m in ordered),
        "primeiro_concurso": min(counts) if counts else None,
        "ultimo_concurso": max(counts) if counts else None,
    }
    return ordered, report


def write_csv(matches: list[Match], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(Match.__dataclass_fields__))
        writer.writeheader()
        writer.writerows(asdict(match) for match in matches)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Importa e valida histórico de 13 CSVs da Loteca")
    parser.add_argument("--local-dir", type=Path, help="Pasta local com os 13 arquivos originais")
    parser.add_argument("--output", type=Path, default=Path("data/loteca_normalizada.csv"))
    parser.add_argument("--report", type=Path, default=Path("data/relatorio_importacao.json"))
    args = parser.parse_args(argv)
    matches, report = import_all(args.local_dir)
    write_csv(matches, args.output)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
