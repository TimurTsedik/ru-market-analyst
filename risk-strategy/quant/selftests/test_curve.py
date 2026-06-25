# quant/selftests/test_curve.py
import numpy as np
from quant import curve

def test_pca_recovers_dominant_factor():
    rng = np.random.default_rng(0)
    n_tenors = 8
    level = np.ones(n_tenors)
    scores = rng.normal(0, 1.0, size=400)
    yields_hist = 10.0 + np.outer(scores, level) + rng.normal(0, 0.01, (400, n_tenors))
    pca = curve.pca_factors(yields_hist, n_factors=3)
    assert pca["components"].shape == (3, n_tenors)
    assert pca["explained"][0] > 0.95                      # one dominant level factor
    assert pca["factor_cov"].shape == (3, 3)

def test_pca_reconstruct_roundtrip():
    rng = np.random.default_rng(1)
    yields_hist = 10 + rng.normal(0, 0.5, (300, 6))
    pca = curve.pca_factors(yields_hist, n_factors=3)
    base = yields_hist[-1]
    paths = curve.simulate_curve_terminal(base, pca, n_paths=5000,
                                           rng=np.random.default_rng(2))
    assert paths.shape == (5000, 6)
    assert np.allclose(paths.mean(axis=0), base, atol=0.05)  # zero-mean innovations
