from datetime import datetime
from typing import Dict, Any

class PaperBroker:
    """
    A mock broker for paper trading, simulating order execution.
    """
    def __init__(self, initial_capital: float):
        self.capital = initial_capital
        self.positions: Dict[str, Any] = {}
        self.orders: Dict[str, Any] = {}
        self.trade_log: list = []

    def place_order(self, symbol: str, quantity: int, price: float, side: str, order_type: str = "MARKET"):
        """
        Simulates placing an order.
        """
        order_id = f"order_{len(self.orders) + 1}"
        self.orders[order_id] = {
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
            "side": side,
            "status": "FILLED", # Assume immediate fill for simplicity
            "timestamp": datetime.now(),
        }
        # Update positions
        if symbol not in self.positions:
            self.positions[symbol] = {"quantity": 0, "avg_price": 0.0}

        current_qty = self.positions[symbol]["quantity"]
        current_avg_price = self.positions[symbol]["avg_price"]

        if side == "BUY":
            new_avg_price = ((current_avg_price * current_qty) + (price * quantity)) / (current_qty + quantity)
            self.positions[symbol]["avg_price"] = new_avg_price
            self.positions[symbol]["quantity"] += quantity
        else: # SELL
            # For shorting, avg price logic might differ based on how you track PnL
            # This is a simplified version
            self.positions[symbol]["quantity"] -= quantity

        self.trade_log.append(self.orders[order_id])
        return order_id

    def modify_order(self, order_id: str, new_price: float):
        """
        Simulates modifying an order.
        """
        if order_id in self.orders:
            self.orders[order_id]["price"] = new_price
            return True
        return False

    def exit_order(self, order_id: str):
        """
        Simulates exiting an order (simplified).
        """
        if order_id in self.orders:
            self.orders[order_id]["status"] = "CANCELLED"
            return True
        return False

if __name__ == "__main__":
    broker = PaperBroker(initial_capital=50000000)
    order_id = broker.place_order("NIFTY25000CE", 75, 100.0, "SELL")
    print(f"Placed order: {order_id}")
    print(f"Positions: {broker.positions}")
    print(f"Orders: {broker.orders}")
