from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd

from ..features import atr_percent, india_vix_filter, iv_percentile, opening_range_deviation


@dataclass
class FilterInputs:
    underlying: pd.DataFrame
    option_chain: pd.DataFrame
    vix: Optional[pd.Series] = None
    iv_history: Optional[pd.Series] = None
    events_path: Optional[str] = None
    timestamp: Optional[pd.Timestamp] = None


class StrategyFilters:
    def __init__(self, config) -> None:
        self.config = config

    def passes(self, inputs: FilterInputs) -> bool:
        cfg = self.config.filters
        if cfg.events.enabled and inputs.timestamp is not None and inputs.events_path:
            if self._is_event_day(inputs.timestamp, inputs.events_path):
                return False
        if cfg.iv_percentile.enabled and inputs.iv_history is not None:
            current_iv = inputs.option_chain["iv"].dropna()
            if not current_iv.empty:
                hist = pd.concat([inputs.iv_history, current_iv])
                percentile = iv_percentile(hist).iloc[-1]
                if percentile < cfg.iv_percentile.min or percentile > cfg.iv_percentile.max:
                    return False
        if cfg.india_vix.enabled and inputs.vix is not None:
            vix_dev = india_vix_filter(inputs.vix, lookback=cfg.india_vix.lookback).iloc[-1]
            if vix_dev > cfg.india_vix.max_above_ma:
                return False
        if cfg.opening_range.enabled:
            deviation = opening_range_deviation(
                inputs.underlying,
                duration_min=cfg.opening_range.duration_min,
            ).iloc[-1]
            if abs(deviation) > cfg.opening_range.tolerance_pct:
                return False
        if cfg.atr.enabled:
            atr_pct = atr_percent(inputs.underlying, lookback=cfg.atr.lookback).iloc[-1]
            if atr_pct > cfg.atr.max_atr_pct:
                return False
        return True

    @staticmethod
    def _is_event_day(ts: pd.Timestamp, events_path: str) -> bool:
        path = Path(events_path)
        if not path.exists():
            return False
        events = pd.read_csv(path, parse_dates=["date"])
        return ts.normalize() in events["date"].dt.normalize().tolist()
