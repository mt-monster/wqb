# -*- coding: utf-8 -*-
"""wqb.gate_attribution — 「只差一两闸」的**零成本归因**：把闸失败翻译成定向动作。

为什么有这层
------------
用户在 2026-10-16 提出的机制：「只有一闸或二闸不过时，先做 robustness 归因，
再**有针对性**地推闸，而不是盲推」。本模块是该机制的**可执行实现**。

落地前的实测依据（KOR `eps_y1_estimate_change_3mo` 与 `shortinterest38` 两轮，共约 50 次仿真）：

1. **盲推的代价是结构性的**：该分析师族 S 与 prod 严格同向单调
   （S 每 +0.07 ⇒ prod 同 +0.01），跨 6 个结构、15+ 次参数/算子替换**永不交叉**
   （prod 全落在 0.6967–0.7117，跨度 0.015 < 分辨率极限）。
   期间 `quantile` 单独把 S 从 1.51 推到 1.55（**有效**），却同时把 prod 从
   0.6989 顶到 0.7117（**过线**）⇒ 单闸 +0.07 在这条腿上**不可达**。
   若一开始先测 prod 余量，就能省掉整轮无效仿真。
2. **同一算子轴的效应可定向**：门控窗口 → S 在分析师族上单调
   （66→1.41 / 22→1.51 / 10→1.57），这是「可解释轴上的定向搜索」，
   与盲扫参数的本质区别是**每个点都能解释**。
3. **收敛即信号**：某结构族在 4 个互不相关的杠杆（内层 group_neutralize /
   粗轴 / signed_power 幂次 / truncation）上 2Y 全部收敛到 1.51–1.56，
   收敛本身即判「机制层天花板」，不是参数没调到位。

本模块做什么
------------
输入 = 一条候选的**已在手读数**（``get_alpha_details`` 的 metrics + checks、
``get_alpha_yearly_stats`` 的逐年、可选的相关性直方图与同族 (S, prod) 采样），
输出 = 每道失败闸的

* ``cause_class`` —— 归因类别（决定用哪一族杠杆）
* ``feasible`` —— **闭式可行性**：这条路在数学上能不能到
* ``levers`` —— 按本项目**已实测**效果排序的杠杆，不是通用清单
* 顶层 ``verdict`` —— ``PUSH_TARGETED`` / ``SWITCH_AXIS`` / ``ABANDON_LEG`` /
  ``BLOCKED_BY_CORRELATION``，以及一条 ``stop_rule``（何时该停手换轴）

本模块**不发仿真**、不碰 DB、不联网：纯函数，便于单测。
取数与落盘由 ``tools/gate_attribution.py``（CLI）负责。

闸线口径（两条铁律，违反即失效）
--------------------------------
1. **闸线取平台 ``checks[].limit``，不取本模块常量。** 仓内
   ``config.PLATFORM_CHECK_LINES`` 记 LOW_SHARPE delay1 = 1.25，而 KOR D1 实测
   平台回的是 ``limit: 1.58``——两者不一致时**以平台为准**（与
   「判定只走平台」一致）。本模块只在平台没给 limit 时才退到 ``DEFAULTS``。
2. **RA 计数把 WARNING 计入失败。** 口径 = 平台插件
   ``getAlphaCheckStates``：结果既非 PASS 也非 PENDING（WARNING/ERROR）即计入
   （见 ``config`` 段内注释）。所以 ``fail: []`` **不等于**过闸。

Fitness 公式（闭式可行性判据，2026-10-16 三点反解验证）
--------------------------------------------------------
``F = S × √( |returns| / max(TO, 0.125) )``

* 反解样本一：``akVJLlWO`` S 1.51 / ret 0.0746 / TO 0.0852 ⇒ 1.51×√(0.0746/0.125)=1.166，
  平台报 1.17 ✔（**无地板**公式会算成 1.41，差 0.24 ⇒ 证明地板存在）
* 反解样本二：``QPYr21wg`` S 1.29 / ret 0.101 / TO 0.0203 ⇒ 1.29×√(0.101/0.125)=1.160，
  平台报 1.16 ✔（TO 远低于 0.125 时收益被地板托住）
* 反解样本三：``bl82VavN`` S 1.79 / ret 0.0933 / TO 0.2835 ⇒ 1.027，平台报 1.03 ✔

⇒ **TO 地板 0.125 是硬约束**：把 TO 从 0.125 继续压低**不再改善 F**。
据此可得闭式判据 ``to_target = returns × (S / F_target)²``：

* ``to_target > 0.125`` ⇒ 减速可救，且给出**精确的 TO 天花板**
* ``to_target ≤ 0.125`` ⇒ **减速路线数学上不可达**，必须抬 returns 或 S
  （此时再刷 decay/backfill/hump 是纯浪费配额）
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Sequence, Tuple

__all__ = [
    "TO_FLOOR",
    "fitness_formula",
    "fitness_feasibility",
    "normalize_checks",
    "normalize_metrics",
    "attribute",
    "verdict_of",
]

#: F 公式的 TO 地板（2026-10-16 三点反解，见模块 docstring）
TO_FLOOR = 0.125

#: 仅在平台未回 limit 时兜底。权威仍 = 平台 checks[].limit。
DEFAULTS: Dict[str, float] = {
    "LOW_SHARPE": 1.58,
    "LOW_FITNESS": 1.0,
    "LOW_2Y_SHARPE": 1.58,
    "IS_LADDER_SHARPE": 1.58,
    "HIGH_TURNOVER": 0.70,
    "LOW_TURNOVER": 0.01,
    "PROD_CORRELATION": 0.70,
    "SELF_CORRELATION": 0.70,
}

#: LOW_SUB_UNIVERSE_SHARPE 是**比率闸**：limit ≈ 0.53 × S（见项目 MEMORY §1）
SUB_RATIO = 0.53
#: LOW_INVESTABILITY_CONSTRAINED_SHARPE 的 limit ≈ 0.70 × S（KOR 实测 0.70–0.72）
INVEST_RATIO = 0.70

#: RA 计数里，除 PASS/PENDING 外都算失败（平台 getAlphaCheckStates 口径）
_NON_FAIL_STATES = {"PASS", "PENDING"}

#: 不参与「推闸」判定的检查名（主题匹配 / 集群等非数值闸）
_NON_NUMERIC_CHECKS = {"MATCHES_THEMES", "MATCHES_PYRAMID", "DATA_DIVERSITY", "REGULAR_SUBMISSION"}

#: **上界闸**：value > limit 才失败。其余一律按下界闸（value < limit 即失败）。
#: 缺了这张表会导致 `HIGH_TURNOVER`（limit 0.7 / TO 0.087）这类**通过项被误判为失败**——
#: 2026-10-17 真实取数实证：`78oQl0n5` 因此报出「失败闸 1 道 HIGH_TURNOVER」。
_UPPER_BOUND_GATES = {
    "HIGH_TURNOVER",
    "CONCENTRATED_WEIGHT",
    "PROD_CORRELATION",
    "SELF_CORRELATION",
    "LOW_POWER_POOL_CORRELATION",
}


def _is_upper_bound(name: str) -> bool:
    return name in _UPPER_BOUND_GATES or name.startswith("HIGH_") \
        or name.endswith("_CORRELATION") or name.startswith("CONCENTRATED_")


# ---------------------------------------------------------------------------
# F 闸：公式与闭式可行性
# ---------------------------------------------------------------------------

def fitness_formula(sharpe: float, returns: float, turnover: float) -> float:
    """平台 F 闸公式：``F = S × √(returns / max(TO, TO_FLOOR))``。"""
    denom = max(abs(turnover), TO_FLOOR)
    return sharpe * math.sqrt(abs(returns) / denom)


def fitness_feasibility(
    sharpe: float, returns: float, turnover: float, target: float = 1.0
) -> Dict[str, Any]:
    """F 闸闭式可行性：给出「要过 F 需要把 TO 压到多少」，并判定减速路线是否可行。

    返回 ``to_target``（精确 TO 天花板）、``feasible_by_slowing``、
    ``arithmetic_verdict``（``"slowing_enough"`` / ``"need_more_returns_or_sharpe"``）。
    """
    to_target = abs(returns) * (sharpe / float(target)) ** 2 if sharpe > 0 else math.inf
    # 只有 TO 天花板严格高于地板时，减速才买得到 F；否则再压 TO 也没有 F 收益。
    feasible = to_target > TO_FLOOR and turnover > TO_FLOOR
    if not feasible:
        reason = "need_more_returns_or_sharpe"
    elif turnover <= to_target:
        reason = "already_passes"
    else:
        reason = "slowing_enough"
    return {
        "to_target": None if math.isinf(to_target) else round(to_target, 6),
        "to_floor": TO_FLOOR,
        "current_to": turnover,
        "feasible_by_slowing": feasible,
        "arithmetic_verdict": reason,
        # 需要砍掉多少比例的换手才有意义（None = 减速无效）
        "to_cut_pct": (
            None
            if (not feasible or math.isinf(to_target))
            else round((turnover - to_target) / turnover, 4)
            if turnover > 0
            else None
        ),
    }


# ---------------------------------------------------------------------------
# checks 解析：闸线取平台 limit；WARNING 计入 RA 失败
# ---------------------------------------------------------------------------

def _iter_check_entries(checks: Dict[str, Any]) -> List[Dict[str, Any]]:
    """把 ``checks`` 的三段（fail/warning/pending/pass）拍平成带状态的条目。"""
    out: List[Dict[str, Any]] = []
    for state in ("fail", "warning", "error", "pending", "pass"):
        for item in checks.get(state) or []:
            if isinstance(item, str):
                out.append({"name": item, "value": None, "limit": None, "state": state})
            elif isinstance(item, dict):
                out.append(
                    {
                        "name": item.get("name"),
                        "value": item.get("value"),
                        "limit": item.get("limit"),
                        "state": state,
                    }
                )
    return out


def failing_gates(checks: Dict[str, Any]) -> List[Dict[str, Any]]:
    """列出计入 RA 失败的闸（fail + warning/error），并解析出平台 limit。

    ★ **不轻信状态桶**：项目铁律「回执/工具输出不可信」。若某 check 被列在
    ``pass`` 里但 ``value < limit``（平台口径漂移时真会出现），照样判为失败——
    漏判一闸会让整轮归因给出错误的「可推」结论。
    """
    out: List[Dict[str, Any]] = []
    seen: set = set()
    for e in _iter_check_entries(checks):
        name = e["name"]
        if not name or name in _NON_NUMERIC_CHECKS or name in seen:
            continue
        state = (e["state"] or "").upper()
        limit = e["limit"]
        if not isinstance(limit, (int, float)):
            limit = DEFAULTS.get(name)
        value = e["value"]
        # 状态桶说失败，或值真的没过线，都算失败
        by_state = state not in _NON_FAIL_STATES
        by_value = False
        if isinstance(value, (int, float)) and isinstance(limit, (int, float)):
            if _is_upper_bound(str(name)):
                by_value = float(value) > float(limit)
            else:
                by_value = float(value) < float(limit)
        if not (by_state or by_value):
            continue
        seen.add(name)
        out.append({
            "name": name, "value": value, "limit": limit,
            "state": state if by_state else "value_violation",
            "direction": "upper" if _is_upper_bound(str(name)) else "lower",
        })
    return out


# ---------------------------------------------------------------------------
# 逐年归因
# ---------------------------------------------------------------------------

def normalize_yearly(yearly: Any) -> List[Dict[str, Any]]:
    """把逐年读数归一成 ``[{"year":…, "sharpe":…, …}]``。

    裸 API 的 ``recordsets/yearly-stats`` 返回 **``[schema, row1, row2, …]``**
    （首行是列名），不是 dict 列表。不归一会直接 ``AttributeError: 'list' object
    has no attribute 'get'``（2026-10-17 真实取数实证）。
    """
    if not yearly:
        return []
    if isinstance(yearly, dict):
        yearly = yearly.get("records") or yearly.get("yearly") or []
    if not isinstance(yearly, (list, tuple)) or not yearly:
        return []
    first = yearly[0]
    if isinstance(first, dict):
        return [y for y in yearly if isinstance(y, dict)]
    if isinstance(first, (list, tuple)):
        header = [str(h) for h in first]
        out: List[Dict[str, Any]] = []
        for row in yearly[1:]:
            if not isinstance(row, (list, tuple)) or len(row) != len(header):
                continue
            out.append(dict(zip(header, row)))
        return out
    return []


def _yearly_diagnosis(yearly: Sequence[Dict[str, Any]], target: float) -> Optional[Dict[str, Any]]:
    """逐年归因。**按闸分诊**：`single_collapse` 与 `recent_decay` 常常同时成立，
    但它们对不同闸的含义不同——

    * 对 **LOW_SHARPE**：单年塌陷最 actionable（压尾部即可），近段衰减反而说明别修 S；
    * 对 **IS_LADDER_SHARPE**：近段衰减最 actionable（ladder 看的就是近段窗口），
      单年塌陷若不在近段窗口内则与该闸无关。

    所以返回 ``class_for_sharpe`` / ``class_for_ladder`` 两个出口，而不是一个 class。
    """
    ys = [y for y in yearly if isinstance(y.get("sharpe"), (int, float))]
    if len(ys) < 3:
        return None
    ys = sorted(ys, key=lambda y: str(y.get("year")))
    vals = [float(y["sharpe"]) for y in ys]
    n = len(vals)
    med = sorted(vals)[n // 2]
    tail = vals[-2:]
    head = vals[:-2]
    tail_m = sum(tail) / len(tail)
    head_m = (sum(head) / len(head)) if head else tail_m
    worst_year, worst = min(zip([str(y.get("year")) for y in ys], vals), key=lambda t: t[1])

    is_collapse = worst < 0.5 and med >= 1.2
    is_decay = bool(head) and tail_m < head_m - 0.5
    if med < 1.2:
        uniform = "uniform_weak"
    else:
        uniform = "target_gap_only"

    # ladder 闸优先看近段衰减（它就是近段窗口）；sharpe 闸优先看单年塌陷
    ladder_cls = "recent_decay" if is_decay else ("single_collapse" if is_collapse else uniform)
    sharpe_cls = "single_collapse" if is_collapse else ("recent_decay" if is_decay else uniform)
    overall = "recent_decay" if is_decay else ("single_collapse" if is_collapse else uniform)

    return {
        "cause_class": overall,
        "class_for_sharpe": sharpe_cls,
        "class_for_ladder": ladder_cls,
        "flags": {"single_collapse": is_collapse, "recent_decay": is_decay},
        # 样本量置信度：<5 年时「前段/末2段」的对比不成立（本函数要求 ≥3 年才返回），
        # 结论应按 UNCLASSIFIED 对待，不要据其换轴。
        "sample_ok": len(ys) >= 5,
        "n_years": len(ys),
        "years": [str(y.get("year")) for y in ys],
        "sharpe_by_year": {str(y.get("year")): round(float(y["sharpe"]), 3) for y in ys},
        "median_sharpe": round(med, 3),
        "worst_year": worst_year,
        "worst_year_sharpe": round(worst, 3),
        "head_mean": round(head_m, 3),
        "tail2_mean": round(tail_m, 3),
        "target": target,
    }


# ---------------------------------------------------------------------------
# 剪刀差检测：同族 (S, prod) 采样是否同向且无交叉
# ---------------------------------------------------------------------------

def detect_scissor(
    siblings: Sequence[Dict[str, Any]], sharpe_now: float, limit: float = 0.70
) -> Optional[Dict[str, Any]]:
    """同族采样 ≥3 点时拟合 ``prod ~ a·S + b``，判断「推到目标 S 是否会撞线」。

    判据（KOR 分析师族实测 6 点）：
    * 斜率 ``a > 0``（S 与 prod 同向）且线性拟合外推到 ``S >= 1.58`` 时 ``prod >= limit``
      ⇒ ``crossing: false`` ⇒ 该腿在当前机制层**不可达**，应换轴。
    """
    pts = [
        (float(s["sharpe"]), float(s["prod_corr"]))
        for s in siblings
        if isinstance(s.get("sharpe"), (int, float))
        and isinstance(s.get("prod_corr"), (int, float))
    ]
    if len(pts) < 3:
        return None
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        return None
    a = sum((x - mx) * (y - my) for x, y in pts) / sxx
    b = my - a * mx
    prod_at_target = a * 1.58 + b
    return {
        "n": n,
        "slope": round(a, 4),
        "intercept": round(b, 4),
        "prod_at_sharpe_158": round(prod_at_target, 4),
        "same_direction": a > 0,
        "crossing": prod_at_target < limit,
        "samples": sorted([(round(x, 3), round(y, 4)) for x, y in pts]),
        "sharpe_now": sharpe_now,
        "verdict": (
            "reachable" if prod_at_target < limit
            else "scissor_structural" if a > 0
            else "slope_negative_check_other_axis"
        ),
    }


# ---------------------------------------------------------------------------
# 每闸的杠杆表（本项目已实测效果优先，未实测的显式标注）
# ---------------------------------------------------------------------------

def _levers_sharpe(ctx: Dict[str, Any]) -> List[Dict[str, Any]]:
    y = ctx.get("yearly") or {}
    cls = y.get("class_for_sharpe") or y.get("cause_class")
    sc = ctx.get("scissor")
    headroom = ctx.get("corr_headroom")
    out: List[Dict[str, Any]] = []
    if sc and sc.get("verdict") == "scissor_structural":
        return [{
            "rank": 1, "lever": "switch_axis_or_field",
            "rationale": f"剪刀差实测：prod 每 +0.01 换 S +0.07，外推到 S=1.58 时 prod="
                         f"{sc['prod_at_sharpe_158']} ≥ 线 {ctx.get('prod_limit')} ⇒ 同轴推 S 不可达",
            "evidence": "KOR analyst 族 6 点同向单调（2026-10-16）", "cost": "换轴成本高",
        }]
    if headroom is not None and headroom < 0.01:
        return [{
            "rank": 1, "lever": "find_prod_neutral_sharpe_lift_first",
            "rationale": f"prod 余量仅 {headroom:.4f}：任何抬高 S 的杠杆多半同时抬高 prod，"
                         f"先找一个 prod 中性的 S 杠杆，否则所有仿真都会白跑",
            "evidence": "KOR akVJLlWO prod 0.6989 / 余量 0.0011，quantile +0.09S 即顶到 0.7117",
            "cost": "需先验 prod 中性",
        }]
    if cls == "single_collapse":
        out = [
            {"rank": 1, "lever": "compress_extremes",
             "rationale": f"{y.get('worst_year')} 年 S={y.get('worst_year_sharpe')} 塌陷而中位 "
                          f"{y.get('median_sharpe')} 尚可 ⇒ 收益被少数极端股/单年主导，"
                          f"先压尾部再谈其他",
             "evidence": "rank_by_side 帖 0.28→2.44；本账号无该算子权限（inaccessible）⇒ 用 winsorize/quantile/tail 近似",
             "cost": "margin 会掉（rank_by_side 实测 0.001→0.000935）"},
            {"rank": 2, "lever": "retime_gate",
             "rationale": "换 trade_when 的信息源/窗口＝改「何时交易」，是唯一不被保序形变钉死 prod 的一族",
             "evidence": "KOR 分析师族门控窗口→S 单调 66→1.41 / 22→1.51 / 10→1.57", "cost": "低，一条仿真"},
        ]
    elif cls == "recent_decay":
        out = [{
            "rank": 1, "lever": "switch_axis_or_field",
            "rationale": f"末 2 年均值 {y.get('tail2_mean')} 明显低于前段 {y.get('head_mean')} ⇒ "
                         f"机制层衰减，继续调参只会复现同一条曲线",
            "evidence": "shortinterest38 族 4 个互不相关杠杆上 2Y 全部收敛 1.51–1.56（收敛即信号）",
            "cost": "换轴成本高"},
        ]
    elif cls == "uniform_weak":
        out = [{
            "rank": 1, "lever": "switch_axis_or_field",
            "rationale": f"逐年中位 S 仅 {y.get('median_sharpe')} ⇒ 机制整体弱，不是某闸的问题",
            "evidence": "其他575 出口腿 S 天花板 1.29（quantile/sector 均不动）", "cost": "换轴"},
        ]
    else:
        out = [
            {"rank": 1, "lever": "quantile_or_signed_power_sweep",
             "rationale": "S 差口小且分布无单年塌陷 ⇒ 先走提 S 的保序杠杆（不改排序）",
             "evidence": "KOR quantile +0.09（处方预测 +0.10，吻合）；幂次 2.5 为 IS 最优点",
             "cost": "quantile 会微抬 prod"},
            {"rank": 2, "lever": "retime_gate",
             "rationale": "门控是低成本的定向轴，改「何时交易」而非「读什么」",
             "evidence": "同上单调关系", "cost": "低"},
        ]
    return out


def _levers_fitness(ctx: Dict[str, Any]) -> List[Dict[str, Any]]:
    feas = ctx["feasibility"]
    out: List[Dict[str, Any]] = []
    if feas["arithmetic_verdict"] == "need_more_returns_or_sharpe":
        out.append({
            "rank": 1, "lever": "raise_returns_or_sharpe_not_turnover",
            "rationale": f"闭式判据：要让 F≥{feas.get('target')} 需 TO≤{feas['to_target']}，"
                         f"但 TO 地板 = {TO_FLOOR}（再压 TO 不再改善 F）⇒ 减速路线数学上不可达，"
                         f"必须抬 returns 或 S",
            "evidence": "F = S×√(returns/max(TO,0.125))，三点反解验证", "cost": "—",
        })
    else:
        out.append({
            "rank": 1, "lever": "slow_the_leg",
            "rationale": f"闭式判据：TO 天花板 {feas['to_target']}（地板 {TO_FLOOR}），"
                         f"当前 {feas['current_to']} ⇒ 需砍 {feas['to_cut_pct']:.0%} 换手",
            "evidence": "按实测 TO 降幅/强度损失排序：ts_backfill(三赢) > decay > ts_decay_linear(5) "
                        "> ts_mean；hump/TVR 类毁强度", "cost": "中",
        })
        out.append({
            "rank": 2, "lever": "margin_thickness_via_quantile",
            "rationale": "F 与 margin 同源（margin = returns/(TO×505)），加厚 margin 等价抬 F",
            "evidence": "Fitness = Sharpe × √(505 × margin)（论坛 60+ 样本拟合误差 <1%）",
            "cost": "低，保序不撞 prod",
        })
    return out


def _levers_ladder(ctx: Dict[str, Any]) -> List[Dict[str, Any]]:
    y = ctx.get("yearly") or {}
    cls = y.get("class_for_ladder") or y.get("cause_class")
    if cls == "recent_decay":
        return [{
            "rank": 1, "lever": "switch_axis_or_field",
            "rationale": f"末 2 年均值 {y.get('tail2_mean')} < 前段 {y.get('head_mean')} ⇒ "
                         f"ladder 的近段窗口是**机制层**塌陷，不是那一年运气差",
            "evidence": "KOR shortinterest38：S 1.79/F 1.03 仍 2Y 1.17，四杠杆收敛 1.51–1.56",
            "cost": "换轴"},
        ]
    if cls == "single_collapse":
        return [
            {"rank": 1, "lever": "inner_group_neutralize",
             "rationale": "内层 group_neutralize 是 2Y 的**已验证**杠杆（论坛 +77%）；"
                          "铁律：内层粒度必须严格细于外层 setting，否则退化成恒等变换",
             "evidence": "KOR shortinterest38 实测 2Y 1.17→1.51（内层 subindustry / 外层 INDUSTRY）",
             "cost": "会掉 S 与 F，并可能触发 LOW_INVESTABILITY"},
            {"rank": 2, "lever": "compress_extremes",
             "rationale": "窗口内被少数极端股主导时压尾部", "evidence": "rank_by_side 帖", "cost": "掉 margin"},
        ]
    return [
        {"rank": 1, "lever": "inner_group_neutralize",
         "rationale": "逐年无单年塌陷 ⇒ 优先试已验证的 2Y 杠杆（内层 GN），注意粒度铁律",
         "evidence": "论坛 2Y 1.15→2.04；KOR 1.17→1.51", "cost": "掉 S/F"},
        {"rank": 2, "lever": "coarser_group_axis",
         "rationale": "换粗轴（subindustry→industry→sector）是**双赢**轴（robust 与 S 同升）",
         "evidence": "KOR shortinterest38：group_rank sector 使 2Y 1.17→1.44", "cost": "掉 F"},
    ]


def _levers_sub_universe(ctx: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [{
        "rank": 1, "lever": "coarser_group_axis",
        "rationale": "sub 是**比率闸**（limit ≈ 0.53×S）⇒ sub/S < 0.53 时再高的 S 也过不了；"
                     "解法是抬 sub 而非追 S",
        "evidence": "KOR shortinterest38：group_rank sector 使 sub/S 0.674→0.856",
        "cost": "低",
    }]


def _levers_investability(ctx: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [{
        "rank": 1, "lever": "loosen_concentration",
        "rationale": "investability 受持仓集中度约束 ⇒ 放宽单股权重上限 / 加粗截断",
        "evidence": "内层 GN 后 0.89 报警（limit≈0.70×S）", "cost": "低",
    }, {
        "rank": 2, "lever": "finer_group_axis", "rationale": "组内分散持仓，降低单票权重",
        "evidence": "—", "cost": "低",
    }]


def _levers_correlation(ctx: Dict[str, Any]) -> List[Dict[str, Any]]:
    """相关性闸的杠杆表（KOR 2026-10-17 实证排序）。

    ⚠ 该闸的读数来自 ``correlation`` 而非 ``checks``：平台把 PROD/SELF 标 PENDING，
    只有 ``check_correlation`` / ``check_self_correlation`` 才给真值。
    """
    hr = ctx.get("corr_headroom")
    out: List[Dict[str, Any]] = []

    out.append({
        "rank": 1, "lever": "换持仓字段（同数据集内 uc/ac 次拥挤的同机制字段）",
        "rationale": (
            "**唯一实测有效的降 prod 手段**：KOR analyst 族 `eps_y1_estimate_change_3mo`(uc30/43)"
            " prod 0.7008 → `eps_revision_magnitude`(uc20/26) prod 0.6952（2Y 同时 2.35→2.71）。"
            "先查该字段的 uc/ac 排名——最挤字段 prod 必然在线上。"
        ),
        "evidence": "KOR 2026-10-17：prod 0.7008❌→0.6952✅、self 0.4723✅、2Y 2.35→2.71，all_passed=true",
        "cost": "S 会掉（1.60→1.39）；同机制换投影，S 天花板需重建",
    })
    out.append({
        "rank": 2, "lever": "改 trade_when 门控窗口（prod 在窗口上非单调，存在甜点）",
        "rationale": (
            "KOR 实测 gate5=0.7008 / **gate6=0.6991（过线）** / gate15=0.7003 / "
            "gate22=0.6989(std20 过) 但 std26=0.7059 ⇒ 必须在 (窗口 × std) 二维上找角点，"
            "不能只沿单一轴推。"
        ),
        "evidence": "KOR 2026-10-17 八点实测：gate6+std22 命中 prod 0.6991 / S 1.60（全闸通过）",
        "cost": "每个角点 1 次仿真 + 1 次 corr 检查；窗口过短 S 会回落（gate3 已掉）",
    })
    if hr is not None and hr >= -0.01:
        out.append({
            "rank": 3, "lever": "刀锋区：优先做 (gate × std) 二维网格，而非换结构",
            "rationale": (
                f"prod 余量 {hr:+.4f} 已进入分辨率极限。本区最优解是找『S 刚好过线 + prod 刚好在线内』"
                "的角点——已验证 gate6+std22 命中（prod 0.6991 / S 1.60）。"
            ),
            "evidence": "KOR 2026-10-17：std 轴上 prod 非单调散布 0.7000/0.7008/0.7051/0.7081，存在角点",
            "cost": "极低；但网格超过 ~10 点仍不命中即应换轴（分辨率极限）",
        })
    out.append({
        "rank": 4, "lever": "⚠ 禁投：hump（低换手腿反升 prod）",
        "rationale": (
            "hump 在 shortinterest38(TO 0.28) 降 prod 0.866→0.469，但在分析师族(TO 0.088) "
            "**反升 0.7008→0.7331**、`[0.7,0.8)` 桶 1→3 颗。判据：TO<0.15 禁投。"
        ),
        "evidence": "KOR 2026-10-17 `1YjLOebQ` prod 0.7331（对照 0.7008）；shortinterest38 上 0.866→0.469",
        "cost": "用错会直接越线；仅 TO>0.15 的腿可试",
    })
    out.append({
        "rank": 5, "lever": "⚠ 无效：保序形变 / 中性化档",
        "rationale": (
            "quantile/winsorize/signed_power 在 group_rank 外层对 prod 逐位同效（只抬 S）；"
            "KOR 实测 MARKET 0.7031、CROWDING 更差 ⇒ 中性化档不解决 prod。"
        ),
        "evidence": "KOR 2026-10-17：MARKET prod 0.7031（S 1.49）、CROWDING S 1.31；std 0.18→0.30 prod 0.7000–0.7081",
        "cost": "无效投入；只在需要抬 S 时才用",
    })
    return out


_LEVER_TABLE: Dict[str, Any] = {
    "LOW_SHARPE": _levers_sharpe,
    "LOW_FITNESS": _levers_fitness,
    "IS_LADDER_SHARPE": _levers_ladder,
    "LOW_2Y_SHARPE": _levers_ladder,
    "LOW_SUB_UNIVERSE_SHARPE": _levers_sub_universe,
    "LOW_INVESTABILITY_CONSTRAINED_SHARPE": _levers_investability,
    "PROD_CORRELATION": _levers_correlation,
    "SELF_CORRELATION": _levers_correlation,
}


# ---------------------------------------------------------------------------
# 顶层：相关性与剪刀差
# ---------------------------------------------------------------------------

def _corr_summary(correlation: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not correlation:
        return {"measured": False}
    out: Dict[str, Any] = {"measured": True}
    for kind in ("production", "prod", "self"):
        blk = correlation.get(kind)
        if not isinstance(blk, dict):
            continue
        key = "prod" if kind != "self" else "self"
        mx = blk.get("max_correlation", blk.get("max"))
        passes = blk.get("passes_check")
        rec: Dict[str, Any] = {"max": mx, "passes": passes}
        if mx is not None:
            rec["headroom"] = round(DEFAULTS["PROD_CORRELATION"] - float(mx), 4)
        hist = blk.get("histogram_nonzero") or []
        white = sum(
            h.get("n", 0) for h in hist
            if isinstance(h.get("range"), (list, tuple)) and h["range"][0] >= 0.6
        )
        rec["white_space_n_ge_0.6"] = white
        out[key] = rec
    return out


def _corr_headroom(corr: Dict[str, Any]) -> Optional[float]:
    prod = corr.get("prod") or {}
    hr = prod.get("headroom")
    return float(hr) if isinstance(hr, (int, float)) else None


def _corr_gates(corr: Dict[str, Any]) -> List[Dict[str, Any]]:
    """把 ``correlation`` 读数转成一等闸条目（PROD/SELF）。

    **为什么必须单独做**：平台的 ``checks`` 把 ``PROD_CORRELATION`` /
    ``SELF_CORRELATION`` 一律标 ``PENDING``（提交时才计算），因此
    ``failing_gates()`` 永远不会计入它们。若不在此处补，归因器在
    「RA 全过 + prod 不过」这一最常见的卡线态会误报「失败闸 0 道 ⇒ PUSH_TARGETED」。

    判定口径：``passes`` 明确为 False 即失败；否则用 ``max >= limit`` 兜底
    （提交层是**严格不等式**，实测 prod 恰为 0.7000 判 FAIL）。
    """
    if not corr or not corr.get("measured"):
        return []
    out: List[Dict[str, Any]] = []
    for key, gate in (("prod", "PROD_CORRELATION"), ("self", "SELF_CORRELATION")):
        rec = corr.get(key)
        if not isinstance(rec, dict):
            continue
        mx = rec.get("max")
        if not isinstance(mx, (int, float)):
            continue
        limit = DEFAULTS.get(gate, 0.70)
        passes = rec.get("passes")
        failed = (passes is False) or (float(mx) >= limit)
        if not failed:
            continue
        out.append({
            "name": gate, "value": round(float(mx), 4), "limit": limit,
            "state": "FAIL", "source": "correlation",
        })
    return out


def _corr_cause_class(ctx: Dict[str, Any]) -> str:
    """相关性闸的病因分型。

    * ``knife_edge``        —— 余量 ≥ −0.01：刀锋区，应做 (gate × std) 二维找角点
    * ``scissor_structural`` —— 存在 (S, prod) 剪刀差拟合，且预测过线时 prod 仍 > limit
    * ``mechanism_crowded`` —— 其余：机制层拥挤，换字段/数据集
    """
    hr = ctx.get("corr_headroom")
    sc = ctx.get("scissor") or {}
    if isinstance(hr, (int, float)) and hr >= -0.01:
        return "knife_edge"
    pred = sc.get("prod_at_sharpe_158")
    if sc.get("verdict") == "scissor_structural" or (
        isinstance(pred, (int, float)) and pred >= DEFAULTS["PROD_CORRELATION"]
    ):
        return "scissor_structural"
    return "mechanism_crowded"


def verdict_of(diag: List[Dict[str, Any]], corr: Dict[str, Any]) -> Tuple[str, str]:
    """顶层裁决 + 停手规则。"""
    classes = {d["gate"]: d.get("cause_class") for d in diag}
    if not diag:
        prod = (corr.get("prod") or {})
        selfc = (corr.get("self") or {})
        if prod.get("measured", True) and selfc.get("measured", True) \
                and prod.get("passes") and selfc.get("passes"):
            return ("READY",
                    "RA 闸 + prod + self 全过。**停手**：不要再做任何结构性改动"
                    "（任何改动都会重新掷骰子，prod 余量 <0.001 时极易掉出）。"
                    "提交权归用户，需用户明确确认后单独调用提交。")
        return ("PUSH_TARGETED",
                "RA 闸全过，但相关性未实测 ⇒ 先跑 check_correlation + "
                "check_self_correlation 补测，不要凭『0 道失败』直接判就绪。")
    corr_only = set(classes) <= {"PROD_CORRELATION", "SELF_CORRELATION"}
    if corr_only:
        cls = classes.get("PROD_CORRELATION") or classes.get("SELF_CORRELATION")
        if cls == "knife_edge":
            return ("PUSH_CORRELATION_CORNER",
                    "刀锋区：RA 已全过，仅相关性差 ≤0.01。**不要再改信号结构**——"
                    "在 (门控窗口 × winsorize std) 二维上找『S 刚好过线 + prod 刚好在线内』的角点，"
                    "每点只消耗 1 次仿真 + 1 次 corr 检查；命中后立即停手。")
        return ("BLOCKED_BY_CORRELATION",
                "相关性是唯一缺口且非刀锋区 ⇒ 该投影与生产池同源，换字段/数据集。")
    ladder_decay = classes.get("IS_LADDER_SHARPE") == "recent_decay" or \
        classes.get("LOW_2Y_SHARPE") == "recent_decay"
    if any(v in ("scissor_structural",) for v in classes.values()):
        return ("SWITCH_AXIS",
                "剪刀差：同轴推 S 结构上撞 prod 线 ⇒ 停止本腿参数搜索，换字段/数据集。")
    if ladder_decay:
        return ("SWITCH_AXIS",
                "ladder 近段窗口系统性衰减：多个互不相关杠杆收敛在同一窗口 ⇒ 本腿到机制层天花板。"
                "可以换**字段/数据集**继续，但不要再在本腿上刷参数（同轴 Δ≤0.005 即分辨率极限）。")
    if classes.get("LOW_FITNESS") == "need_more_returns_or_sharpe":
        return ("BLOCKED_BY_CORRELATION" if _corr_headroom(corr) is not None
                and _corr_headroom(corr) < 0.01 else "SWITCH_AXIS",
                "F 闸减速路线不可达（TO 地板 0.125）⇒ 不要继续刷 decay/backfill/hump。")
    hr = _corr_headroom(corr)
    if hr is not None and hr < 0.01 and "LOW_SHARPE" in classes:
        return ("BLOCKED_BY_CORRELATION",
                f"prod 余量仅 {hr:.4f} ⇒ 任何抬 S 杠杆都先验会撞线，先找 prod 中性杠杆再推。")
    return ("PUSH_TARGETED",
            "按 diagnose.levers 的 rank 顺序逐条推，每条只动一个变量；"
            "同一杠杆两次 Δ ≤ 0.005 即判定分辨率极限，停手换轴。")


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 读数归一：平台有两种形状，必须都吃
# ---------------------------------------------------------------------------

def normalize_checks(raw: Any) -> Dict[str, List[Any]]:
    """把两种平台形状归一成 ``{fail:[], warning:[], pending:[], pass:[]}``。

    形状 A（MCP ``get_alpha_details``）：``checks = {"fail":[{name,value,limit}], ...}``
    形状 B（裸 API ``GET /alphas/{id}``）：``is.checks = [{"name","result","value","limit"}]``，
    其中 ``result ∈ {PASS, FAIL, WARNING, PENDING, ERROR}``

    不归一会导致「把 list 当 dict 取 .get」而**静默漏判全部闸**——本层最大的失败模式。
    """
    if raw is None:
        return {}
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, list):
        out: Dict[str, List[Any]] = {"fail": [], "warning": [], "pending": [], "pass": []}
        for c in raw:
            if not isinstance(c, dict):
                continue
            r = str(c.get("result") or c.get("state") or "").upper()
            key = {
                "FAIL": "fail", "ERROR": "error", "WARNING": "warning",
                "PENDING": "pending", "PASS": "pass",
            }.get(r, "pass")
            out.setdefault(key, []).append(c)
        return out
    return {}


#: 裸 API 把指标**内联在 `is` 里**（无 `metrics` 子键）。缺了这条白名单
#: ⇒ `returns`/`turnover` 读成 0，F 闸闭式可行性直接失效（2026-10-17 真实取数实证）。
_METRIC_KEYS = (
    "sharpe", "fitness", "turnover", "returns", "drawdown", "margin",
    "pnl", "bookSize", "longCount", "shortCount", "startDate",
)


def normalize_metrics(detail: Dict[str, Any]) -> Dict[str, Any]:
    """取 metrics。三种形状都吃：

    * MCP ``get_alpha_details`` → 顶层 ``metrics``
    * 裸 API ``GET /alphas/{id}`` → ``is`` 里**内联**（sharpe/turnover/returns…）
    * 个别包装器 → ``is.metrics``
    """
    if not isinstance(detail, dict):
        return {}
    m = detail.get("metrics")
    if isinstance(m, dict) and m:
        return m
    inner = detail.get("is")
    if isinstance(inner, dict):
        if isinstance(inner.get("metrics"), dict) and inner["metrics"]:
            return inner["metrics"]
        inline = {k: inner[k] for k in _METRIC_KEYS if k in inner}
        if inline:
            # two_year_sharpe 不在 `is` 里，从 checks 的 IS_LADDER_SHARPE 补
            for bucket in ("pass", "warning", "fail"):
                for c in (normalize_checks(detail.get("checks")).get(bucket) or []):
                    if isinstance(c, dict) and c.get("name") in (
                            "IS_LADDER_SHARPE", "LOW_2Y_SHARPE") and c.get("value") is not None:
                        inline.setdefault("two_year_sharpe", c["value"])
                        break
            return inline
    return {}


def normalize_checks_container(detail: Dict[str, Any]) -> Dict[str, Any]:
    """定位 checks 容器并归一（MCP 顶层 ``checks`` / 裸 API ``is.checks``）。"""
    if not isinstance(detail, dict):
        return {}
    c = detail.get("checks")
    if c is None:
        inner = detail.get("is")
        if isinstance(inner, dict):
            c = inner.get("checks")
    return normalize_checks(c)


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------

def attribute(payload: Dict[str, Any]) -> Dict[str, Any]:
    """把一条候选的读数翻译成逐闸归因 + 定向杠杆 + 顶层裁决。

    ``payload`` 字段（除 ``alpha_id`` 外均可缺省；缺了就少一类归因，不报错）：

    * ``alpha_id``    —— 候选 id
    * ``detail``      —— **可选**：直接塞 ``get_alpha_details`` 的**整份返回**
      （MCP 或裸 API 形状都吃；``metrics`` / ``checks`` 会自动从中提取）
    * ``metrics``     —— 或直接给 metrics（sharpe / fitness / turnover / returns /
      margin / two_year_sharpe / sub_universe_sharpe …）
    * ``checks``      —— 或直接给 checks（**闸线取这里的 limit**）
    * ``yearly``      —— ``get_alpha_yearly_stats`` 的 ``records``
    * ``correlation`` —— ``check_correlation`` 的 ``{"production":…, "self":…}``
    * ``siblings``    —— 同族采样的 ``[{"label","sharpe","prod_corr"}]``（剪刀差检测，可选）
    """
    detail = payload.get("detail") or {}
    metrics = payload.get("metrics") or normalize_metrics(detail)
    checks = payload.get("checks") or normalize_checks_container(detail)
    yearly = normalize_yearly(payload.get("yearly"))
    corr = _corr_summary(payload.get("correlation"))

    sharpe = float(metrics.get("sharpe") or 0.0)
    returns = float(metrics.get("returns") or 0.0)
    turnover = float(metrics.get("turnover") or 0.0)
    reported_fit = metrics.get("fitness")

    fails = failing_gates(checks)
    fails.extend(_corr_gates(corr))
    y_diag = _yearly_diagnosis(yearly, target=1.58)
    scissor = detect_scissor(payload.get("siblings") or [], sharpe_now=sharpe)

    feas = fitness_feasibility(sharpe, returns, turnover, target=1.0)
    if isinstance(reported_fit, (int, float)):
        feas["reported_fitness"] = reported_fit
        feas["formula_value"] = round(fitness_formula(sharpe, returns, turnover), 3)

    ctx = {
        "yearly": y_diag, "scissor": scissor, "feasibility": feas,
        "corr_headroom": _corr_headroom(corr),
        "prod_limit": DEFAULTS["PROD_CORRELATION"],
    }

    diagnoses: List[Dict[str, Any]] = []
    for f in fails:
        name = f["name"]
        lever_fn = _LEVER_TABLE.get(name)
        if lever_fn is None:
            diagnoses.append({
                "gate": name, "value": f["value"], "limit": f["limit"],
                "cause_class": "UNMAPPED", "feasible": None,
                "levers": [], "note": "本表未收该闸；按 references/gate-attribution.md 手工补",
            })
            continue
        d = {
            "gate": name, "value": f["value"], "limit": f["limit"],
            "cause_class": (
                _corr_cause_class(ctx) if name in ("PROD_CORRELATION", "SELF_CORRELATION")
                else (y_diag or {}).get(
                    "class_for_ladder" if name in ("IS_LADDER_SHARPE", "LOW_2Y_SHARPE")
                    else "class_for_sharpe"
                ) or (y_diag or {}).get("cause_class") or "UNCLASSIFIED"
            ),
            "feasible": None, "levers": lever_fn(ctx),
        }
        if name == "LOW_FITNESS":
            d["feasible"] = feas["feasible_by_slowing"] or feas["arithmetic_verdict"] == "already_passes"
            d["fitness_feasibility"] = feas
        if name in ("IS_LADDER_SHARPE", "LOW_2Y_SHARPE"):
            d["yearly"] = y_diag
        if name == "LOW_SHARPE":
            d["scissor"] = scissor
        diagnoses.append(d)

    verdict, stop_rule = verdict_of(diagnoses, corr)

    return {
        "alpha_id": payload.get("alpha_id"),
        "failed_gates": fails,
        "gate_count": len(fails),
        "eligible_for_targeted_push": 0 < len(fails) <= 2,
        "yearly_attribution": y_diag,
        "fitness_feasibility": feas,
        "scissor": scissor,
        "correlations": corr,
        "diagnoses": diagnoses,
        "verdict": verdict,
        "stop_rule": stop_rule,
        "simulations_consumed": 0,
    }


def main() -> None:  # pragma: no cover - 便捷入口
    import json
    import sys

    if len(sys.argv) < 2:
        print("用法：读入 payload JSON 文件路径或 -（stdin），输出归因报告", file=sys.stderr)
        raise SystemExit(2)
    raw = sys.stdin.read() if sys.argv[1] == "-" else open(sys.argv[1], encoding="utf-8").read()
    print(json.dumps(attribute(json.loads(raw)), ensure_ascii=False, indent=2))