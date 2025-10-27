from __future__ import annotations

from pathlib import Path

import typer
from loguru import logger

from src.cfg import load_config
from src.data import DataCache, NSEClient

app = typer.Typer(help="Fetch and cache NSE option chain data")


@app.command()
def fetch(config_path: Path, expiry: str | None = typer.Option(None)) -> None:
    bundle = load_config(config_path)
    client = NSEClient(DataCache())
    df = client.option_chain(bundle.config.underlying, expiry)
    output_path = Path("data") / f"{bundle.config.underlying}_option_chain.csv"
    df.to_csv(output_path, index=False)
    logger.info("Saved option chain to %s", output_path)


if __name__ == "__main__":
    app()
