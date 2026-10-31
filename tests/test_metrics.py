"""Testes básicos de probabilidades 1X2 e métricas."""

import math

import pytest

from loteca_fivethirtyeight import multiclass_brier, multiclass_log_loss, normalize_1x2


def test_normalization():
    assert normalize_1x2(5, 3, 2) == pytest.approx((0.5, 0.3, 0.2))


@pytest.mark.parametrize("weights", [(0, 0, 0), (-1, 2, 3), (float("nan"), 1, 1)])
def test_invalid_weights(weights):
    with pytest.raises(ValueError):
        normalize_1x2(*weights)


def test_perfect_forecast_scores_zero():
    assert multiclass_brier((1, 0, 0), 0) == 0
    assert multiclass_log_loss((1, 0, 0), 0) == 0


def test_uniform_forecast():
    probabilities = (1 / 3, 1 / 3, 1 / 3)
    assert multiclass_brier(probabilities, 1) == pytest.approx(2 / 3)
    assert multiclass_log_loss(probabilities, 1) == pytest.approx(math.log(3))


def test_zero_probability_log_loss_is_infinite():
    assert math.isinf(multiclass_log_loss((1, 0, 0), 1))


@pytest.mark.parametrize("probabilities,outcome", [
    ((0.4, 0.3, 0.2), 0),
    ((0.5, 0.5), 0),
    ((0.5, 0.3, 0.2), 3),
    ((float("nan"), 0.5, 0.5), 0),
])
def test_invalid_probabilities(probabilities, outcome):
    with pytest.raises(ValueError):
        multiclass_brier(probabilities, outcome)
