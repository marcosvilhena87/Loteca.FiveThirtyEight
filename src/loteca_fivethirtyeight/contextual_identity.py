"""Contextual candidates require a unique documented fixture, not just a unique club ID.

This module only emits review candidates and never updates the Elo dataset.
"""
import csv
import datetime as dt
from collections import defaultdict
from pathlib import Path
from .club_identity import clean, resolve
from .rsssf_match import parse_date

def contextual_candidates(games, references, registry):
    by_date = defaultdict(list)
    for ref in references:
        try:
            day = dt.date.fromisoformat(ref["date"])
            int(ref["goals_home"]); int(ref["goals_away"])
        except (KeyError, ValueError, TypeError):
            continue
        if (ref.get("category") != "PRINCIPAL" or not ref.get("competition")
                or not ref.get("url") or not ref.get("home") or not ref.get("away")
                or not ref.get("line")):
            continue
        by_date[day].append(ref)
    for g in games:
        day = parse_date(g.get("data_jogo", ""))
        year = day.year if day else None
        category = g.get("category") or g.get("categoria") or "PRINCIPAL"
        home_id = resolve(g["equipe_1"], year, registry, category=category)
        away_id = resolve(g["equipe_2"], year, registry, category=category)
        possibilities = {}
        if day and category == "PRINCIPAL" and ((home_id is None) != (away_id is None)):
            try:
                score = (int(g["gols_1"]), int(g["gols_2"]))
            except (ValueError, TypeError, KeyError):
                score = None
            for ref in by_date[day]:
                if score != (int(ref["goals_home"]), int(ref["goals_away"])):
                    continue
                reference_known = ref["away"] if home_id is None else ref["home"]
                known_id = away_id if home_id is None else home_id
                if resolve(reference_known, year, registry) != known_id:
                    continue
                missing_reference = ref["home"] if home_id is None else ref["away"]
                missing_caixa = g["equipe_1"] if home_id is None else g["equipe_2"]
                if clean(missing_caixa.split("/")[0]) != clean(missing_reference.split("/")[0]):
                    continue
                proposed = resolve(missing_reference, year, registry)
                if proposed is None or proposed == known_id:
                    continue
                # Distinct source lines are separate documentary hypotheses.
                key = (ref["competition"], ref["url"], str(ref["line"]),
                       ref["home"], ref["away"], ref["date"])
                possibilities[key] = (proposed, ref)
        unique_ids = {item[0] for item in possibilities.values()}
        if len(possibilities) == 1 and len(unique_ids) == 1:
            status = "CANDIDATO_CONTEXTO_REVISAR"
            candidate, evidence = next(iter(possibilities.values()))
        elif len(possibilities) > 1:
            status, candidate, evidence = "AMBIGUO_CONTEXTO", "", {}
        else:
            status, candidate, evidence = "QUARENTENA", "", {}
        yield {
            "concurso": g.get("concurso", ""), "jogo": g.get("jogo", ""),
            "data_jogo": g.get("data_jogo", ""),
            "equipe_1": g["equipe_1"], "equipe_2": g["equipe_2"],
            "gols_1": g["gols_1"], "gols_2": g["gols_2"],
            "home_club_id": home_id or "", "away_club_id": away_id or "",
            "candidate_id": candidate, "status": status,
            "competition": evidence.get("competition", ""),
            "source_url": evidence.get("url", ""),
            "source_line": evidence.get("line", ""),
            "matching_sources": len(possibilities),
        }

def export_contextual(games, references, registry, destination):
    rows = list(contextual_candidates(games, references, registry))
    Path(destination).parent.mkdir(parents=True, exist_ok=True)
    fields = ["concurso", "jogo", "data_jogo", "equipe_1", "equipe_2",
              "gols_1", "gols_2", "home_club_id", "away_club_id",
              "candidate_id", "status", "competition", "source_url",
              "source_line", "matching_sources"]
    with Path(destination).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter=";")
        w.writeheader()
        w.writerows(rows)
    from collections import Counter
    return dict(Counter(r["status"] for r in rows))
