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
