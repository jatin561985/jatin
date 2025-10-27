from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional

import pandas as pd

from .position_sizing import PositionSizingResult, lots_allowed


@dataclass(slots=True)
class OptionLeg:
    symbol: str
    strike: float
    option_type: str
    entry_price: float
    lot_size: int
    lots: int
    sl_pct: float
    current_price: float
    stop_loss_price: float = field(init=False)
    exit_price: Optional[float] = None
    active: bool = True

    def __post_init__(self) -> None:
        self.stop_loss_price = self.entry_price * (1 + self.sl_pct)

    @property
    def quantity(self) -> int:
        return -self.lots * self.lot_size

    def update_price(self, price: float) -> None:
        self.current_price = price
        if price >= self.stop_loss_price:
            self.exit_price = self.stop_loss_price
            self.active = False

    def mtm(self) -> float:
        price = self.exit_price if self.exit_price is not None else self.current_price
        return (self.entry_price - price) * self.lot_size * self.lots

    def mark_exit(self, price: float) -> None:
        self.exit_price = price
        self.active = False


@dataclass
class StraddlePosition:
    ce: OptionLeg
    pe: OptionLeg
    sizing: PositionSizingResult
    combined_stop_loss: float
    combined_trailing_pct: float
    profit_target: float
    mtm_history: list[float] = field(default_factory=list)
    closed: bool = False

    def update_prices(self, ce_price: float, pe_price: float) -> None:
        if not self.closed:
            self.ce.update_price(ce_price)
            self.pe.update_price(pe_price)
            self.mtm_history.append(self.mtm())
            self._check_rules()

    def mtm(self) -> float:
        return self.ce.mtm() + self.pe.mtm()

    def _check_rules(self) -> None:
        if self.closed:
            return
        combined_loss = -min(0.0, self.mtm())
        if combined_loss >= self.combined_stop_loss:
            self.close(self.ce.current_price, self.pe.current_price)
            return
        if self.mtm() >= self.profit_target:
            self.close(self.ce.current_price, self.pe.current_price)
            return
        if self.combined_trailing_pct > 0 and self.mtm_history:
            peak = max(self.mtm_history)
            if peak > 0 and self.mtm() <= peak * (1 - self.combined_trailing_pct):
                self.close(self.ce.current_price, self.pe.current_price)

    def close(self, ce_price: float, pe_price: float) -> None:
        if self.closed:
            return
        self.ce.mark_exit(ce_price)
        self.pe.mark_exit(pe_price)
        self.closed = True

    def to_dict(self) -> Dict[str, float]:
        return {
            "ce_entry": self.ce.entry_price,
            "pe_entry": self.pe.entry_price,
            "ce_exit": self.ce.exit_price or self.ce.current_price,
            "pe_exit": self.pe.exit_price or self.pe.current_price,
            "mtm": self.mtm(),
            "lots": self.ce.lots,
        }


class StraddleBuilder:
    def __init__(self, config, option_chain: pd.DataFrame) -> None:
        self.config = config
        self.option_chain = option_chain

    def build(self, underlying_price: float) -> Optional[StraddlePosition]:
        strike = self._find_atm_strike(underlying_price)
        if strike is None:
            return None
        ce_row = self._select_option(strike, "CE")
        pe_row = self._select_option(strike, "PE")
        if ce_row is None or pe_row is None:
            return None
        premium = ce_row["last_price"] + pe_row["last_price"]
        sizing = lots_allowed(
            premium=premium,
            lot_size=self.config.lot_size,
            risk_budget=self.config.risk_budget_for_day(),
            sl_pct=self.config.positioning.sl_pct,
            margin_cap_lots=self.config.positioning.margin_cap_lots,
            liq_cap_lots=self.config.positioning.liquidity_cap_lots,
        )
        if sizing.lots <= 0:
            return None
        ce_leg = OptionLeg(
            symbol=f"{self.config.underlying}{strike}CE",
            strike=strike,
            option_type="CE",
            entry_price=float(ce_row["last_price"]),
            lot_size=self.config.lot_size,
            lots=sizing.lots,
            sl_pct=self.config.positioning.sl_pct,
            current_price=float(ce_row["last_price"]),
        )
        pe_leg = OptionLeg(
            symbol=f"{self.config.underlying}{strike}PE",
            strike=strike,
            option_type="PE",
            entry_price=float(pe_row["last_price"]),
            lot_size=self.config.lot_size,
            lots=sizing.lots,
            sl_pct=self.config.positioning.sl_pct,
            current_price=float(pe_row["last_price"]),
        )
        combined_sl = min(
            self.config.risk_budget_for_day(),
            self.config.capital * self.config.risk.combined_sl_pct,
        )
        trailing_pct = self.config.risk.trailing.trail_pct if self.config.risk.trailing.enabled else 0.0
        return StraddlePosition(
            ce=ce_leg,
            pe=pe_leg,
            sizing=sizing,
            combined_stop_loss=combined_sl,
            combined_trailing_pct=trailing_pct,
            profit_target=self.config.profit_target_for_day(),
        )

    def _find_atm_strike(self, underlying: float) -> Optional[float]:
        strikes = self.option_chain["strike"].dropna().unique()
        if len(strikes) == 0:
            return None
        strike = min(strikes, key=lambda s: abs(s - underlying))
        return strike

    def _select_option(self, strike: float, option_type: str) -> Optional[pd.Series]:
        mask = (self.option_chain["strike"] == strike) & (self.option_chain["type"] == option_type)
        if not mask.any():
            return None
        row = self.option_chain.loc[mask].iloc[0]
        return row
