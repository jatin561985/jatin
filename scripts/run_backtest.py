import typer
from pathlib import Path
import pandas as pd
import sys

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.cfg.loader import load_config
from src.backtest.engine import BacktestEngine
from src.reporting.metrics import calculate_sharpe_ratio, calculate_max_drawdown
from src.reporting.plots import plot_equity_curve

app = typer.Typer()

@app.command()
def run(
    config_path: Path = typer.Option("config/nifty_tuesday.yaml", help="Path to the strategy config file."),
    data_path: Path = typer.Option("data/nifty_ticks.csv", help="Path to the historical data file.")
):
    """
    Runs a backtest for the short straddle strategy.
    """
    typer.echo(f"Starting backtest with config: {config_path}")

    config = load_config(config_path)
    historical_data = pd.read_csv(data_path, parse_dates=["timestamp"])
    historical_data['timestamp'] = historical_data['timestamp'].dt.tz_localize('Asia/Kolkata')

    backtester = BacktestEngine(config, historical_data)
    backtester.run()

    # Generate and display reports
    # This is a simplified reporting section; a real one would be more detailed.
    equity_curve = pd.Series(backtester.broker.capital, name="Equity") # Simplified

    typer.echo("\\n--- Backtest Results ---")
    sharpe = calculate_sharpe_ratio(equity_curve.pct_change().dropna())
    max_dd = calculate_max_drawdown(equity_curve)

    typer.echo(f"Final Capital: ₹{backtester.broker.capital:,.2f}")
    typer.echo(f"Sharpe Ratio: {sharpe:.2f}")
    typer.echo(f"Max Drawdown: {max_dd:.2f}%")

    # Generate plots
    plot_equity_curve(equity_curve)
    typer.echo("\\nEquity curve plot saved to data/equity_curve.png")

if __name__ == "__main__":
    app()
