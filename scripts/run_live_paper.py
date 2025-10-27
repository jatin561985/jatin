import typer
from pathlib import Path
import time
import schedule
import sys

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.cfg.loader import load_config
from src.broker.paper import PaperBroker
from src.strategy.straddle import ShortStraddleStrategy
from src.utils.time import get_ist_now

app = typer.Typer()

@app.command()
def run(config_path: Path = typer.Option("config/nifty_tuesday.yaml", help="Path to the strategy config file.")):
    """
    Runs the trading bot in live paper trading mode.
    """
    typer.echo("Starting live paper trading...")

    config = load_config(config_path)
    broker = PaperBroker(initial_capital=config.capital)
    strategy = ShortStraddleStrategy(config.strategies[0], broker)

    # Schedule the strategy to run every minute
    schedule.every(1).minutes.do(strategy.run)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    app()
