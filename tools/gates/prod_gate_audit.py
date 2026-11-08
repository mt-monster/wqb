#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prod 闸口径校准与泄漏审计 —— 用平台官方均值反验「我们 gate 的数是不是同一个数」。

背景（2026-11-08 用户提问）
--------------------------------
用户发现 ``GET /consultant/boards/leader?stage=osmosis&user=<uid>`` 能拿到 prod 读数，
问「是不是应该按这个结果来定 gate」。实测结论：**不能**，但**必须用它做校准**。

该端点返回体（实测 404 字节，1 条记录）::

    {"user": "...", "weightFactor": 0.0, "valueFactor": 0.43, "dailyOsmosisRank": 0.82,
     "dataFieldsUsed": 397, "submissionsCount": 217,
     "meanProdCorrelation": 0.6417, "meanSelfCorrelation": 0.4085,
     "superAlphaSubmissionsCount": 49,
     "superAlphaMeanProdCorrelation": 0.638, "superAlphaMeanSelfCorrelation": 0.6055}

三条不能当 gate 的理由
--------------------------------
1. **无分辨率**：``meanProdCorrelation`` 是 N≈217 的账户均值，单颗新 alpha 最多推动
   ``(1-0.6417)/218 ≈ 0.0016``。0.7 这条线对均值毫无区分力。
2. **因果倒置**：只统计**已提交**的 alpha。候选在提交前不进入该指标分母
   ⇒ 等于「用结果去决定是否产生结果」。
3. **不是候选属性**：账户均值是 217 颗历史的平均，单颗候选 prod 是 0.00 还是 0.99，
   这个数都不动一格。gate 必须对「被判定对象」敏感，均值不满足。

它真正的作用 = 校准
--------------------------------
逐颗真值在 ``/users/self/alphas`` 的 ``is.prodCorrelation`` / ``is.selfCorrelation``。
把逐颗值聚合起来，与 board 的官方均值对账：

- 有值子集（2026 起才填）均值 ≈ **0.6388** vs board **0.6417**
- 2026 段均值 ≈ **0.6353**
- SUPER prod 均值 ≈ **0.6372** vs board ``superAlphaMeanProdCorrelation`` **0.638**
- SUPER self 均值 ≈ **0.6054** vs board ``superAlphaMeanSelfCorrelation`` **0.6055**（逐位吻合）

⇒ 我们 gate 用的 ``check_correlation(production).max`` 与平台官方口径**是同一个数**，
0.7 阈值没有被测错东西。这条对账每次跑都能重验，不靠记忆。

另一个实证（更硬的）
--------------------------------
``is.prodCorrelation`` 是**提交瞬间的冻结值**，永不随池子变动。已核对三颗逐位吻合：
kqN92KpK 0.6196 / bl6AvMkN 0.6470 / zq3eb7No 0.6171。
⇒ 「prod 会漂移」这个说法必须拆开说：
  - **已提交**的 alpha：冻死不动，可当闸门快照用；
  - **未提交候选**：读数随池子变动（自己或同族的新提交会顶高它）——d5Wvpmbx
    0.6906→0.9081 就是 kqN92KpK 入池造成的，不是它自己漂。

用法
--------------------------------
::

    python tools/gates/prod_gate_audit.py            # 人读报表
    python tools/gates/prod_gate_audit.py --json     # 机器可读
    python tools/gates/prod_gate_audit.py --strict   # 对账偏差 >0.02 时 exit 1

**不改 gate**：本工具只读、只对账。gate 仍走 ``submit_alpha`` Step 1.6（fail-closed）。
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import statistics as st
import sys
from collections import defaultdict

_MCP = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                    "world-quant-brain-mcp")
if _MCP not in sys.path:
    sys.path.insert(0, _MCP)

PROD_LIMIT = 0.70
# 0.7 prod 红线成为硬闸的日期（此前提交的 >=0.7 属历史，不算泄漏）
RULE_SINCE = "2026-10-18"
GAP_TOL = 0.02


def _f(x):
    return x if isinstance(x, (int, float)) else None


