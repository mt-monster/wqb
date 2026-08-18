"""一次性脚本: 登记 sentiment22 批次用字段进 data/fields_gate.json (USA/TOP3000/D1)
字段来源: get_datafields sentiment22 (2026-08-16), coverage 均 >=0.999"""
import json

GATE = r"d:\coding\traeCN_project\wqb\data\fields_gate.json"

fields = {
    # 无后缀变体组 (_253 系, cov 1.0)
    "snt22neg_mean_253":   {"type": "MATRIX", "coverage": 1.0},
    "snt22pos_mean_270":   {"type": "MATRIX", "coverage": 1.0},
    "snt22neg_median_256": {"type": "MATRIX", "coverage": 1.0},
    "snt22neut_mean_267":  {"type": "MATRIX", "coverage": 1.0},
    # GLOBAL 模型5 D1
    "snt22_5neg_mean_307": {"type": "MATRIX", "coverage": 1.0},
    "snt22_5pos_median_295": {"type": "MATRIX", "coverage": 1.0},
    # 变体2 (USA, D1)
    "snt22_2neg_mean_168": {"type": "MATRIX", "coverage": 1.0},
    "snt22_2pos_mean_164": {"type": "MATRIX", "coverage": 1.0},
    "snt22_2neg_median_156": {"type": "MATRIX", "coverage": 1.0},
    # 变体3 (D1)
    "snt22_3neg_mean_112": {"type": "MATRIX", "coverage": 1.0},
    "snt22_3pos_mean_116": {"type": "MATRIX", "coverage": 1.0},
    # 时序标准差族
    "snt22dts_gen_265":    {"type": "MATRIX", "coverage": 1.0},
}

with open(GATE, encoding="utf-8") as f:
    gate = json.load(f)

scope = gate.setdefault("USA/TOP3000/D1", {})
ds = scope.setdefault("sentiment22", {"fields": {}})
ds["fields"].update(fields)

with open(GATE, "w", encoding="utf-8") as f:
    json.dump(gate, f, ensure_ascii=False, indent=1)

print(f"registered {len(ds['fields'])} sentiment22 fields; D1 datasets: {list(scope.keys())}")
