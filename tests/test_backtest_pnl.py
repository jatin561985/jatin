import numpy as np
import pandas as pd

from src.backtest import BacktestEngine
from src.cfg import load_config


def _synthetic_config(tmp_path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
name: test
broker: paper
capital: 1000000
risk_budget_pct: 0.01
profit_target_pct: 0.02
lot_sizes:
  NIFTY: 75
underlying: NIFTY
expiry_weekday: Thursday
entry:
  start_time: '09:20'
  end_time: '09:21'
  order_type: market
filters:
  iv_percentile:
    enabled: false
  india_vix:
    enabled: false
  opening_range:
    enabled: false
  atr:
    enabled: false
  events:
    enabled: false
reentry:
  enabled: false
risk:
  combined_sl_pct: 0.01
  leg_sl_pct: 0.3
  trailing:
    enabled: false
  emergency_iv_spike:
    enabled: false
exit:
  hard_stop_time: '15:10'
  soft_exit_time: '14:45'
positioning:
  margin_cap_lots: 10
  liquidity_cap_lots: 10
  sl_pct: 0.3
        """
    )
    return load_config(config_path).config


def test_backtest_generates_reasonable_pnl(tmp_path):
    config = _synthetic_config(tmp_path)
    timestamps = pd.date_range("2024-01-02 09:15", periods=30, freq="1min", tz="Asia/Kolkata")
    base_price = 18000
    prices = base_price + np.linspace(0, -100, num=len(timestamps))
    underlying = pd.DataFrame(
        {
            "open": prices,
            "high": prices + 5,
            "low": prices - 5,
            "close": prices,
        },
        index=timestamps,
    )
    option_chain = pd.DataFrame(
        [
            {"strike": base_price, "type": "CE", "last_price": 200.0, "iv": 0.18},
            {"strike": base_price, "type": "PE", "last_price": 180.0, "iv": 0.18},
        ]
    )
    engine = BacktestEngine(config, underlying, option_chain)
    result = engine.run()
    assert result.trades == 1
    assert result.pnl < config.profit_target_for_day()
    assert result.pnl > -config.risk_budget_for_day()
