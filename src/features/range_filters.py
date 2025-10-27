from __future__ import annotations

import pandas as pd
from ta.volatility import AverageTrueRange


def atr_percent(df: pd.DataFrame, lookback: int = 14) -> pd.Series:
    atr = AverageTrueRange(high=df["high"], low=df["low"], close=df["close"], window=lookback)
    return atr.average_true_range() / df["close"]


def opening_range_deviation(df: pd.DataFrame, duration_min: int = 15) -> pd.Series:
    idx = df.index
    start = idx.min().normalize() + pd.Timedelta(hours=9, minutes=15)
    end = start + pd.Timedelta(minutes=duration_min)
    mask = (idx >= start) & (idx < end)
    if mask.sum() == 0:
        return pd.Series(0.0, index=idx)
    high = df.loc[mask, "high"].max()
    low = df.loc[mask, "low"].min()
    if pd.isna(high) or pd.isna(low) or high == low:
        return pd.Series(0.0, index=idx)
    range_mid = (high + low) / 2
    return (df["close"] - range_mid) / (high - low)
