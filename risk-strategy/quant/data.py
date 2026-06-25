# quant/data.py
import numpy as np
import requests

GCURVE_URL = "https://iss.moex.com/iss/engines/stock/zcyc.json"
CBR_KEYRATE_URL = "https://www.cbr.ru/eng/hd_base/KeyRate/"

def _block_rows(block):
    return block["columns"], block["data"]

def parse_gcurve(zcyc_json):
    cols, rows = _block_rows(zcyc_json["yearyields"])
    i_p, i_v = cols.index("period"), cols.index("value")
    pairs = sorted((float(r[i_p]), float(r[i_v])) for r in rows)
    tenors = np.array([p for p, _ in pairs])
    yields = np.array([v for _, v in pairs])
    pcols, prows = _block_rows(zcyc_json["params"])
    params = {pcols[i]: prows[0][i] for i in range(len(pcols))}
    return {"tenors": tenors, "yields": yields, "params": params,
            "asof": params.get("tradedate")}

def fetch_gcurve(session=None):
    s = session or requests
    r = s.get(GCURVE_URL, params={"iss.meta": "off"}, timeout=30)
    r.raise_for_status()
    return parse_gcurve(r.json())
