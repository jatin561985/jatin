def calculate_slippage(price: float, slippage_percent: float) -> float:
    """
    Calculates the slippage amount for a given price.
    """
    return price * (slippage_percent / 100.0)

def apply_slippage(price: float, slippage_percent: float, side: str) -> float:
    """
    Applies slippage to a trade price.
    For buy orders, slippage increases the price.
    For sell orders, slippage decreases the price.
    """
    slippage = calculate_slippage(price, slippage_percent)
    if side == "BUY":
        return price + slippage
    else: # SELL
        return price - slippage

if __name__ == "__main__":
    entry_price = 100.0
    slippage_pct = 0.5

    buy_price_with_slippage = apply_slippage(entry_price, slippage_pct, "BUY")
    print(f"Buy price with {slippage_pct}% slippage: {buy_price_with_slippage}")

    sell_price_with_slippage = apply_slippage(entry_price, slippage_pct, "SELL")
    print(f"Sell price with {slippage_pct}% slippage: {sell_price_with_slippage}")
