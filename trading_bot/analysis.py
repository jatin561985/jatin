import pandas as pd
import numpy as np

# In a real application, you'd pass the data provider object
# For now, we import the mock functions directly
from . import data_provider

def calculate_spot_future_diff(spot_price: float, future_price: float) -> dict:
    """Calculates the difference and basis between spot and future prices."""
    difference = future_price - spot_price
    basis_points = (difference / spot_price) * 10000
    return {"difference": difference, "basis_points": basis_points}

def calculate_pcr(option_chain_df: pd.DataFrame) -> float:
    """Calculates the Put-Call Ratio from the option chain."""
    if option_chain_df.empty:
        return np.nan

    total_pe_oi = option_chain_df[option_chain_df['type'] == 'PE']['oi'].sum()
    total_ce_oi = option_chain_df[option_chain_df['type'] == 'CE']['oi'].sum()

    if total_ce_oi == 0:
        return np.inf # Avoid division by zero

    return total_pe_oi / total_ce_oi

def calculate_max_pain(option_chain_df: pd.DataFrame) -> float:
    """
    Calculates the Max Pain strike from the option chain.
    Max Pain is the strike price with the minimum total intrinsic value for all options.
    """
    if option_chain_df.empty:
        return np.nan

    strikes = option_chain_df['strike'].unique()
    total_loss = {}

    for strike_price in strikes:
        # Calculate loss for call option holders if stock expires at strike_price
        calls = option_chain_df[option_chain_df['type'] == 'CE'].copy()
        calls['intrinsic_value'] = (strike_price - calls['strike']).clip(lower=0)
        calls['loss'] = calls['intrinsic_value'] * calls['oi']

        # Calculate loss for put option holders if stock expires at strike_price
        puts = option_chain_df[option_chain_df['type'] == 'PE'].copy()
        puts['intrinsic_value'] = (puts['strike'] - strike_price).clip(lower=0)
        puts['loss'] = puts['intrinsic_value'] * puts['oi']

        total_loss[strike_price] = calls['loss'].sum() + puts['loss'].sum()

    # The strike with the minimum total loss is the max pain point
    max_pain_strike = min(total_loss, key=total_loss.get)
    return max_pain_strike

def analyze_oi_buildup(price_change: float, oi_change: float) -> str:
    """
    Analyzes Open Interest buildup based on price and OI changes.
    This is a simplified view. Real analysis is more nuanced.
    """
    if price_change > 0 and oi_change > 0:
        return "Long Buildup"
    elif price_change > 0 and oi_change < 0:
        return "Short Covering"
    elif price_change < 0 and oi_change > 0:
        return "Short Buildup"
    elif price_change < 0 and oi_change < 0:
        return "Long Unwinding"
    else:
        return "Indecisive"

def run_full_analysis():
    """
    Runs all analysis functions on the mock data and returns a consolidated report.
    """
    # 1. Fetch all necessary data
    option_chain = data_provider.get_mock_option_chain_data()
    vix = data_provider.get_india_vix()
    prices = data_provider.get_spot_and_future_prices()
    ivp = data_provider.get_implied_volatility_percentile()
    participant_data = data_provider.get_participant_data()
    hist_oi = data_provider.get_historical_oi_data()

    # 2. Perform calculations
    pcr = calculate_pcr(option_chain)
    max_pain = calculate_max_pain(option_chain.copy()) # Pass a copy to avoid SettingWithCopyWarning
    spot_future_diff = calculate_spot_future_diff(prices['spot'], prices['future'])

    # Simulate price and OI change for buildup analysis
    # In a real scenario, you'd compare current vs previous values.
    price_change_sim = prices['spot'] - (prices['spot'] * 0.995)
    oi_change_sim = hist_oi.iloc[0]['future_oi'] - hist_oi.iloc[1]['future_oi']
    buildup = analyze_oi_buildup(price_change_sim, oi_change_sim)

    # 3. Consolidate into a single dictionary
    analysis_report = {
        "timestamp": pd.Timestamp.now(),
        "spot_price": prices['spot'],
        "future_price": prices['future'],
        "spot_future_diff_pts": spot_future_diff['difference'],
        "india_vix": vix,
        "ivp": ivp,
        "pcr": pcr,
        "max_pain": max_pain,
        "buildup": buildup,
        "participant_data": participant_data,
        "raw_option_chain": option_chain,
    }

    return analysis_report

if __name__ == '__main__':
    report = run_full_analysis()
    print("--- Market Analysis Report ---")
    for key, value in report.items():
        if key not in ["participant_data", "raw_option_chain"]:
            if isinstance(value, float):
                print(f"{key.replace('_', ' ').title()}: {value:.2f}")
            else:
                print(f"{key.replace('_', ' ').title()}: {value}")

    print("\n--- Participant Data ---")
    print(pd.DataFrame(report['participant_data']).T)

    print(f"\nAnalysis Complete. Report generated at {report['timestamp']}")
