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

def test_rio_semifinals_and_finals_real_format():
    lines = ["Round 15", "[Apr 14]", "Flamengo 2-1 Jundiaí",
        "Semi-Finals", "[Apr 20 and 28]",
        "São Caetano    1-1   1-3  Corinthians",
        "[Apr 21 and 27]", "São Paulo      1-1   2-2  Palmeiras",
        "Finals", "[May 5 and 12]",
        "São Paulo      2-3   1-1  Corinthians"]
    games = parse_lines(lines, "rio_sp_2002")
    assert len(games) == 7
    assert [(g["date"],g["home"],g["away"],g["home_goals"],g["away_goals"]) for g in games[-6:]] == [
        ("2002-04-20","São Caetano","Corinthians",1,1),
        ("2002-04-28","Corinthians","São Caetano",3,1),
        ("2002-04-21","São Paulo","Palmeiras",1,1),
        ("2002-04-27","Palmeiras","São Paulo",2,2),
        ("2002-05-05","São Paulo","Corinthians",2,3),
        ("2002-05-12","Corinthians","São Paulo",1,1)]

def test_sul_minas_with_postponed_and_awarded_match():
    lines=["Liga Sul-Minas 2002","Round 12","[Mar 24]",
           "Cruzeiro       2-0  Grêmio",
           "Moved Match","[Apr 3]","Atlético-PR    1-1  Tubarão",
           "Round 14","[Apr 6]",
           "Atlético-MG    awd  Pelotas [abandoned at 70' in 2-2, awarded 1-0]",
           "Semi-Finals","[Apr 20 and 27]",
           "Grêmio         1-5   1-1  Atlético-PR",
           "[Apr 21 and 28]",
           "Atlético-MG    1-1   1-1  Cruzeiro       [pen 2-4]",
           "Finals","[May 5 and 12]",
           "Atlético-PR    1-2   0-1  Cruzeiro"]
    records=parse_lines(lines,"sul_minas_2002")
    assert len(records)==8
    assert records[0]["date"]=="2002-03-24"
    assert records[0]["home"]=="Cruzeiro"
    assert records[0]["home_goals"]==2
    assert any(r["round"]=="Adiada" for r in records)
    assert not any(r["away"]=="Pelotas" for r in records)
    assert records[-1]["home"]=="Cruzeiro"
    assert records[-1]["away"]=="Atlético-PR"
