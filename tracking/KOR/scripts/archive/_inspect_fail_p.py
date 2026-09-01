# -*- coding: utf-8 -*-
"""wave96 批P FAIL 仿真错误排查: GET /simulations/{id} 查响应头 x-error"""
import os, json, requests
from dotenv import load_dotenv

load_dotenv(r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.env")
s = requests.Session()
import base64
cred = f"{os.environ['CREDENTIALS_EMAIL']}:{os.environ['CREDENTIALS_PASSWORD']}"
BASE = "https://api.worldquantbrain.com"
# 1) 认证: POST /authentication -> cookie t
r_auth = s.post(f"{BASE}/authentication", headers={"Authorization": "Basic " + base64.b64encode(cred.encode()).decode()})
assert r_auth.status_code == 201, f"auth failed: {r_auth.status_code} {r_auth.text[:200]}"
print("auth ok, cookie t =", "t" in s.cookies)

ids = [
    "350udgkK563ckzo4J0EGbB",
    "4zHrRm3604qHa7tr9aO8na3",
    "3fdD2Z3bx4DIaipabHlW48",
    "47Cy3Fg1C4mkcbtbjnaCiSN",
    "1PV27M5dU55IafmwFpkYs7K",
    "1bODCU3Cf5fY9qVeUJRbaZs",
]
out = {}
for sid in ids:
    r = s.get(f"{BASE}/simulations/{sid}")
    d = r.json() if r.headers.get("content-type", "").startswith("application/json") else r.text[:400]
    hdrs = {k: v for k, v in r.headers.items() if k.lower() in ("x-error", "x-request-id", "x-rate-limit-remaining")}
    out[sid] = {"status_code": r.status_code, "headers": hdrs, "body": d}
with open(r"d:\coding\traeCN_project\wqb\tracking\KOR\cache\wave96_batchP_fail_detail.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print(json.dumps({k: {"status_code": v["status_code"], "headers": v["headers"]} for k, v in out.items()}, indent=1))
