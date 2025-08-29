from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Strategy:
    """A dataclass to hold the definition of a trading strategy."""
    name: str
    market_view: str
    max_profit: str
    max_loss: str
    premium: str
    strategy_type: str  # 'bullish', 'bearish', 'neutral', 'volatile'

# Using the user-provided list to define strategies.
# This is a representative sample. A full implementation would include all strategies.

_all_strategies = [
    # --- Bullish Strategies ---
    Strategy("Buy Call", "Bullish", "Unlimited", "Limited (Premium Paid)", "Pay", "bullish"),
    Strategy("Sell Put", "Moderately Bullish", "Limited (Premium Received)", "Unlimited", "Receive", "bullish"),
    Strategy("Bull Call Spread", "Moderately Bullish", "Limited", "Limited (Net Premium Paid)", "Pay", "bullish"),
    Strategy("Bull Put Spread", "Mildly Bullish", "Limited (Net Premium Received)", "Limited", "Receive", "bullish"),
    Strategy("Buy Future", "Bullish", "Unlimited", "Unlimited", "N/A", "bullish"),

    # --- Bearish Strategies ---
    Strategy("Buy Put", "Bearish", "Unlimited", "Limited (Premium Paid)", "Pay", "bearish"),
    Strategy("Sell Call", "Moderately Bearish", "Limited (Premium Received)", "Unlimited", "Receive", "bearish"),
    Strategy("Bear Call Spread", "Mildly Bearish", "Limited (Net Premium Received)", "Limited", "Receive", "bearish"),
    Strategy("Bear Put Spread", "Moderately Bearish", "Limited", "Limited (Net Premium Paid)", "Pay", "bearish"),
    Strategy("Sell Future", "Bearish", "Unlimited", "Unlimited", "N/A", "bearish"),

    # --- Neutral Strategies ---
    Strategy("Short Straddle", "Neutral", "Limited (Net Premium Received)", "Unlimited", "Receive", "neutral"),
    Strategy("Short Strangle", "Neutral", "Limited (Net Premium Received)", "Unlimited", "Receive", "neutral"),
    Strategy("Iron Butterfly", "Neutral", "Limited (Net Premium Received)", "Limited", "Receive", "neutral"),
    Strategy("Short Iron Condor", "Neutral", "Limited (Net Premium Received)", "Limited", "Receive", "neutral"),

    # --- Volatile Strategies (Expecting a big move) ---
    Strategy("Long Straddle", "Highly Volatile", "Unlimited", "Limited (Net Premium Paid)", "Pay", "volatile"),
    Strategy("Long Strangle", "Volatile", "Unlimited", "Limited (Net Premium Paid)", "Pay", "volatile"),
]

# Create dictionaries for easy lookup
ALL_STRATEGIES: Dict[str, Strategy] = {s.name: s for s in _all_strategies}
BULLISH_STRATEGIES: Dict[str, Strategy] = {s.name: s for s in _all_strategies if s.strategy_type == 'bullish'}
BEARISH_STRATEGIES: Dict[str, Strategy] = {s.name: s for s in _all_strategies if s.strategy_type == 'bearish'}
NEUTRAL_STRATEGIES: Dict[str, Strategy] = {s.name: s for s in _all_strategies if s.strategy_type == 'neutral'}
VOLATILE_STRATEGIES: Dict[str, Strategy] = {s.name: s for s in _all_strategies if s.strategy_type == 'volatile'}


def get_strategies_by_view(market_view: str) -> List[Strategy]:
    """
    Returns a list of strategies matching a given market view.
    e.g., market_view="Bullish" or market_view="Neutral"
    """
    view_lower = market_view.lower()

    # Simple mapping from a general view to our strategy types
    if 'bullish' in view_lower:
        return list(BULLISH_STRATEGIES.values())
    if 'bearish' in view_lower:
        return list(BEARISH_STRATEGIES.values())
    if 'neutral' in view_lower:
        return list(NEUTRAL_STRATEGIES.values())
    if 'volatile' in view_lower:
        return list(VOLATILE_STRATEGIES.values())

    return []

if __name__ == '__main__':
    print("--- Bullish Strategies ---")
    for name, s in BULLISH_STRATEGIES.items():
        print(f"  - {name}: {s.market_view}")

    print("\n--- Testing get_strategies_by_view ---")
    bullish_strategies = get_strategies_by_view("Bullish")
    print(f"Found {len(bullish_strategies)} strategies for 'Bullish' view:")
    for s in bullish_strategies:
        print(f"  - {s.name}")

    neutral_strategies = get_strategies_by_view("Neutral")
    print(f"Found {len(neutral_strategies)} strategies for 'Neutral' view:")
    for s in neutral_strategies:
        print(f"  - {s.name}")
