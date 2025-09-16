import random
from typing import List, Dict, Any

from . import strategies
from . import decision_engine
from . import analysis

class Portfolio:
    """Manages the simulated trading account."""
    def __init__(self, initial_capital: float, risk_config: Dict[str, Any]):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions = []
        self.daily_pnl = 0.0
        self.day_over = False
        self.risk_config = risk_config

        # Setup risk limits from configuration
        profit_target_pct = self.risk_config.get('profit_target_percent', 1.0)
        stop_loss_pct = self.risk_config.get('stop_loss_percent', 0.5)
        self.profit_target = self.initial_capital * (profit_target_pct / 100.0)
        self.stop_loss = -self.initial_capital * (stop_loss_pct / 100.0)


    def get_total_value(self):
        # In a real scenario, this would mark-to-market all open positions.
        # For our simulation, we'll just track PnL directly.
        return self.initial_capital + self.daily_pnl

    def record_trade(self, strategy_name: str, cost: float, trade_type: str):
        """Records a new trade and adjusts cash."""
        self.positions.append({"strategy": strategy_name, "cost": cost, "pnl": 0})
        if trade_type == "Pay":
            self.cash -= cost
        elif trade_type == "Receive":
            self.cash += cost
        print(f"Portfolio: Executed {strategy_name}. Cash available: {self.cash:.2f}")

    def update_daily_pnl(self, pnl_change: float):
        """Updates the daily PnL."""
        self.daily_pnl += pnl_change
        print(f"Portfolio: PnL for the day is now: {self.daily_pnl:.2f}")
        self.check_risk_limits()

    def check_risk_limits(self):
        """Checks if the daily profit target or stop loss has been hit."""
        # Use pre-calculated limits from __init__
        if self.daily_pnl >= self.profit_target:
            print(f"!!! PROFIT TARGET HIT: {self.daily_pnl:.2f} >= {self.profit_target:.2f} !!!")
            self.close_all_positions("Profit Target")
            self.day_over = True
        elif self.daily_pnl <= self.stop_loss:
            print(f"!!! STOP LOSS HIT: {self.daily_pnl:.2f} <= {self.stop_loss:.2f} !!!")
            self.close_all_positions("Stop Loss")
            self.day_over = True

    def close_all_positions(self, reason: str):
        """Simulates closing all open positions."""
        print(f"--- Closing all positions due to: {reason} ---")
        # In a real scenario, you'd place closing orders for each position.
        # Here, we just clear them and realize the PnL.
        self.cash += self.daily_pnl # Realize PnL into cash
        self.positions = []
        print(f"All positions closed. Final cash: {self.cash:.2f}")

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
        print(f"Decision: Market view is '{market_view}'. Chosen strategy: '{chosen_strategy.name}'")
        return chosen_strategy

    def execute_trade(self, strategy: strategies.Strategy):
        """Simulates executing a trade."""
        if self.portfolio.day_over:
            print("Trading for the day is over. No new trades will be executed.")
            return

        # Use position sizing from the portfolio's risk configuration
        position_sizing_config = self.portfolio.risk_config.get('position_sizing', {})
        risk_per_trade_pct = position_sizing_config.get('risk_per_trade_percent', 2.0) # Default to 2% if not found
        simulated_cost = self.portfolio.initial_capital * (risk_per_trade_pct / 100.0)

        print(f"Trader: Executing trade with {risk_per_trade_pct}% of capital: {simulated_cost:.2f}")
        self.portfolio.record_trade(strategy.name, simulated_cost, strategy.premium)

if __name__ == '__main__':
    # --- Simulation Run ---
    print("--- Starting Trading Day Simulation (from trader.py) ---")

    # Mock risk config for testing
    mock_risk_config = {
        "profit_target_percent": 1.5,
        "stop_loss_percent": 0.7,
        "position_sizing": {
            "risk_per_trade_percent": 2.5
        }
    }

    my_portfolio = Portfolio(initial_capital=100000.0, risk_config=mock_risk_config)
    trader = Trader(portfolio=my_portfolio)

    print(f"Initialized with Profit Target: {my_portfolio.profit_target:.2f}, Stop Loss: {my_portfolio.stop_loss:.2f}")

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
        my_portfolio.update_daily_pnl(1600) # 1.6% profit > 1.5% target

    # Reset for next scenario
    print("\n--- Resetting for another simulation ---")
    my_portfolio = Portfolio(initial_capital=100000.0, risk_config=mock_risk_config)
    trader = Trader(portfolio=my_portfolio)
    if strat_to_execute:
        trader.execute_trade(strat_to_execute)

    print("\n* Scenario 2: Losing Trade *")
    if my_portfolio.positions:
        # Simulate a losing trade that hits the stop loss
        my_portfolio.update_daily_pnl(-800) # 0.8% loss > 0.7% stop loss
