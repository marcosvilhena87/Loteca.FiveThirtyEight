"""Registro conservador de clubes. IDs sem UF só são aceitos quando unívocos no período."""
import csv
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

def clean(s):
    s=unicodedata.normalize("NFKD",s.upper().strip())
    s="".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^A-Z0-9]+"," ",s).strip()

@dataclass(frozen=True)
class Club:
    club_id:str
    country:str
    region:str
    alias:str
    since:int
    until:int

def read_registry(path):
    with Path(path).open(encoding="utf-8-sig",newline="") as f:
        return [Club(r["club_id"],r["country"],r["region"],r["alias"],int(r["since"]),int(r["until"])) for r in csv.DictReader(f,delimiter=";")]

def resolve(name, year, registry):
    """Retorna ID apenas se a grafia e a região forem inequívocas."""
    m=re.search(r"/([A-Z]{2})$",name.upper().strip())
    region=m[1] if m else None
    canonical=clean(re.sub(r"/[A-Z]{2}$","",name.upper().strip()))
    candidates={r.club_id for r in registry if clean(r.alias)==canonical
                and r.since<=year<=r.until and (region is None or r.region==region)}
    return next(iter(candidates)) if len(candidates)==1 else None

def same_club(a,b,year,registry):
    x,y=resolve(a,year,registry),resolve(b,year,registry)
    return x is not None and x==y
