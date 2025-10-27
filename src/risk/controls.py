from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time
from typing import Optional

from loguru import logger


@dataclass
class RiskState:
    combined_sl_hit: bool = False
    profit_target_hit: bool = False
    emergency_exit: bool = False
    reason: Optional[str] = None


class RiskManager:
    def __init__(self, config) -> None:
        self.config = config
        self.state = RiskState()

    def should_halt_for_time(self, now: datetime) -> bool:
        hard_stop = self.config.exit.hard_stop_time
        return now.time() >= hard_stop

    def should_emergency_exit(self, iv_spike_pct: float) -> bool:
        if not self.config.risk.emergency_iv_spike.enabled:
            return False
        threshold = self.config.risk.emergency_iv_spike.threshold_pct
        if iv_spike_pct >= threshold:
            self.state.emergency_exit = True
            self.state.reason = f"IV spike {iv_spike_pct:.2%} above threshold"
            logger.warning(self.state.reason)
            return True
        return False

    def check_mtm(self, mtm: float) -> None:
        if mtm <= -self.config.risk_budget_for_day():
            self.state.combined_sl_hit = True
            self.state.reason = "Combined MTM stop loss"
        if mtm >= self.config.profit_target_for_day():
            self.state.profit_target_hit = True
            self.state.reason = "Profit target reached"

    def should_exit_positions(self) -> bool:
        return any([self.state.combined_sl_hit, self.state.profit_target_hit, self.state.emergency_exit])

    def reset_intraday(self) -> None:
        self.state = RiskState()
