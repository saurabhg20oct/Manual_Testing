from __future__ import annotations

from dataclasses import dataclass

from .models import OptionLeg


@dataclass
class StrategyResult:
    spot: float
    payoff: float


def total_payoff(legs: list[OptionLeg], spot: float) -> float:
    return sum(leg.payoff(spot) for leg in legs)


def payoff_table(legs: list[OptionLeg], start: float, stop: float, step: float) -> list[StrategyResult]:
    spots = []
    current = start
    while current <= stop:
        spots.append(StrategyResult(spot=current, payoff=total_payoff(legs, current)))
        current += step
    return spots
