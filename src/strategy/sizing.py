def lots_allowed(P0: float, lot_size: int, risk_budget: float, sl_pct: float, margin_cap_lots: int, liq_cap_lots: int) -> int:
    """
    Calculates the number of lots to trade based on risk, margin, and liquidity.

    Args:
        P0: Entry price of the instrument.
        lot_size: The number of shares per lot.
        risk_budget: The maximum amount of money to risk on this trade.
        sl_pct: The stop-loss percentage.
        margin_cap_lots: The maximum number of lots allowed by margin.
        liq_cap_lots: The maximum number of lots allowed by liquidity.

    Returns:
        The number of lots to trade.
    """
    per_lot_loss = sl_pct * P0 * lot_size
    if per_lot_loss <= 0:
        return 0

    risk_lots = int(risk_budget // per_lot_loss)
    return max(0, min(risk_lots, margin_cap_lots, liq_cap_lots))

if __name__ == "__main__":
    entry_price = 100.0
    lot_size = 75
    daily_risk_budget = 125000.0 # 0.25% of 5 Cr
    stop_loss_percent = 0.7 # 70% SL on the premium
    margin_lots = 100
    liquidity_lots = 100

    num_lots = lots_allowed(
        P0=entry_price,
        lot_size=lot_size,
        risk_budget=daily_risk_budget,
        sl_pct=stop_loss_percent,
        margin_cap_lots=margin_lots,
        liq_cap_lots=liquidity_lots
    )

    print(f"Lots allowed: {num_lots}")
    per_lot_loss = stop_loss_percent * entry_price * lot_size
    print(f"Per lot loss: ₹{per_lot_loss}")
    total_risk = num_lots * per_lot_loss
    print(f"Total risk for {num_lots} lots: ₹{total_risk}")
