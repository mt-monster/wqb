"""一次性脚本: 登记 option40 批次用字段进 data/fields_gate.json (USA/TOP3000/D1)
字段来源: get_datafields option40 (2026-08-16), coverage 均 >=0.97, userCount 均 <=40 (蓝海)"""
import json

GATE = r"d:\coding\traeCN_project\wqb\data\fields_gate.json"

fields = {
    # ATM 隐含波动率均值族 (call+put 平均)
    "opt40_ivmean30":  {"type": "MATRIX", "coverage": 0.9841},
    "opt40_ivmean90":  {"type": "MATRIX", "coverage": 0.9841},
    "opt40_ivmean180": {"type": "MATRIX", "coverage": 0.9841},
    # call/put IV (30d/150d, 可构造 skew 比率)
    "opt40_ivcall30":  {"type": "MATRIX", "coverage": 0.9841},
    "opt40_ivput30":   {"type": "MATRIX", "coverage": 0.9841},
    "opt40_ivcall150": {"type": "MATRIX", "coverage": 0.9841},
    "opt40_ivput150":  {"type": "MATRIX", "coverage": 0.9841},
    # IV 期限结构两端 (10d/360d)
    "opt40_ivcall10":  {"type": "MATRIX", "coverage": 0.9816},
    "opt40_ivcall360": {"type": "MATRIX", "coverage": 0.9841},
    # 历史波动率族 (Parkinson/close-to-close)
    "opt40_01vhp":     {"type": "MATRIX", "coverage": 0.9840},
    "opt40_02vh":      {"type": "MATRIX", "coverage": 0.9840},
    "opt40_021vh":     {"type": "MATRIX", "coverage": 0.9843},
    "opt40_021vhp":    {"type": "MATRIX", "coverage": 0.9843},
    # Greeks (theta/gamma/vega/delta, userCount 低)
    "opt40_call_theta_91days":  {"type": "MATRIX", "coverage": 0.9727},
    "opt40_put_theta_122days":  {"type": "MATRIX", "coverage": 0.9724},
    "opt40_call_gamma_273days": {"type": "MATRIX", "coverage": 0.9730},
    "opt40_call_vega_365days":  {"type": "MATRIX", "coverage": 0.9725},
    "opt40_call_delta_122days": {"type": "MATRIX", "coverage": 0.9729},
}

with open(GATE, encoding="utf-8") as f:
    gate = json.load(f)

scope = gate.setdefault("USA/TOP3000/D1", {})
ds = scope.setdefault("option40", {"fields": {}})
ds["fields"].update(fields)

with open(GATE, "w", encoding="utf-8") as f:
    json.dump(gate, f, ensure_ascii=False, indent=1)

print(f"registered {len(ds['fields'])} option40 fields; D1 datasets: {list(scope.keys())}")
