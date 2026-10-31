"""Diagnóstico secundário das exceções sem alterar o gate Elo."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from .rsssf_match import date_iso, norm

def summarize(rows, sources):
    dates=[date_iso(s["date"]) for s in sources]
    start,end=(min(dates),max(dates)) if dates else (None,None)
    aliases=Counter()
    reasons=Counter()
    annotated=[]
    for row in rows:
        item=dict(row)
        label=row.get("categoria_excecao") or "confirmado"
        reasons[label]+=1
        try:
            d=date_iso(row["data_loteca"])
            within=bool(start and start<=d<=end)
        except (ValueError,KeyError):
            within=False
        item["dentro_janela_global"]="sim" if within else "nao"
        if label=="alias_ausente":
            # Extrai variantes diretamente da justificativa gerada pelo cruzador.
            message=row.get("motivo","")
            if message.startswith("alias nao cadastrado: "):
                for name in message.partition(": ")[2].split(", "):
                    if name.strip():
                        aliases[norm(name)]+=1
            item["prioridade"]="alta" if within else "baixa_escopo"
        elif label in ("divergencia_data","divergencia_placar","conflito_fontes","revisao_humana"):
            item["prioridade"]="revisao"
        else:
            item["prioridade"]="rotina"
        annotated.append(item)
    return annotated, {"motivos":dict(reasons),"aliases":dict(aliases),
                       "periodo_coberto":[start,end],
                       "observacao":"Janela global diagnostica; nao comprova competicao"}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--matches",required=True)
    p.add_argument("--rsssf",required=True)
    p.add_argument("--out",default="reports/excecoes_anotadas.csv")
    p.add_argument("--summary",default="reports/aliases_prioritarios.json")
    a=p.parse_args()
    def read(path):
        with open(path,encoding="utf-8-sig",newline="") as f:
            return list(csv.DictReader(f,delimiter=";"))
    rows,summary=summarize(read(a.matches),read(a.rsssf))
    target=Path(a.out);target.parent.mkdir(parents=True,exist_ok=True)
    with target.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=";")
        writer.writeheader();writer.writerows(rows)
    Path(a.summary).write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"registros":len(rows),"aliases_distintos":len(summary["aliases"])},ensure_ascii=False))
if __name__=="__main__":
    main()
