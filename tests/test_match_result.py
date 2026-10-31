import pytest
from loteca_fivethirtyeight.match_result import MatchResult

def test_extra_time_does_not_change_90_minutes():
    r=MatchResult(1,1,0,1,lottery_symbol="X")
    assert r.result_90=="X"
    assert r.after_extra==(1,2)
    assert r.knockout_winner=="2"

def test_penalties_not_90_result():
    r=MatchResult(1,1,0,0,3,2,lottery_symbol="X")
    assert r.result_90=="X"
    assert r.knockout_winner=="1"

def test_draw_never_eligible_without_real_result():
    r=MatchResult(lottery_symbol="1",lottery_draw=True)
    assert r.result_90 is None
    assert not r.elo_90_eligible

def test_invalid_scores():
    with pytest.raises(ValueError):
        MatchResult(1,None)
    with pytest.raises(ValueError):
        MatchResult(1,1,0,0,2,2)
    with pytest.raises(ValueError):
        MatchResult(1,0,0,0,4,3)
