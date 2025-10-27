import pytest
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.strategy.sizing import lots_allowed

def test_lots_allowed():
    """
    Tests the lots_allowed function with various scenarios.
    """
    # Basic scenario
    assert lots_allowed(P0=100, lot_size=75, risk_budget=10000, sl_pct=0.5, margin_cap_lots=100, liq_cap_lots=100) == 2

    # Risk budget allows zero lots
    assert lots_allowed(P0=100, lot_size=75, risk_budget=1000, sl_pct=0.5, margin_cap_lots=100, liq_cap_lots=100) == 0

    # Margin limited
    assert lots_allowed(P0=100, lot_size=75, risk_budget=100000, sl_pct=0.5, margin_cap_lots=5, liq_cap_lots=100) == 5

    # Liquidity limited
    assert lots_allowed(P0=100, lot_size=75, risk_budget=100000, sl_pct=0.5, margin_cap_lots=100, liq_cap_lots=3) == 3

    # Zero stop-loss
    assert lots_allowed(P0=100, lot_size=75, risk_budget=10000, sl_pct=0, margin_cap_lots=100, liq_cap_lots=100) == 0

if __name__ == "__main__":
    pytest.main()
