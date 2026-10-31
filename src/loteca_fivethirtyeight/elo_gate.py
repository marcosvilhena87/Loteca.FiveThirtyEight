"""Barreira fail-closed para liberação de jogos auditados ao Elo."""
import csv
from pathlib import Path

REQUIRED = ("concurso", "jogo", "mandante", "visitante", "data_jogo",
            "competicao", "categoria", "fonte_oficial", "tipo_evidencia_oficial",
            "status_placar", "decisao_elo", "observacoes")
ACCEPTED = {"oficial_profissional"}
APPROVED = {"liberar"}
VERIFIED_SCORE = {"oficial_confirmado", "sumula_confirmada"}
OFFICIAL_EVIDENCE = {"sumula_oficial", "tabela_oficial_resultado", "pagina_oficial_partida"}
def assess(row):
    """Exige decisão explícita e evidência oficial suficiente. Não infere aprovação."""
    checks = {
        "categoria": str(row.get("categoria", "")).strip().lower() in ACCEPTED,
        "decisao": str(row.get("decisao_elo", "")).strip().lower() in APPROVED,
        "fonte": str(row.get("fonte_oficial", "")).startswith("https://"),
        "evidencia": str(row.get("tipo_evidencia_oficial", "")).strip().lower() in OFFICIAL_EVIDENCE,
        "placar": str(row.get("status_placar", "")).strip().lower() in VERIFIED_SCORE,
        "competicao": bool(str(row.get("competicao", "")).strip()),
        "data": bool(str(row.get("data_jogo", "")).strip()),
        "identidades": bool(str(row.get("mandante", "")).strip() and str(row.get("visitante", "")).strip()),
        "observacoes": bool(str(row.get("observacoes", "")).strip()),
    }
    return all(checks.values()), [key for key, ok in checks.items() if not ok]

def export_approved(source, destination):
    """Falha também com chave duplicada ou linha malformada."""
    source, destination = Path(source), Path(destination)
    with source.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=";")
        if not set(REQUIRED).issubset(reader.fieldnames or []):
            raise ValueError("Registro de evidências sem colunas obrigatórias")
        rows = list(reader)
    seen, approved = set(), []
    for row in rows:
        key = (row["concurso"].strip(), row["jogo"].strip())
        if not all(key) or key in seen:
            raise ValueError(f"Chave ausente ou duplicada: {key}")
        seen.add(key)
        allowed, _ = assess(row)
        if allowed:
            approved.append(row)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=reader.fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(approved)
    return len(approved)
