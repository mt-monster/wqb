# -*- coding: utf-8 -*-
"""wqb.region_rotation — 区域结构性饱和检测 + 跨区轮转决策。

背景
----
单区挖掘到一定阶段会「结构性饱和」：可行集（sharpe ∧ prod ∧ self 三闸全过、且尚未提交
的存量）被生产池同质化（prod 墙）与判死清单（dead_end）耗尽，继续在区内打磨只是烧算力。
本模块把 objective §7 的止损规则（"白名单被 dead_end 全覆盖→停止"、"连续 3 波全 FAIL→
转区"）自动化为**确定性、DB 驱动、可复现**的跨区轮转决策，供 CLI 与 MCP 工具共用。

设计分层（对齐 ``diagnostics.py`` 的纯函数纪律）
------------------------------------------------
- **采集层** :func:`gather_region_metrics` —— 只读 SQL，吃一个 DB-API 连接
  （``sqlite3.Connection`` 或等价），返回区域指标 dict。无副作用、无网络。
- **决策层** :func:`detect_saturation` / :func:`rank_next_regions` /
  :func:`recommend_rotation` —— **纯函数**，只吃指标 dict + 阈值/权重，返回决策 dict，
  完全可单测（无需 DB）。

关键数据纪律（2026-09-14 实测校准，勿回退）
------------------------------------------
``alphas.prod_correlation`` 只对**做过相关性核查**的 alpha 有值（通常是已提交→ACTIVE 的），
大量 harvested alpha 的 prod 为 NULL。故 ``NULL = 未测量``，既不能当「可行」（会假阳性——
实测 EUR 33 条 sharpe 达标里 29 条 prod 为 NULL，COALESCE→0 会虚报 29 条可行），也不能当
「饱和」。可行集 / prod 墙一律只在 **measured 子集**上判定；measured 样本不足
（< ``min_measured``）时，prod 相关信号**不触发**，改回传 ``data_caveat`` 显式声明证据不足，
绝不把「没测过」误报成「已饱和」。区域是否饱和由**不依赖 prod 测量量**的信号
（战役穷尽 / 判死厚度 / 波次投入）独立支撑。
"""
from __future__ import annotations

import math
from typing import Any, Dict, Iterable, List, Optional, Sequence

try:  # 规范域常量单一事实源（AGENTS.md §3.x）；测试环境若未装 src 则安全降级
    from .config import GATES_PLATFORM, REGION_PRIORITY
except Exception:  # pragma: no cover - 降级路径，常量与 config.py 保持一致
    GATES_PLATFORM = {"sharpe_min": 1.58, "prod_corr_max": 0.70, "self_corr_max": 0.70}
    REGION_PRIORITY = {}

# ---------------------------------------------------------------------------
# 阈值与权重（全部可覆写；默认值有实证依据，见各注释）
# ---------------------------------------------------------------------------

#: 饱和判定阈值。measured 样本 < min_measured 时 prod 类信号不触发（证据不足）。
SATURATION_THRESHOLDS: Dict[str, float] = {
    # prod 墙占比上限：measured 中 >=60% 撞 prod 墙 = 生产池同质（IND 实测 73%、MEA 71%）
    "prod_wall_ratio_max": 0.60,
    # prod/self 有效测量的最小样本量（与 campaign_intel s0-select --min-samples 对齐）
    "min_measured": 8,
    # 战役穷尽占比：>=80% 且战役总数 >=5 = 结构性穷尽（EUR/MEA/USA 实测 100%）
    "exhausted_pct_min": 0.80,
    "min_campaigns": 5,
    # 深挖判定：波次 >=100 且战役穷尽占比 >=exhausted_pct_min = 已充分开采
    "mined_waves_min": 100,
    # 判死清单厚度：>=50 medium，>=100 strong（EUR 110、KOR 76、IND 53）
    "dead_ends_medium": 50,
    "dead_ends_strong": 100,
    # 标的命中崩塌：产出率 <5% 且回测量 >=100（GBR 267 回测 0 达标即此类）
    "yield_floor": 0.05,
    "yield_min_backtested": 100,
    # 可行库存豁免：未提交可行存量 >= 此值 → 未被「证明」饱和，SATURATED 降级为 WATCH
    #（仍有可采库存；IND 实测 feasible_unsubmitted=8 → 豁免，EUR=0 → 不豁免）
    "feasible_reprieve_min": 5,
    # proven-zero-yield 罚：回测 >= 此量却 yield<floor = 结构性难产，轮转打分 ×0.5
    "zero_yield_min_backtested": 50,
}

