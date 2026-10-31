"""Conservative institutional identity resolution; never infer a club by fuzzy name."""
import csv
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

REGIONS = {"AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MG","MS","MT","PA","PB","PE","PI","PR","RJ","RN","RO","RR","RS","SC","SE","SP","TO"}

def clean(s):
    s = unicodedata.normalize("NFKD", (s or "").upper().strip())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^A-Z0-9]+", " ", s).strip()

@dataclass(frozen=True)
class Club:
    club_id: str
    country: str
    region: str
    alias: str
    since: int
    until: int
    category: str = "PRINCIPAL"
    competition: str = ""

def read_registry(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        rows = csv.DictReader(f, delimiter=";")
        return [Club(r["club_id"], r["country"], r["region"], r["alias"],
                     int(r["since"]), int(r["until"]),
                     r.get("category") or "PRINCIPAL", r.get("competition") or "")
                for r in rows]

def resolve(name, year, registry, *, country=None, region=None,
            category="PRINCIPAL", competition=None):
    """Return an ID only when the name and *all supplied* trusted context agree.

    Suffix /UF is read from the match name, not guessed. Country/competition
    must originate in verified match metadata, never from a guessed alias.
    """
    if year is None or not name:
        return None
    value = name.upper().strip()
    match = re.search(r"/([A-Z]{2})$", value)
    suffix = match.group(1) if match and match.group(1) in REGIONS else None
    if suffix and region and region.upper() != suffix:
        return None
    requested_region = suffix or (region.upper() if region else None)
    canonical = clean(value[:match.start()] if suffix else value)
    candidates = {
        r.club_id for r in registry
        if clean(r.alias) == canonical
        and r.since <= year <= r.until
        and (not requested_region or r.region == requested_region)
        and (not country or r.country == country.upper())
        and clean(r.category) == clean(category)
        and (not r.competition or (competition and clean(r.competition) == clean(competition)))
    }
    return next(iter(candidates)) if len(candidates) == 1 else None

def same_club(a, b, year, registry, **context):
    x, y = resolve(a, year, registry, **context), resolve(b, year, registry, **context)
    return x is not None and x == y
