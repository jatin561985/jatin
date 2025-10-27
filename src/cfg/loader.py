import sys
import yaml
from pathlib import Path
from typing import Dict, Any

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.cfg.models import BaseConfig

def load_config(strategy_config_path: Path) -> BaseConfig:
    """
    Loads and validates the configuration from YAML files.

    Args:
        strategy_config_path: Path to the strategy-specific YAML file.

    Returns:
        A validated BaseConfig object.
    """
    base_config_path = Path("config/base.yaml")

    with open(base_config_path, "r") as f:
        base_config_dict = yaml.safe_load(f)

    with open(strategy_config_path, "r") as f:
        strategy_config_dict = yaml.safe_load(f)

    # A simple merge, strategy config overrides base for overlapping keys
    # A more sophisticated deep merge could be used if needed
    merged_config_dict: Dict[str, Any] = {**base_config_dict, **strategy_config_dict}

    return BaseConfig(**merged_config_dict)

if __name__ == "__main__":
    # Example usage:
    nifty_config_path = Path("config/nifty_tuesday.yaml")
    # To make this runnable, we need to create some dummy content for the yaml files
    # This is just for demonstration purposes
    dummy_base_content = """
capital: 50000000
daily_risk_budget_percent: 0.25
profit_target_percent: 1.0
"""
    dummy_nifty_content = """
strategies:
  - underlying: "NIFTY"
    lot_size: 75
    entry_window:
      start: "09:20"
      end: "09:25"
    filters:
      iv_percentile_min: 0.0
      iv_percentile_max: 100.0
      india_vix_ma_filter: false
      opening_range_bound_check: true
      atr_percent_threshold: 1.0
      avoid_major_events: true
    re_entry:
      enabled: true
      max_re_entries: 2
      return_to_sl_percent: 50.0
      range_re_compression: false
    exits:
      hard_mtm_stop_loss_percent: 100.0 # This will be the daily risk budget
      per_leg_sl_percent: 70.0
      combined_premium_sl: false
      trailing_stop_enabled: true
      time_based_exit_before: "15:10"
      emergency_iv_spike_threshold: 5.0
      orb_atr_breakout_flat: true
"""
    with open("config/base.yaml", "w") as f:
        f.write(dummy_base_content)
    with open("config/nifty_tuesday.yaml", "w") as f:
        f.write(dummy_nifty_content)

    config = load_config(nifty_config_path)
    print(config.model_dump_json(indent=2))
