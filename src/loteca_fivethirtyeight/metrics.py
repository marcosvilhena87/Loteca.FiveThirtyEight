"""Probabilidades 1X2 e métricas por partida.

Índices dos resultados: 0 = vitória do mandante (1);
1 = empate (X); 2 = vitória do visitante (2).
"""

import math
from typing import Sequence


def normalize_1x2(home: float, draw: float, away: float) -> tuple[float, float, float]:
    """Normaliza três pesos não negativos em probabilidades que somam 1."""
    weights = (float(home), float(draw), float(away))
    if not all(math.isfinite(weight) and weight >= 0 for weight in weights):
        raise ValueError("Os pesos devem ser finitos e não negativos.")
    total = sum(weights)
    if total <= 0:
        raise ValueError("A soma dos pesos deve ser positiva.")
    return tuple(weight / total for weight in weights)


def _validated(probabilities: Sequence[float], outcome: int) -> tuple[float, float, float]:
    if len(probabilities) != 3:
        raise ValueError("São necessárias exatamente três probabilidades.")
    values = tuple(float(p) for p in probabilities)
    if not all(math.isfinite(p) and 0 <= p <= 1 for p in values):
        raise ValueError("Probabilidades devem estar entre 0 e 1 e ser finitas.")
    if not math.isclose(sum(values), 1.0, rel_tol=0.0, abs_tol=1e-9):
        raise ValueError("As probabilidades devem somar 1.")
    if type(outcome) is not int or outcome not in (0, 1, 2):
        raise ValueError("O resultado deve ser 0, 1 ou 2.")
    return values


def multiclass_brier(probabilities: Sequence[float], outcome: int) -> float:
    """Brier multiclasses: soma dos três erros quadráticos (escala de 0 a 2)."""
    values = _validated(probabilities, outcome)
    return sum((p - float(index == outcome)) ** 2 for index, p in enumerate(values))


def multiclass_log_loss(probabilities: Sequence[float], outcome: int) -> float:
    """Log loss da classe observada; probabilidade zero retorna infinito."""
    values = _validated(probabilities, outcome)
    probability = values[outcome]
    return -math.log(probability) if probability > 0 else math.inf
