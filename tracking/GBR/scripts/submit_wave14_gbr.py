#!/usr/bin/env python3
"""GBR Wave 14 批量回测脚本 - 使用正确的 GBR 设置"""
import requests
import json
import time
import os
from datetime import datetime

# BRAIN API 配置
BRAIN_API = "https://api.worldquantbrain.com"
EMAIL = os.getenv("BRAIN_EMAIL")
PASSWORD = os.getenv("BRAIN_PASSWORD")

if not EMAIL or not PASSWORD:
    # 尝试从 .env 文件读取
    env_path = "D:/coding/traeCN_project/wqb/world-quant-brain-mcp/.env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("BRAIN_EMAIL="):
                    EMAIL = line.strip().split("=", 1)[1]
                elif line.startswith("BRAIN_PASSWORD="):
                    PASSWORD = line.strip().split("=", 1)[1]

if not EMAIL or not PASSWORD:
    print("ERROR: BRAIN_EMAIL and BRAIN_PASSWORD must be set")
    exit(1)

# 登录
session = requests.Session()
auth_response = session.post(
    f"{BRAIN_API}/authentication",
    json={"email": EMAIL, "password": PASSWORD}
)
if auth_response.status_code != 201:
    print(f"ERROR: Authentication failed: {auth_response.status_code}")
    print(auth_response.text)
    exit(1)

print(f"Authenticated successfully")

# GBR 设置
GBR_SETTINGS = {
    "instrumentType": "EQUITY",
    "region": "GBR",
    "universe": "TOP700",
    "delay": 1,
    "decay": 4,
    "neutralization": "SECTOR",
    "truncation": 0.08,
    "pasteurization": "ON",
    "unitHandling": "VERIFY",
    "nanHandling": "OFF",
    "maxTrade": "ON",
    "language": "FASTEXPR",
    "visualization": False
}

# Wave 14 表达式
expressions = [
    "rank(oth455_competitor_n2v_p10_q200_w1_pca_fact1_value)",
    "add(rank(oth455_competitor_n2v_p10_q200_w1_pca_fact1_value), rank(oth455_competitor_n2v_p10_q200_w1_pca_fact2_value))",
    "multiply(rank(oth455_competitor_n2v_p10_q200_w1_pca_fact1_value), rank(oth455_competitor_n2v_p10_q200_w1_pca_fact2_value))",
    "ts_delta(oth455_competitor_n2v_p10_q200_w1_pca_fact1_value, 5)",
    "ts_mean(oth455_competitor_n2v_p10_q200_w1_pca_fact1_value, 10)",
    "group_zscore(oth455_competitor_n2v_p10_q200_w1_pca_fact1_value, industry)",
    "winsorize(oth455_competitor_n2v_p10_q200_w1_pca_fact1_value, std=4)",
    "ts_ir(oth455_competitor_n2v_p10_q200_w1_pca_fact1_value, 20)"
]

# 创建多模拟
alphas = []
for expr in expressions:
    alphas.append({
        "type": "REGULAR",
        "settings": GBR_SETTINGS,
        "regular": expr
    })

print(f"Submitting {len(alphas)} alphas for GBR/TOP700...")

response = session.post(
    f"{BRAIN_API}/simulations",
    json=alphas
)

if response.status_code != 201:
    print(f"ERROR: Failed to create simulation: {response.status_code}")
    print(response.text)
    exit(1)

result = response.json()
print(f"Multi-simulation created: {result.get('id', 'N/A')}")

# 保存结果
output = {
    "wave": "W14",
    "dataset": "other455",
    "region": "GBR",
    "universe": "TOP700",
    "submitted_at": datetime.now().isoformat(),
    "multisim_id": result.get("id"),
    "location": result.get("location"),
    "alphas": alphas
}

output_file = "D:/coding/traeCN_project/wqb/tracking/GBR/results/gbr_wave14_submission.json"
with open(output_file, "w") as f:
    json.dump(output, f, indent=2)

print(f"Submission saved to {output_file}")
print(f"Location: {result.get('location')}")
