from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd


class DataCache:
    """Simple on-disk cache for time-series dataframes."""

    def __init__(self, root: str | Path = "data") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def path_for(self, key: str) -> Path:
        return self.root / f"{key}.parquet"

    def load(self, key: str) -> Optional[pd.DataFrame]:
        path = self.path_for(key)
        if not path.exists():
            return None
        return pd.read_parquet(path)

    def store(self, key: str, df: pd.DataFrame) -> Path:
        path = self.path_for(key)
        df.to_parquet(path)
        return path
