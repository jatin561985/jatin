from __future__ import annotations

import pandas as pd


class AverageTrueRange:
    def __init__(self, high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14) -> None:
        self.high = high
        self.low = low
        self.close = close
        self.window = window

    def average_true_range(self) -> pd.Series:
        high_low = self.high - self.low
        high_close = (self.high - self.close.shift(1)).abs()
        low_close = (self.low - self.close.shift(1)).abs()
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        return tr.rolling(self.window).mean()
