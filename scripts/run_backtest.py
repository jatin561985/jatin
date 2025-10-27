from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import typer
from loguru import logger

from src.backtest import BacktestEngine
from src.cfg import load_config
from src.utils import configure_logging

app = typer.Typer(help="Run backtests for the short straddle strategy")


def _load_underlying(path: Path) -> pd.DataFrame:
    if path.exists():
        df = pd.read_csv(path, parse_dates=["timestamp"])
        df = df.set_index("timestamp")
    else:
        logger.warning("Underlying data missing, generating synthetic series")
        timestamps = pd.date_range("2024-01-02 09:15", periods=360, freq="1min", tz="Asia/Kolkata")
        prices = 18000 + np.cumsum(np.random.normal(0, 5, size=len(timestamps)))
        df = pd.DataFrame({"open": prices, "high": prices + 5, "low": prices - 5, "close": prices}, index=timestamps)
    return df


def _load_option_chain(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    logger.warning("Option chain missing, synthesizing ATM chain")
    strikes = np.arange(17000, 19001, 50)
    records = []
    for strike in strikes:
        records.append({"strike": strike, "type": "CE", "last_price": max(1, 200 - abs(strike - 18000) * 0.8), "iv": 0.18})
        records.append({"strike": strike, "type": "PE", "last_price": max(1, 200 - abs(strike - 18000) * 0.8), "iv": 0.18})
    return pd.DataFrame(records)


@app.command()
def run(
    config_path: Path = typer.Argument(..., help="Path to YAML config"),
    underlying_csv: Path = typer.Option(Path("data/underlying.csv")),
    option_chain_csv: Path = typer.Option(Path("data/option_chain.csv")),
) -> None:
    configure_logging()
    bundle = load_config(config_path)
    underlying = _load_underlying(underlying_csv)
    option_chain = _load_option_chain(option_chain_csv)
    engine = BacktestEngine(bundle.config, underlying, option_chain)
    result = engine.run()
    typer.echo(f"PnL: {result.pnl:,.2f} | Gross: {result.gross:,.2f} | Costs: {result.costs:,.2f}")


if __name__ == "__main__":
    app()
