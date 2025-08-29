import pandas as pd
import numpy as np
import datetime

# --- Mock Data Generation ---

def get_mock_option_chain_data(instrument="NIFTY"):
    """
    Generates a mock option chain as a pandas DataFrame.
    In a real implementation, this would fetch data from the broker's API.
    """
    spot_price = 23500
    strikes = np.arange(spot_price - 500, spot_price + 500, 50)
    data = []
    for strike in strikes:
        # Call Option
        data.append({
            "strike": strike,
            "type": "CE",
            "ltp": max(0.1, spot_price - strike) + np.random.uniform(50, 150),
            "oi": np.random.randint(10000, 500000),
            "iv": np.random.uniform(10, 25),
            "delta": np.random.uniform(0.4, 0.6),
            "gamma": np.random.uniform(0.001, 0.005),
            "theta": -np.random.uniform(1, 5),
            "vega": np.random.uniform(0.1, 0.5),
            "change_in_oi": np.random.randint(-50000, 50000),
        })
        # Put Option
        data.append({
            "strike": strike,
            "type": "PE",
            "ltp": max(0.1, strike - spot_price) + np.random.uniform(50, 150),
            "oi": np.random.randint(10000, 500000),
            "iv": np.random.uniform(10, 25),
            "delta": -np.random.uniform(0.4, 0.6),
            "gamma": np.random.uniform(0.001, 0.005),
            "theta": -np.random.uniform(1, 5),
            "vega": np.random.uniform(0.1, 0.5),
            "change_in_oi": np.random.randint(-50000, 50000),
        })
    return pd.DataFrame(data)

def get_india_vix():
    """Returns a mock India VIX value."""
    return np.random.uniform(12.0, 18.0)

def get_spot_and_future_prices(instrument="NIFTY"):
    """Returns mock spot and future prices."""
    spot = 23500.50
    future = spot + np.random.uniform(20, 60)
    return {"spot": spot, "future": future}

def get_implied_volatility_percentile():
    """Returns a mock IV Percentile."""
    return np.random.uniform(10.0, 90.0)

def get_participant_data():
    """Returns mock FII, DII, Pro, Client data."""
    participants = ["FII", "DII", "PRO", "CLIENT"]
    data = {}
    for p in participants:
        data[p] = {
            "index_future_long": np.random.randint(10000, 50000),
            "index_future_short": np.random.randint(10000, 50000),
            "index_option_long": np.random.randint(100000, 500000),
            "index_option_short": np.random.randint(100000, 500000),
            "cash_market_buy": np.random.randint(5000, 15000), # in Crores
            "cash_market_sell": np.random.randint(5000, 15000), # in Crores
        }
    return data

def get_historical_oi_data(instrument="NIFTY"):
    """Returns mock historical OI data for options and futures."""
    dates = pd.to_datetime([datetime.date.today() - datetime.timedelta(days=i) for i in range(10)])
    data = {
        "timestamp": dates,
        "option_oi": np.random.randint(1000000, 2000000, size=10),
        "future_oi": np.random.randint(200000, 500000, size=10)
    }
    return pd.DataFrame(data)

if __name__ == '__main__':
    # Example of how to use the functions
    print("--- Mock Option Chain ---")
    print(get_mock_option_chain_data().head())
    print("\n--- Mock India VIX ---")
    print(f"India VIX: {get_india_vix():.2f}")
    print("\n--- Mock Spot/Future Prices ---")
    print(get_spot_and_future_prices())
    print("\n--- Mock IV Percentile ---")
    print(f"IVP: {get_implied_volatility_percentile():.2f}%")
    print("\n--- Mock Participant Data ---")
    print(pd.DataFrame(get_participant_data()).T)
    print("\n--- Mock Historical OI ---")
    print(get_historical_oi_data())
