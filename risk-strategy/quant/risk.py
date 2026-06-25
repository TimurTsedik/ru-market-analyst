# quant/risk.py
import numpy as np

def var(losses, alpha):
    return float(np.quantile(losses, alpha))

def es(losses, alpha):
    v = var(losses, alpha)
    tail = losses[losses >= v]
    return float(tail.mean()) if tail.size else v

def percentiles(values, pcts):
    return np.percentile(values, pcts)

def prob_loss_beyond(losses, threshold):
    return float(np.mean(losses > threshold))

def component_es(position_losses, alpha):
    """Euler/Expected-Shortfall contribution: E[L_i | L_port >= VaR_port]. Sums to portfolio ES."""
    port = position_losses.sum(axis=1)
    v = var(port, alpha)
    mask = port >= v
    return position_losses[mask].mean(axis=0)

def fan_chart_data(path_values, pcts=(5, 25, 50, 75, 95)):
    """path_values: (n_paths, n_steps). Returns dict pct->(n_steps,) bands."""
    return {p: np.percentile(path_values, p, axis=0) for p in pcts}

def es_standard_error(losses, alpha, n_batches=20):
    """Batch-means standard error of the ES estimate — MC convergence diagnostic.
    Warn upstream if the tail sample (n_paths*(1-alpha)) is small."""
    batches = [b for b in np.array_split(np.asarray(losses), n_batches) if len(b)]
    ests = np.array([es(b, alpha) for b in batches])
    return float(ests.std(ddof=1) / np.sqrt(len(ests)))
