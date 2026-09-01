import json
from pathlib import Path
CKPT = Path(r"D:/coding/traeCN_project/wqb/research-data/prod_final_20260901.json")
if not CKPT.exists():
    print("未开始"); raise SystemExit
d = json.load(open(CKPT, encoding="utf-8"))
ok = [k for k, v in d.items() if v.get("pass") is True]
bad = [k for k, v in d.items() if v.get("pass") is False]
err = [k for k, v in d.items() if v.get("pass") is None]
print(f"已检 {len(d)} 颗 | PASS={len(ok)} FAIL={len(bad)} ERR={len(err)}")
print()
for k, v in d.items():
    p = v.get("prod")
    tag = "PASS" if v.get("pass") else ("FAIL" if v.get("pass") is False else "ERR ")
    ps = f"{p:.4f}" if isinstance(p, (int, float)) else str(v.get("error"))
    print(f"  {k:<10} {str(v.get('region')):<4} fit={v.get('fitness',0):>5.2f} {tag} {ps}")
