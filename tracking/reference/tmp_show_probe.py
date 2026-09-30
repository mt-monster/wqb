# -*- coding: utf-8 -*-
"""快速查看 probe checkpoint 进度"""
import json, os, sys

REPO = r"D:\coding\traeCN_project\wqb"

def show(tag, region="KOR"):
    p = os.path.join(REPO, "tracking", region, "candidates", f"probe_{tag}.json")
    if not os.path.exists(p):
        print(f"=== {tag}: NOT YET ==="); return
    d = json.load(open(p, encoding="utf-8"))
    rs = d.get("results", [])
    ok = [r for r in rs if isinstance(r.get("S"), (int, float))]
    ok.sort(key=lambda x: -(x["S"] or -9))
    print(f"=== {tag}: total={len(rs)} with_alpha={len([r for r in rs if r.get('alpha')])} ===")
    for r in ok:
        print("  %-28s %s S=%-7s F=%-6s 2Y=%s" % (r["label"], r.get("alpha"), r["S"], r["F"], r.get("y2")))
    errs = [r for r in rs if not r.get("alpha")]
    if errs:
        from collections import Counter
        print("  errs:", Counter(str(r.get("err") or r.get("sim"))[:45] for r in errs))

if __name__ == "__main__":
    tags = sys.argv[1:] or ["kor_inst6_all", "kor_insd5_w8"]
    for t in tags:
        show(t)
