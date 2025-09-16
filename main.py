import sys
import time
from trading_bot import analysis, decision_engine, trader, strategies
from trading_bot.config import CONFIG

def run_trading_session():
    """
    Simulates a single trading session from analysis to execution.
    """
    if not CONFIG:
        print("CRITICAL: Configuration not loaded. Exiting.")
        sys.exit(1)

    print("--- Initializing Trading Bot from Configuration ---")
    print(f"Bot Name: {CONFIG['bot_configuration']['name']} v{CONFIG['bot_configuration']['version']}")

    # 1. Setup Portfolio and Trader from config
    initial_capital = float(CONFIG.get('safety_features', {}).get('max_order_value', 100000.0))
    risk_config = CONFIG.get('risk_management', {})
    profit_target_pct = risk_config.get('profit_target_percent', 1.0)
    stop_loss_pct = risk_config.get('stop_loss_percent', 0.5)

    # Pass the entire risk_config to the Portfolio
    portfolio = trader.Portfolio(initial_capital=initial_capital, risk_config=risk_config)
    trading_agent = trader.Trader(portfolio=portfolio)

    profit_target_abs = portfolio.profit_target
    stop_loss_abs = portfolio.stop_loss

    print(f"Portfolio initialized with Capital: {initial_capital:.2f}")
    print(f"Daily Profit Target ({profit_target_pct}%): {profit_target_abs:.2f}")
    print(f"Daily Stop Loss ({stop_loss_pct}%): {stop_loss_abs:.2f}")
    print("-" * 30)


    # Main operational loop. In a real bot, this would run on a schedule.
    # For this simulation, we will run it once.

    # Check if the trading day is already over (e.g. from a previous run)
    if portfolio.day_over:
        print("Trading is closed for the day.")
        return

    print("\nSTEP 1: Analyzing Market Data...")
    # In a real bot, you would pass live data here.
    # Our analysis function uses the mock data provider.
    market_report = analysis.run_full_analysis()

    # Print a summary of the analysis
    print(f"  - Spot/Future Diff: {market_report['spot_future_diff_pts']:.2f} pts")
    print(f"  - India VIX: {market_report['india_vix']:.2f}")
    print(f"  - PCR: {market_report['pcr']:.2f}")
    print(f"  - Max Pain: {market_report['max_pain']}")
    print(f"  - OI Buildup: {market_report['buildup']}")

    print("\nSTEP 2: Making a Trading Decision...")
    market_view = decision_engine.make_decision(market_report)

    print("\nSTEP 3: Selecting and Executing a Strategy...")
    # The trader will choose a strategy based on the view and execute it.
    chosen_strategy = trading_agent.choose_strategy(market_view)

    if chosen_strategy:
        trading_agent.execute_trade(chosen_strategy)
    else:
        print("No suitable strategy found. Holding position.")

    print("\n--- End of Automated Execution ---")

    # --- P&L Simulation to test Risk Management ---
    if portfolio.positions:
        print("\n--- Simulating P&L to test risk management ---")
        # Simulate a PnL that hits the profit target
        pnl_update = profit_target_abs * 1.1 # a value to trigger the profit target
        print(f"Simulating PnL update of: {pnl_update:.2f}")
        portfolio.update_daily_pnl(pnl_update)


if __name__ == "__main__":
    run_trading_session()
    print("\n--- Trading Bot Simulation Finished ---")
