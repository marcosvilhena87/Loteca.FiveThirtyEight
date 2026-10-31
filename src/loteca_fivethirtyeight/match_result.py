"""Representa resultado lotérico, 90 minutos, prorrogação e pênaltis separadamente.

Não deduz placares esportivos a partir de resultados sorteados.
"""
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class MatchResult:
    home_90: Optional[int] = None
    away_90: Optional[int] = None
    home_extra: Optional[int] = None
    away_extra: Optional[int] = None
    home_penalties: Optional[int] = None
    away_penalties: Optional[int] = None
    lottery_symbol: Optional[str] = None
    lottery_draw: bool = False

    def __post_init__(self):
        nums = (self.home_90, self.away_90, self.home_extra,
                self.away_extra, self.home_penalties, self.away_penalties)
        if any(v is not None and (type(v) is not int or v < 0) for v in nums):
            raise ValueError("Gols e penaltis devem ser inteiros nao negativos")
        for left,right in ((self.home_90,self.away_90),
                           (self.home_extra,self.away_extra),
                           (self.home_penalties,self.away_penalties)):
            if (left is None) != (right is None):
                raise ValueError("Placar incompleto")
        if self.home_extra is not None and self.home_90 is None:
            raise ValueError("Prorrogacao sem tempo normal")
        if self.home_penalties is not None:
            if self.home_90 is None:
                raise ValueError("Penaltis sem jogo")
            h,a=self.after_extra
            if h != a or self.home_penalties == self.away_penalties:
                raise ValueError("Penaltis exigem empate anterior e vencedor")
        if self.lottery_symbol not in (None, "1", "X", "2"):
            raise ValueError("Sinal loterico invalido")

    @property
    def after_extra(self):
        if self.home_90 is None:
            return None
        return (self.home_90 + (self.home_extra or 0),
                self.away_90 + (self.away_extra or 0))

    @property
    def result_90(self):
        if self.home_90 is None:
            return None
        return "1" if self.home_90 > self.away_90 else ("2" if self.home_90 < self.away_90 else "X")

    @property
    def knockout_winner(self):
        if self.home_90 is None:
            return None
        if self.home_penalties is not None:
            return "1" if self.home_penalties > self.away_penalties else "2"
        h,a=self.after_extra
        return "1" if h>a else ("2" if h<a else None)

    @property
    def elo_90_eligible(self):
        return not self.lottery_draw and self.result_90 is not None
