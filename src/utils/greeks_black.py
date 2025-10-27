from __future__ import annotations

import math
from typing import Literal

from scipy.stats import norm


OptionType = Literal["call", "put"]


def black_scholes_price(
    option_type: OptionType,
    spot: float,
    strike: float,
    time_to_expiry: float,
    rate: float,
    volatility: float,
) -> float:
    if time_to_expiry <= 0 or volatility <= 0:
        intrinsic = max(0.0, spot - strike) if option_type == "call" else max(0.0, strike - spot)
        return intrinsic
    d1 = (math.log(spot / strike) + (rate + 0.5 * volatility**2) * time_to_expiry) / (volatility * math.sqrt(time_to_expiry))
    d2 = d1 - volatility * math.sqrt(time_to_expiry)
    if option_type == "call":
        return spot * norm.cdf(d1) - strike * math.exp(-rate * time_to_expiry) * norm.cdf(d2)
    return strike * math.exp(-rate * time_to_expiry) * norm.cdf(-d2) - spot * norm.cdf(-d1)


def black_scholes_delta(option_type: OptionType, spot: float, strike: float, time_to_expiry: float, rate: float, volatility: float) -> float:
    if time_to_expiry <= 0 or volatility <= 0:
        return 1.0 if option_type == "call" and spot > strike else -1.0 if option_type == "put" and spot < strike else 0.0
    d1 = (math.log(spot / strike) + (rate + 0.5 * volatility**2) * time_to_expiry) / (volatility * math.sqrt(time_to_expiry))
    if option_type == "call":
        return norm.cdf(d1)
    return norm.cdf(d1) - 1
