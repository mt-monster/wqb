# -*- coding: utf-8 -*-
"""S_req 前置筛选：进设置轴扫描之前，先判「F 轴是否可达」。

背景（2026-10-27 实测）
----------------------
fitness 在 TO<0.125 时满足闭式 `F = S^1.5 × sqrt(vol/0.125)`，由此反解：

    **S_req(F=1.0) = S × (1/F)^(2/3)**

含义：手上这颗 (S, F) 若要把 F 抬到 1.0（F 闸），S 至少要到 S_req。
若 S_req 超过该集**实测可达的 S 上限**，那么无论怎么扫设置轴都过不了 F 闸 ⇒ 零仿真判死。

EUR 实测（72 个有 (S,F) 的集）：**62 个（86%）F 轴不可达**，只有 9 个（核实 region 后）可达。
典型误判案例：`analyst45` S_req **1.87** vs 实测上限 1.40 ⇒ 白跑 3 批仿真。

用法
----
    python tools/sreq_precheck.py --region EUR                # 分级输出
    python tools/sreq_precheck.py --region EUR --verify       # 用平台 settings 核实 region（慢，准）
    python tools/sreq_precheck.py --region EUR --dataset model25
    python tools/sreq_precheck.py --region EUR --json out.json

输出分级
--------
    REACHABLE  S_req ≤ 实测 S 上限 + 0.05（值得投入设置轴扫描）
    HOPELESS   S_req 超上限（零仿真判死）
    NO_SF      无可用 (S,F) 记录

注意
----
- `F = S^1.5 × sqrt(vol/0.125)` 只在 **TO < 0.125** 成立。TO 更高的集闭式会偏保守，
  故阈值留 0.05 容差。TO > 0.125 的集建议只用本工具做粗筛。
- results 文件（默认 `results/full_template_campaign_results.json`）在多区域间**共用**，
  集名无法判断归属（EUR 与 GLB 有 74 个同名集）⇒ 跨区统计**必须** `--verify`。
"""
import argparse
import asyncio
import json
import os
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_RESULTS = os.path.join(ROOT, "results", "full_template_campaign_results.json")
DB = os.path.join(ROOT, "data", "wqb.db")
TOL = 0.05


def load_best(results_path, datasets=None):
    """每集取 (S,F) 最优颗 —— 按 S 排序取第一颗有 F 的。"""
    doc = json.load(open(results_path, encoding="utf-8"))
    res = doc.get("results") or doc
    out = {}
    for ds, v in res.items():
        if not isinstance(v, dict):
            continue
        if datasets and ds not in datasets:
            continue
        al = [a for a in (v.get("alphas") or []) if a.get("s") is not None and a.get("f") is not None]
        if not al:
            out[ds] = None
            continue
        by_s = max(al, key=lambda a: a["s"])
        out[ds] = dict(
            alpha=by_s.get("alpha"), tpl=by_s.get("tpl"),
            S=by_s["s"], F=by_s["f"],
            smax=max(a["s"] for a in al),
            y2=v.get("max_2y"), verdict=v.get("verdict"), n=len(al),
        )
    return out


def region_datasets(region):
    con = sqlite3.connect(DB); con.execute("PRAGMA busy_timeout=30000")
    con.row_factory = sqlite3.Row
    rows = list(con.execute(
        "select dataset, category from dataset_profile where region=?", (region,)))
    con.close()
    return {r["dataset"]: (r["category"] or "?") for r in rows}


async def verify(region, items):
    """用平台 settings 核实每个集的 region/universe 归属。"""
    sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    # EUR/GLB universe 交集为空 ⇒ 可硬判
    UNIV = dict(EUR={"TOP2500", "TOP1200", "TOP800", "TOP400", "TOPCS1600"},
                GLB={"TOP3000", "MINVOL1M", "MINVOL10M", "TOPDIV3000"})
    for ds, d in items.items():
        if not d:
            continue
        try:
            j = brain_client.session.get("%s/alphas/%s" % (brain_client.base_url, d["alpha"]),
                                         timeout=30).json()
        except Exception:
            d["verified"] = "ERR"
            continue
        s = j.get("settings") or {}
        d["platform_region"] = s.get("region")
        d["platform_universe"] = s.get("universe")
        d["platform_decay"] = s.get("decay")
        ok = (s.get("region") == region)
        allow = UNIV.get(region)
        if allow and s.get("universe") not in allow:
            ok = False
        d["verified"] = "OK" if ok else "MISMATCH"
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", default="EUR")
    ap.add_argument("--results", default=DEFAULT_RESULTS)
    ap.add_argument("--dataset", default=None, help="逗号分隔，只看这些集")
    ap.add_argument("--verify", action="store_true", help="用平台 settings 核实 region（慢但准）")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()

    want = set(x.strip() for x in a.dataset.split(",")) if a.dataset else None
    cats = region_datasets(a.region)
    items = load_best(a.results, datasets=(want or set(cats)))

    if a.verify:
        asyncio.run(verify(a.region, items))

    rows = []
    for ds, d in items.items():
        if d is None:
            rows.append(dict(ds=ds, cat=cats.get(ds, "?"), cls="NO_SF"))
            continue
        if d.get("verified") == "MISMATCH":
            rows.append(dict(ds=ds, cat=cats.get(ds, "?"), cls="OTHER_REGION",
                             plat="%s/%s" % (d.get("platform_region"), d.get("platform_universe"))))
            continue
        S, F, smax = d["S"], d["F"], d["smax"]
        sreq = S * (1.0 / F) ** (2.0 / 3.0) if F > 0 else float("inf")
        cls = "REACHABLE" if sreq <= smax + TOL else "HOPELESS"
        rows.append(dict(ds=ds, cat=cats.get(ds, "?"), cls=cls, S=S, F=F, smax=smax,
                         sreq=sreq, margin=smax - sreq, y2=d.get("y2"),
                         verdict=d.get("verdict"), alpha=d.get("alpha"), tpl=d.get("tpl"),
                         n=d.get("n")))

    from collections import Counter
    cnt = Counter(r["cls"] for r in rows)
    print("region=%s  集数=%d  %s" % (a.region, len(rows), dict(cnt)))
    print("\n=== REACHABLE（值得投设置轴）===")
    print("%-22s %-11s %6s %6s %7s %7s %6s" % ("dataset", "cat", "maxS", "maxF", "S_req", "余量", "max2Y"))
    for r in sorted([x for x in rows if x["cls"] == "REACHABLE"], key=lambda x: x["margin"]):
        print("%-22s %-11s %6.2f %6.2f %7.2f %+7.2f %6s" % (
            r["ds"], r["cat"], r["smax"], r["F"], r["sreq"], r["margin"], r["y2"]))
    print("\n=== HOPELESS（零仿真判死，前 15）===")
    for r in sorted([x for x in rows if x["cls"] == "HOPELESS"], key=lambda x: x["margin"])[:15]:
        print("  %-22s %-11s S %.2f F %.2f ⇒ S_req %.2f（超上限 %.2f）" % (
            r["ds"], r["cat"], r["smax"], r["F"], r["sreq"], -r["margin"]))
    if cnt.get("OTHER_REGION"):
        print("\n=== 非本区（被 --verify 剔除）===")
        for r in [x for x in rows if x["cls"] == "OTHER_REGION"]:
            print("  %-22s %s" % (r["ds"], r["plat"]))

    if a.json:
        json.dump(rows, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("\n已写 %s" % a.json)


if __name__ == "__main__":
    main()
