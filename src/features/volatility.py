from __future__ import annotations

import pandas as pd


def iv_percentile(series: pd.Series, window: int = 252) -> pd.Series:
    ranks = series.rolling(window).apply(lambda x: pd.Series(x).rank(pct=True).iloc[-1], raw=False)
    return ranks.fillna(method="ffill")


def india_vix_filter(vix: pd.Series, lookback: int = 20) -> pd.Series:
    ma = vix.rolling(lookback).mean()
    return (vix - ma) / ma
