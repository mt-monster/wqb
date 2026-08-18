"""一次性脚本: 将 option8 的 64 个字段登记进 data/fields_gate.json (USA/TOP3000/D1)"""
import json

GATE = r"d:\coding\traeCN_project\wqb\data\fields_gate.json"

FIELDS = [
    # (id, coverage)
    ("historical_volatility_10", 0.9808), ("historical_volatility_20", 0.9807),
    ("historical_volatility_30", 0.9807), ("historical_volatility_60", 0.9805),
    ("historical_volatility_90", 0.9803), ("historical_volatility_120", 0.98),
    ("historical_volatility_150", 0.9798), ("historical_volatility_180", 0.9796),
    ("parkinson_volatility_10", 0.9808), ("parkinson_volatility_20", 0.9807),
    ("parkinson_volatility_30", 0.9807), ("parkinson_volatility_60", 0.9805),
    ("parkinson_volatility_90", 0.9803), ("parkinson_volatility_120", 0.9801),
    ("parkinson_volatility_150", 0.9798), ("parkinson_volatility_180", 0.9796),
    ("implied_volatility_call_10", 0.9729), ("implied_volatility_call_20", 0.9729),
    ("implied_volatility_call_30", 0.9729), ("implied_volatility_call_60", 0.9729),
    ("implied_volatility_call_90", 0.9729), ("implied_volatility_call_120", 0.9729),
    ("implied_volatility_call_150", 0.9729), ("implied_volatility_call_180", 0.9729),
    ("implied_volatility_call_270", 0.9729), ("implied_volatility_call_360", 0.9729),
    ("implied_volatility_call_720", 0.9729), ("implied_volatility_call_1080", 0.9729),
    ("implied_volatility_put_10", 0.9727), ("implied_volatility_put_20", 0.9727),
    ("implied_volatility_put_30", 0.9727), ("implied_volatility_put_60", 0.9727),
    ("implied_volatility_put_90", 0.9727), ("implied_volatility_put_120", 0.9727),
    ("implied_volatility_put_150", 0.9727), ("implied_volatility_put_180", 0.9727),
    ("implied_volatility_put_270", 0.9727), ("implied_volatility_put_360", 0.9727),
    ("implied_volatility_put_720", 0.9727), ("implied_volatility_put_1080", 0.9727),
    ("implied_volatility_mean_10", 0.9688), ("implied_volatility_mean_20", 0.9688),
    ("implied_volatility_mean_30", 0.9688), ("implied_volatility_mean_60", 0.9688),
    ("implied_volatility_mean_90", 0.9688), ("implied_volatility_mean_120", 0.9688),
    ("implied_volatility_mean_150", 0.9688), ("implied_volatility_mean_180", 0.9688),
    ("implied_volatility_mean_270", 0.9688), ("implied_volatility_mean_360", 0.9688),
    ("implied_volatility_mean_720", 0.9688), ("implied_volatility_mean_1080", 0.9688),
    ("implied_volatility_mean_skew_10", 0.9508), ("implied_volatility_mean_skew_20", 0.9508),
    ("implied_volatility_mean_skew_30", 0.9508), ("implied_volatility_mean_skew_60", 0.9508),
    ("implied_volatility_mean_skew_90", 0.9508), ("implied_volatility_mean_skew_120", 0.9508),
    ("implied_volatility_mean_skew_150", 0.9508), ("implied_volatility_mean_skew_180", 0.9508),
    ("implied_volatility_mean_skew_270", 0.9508), ("implied_volatility_mean_skew_360", 0.9508),
    ("implied_volatility_mean_skew_720", 0.9508), ("implied_volatility_mean_skew_1080", 0.9508),
]

with open(GATE, encoding="utf-8") as f:
    gate = json.load(f)

scope = gate.setdefault("USA/TOP3000/D1", {})
ds = scope.setdefault("option8", {"fields": {}})
for fid, cov in FIELDS:
    ds["fields"][fid] = {"type": "MATRIX", "coverage": cov}

with open(GATE, "w", encoding="utf-8") as f:
    json.dump(gate, f, ensure_ascii=False, indent=1)

print(f"registered {len(FIELDS)} option8 fields; scope datasets: {list(scope.keys())}")
