# quant/selftests/test_data.py
import numpy as np
from quant import data

ZCYC_FIXTURE = {
    "yearyields": {"columns": ["period", "value"],
                   "data": [[0.25, 18.0], [0.5, 17.5], [1, 17.0], [2, 16.0],
                            [3, 15.5], [5, 15.0], [7, 14.8], [10, 14.6],
                            [15, 14.5], [20, 14.4], [0.75, 17.2]]},
    "params": {"columns": ["tradedate", "tradetime", "B1", "B2", "B3", "T1"],
               "data": [["2026-06-25", "18:00:00", 1551.4, -202.85, -615.56, 0.797]]},
}

def test_parse_gcurve_sorted_and_asof():
    c = data.parse_gcurve(ZCYC_FIXTURE)
    assert list(c["tenors"]) == sorted(c["tenors"])          # sorted ascending
    assert c["tenors"][0] == 0.25 and c["tenors"][-1] == 20
    assert abs(c["yields"][0] - 18.0) < 1e-9                  # yield aligned to 0.25y
    assert c["asof"] == "2026-06-25"
    assert c["params"]["B1"] == 1551.4
