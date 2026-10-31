from loteca_fivethirtyeight.club_identity import Club, resolve
from loteca_fivethirtyeight.contextual_identity import contextual_candidates

REGISTRY = [
    Club("ESP-BARCELONA", "ESP", "", "BARCELONA", 2000, 2030),
    Club("ECU-BARCELONA", "ECU", "", "BARCELONA", 2000, 2030),
    Club("BRA-SP-SANTOS", "BRA", "SP", "SANTOS", 2000, 2030),
    Club("BRA-SP-BARCELONA", "BRA", "SP", "BARCELONA", 2000, 2030),
    Club("BRA-RJ-BARCELONA", "BRA", "RJ", "BARCELONA", 2000, 2030),
]
GAME = dict(concurso="1", jogo="1", equipe_1="BARCELONA", equipe_2="SANTOS/SP",
            gols_1="2", gols_2="1", data_jogo="17/02/2025")
REF = dict(home="Barcelona/SP", away="Santos/SP", goals_home="2",
           goals_away="1", date="2025-02-17", category="PRINCIPAL",
           competition="Copa", url="https://rsssf.org/sample", line=2)

def test_international_homonym_requires_trusted_country():
    assert resolve("BARCELONA", 2025, REGISTRY) is None
    assert resolve("BARCELONA", 2025, REGISTRY, country="ESP") == "ESP-BARCELONA"
    assert resolve("BARCELONA", 2025, REGISTRY, country="ECU") == "ECU-BARCELONA"

def test_region_and_country_conflict_is_rejected():
    assert resolve("BARCELONA/SP", 2025, REGISTRY, region="RJ") is None
    assert resolve("BARCELONA/SP", 2025, REGISTRY, country="ESP") is None

def test_category_separation():
    rows = [Club("A", "BRA", "SP", "TESTE", 2020, 2026),
            Club("B", "BRA", "SP", "TESTE", 2020, 2026, "SUB-20")]
    assert resolve("TESTE/SP", 2025, rows) == "A"
    assert resolve("TESTE/SP", 2025, rows, category="SUB-20") == "B"

def test_competition_scoped_record_not_global():
    rows = [Club("A", "BRA", "SP", "TESTE", 2020, 2026, competition="Copa")]
    assert resolve("TESTE/SP", 2025, rows) is None
    assert resolve("TESTE/SP", 2025, rows, competition="Copa") == "A"

def test_duplicate_documentary_hypotheses_quarantined():
    first = dict(REF)
    second = dict(REF, line=3)
    result = next(contextual_candidates([GAME], [first, second], REGISTRY))
    assert result["status"] == "AMBIGUO_CONTEXTO"
    assert result["candidate_id"] == ""
    assert result["matching_sources"] == 2

def test_identical_repeated_record_is_deduplicated():
    result = next(contextual_candidates([GAME], [REF, dict(REF)], REGISTRY))
    assert result["status"] == "CANDIDATO_CONTEXTO_REVISAR"
    assert result["matching_sources"] == 1

def test_youth_fixture_never_proposed_as_main_team():
    game = dict(GAME, categoria="SUB-20")
    result = next(contextual_candidates([game], [REF], REGISTRY))
    assert result["status"] == "QUARENTENA"

def test_missing_documentary_line_quarantined():
    ref = dict(REF)
    ref.pop("line")
    assert next(contextual_candidates([GAME], [ref], REGISTRY))["status"] == "QUARENTENA"
