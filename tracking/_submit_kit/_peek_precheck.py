import json
from pathlib import Path
RD = Path(r"D:/coding/traeCN_project/wqb/research-data")
d = json.load(open(RD / "mea7_cw_20260901.json", encoding="utf-8"))
print("type:", type(d).__name__)
if isinstance(d, dict):
    print("keys:", list(d.keys()))
    print(json.dumps(d, ensure_ascii=False, indent=2)[:2500])
else:
    for r in d[:8]:
        print(json.dumps(r, ensure_ascii=False)[:400])
