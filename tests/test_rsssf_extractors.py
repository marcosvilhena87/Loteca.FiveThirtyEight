import pytest
from loteca_fivethirtyeight.rsssf_extractors import parse_lines, html_to_lines, _match_line

def test_rio_real_format():
    lines = ["Liga Rio-São Paulo 2002","Round 6","[Feb 16]",
             "Bangu          1-3  Palmeiras",
             "Jundiaí        3-0  Fluminense",
             "  [goal details]",
             "[Feb 17]","Santos         2-1  São Caetano"]
    games=parse_lines(lines,"rio_sp_2002")
    assert len(games)==3
    assert games[0]["date"]=="2002-02-16"
    assert games[0]["home"]=="Bangu"
    assert games[0]["round"]=="6"
    assert games[2]["away"]=="São Caetano"

def test_copa_groups_and_final_penalties_not_extra_game():
    lines=["Brazil - Copa dos Campeões 2002",
        "FIRST PHASE","Group A (matches in Belém)","[Jul 7]",
        "Náutico     1-1 Corinthians","Paysandu    0-0 Fluminense",
        "QUARTERFINALS","[Jul 17]",
        "Flamengo    2-1 Vitória        (played in Fortaleza)",
        "FINAL","First Leg [Jul 31] (played in Belém)",
        "Paysandu    1-2 Cruzeiro",
        "Second Leg [Aug 4] (played in Fortaleza)",
        "Cruzeiro    3-4 Paysandu       (Paysandu won 3-0 on penalties)",
        "Topscorer: Fábio Júnior (Cruzeiro), 6 goals"]
    games=parse_lines(lines,"copa_campeoes_2002")
    assert len(games)==5
    assert games[0]["round"].startswith("GROUP A")
    assert games[3]["date"]=="2002-07-31"
    assert games[4]["date"]=="2002-08-04"
    assert games[4]["home_goals"]==3
    assert games[4]["away_goals"]==4

def test_no_reconstructed_dates_and_fail_closed():
    with pytest.raises(ValueError):
        parse_lines(["Round 1","Santos 2-1 São Caetano"],"rio_sp_2002")
    with pytest.raises(ValueError):
        parse_lines([],"copa_campeoes_2002")

def test_html_text_lines():
    assert "Santos 2-1 São Caetano" in html_to_lines("<pre>Santos 2-1 São Caetano</pre>")

def test_notes_not_part_of_visitor():
    assert _match_line("Cruzeiro    3-4 Paysandu       (Paysandu won 3-0 on penalties)") == ("Cruzeiro","Paysandu",3,4)
