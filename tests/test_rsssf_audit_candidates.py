from audits.rsssf.audit_candidates import audit_row
def test_vasco_independent_discrepancy():
 caixa={"concurso":"48","jogo":"1","data_jogo":"sábado, 18/01/2003","equipe_1":"VASCO DA GAMA/RJ","equipe_2":"AMERICA/RJ","gols_1":"1","gols_2":"0","sorteio":"Não"}
 aliases=[{"alias":"VASCO DA GAMA/RJ","canonical_id":"BR_RJ_VASCO","valid_from":"","valid_to":""},{"alias":"AMERICA/RJ","canonical_id":"BR_RJ_AMERICA","valid_from":"","valid_to":""}]
 sources=[{"competition":"Campeonato Carioca 2003","date":"2003-01-16","home":"Vasco da Gama","away":"América","home_goals":"1","away_goals":"0","source_url":"https://www.rsssfbrasil.com/tablesr/rj2003.htm"}]
 r=audit_row(caixa,[],sources,aliases)
 assert r["status"]=="data_rsssf_divergente_documentada"
 assert r["source_date"]=="2003-01-16" and r["data_caixa"]=="2003-01-18" and r["elo_eligible"]=="nao"
def test_no_canonical_no_elo():
 c={"concurso":"40","jogo":"1","data_jogo":"domingo, 17/11/2002","equipe_1":"TEST","equipe_2":"TEAM","gols_1":"1","gols_2":"0","sorteio":"Não"}
 m={"competition":"C","date":"2002-11-17","home":"TEST","away":"TEAM","home_goals":"1","away_goals":"0","source_url":"source"}
 cand={"competition":"C","rsssf_date":"2002-11-17","rsssf_score":"1-0","source_url":"source","home":"TEST","away":"TEAM"}
 r=audit_row(c,[cand],[m],[])
 assert r["status"]=="identidade_incompleta" and r["elo_eligible"]=="nao"
