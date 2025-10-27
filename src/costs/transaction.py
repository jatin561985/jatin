from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CostBreakdown:
    brokerage: float
    exchange_fees: float
    sebi_charges: float
    gst: float
    stamp_duty: float

    @property
    def total(self) -> float:
        return self.brokerage + self.exchange_fees + self.sebi_charges + self.gst + self.stamp_duty


def option_transaction_cost(notional: float, trades: int = 2, brokerage_per_trade: float = 20.0) -> CostBreakdown:
    brokerage = trades * brokerage_per_trade
    exchange_fees = notional * 0.00053
    sebi_charges = notional * 0.000001
    gst = 0.18 * brokerage
    stamp_duty = notional * 0.00003
    return CostBreakdown(
        brokerage=brokerage,
        exchange_fees=exchange_fees,
        sebi_charges=sebi_charges,
        gst=gst,
        stamp_duty=stamp_duty,
    )
