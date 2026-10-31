"""Cruzamento estrito de Loteca com RSSSF, sem aprovação automática do Elo.

Entrada RSSSF: CSV extraído e revisado, com colunas date,home,away,home_goals,
away_goals,competition,source_url. Nenhuma linha é inventada a partir de snippets.
"""
import argparse
import csv
import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

RSSSF_FIELDS = ("date","home","away","home_goals","away_goals","competition","source_url")
OUTPUT = ("concurso","jogo","data_loteca","mandante_loteca","visitante_loteca",
          "placar_loteca","estado","motivo","competicao","fonte_url",
          "aliases_utilizados","candidatos","elo_liberado")
# IDs explícitos: não unir homônimos nem equipes B sem autorização.
ALIASES = {
    "FLAMENGO/RJ":"flamengo_rj","FLAMENGO":"flamengo_rj",
    "VASCO DA GAMA/RJ":"vasco_rj","VASCO/RJ":"vasco_rj","VASCO DA GAMA":"vasco_rj",
    "SAO PAULO/SP":"sao_paulo_sp","S. PAULO/SP":"sao_paulo_sp","SAO PAULO":"sao_paulo_sp",
    "SANTOS/SP":"santos_sp","SANTOS":"santos_sp",
    "SAO CAETANO/SP":"sao_caetano_sp","SAO CAETANO":"sao_caetano_sp",
    "BANGU/RJ":"bangu_rj","BANGU":"bangu_rj",
    "PALMEIRAS/SP":"palmeiras_sp","PALMEIRAS":"palmeiras_sp",
    "FLUMINENSE/RJ":"fluminense_rj","FLUMINENSE":"fluminense_rj",
    "ETTI JUNDIAI/SP":"jundiai_sp","JUNDIAI":"jundiai_sp",
    "CORINTHIANS/SP":"corinthians_sp","CORINTHIANS":"corinthians_sp",
    "P. DESPORTOS/SP":"portuguesa_sp","P.  DESPORTOS/SP":"portuguesa_sp","PORTUGUESA":"portuguesa_sp",
    "NAUTICO/PE":"nautico_pe","NAUTICO":"nautico_pe",
    "PAYSANDU/PA":"paysandu_pa","PAYSANDU":"paysandu_pa",
    "GOIAS/GO":"goias_go","GOIAS":"goias_go",
    "GREMIO/RS":"gremio_rs","GREMIO":"gremio_rs",
    "CRUZEIRO/MG":"cruzeiro_mg","CRUZEIRO":"cruzeiro_mg",
    "VITORIA/BA":"vitoria_ba","VITORIA":"vitoria_ba",
    "BAHIA/BA":"bahia_ba","BAHIA":"bahia_ba",
    "ATLETICO/MG":"atletico_mg","ATLETICO-MG":"atletico_mg",
    "ATHLETICO/PR":"athletico_pr","ATLETICO/PR":"athletico_pr","ATLETICO-PR":"athletico_pr",
    "GUARANI/SP":"guarani_sp","GUARANI":"guarani_sp",
    "AMERICANO/RJ":"americano_rj","AMERICANO":"americano_rj",
    "PONTE PRETA/SP":"ponte_preta_sp","PONTE PRETA":"ponte_preta_sp",
    "BOTAFOGO/RJ":"botafogo_rj","BOTAFOGO":"botafogo_rj",
}
def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    return re.sub(r"\s+"," ","".join(c for c in s if not unicodedata.combining(c)).upper()).strip()
ALIASES = {norm(k):v for k,v in ALIASES.items()}

def date_iso(value):
    match = re.search(r"\d{2}/\d{2}/\d{4}",str(value))
    if match:
        return datetime.strptime(match.group(),"%d/%m/%Y").date().isoformat()
    return datetime.strptime(str(value).strip(),"%Y-%m-%d").date().isoformat()

def load_csv(path, fields):
    with open(path,encoding="utf-8-sig",newline="") as f:
        reader=csv.DictReader(f,delimiter=";")
        if not set(fields).issubset(reader.fieldnames or []):
            raise ValueError(f"Colunas ausentes em {path}: {set(fields)-set(reader.fieldnames or [])}")
        return list(reader)

def match_all(loteca, rsssf):
    index=defaultdict(list)
    for r in rsssf:
        try:
            d=date_iso(r["date"])
            h,a=ALIASES.get(norm(r["home"])),ALIASES.get(norm(r["away"]))
            g1,g2=int(r["home_goals"]),int(r["away_goals"])
            if min(g1,g2)<0: raise ValueError("gols negativos")
            if not r["competition"].strip() or not r["source_url"].startswith("https://"):
                continue
            if h and a and h!=a:
                index[(d,h,a,g1,g2)].append(r)
        except (ValueError,KeyError):
            continue
    seen=Counter((r["concurso"].strip(),r["jogo"].strip()) for r in loteca)
    output=[]
    for r in loteca:
        key=(r["concurso"].strip(),r["jogo"].strip())
        result=dict(concurso=key[0],jogo=key[1],data_loteca=r["data_jogo"],
                    mandante_loteca=r["equipe_1"],visitante_loteca=r["equipe_2"],
                    placar_loteca=f'{r["gols_1"]}-{r["gols_2"]}',
                    estado="pendente",motivo="",competicao="",fonte_url="",
                    aliases_utilizados="",candidatos="0",elo_liberado="nao")
        if seen[key]>1:
            result["motivo"]="chave concurso+jogo duplicada"
        elif norm(r.get("sorteio",""))=="SIM":
            result["motivo"]="sorteio loterico sem placar esportivo comprovado"
        else:
            try:
                d=date_iso(r["data_jogo"])
                h=ALIASES.get(norm(r["equipe_1"]))
                a=ALIASES.get(norm(r["equipe_2"]))
                if not h or not a or h==a:
                    result["motivo"]="alias ausente ou identidade ambigua"
                else:
                    result["aliases_utilizados"]=h+" | "+a
                    candidates=index.get((d,h,a,int(r["gols_1"]),int(r["gols_2"])),[])
                    unique={(c["competition"],c["source_url"]) for c in candidates}
                    result["candidatos"]=str(len(unique))
                    if len(unique)==1:
                        comp,url=next(iter(unique))
                        result.update(estado="confirmado",motivo="correspondencia estrita por data mando identidade placar e competicao",competicao=comp,fonte_url=url)
                    elif len(unique)>1:
                        result["motivo"]="multiplas evidencias/competicoes: revisao humana"
                    else:
                        result["motivo"]="nenhuma correspondencia estrita; revisar datas placar e fonte"
            except (ValueError,KeyError):
                result["motivo"]="data ou placar invalido"
        output.append(result)
    return output

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--loteca",required=True,help="CSV Loteca, delimitador ;")
    p.add_argument("--rsssf",required=True,help="Extracao RSSSF revisada, delimitador ;")
    p.add_argument("--output",default="reports/cruzamento_rsssf.csv")
    args=p.parse_args()
    records=match_all(load_csv(args.loteca,("concurso","jogo","data_jogo","equipe_1","equipe_2","gols_1","gols_2","sorteio")),
                      load_csv(args.rsssf,RSSSF_FIELDS))
    path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=OUTPUT,delimiter=";")
        writer.writeheader();writer.writerows(records)
    print(json.dumps(dict(Counter(r["estado"] for r in records)),ensure_ascii=False))
if __name__=="__main__":
    main()
