import pandas as pd
from ta.volatility import average_true_range

def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculates the Average True Range (ATR).
    """
    return average_true_range(high=high, low=low, close=close, window=period)

def calculate_iv_percentile(iv_series: pd.Series, window: int = 252) -> float:
    """
    Calculates the Implied Volatility (IV) Percentile.
    """
    rolling_iv = iv_series.rolling(window=window)
    iv_rank = rolling_iv.apply(lambda x: x.rank(pct=True).iloc[-1], raw=False)
    return iv_rank.iloc[-1] * 100 if not iv_rank.empty else 0.0

def vix_ma_filter(vix_series: pd.Series, ma_period: int = 20) -> bool:
    """
    A simple VIX filter based on its moving average.
    Returns True if VIX is above its MA, indicating higher volatility.
    """
    if len(vix_series) < ma_period:
        return False
    vix_ma = vix_series.rolling(window=ma_period).mean().iloc[-1]
    current_vix = vix_series.iloc[-1]
    return current_vix > vix_ma

def opening_range_breakout(price_series: pd.Series, opening_range_minutes: int = 15) -> str:
    """
    Checks for a breakout from the opening range.
    """
    if len(price_series) < opening_range_minutes:
        return "Inside"

    opening_range = price_series.iloc[:opening_range_minutes]
    high = opening_range.max()
    low = opening_range.min()

    current_price = price_series.iloc[-1]

    if current_price > high:
        return "Breakout_Up"
    elif current_price < low:
        return "Breakout_Down"
    else:
        return "Inside"

if __name__ == "__main__":
    # Example usage:
    close_prices = pd.Series([100, 101, 102, 103, 102, 104, 105, 103, 106, 107])
    high_prices = pd.Series([101, 102, 103, 104, 103, 105, 106, 104, 107, 108])
    low_prices = pd.Series([99, 100, 101, 102, 101, 103, 104, 102, 105, 106])

    atr = calculate_atr(high_prices, low_prices, close_prices)
    print(f"ATR:\\n{atr}")

    ivs = pd.Series([0.1, 0.12, 0.15, 0.14, 0.16, 0.18, 0.2, 0.19, 0.17, 0.15])
    ivp = calculate_iv_percentile(ivs, window=5)
    print(f"\\nIV Percentile: {ivp:.2f}%")

    vix = pd.Series([12, 13, 14, 15, 16, 17, 18, 19, 20, 18])
    is_vix_high = vix_ma_filter(vix, ma_period=5)
    print(f"\\nVIX is high: {is_vix_high}")

    prices_today = pd.Series([25000, 25010, 25005, 25020, 25015, 25030, 25025])
    orb_status = opening_range_breakout(prices_today, opening_range_minutes=5)
    print(f"\\nOpening Range Status: {orb_status}")
