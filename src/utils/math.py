from __future__ import annotations

import numpy as np


def annualized_return(returns: np.ndarray, periods_per_year: int = 252) -> float:
    if returns.size == 0:
        return 0.0
    compounded = np.prod(1 + returns)
    years = returns.size / periods_per_year
    return compounded ** (1 / years) - 1 if years > 0 else 0.0
