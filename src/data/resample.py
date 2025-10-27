from __future__ import annotations

import pandas as pd


def to_minute_bars(df: pd.DataFrame, price_col: str = "close") -> pd.DataFrame:
    if df.index.tz is None:
        df = df.tz_localize("Asia/Kolkata")
    ohlc = df[price_col].resample("1T").ohlc()
    ohlc["volume"] = df.get("volume", pd.Series(dtype=float)).resample("1T").sum().fillna(0)
    return ohlc.dropna(how="all")
