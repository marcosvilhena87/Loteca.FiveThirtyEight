from audits.rsssf.reconcile_auto import norm,date,canon,run
def test_norm():assert norm("São  Caetano/SP")=="SAO CAETANO SP"
def test_date():assert date("domingo, 08/09/2002").isoformat()=="2002-09-08"
def test_temporal():
 a=[{"alias":"ETTI","canonical_id":"X","valid_from":"2000-01-01","valid_to":"2002-12-31"}]
 assert canon("ETTI",date("08/09/2002"),a)=="X"
 assert canon("ETTI",date("08/09/2003"),a)==""
def test_draw():
 c=[{"concurso":"43","jogo":"1","data_jogo":"","equipe_1":"A","equipe_2":"B","gols_1":"1","gols_2":"0","sorteio":"SIM"}]
 assert run(c,[],[])[0]["status"]=="sorteio_bloqueado"
def test_multiple():
 c=[{"concurso":"32","jogo":"1","data_jogo":"08/09/2002","equipe_1":"A","equipe_2":"B","gols_1":"2","gols_2":"0","sorteio":"Não"}]
 m={"date":"08/09/2002","home":"A","away":"B","home_goals":"2","away_goals":"0","competition":"L","source_url":"https://rsssf.org/x"}
 assert run(c,[m,m],[])[0]["status"]=="multiplos_candidatos_revisao"
