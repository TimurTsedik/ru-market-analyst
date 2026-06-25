# quant/reprice.py
import numpy as np

def zero_rate(tenors, yields, t):
    """Linear interpolation of the zero curve (percent). Flat-extrapolate beyond ends."""
    return float(np.interp(t, tenors, yields, left=yields[0], right=yields[-1]))

def price(times, amounts, tenors, yields, spread_bp=0.0):
    """Present value of cashflows discounted on the zero curve + credit spread (bp).
    Yields/spread in percent annual, continuous-ish via (1+y)^-t convention."""
    times = np.asarray(times, float); amounts = np.asarray(amounts, float)
    rates = np.array([zero_rate(tenors, yields, t) for t in times]) + spread_bp / 100.0
    disc = (1.0 + rates / 100.0) ** (-times)
    return float(np.sum(amounts * disc))

def cashflows(face, coupon_pct, freq, maturity, amort=None):
    """Return (times, amounts). amort: list of principal repaid each period (sums to face)."""
    n = int(round(maturity * freq))
    times = np.arange(1, n + 1) / freq
    c = coupon_pct / 100.0 / freq
    if amort is None:
        amounts = np.full(n, face * c)
        amounts[-1] += face
    else:
        amort = np.asarray(amort, float)
        outstanding = face - np.concatenate([[0], np.cumsum(amort)[:-1]])
        amounts = outstanding * c + amort
    return times, amounts

def total_return(cf, tenors, curve0, curve1, spread_bp=0.0, horizon=1.0):
    """(price_end + coupons paid within horizon) / price_start - 1.
    Cashflows still outstanding at horizon are re-timed to t-horizon and repriced on curve1."""
    times, amounts = cf
    p0 = price(times, amounts, tenors, curve0, spread_bp)
    paid = amounts[times <= horizon].sum()
    fut_mask = times > horizon
    p1 = price(times[fut_mask] - horizon, amounts[fut_mask], tenors, curve1, spread_bp)
    return (p1 + paid) / p0 - 1.0

def mod_duration(cf, tenors, yields, bump=0.01):
    times, amounts = cf
    p_up = price(times, amounts, tenors, yields + bump)
    p_dn = price(times, amounts, tenors, yields - bump)
    p0 = price(times, amounts, tenors, yields)
    return -(p_up - p_dn) / (2 * bump / 100.0) / p0
