"""Conservative per-row triage of international candidate matches.

An algorithmic match is NOT independent verification; all records remain
blocked until a human reviewer checks an additional source.
"""
import csv
import sys
from collections import Counter
from pathlib import Path

def read_rows(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))

def triage(rows):
    counts = Counter((r.get("concurso"), r.get("jogo")) for r in rows)
    for r in rows:
        result = dict(r)
        required = ("concurso", "jogo", "date", "home_club_id_candidate",
                    "away_club_id_candidate", "competition", "url", "line", "score")
        reasons = []
        if any(not r.get(k) for k in required):
            reasons.append("MISSING_PROVENANCE")
        if r.get("home_club_id_candidate") == r.get("away_club_id_candidate"):
            reasons.append("SAME_CLUB_ID")
        if counts[(r.get("concurso"), r.get("jogo"))] > 1:
            reasons.append("MULTIPLE_MATCHES_PER_CAIXA_GAME")
        if r.get("status") != "REVIEW_ONLY_UNVERIFIED_ALIAS":
            reasons.append("SOURCE_OR_ALIAS_NOT_ELIGIBLE")
        result["audit_reasons"] = "|".join(reasons)
        result["independent_source_url"] = ""
        result["reviewer"] = ""
        result["reviewed_at"] = ""
        result["identity_decision"] = "PENDING"
        result["fixture_decision"] = "PENDING"
        result["elo_eligible"] = "NO"
        result["triage_status"] = "BLOCKED_ANOMALY" if reasons else "PENDING_INDEPENDENT_REVIEW"
        yield result

def main(source, destination):
    rows = list(triage(read_rows(source)))
    Path(destination).parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else ["triage_status", "elo_eligible"]
    with open(destination, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)
    print(dict(Counter(x["triage_status"] for x in rows)))
    print(f"Review candidates: {len(rows)}; Elo releases: 0")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
