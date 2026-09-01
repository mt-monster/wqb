#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""合并两轮扫描的可提交候选 -> 按表达式结构同族聚类去重 -> 每族留最优 1 颗。

纪律：同族连测 = 自相残杀，一族只留最优 1 颗提交候选。
"""
import json
import re
import os
from collections import defaultdict, Counter

RD = r"D:/coding/traeCN_project/wqb/research-data"

scan1 = json.load(open(os.path.join(RD, "submittable_scan_20260901.json"), encoding="utf-8"))
scan2 = json.load(open(os.path.join(RD, "submittable_scan2_20260901.json"), encoding="utf-8"))

rows = []
for tag, scan in (("scan1", scan1), ("scan2", scan2)):
    for r in scan["submittable"]:
        rows.append({
            "src": tag,
            "id": r.get("alpha_id"),
            "region": r.get("region"),
            "sharpe": r.get("sharpe"),
            "fitness": r.get("fitness"),
            "turnover": r.get("turnover"),
            "returns": r.get("returns"),
            "universe": r.get("universe"),
            "delay": r.get("delay"),
            "neut": r.get("neutralization"),
            "ladder": r.get("ladder"),
            "robust": r.get("robust"),
            "sub_univ": r.get("sub_univ"),
            "expr": (r.get("expr") or "").strip(),
        })

byid = {}
for r in rows:
    if r["id"] and r["id"] not in byid:
        byid[r["id"]] = r
rows = list(byid.values())
print(f"[INFO] 合并去重后候选总数: {len(rows)}")
print("[INFO] 区域分布:", dict(Counter(r["region"] for r in rows)))

FIELD_RE = re.compile(r"\b([a-z][a-z0-9]*_[a-z0-9_]+)")


def sig(expr):
    """族签名 = 算式骨架（数字归一化）+ 字段集合。"""
    if not expr:
        return None  # 无表达式的不聚类，单独保留
    skeleton = re.sub(r"\d+(?:\.\d+)?", "#", expr)
    skeleton = re.sub(r"\s+", "", skeleton)
    fields = sorted(set(FIELD_RE.findall(expr)))
    return skeleton + "||" + ",".join(fields)


fams = defaultdict(list)
nofam = []
for r in rows:
    s = sig(r["expr"])
    if s is None:
        nofam.append(r)
    else:
        fams[s].append(r)

reps = []
for s, members in fams.items():
    members.sort(key=lambda x: (-(x["fitness"] or 0), -(x["sharpe"] or 0)))
    best = members[0]
    best["fam_size"] = len(members)
    best["fam_members"] = [m["id"] for m in members[1:]]
    reps.append(best)
for r in nofam:
    r["fam_size"] = 1
    r["fam_members"] = []
    reps.append(r)

reps.sort(key=lambda x: (-(x["fitness"] or 0), -(x["sharpe"] or 0)))
print(f"[INFO] 同族聚类后: {len(reps)} 族 (原始 {len(rows)} 颗)")
print(f"[INFO] 其中无表达式(无法聚类): {len(nofam)} 颗")
print()
print("=== 各族代表（按 fitness 降序，前 45） ===")
print(f"{'#':>3} {'id':<10} {'reg':<4} {'shrp':>5} {'fit':>5} {'to':>6} {'族':>3}  字段")
for i, r in enumerate(reps[:45], 1):
    fields = sorted(set(FIELD_RE.findall(r["expr"])))
    fstr = (",".join(fields) or "?")[:44]
    print(f"{i:>3} {r['id']:<10} {str(r['region']):<4} {r['sharpe']:>5.2f} {r['fitness']:>5.2f} "
          f"{r['turnover']:>6.4f} {r['fam_size']:>3}  {fstr}")

out = os.path.join(RD, "submittable_merged_20260901.json")
json.dump(reps, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print()
print(f"[OK] written: {out}")
