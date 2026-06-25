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

def test_cashflows_fixed_and_amortizing():
    cf = reprice.cashflows(face=100, coupon_pct=8.0, freq=1, maturity=3)
    assert np.allclose(cf[0], [1, 2, 3]) and np.allclose(cf[1], [8, 8, 108])
    cfa = reprice.cashflows(face=100, coupon_pct=8.0, freq=1, maturity=2,
                            amort=[50, 50])   # 50 principal each year
    # year1: coupon 8 + amort 50; year2: coupon on remaining 50 = 4 + amort 50
    assert np.allclose(cfa[1], [58, 54])

def test_total_return_sign():
    cf = reprice.cashflows(face=100, coupon_pct=8.0, freq=1, maturity=3)
    tenors = np.array([0.5,1,2,3,5])
    tr = reprice.total_return(cf, tenors, np.full(5,8.0), np.full(5,6.0),
                              spread_bp=0.0, horizon=1.0)
    assert tr > 0      # rates fell 8→6 over horizon → positive total return

def test_mod_duration_positive_and_finite_diff():
    cf = reprice.cashflows(face=100, coupon_pct=8.0, freq=1, maturity=5)
    tenors = np.array([0.5,1,2,3,5,7]); y = np.full(6,8.0)
    d = reprice.mod_duration(cf, tenors, y)
    assert 3.0 < d < 5.0
