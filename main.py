import time
from typing import Optional

from trading_bot import analysis, decision_engine, trader, reporting

def run_trading_session(
    excel_path: str = "trading_bot_report.xlsx",
    google_sheet_id: Optional[str] = None,
):
    """
    Simulates a single trading session from analysis to execution.
    """
    print("--- Initializing Trading Bot ---")

    # 1. Setup Portfolio and Trader
    # The initial capital can be configured here
    initial_capital = 200000.0
    portfolio = trader.Portfolio(initial_capital=initial_capital)
    trading_agent = trader.Trader(portfolio=portfolio)

    print(f"Portfolio initialized with Capital: {initial_capital:.2f}")
    print(f"Daily Profit Target: {portfolio.initial_capital * 0.01:.2f}")
    print(f"Daily Stop Loss: -{portfolio.initial_capital * 0.005:.2f}")
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
        # You can change this value to see different outcomes
        # e.g., 2500 for profit target, -1100 for stop loss
        pnl_update = 2500
        portfolio.update_daily_pnl(pnl_update)

    # --- Reporting ---
    reporter = reporting.SpreadsheetReporter(output_path=excel_path, google_sheet_id=google_sheet_id)
    tables = reporter.build_tables(
        market_report,
        market_view,
        portfolio,
        chosen_strategy=chosen_strategy.name if chosen_strategy else None,
    )

    excel_file = reporter.export_to_excel(tables)
    print(f"\nSpreadsheet report created at: {excel_file.resolve()}")

    if google_sheet_id:
        reporter.export_to_google_sheet(tables)


if __name__ == "__main__":
    run_trading_session()
    print("\n--- Trading Bot Simulation Finished ---")
