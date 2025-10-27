from __future__ import annotations

from pathlib import Path

import typer

from src.broker import KiteBroker
from src.cfg import load_config
from src.data import DataCache, NSEClient
from src.exec import LiveExecutor
from src.utils import configure_logging

app = typer.Typer(help="Run live trading with Kite Connect")


class DataClient:
    def __init__(self) -> None:
        self.client = NSEClient(DataCache())

    def option_chain(self, symbol: str):
        return self.client.option_chain(symbol, use_cache=False)


@app.command()
def run(config_path: Path) -> None:
    configure_logging()
    bundle = load_config(config_path)
    broker = KiteBroker()
    executor = LiveExecutor(bundle.config, DataClient(), broker=broker)
    executor.start()


if __name__ == "__main__":
    app()
