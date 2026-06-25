# quant/run.py
import json, sys
import numpy as np
from . import curve as _curve, mc as _mc, risk as _risk

def run_analysis(portfolio, config):
    tenors = np.asarray(portfolio["tenors"], float)
    pca = _curve.pca_factors(np.asarray(portfolio["yields_hist"], float),
                             config.get("n_factors", 3))
    out = _mc.simulate_book(portfolio["positions"], portfolio["base_yields"], tenors,
                            pca, config["n_paths"], config["horizon"], config["seed"])
    losses = -out["port_return"]                      # loss = negative return
    a = config.get("alpha", 0.95)
    pos_losses = -out["pos_return"] * out["weights"]
    return {
        "asof": portfolio.get("asof"),
        "var": _risk.var(losses, a), "es": _risk.es(losses, a),
        "percentiles": {str(p): float(v) for p, v in
                        zip([5,50,95], _risk.percentiles(out["port_return"], [5,50,95]))},
        "prob_loss_beyond_0": _risk.prob_loss_beyond(losses, 0.0),
        "components": [float(x) for x in _risk.component_es(pos_losses, a)],
        "fan_chart": {str(k): [float(x)] for k, v in
                      _risk.fan_chart_data(out["port_return"][:, None]).items() for x in [v[0]]},
        "n_paths": config["n_paths"], "explained_var": [float(x) for x in pca["explained"]],
        "model_risk": "MC informs ordinal scoring; correlations/recovery/jumps are flagged assumptions",
    }

def main(argv=None):
    argv = argv or sys.argv[1:]
    portfolio = json.load(open(argv[0])); config = json.load(open(argv[1]))
    json.dump(run_analysis(portfolio, config), sys.stdout, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
