from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class PerformanceSummary:
    total_pnl: float
    sharpe: float
    max_drawdown: float
    win_rate: float


def summarize(trade_pnls: pd.Series, equity_curve: pd.Series) -> PerformanceSummary:
    total_pnl = trade_pnls.sum()
    daily_returns = equity_curve.pct_change().dropna()
    sharpe = (daily_returns.mean() / daily_returns.std() * (252**0.5)) if not daily_returns.empty else 0.0
    cumulative = equity_curve.cummax()
    drawdown = (equity_curve - cumulative) / cumulative
    max_drawdown = drawdown.min() if not drawdown.empty else 0.0
    wins = (trade_pnls > 0).sum()
    win_rate = wins / len(trade_pnls) if len(trade_pnls) else 0.0
    return PerformanceSummary(total_pnl=total_pnl, sharpe=sharpe, max_drawdown=max_drawdown, win_rate=win_rate)
