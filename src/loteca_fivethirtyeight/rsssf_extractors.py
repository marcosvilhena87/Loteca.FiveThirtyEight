"""Extratores especializados para RSSSF 2002 (Rio-São Paulo e Copa dos Campeões).

Resultados são evidência histórica, NÃO aprovação de dados ao Elo.
"""
from __future__ import annotations
import argparse
import csv
import json
import re
from datetime import date
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from pathlib import Path

SOURCES = {
    "rio_sp_2002": ("https://www.rsssf.org/tablesr/riospl02.html", "Torneio Rio-São Paulo 2002"),
    "copa_campeoes_2002": ("https://www.rsssf.org/tablesb/brazchampcup02.html", "Copa dos Campeões 2002"),
}
COLUMNS = ("date", "home", "away", "home_goals", "away_goals",
           "competition", "source_url", "phase", "round", "evidence_level")
MONTHS = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5,
          "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
# Cup round details can include notes after result, but must have a full team at both ends.
SCORE = re.compile(r"^\s*(?P<home>[\wÀ-ÿ][\wÀ-ÿ ./'-]*?)\s+"
                   r"(?P<h>\d{1,2})\s*-\s*(?P<a>\d{1,2})\s+"
                   r"(?P<away>[\wÀ-ÿ][\wÀ-ÿ ./'-]*?)"
                   r"(?:\s{2,}.*)?\s*$")
DATES = re.compile(r"^\s*\[(?P<mon>Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+"
                   r"(?P<day>\d{1,2})\]\s*$", re.I)
ROUND = re.compile(r"^\s*Round\s+(\d+)\s*$", re.I)
TWO_LEGS = re.compile(r"^\s*(?P<home>[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ .'-]+?)\s+(?P<h1>\d+)-(?P<a1>\d+)\s+(?P<h2>\d+)-(?P<a2>\d+)\s+(?P<away>[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ .'-]+?)\s*$")
TWO_DATES = re.compile(r"^\[(?P<month>Apr|May)\s+(?P<first>\d{1,2})\s+and\s+(?P<second>\d{1,2})\]$", re.I)
PHASES = {"FIRST PHASE", "QUARTERFINALS", "SEMIFINALS", "FINAL"}
class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
    def handle_data(self, value):
        self.parts.append(value)
    def handle_starttag(self, tag, attrs):
        if tag in ("br","p","div","pre","h1","h2","h3","tr","li"):
            self.parts.append("\n")
    def handle_endtag(self, tag):
        if tag in ("p","div","pre","tr","h1","h2","h3"):
            self.parts.append("\n")

def html_to_lines(html):
    parser = TextExtractor()
    parser.feed(html)
    return "".join(parser.parts).splitlines()

def _match_line(raw):
    # Remove HTML artifacts and trailing match-location/pk notes.
    s = re.sub(r"\s+\(.*$", "", raw.rstrip())
    m = SCORE.match(s)
    if not m:
        return None
    home, away = m["home"].strip(), m["away"].strip()
    if not home or not away or home[0].isdigit() or away[0].isdigit():
        return None
    return home, away, int(m["h"]), int(m["a"])