async def _fetch_board(client):
    """账户级均值。stage 参数被平台忽略（osmosis/OS/IS 返回体字节数完全相同），故只用 osmosis。"""
    prof = None
    try:
        prof = (await client._request("GET", "/users/self")).json()
    except Exception:
        prof = None
    uid = (prof or {}).get("id") or (prof or {}).get("userId")
    if not uid:
        raise RuntimeError("拿不到 self user id，请显式传 --user")
    r = await client._request("GET", "/consultant/boards/leader",
                              params={"stage": "osmosis", "user": uid})
    r.raise_for_status()
    res = (r.json().get("results") or [])
    return uid, (res[0] if res else {})


async def _fetch_os_alphas(client):
    rows, off = [], 0
    while True:
        r = await client._request("GET", "/users/self/alphas",
                                  params={"limit": 100, "offset": off,
                                          "order": "-dateSubmitted", "stage": "OS"})
        r.raise_for_status()
        j = r.json()
        rows += j.get("results") or []
        off += 100
        if not j.get("next") or off >= 2000:
            break
    return rows


def _classify(a):
    tags = a.get("tags") or []
    if a.get("type") == "SUPER":
        return "SUPER"
    if any("PowerPool" in t for t in tags):
        return "POWER_POOL"
    return "REGULAR"


def _aggregate(alphas):
    out = []
    for a in alphas:
        is_ = a.get("is") or {}
        out.append({
            "id": a.get("id"),
            "channel": _classify(a),
            "region": (a.get("settings") or {}).get("region"),
            "submitted": (a.get("dateSubmitted") or "")[:10],
            "prod": _f(is_.get("prodCorrelation")),
            "self": _f(is_.get("selfCorrelation")),
        })
    return out


def _mean(xs):
    v = [x for x in xs if x is not None]
    return (sum(v) / len(v)) if v else None


def build_report(uid, board, rows):
    filled = [r for r in rows if r["prod"] is not None]
    nonzero = [r for r in filled if r["prod"] > 0]
    y2026 = [r for r in filled if r["submitted"] >= "2026-01-01"]
    sup = [r for r in filled if r["channel"] == "SUPER"]
    reg = [r for r in filled if r["channel"] != "SUPER"]

    hi = sorted([r for r in filled if r["prod"] >= PROD_LIMIT],
                key=lambda x: -x["prod"])
    leak = [r for r in hi if r["submitted"] >= RULE_SINCE]

    report = {
        "user": uid,
        "board": {
            "submissionsCount": board.get("submissionsCount"),
            "meanProdCorrelation": board.get("meanProdCorrelation"),
            "meanSelfCorrelation": board.get("meanSelfCorrelation"),
            "superAlphaSubmissionsCount": board.get("superAlphaSubmissionsCount"),
            "superAlphaMeanProdCorrelation": board.get("superAlphaMeanProdCorrelation"),
            "superAlphaMeanSelfCorrelation": board.get("superAlphaMeanSelfCorrelation"),
            "dailyOsmosisRank": board.get("dailyOsmosisRank"),
        },
        "os_alphas": len(rows),
        "prod_filled": len(filled),
        "prod_nonzero": len(nonzero),
        "prod_zero_or_null": len(rows) - len(nonzero),
        "computed": {
            "all_filled_prod_mean": _mean(r["prod"] for r in filled),
            "nonzero_prod_mean": _mean(r["prod"] for r in nonzero),
            "y2026_prod_mean": _mean(r["prod"] for r in y2026),
            "regular_prod_mean": _mean(r["prod"] for r in reg),
            "super_prod_mean": _mean(r["prod"] for r in sup),
            "super_self_mean": _mean(r["self"] for r in sup),
        },
        "over_limit": {"total": len(hi), "since_rule": len(leak),
                       "items": hi},
    }
    b = report["board"]
    c = report["computed"]
    checks = []
    # 对账基准必须用 prod>0 子集：2025 年及更早提交的 alpha 该字段未回填（恒 0），
    # board 均值显然不含这些 0，混入会把 gap 撑到 0.19 从而误报「口径偏离」。
    pairs = [
        ("prod>0 子集 prod 均值", c["nonzero_prod_mean"], b["meanProdCorrelation"]),
        ("SUPER prod 均值", c["super_prod_mean"], b["superAlphaMeanProdCorrelation"]),
        ("SUPER self 均值", c["super_self_mean"], b["superAlphaMeanSelfCorrelation"]),
    ]
    for name, ours, theirs in pairs:
        if ours is None or not isinstance(theirs, (int, float)):
            continue
        gap = abs(ours - theirs)
        checks.append({"pair": name, "ours": round(ours, 4),
                       "board": round(theirs, 4), "gap": round(gap, 4),
                       "ok": gap <= GAP_TOL})
    report["reconciliation"] = checks
    report["reconciliation_ok"] = all(x["ok"] for x in checks) if checks else None
    return report


