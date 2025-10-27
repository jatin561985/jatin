from src.strategy import lots_allowed


def test_lots_allowed_respects_caps():
    result = lots_allowed(
        premium=200.0,
        lot_size=75,
        risk_budget=125000.0,
        sl_pct=0.3,
        margin_cap_lots=10,
        liq_cap_lots=8,
    )
    assert result.lots == 8
    assert result.per_lot_loss == 4500.0