#: 轮转目标排序权重（对 0-1 归一化特征加权；越大越优先作为转入区）。
ROTATION_WEIGHTS: Dict[str, float] = {
    "yield": 0.30,          # 历史产出率（passed/backtested）
    "headroom": 0.20,       # 1 - exhausted_pct（战役未穷尽余量）
    "prod_ok": 0.15,        # 1 - prod_wall_ratio（生产池不同质；未测→中性 0.5）
    "feasible": 0.20,       # 未提交可行存量（对数缩放，见 _feat_feasible）
    "untried": 0.10,        # 未开采战役数（对数缩放）
    "priority": 0.05,       # config.REGION_PRIORITY 平台优先级（次要 tiebreaker）
}

#: entry_verdict → 轮转目标可用性乘数（frozen 区不可挖，直接排除）。
_VERDICT_MULT: Dict[str, float] = {
    "active": 1.0,
    "probe-only": 0.55,
    "frozen": 0.0,
    "unknown": 0.35,
    "(unset)": 0.35,
    "(no-profile)": 0.35,
}

VERDICT_SATURATED = "SATURATED"
VERDICT_WATCH = "WATCH"
VERDICT_VIABLE = "VIABLE"


# ---------------------------------------------------------------------------
# 采集层：只读 SQL，吃 DB-API 连接
# ---------------------------------------------------------------------------

def gather_region_metrics(conn: Any, region: str,
                          gates: Optional[Dict[str, Any]] = None,
                          entry_verdict: Optional[str] = None) -> Dict[str, Any]:
    """从 DB 采集单区域的饱和/轮转指标（只读，无副作用）。

    Args:
        conn: DB-API 连接（``sqlite3.Connection`` 或等价，支持 ``execute(sql, params)``）。
        region: 区域码（大小写不敏感，内部按原样匹配 regions.name）。
        gates: 覆写 GATES_PLATFORM（sharpe_min/prod_corr_max/self_corr_max）。
        entry_verdict: 区域 profile 的 entry_verdict（active/probe-only/frozen）；
            来自 ``references/regions/<R>.md``，DB 无此列，由调用方注入。None→"unknown"。

    Returns:
        指标 dict（见模块 docstring 的字段说明）。缺表/缺列时对应字段安全降级为 0/None，
        不抛异常（轮转决策不应因单表缺失而崩）。
    """
    g = dict(GATES_PLATFORM)
    if gates:
        g.update(gates)
    smin = float(g.get("sharpe_min", 1.58))
    pmax = float(g.get("prod_corr_max", 0.70))
    smax = float(g.get("self_corr_max", 0.70))

    m: Dict[str, Any] = {
        "region": region,
        "entry_verdict": entry_verdict or "unknown",
        "gates": {"sharpe_min": smin, "prod_corr_max": pmax, "self_corr_max": smax},
    }

    # ① backtest_results：回测量与 sharpe 达标数 → 产出率（yield）
    m["backtested"], m["bt_sharpe_pass"] = _q2(
        conn,
        "SELECT COUNT(*), COALESCE(SUM(CASE WHEN ABS(COALESCE(sharpe,0))>=? THEN 1 ELSE 0 END),0) "
        "FROM backtest_results WHERE region=?",
        (smin, region),
    )
    m["yield_rate"] = round(m["bt_sharpe_pass"] / m["backtested"], 4) if m["backtested"] else None

    # ② alphas：measured 子集上的 prod 墙 / 可行集（NULL prod 不计入，见模块纪律）
    a = _row(
        conn,
        """
        SELECT
          COUNT(*) AS alphas_total,
          COALESCE(SUM(CASE WHEN sharpe>=? THEN 1 ELSE 0 END),0) AS sharpe_pass,
          COALESCE(SUM(CASE WHEN sharpe>=? AND prod_correlation IS NOT NULL THEN 1 ELSE 0 END),0) AS prod_measured,
          COALESCE(SUM(CASE WHEN sharpe>=? AND prod_correlation>=? THEN 1 ELSE 0 END),0) AS prod_wall,
          COALESCE(SUM(CASE WHEN sharpe>=? AND prod_correlation IS NOT NULL AND prod_correlation<?
                            AND (self_correlation IS NULL OR self_correlation<?) THEN 1 ELSE 0 END),0) AS feasible_measured,
          COALESCE(SUM(CASE WHEN sharpe>=? AND prod_correlation IS NOT NULL AND prod_correlation<?
                            AND (self_correlation IS NULL OR self_correlation<?)
                            AND UPPER(COALESCE(platform_status,''))<>'ACTIVE' THEN 1 ELSE 0 END),0) AS feasible_unsubmitted,
          COALESCE(SUM(CASE WHEN UPPER(COALESCE(platform_status,''))='ACTIVE' THEN 1 ELSE 0 END),0) AS active
        FROM alphas a JOIN regions r ON r.id=a.region_id
        WHERE r.name=?
        """,
        (smin, smin, smin, pmax, smin, pmax, smax, smin, pmax, smax, region),
    )
    m.update(a)
    m["prod_wall_ratio"] = (round(m["prod_wall"] / m["prod_measured"], 4)
                            if m["prod_measured"] else None)

    # ③ registry_empirical：判死/胜路/战役状态分布
    m["dead_ends"] = _q1(
        conn, "SELECT COUNT(*) FROM registry_empirical WHERE region=? AND layer='dead_end'",
        (region,))
    m["wins"] = _q1(
        conn, "SELECT COUNT(*) FROM registry_empirical WHERE region=? AND layer='win'",
        (region,))
    m["campaigns"] = _campaign_status(conn, region)
    total_camp = sum(m["campaigns"].values())
    m["campaigns_total"] = total_camp
    m["exhausted_pct"] = (round(m["campaigns"]["exhausted"] / total_camp, 4)
                          if total_camp else 0.0)

    # ④ waves：波次投入（深挖判据）
    m["waves"] = _q1(
        conn, "SELECT COUNT(*) FROM waves w JOIN regions r ON r.id=w.region_id WHERE r.name=?",
        (region,))
    return m


