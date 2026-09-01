import json, os
RD = r"D:/coding/traeCN_project/wqb/research-data"
for f in ["submittable_scan_20260901.json", "submittable_scan2_20260901.json"]:
    d = json.load(open(os.path.join(RD, f), encoding="utf-8"))
    lst = d["submittable"]
    n_expr = sum(1 for r in lst if (r.get("expr") or "").strip())
    print(f"== {f}: submittable={len(lst)}, 有表达式={n_expr}")
    # 区域分布
    from collections import Counter
    print("   区域:", dict(Counter(r.get("region") for r in lst)))
    print("   keys:", sorted(lst[0].keys()))
    print()
