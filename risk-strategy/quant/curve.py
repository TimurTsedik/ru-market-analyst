# quant/curve.py
import numpy as np

def pca_factors(yields_hist, n_factors=3):
    """PCA on daily yield CHANGES. yields_hist: (n_days, n_tenors)."""
    changes = np.diff(yields_hist, axis=0)
    mean_change = changes.mean(axis=0)
    X = changes - mean_change
    cov = np.cov(X, rowvar=False)
    vals, vecs = np.linalg.eigh(cov)
    order = np.argsort(vals)[::-1]
    vals, vecs = vals[order], vecs[:, order]
    comps = vecs[:, :n_factors].T                      # (n_factors, n_tenors)
    explained = (vals[:n_factors] / vals.sum())
    scores = X @ vecs[:, :n_factors]                   # (n_days-1, n_factors)
    factor_cov = np.cov(scores, rowvar=False)
    if np.ndim(factor_cov) == 0:
        factor_cov = factor_cov.reshape(1, 1)
    return {"components": comps, "explained": explained,
            "factor_cov": factor_cov, "mean_change": mean_change}

def simulate_curve_terminal(base_yields, pca, n_paths, rng, horizon_scale=1.0,
                            include_drift=False):
    """Correlated factor innovations → yield changes → terminal curve.
    horizon_scale scales the factor covariance to the horizon: pass
    horizon_years*trading_days_per_year for i.i.d. random-walk daily changes (no
    autocorrelation/mean-reversion assumed — a flagged modelling choice).
    include_drift=False (default) = no-drift risk view; True adds mean_change*horizon_scale."""
    k = pca["factor_cov"].shape[0]
    L = np.linalg.cholesky(pca["factor_cov"] * horizon_scale + 1e-12 * np.eye(k))
    z = rng.standard_normal((n_paths, k))
    factor_draws = z @ L.T
    dy = factor_draws @ pca["components"]              # (n_paths, n_tenors)
    if include_drift:
        dy = dy + pca["mean_change"] * horizon_scale
    return base_yields + dy
