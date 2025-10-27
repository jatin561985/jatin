from __future__ import annotations

import itertools
from typing import Dict

from loguru import logger

from .base import Broker, OrderRequest, OrderResponse


class PaperBroker(Broker):
    _ids = itertools.count(1)

    def __init__(self) -> None:
        self.positions: Dict[str, int] = {}

    def place_order(self, order: OrderRequest) -> OrderResponse:
        order_id = f"paper_{next(self._ids)}"
        logger.info("Paper fill for %s", order)
        self.positions[order.symbol] = self.positions.get(order.symbol, 0) + order.quantity
        return OrderResponse(order_id=order_id, status="filled")

    def exit_position(self, symbol: str) -> None:
        if symbol in self.positions:
            logger.info("Paper exit %s", symbol)
            del self.positions[symbol]
