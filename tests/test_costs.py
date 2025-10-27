import pytest
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.costs.slippage import apply_slippage
from src.costs.transactions import calculate_total_transaction_cost

def test_apply_slippage():
    """
    Tests the apply_slippage function.
    """
    assert apply_slippage(100.0, 0.5, "BUY") == 100.5
    assert apply_slippage(100.0, 0.5, "SELL") == 99.5

def test_calculate_total_transaction_cost():
    """
    Tests the calculate_total_transaction_cost function.
    """
    assert calculate_total_transaction_cost(100.0, 10, 20.0) == 200.0

if __name__ == "__main__":
    pytest.main()
