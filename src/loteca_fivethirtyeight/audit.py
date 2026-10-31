"""Auditoria de cobertura, clubes e segurança temporal dos dados da Loteca.

Não faz reconciliação automática por similaridade: aliases não triviais
precisam de evidência externa e aprovação humana.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import asdict
from pathlib import Path

from .importer import Match, import_all, normalize_team

# Aliases explícitos de formatação, mantidos para documentar decisões.
# Nenhum nome de clube distinto deve ser fundido apenas pela similaridade.
FORMAT_ALIASES = {
    "SAO  CAETANO/SP": "SAO CAETANO/SP",
    "P.  DESPORTOS/SP": "P DESPORTOS/SP",
    "P. DESPORTOS/SP": "P DESPORTOS/SP",
    "JI-PARANA": "JI PARANA",
    "LETÔNIA": "LETONIA",
    "UNIAO S.JOAO/SP": "UNIAO S JOAO/SP",
    "NOVA VENÉCIA/ES": "NOVA VENECIA/ES",
    "PALMEIRAS-B/SP": "PALMEIRAS B/SP",
}


def canonical_team(raw: str) -> str:
    """Identificador textual auditável; não pressupõe identidade esportiva."""
    return normalize_team(FORMAT_ALIASES.get(raw.strip(), raw))


def audit_matches(matches: list[Match]) -> dict:
    """Verifica sequência de concursos, jogos e possíveis aliases para revisão."""
    keys = [(m.concurso, m.jogo) for m in matches]
    by_concurso = defaultdict(set)
    original_names = Counter()
    variants = defaultdict(set)
    flags = Counter()
    chronology = []
    for match in matches:
        by_concurso[match.concurso].add(match.jogo)
        for raw in (match.equipe_1, match.equipe_2):
            original_names[raw] += 1
            variants[canonical_team(raw)].add(raw)
        flags[match.sorteio] += 1
        if match.data_jogo > match.data_apuracao:
            chronology.append([match.concurso, match.jogo])
    distinct = sorted(by_concurso)
    missing = sorted(set(range(distinct[0], distinct[-1] + 1)) - set(distinct)) if distinct else []
    incomplete = {str(k): sorted(set(range(1, 15)) - v) for k, v in sorted(by_concurso.items()) if v != set(range(1, 15))}
    collisions = [
        {"identificador": k, "grafias": sorted(v)}
        for k, v in sorted(variants.items())
        if len(v) > 1
    ]
    # Não assumir que mesmo prefixo, abreviação ou mesmo nome sem UF prova identidade.
    review = sorted(n for n in original_names if "." in n or "  " in n)
    return {
        "partidas": len(matches),
        "concursos": len(distinct),
        "primeiro_concurso": distinct[0] if distinct else None,
        "ultimo_concurso": distinct[-1] if distinct else None,
        "duplicatas_chave": len(keys) - len(set(keys)),
        "concursos_faltantes_no_intervalo": missing,
        "concursos_incompletos": incomplete,
        "datas_invertidas": chronology,
        "grafias_originais": len(original_names),
        "identificadores_textuais": len(variants),
        "grupos_grafias_equivalentes": collisions,
        "grafias_a_revisar": review,
        "sorteio_por_categoria": dict(sorted(flags.items())),
        "nao_adequados_para_elo_por_sorteio": sum(m.sorteio_indicado for m in matches),
        "pronto_para_treinar_elo": False,
        "pendencias": [
            "Revisar aliases não triviais usando fonte externa e histórico de clubes.",
            "Separar jogos decididos por sorteio antes do treinamento.",
            "Validar a cobertura temporal e a autenticidade com fontes independentes.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audita o histórico da Loteca sem treinar Elo")
    parser.add_argument("--local-dir", type=Path, help="Diretório com os 13 CSVs históricos")
    parser.add_argument("--output", type=Path, default=Path("data/auditoria_historica.json"))
    args = parser.parse_args(argv)
    matches, _ = import_all(args.local_dir)
    report = audit_matches(matches)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["duplicatas_chave"] or report["concursos_faltantes_no_intervalo"] or report["concursos_incompletos"] or report["datas_invertidas"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
