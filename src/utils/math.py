def calculate_pnl(entry_price: float, exit_price: float, quantity: int, side: str) -> float:
    """
    Calculates the Profit and Loss (PnL) for a trade.
    """
    if side == "BUY":
        return (exit_price - entry_price) * quantity
    else: # SELL
        return (entry_price - exit_price) * quantity
