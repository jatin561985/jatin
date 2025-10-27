import numpy as np
import pandas as pd

def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0) -> float:
    """
    Calculates the Sharpe Ratio of a returns series.
    """
    return (returns.mean() - risk_free_rate) / returns.std() if returns.std() != 0 else 0.0

def calculate_max_drawdown(equity_curve: pd.Series) -> float:
    """
    Calculates the Maximum Drawdown of an equity curve.
    """
    peak = equity_curve.expanding(min_periods=1).max()
    drawdown = (equity_curve - peak) / peak
    return drawdown.min() * 100 if not drawdown.empty else 0.0

def calculate_win_rate(trade_log: pd.DataFrame) -> float:
    """
    Calculates the Win Rate from a trade log.
    Assumes the trade log has a 'pnl' column.
    """
    if 'pnl' not in trade_log.columns or trade_log.empty:
        return 0.0
    wins = trade_log[trade_log['pnl'] > 0]
    return (len(wins) / len(trade_log)) * 100 if not trade_log.empty else 0.0

if __name__ == "__main__":
    # Example usage:
    returns_data = pd.Series([0.01, -0.005, 0.02, 0.015, -0.01])
    sharpe = calculate_sharpe_ratio(returns_data)
    print(f"Sharpe Ratio: {sharpe:.2f}")

    equity = pd.Series([100, 102, 101, 103, 102, 104, 103])
    max_dd = calculate_max_drawdown(equity)
    print(f"Max Drawdown: {max_dd:.2f}%")

    trades = pd.DataFrame({'pnl': [100, -50, 200, 150, -100]})
    win_rate = calculate_win_rate(trades)
    print(f"Win Rate: {win_rate:.2f}%")
