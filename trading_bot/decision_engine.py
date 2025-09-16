from typing import Dict, Any

from . import analysis
from .config import CONFIG

def make_decision(analysis_report: Dict[str, Any]) -> str:
    """
    Analyzes the market report and makes a trading decision based on configured rules.
    This engine uses a scoring system to determine a market view.
    """
    bullish_score = 0
    bearish_score = 0
    neutral_score = 0

    # Get configs, with fallbacks if the config file is incomplete
    pcr_config = CONFIG.get('market_analysis', {}).get('option_chain_analysis', {}).get('put_call_ratio', {})
    vix_config = CONFIG.get('market_analysis', {}).get('fundamental_checks', {}).get('vix_threshold', {})

    # --- Rule 1: PCR (Put-Call Ratio) ---
    pcr = analysis_report.get('pcr', 1.0)
    # Using configured thresholds. Assuming low PCR is bullish (oversold) and high is bearish (overbought).
    if pcr < pcr_config.get('oversold', 0.7):
        bullish_score += 2
    elif pcr < pcr_config.get('neutral', [0.9, 1.1])[0]:
        bullish_score += 1
    elif pcr > pcr_config.get('overbought', 1.3):
        bearish_score += 2
    elif pcr > pcr_config.get('neutral', [0.9, 1.1])[1]:
        bearish_score += 1
    else:
        neutral_score += 1

    # --- Rule 2: OI Buildup (logic remains the same as it's not configured by numbers) ---
    buildup = analysis_report.get('buildup', 'Indecisive')
    if buildup == 'Long Buildup':
        bullish_score += 1
    elif buildup == 'Short Buildup':
        bearish_score += 1
    elif buildup == 'Short Covering':
        bullish_score += 0.5 # Mildly bullish
    elif buildup == 'Long Unwinding':
        bearish_score += 0.5 # Mildly bearish
    else:
        neutral_score += 1

    # --- Rule 3: India VIX (Volatility) ---
    vix = analysis_report.get('india_vix', 15)
    # If VIX is high, it can either signal volatility or amplify the existing trend.
    if vix > vix_config.get('medium', 20):
        # If scores are close, it points to high uncertainty -> Volatile
        if abs(bullish_score - bearish_score) < 1:
             return "Volatile"
        # If there's a clear bias, high VIX amplifies that view.
        if bullish_score > bearish_score:
            bullish_score += 1
        elif bearish_score > bullish_score:
            bearish_score += 1
    else: # Low VIX suggests a range-bound or trending market
        neutral_score += 1

    # --- Rule 4: Spot-Future Difference (Premium/Discount) ---
    # Thresholds are not in config, keeping them as is for simulation purposes.
    diff = analysis_report.get('spot_future_diff_pts', 0)
    if diff > 50: # Heavy premium
        bullish_score += 1
    elif diff < -20: # Discount
        bearish_score += 1

    # --- Final Decision ---
    if bullish_score > bearish_score and bullish_score > neutral_score:
        return "Bullish"
    elif bearish_score > bullish_score and bearish_score > neutral_score:
        return "Bearish"
    else:
        # If scores are tied or neutral is highest, assume neutral
        return "Neutral"

if __name__ == '__main__':
    print("Running Decision Engine with mock data...")

    # Generate a sample analysis report
    mock_report = analysis.run_full_analysis()

    print("\n--- Sample Analysis Report ---")
    for key, value in mock_report.items():
        if key not in ["participant_data", "raw_option_chain"]:
            if isinstance(value, float):
                print(f"{key.replace('_', ' ').title()}: {value:.2f}")
            else:
                print(f"{key.replace('_', ' ').title()}: {value}")

    # Make a decision based on the report
    decision = make_decision(mock_report)

    print(f"\n--- Final Decision ---")
    print(f"Market View: {decision}")
