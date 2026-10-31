from audits.rsssf.diagnose_missing import classify
def test_alias_missing_when_no_sources():
 c={"data_jogo":"domingo, 08/09/2002","equipe_1":"ABC","equipe_2":"XYZ","gols_1":"1","gols_2":"2"}
 assert classify(c,[],[])[0]=="alias_ausente_ou_nao_coberto"
def test_score_mismatch():
 c={"data_jogo":"domingo, 08/09/2002","equipe_1":"Flamengo","equipe_2":"Bahia","gols_1":"1","gols_2":"2"}
 s=[{"date":"2002-09-08","home":"Flamengo","away":"Bahia","home_goals":"1","away_goals":"1","source_url":"https://www.rsssf.org/x"}]
 assert classify(c,s,[])[0]=="divergencia_placar_possivel"
def test_date_mismatch():
 c={"data_jogo":"domingo, 08/09/2002","equipe_1":"Flamengo","equipe_2":"Bahia","gols_1":"1","gols_2":"2"}
 s=[{"date":"2002-09-11","home":"Flamengo","away":"Bahia","home_goals":"1","away_goals":"2","source_url":"https://www.rsssf.org/x"}]
 assert classify(c,s,[])[0]=="divergencia_data_possivel"
