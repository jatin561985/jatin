import pandas as pd
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.strategy.straddle import ShortStraddleStrategy
from src.broker.paper import PaperBroker
from src.cfg.models import BaseConfig

class BacktestEngine:
    """
    An event-driven backtester for the trading strategy.
    """
    def __init__(self, config: BaseConfig, historical_data: pd.DataFrame):
        self.config = config
        self.historical_data = historical_data
        self.broker = PaperBroker(initial_capital=self.config.capital)
        self.strategy = ShortStraddleStrategy(self.config.strategies[0], self.broker)

    def run(self):
        """
        Runs the backtest loop.
        """
        for index, row in self.historical_data.iterrows():
            # Pass the current timestamp to the strategy's run method
            self.strategy.run(row['timestamp'])

        print("Backtest complete.")
        print(f"Final capital: {self.broker.capital}")
        print(f"Trade log: {self.broker.trade_log}")

if __name__ == "__main__":
    # This is for demonstration purposes only.
    # The main entry point is scripts/run_backtest.py
    pass