def render(rep):
    b, c = rep["board"], rep["computed"]
    L = []
    L.append("=" * 78)
    L.append("prod 闸口径校准 / 泄漏审计   user=%s" % rep["user"])
    L.append("=" * 78)
    L.append("【账户级（board/leader，唯一 prod 字段是均值，不能当 gate）】")
    for k in ("submissionsCount", "meanProdCorrelation", "meanSelfCorrelation",
              "superAlphaSubmissionsCount", "superAlphaMeanProdCorrelation",
              "superAlphaMeanSelfCorrelation", "dailyOsmosisRank"):
        L.append("  %-32s %s" % (k, b.get(k)))
    L.append("")
    L.append("【逐颗真值（/users/self/alphas → is.prodCorrelation，提交时冻结）】")
    L.append("  OS alpha 总数 %d ｜ prod>0 有效 %d ｜ prod=0（2025 及更早未回填）%d"
             % (rep["os_alphas"], rep["prod_nonzero"], rep["prod_zero_or_null"]))
    for k, label in (("all_filled_prod_mean", "有值全集 prod 均值"),
                     ("nonzero_prod_mean", "prod>0 子集均值"),
                     ("y2026_prod_mean", "2026 段 prod 均值"),
                     ("regular_prod_mean", "REGULAR prod 均值"),
                     ("super_prod_mean", "SUPER prod 均值"),
                     ("super_self_mean", "SUPER self 均值")):
        v = c.get(k)
        L.append("  %-28s %s" % (label, "%.4f" % v if v is not None else "-"))
    L.append("")
    L.append("【口径对账（决定 0.7 阈值是否测的是同一个数）】")
    for x in rep["reconciliation"]:
        L.append("  %-24s ours=%.4f board=%.4f gap=%.4f  %s"
                 % (x["pair"], x["ours"], x["board"], x["gap"],
                    "OK" if x["ok"] else "DIVERGE"))
    L.append("  结论：%s" % ("口径一致，gate 数即官方数"
                            if rep["reconciliation_ok"] else "口径偏离，需查读数来源"))
    L.append("")
    ol = rep["over_limit"]
    L.append("【提交后 prod ≥ %.2f 的 alpha】共 %d 颗 ｜ 规则生效(%s)后提交 %d 颗（真泄漏）"
             % (PROD_LIMIT, ol["total"], RULE_SINCE, ol["since_rule"]))
    for r in ol["items"][:20]:
        flag = "LEAK" if r["submitted"] >= RULE_SINCE else "pre-rule"
        L.append("  %-10s %-10s %-5s prod=%.4f self=%.4f %s  %s"
                 % (r["id"], r["channel"], r["region"] or "-",
                    r["prod"], r["self"] if r["self"] is not None else 0, r["submitted"], flag))
    L.append("")
    L.append("注：is.prodCorrelation 冻结于提交瞬间 ⇒ 该表是「当时闸门看到的数」的权威快照；")
    L.append("    ≥0.7 且早于 %s 的属历史（红线成制度前），不计泄漏。" % RULE_SINCE)
    return "\n".join(L)


async def _main(args):
    from brain_api import BrainApiClient
    client = BrainApiClient()
    await client.ensure_authenticated()
    uid, board = await _fetch_board(client)
    alphas = await _fetch_os_alphas(client)
    rep = build_report(uid, board, _aggregate(alphas))
    if args.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print(render(rep))
    if args.strict:
        bad = (rep["reconciliation_ok"] is False) or (rep["over_limit"]["since_rule"] > 0)
        return 1 if bad else 0
    return 0


def main():
    ap = argparse.ArgumentParser(description="prod 闸口径校准与泄漏审计（只读）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--strict", action="store_true", help="口径偏离或有真泄漏时 exit 1")
    args = ap.parse_args()
    sys.exit(asyncio.run(_main(args)))


if __name__ == "__main__":
    main()
