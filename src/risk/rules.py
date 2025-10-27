from typing import Dict, Any

def check_stop_loss(positions: Dict[str, Any], current_prices: Dict[str, float], stop_loss_percent: float) -> bool:
    """
    Checks if the combined stop-loss has been hit.
    """
    total_pnl = 0.0
    for symbol, position in positions.items():
        entry_price = position["avg_price"]
        current_price = current_prices.get(symbol, entry_price)
        quantity = position["quantity"]
        pnl = (entry_price - current_price) * quantity # For short positions
        total_pnl += pnl

    # This is a simplified MTM SL based on entry premium
    # A more robust implementation would track the initial premium collected
    initial_premium = sum(pos["avg_price"] * pos["quantity"] for pos in positions.values())

    if initial_premium > 0 and (total_pnl / initial_premium) < -(stop_loss_percent / 100.0):
        return True
    return False

def check_profit_target(pnl: float, profit_target_amount: float) -> bool:
    """
    Checks if the profit target has been reached.
    """
    return pnl >= profit_target_amount

if __name__ == "__main__":
    mock_positions = {
        "NIFTY25000CE": {"quantity": 75, "avg_price": 100.0},
        "NIFTY25000PE": {"quantity": 75, "avg_price": 100.0},
    }

    # SL hit scenario
    mock_current_prices_sl = {
        "NIFTY25000CE": 140.0,
        "NIFTY25000PE": 140.0,
    }
    sl_hit = check_stop_loss(mock_positions, mock_current_prices_sl, stop_loss_percent=70.0)
    print(f"Stop-loss hit: {sl_hit}")

    # Profit target hit scenario
    pnl = 150000.0
    profit_target = 125000.0
    pt_hit = check_profit_target(pnl, profit_target)
    print(f"Profit-target hit: {pt_hit}")
