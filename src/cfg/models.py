from __future__ import annotations

from datetime import time
from typing import Dict, Literal

from pydantic import BaseModel, Field, validator


class EntryConfig(BaseModel):
    start_time: time = time(hour=9, minute=20)
    end_time: time = time(hour=9, minute=25)
    order_type: Literal["market", "limit"] = "market"

    @validator("end_time")
    def validate_window(cls, value: time, values: Dict[str, time]) -> time:
        start = values.get("start_time")
        if start and value <= start:
            raise ValueError("Entry end_time must be after start_time")
        return value


class FilterToggle(BaseModel):
    enabled: bool = False


class IVPercentileFilter(FilterToggle):
    min: float = 0.0
    max: float = 1.0


class IndiaVixFilter(FilterToggle):
    lookback: int = 20
    max_above_ma: float = 0.15


class OpeningRangeFilter(FilterToggle):
    duration_min: int = 15
    tolerance_pct: float = 0.3


class AtrFilter(FilterToggle):
    lookback: int = 14
    max_atr_pct: float = 0.03


class EventFilter(FilterToggle):
    calendar_csv: str = "config/events.csv"


class FiltersConfig(BaseModel):
    iv_percentile: IVPercentileFilter = Field(default_factory=IVPercentileFilter)
    india_vix: IndiaVixFilter = Field(default_factory=IndiaVixFilter)
    opening_range: OpeningRangeFilter = Field(default_factory=OpeningRangeFilter)
    atr: AtrFilter = Field(default_factory=AtrFilter)
    events: EventFilter = Field(default_factory=EventFilter)


class ReentryConfig(FilterToggle):
    max_retries: int = 0
    cooldown_min: int = 30
    reentry_trigger_pct: float = 0.5


class TrailingConfig(FilterToggle):
    trail_pct: float = 0.25


class EmergencyIVSpikeConfig(FilterToggle):
    threshold_pct: float = 0.25


class RiskConfig(BaseModel):
    combined_sl_pct: float = 0.0025
    leg_sl_pct: float = 0.3
    trailing: TrailingConfig = Field(default_factory=TrailingConfig)
    emergency_iv_spike: EmergencyIVSpikeConfig = Field(default_factory=EmergencyIVSpikeConfig)


class ExitConfig(BaseModel):
    hard_stop_time: time = time(hour=15, minute=10)
    soft_exit_time: time = time(hour=14, minute=45)
    trail_from_profit_pct: float = 0.005


class PositioningConfig(BaseModel):
    margin_cap_lots: int = 100
    liquidity_cap_lots: int = 60
    sl_pct: float = 0.3


class ReportingConfig(BaseModel):
    output_dir: str = "reports"
    enable_plots: bool = True


class ScheduleConfig(BaseModel):
    timezone: str = "Asia/Kolkata"
    backfill_days: int = 365


class StrategyConfig(BaseModel):
    name: str = "base"
    broker: Literal["paper", "kite"] = "paper"
    capital: float = 50_000_000
    risk_budget_pct: float = 0.0025
    profit_target_pct: float = 0.01
    lot_sizes: Dict[str, int] = Field(default_factory=lambda: {"NIFTY": 75, "SENSEX": 20})
    underlying: Literal["NIFTY", "SENSEX"] = "NIFTY"
    expiry_weekday: str = "Thursday"
    entry: EntryConfig = Field(default_factory=EntryConfig)
    filters: FiltersConfig = Field(default_factory=FiltersConfig)
    reentry: ReentryConfig = Field(default_factory=ReentryConfig)
    risk: RiskConfig = Field(default_factory=RiskConfig)
    exit: ExitConfig = Field(default_factory=ExitConfig)
    positioning: PositioningConfig = Field(default_factory=PositioningConfig)
    reporting: ReportingConfig = Field(default_factory=ReportingConfig)
    schedule: ScheduleConfig = Field(default_factory=ScheduleConfig)

    @property
    def risk_budget(self) -> float:
        return self.capital * self.risk_budget_pct

    @property
    def profit_target(self) -> float:
        return self.capital * self.profit_target_pct

    @property
    def lot_size(self) -> int:
        return self.lot_sizes.get(self.underlying, 0)

    def risk_budget_for_day(self) -> float:
        return self.risk_budget

    def profit_target_for_day(self) -> float:
        return self.profit_target


class ConfigBundle(BaseModel):
    config: StrategyConfig
    source_path: str
