"""Identity resolution with explicit state/category; never equate main and B/U20."""
from __future__ import annotations
import csv
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

def normalize(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c)).upper()
    return re.sub(r"\s+", " ", s).strip()

@dataclass(frozen=True)
class Identity:
    club_id: str
    canonical_name: str
    state: str
    squad: str
    status: str

# Only exact aliases: do not do fuzzy auto-merging.
ALIASES = {
    ("FLAMENGO", "RJ"): ("flamengo_rj", "Flamengo"),
    ("VASCO", "RJ"): ("vasco_rj", "Vasco da Gama"),
    ("VASCO DA GAMA", "RJ"): ("vasco_rj", "Vasco da Gama"),
    ("S. PAULO", "SP"): ("sao_paulo_sp", "São Paulo"),
    ("SAO PAULO", "SP"): ("sao_paulo_sp", "São Paulo"),
    ("SAO CAETANO", "SP"): ("sao_caetano_sp", "São Caetano"),
    ("P. DESPORTOS", "SP"): ("portuguesa_sp", "Portuguesa de Desportos"),
    ("PORTUGUESA", "SP"): ("portuguesa_sp", "Portuguesa de Desportos"),
    ("PONTE PRETA", "SP"): ("ponte_preta_sp", "Ponte Preta"),
    ("PALMEIRAS", "SP"): ("palmeiras_sp", "Palmeiras"),
    ("CORINTHIANS", "SP"): ("corinthians_sp", "Corinthians"),
    ("BOTAFOGO", "RJ"): ("botafogo_rj", "Botafogo RJ"),
    ("BOTAFOGO", "SP"): ("botafogo_sp", "Botafogo SP"),
    ("BOTAFOGO", "PB"): ("botafogo_pb", "Botafogo PB"),
    ("RETRO BRASIL", "PE"): ("retro_pe", "Retrô"),
    ("RETRO", "PE"): ("retro_pe", "Retrô"),
    ("ATHLETICO", "PR"): ("athletico_pr", "Athletico Paranaense"),
    ("ATLETICO", "PR"): ("athletico_pr", "Athletico Paranaense"),
    ("ATLETICO", "MG"): ("atletico_mg", "Atlético Mineiro"),
    ("ATLETICO", "GO"): ("atletico_go", "Atlético Goianiense"),
    ("ATLETICO", "PB"): ("atletico_pb", "Atlético PB"),
}
SQUAD_RE = re.compile(r"(?<![A-Z0-9])(SUB\s*-?\s*(?:15|17|18|19|20|21|23)|U\s*-?\s*(?:15|17|18|19|20|21|23)|B)(?![A-Z0-9])")
def resolve(raw: str) -> Identity:
    value = normalize(raw).replace("–", "-")
    value = re.sub(r"(?<=\w)-(?=SUB)", " ", value)
    m = re.search(r"/([A-Z]{2})(?=$|[\s/])", value)
    state = m.group(1) if m else ""
    name = value[:m.start()] + " " + value[m.end():] if m else value
    name = re.sub(r"\s*-\s*SUB", " SUB", name)
    squad_tokens = SQUAD_RE.findall(name)
    squad = "principal" if not squad_tokens else ("B" if squad_tokens[0] == "B" else squad_tokens[0].replace(" ", "").replace("-", ""))
    name = SQUAD_RE.sub(" ", name)
    name = re.sub(r"\s+", " ", name).strip(" -/")
    known = ALIASES.get((name, state))
    if known:
        base_id, canonical = known
        return Identity(f"{base_id}:{squad}", canonical, state, squad, "alias_exato")
    return Identity("", name, state, squad, "revisar_identidade")

def resolve_rows(raw_rows: list[dict]) -> list[dict]:
    out = []
    for row in raw_rows:
        a, b = resolve(row["equipe_1"]), resolve(row["equipe_2"])
        out.append({"concurso": row["concurso"], "jogo": row["jogo"],
                    "mandante_raw": row["equipe_1"], "visitante_raw": row["equipe_2"],
                    "mandante_id": a.club_id, "visitante_id": b.club_id,
                    "mandante_categoria": a.squad, "visitante_categoria": b.squad,
                    "status_alias": "resolvido" if a.club_id and b.club_id else "pendente",
                    "bloqueio_categoria": "sim" if a.squad != "principal" or b.squad != "principal" else "nao"})
    return out

def write_alias_report(rows: list[dict], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with destination.open("w", newline="", encoding="utf-8-sig") as h:
        w = csv.DictWriter(h, fieldnames=list(rows[0]), delimiter=";")
        w.writeheader()
        w.writerows(rows)
