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
          "aliases_utilizados","candidatos","elo_liberado","categoria_excecao","detalhes_excecao")
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
    """Classifica evidências sem inventar a competição do registro Loteca.

    Divergência de placar só é apontada para mesma data e mesmas equipes.
    Divergência de data só é apontada para mesmas equipes e mesmo placar,
    exigindo ocorrência única. Sem fixture correspondente, trata-se de
    partida fora do escopo das fontes carregadas, não de erro no CSV.
    """
    exact=defaultdict(list)
    by_fixture=defaultdict(list)
    by_date_fixture=defaultdict(list)
    by_fixture_score=defaultdict(list)
    for src in rsssf:
        try:
            d=date_iso(src["date"])
            h,a=ALIASES.get(norm(src["home"])),ALIASES.get(norm(src["away"]))
            hg,ag=int(src["home_goals"]),int(src["away_goals"])
            comp=src["competition"].strip()
            url=src["source_url"].strip()
            if min(hg,ag)<0 or not (h and a) or h==a or not comp or not url.startswith("https://"):
                continue
        except (ValueError,KeyError,TypeError):
            continue
        record=(d,h,a,hg,ag,comp,url)
        exact[(d,h,a,hg,ag)].append(record)
        by_fixture[(h,a)].append(record)
        by_date_fixture[(d,h,a)].append(record)
        by_fixture_score[(h,a,hg,ag)].append(record)
    seen=Counter((r["concurso"].strip(),r["jogo"].strip()) for r in loteca)
    output=[]
    for r in loteca:
        key=(r["concurso"].strip(),r["jogo"].strip())
        result=dict(concurso=key[0],jogo=key[1],data_loteca=r["data_jogo"],
                    mandante_loteca=r["equipe_1"],visitante_loteca=r["equipe_2"],
                    placar_loteca=f'{r["gols_1"]}-{r["gols_2"]}',
                    estado="pendente",motivo="",competicao="",fonte_url="",
                    aliases_utilizados="",candidatos="0",elo_liberado="nao",
                    categoria_excecao="",detalhes_excecao="")
        def fail(category,detail):
            result["categoria_excecao"]=category
            result["motivo"]=detail
            result["detalhes_excecao"]=detail
        if seen[key]>1:
            fail("duplicidade","chave concurso+jogo duplicada")
        elif norm(r.get("sorteio",""))=="SIM":
            fail("sorteio","sorteio loterico sem resultado esportivo comprovado")
        else:
            try:
                d=date_iso(r["data_jogo"])
                hg,ag=int(r["gols_1"]),int(r["gols_2"])
                if min(hg,ag)<0:
                    raise ValueError("placar negativo")
                h=ALIASES.get(norm(r["equipe_1"]))
                a=ALIASES.get(norm(r["equipe_2"]))
                if not h or not a:
                    missing=[x for x,ident in ((r["equipe_1"],h),(r["equipe_2"],a)) if not ident]
                    fail("alias_ausente","alias nao cadastrado: "+", ".join(missing))
                elif h==a:
                    fail("identidade_ambigua","mandante e visitante resolvem para mesma entidade")
                else:
                    result["aliases_utilizados"]=h+" | "+a
                    matches=exact.get((d,h,a,hg,ag),[])
                    comps={x[5] for x in matches}
                    result["candidatos"]=str(len(matches))
                    if len(comps)>1:
                        fail("conflito_fontes","mesma partida atribuida a multiplas competicoes: "+", ".join(sorted(comps)))
                    elif matches:
                        # Fontes redundantes da mesma competição não geram conflito.
                        result.update(estado="confirmado",motivo="correspondencia estrita por data mando identidade placar e competicao",
                                      competicao=next(iter(comps)),fonte_url=sorted(x[6] for x in matches)[0])
                    else:
                        same_day=by_date_fixture.get((d,h,a),[])
                        same_score=[x for x in by_fixture_score.get((h,a,hg,ag),[]) if x[0][:4]==d[:4]]
                        known=[x for x in by_fixture.get((h,a),[]) if x[0][:4]==d[:4]]
                        if same_day and len({x[5] for x in same_day})>1:
                            fail("conflito_fontes","fontes divergem sobre competicao do mesmo confronto e data")
                        elif same_day:
                            scores=sorted({f"{x[3]}-{x[4]}" for x in same_day})
                            fail("divergencia_placar","mesma data e equipes com placar diferente: "+", ".join(scores))
                            result["competicao"]=same_day[0][5]
                            result["fonte_url"]=same_day[0][6]
                        elif len({(x[0],x[5]) for x in same_score})==1 and same_score:
                            fail("divergencia_data","mesmas equipes e placar com data diferente: "+same_score[0][0])
                            result["competicao"]=same_score[0][5]
                            result["fonte_url"]=same_score[0][6]
                        elif same_score:
                            fail("conflito_fontes","multiplas datas ou competicoes possiveis para mesmo confronto e placar")
                        elif known:
                            fail("revisao_humana","equipes identificadas em outros encontros, sem correspondencia segura de data ou placar")
                        else:
                            fail("fora_escopo","confronto nao encontrado nas competicoes RSSSF carregadas")
            except (ValueError,KeyError,TypeError):
                fail("entrada_invalida","data ou placar invalido")
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
