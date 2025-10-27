# A simplified transaction cost model for Indian markets
# In a real scenario, this would be much more detailed, including STT, exchange fees, etc.

def calculate_brokerage(price: float, quantity: int, brokerage_per_lot: float) -> float:
    """
    Calculates the brokerage fee.
    This is a simplified model assuming a flat fee per lot.
    """
    return brokerage_per_lot * quantity

def calculate_total_transaction_cost(price: float, quantity: int, brokerage_per_lot: float) -> float:
    """
    Calculates the total transaction cost for a trade.
    """
    brokerage = calculate_brokerage(price, quantity, brokerage_per_lot)
    # Add other charges like STT, GST, etc. here
    # For simplicity, we are only considering brokerage for now.
    return brokerage

if __name__ == "__main__":
    trade_price = 100.0
    num_lots = 10
    brokerage_fee_per_lot = 20.0 # Zerodha's F&O brokerage

    total_cost = calculate_total_transaction_cost(trade_price, num_lots, brokerage_fee_per_lot)
    print(f"Total transaction cost for {num_lots} lots: ₹{total_cost}")
