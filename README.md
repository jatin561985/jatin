# Short Straddle Research & Execution Stack

Production-oriented Python 3.11+ project for researching, backtesting, and executing NIFTY & SENSEX weekly ATM short straddles with strong risk controls.

## Features

- Configurable strategy definitions via YAML for different underlying/expiry profiles.
- Minute-level event-driven backtester with synthetic option price simulator.
- Deterministic position sizing bounded by risk budget, margin, and liquidity caps.
- Risk management covering MTM stop, profit targets, trailing protection, and IV spike halts.
- Broker abstraction with Zerodha Kite Connect integration and paper broker.
- CLI utilities (Typer) for fetching option chains, running backtests, and launching paper/live trading loops.
- Reporting helpers for portfolio metrics and Streamlit-ready data structures.
- Modular architecture with typed Pydantic configs and reusable feature filters.

## Project Layout

```
├─ config/
│  ├─ base.yaml                # shared defaults
│  ├─ nifty_tuesday.yaml       # NIFTY Tuesday expiry overrides
│  └─ sensex_thursday.yaml     # SENSEX Thursday expiry overrides
├─ data/                       # cached option chains, index bars
├─ scripts/                    # Typer CLI entry-points
├─ src/
│  ├─ cfg/                     # config loading & validation
│  ├─ data/                    # NSE clients, caching, resampling
│  ├─ features/                # IV percentile, ATR, ORB filters
│  ├─ strategy/                # straddle logic & sizing
│  ├─ costs/                   # brokerage and funding models
│  ├─ risk/                    # stop-loss, emergency rules
│  ├─ backtest/                # minute event-driven backtester
│  ├─ exec/                    # live loops & scheduling
│  ├─ reporting/               # equity curve metrics
│  └─ utils/                   # logging, time, math, greeks
└─ tests/                      # pytest unit coverage
```

## Getting Started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Fill in `.env` with Kite credentials for live trading. For paper/backtest, credentials are not required.

## Running Backtests

```bash
python scripts/run_backtest.py config/nifty_tuesday.yaml \
  --underlying-csv data/nifty_minute.csv \
  --option-chain-csv data/nifty_option_chain.csv
```

If data files are absent, synthetic series are generated for exploratory use.

## Live & Paper Trading

- Paper mode (no broker orders):
  ```bash
  python scripts/run_live_paper.py config/nifty_tuesday.yaml
  ```
- Zerodha execution (requires `kiteconnect` and API keys in `.env`):
  ```bash
  python scripts/run_live_trade.py config/nifty_tuesday.yaml
  ```

The live executor relies on scheduled jobs in the India timezone to enter and exit positions per config.

## Tests

```bash
pytest
```

## Streamlit Visualization (Optional)

Load `BacktestResult.mtm_series` and `reporting.summarize` outputs in a Streamlit app for interactive dashboards (left for strategy customization).

## Safety Notes

- Always validate filters and risk budgets with real market data before enabling broker execution.
- Monitor margin requirements and liquidity for the configured lot caps.
