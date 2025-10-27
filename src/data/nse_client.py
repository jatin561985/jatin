from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd
import requests
from loguru import logger

from .cache import DataCache

NSE_OPTION_CHAIN_URL = "https://www.nseindia.com/api/option-chain-indices"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.nseindia.com/option-chain"
}


class NSEClient:
    def __init__(self, cache: Optional[DataCache] = None, session: Optional[requests.Session] = None) -> None:
        self.cache = cache or DataCache()
        self.session = session or requests.Session()

    def _fetch_json(self, symbol: str) -> Dict[str, Any]:
        params = {"symbol": symbol}
        response = self.session.get(NSE_OPTION_CHAIN_URL, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def option_chain(self, symbol: str, expiry: Optional[str] = None, use_cache: bool = True) -> pd.DataFrame:
        cache_key = f"option_chain_{symbol}_{expiry or 'latest'}"
        if use_cache and (cached := self.cache.load(cache_key)) is not None:
            return cached
        try:
            payload = self._fetch_json(symbol)
        except Exception as exc:  # noqa: BLE001 - network errors should be logged and re-raised
            logger.error("Failed to fetch option chain for %s: %s", symbol, exc)
            raise
        records = self._parse_option_chain(payload, expiry)
        df = pd.DataFrame(records)
        if use_cache:
            self.cache.store(cache_key, df)
        return df

    def _parse_option_chain(self, payload: Dict[str, Any], expiry: Optional[str]) -> list[Dict[str, Any]]:
        records: list[Dict[str, Any]] = []
        timestamp = datetime.utcnow()
        data = payload.get("records", {}).get("data", [])
        for item in data:
            if expiry and item.get("expiryDate") != expiry:
                continue
            ce = item.get("CE")
            pe = item.get("PE")
            if ce:
                records.append(self._extract_contract(ce, timestamp, "CE"))
            if pe:
                records.append(self._extract_contract(pe, timestamp, "PE"))
        return records

    @staticmethod
    def _extract_contract(raw: Dict[str, Any], timestamp: datetime, option_type: str) -> Dict[str, Any]:
        return {
            "timestamp": timestamp,
            "strike": raw.get("strikePrice"),
            "expiry": raw.get("expiryDate"),
            "type": option_type,
            "last_price": raw.get("lastPrice"),
            "open_interest": raw.get("openInterest"),
            "change_in_oi": raw.get("changeinOpenInterest"),
            "iv": raw.get("impliedVolatility"),
            "underlying_value": raw.get("underlyingValue"),
        }


def load_cached_index(path: str | Path) -> pd.DataFrame:
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"Index file {source} not found")
    df = pd.read_csv(source, parse_dates=["timestamp"])
    return df.sort_values("timestamp").set_index("timestamp")
