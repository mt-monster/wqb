#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""杠杆计划：输入候选的当前指标，输出「按实测效果排序」的推指标动作清单。

用法：
    python plan.py --sharpe 1.56 --fitness 1.15 --two-year 1.91 --self 0.14 --prod 0.41 --turnover 0.133
    python plan.py --sharpe 1.54 --fitness 1.07 --two-year 2.69 --self 0.24 --prod 0.7134 --ops 12 --axis fact1
    python plan.py --sharpe 1.33 --fitness 0.91 --two-year 1.54 --self 0.19 --prod 0.45 --json

只读、零副作用。阈值与杠杆效果出处见 references/lever-ladder.md 与 references/metric-map.md。
"""
from __future__ import annotations

import argparse
import json

LIM_SHARPE = 1.58
LIM_FITNESS = 1.0
LIM_2Y = 1.58
LIM_2Y_STRICT = 1.585   # 平台四舍五入 2 位后严格比较
LIM_CORR = 0.7


def _fmt(v, nd=3):
    return "—" if v is None else (f"{v:.{nd}f}" if isinstance(v, float) else str(v))


def build_plan(a) -> dict:
    gaps = {}
    actions = []

    # ---------------- 1. 算子预算（前置） ----------------
    op_actions = []
    if a.ops is not None:
        if a.ops >= 10:
            op_actions.append(
                f"**算子调用点 {a.ops} ≥ 复杂度闸 10 ⇒ 先压缩再推指标**："
                f"`python scripts/compress.py --expr \"<表达式>\"` → 逐点消融"
            )
        elif a.target_ppa and a.ops > 8:
            op_actions.append(
                f"**PPA 目标：算子 {a.ops} > 上限 8 ⇒ 先压缩**（PPA 平台规则 operatorCount ≤ 8）"
            )

    # ---------------- 2. 逐闸缺口 ----------------
    # SHARPE
    if a.sharpe is not None and a.sharpe < LIM_SHARPE:
        gap = LIM_SHARPE - a.sharpe
        gaps["LOW_SHARPE"] = round(gap, 3)
        steps = []
        if (a.axis or "").lower() not in ("sector", "industry", "subindustry"):
            steps.append("L1 **轴 → `sector`**（实测 S +0.26~0.29；同时把 2Y 检查换成宽松档）"
                         "  ⚠ institutions1 类掩码腿上反向失效")
        steps.append("L2 **双窗级联** `multiply(rank(ts_delta(x,a)), rank(ts_delta(x,b)))`（a≈240, b≈176；S +0.18、2Y +0.6）"
                     "  ⚠ 窗为尖峰，必做 ≥5×5 网格")
        steps.append("L3 `ts_target_tvr_decay(x, target_tvr=TO×0.4~0.6)`（S +0.03；**须 TO > target 才激活**）")
        steps.append("L4 `winsorize(..., std=3~4)`（S +0.02；std≥3 饱和，std=1 崩塌）")
        steps.append("L6 `multiply(rank(A), rank(B))` 两腿联合（S +0.11；**逐 category 实测**，基本面上曾反向失效）")
        steps.append("L5 decay 3~8 微调（S ±0.02，主要提 fit）")
        actions.append({"gate": "LOW_SHARPE", "gap": round(gap, 3), "steps": steps})

    # FITNESS
    if a.fitness is not None and a.fitness < LIM_FITNESS:
        gap = LIM_FITNESS - a.fitness
        gaps["LOW_FITNESS"] = round(gap, 3)
        steps = []
        if a.turnover is not None and a.turnover > 0.125:
            steps.append(f"**fitness = S × √(ret / max(tvr, 0.125))**：当前 TO {_fmt(a.turnover,4)} > 0.125 ⇒ "
                         f"**降 TO 有二次收益**（TO 压到 0.125 可让 fit ×"
                         f"{ (a.turnover/0.125) ** 0.5 :.2f}）")
        steps.append("L3 `ts_target_tvr_decay`（TO↓ ⇒ fit↑，且 S +0.03）")
        steps.append("L5 `decay` 4→8（TO↓；但快信号上高 decay 是反的，注意 S 是否掉）")
        steps.append("提 S（S↑ ⇒ fit 同向↑）")
        actions.append({"gate": "LOW_FITNESS", "gap": round(gap, 3), "steps": steps})

    # 2Y
    if a.two_year is not None and a.two_year < LIM_2Y_STRICT:
        gap = LIM_2Y_STRICT - a.two_year
        gaps["2Y"] = round(gap, 3)
        steps = []
        if (a.axis or "").lower() not in ("sector", "industry", "subindustry"):
            steps.append("L1 **换成平台内置轴（`sector` 等）**：把严格的 `IS_LADDER_SHARPE` 换成宽松的 `LOW_2Y_SHARPE`"
                         "（同一数值可能从 FAIL 变 PASS）")
        steps.append("L2 **双窗级联**（2Y +0.6，本战役最强）")
        steps.append("**字段变体换 `_main`**（同概念 2Y 1.88 → 2.71，S 保持；比调窗便宜）")
        steps.append("拉长窗到 252~264（本战役 252 是尖峰）")
        actions.append({"gate": "2Y", "gap": round(gap, 3), "steps": steps})

    # SELF
    if a.self_corr is not None and a.self_corr >= LIM_CORR:
        gaps["SELF_CORRELATION"] = round(a.self_corr - LIM_CORR, 3)
        actions.append({"gate": "SELF_CORRELATION", "gap": round(a.self_corr - LIM_CORR, 3), "steps": [
            "W1 **换信号样本**（去相关第 3 维度：用数据集元字段做 `if_else` 掩码筛子集事件）——优先级最高",
            "W2 换字段族 / 换分组轴（换持仓）",
            "W3 `group_rank` → `group_zscore`（非保序，须重测 prod）",
            "⚠ 同骨架复制会使互相关 >0.99 ⇒ 同腿只出 1 颗",
        ]})

    # PROD
    if a.prod_corr is not None and a.prod_corr >= LIM_CORR:
        gaps["PROD_CORRELATION"] = round(a.prod_corr - LIM_CORR, 3)
        structural = a.sharpe is not None and a.sharpe >= 1.40
        steps = [
            "P1 **换横截面排序**（唯一正解）：换 `multiply` 第 2 腿 / 换字段族 / 换分组轴",
            "P2 换字段变体（低 alphaCount 变体：同概念但 prod 池稀薄）",
            "P3 水平 → 变化（`ts_delta`；高效市场里水平量已被定价）",
            "⚠ **不要**用 neutralization 换档降 prod —— 实测全档同量级降 S（CROWDING: prod −0.074 代价 S −0.55）",
        ]
        if structural:
            steps.insert(0, "★ **结构性判定**：S ≥ 1.40 且 prod ≥ 0.7 ⇒ 本族「S↔prod 前沿」已到顶，"
                            "**调参无效**，必须换横截面排序（把点移出前沿，而非沿前沿滑动）")
        actions.append({"gate": "PROD_CORRELATION", "gap": round(a.prod_corr - LIM_CORR, 3), "steps": steps})

    passed = not gaps and not op_actions
    return {
        "metrics": {
            "sharpe": a.sharpe, "fitness": a.fitness, "two_year": a.two_year,
            "self": a.self_corr, "prod": a.prod_corr, "turnover": a.turnover, "ops": a.ops,
        },
        "gaps": gaps,
        "pre_ops_actions": op_actions,
        "actions": actions,
        "all_pass": passed,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="WQ alpha 推指标杠杆计划（只读）")
    ap.add_argument("--sharpe", type=float)
    ap.add_argument("--fitness", type=float)
    ap.add_argument("--two-year", type=float, dest="two_year")
    ap.add_argument("--self", type=float, dest="self_corr")
    ap.add_argument("--prod", type=float, dest="prod_corr")
    ap.add_argument("--turnover", type=float)
    ap.add_argument("--ops", type=int, help="当前算子调用点数")
    ap.add_argument("--axis", default="", help="当前分组轴（如 sector / fact1 / industry）")
    ap.add_argument("--region", default="")
    ap.add_argument("--target-ppa", action="store_true",
                    help="目标为 PPA（此时平台规则 operatorCount ≤ 8）")
    ap.add_argument("--json", action="store_true", help="输出 JSON（机器可读）")
    a = ap.parse_args()

    plan = build_plan(a)
    if a.json:
        print(json.dumps(plan, ensure_ascii=False, indent=1))
        return

    m = plan["metrics"]
    print("=" * 72)
    print("当前指标 vs 闸门")
    rows = [
        ("LOW_SHARPE", m["sharpe"], LIM_SHARPE, "≥"),
        ("LOW_FITNESS", m["fitness"], LIM_FITNESS, "≥"),
        ("2Y(真值需)", m["two_year"], LIM_2Y_STRICT, "≥"),
        ("SELF_CORRELATION", m["self"], LIM_CORR, "<"),
        ("PROD_CORRELATION", m["prod"], LIM_CORR, "<"),
        ("TURNOVER", m["turnover"], 0.7, "≤"),
    ]
    for name, val, lim, direction in rows:
        if val is None:
            print(f"  {name:<20} {_fmt(val):>8}   (未提供)")
            continue
        ok = (val >= lim) if direction == "≥" else (val <= lim)
        print(f"  {name:<20} {_fmt(val):>8}   {'PASS' if ok else 'FAIL'}   ({direction} {lim})")
    if m["ops"] is not None:
        print(f"  {'operatorCount':<20} {m['ops']:>8}")
    print()

    if plan["all_pass"]:
        print("✅ 全部闸门通过。下一步：self 快筛 → 稳健性 → **用户确认后**提交。")
        return

    if plan["pre_ops_actions"]:
        print("── ⓪ 前置：算子预算（先做）──")
        for s in plan["pre_ops_actions"]:
            print("  " + s)
        print()

    print("── 推指标动作（按实测效果排序）──")
    for act in plan["actions"]:
        print(f"● {act['gate']}  缺口 {act['gap']}")
        for i, s in enumerate(act["steps"], 1):
            print(f"    {i}. {s}")
        print()

    print("── 禁用杠杆（已证否，别再投）──")
    for s in [
        "换 neutralization 档（11 档全降 S）",
        "ts_decay_linear / hump（累积型信号上零和）",
        "group_zscore / tail / bucket 轴（rank 类信号上常灾难）",
        "trade_when 门控（稀疏事件型样本骤减）",
        "腿方向混合（平台 reverse = 整体取负，无混合语义）",
        "扫 truncation（零杠杆）",
    ]:
        print("  ✗ " + s)


if __name__ == "__main__":
    main()
