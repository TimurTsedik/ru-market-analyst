# quant/selftests/test_risk.py
import numpy as np
from quant import risk

def test_var_es_ordering_and_known_normal():
    rng = np.random.default_rng(7)
    losses = rng.normal(0, 1, 200000)               # loss distribution
    v = risk.var(losses, 0.95); e = risk.es(losses, 0.95)
    assert abs(v - 1.645) < 0.05                     # normal 95% VaR ≈ 1.645σ
    assert e >= v                                    # ES ≥ VaR
    assert abs(e - 2.063) < 0.05                     # normal 95% ES ≈ 2.063σ

def test_component_es_sums_to_portfolio_es():
    rng = np.random.default_rng(8)
    pos = rng.normal(0, 1, (50000, 3))               # per-position losses
    comp = risk.component_es(pos, 0.95)
    port = risk.es(pos.sum(axis=1), 0.95)
    assert abs(comp.sum() - port) < 1e-6             # Euler allocation is additive

def test_prob_loss_and_percentiles():
    losses = np.linspace(-10, 10, 1001)   # step 0.02; values >5 are (5.02..10] = 250 points
    assert abs(risk.prob_loss_beyond(losses, 5.0) - 250/1001) < 0.01
    p = risk.percentiles(losses, [5, 50, 95])
    assert p[1] == 0.0

def test_es_standard_error_shrinks_with_n():
    rng = np.random.default_rng(11)
    se_small = risk.es_standard_error(rng.normal(0, 1, 20000), 0.95)
    se_big = risk.es_standard_error(rng.normal(0, 1, 400000), 0.95)
    assert se_big < se_small and se_big > 0
