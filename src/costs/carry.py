from __future__ import annotations


def funding_cost(notional: float, annual_rate: float = 0.07, days: int = 1) -> float:
    return notional * annual_rate * days / 365
