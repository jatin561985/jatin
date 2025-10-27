from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(slots=True)
class OrderRequest:
    symbol: str
    quantity: int
    order_type: str = "MARKET"
    product: str = "NRML"
    price: float | None = None
    variety: str = "regular"
    transaction_type: str = "SELL"


@dataclass(slots=True)
class OrderResponse:
    order_id: str
    status: str


class Broker(Protocol):
    def place_order(self, order: OrderRequest) -> OrderResponse:
        ...

    def exit_position(self, symbol: str) -> None:
        ...
