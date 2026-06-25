# quant/mc.py
import numpy as np
from . import curve as _curve, reprice as _reprice

def simulate_book(positions, base_yields, tenors, pca, n_paths, horizon, seed,
                  horizon_scale=None, credit_on=False, include_drift=False,
                  student_t_df=None, jump_prob=0.0, jump_scale=0.0,
                  recovery_factor_load=0.15):
    rng = np.random.default_rng(seed)
    base_yields = np.asarray(base_yields, float); tenors = np.asarray(tenors, float)
    scale = horizon_scale if horizon_scale is not None else horizon * 252
    curve1 = _curve.simulate_curve_terminal(base_yields, pca, n_paths, rng, scale,
                                            include_drift=include_drift, student_t_df=student_t_df,
                                            jump_prob=jump_prob, jump_scale=jump_scale)
    weights = np.array([p["weight"] for p in positions])
    pos_ret = np.empty((n_paths, len(positions)))
    for j, p in enumerate(positions):
        cf = _reprice.cashflows(p["face"], p["coupon_pct"], p["freq"], p["maturity"],
                                p.get("amort"))
        sp = p.get("spread_bp", 0.0)
        for i in range(n_paths):
            pos_ret[i, j] = _reprice.total_return(cf, tenors, base_yields, curve1[i],
                                                  sp, horizon)
    if credit_on and any("pd" in p for p in positions):
        from . import credit as _credit
        # a position carrying default risk must specify all three — no silent hardcoded default
        for p in positions:
            if "pd" in p and ("beta" not in p or "mean_rr" not in p):
                raise ValueError("credit position with pd needs beta and mean_rr (no silent default)")
        pd = np.array([p.get("pd", 0.0) for p in positions])
        beta = np.array([p.get("beta", 0.0) for p in positions])
        mean_rr = np.array([p.get("mean_rr", 0.4) for p in positions])
        dmask, Z = _credit.simulate_defaults(pd, beta, n_paths, seed + 2)
        # recovery per (path, obligor) tied to the SAME systematic factor Z (neg PD-recovery);
        # recovery_factor_load is a flagged assumption surfaced in run.py output
        rr_paths = np.column_stack([_credit.recovery(Z, mean_rr[j], recovery_factor_load)
                                    for j in range(len(positions))])
        # FLAGGED ASSUMPTION: default at horizon → defaulted position returns (recovery - 1)
        # relative to its start mark (coupons-to-default folded into mark/spread). MVP
        # relative-loss; precise default-timing/coupon-accrual is a later refinement.
        pos_ret = np.where(dmask, rr_paths - 1.0, pos_ret)
    port_ret = pos_ret @ weights
    return {"port_return": port_ret, "pos_return": pos_ret, "weights": weights}
