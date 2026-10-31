"""Extração conservadora de evidências em PDFs oficiais, com rastreabilidade por página.

Uma detecção textual nunca representa homologação automática de resultado.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import re
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import fitz  # PyMuPDF

COLUMNS = ("organizadora","temporada","competicao","documento_url","sha256",
           "pagina","mandante_texto","visitante_texto","data_iso","placar",
           "categoria_texto","id_partida","status","trecho_evidencia")
DATE = re.compile(r"(?<!\d)(\d{2})/(\d{2})/(\d{4})(?!\d)")
SCORE = re.compile(r"(?<!\d)(\d{1,2})\s*[-xX×]\s*(\d{1,2})(?!\d)")
MATCH = re.compile(r"(?P<home>[^\n;]{3,65}?)\s+(?P<g1>\d{1,2})\s*[-xX×]\s*(?P<g2>\d{1,2})\s+(?P<away>[^\n;]{3,65})")
CATEGORY = re.compile(r"\b(sub[\s-]?(?:15|17|20|23)|feminin[oa]|equipe\s+b|reservas?)\b", re.I)
MATCH_ID = re.compile(r"(?:partida|jogo|match)\s*(?:n[ºo°.]?\s*)?(\d{1,8})", re.I)

def safe_pdf(data: bytes, max_bytes: int = 20_000_000, max_pages: int = 300):
    if len(data) > max_bytes or not data.startswith(b"%PDF-"):
        raise ValueError("PDF inválido ou acima do limite")
    doc = fitz.open(stream=data, filetype="pdf")
    if doc.is_encrypted or len(doc) > max_pages:
        doc.close()
        raise ValueError("PDF protegido ou páginas acima do limite")
    return doc

def read_pdf(data: bytes, metadata: dict) -> list[dict]:
    sha = hashlib.sha256(data).hexdigest()
    results = []
    with safe_pdf(data) as doc:
        for number, page in enumerate(doc, 1):
            text = page.get_text("text", sort=True)
            base = {k: metadata.get(k, "") for k in ("organizadora","temporada","competicao","documento_url")}
            base.update(sha256=sha,pagina=str(number),mandante_texto="",
                        visitante_texto="",data_iso="",placar="",categoria_texto="",
                        id_partida="",status="revisar",trecho_evidencia="")
            if not text.strip():
                results.append({**base,"status":"pagina_sem_texto",
                                "trecho_evidencia":"Sem camada de texto; OCR somente após revisão"})
                continue
            dates = DATE.findall(text)
            cats = CATEGORY.findall(text)
            ids = MATCH_ID.findall(text)
            if len(dates) == 1:
                d,m,y=dates[0]
                try:
                    from datetime import date
                    base["data_iso"]=date(int(y),int(m),int(d)).isoformat()
                except ValueError:
                    pass
            if len(cats) == 1:
                base["categoria_texto"]=cats[0]
            if len(ids) == 1:
                base["id_partida"]=ids[0]
            found=list(MATCH.finditer(text))
            if len(found) == 1:
                match=found[0]
                base.update(mandante_texto=match["home"].strip(),
                            visitante_texto=match["away"].strip(),
                            placar=f'{match["g1"]}-{match["g2"]}',
                            status="candidato_extraido",
                            trecho_evidencia=match.group(0)[:250])
            elif found:
                base.update(status="multiplos_confrontos_na_pagina",
                            trecho_evidencia=f"{len(found)} confrontos; revisão necessária")
            else:
                base.update(status="sem_confronto_estruturado",
                            trecho_evidencia=text[:250].replace("\n"," "))
            results.append(base)
    return results

def download(url: str, max_bytes: int = 20_000_000) -> bytes:
    p=urlparse(url)
    if p.scheme != "https" or not p.hostname:
        raise ValueError("Somente URL HTTPS")
    from .official_collectors import ALLOWED
    if p.hostname not in {host for hosts in ALLOWED.values() for host in hosts}:
        raise ValueError("Download restrito aos sites oficiais cadastrados")
    req=Request(url,headers={"User-Agent":"Loteca538-research/1.0"})
    with urlopen(req,timeout=30) as response:
        if urlparse(response.url).hostname not in {h for hs in ALLOWED.values() for h in hs}:
            raise ValueError("Redirecionamento externo não autorizado")
        length=response.headers.get("Content-Length")
        if length and int(length)>max_bytes:
            raise ValueError("Arquivo acima do limite")
        raw=response.read(max_bytes+1)
    if len(raw)>max_bytes:
        raise ValueError("Arquivo acima do limite")
    return raw

def export(rows: list[dict], folder: Path):
    folder.mkdir(parents=True,exist_ok=True)
    for filename,subset in [
        ("extracao_documental.csv",rows),
        ("fila_revisao_pdf.csv",[r for r in rows if r["status"]!="candidato_extraido"]),
        ("candidatos_confronto.csv",[r for r in rows if r["status"]=="candidato_extraido"])
    ]:
        with (folder/filename).open("w",encoding="utf-8-sig",newline="") as f:
            w=csv.DictWriter(f,fieldnames=COLUMNS,delimiter=";",extrasaction="ignore")
            w.writeheader()
            w.writerows(subset)
    (folder/"resumo_pdf.json").write_text(json.dumps({
        "paginas":len(rows),"candidatos":sum(r["status"]=="candidato_extraido" for r in rows),
        "liberados_elo":0,
        "nota":"Nenhuma extração textual comprova súmula ou valida resultado automaticamente."
    },ensure_ascii=False,indent=2),encoding="utf-8")

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--pdf",type=Path,help="PDF local")
    p.add_argument("--url",help="URL HTTPS oficial do PDF")
    p.add_argument("--organizadora",required=True)
    p.add_argument("--temporada",required=True)
    p.add_argument("--competicao",required=True)
    p.add_argument("--output",type=Path,default=Path("reports/extracao_pdf"))
    a=p.parse_args()
    if bool(a.pdf)==bool(a.url):
        p.error("Informe exatamente --pdf ou --url")
    payload=a.pdf.read_bytes() if a.pdf else download(a.url)
    origin=a.url or a.pdf.resolve().as_uri()
    rows=read_pdf(payload,dict(organizadora=a.organizadora,temporada=a.temporada,
                               competicao=a.competicao,documento_url=origin))
    export(rows,a.output)
    print(f"Paginas: {len(rows)}; Elo liberado: 0; relatorio: {a.output}")

if __name__=="__main__":
    main()
