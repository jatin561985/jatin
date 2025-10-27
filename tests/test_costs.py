from src.costs import option_transaction_cost


def test_transaction_cost_components_sum():
    breakdown = option_transaction_cost(1_000_000, trades=4, brokerage_per_trade=20)
    assert breakdown.total == breakdown.brokerage + breakdown.exchange_fees + breakdown.sebi_charges + breakdown.gst + breakdown.stamp_duty
    assert breakdown.brokerage == 80