def parse_lines(lines, competition_key):
    if competition_key not in SOURCES:
        raise ValueError("Competição desconhecida")
    url, comp = SOURCES[competition_key]
    phase = ""
    round_number = ""
    current_date = None
    output = []
    started = False
    two_dates = None
    for raw in lines:
        line = raw.strip()
        upper = line.upper()
        if competition_key == "rio_sp_2002":
            rm = ROUND.fullmatch(line)
            if rm:
                started = True
                phase = "Primeira fase"
                round_number = rm.group(1)
                current_date = None
                continue
            if not started:
                continue
            if upper in ("SEMI-FINALS", "SEMIFINALS", "FINALS", "FINAL"):
                phase = "Semifinais" if "SEMI" in upper else "Final"
                round_number = ""
                current_date = None
                two_dates = None
                continue
            if phase in ("Semifinais", "Final"):
                mdates = TWO_DATES.fullmatch(line)
                if mdates:
                    month = MONTHS[mdates["month"].title()]
                    two_dates = (
                        date(2002, month, int(mdates["first"])).isoformat(),
                        date(2002, month, int(mdates["second"])).isoformat()
                    )
                    continue
                legs = TWO_LEGS.fullmatch(line)
                if legs and two_dates:
                    home, away = legs["home"].strip(), legs["away"].strip()
                    scores = (
                        (two_dates[0], home, away, int(legs["h1"]), int(legs["a1"])),
                        (two_dates[1], away, home, int(legs["a2"]), int(legs["h2"]))
                    )
                    for d, h, a, hg, ag in scores:
                        output.append(dict(date=d, home=h, away=a,
                            home_goals=hg, away_goals=ag, competition=comp,
                            source_url=url, phase=phase, round=round_number,
                            evidence_level="B"))
                    two_dates = None
                    continue
        else:
            if upper in PHASES:
                phase = upper.title()
                started = True
                current_date = None
                continue
            if not started:
                continue
            if upper.startswith("GROUP ") and phase == "First Phase":
                round_number = upper.split("(", 1)[0].strip()
                current_date = None
                continue
            if "LEG" in upper and phase == "Final":
                round_number = line.split("[", 1)[0].strip()
        dm = DATES.fullmatch(line)
        if not dm:
            # Cup final leg date is embedded in the heading.
            inline = re.search(r"\[(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2})\]", line, re.I)
            if inline and phase == "Final":
                dm = DATES.fullmatch("[" + inline.group(1) + " " + inline.group(2) + "]")
        if dm:
            current_date = date(2002, MONTHS[dm["mon"].title()], int(dm["day"])).isoformat()
            continue
        if current_date is None:
            continue
        found = _match_line(raw)
        if not found:
            continue
        home, away, h, a = found
        output.append(dict(date=current_date, home=home, away=away,
                           home_goals=h, away_goals=a, competition=comp,
                           source_url=url, phase=phase, round=round_number,
                           evidence_level="B"))
    # Fail closed when RSSSF layout changed or page was not an expected competition.
    if not output:
        raise ValueError(f"Não foi possível extrair partidas de {competition_key}")
    seen = set()
    for r in output:
        key = (r["date"], r["home"], r["away"], r["home_goals"], r["away_goals"])
        if key in seen:
            raise ValueError(f"Partida duplicada na extração: {key}")
        seen.add(key)
    return output

def fetch_and_parse(key):
    if key not in SOURCES:
        raise ValueError("Competição desconhecida")
    req = Request(SOURCES[key][0], headers={"User-Agent":"Loteca538-evidence-audit/1.0"})
    with urlopen(req, timeout=30) as response:
        body = response.read()
        charset = response.headers.get_content_charset() or "windows-1252"
    return parse_lines(html_to_lines(body.decode(charset, errors="replace")), key)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--competition", choices=list(SOURCES)+["all"], default="all")
    p.add_argument("--output", default="data/evidencias/rsssf_2002_extraido.csv")
    p.add_argument("--input-html", help="Arquivo HTML local, somente para competição única")
    args = p.parse_args()
    keys = list(SOURCES) if args.competition == "all" else [args.competition]
    if args.input_html and len(keys) != 1:
        p.error("--input-html exige apenas uma competição")
    records=[]
    for key in keys:
        if args.input_html:
            path=Path(args.input_html)
            content=path.read_bytes().decode("windows-1252", errors="replace")
            records.extend(parse_lines(html_to_lines(content), key))
        else:
            records.extend(fetch_and_parse(key))
    target=Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer=csv.DictWriter(handle, fieldnames=COLUMNS, delimiter=";")
        writer.writeheader()
        writer.writerows(records)
    print(json.dumps({"partidas":len(records),"arquivo":str(target)},ensure_ascii=False))

if __name__ == "__main__":
    main()
