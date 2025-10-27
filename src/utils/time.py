from __future__ import annotations

from datetime import datetime

import pandas as pd
import pytz


IST = pytz.timezone("Asia/Kolkata")


def now_ist() -> datetime:
    return datetime.now(tz=IST)


def ensure_ist_index(df: pd.DataFrame) -> pd.DataFrame:
    if df.index.tzinfo is None:
        df = df.tz_localize(IST)
    else:
        df = df.tz_convert(IST)
    return df
