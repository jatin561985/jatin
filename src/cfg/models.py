from pydantic import BaseModel
from typing import List, Optional

class EntryWindow(BaseModel):
    start: str
    end: str

class Filters(BaseModel):
    iv_percentile_min: float
    iv_percentile_max: float
    india_vix_ma_filter: bool
    opening_range_bound_check: bool
    atr_percent_threshold: float
    avoid_major_events: bool

class ReEntry(BaseModel):
    enabled: bool
    max_re_entries: int
    return_to_sl_percent: float
    range_re_compression: bool

class Exits(BaseModel):
    hard_mtm_stop_loss_percent: float
    per_leg_sl_percent: float
    combined_premium_sl: bool
    trailing_stop_enabled: bool
    time_based_exit_before: str
    emergency_iv_spike_threshold: float
    orb_atr_breakout_flat: bool

class StrategyConfig(BaseModel):
    underlying: str
    lot_size: int
    entry_window: EntryWindow
    filters: Filters
    re_entry: ReEntry
    exits: Exits

class BaseConfig(BaseModel):
    capital: float
    daily_risk_budget_percent: float
    profit_target_percent: float
    strategies: List[StrategyConfig]
