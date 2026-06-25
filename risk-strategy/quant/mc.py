# quant/mc.py
import numpy as np
from . import curve as _curve, reprice as _reprice

def simulate_book(positions, base_yields, tenors, pca, n_paths, horizon, seed,
                  horizon_scale=None):
    rng = np.random.default_rng(seed)
    base_yields = np.asarray(base_yields, float); tenors = np.asarray(tenors, float)
    scale = horizon_scale if horizon_scale is not None else horizon * 252
    curve1 = _curve.simulate_curve_terminal(base_yields, pca, n_paths, rng, scale)
    weights = np.array([p["weight"] for p in positions])
    pos_ret = np.empty((n_paths, len(positions)))
    for j, p in enumerate(positions):
        cf = _reprice.cashflows(p["face"], p["coupon_pct"], p["freq"], p["maturity"],
                                p.get("amort"))
        sp = p.get("spread_bp", 0.0)
        for i in range(n_paths):
            pos_ret[i, j] = _reprice.total_return(cf, tenors, base_yields, curve1[i],
                                                  sp, horizon)
    port_ret = pos_ret @ weights
    return {"port_return": port_ret, "pos_return": pos_ret, "weights": weights}
