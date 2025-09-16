from dataclasses import dataclass
from typing import List, Dict

from .config import CONFIG

@dataclass
class Strategy:
    """A dataclass to hold the definition of a trading strategy."""
    name: str
    market_view: str
    max_profit: str
    max_loss: str
    premium: str # 'Pay' or 'Receive'
    strategy_type: str  # 'bullish', 'bearish', 'neutral', 'volatile'

# This list acts as a master registry of all possible strategies and their properties.
# The configuration file will then select from this list.
# I have expanded this list to include all strategies from the config.
_all_strategies = [
    # --- Bullish Strategies ---
    Strategy("Buy Call", "Strong Bullish", "Unlimited", "Limited (Premium Paid)", "Pay", "bullish"),
    Strategy("Bull Call Spread", "Moderate Bullish", "Limited", "Limited", "Pay", "bullish"),
    Strategy("Long Synthetic Future", "Strong Bullish", "Unlimited", "Unlimited", "Pay", "bullish"),
    Strategy("Bull Put Spread", "Moderate Bullish", "Limited", "Limited", "Receive", "bullish"),
    Strategy("Sell Put", "Moderate Bullish", "Limited", "Unlimited", "Receive", "bullish"),
    Strategy("Bull Condor", "Moderate Bullish", "Limited", "Limited", "Receive", "bullish"),
    Strategy("Bull Butterfly", "Mild Bullish", "Limited", "Limited", "Pay", "bullish"),
    Strategy("Jade Lizard", "Mild Bullish", "Limited (Premium)", "Unlimited", "Receive", "bullish"),

    # --- Bearish Strategies ---
    Strategy("Buy Put", "Strong Bearish", "Unlimited", "Limited (Premium Paid)", "Pay", "bearish"),
    Strategy("Bear Put Spread", "Moderate Bearish", "Limited", "Limited", "Pay", "bearish"),
    Strategy("Short Synthetic Future", "Strong Bearish", "Unlimited", "Unlimited", "Receive", "bearish"),
    Strategy("Bear Call Spread", "Moderate Bearish", "Limited", "Limited", "Receive", "bearish"),
    Strategy("Sell Call", "Moderate Bearish", "Limited", "Unlimited", "Receive", "bearish"),
    Strategy("Bear Condor", "Moderate Bearish", "Limited", "Limited", "Receive", "bearish"),
    Strategy("Bear Butterfly", "Mild Bearish", "Limited", "Limited", "Pay", "bearish"),
    Strategy("Reverse Jade Lizard", "Mild Bearish", "Limited (Premium)", "Unlimited", "Pay", "bearish"),

    # --- Neutral Strategies ---
    Strategy("Short Straddle", "Neutral High-Vol", "Limited (Premium)", "Unlimited", "Receive", "neutral"),
    Strategy("Short Strangle", "Neutral High-Vol", "Limited (Premium)", "Unlimited", "Receive", "neutral"),
    Strategy("Iron Butterfly", "Neutral High-Vol", "Limited (Premium)", "Limited", "Receive", "neutral"),
    Strategy("Iron Condor", "Neutral Low-Vol", "Limited (Premium)", "Limited", "Receive", "neutral"),
    Strategy("Calendar Spread", "Neutral Low-Vol", "Limited", "Limited", "Pay", "neutral"),
    Strategy("Short Iron Condor", "Range-bound", "Limited", "Limited", "Receive", "neutral"),
    Strategy("Batman", "Range-bound", "Limited", "Limited", "Pay", "neutral"),
    Strategy("Double Plateau", "Range-bound", "Limited", "Limited", "Receive", "neutral"),

    # --- Volatile Strategies ---
    Strategy("Strip", "Volatile Bias-Up", "Unlimited", "Limited (Premium)", "Pay", "volatile"),
    Strategy("Long Straddle", "Volatile Bias-Up", "Unlimited", "Limited (Premium)", "Pay", "volatile"),
    Strategy("Strap", "Volatile Bias-Down", "Unlimited", "Limited (Premium)", "Pay", "volatile"),
    Strategy("Long Strangle", "Volatile Bias-Down", "Unlimited", "Limited (Premium)", "Pay", "volatile"),
    Strategy("Long Iron Butterfly", "Volatile No-Bias", "Limited", "Limited", "Pay", "volatile"),
    Strategy("Long Iron Condor", "Volatile No-Bias", "Limited", "Limited", "Pay", "volatile"),
]

# Create a dictionary for easy lookup by name
ALL_STRATEGIES: Dict[str, Strategy] = {s.name: s for s in _all_strategies}

def get_strategies_by_view(market_view: str) -> List[Strategy]:
    """
    Returns a list of strategies from the config that match a given market view.
    e.g., market_view="Bullish" will return all bullish strategies (strong, moderate, mild).
    """
    view_lower = market_view.lower()
    conditions = CONFIG.get('strategy_selection', {}).get('market_conditions', {})

    if view_lower not in conditions:
        print(f"Warning: Market view '{view_lower}' not found in strategy configuration.")
        return []

    strategy_names = []
    # Get all strategy names for the given view from the config
    view_conditions = conditions[view_lower]
    for strength in view_conditions: # e.g., 'strong', 'moderate', 'mild'
        strategy_names.extend(view_conditions[strength])

    if not strategy_names:
        print(f"Warning: No strategies found in config for market view: {market_view}")
        return []

    # Get the full Strategy objects from our master list
    selected_strategies = []
    for name in strategy_names:
        # Normalize name from "buy_call" in config to "Buy Call" in our master list
        normalized_name = name.replace('_', ' ').title()
        if normalized_name in ALL_STRATEGIES:
            selected_strategies.append(ALL_STRATEGIES[normalized_name])
        else:
            print(f"Warning: Strategy '{name}' (normalized to '{normalized_name}') from config not found in master strategy list.")

    return selected_strategies

if __name__ == '__main__':
    print("--- Master Strategy List ---")
    print(f"Total strategies defined: {len(ALL_STRATEGIES)}")

    print("\n--- Testing get_strategies_by_view (from config) ---")

    # Test Bullish
    bullish_strategies = get_strategies_by_view("Bullish")
    print(f"\nFound {len(bullish_strategies)} strategies for 'Bullish' view:")
    for s in bullish_strategies:
        print(f"  - {s.name} (Type: {s.strategy_type})")

    # Test Neutral
    neutral_strategies = get_strategies_by_view("Neutral")
    print(f"\nFound {len(neutral_strategies)} strategies for 'Neutral' view:")
    for s in neutral_strategies:
        print(f"  - {s.name} (Type: {s.strategy_type})")

    # Test an unknown view
    unknown_strategies = get_strategies_by_view("Confused")
    print(f"\nFound {len(unknown_strategies)} strategies for 'Confused' view.")
    assert len(unknown_strategies) == 0
