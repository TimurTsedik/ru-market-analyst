# quant/selftests/test_reprice.py
import numpy as np
from quant import reprice

def test_flat_curve_par_bond_prices_at_face():
    # 5% annual coupon, 3y, flat 5% curve → price ≈ 100
    times = np.array([1.0, 2.0, 3.0]); amounts = np.array([5.0, 5.0, 105.0])
    tenors = np.array([0.5, 1, 2, 3, 5]); yields = np.full(5, 5.0)
    px = reprice.price(times, amounts, tenors, yields, spread_bp=0.0)
    assert abs(px - 100.0) < 0.05

def test_zero_interp_linear():
    tenors = np.array([1.0, 3.0]); yields = np.array([10.0, 14.0])
    assert abs(reprice.zero_rate(tenors, yields, 2.0) - 12.0) < 1e-9   # linear midpoint

def test_higher_yield_lower_price():
    times = np.array([1.0, 2.0, 3.0]); amounts = np.array([5.0, 5.0, 105.0])
    tenors = np.array([0.5, 1, 2, 3, 5])
    p_lo = reprice.price(times, amounts, tenors, np.full(5, 5.0))
    p_hi = reprice.price(times, amounts, tenors, np.full(5, 7.0))
    assert p_hi < p_lo
