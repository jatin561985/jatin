import typer
from pathlib import Path
import time
import schedule
import sys

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.cfg.loader import load_config
from src.broker.kite_connect import KiteBroker
from src.strategy.straddle import ShortStraddleStrategy
from src.utils.time import get_ist_now

app = typer.Typer()

@app.command()
def run(config_path: Path = typer.Option("config/nifty_tuesday.yaml", help="Path to the strategy config file.")):
    """
    Runs the trading bot in live trading mode with Zerodha Kite Connect.
    """
    typer.echo("Starting live trading...")

    # from dotenv import load_dotenv
    # load_dotenv() # Load environment variables from .env file

    config = load_config(config_path)
    # This will be replaced with KiteBroker once fully implemented
    # broker = KiteBroker()
    broker = None # Placeholder
    # strategy = ShortStraddleStrategy(config.strategies[0], broker)

    typer.echo("Live trading script is a placeholder and not yet implemented.")
    # Schedule the strategy to run every minute
    # schedule.every(1).minutes.do(strategy.run)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

if __name__ == "__main__":
    app()
