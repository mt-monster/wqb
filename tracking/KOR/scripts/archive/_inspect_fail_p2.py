# -*- coding: utf-8 -*-
"""wave96 批P multisim 完整响应 + 子仿真重放错误排查"""
import os, json, base64, requests
from dotenv import load_dotenv

load_dotenv(r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.env")
s = requests.Session()
cred = f"{os.environ['CREDENTIALS_EMAIL']}:{os.environ['CREDENTIALS_PASSWORD']}"
BASE = "https://api.worldquantbrain.com"
r_auth = s.post(f"{BASE}/authentication", headers={"Authorization": "Basic " + base64.b64encode(cred.encode()).decode()})
assert r_auth.status_code == 201, f"auth failed: {r_auth.status_code}"

# 1) multisim 完整响应
r = s.get(f"{BASE}/simulations/2Yfs2P5Dk51R9OG14kbEwIvC")
print("=== multisim status:", r.status_code)
print(json.dumps(r.json(), ensure_ascii=False, indent=1)[:3000])
