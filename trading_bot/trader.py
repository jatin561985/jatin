import random
from datetime import datetime
from typing import List, Dict, Any

from . import strategies
from . import decision_engine
from . import analysis

class Portfolio:
    """Manages the simulated trading account."""
    def __init__(self, initial_capital: float = 100000.0):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions = []
        self.daily_pnl = 0.0
        self.day_over = False
        self.trade_log: List[Dict[str, Any]] = []

    def get_total_value(self):
        # In a real scenario, this would mark-to-market all open positions.
        # For our simulation, we'll just track PnL directly.
        return self.initial_capital + self.daily_pnl

    def record_trade(self, strategy_name: str, notional: float, trade_type: str):
        """Records a new trade, adjusts cash, and logs the event."""

        trade_entry = {
            "timestamp": datetime.now(),
            "strategy": strategy_name,
            "notional": notional,
            "trade_type": trade_type,
            "pnl": 0.0,
        }
        self.positions.append(trade_entry.copy())
        self.trade_log.append({**trade_entry, "event": "Entry"})

        if trade_type == "Pay":
            self.cash -= notional
        elif trade_type == "Receive":
            self.cash += notional

        print(
            f"Portfolio: Executed {strategy_name} ({trade_type}). "
            f"Capital allocated: {notional:.2f}. Cash available: {self.cash:.2f}"
        )

    def update_daily_pnl(self, pnl_change: float):
        """Updates the daily PnL."""
        self.daily_pnl += pnl_change
        print(f"Portfolio: PnL for the day is now: {self.daily_pnl:.2f}")
        self.check_risk_limits()

    def check_risk_limits(self):
        """Checks if the daily profit target or stop loss has been hit."""
        profit_target = self.initial_capital * 0.01  # 1%
        stop_loss = -self.initial_capital * 0.005 # 0.5%

        if self.daily_pnl >= profit_target:
            print(f"!!! PROFIT TARGET HIT: {self.daily_pnl:.2f} >= {profit_target:.2f} !!!")
            self.close_all_positions("Profit Target")
            self.day_over = True
        elif self.daily_pnl <= stop_loss:
            print(f"!!! STOP LOSS HIT: {self.daily_pnl:.2f} <= {stop_loss:.2f} !!!")
            self.close_all_positions("Stop Loss")
            self.day_over = True

    def close_all_positions(self, reason: str):
        """Simulates closing all open positions."""
        print(f"--- Closing all positions due to: {reason} ---")
        # In a real scenario, you'd place closing orders for each position.
        # Here, we just clear them and realize the PnL.
        self.cash += self.daily_pnl # Realize PnL into cash
        self.trade_log.append(
            {
                "timestamp": datetime.now(),
                "strategy": "ALL",
                "notional": 0.0,
                "trade_type": "Exit",
                "pnl": self.daily_pnl,
                "event": f"Closed due to {reason}",
            }
        )
        self.positions = []
        print(f"All positions closed. Final cash: {self.cash:.2f}")

    def get_risk_snapshot(self) -> Dict[str, Any]:
        """Returns key risk numbers for reporting."""

        return {
            "initial_capital": self.initial_capital,
            "cash_on_hand": self.cash,
            "daily_pnl": self.daily_pnl,
            "profit_target": self.initial_capital * 0.01,
            "stop_loss": -self.initial_capital * 0.005,
            "day_over": self.day_over,
        }

class Trader:
    """The main trading agent."""
    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio

    def choose_strategy(self, market_view: str) -> strategies.Strategy:
        """Chooses a suitable strategy based on the market view."""

        # Get all strategies that match the general view
        potential_strategies = strategies.get_strategies_by_view(market_view)

        if not potential_strategies:
            print(f"No strategies found for market view: {market_view}")
            return None

        # Simple logic: pick a random strategy from the suitable list.
        # A more advanced bot could rank them based on IV, risk, etc.
        chosen_strategy = random.choice(potential_strategies)
        print(
            f"Decision: Market view is '{market_view}'. "
            f"Chosen strategy: '{chosen_strategy.name}'"
        )
        if chosen_strategy.setup:
            print(f"  Setup: {chosen_strategy.setup}")
        if chosen_strategy.breakeven:
            print(f"  Breakeven: {chosen_strategy.breakeven}")
        print(f"  Max Profit: {chosen_strategy.max_profit}")
        print(f"  Max Loss: {chosen_strategy.max_loss}")
        return chosen_strategy

    def execute_trade(self, strategy: strategies.Strategy):
        """Simulates executing a trade."""
        if self.portfolio.day_over:
            print("Trading for the day is over. No new trades will be executed.")
            return

        # Simplified cost simulation
        simulated_cost = self.portfolio.initial_capital * 0.005 # Risk 0.5% capital per trade

        self.portfolio.record_trade(strategy.name, simulated_cost, strategy.premium)

if __name__ == '__main__':
    # --- Simulation Run ---
    print("--- Starting Trading Day Simulation ---")
    my_portfolio = Portfolio(initial_capital=100000.0)
    trader = Trader(portfolio=my_portfolio)

    # 1. Get market analysis
    report = analysis.run_full_analysis()

    # 2. Make a decision
    view = decision_engine.make_decision(report)

    # 3. Choose and execute a strategy
    strat_to_execute = trader.choose_strategy(view)
    if strat_to_execute:
        trader.execute_trade(strat_to_execute)

    # 4. Simulate market movement and PnL changes
    print("\n--- Simulating market updates ---")
    if my_portfolio.positions:
        # Simulate a winning trade that hits the profit target
        print("\n* Scenario 1: Winning Trade *")
        my_portfolio.update_daily_pnl(1100) # 1.1% profit

    # Reset for next scenario
    print("\n--- Resetting for another simulation ---")
    my_portfolio = Portfolio(initial_capital=100000.0)
    trader = Trader(portfolio=my_portfolio)
    if strat_to_execute:
        trader.execute_trade(strat_to_execute)

    print("\n* Scenario 2: Losing Trade *")
    if my_portfolio.positions:
        # Simulate a losing trade that hits the stop loss
        my_portfolio.update_daily_pnl(-600) # 0.6% loss
