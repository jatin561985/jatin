from src.cfg.models import StrategyConfig
from src.broker.paper import PaperBroker
from src.strategy.sizing import lots_allowed
from datetime import time, datetime

class ShortStraddleStrategy:
    """
    Implements the short straddle trading strategy.
    """
    def __init__(self, config: StrategyConfig, broker: PaperBroker):
        self.config = config
        self.broker = broker

    def run(self, current_time: datetime):
        """
        Executes the main strategy loop.
        """
        import pytz
        IST = pytz.timezone("Asia/Kolkata")

        entry_start = datetime.strptime(self.config.entry_window.start, '%H:%M').time()
        entry_end = datetime.strptime(self.config.entry_window.end, '%H:%M').time()

        now_time = current_time.astimezone(IST).time()

        if entry_start <= now_time <= entry_end and not self.broker.positions:
            self.enter_straddle()

        # Exit logic will be added later
        # self.manage_positions()

    def enter_straddle(self):
        """
        Enters a short straddle position.
        """
        print("Entering short straddle...")
        # In a real scenario, you would get the ATM strike from the option chain
        atm_strike = 25000
        ce_symbol = f"{self.config.underlying}{atm_strike}CE"
        pe_symbol = f"{self.config.underlying}{atm_strike}PE"

        # Mock prices for now
        ce_price = 100.0
        pe_price = 100.0

        # Calculate lots
        num_lots = lots_allowed(
            P0=(ce_price + pe_price),
            lot_size=self.config.lot_size,
            risk_budget=self.broker.capital * (self.config.exits.hard_mtm_stop_loss_percent / 100.0),
            sl_pct=self.config.exits.per_leg_sl_percent / 100.0,
            margin_cap_lots=100, # Mock value
            liq_cap_lots=100, # Mock value
        )

        if num_lots > 0:
            self.broker.place_order(ce_symbol, num_lots, ce_price, "SELL")
            self.broker.place_order(pe_symbol, num_lots, pe_price, "SELL")
            print(f"Sold {num_lots} lots of {ce_symbol} at {ce_price}")
            print(f"Sold {num_lots} lots of {pe_symbol} at {pe_price}")

    def manage_positions(self):
        """
        Manages open positions, checking for stop-loss or profit-target.
        """
        # In a real scenario, you would get live prices for the open positions
        # For now, we'll use mock prices to demonstrate the logic
        mock_prices = {
            "NIFTY25000CE": 110.0,
            "NIFTY25000PE": 90.0
        }

        # Check for stop-loss
        from src.risk.rules import check_stop_loss
        sl_hit = check_stop_loss(
            self.broker.positions,
            mock_prices,
            self.config.exits.per_leg_sl_percent
        )
        if sl_hit:
            print("Stop-loss hit! Exiting all positions.")
            # In a real scenario, you would exit all positions here
            pass

if __name__ == "__main__":
    # This is a simplified example of how the strategy might be run.
    # A full backtester or live execution engine is needed to run this properly.

    # We need to load a dummy config for this to run
    from src.cfg.loader import load_config
    from pathlib import Path

    config = load_config(Path("config/nifty_tuesday.yaml"))
    paper_broker = PaperBroker(initial_capital=config.capital)
    strategy = ShortStraddleStrategy(config.strategies[0], paper_broker)

    # To test the entry logic, we need to be within the entry window
    # This is just a demonstration; a proper scheduler is needed for live trading.
    print("Running strategy check...")
    strategy.run()

