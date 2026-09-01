# -*- coding: utf-8 -*-
"""wave96 批P P1 单仿真重放: POST /simulations 抓 x-error"""
import os, json, base64, requests
from dotenv import load_dotenv

load_dotenv(r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.env")
s = requests.Session()
cred = f"{os.environ['CREDENTIALS_EMAIL']}:{os.environ['CREDENTIALS_PASSWORD']}"
BASE = "https://api.worldquantbrain.com"
r_auth = s.post(f"{BASE}/authentication", headers={"Authorization": "Basic " + base64.b64encode(cred.encode()).decode()})
assert r_auth.status_code == 201, f"auth failed: {r_auth.status_code}"

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
    "regular": "rank(ts_delta(raw_trend_indicator_0, 20))",
}
r = s.post(f"{BASE}/simulations", json=payload)
hdrs = {k: v for k, v in r.headers.items() if k.lower() in ("x-error", "location")}
print("status:", r.status_code)
print("headers:", json.dumps(hdrs, indent=1))
print("body:", r.text[:600])
