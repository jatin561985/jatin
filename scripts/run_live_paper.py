from __future__ import annotations

from pathlib import Path

import typer

from src.cfg import load_config
from src.data import DataCache, NSEClient
from src.exec import LiveExecutor
from src.utils import configure_logging

app = typer.Typer(help="Run live paper trading loop")


class DataClient:
    def __init__(self) -> None:
        self.client = NSEClient(DataCache())

    def option_chain(self, symbol: str):
        return self.client.option_chain(symbol)


@app.command()
def run(config_path: Path) -> None:
    configure_logging()
    bundle = load_config(config_path)
    executor = LiveExecutor(bundle.config, DataClient())
    executor.start()


if __name__ == "__main__":
    app()