def gather_all_regions(conn: Any, gates: Optional[Dict[str, Any]] = None,
                       verdicts: Optional[Dict[str, str]] = None) -> Dict[str, Dict[str, Any]]:
    """采集 DB 内所有出现过（有回测/波次/alpha 记录）区域的指标。

    Args:
        conn: DB-API 连接。
        gates: 覆写 GATES_PLATFORM。
        verdicts: {region: entry_verdict} 映射（由调用方从 profile 注入）。

    Returns:
        {region: metrics_dict}。
    """
    verdicts = verdicts or {}
    names = set()
    for sql in (
        "SELECT DISTINCT region FROM backtest_results WHERE region IS NOT NULL",
        "SELECT name FROM regions",
    ):
        try:
            for (r,) in conn.execute(sql):
                if r:
                    names.add(r)
        except Exception:
            continue
    # 只保留有实际活动痕迹的区域（回测/alpha/波次任一 >0），排除 GLOBAL/PINGTEST 等非挖掘占位
    out: Dict[str, Dict[str, Any]] = {}
    for r in sorted(names):
        mm = gather_region_metrics(conn, r, gates=gates, entry_verdict=verdicts.get(r))
        if mm["backtested"] or mm["alphas_total"] or mm["waves"]:
            out[r] = mm
    return out


# ---------------------------------------------------------------------------
# 决策层：纯函数（吃指标 dict，无 DB / 无网络）
# ---------------------------------------------------------------------------

