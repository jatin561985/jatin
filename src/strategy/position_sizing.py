from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PositionSizingResult:
    lots: int
    per_lot_loss: float
    max_loss: float


def lots_allowed(
    premium: float,
    lot_size: int,
    risk_budget: float,
    sl_pct: float,
    margin_cap_lots: int,
    liq_cap_lots: int,
) -> PositionSizingResult:
    per_lot_loss = sl_pct * premium * lot_size
    risk_lots = int(risk_budget // per_lot_loss) if per_lot_loss > 0 else 0
    lots = max(0, min(risk_lots, margin_cap_lots, liq_cap_lots))
    max_loss = per_lot_loss * lots
    return PositionSizingResult(lots=lots, per_lot_loss=per_lot_loss, max_loss=max_loss)
