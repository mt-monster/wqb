"""一次性脚本: 将 news_transformer_scores 全量字段登记进 data/fields_gate.json (USA/TOP3000/D1)
数据源: get_datafields 落盘 d2c1bbfe.txt (2026-08-16)"""
import json

GATE = r"d:\coding\traeCN_project\wqb\data\fields_gate.json"
DUMP = r"C:\Users\MENGTAO\.qoder-cn\cache\projects\wqb-a40170ec\agent-tools\task-080\d2c1bbfe.txt"

d = json.load(open(DUMP, encoding="utf-8"))
fields = {r["id"]: {"type": r["type"], "coverage": r["coverage"]} for r in d["results"]}

with open(GATE, encoding="utf-8") as f:
    gate = json.load(f)

scope = gate.setdefault("USA/TOP3000/D1", {})
ds = scope.setdefault("news_transformer_scores", {"fields": {}})
ds["fields"].update(fields)

with open(GATE, "w", encoding="utf-8") as f:
    json.dump(gate, f, ensure_ascii=False, indent=1)

hi = [k for k, v in fields.items() if v["coverage"] >= 0.85]
print(f"registered {len(fields)} fields; cov>=0.85: {len(hi)}; D1 datasets: {list(scope.keys())}")
