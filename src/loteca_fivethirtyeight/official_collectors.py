"""Coletores conservadores de documentos oficiais (CBF, federações estaduais e CONMEBOL).

Descobre páginas/documentos com origem verificável. NÃO extrai placares de textos
ambíguos e NÃO cria fixtures sem dados estruturados revisados.
"""
from __future__ import annotations
import argparse
import csv
import json
import re
import time
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

ALLOWED = {
    "cbf": ("cbf.com.br", "www.cbf.com.br"),
    "fpf": ("futebolpaulista.com.br", "www.futebolpaulista.com.br"),
    "conmebol": ("conmebol.com", "www.conmebol.com"),
}
CLASSES = {
    "sumula": re.compile(r"sumul|match report|ficha (?:del )?partido|informe arbitral", re.I),
    "tabela": re.compile(r"tabela|fixture|calendario|programa.cao|programacion", re.I),
    "regulamento": re.compile(r"regulamento|reglamento|regulations|\bREC\b", re.I),
}
FIELDS = ("organizadora","temporada","competicao","pagina_fonte","documento_url",
          "titulo","tipo","formato","status","observacoes")
DEFAULT_SEEDS = [
    {"organizadora":"cbf","temporada":"2026","competicao":"Brasileiro Série A",
     "url":"https://www.cbf.com.br/futebol-brasileiro/tabelas/campeonato-brasileiro/serie-a/2026?documento=IMT"},
    {"organizadora":"cbf","temporada":"2024","competicao":"Brasileiro séries A-D",
     "url":"https://www.cbf.com.br/a-cbf/noticias/detalhes/arbitragem/cbf-divulga-sumulas-do-brasileirao-serie-a-b-c-e-d"},
    {"organizadora":"fpf","temporada":"2018","competicao":"Copa São Paulo Júnior",
     "url":"https://futebolpaulista.com.br/Noticias/Detalhe.aspx?Noticia=4908"},
    {"organizadora":"fpf","temporada":"2018","competicao":"Paulista Série A1",
     "url":"https://futebolpaulista.com.br/Repositorio/Competicao/Tabela/284/284_636689102177934987.pdf"},
    {"organizadora":"conmebol","temporada":"2026","competicao":"Libertadores",
     "url":"https://www.conmebol.com/libertadores/"},
]
class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.href = None
        self.text = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.href = dict(attrs).get("href")
            self.text = []
    def handle_data(self, data):
        if self.href is not None:
            self.text.append(data)
    def handle_endtag(self, tag):
        if tag == "a" and self.href is not None:
            self.links.append((self.href, " ".join(self.text).strip()))
            self.href = None

def allowed(url: str, org: str) -> bool:
    p = urlparse(url)
    return p.scheme == "https" and p.hostname in ALLOWED.get(org, ())

def classify_link(url: str, label: str) -> str:
    text = label + " " + urlparse(url).path
    for kind, pattern in CLASSES.items():
        if pattern.search(text):
            return kind
    return "indeterminado"

def collect_seed(seed: dict, timeout: int = 25) -> list[dict]:
    org = seed["organizadora"].strip().lower()
    url = seed["url"].strip()
    if not allowed(url, org):
        raise ValueError("Fonte fora do domínio oficial permitido: " + url)
    base = {"organizadora":org,"temporada":seed["temporada"],
            "competicao":seed["competicao"],"pagina_fonte":url}
    def make(docurl, title, status, comment=""):
        return {**base,"documento_url":docurl,"titulo":title,
                "tipo":classify_link(docurl,title),
                "formato":"pdf" if urlparse(docurl).path.lower().endswith(".pdf") else "html",
                "status":status,"observacoes":comment}
    if urlparse(url).path.lower().endswith(".pdf"):
        return [make(url, "documento oficial PDF", "url_cadastrada_pdf_nao_lido",
                     "Link oficial apenas; conteúdo e confrontos não verificados")]
    req = Request(url, headers={"User-Agent":"Loteca538-research/1.0"})
    with urlopen(req, timeout=timeout) as response:
        if urlparse(response.url).hostname not in ALLOWED[org]:
            raise ValueError("Redirecionamento para host não autorizado")
        mime = response.headers.get("Content-Type","").lower()
        if "html" not in mime:
            return [make(url, "recurso oficial", "mime_nao_html",
                         "Requer adaptador de leitura específico: "+mime)]
        html = response.read(3_000_000).decode("utf-8", "replace")
    parser = LinkParser()
    parser.feed(html)
    out = [make(url, "página oficial de referência", "pagina_lida_links_nao_auditados")]
    seen = {url}
    for href, label in parser.links:
        target = urljoin(url,href)
        if not allowed(target,org) or target in seen:
            continue
        kind = classify_link(target,label)
        if kind == "indeterminado" and not target.lower().endswith(".pdf"):
            continue
        seen.add(target)
        out.append(make(target,label[:240] or "link sem rótulo",
                        "documento_descoberto_nao_verificado",
                        "A presença de hyperlink não confirma súmula, campeonato ou placar"))
    return out

def run(seeds: list[dict], pause=1.0) -> tuple[list[dict],list[dict]]:
    documents, errors = [], []
    for seed in seeds:
        try:
            documents.extend(collect_seed(seed))
        except Exception as exc:
            errors.append({"organizadora":seed["organizadora"],"temporada":seed["temporada"],
                           "competicao":seed["competicao"],"pagina_fonte":seed["url"],
                           "erro":str(exc)[:250]})
        if pause > 0:
            time.sleep(pause)
    return documents,errors

def write(outdir:Path, docs:list[dict],errors:list[dict]):
    outdir.mkdir(parents=True,exist_ok=True)
    for filename, rows, cols in [
        ("documentos_oficiais.csv",docs,FIELDS),
        ("falhas_coleta.csv",errors,("organizadora","temporada","competicao","pagina_fonte","erro")),
        ("fila_sumulas_documentais.csv",[d for d in docs if d["tipo"] == "sumula"],FIELDS)]:
        with (outdir/filename).open("w",encoding="utf-8-sig",newline="") as file:
            writer=csv.DictWriter(file,fieldnames=cols,delimiter=";",extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
    (outdir/"resumo_coleta.json").write_text(json.dumps({
        "documentos":len(docs),"falhas":len(errors),
        "tipo":dict(Counter(x["tipo"] for x in docs)),
        "partidas_confirmadas":0,
        "observacao":"Descoberta de documentos, não importação de resultados/súmulas verificadas."
    },ensure_ascii=False,indent=2),encoding="utf-8")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--seeds",type=Path)
    p.add_argument("--output",type=Path,default=Path("reports/fontes_oficiais"))
    p.add_argument("--pause",type=float,default=1.0)
    args=p.parse_args()
    seeds=json.loads(args.seeds.read_text(encoding="utf-8")) if args.seeds else DEFAULT_SEEDS
    docs,errors=run(seeds,args.pause)
    write(args.output,docs,errors)
    print(f"Links documentais: {len(docs)}; falhas: {len(errors)}; partidas homologadas: 0")

if __name__=="__main__":
    main()
