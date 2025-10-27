from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time
from typing import Optional

import pandas as pd
from loguru import logger

from ..costs import option_transaction_cost
from ..risk import RiskManager
from ..strategy import FilterInputs, StraddleBuilder, StrategyFilters


@dataclass
class BacktestResult:
    pnl: float
    gross: float
    costs: float
    trades: int
    mtm_series: pd.Series


class OptionPriceSimulator:
    def __init__(self, ce_entry: float, pe_entry: float, strike: float, entry_underlying: float) -> None:
        self.ce_entry = ce_entry
        self.pe_entry = pe_entry
        self.strike = strike
        self.entry_underlying = entry_underlying

    def ce_price(self, underlying: float) -> float:
        delta = 0.5
        intrinsic = max(0.0, underlying - self.strike)
        theo = max(0.5, self.ce_entry + delta * (underlying - self.entry_underlying))
        return max(intrinsic, theo)

    def pe_price(self, underlying: float) -> float:
        delta = 0.5
        intrinsic = max(0.0, self.strike - underlying)
        theo = max(0.5, self.pe_entry - delta * (underlying - self.entry_underlying))
        return max(intrinsic, theo)


class BacktestEngine:
    def __init__(
        self,
        config,
        underlying: pd.DataFrame,
        option_chain: pd.DataFrame,
        vix: Optional[pd.Series] = None,
        iv_history: Optional[pd.Series] = None,
    ) -> None:
        self.config = config
        self.underlying = underlying
        self.option_chain = option_chain
        self.vix = vix
        self.iv_history = iv_history
        self.filters = StrategyFilters(config)
        self.risk_manager = RiskManager(config)

    def run(self) -> BacktestResult:
        entry_window = self._entry_window()
        minute_data = self.underlying.between_time(entry_window[0], entry_window[1])
        if minute_data.empty:
            raise ValueError("No data available in entry window")
        entry_timestamp = minute_data.index[0]
        if not self._filters_pass(entry_timestamp):
            logger.info("Filters rejected trade on %s", entry_timestamp.date())
            return BacktestResult(pnl=0.0, gross=0.0, costs=0.0, trades=0, mtm_series=pd.Series(dtype=float))
        underlying_entry = minute_data.iloc[0]["close"]
        builder = StraddleBuilder(self.config, self.option_chain)
        position = builder.build(underlying_entry)
        if position is None:
            logger.warning("Unable to build position")
            return BacktestResult(pnl=0.0, gross=0.0, costs=0.0, trades=0, mtm_series=pd.Series(dtype=float))
        simulator = OptionPriceSimulator(
            ce_entry=position.ce.entry_price,
            pe_entry=position.pe.entry_price,
            strike=position.ce.strike,
            entry_underlying=underlying_entry,
        )
        mtm_records: list[tuple[pd.Timestamp, float]] = []
        for ts, row in self.underlying.iterrows():
            if ts < entry_timestamp:
                continue
            ce_price = simulator.ce_price(row["close"])
            pe_price = simulator.pe_price(row["close"])
            position.update_prices(ce_price, pe_price)
            mtm_records.append((ts, position.mtm()))
            self.risk_manager.check_mtm(position.mtm())
            if self._should_exit(ts) or self.risk_manager.should_exit_positions():
                position.close(ce_price, pe_price)
                break
        mtm_series = pd.Series({ts: pnl for ts, pnl in mtm_records})
        notional = (position.ce.entry_price + position.pe.entry_price) * position.ce.lot_size * position.ce.lots
        costs = option_transaction_cost(notional).total
        pnl = position.mtm() - costs
        return BacktestResult(
            pnl=pnl,
            gross=position.mtm(),
            costs=costs,
            trades=1,
            mtm_series=mtm_series,
        )

    def _entry_window(self) -> tuple[time, time]:
        return self.config.entry.start_time, self.config.entry.end_time

    def _filters_pass(self, timestamp: pd.Timestamp) -> bool:
        inputs = FilterInputs(
            underlying=self.underlying.loc[:timestamp],
            option_chain=self.option_chain,
            vix=self.vix,
            iv_history=self.iv_history,
            events_path=self.config.filters.events.calendar_csv,
            timestamp=timestamp,
        )
        return self.filters.passes(inputs)

    def _should_exit(self, ts: pd.Timestamp) -> bool:
        if ts.time() >= self.config.exit.soft_exit_time:
            logger.info("Soft exit time reached")
            return True
        if self.risk_manager.should_halt_for_time(datetime.combine(ts.date(), ts.time())):
            logger.info("Hard stop time reached")
            return True
        return False
