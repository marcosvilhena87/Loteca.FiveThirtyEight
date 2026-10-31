from datetime import date
from audits.rsssf.reconcile_auto import canon_source
def test_xv_distinct_by_competition():
 d=date(2002,10,5)
 assert canon_source("XV de Novembro",d,[],"Campeonato Brasileiro Série B 2002")=="BR_SP_XV_PIRACICABA"
 assert canon_source("XV de Novembro",d,[],"Campeonato Paulista Série B1 2002")=="BR_SP_XV_CARAGUATATUBA"
def test_america_distinct_by_state():
 d=date(2003,1,26)
 assert canon_source("América",d,[],"Campeonato Mineiro 2003")=="BR_MG_AMERICA"
 assert canon_source("América",d,[],"Campeonato Carioca 2003")=="BR_RJ_AMERICA"

def test_damaged_diacritic_not_global():
 d=date(2002,10,26)
 assert canon_source("Tup�",d,[],"Campeonato Paulista Série B1 2002")=="BR_SP_TUPA"
 assert canon_source("Guaratinguet�",d,[],"Campeonato Paulista Série B1 2002")=="BR_SP_GUARATINGUETA"
 assert canon_source("Tup�",d,[],"Campeonato Brasileiro Série B 2002")==""
