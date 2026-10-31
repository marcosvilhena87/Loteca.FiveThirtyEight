from loteca_fivethirtyeight.league_integrity import audit_league

def test_detects_duplicate_and_missing_teams():
    aliases=[{"competition":"La Liga","alias":"A","club_id":"A"},{"competition":"La Liga","alias":"B","club_id":"B"}]
    games=[{"competition":"La Liga","home":"A","away":"B","date":"2025-01-01"},
           {"competition":"La Liga","home":"A","away":"B","date":"2025-02-01"}]
    report,issues=audit_league(games,"La Liga",aliases)
    assert report["status"]=="QUARANTINE_STRUCTURAL"
    assert any(reason=="DUPLICATE_OR_SELF_FIXTURE" for _,reason in issues)

def test_unresolved_alias_not_accepted():
    aliases=[{"competition":"Premier League","alias":"Liverpool","club_id":"ENG-LIVERPOOL"}]
    report,issues=audit_league([{"home":"Liverpool","away":"Unknown","date":"2025-05-25"}],"Premier League",aliases)
    assert any(reason=="ALIAS_UNRESOLVED_OR_AMBIGUOUS" for _,reason in issues)
