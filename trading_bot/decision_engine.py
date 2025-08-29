from typing import Dict, Any

# In a real application, you might pass the analysis module or its results
from . import analysis

def make_decision(analysis_report: Dict[str, Any]) -> str:
    """
    Analyzes the market report and makes a trading decision.
    This is a simplified rule-based engine. A real-world system would be far more complex.

    Returns a market view: 'Bullish', 'Bearish', 'Neutral', 'Volatile'.
    """
    bullish_score = 0
    bearish_score = 0
    neutral_score = 0

    # --- Rule 1: PCR (Put-Call Ratio) ---
    pcr = analysis_report.get('pcr', 1.0)
    if pcr > 1.3:
        bullish_score += 2 # Strong bullish signal
    elif pcr > 1.0:
        bullish_score += 1
    elif pcr < 0.7:
        bearish_score += 2 # Strong bearish signal
    elif pcr < 1.0:
        bearish_score += 1
    else:
        neutral_score += 1

    # --- Rule 2: OI Buildup ---
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
    # High VIX can mean fear (bearish) or just high volatility (non-directional)
    # We'll use it to determine if a volatile strategy is appropriate.
    vix = analysis_report.get('india_vix', 15)
    if vix > 20:
        # If VIX is high, a directional bet is risky. Volatile strategies might be better.
        # But if scores are already strongly directional, it amplifies that view.
        if bullish_score > bearish_score:
            bullish_score += 1
        elif bearish_score > bullish_score:
            bearish_score += 1
        # If scores are close, it points to high uncertainty -> Volatile
        if abs(bullish_score - bearish_score) < 1:
             return "Volatile"
    else: # Low VIX suggests a range-bound or trending market
        neutral_score += 1

    # --- Rule 4: Spot-Future Difference (Premium/Discount) ---
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