def detect_saturation(metrics: Dict[str, Any],
                      thresholds: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """判定单区域是否结构性饱和（纯函数）。

    Args:
        metrics: :func:`gather_region_metrics` 产出的指标 dict（或手工构造的同形 dict）。
        thresholds: 覆写 SATURATION_THRESHOLDS。

    Returns:
        ``{"verdict": SATURATED|WATCH|VIABLE, "strong": [...], "medium": [...],
        "reasons": [...], "data_caveat": str|None, "signals": {...}}``。
        verdict 规则：frozen 硬饱和；否则 strong>=2 → SATURATED，strong==1 或 medium>=2 →
        WATCH，其余 VIABLE。prod 类信号在 measured<min_measured 时**不触发**（回 data_caveat）。
    """
    t = dict(SATURATION_THRESHOLDS)
    if thresholds:
        t.update(thresholds)
    m = metrics or {}
    strong: List[str] = []
    medium: List[str] = []
    reasons: List[str] = []

    verdict_profile = str(m.get("entry_verdict") or "unknown").lower()
    exhausted_pct = float(m.get("exhausted_pct") or 0.0)
    campaigns_total = int(m.get("campaigns_total") or sum((m.get("campaigns") or {}).values()))
    waves = int(m.get("waves") or 0)
    dead_ends = int(m.get("dead_ends") or 0)
    prod_measured = int(m.get("prod_measured") or 0)
    prod_wall_ratio = m.get("prod_wall_ratio")
    feasible_unsub = int(m.get("feasible_unsubmitted") or 0)
    yield_rate = m.get("yield_rate")
    backtested = int(m.get("backtested") or 0)

    # 硬冻结：profile 判 frozen（如 MEA 本季度不提交）
    if verdict_profile == "frozen":
        strong.append("frozen_profile")
        reasons.append("区域 profile entry_verdict=frozen（平台/季度限制，不可挖）")

    # 战役穷尽（不依赖 prod 测量）
    if exhausted_pct >= t["exhausted_pct_min"] and campaigns_total >= t["min_campaigns"]:
        strong.append("campaigns_exhausted")
        reasons.append(f"战役穷尽 {exhausted_pct:.0%}（{campaigns_total} 个战役，"
                       f"{(m.get('campaigns') or {}).get('exhausted', '?')} exhausted）")

    # 深挖 + 穷尽（波次投入巨大且战役已穷尽）
    if waves >= t["mined_waves_min"] and exhausted_pct >= t["exhausted_pct_min"]:
        strong.append("mined_out")
        reasons.append(f"已深挖 {waves} 波且战役穷尽 {exhausted_pct:.0%}（开采充分）")

    # 判死清单厚度（不依赖 prod 测量）
    if dead_ends >= t["dead_ends_strong"]:
        strong.append("dead_end_saturated")
        reasons.append(f"判死清单厚重 dead_ends={dead_ends}（>={t['dead_ends_strong']:.0f}）")
    elif dead_ends >= t["dead_ends_medium"]:
        medium.append("dead_ends_thick")
        reasons.append(f"判死清单偏厚 dead_ends={dead_ends}（>={t['dead_ends_medium']:.0f}）")

    # 标的命中崩塌（回测很多但 sharpe 达标极少）
    if (yield_rate is not None and yield_rate < t["yield_floor"]
            and backtested >= t["yield_min_backtested"]):
        medium.append("yield_collapse")
        reasons.append(f"产出率崩塌 yield={yield_rate:.1%}（{backtested} 回测，"
                       f"<{t['yield_floor']:.0%}）")

    # prod 墙 / 无可行存量：仅在 measured 充足时触发（否则证据不足）
    data_caveat: Optional[str] = None
    if prod_measured < t["min_measured"]:
        data_caveat = (f"prod 仅 {prod_measured} 条有效测量（<{t['min_measured']:.0f}），"
                       f"prod 墙/可行集证据不足；NULL prod ≠ 可行，需 live 重测方能定论")
    else:
        if prod_wall_ratio is not None and prod_wall_ratio >= t["prod_wall_ratio_max"]:
            strong.append("prod_wall")
            reasons.append(f"生产池同质：measured 中 {prod_wall_ratio:.0%} 撞 prod 墙"
                           f"（{m.get('prod_wall')}/{prod_measured}）")
        if feasible_unsub <= 0:
            strong.append("no_feasible_headroom")
            reasons.append(f"无未提交可行存量（feasible_unsubmitted={feasible_unsub}，"
                           f"measured 口径三闸全过者已耗尽/已 ACTIVE）")

    n_strong, n_medium = len(strong), len(medium)
    if verdict_profile == "frozen" or n_strong >= 2 or (n_strong >= 1 and n_medium >= 2):
        verdict = VERDICT_SATURATED
    elif n_strong >= 1 or n_medium >= 2:
        verdict = VERDICT_WATCH
    else:
        verdict = VERDICT_VIABLE

    # 可行库存豁免：仍有未提交可行存量 → 未被「证明」饱和，降级为 WATCH（frozen 除外）
    if (verdict == VERDICT_SATURATED and verdict_profile != "frozen"
            and feasible_unsub >= t["feasible_reprieve_min"]):
        verdict = VERDICT_WATCH
        reasons.append(f"可行库存豁免：feasible_unsubmitted={feasible_unsub}"
                       f"（>={t['feasible_reprieve_min']:.0f}），仍有可采存量，SATURATED→WATCH")

    return {
        "verdict": verdict,
        "strong": strong,
        "medium": medium,
        "reasons": reasons,
        "data_caveat": data_caveat,
        "signals": {
            "exhausted_pct": exhausted_pct,
            "campaigns_total": campaigns_total,
            "waves": waves,
            "dead_ends": dead_ends,
            "yield_rate": yield_rate,
            "prod_measured": prod_measured,
            "prod_wall_ratio": prod_wall_ratio,
            "feasible_unsubmitted": feasible_unsub,
            "entry_verdict": m.get("entry_verdict"),
        },
    }


def rotation_score(metrics: Dict[str, Any],
                   saturation: Optional[Dict[str, Any]] = None,
                   weights: Optional[Dict[str, float]] = None,
                   thresholds: Optional[Dict[str, float]] = None) -> float:
    """轮转目标适配分（0-1，越大越适合作为转入区）。纯函数。

    特征全部归一化到 0-1 后按 ROTATION_WEIGHTS 加权，再乘 entry_verdict 可用性乘数；
    已判 SATURATED 的区域额外罚 0.5（仍可作"最不乏味"兜底，但排在新开垦区之后）。

    诚实性纪律（2026-09-14 校准，勿回退）：
      - prod_ok 仅在 measured >= min_measured 时采信 prod_wall_ratio；薄样本/未测→中性 0.5
        （GBR 仅 4 条 measured、GLB 仅 1 条，不得据此给满分 prod_ok 而虚高排名）。
      - proven-zero-yield 罚：回测量 >= zero_yield_min_backtested 却 yield<floor = 结构性
        难产（GBR 267 回测 0 达标），×0.5 沉底，避免把"没人记录战役状态"误当"新大陆"。
    """
    t = dict(SATURATION_THRESHOLDS)
    if thresholds:
        t.update(thresholds)
    w = dict(ROTATION_WEIGHTS)
    if weights:
        w.update(weights)
    m = metrics or {}

    f_yield = _clamp01(m.get("yield_rate") or 0.0) / 0.40  # 40% 产出率封顶为满分
    f_headroom = 1.0 - _clamp01(m.get("exhausted_pct") or 0.0)
    prod_measured = int(m.get("prod_measured") or 0)
    pwr = m.get("prod_wall_ratio")
    # prod_ok 仅在 measured 充足时可信；样本不足→中性 0.5（薄样本 ≠ 低 prod 风险）
    f_prod = ((1.0 - _clamp01(pwr))
              if (pwr is not None and prod_measured >= t["min_measured"]) else 0.5)
    f_feasible = _feat_log(m.get("feasible_unsubmitted") or 0, cap=20)
    f_untried = _feat_log((m.get("campaigns") or {}).get("untried", 0) or 0, cap=10)
    f_priority = _clamp01((REGION_PRIORITY.get(str(m.get("region")), 1) - 1) / 2.0)

    raw = (w["yield"] * _clamp01(f_yield) + w["headroom"] * f_headroom
           + w["prod_ok"] * f_prod + w["feasible"] * f_feasible
           + w["untried"] * f_untried + w["priority"] * f_priority)
    wsum = sum(w.values()) or 1.0
    score = raw / wsum

    mult = _VERDICT_MULT.get(str(m.get("entry_verdict") or "unknown").lower(), 0.35)
    score *= mult
    if saturation and saturation.get("verdict") == VERDICT_SATURATED:
        score *= 0.5
    # proven-zero-yield 罚：大量回测却几乎不达标 = 结构性难产，非"新大陆"
    yr = m.get("yield_rate")
    if (yr is not None and yr < t["yield_floor"]
            and int(m.get("backtested") or 0) >= t["zero_yield_min_backtested"]):
        score *= 0.5
    return round(score, 4)


def rank_next_regions(all_metrics: Dict[str, Dict[str, Any]],
                      exclude: Iterable[str] = (),
                      thresholds: Optional[Dict[str, float]] = None,
                      weights: Optional[Dict[str, float]] = None,
                      include_saturated: bool = True) -> List[Dict[str, Any]]:
    """对所有区域按轮转适配分排序，返回候选列表（纯函数）。

    Args:
        all_metrics: {region: metrics_dict}。
        exclude: 排除的区域码（通常是当前饱和区）。
        thresholds / weights: 覆写默认。
        include_saturated: True（默认）→ 饱和区也进列表但被罚分沉底（供"全饱和"兜底）；
            False → 只返回非 SATURATED 区。

    Returns:
        ``[{"region", "score", "verdict", "saturation", "yield_rate", "feasible_unsubmitted",
        "exhausted_pct", "entry_verdict", "reasons"}]``，按 score 降序。frozen 区始终排除
        （不可挖）。
    """
    excl = {str(e).upper() for e in (exclude or ())}
    out: List[Dict[str, Any]] = []
    for rg, m in (all_metrics or {}).items():
        if str(rg).upper() in excl:
            continue
        if str(m.get("entry_verdict") or "").lower() == "frozen":
            continue  # 冻结区不可作为转入目标
        sat = detect_saturation(m, thresholds=thresholds)
        if not include_saturated and sat["verdict"] == VERDICT_SATURATED:
            continue
        out.append({
            "region": rg,
            "score": rotation_score(m, sat, weights=weights, thresholds=thresholds),
            "verdict": sat["verdict"],
            "saturation": sat,
            "yield_rate": m.get("yield_rate"),
            "feasible_unsubmitted": m.get("feasible_unsubmitted"),
            "exhausted_pct": m.get("exhausted_pct"),
            "prod_wall_ratio": m.get("prod_wall_ratio"),
            "entry_verdict": m.get("entry_verdict"),
            "reasons": sat["reasons"],
        })
    out.sort(key=lambda x: (-x["score"], x["region"]))
    return out


def recommend_rotation(current_region: str,
                       all_metrics: Dict[str, Dict[str, Any]],
                       target: Optional[int] = None,
                       thresholds: Optional[Dict[str, float]] = None,
                       weights: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """顶层轮转决策：当前区饱和？→ 推荐转入区 + 承接目标（纯函数）。

    Args:
        current_region: 当前挖掘区。
        all_metrics: {region: metrics_dict}（含 current_region）。
        target: 待承接的过闸目标数（如 objective 的 20）；写入 carry_target。
        thresholds / weights: 覆写默认。

    Returns:
        ``{"should_rotate": bool, "from_region", "current_saturation", "to_region",
        "ranked": [...], "carry_target", "all_saturated": bool, "reason", "next_action"}``。
        - 当前区非 SATURATED → should_rotate=False，to_region=None，next_action="继续当前区"。
        - 当前区 SATURATED 且有非饱和候选 → to_region=最高分非饱和区。
        - 当前区 SATURATED 但候选全饱和 → all_saturated=True，to_region=最不乏味者，
          next_action 提示升级 brain-next-move-analysis（平台级 prod 墙，非单区问题）。
    """
    cur = (all_metrics or {}).get(current_region)
    if cur is None:
        return {
            "should_rotate": False, "from_region": current_region, "to_region": None,
            "current_saturation": None, "ranked": [], "carry_target": target,
            "all_saturated": False, "error": f"无 {current_region} 指标（DB 无记录？）",
            "reason": "当前区无指标，无法判定饱和", "next_action": "核查 DB / 区域码",
        }
    cur_sat = detect_saturation(cur, thresholds=thresholds)
    if cur_sat["verdict"] != VERDICT_SATURATED:
        return {
            "should_rotate": False, "from_region": current_region, "to_region": None,
            "current_saturation": cur_sat, "ranked": [], "carry_target": target,
            "all_saturated": False,
            "reason": f"{current_region} 未达饱和（verdict={cur_sat['verdict']}）",
            "next_action": f"继续 {current_region} 的 Phase 1 挖掘",
        }

    ranked = rank_next_regions(all_metrics, exclude=(current_region,),
                               thresholds=thresholds, weights=weights,
                               include_saturated=True)
    viable = [r for r in ranked if r["verdict"] != VERDICT_SATURATED]
    all_saturated = not viable
    pick = (viable or ranked or [None])[0]
    to_region = pick["region"] if pick else None

    if to_region is None:
        reason = f"{current_region} 已饱和且无其它可挖区域"
        next_action = "升级 brain-next-move-analysis：平台级 prod 墙，非单区问题"
    elif all_saturated:
        reason = (f"{current_region} 饱和（{'; '.join(cur_sat['reasons'][:2])}），"
                  f"但所有候选区亦近饱和——{to_region} 为相对最优（score={pick['score']}）")
        next_action = (f"谨慎转 {to_region}（先 P0.3 探针验可行集），并升级 "
                       f"brain-next-move-analysis 评估平台级 prod 墙")
    else:
        reason = (f"{current_region} 饱和（{'; '.join(cur_sat['reasons'][:2])}）→ "
                  f"转 {to_region}（score={pick['score']}, yield={pick['yield_rate']}, "
                  f"未提交可行存量={pick['feasible_unsubmitted']}, verdict={pick['verdict']}）")
        next_action = (f"在 {to_region} 重启 Phase 1（S-PRE→S6），承接目标 "
                       f"{target if target is not None else 'N'} 颗过闸；先跑步 1 查表 + P0.3 探针")

    return {
        "should_rotate": True, "from_region": current_region, "to_region": to_region,
        "current_saturation": cur_sat, "ranked": ranked, "carry_target": target,
        "all_saturated": all_saturated, "reason": reason, "next_action": next_action,
    }


# ---------------------------------------------------------------------------
# 内部小工具
# ---------------------------------------------------------------------------

def _clamp01(x: Any) -> float:
    try:
        return max(0.0, min(1.0, float(x)))
    except (TypeError, ValueError):
        return 0.0


def _feat_log(n: Any, cap: int) -> float:
    """对数缩放计数特征到 0-1（cap 处饱和为 1.0）。"""
    try:
        n = float(n or 0)
    except (TypeError, ValueError):
        return 0.0
    if n <= 0:
        return 0.0
    return _clamp01(math.log1p(n) / math.log1p(cap))


def _q1(conn: Any, sql: str, params: Sequence = ()) -> int:
    try:
        row = conn.execute(sql, tuple(params)).fetchone()
        return int(row[0]) if row and row[0] is not None else 0
    except Exception:
        return 0


def _q2(conn: Any, sql: str, params: Sequence = ()) -> tuple:
    try:
        row = conn.execute(sql, tuple(params)).fetchone()
        return (int(row[0] or 0), int(row[1] or 0)) if row else (0, 0)
    except Exception:
        return (0, 0)


def _row(conn: Any, sql: str, params: Sequence = ()) -> Dict[str, int]:
    """执行聚合查询，返回 {列名: int}；缺表/缺列安全降级为全 0。"""
    keys = ["alphas_total", "sharpe_pass", "prod_measured", "prod_wall",
            "feasible_measured", "feasible_unsubmitted", "active"]
    try:
        # 按整数下标取值，sqlite3.Row 与 tuple 均兼容；不篡改调用方 row_factory
        row = conn.execute(sql, tuple(params)).fetchone()
        if not row:
            return {k: 0 for k in keys}
        return {k: int(row[i] or 0) for i, k in enumerate(keys)}
    except Exception:
        return {k: 0 for k in keys}


def _campaign_status(conn: Any, region: str) -> Dict[str, int]:
    """从 registry_empirical layer=campaign 统计 untried/in_progress/exhausted。"""
    camp = {"untried": 0, "in_progress": 0, "exhausted": 0}
    try:
        import json as _json
        for (payload,) in conn.execute(
                "SELECT payload FROM registry_empirical WHERE region=? AND layer='campaign'",
                (region,)):
            try:
                st = (_json.loads(payload) or {}).get("status") if payload else None
            except Exception:
                continue
            if st in camp:
                camp[st] += 1
    except Exception:
        pass
    return camp
