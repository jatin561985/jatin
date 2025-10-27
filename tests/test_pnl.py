import pytest
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.math import calculate_pnl

def test_calculate_pnl():
    """
    Tests the calculate_pnl function.
    """
    # Long position profit
    assert calculate_pnl(100.0, 110.0, 10, "BUY") == 100.0
    # Long position loss
    assert calculate_pnl(100.0, 90.0, 10, "BUY") == -100.0
    # Short position profit
    assert calculate_pnl(100.0, 90.0, 10, "SELL") == 100.0
    # Short position loss
    assert calculate_pnl(100.0, 110.0, 10, "SELL") == -100.0

if __name__ == "__main__":
    pytest.main()
