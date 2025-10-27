from __future__ import annotations

import time

import schedule
from loguru import logger

from ..broker import Broker, OrderRequest, PaperBroker
from ..risk import RiskManager
from ..strategy import StraddleBuilder


class LiveExecutor:
    def __init__(self, config, data_client, broker: Broker | None = None) -> None:
        self.config = config
        self.data_client = data_client
        self.broker = broker or PaperBroker()
        self.risk_manager = RiskManager(config)

    def start(self) -> None:
        schedule.every().day.at(self.config.entry.start_time.strftime("%H:%M")).do(self.execute_open)
        schedule.every().day.at(self.config.exit.hard_stop_time.strftime("%H:%M")).do(self.close_all)
        logger.info("LiveExecutor started")
        while True:
            schedule.run_pending()
            time.sleep(1)

    def execute_open(self) -> None:
        option_chain = self.data_client.option_chain(self.config.underlying)
        underlying_price = option_chain["underlying_value"].dropna().iloc[-1]
        builder = StraddleBuilder(self.config, option_chain)
        position = builder.build(underlying_price)
        if position is None:
            logger.warning("No position opened")
            return
        for leg in (position.ce, position.pe):
            order = OrderRequest(symbol=leg.symbol, quantity=leg.quantity, order_type=self.config.entry.order_type.upper())
            self.broker.place_order(order)
        logger.info("Opened straddle %s", position.to_dict())

    def close_all(self) -> None:
        logger.info("Closing all positions via risk manager")
