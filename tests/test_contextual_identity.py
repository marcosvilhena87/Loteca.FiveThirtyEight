from loteca_fivethirtyeight.contextual_identity import contextual_candidates
from loteca_fivethirtyeight.club_identity import Club

R=[Club("BRA-SP-SANTOS","BRA","SP","SANTOS",2002,2026),
   Club("BRA-RJ-BARCELONA","BRA","RJ","BARCELONA",2002,2026),
   Club("BRA-SP-BARCELONA","BRA","SP","BARCELONA",2002,2026)]
G={"concurso":"1","jogo":"1","equipe_1":"BARCELONA","equipe_2":"SANTOS/SP","gols_1":"2","gols_2":"1","data_jogo":"17/02/2025"}
REF={"home":"Barcelona/SP","away":"Santos/SP","goals_home":"2","goals_away":"1","date":"2025-02-17","category":"PRINCIPAL","competition":"Copa","url":"https://rsssf.org/test","line":2}

def test_context_keeps_homonym_as_review_only():
    assert next(contextual_candidates([G],[REF],R))["status"]=="CANDIDATO_CONTEXTO_REVISAR"

def test_context_must_match_date():
    r=R
    ref=dict(REF,date="2025-02-18")
    assert next(contextual_candidates([G],[ref],r))["status"]=="QUARENTENA"

def test_context_must_match_score():
    r=R
    ref=dict(REF,goals_home="3")
    assert next(contextual_candidates([G],[ref],r))["status"]=="QUARENTENA"

def test_context_evidence_is_only_candidate():
    r=R
    result=next(contextual_candidates([G],[REF],r))
    assert result["status"]=="CANDIDATO_CONTEXTO_REVISAR"
    assert result["candidate_id"]=="BRA-SP-BARCELONA"

def test_without_competition_does_not_propose():
    r=R
    assert next(contextual_candidates([G],[dict(REF,competition="")],r))["status"]=="QUARENTENA"
