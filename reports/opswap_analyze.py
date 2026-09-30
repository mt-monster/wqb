#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""近闸算子平替实验：结果分析 + 破闸判定 + DB 回写 + 报告。

输入：
- cache/opswap_state.json / opswap_results.json（driver 产出）
- cache/opswap_plan.json（parents 平台权威设置+真实失败闸）
动作：
- 重新拉取 20 个父 alpha 的当前 checks（权威基线）
- 逐变体对比：父代失败闸是否通过、是否引入新 FAIL、四闸指标差值
- 回写 DB（expressions 状态推进 + backtest_results）
- 产出 output_report/opswap_experiment_20260930.md
"""
from __future__ import annotations

import json
import os
import sys
import time
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from opswap_driver import new_session, API, ROOT  # noqa: E402

PLAN_PATH = os.path.join(ROOT, "cache", "opswap_plan.json")
RESULT_PATH = os.path.join(ROOT, "cache", "opswap_results.json")
OUT_MD = os.path.join(ROOT, "output_report", "opswap_experiment_20260930.md")
OUT_JSON = os.path.join(ROOT, "output_report", "opswap_experiment_20260930.json")


def fail_checks(alpha_json):
    """从平台 alpha detail 提取失败/警示检查清单 + 全检查值表。"""
    isd = alpha_json.get("is", {})
    fails, warns = [], []
    allc = {}
    for c in (isd.get("checks") or []):
        name = c.get("name")
        res = c.get("result")
        allc[name] = {"result": res, "value": c.get("value"), "limit": c.get("limit")}
        if res == "FAIL":
            fails.append({"name": name, "value": c.get("value"), "limit": c.get("limit")})
        elif res == "WARNING":
            warns.append({"name": name, "value": c.get("value"), "limit": c.get("limit")})
    return isd, fails, warns, allc


def gating_names(allc):
    """数值型未达标检查集合（FAIL 或 WARNING 且 value<limit）。

    平台语义：不少闸（LOW_FITNESS、LOW_GLB_EMEA_SHARPE、LOW_SHARPE 边界情形）
    在 checks 里只给 WARNING，但仍计入 ra_failed_checks（2026-09-30 实测 LLNlP3lM：
    LOW_FITNESS 0.99 是 WARNING 却在 ra_failed 名单）。故破闸判定必须用
    「数值未达 limit」而非仅 result==FAIL。
    无 value/limit 的信息类告警（MATCHES_*、UNITS 等）不参与。
    """
    out = set()
    for name, c in allc.items():
        v, lim = c.get("value"), c.get("limit")
        if isinstance(v, (int, float)) and isinstance(lim, (int, float)):
            if c.get("result") in ("FAIL", "WARNING") and v < lim:
                out.add(name)
    return out


def main():
    plan = json.load(open(PLAN_PATH, encoding="utf-8"))
    results = json.load(open(RESULT_PATH, encoding="utf-8"))
    parents = plan["parents"]

    sess = new_session()

    # 1) 父代基线（平台当前值）
    base = {}
    for pid in parents:
        r = sess.get(f"{API}/alphas/{pid}", timeout=60)
        r.raise_for_status()
        isd, fails, warns, allc = fail_checks(r.json())
        base[pid] = {"metrics": {k: isd.get(k) for k in
                                 ("sharpe", "fitness", "turnover", "returns", "drawdown", "margin")},
                     "fails": fails, "warns": warns, "checks": allc}
        time.sleep(0.2)

    # 2) 逐变体对比
    rows = []
    for tag, rec in results.items():
        pid, swap = tag.split("|", 1)
        p = parents[pid]
        row = {"tag": tag, "parent": pid, "swap": swap, "region": p["region"],
               "gate": p["gate"], "status": rec["status"], "alpha_id": rec.get("alpha_id")}
        if rec["status"] != "done":
            row["error"] = rec.get("error")
            rows.append(row)
            continue
        m = rec.get("metrics") or {}
        checks = rec.get("checks") or []
        v_all = {c["name"]: c for c in checks}
        p_all = base[pid]["checks"]
        # 数值未达标集合（FAIL∪WARNING 且 value<limit；剔除 MATCHES_*/UNITS 信息类）
        p_failing = gating_names(p_all)
        v_failing = gating_names(v_all)
        v_fails = [c for c in checks if c.get("result") == "FAIL"]
        v_warns = [c for c in checks if c.get("result") == "WARNING"]
        # 2Y/SUB 从 checks 值提取（IS_LADDER_SHARPE / LOW_2Y_SHARPE / LOW_SUB_UNIVERSE_SHARPE）
        def chk_val(d, *names):
            for n in names:
                if n in d and isinstance(d[n].get("value"), (int, float)):
                    return d[n]["value"]
            return None
        row.update({
            "metrics": m,
            "parent_metrics": base[pid]["metrics"],
            "v_fails": v_fails, "v_warns": [w["name"] for w in v_warns],
            "parent_fail_names": sorted(p_failing),
            "variant_fail_names": sorted(v_failing),
            "y2_v": chk_val(v_all, "IS_LADDER_SHARPE", "LOW_2Y_SHARPE"),
            "y2_p": chk_val(p_all, "IS_LADDER_SHARPE", "LOW_2Y_SHARPE"),
            "sub_v": chk_val(v_all, "LOW_SUB_UNIVERSE_SHARPE"),
            "sub_p": chk_val(p_all, "LOW_SUB_UNIVERSE_SHARPE"),
            "fixed": sorted(p_failing - v_failing),            # 父未达标 → 变体达标
            "new_fail": sorted(v_failing - p_failing),         # 变体新增未达标
            "broke_gate": bool(p_failing) and not v_failing,   # 父有未达标且变体全清
        })
        rows.append(row)
        time.sleep(0.1)

    # 3) 聚合
    by_swap = defaultdict(lambda: {"n": 0, "broke": 0, "fixed_some": 0, "new_fail": 0})
    by_gate = defaultdict(lambda: {"n": 0, "broke": 0})
    for r in rows:
        if r.get("status") != "done":
            continue
        by_swap[r["swap"]]["n"] += 1
        by_gate[r["gate"]]["n"] += 1
        if r.get("broke_gate"):
            by_swap[r["swap"]]["broke"] += 1
            by_gate[r["gate"]]["broke"] += 1
        if r.get("fixed"):
            by_swap[r["swap"]]["fixed_some"] += 1
        if r.get("new_fail"):
            by_swap[r["swap"]]["new_fail"] += 1

    # 4) 报告
    L = ["# 近闸 Alpha 算子平替破闸实验（2026-09-30）\n",
         "- 父代：DB 初筛「恰好挂一闸、差距≤12%」110 个 → 去重 97 → 按闸型分层取 20 个（平台 get_alpha_details 校准真实失败闸）",
         "- 变体：44 条 1:1 算子平替（单变体单替换，签名兼容，比较语境保护），同设置对照回测（44/44 全部 COMPLETE，0 ERROR）",
         "- 平替族：ts_mean↔ts_decay_linear（量纲安全）、group_rank↔group_zscore、rank↔zscore、ts_zscore→ts_rank",
         "- 判定口径：未达标 = 数值型检查 FAIL **或 WARNING 且 value<limit**（平台把 LOW_FITNESS/LOW_GLB_EMEA_SHARPE 等真闸常放 WARNING 但计入 ra_failed，实测校准）；"
         "信息类告警（MATCHES_*/UNITS）不参与",
         "\n## 一、按平替方向的破闸率\n",
         "| 平替方向 | 变体数 | 完全破闸(父代未达标全清且无新增) | 部分修复 | 引入新增未达标 |",
         "|---|---|---|---|---|"]
    for s, d in sorted(by_swap.items(), key=lambda kv: -kv[1]["broke"]):
        L.append(f"| `{s}` | {d['n']} | {d['broke']} | {d['fixed_some']} | {d['new_fail']} |")
    L.append("\n## 二、按闸型的破闸率\n")
    L.append("| 闸型 | 变体数 | 完全破闸 |")
    L.append("|---|---|---|")
    for g, d in sorted(by_gate.items()):
        L.append(f"| {g} | {d['n']} | {d['broke']} |")

    L.append("\n## 三、逐变体明细（仅列 done）\n")
    L.append("| 变体 alpha | 父代 | 平替 | S(父) | F(父) | 2Y(父) | SUB(父) | 换手 | 父代失败闸 | 变体失败闸 | 判定 |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in sorted(rows, key=lambda x: (x.get("parent", ""), x.get("swap", ""))):
        if r.get("status") != "done":
            continue
        m, pm = r["metrics"], r["parent_metrics"]
        def f2(x):
            return f"{x:.2f}" if isinstance(x, (int, float)) else "—"
        verdict = "✅破闸" if r["broke_gate"] else ("🔶修复部分" if r["fixed"] else "❌未破")
        if r["new_fail"]:
            verdict += f" ⚠新FAIL:{','.join(r['new_fail'])}"
        L.append(f"| {r['alpha_id']} | {r['parent']} | `{r['swap']}` | "
                 f"{f2(m.get('sharpe'))}({f2(pm.get('sharpe'))}) | {f2(m.get('fitness'))}({f2(pm.get('fitness'))}) | "
                 f"{f2(r.get('y2_v'))}({f2(r.get('y2_p'))}) | {f2(r.get('sub_v'))}({f2(r.get('sub_p'))}) | "
                 f"{f2(m.get('turnover'))} | {','.join(r['parent_fail_names']) or '—'} | "
                 f"{','.join(r['variant_fail_names']) or '无'} | {verdict} |")
    L.append("\n*2Y 取值优先级 IS_LADDER_SHARPE > LOW_2Y_SHARPE（平台 ladder 窗口因 alpha 而异）；SUB = LOW_SUB_UNIVERSE_SHARPE 实测值。\n")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump({"base": base, "rows": rows,
                   "by_swap": {k: dict(v) for k, v in by_swap.items()},
                   "by_gate": {k: dict(v) for k, v in by_gate.items()}},
                  f, ensure_ascii=False, indent=1)

    # 5) DB 回写（backtest_results + expressions 状态推进）
    sys.path.insert(0, os.path.join(ROOT, "src"))
    from wqb.store import CampaignStore, default_db_path
    store = CampaignStore(default_db_path())
    by_region = defaultdict(list)
    vmap = {v["parent"] + "|" + v["swap"]: v for v in plan["variants"]}
    for r in rows:
        if r.get("status") != "done" or not r.get("alpha_id"):
            continue
        v = vmap[r["tag"]]
        m = r["metrics"]
        by_region[r["region"]].append({
            "id": r["alpha_id"], "code": v["expression"],
            "sharpe": m.get("sharpe"), "fitness": m.get("fitness"),
            "turnover": m.get("turnover"), "margin": m.get("margin"),
            "returns": m.get("returns"), "drawdown": m.get("drawdown"),
            "ra_failed_checks": [c["name"] for c in r["v_fails"]],
            "status": "COMPLETE",
        })
    for region, rrows in by_region.items():
        n = store.upsert_backtest_rows(region, "OPSWAP0930", rrows)
        print(f"[db] {region}: upsert_backtest_rows -> {n}")

    print(f"[report] {OUT_MD}")
    print(f"[json] {OUT_JSON}")
    broke = sum(1 for r in rows if r.get("broke_gate"))
    print(f"[summary] variants done={sum(1 for r in rows if r.get('status')=='done')}/{len(rows)}, 完全破闸={broke}")


if __name__ == "__main__":
    main()
