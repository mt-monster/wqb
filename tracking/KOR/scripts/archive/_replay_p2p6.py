# -*- coding: utf-8 -*-
"""wave96 批P 其余5条单仿真重放: POST /simulations 抓 location"""
import os, json, base64, requests
from dotenv import load_dotenv

load_dotenv(r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.env")
s = requests.Session()
cred = f"{os.environ['CREDENTIALS_EMAIL']}:{os.environ['CREDENTIALS_PASSWORD']}"
BASE = "https://api.worldquantbrain.com"
r_auth = s.post(f"{BASE}/authentication", headers={"Authorization": "Basic " + base64.b64encode(cred.encode()).decode()})
assert r_auth.status_code == 201, f"auth failed: {r_auth.status_code}"

exprs = {
    "P2": "rank(ts_delta(normalized_trend_indicator_1, 20))",
    "P3": "rank(add(multiply(2, rank(ts_delta(raw_trend_indicator_0, 20))), rank(ts_delta(raw_volume_indicator_0, 20))))",
    "P4": "rank(ts_zscore(ts_delta(raw_trend_indicator_3, 20), 60))",
    "P5": "rank(ts_corr(raw_trend_indicator_0, raw_volume_indicator_0, 20))",
    "P6": "rank(ts_corr(normalized_trend_indicator_1, normalized_volume_indicator_0, 20))",
}
out = {}
for pid, code in exprs.items():
    payload = {
        "type": "REGULAR",
        "settings": {
            "instrumentType": "EQUITY",
            "region": "KOR",
            "universe": "TOP600",
            "delay": 1,
            "decay": 4,
            "neutralization": "STATISTICAL",
            "truncation": 0.08,
            "pasteurization": "ON",
            "unitHandling": "VERIFY",
            "nanHandling": "OFF",
            "language": "FASTEXPR",
            "visualization": False,
        },
        "regular": code,
    }
    r = s.post(f"{BASE}/simulations", json=payload)
    loc = r.headers.get("Location", "")
    err = r.headers.get("x-error", "")
    out[pid] = {"status_code": r.status_code, "location": loc, "x_error": err, "body": r.text[:300]}
with open(r"d:\coding\traeCN_project\wqb\tracking\KOR\cache\wave96_batchP_replay.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
