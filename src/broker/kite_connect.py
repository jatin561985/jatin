from __future__ import annotations

import os
from typing import Optional

try:
    from kiteconnect import KiteConnect
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    KiteConnect = None  # type: ignore[assignment]

from loguru import logger

from .base import Broker, OrderRequest, OrderResponse


class KiteBroker(Broker):
    def __init__(self, api_key: Optional[str] = None, access_token: Optional[str] = None) -> None:
        if KiteConnect is None:
            raise RuntimeError("kiteconnect package not available. Install kiteconnect to use KiteBroker")
        api_key = api_key or os.getenv("KITE_API_KEY")
        access_token = access_token or os.getenv("KITE_ACCESS_TOKEN")
        if not api_key or not access_token:
            raise RuntimeError("KITE_API_KEY and KITE_ACCESS_TOKEN must be set")
        self.client = KiteConnect(api_key=api_key)
        self.client.set_access_token(access_token)
        logger.info("KiteBroker initialized for API key %s", api_key)

    def place_order(self, order: OrderRequest) -> OrderResponse:
        logger.info("Placing order %s", order)
        response = self.client.place_order(
            variety=order.variety,
            exchange="NFO",
            tradingsymbol=order.symbol,
            transaction_type=order.transaction_type,
            quantity=abs(order.quantity),
            order_type=order.order_type,
            product=order.product,
            price=order.price or 0.0,
        )
        return OrderResponse(order_id=response["order_id"], status="placed")

    def exit_position(self, symbol: str) -> None:
        logger.info("Exiting position %s", symbol)
        self.client.exit_order(order_id=symbol)
