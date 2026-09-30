# -*- coding: utf-8 -*-
"""step_scoring — 质量/效能/增益评分的**唯一实现**（R2 单点，2026-09-30 方案 B）。

历史教训（2026-09-17 下线评估）：旧方案 CLI 与 MCP 两份归一化公式互相漂移
（efficiency_score=13.33 超界事故）。自本模块起，任何"分数"都必须经此计算；
CLI（tools/step_funnel.py --full）与 MCP（wqb_db_mcp get_step_eval_report）
都 import 本模块，禁止各自实现。

## 口径（替代旧的魔法常数归一化与 net_gain 合成分）

- 一切进入评分的指标必须是**好方向比率**（越高越好，∈ [0,1]）；
  原始量（时长/吞吐/计数）标 `score_eligible=False`，只展示不评分。
- 三个分数 = 各维度 score_eligible 指标的等权平均；全 None → None（未知，不报 0）。
- ROI = 达标产出 / 配额消耗 = cheap_pass / backtest_rows ∈ [0,1]；
  单位成本 = backtest_rows / cheap_pass 为原始量（≥1 或 None），不评分。
- 边界铁律（R5）：任何 x/y，y 为 0/None → None；**禁止除零、禁止 inf、禁止魔法常数**。
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional


def safe_ratio(numerator: Optional[float], denominator: Optional[float]) -> Optional[float]:
    """安全比率：分母缺失/为 0 → None（未知）；分子缺失 → None。结果夹在 [0,1] 外时原样返回由调用方决定。"""
    if numerator is None or denominator is None:
        return None
    try:
        n = float(numerator)
        d = float(denominator)
    except (TypeError, ValueError):
        return None
    if d == 0.0:
        return None
    return n / d


def safe_rate(numerator: Optional[float], denominator: Optional[float]) -> Optional[float]:
    """好方向比率：safe_ratio 且结果夹到 [0,1]（超出说明口径错，夹住并由契约测试抓）。"""
    r = safe_ratio(numerator, denominator)
    if r is None:
        return None
    return max(0.0, min(1.0, r))


def score_metrics(metrics: Iterable[Dict[str, Any]]) -> Optional[float]:
    """对一组指标条目取等权平均分。

    每条目形如 {"value": float|None, "score_eligible": bool, ...}；
    只对 score_eligible 且 value 非 None 的条目求均值；一条都没有 → None。
    入参 value 会被再次夹到 [0,1]（防上游口径漂移，R5）。
    """
    vals: List[float] = []
    for m in metrics or []:
        if not m.get("score_eligible"):
            continue
        v = m.get("value")
        if v is None:
            continue
        try:
            fv = float(v)
        except (TypeError, ValueError):
            continue
        vals.append(max(0.0, min(1.0, fv)))
    if not vals:
        return None
    return sum(vals) / len(vals)


def compute_scores(step_matrix: Dict[str, Dict[str, List[Dict[str, Any]]]],
                   counts: Optional[Dict[str, Optional[float]]] = None) -> Dict[str, Optional[float]]:
    """由九步指标矩阵计算总评分。

    Args:
        step_matrix: {step: {"quality": [...], "efficiency": [...], "gain": [...]}}
        counts: 客观计数 {"backtested": n, "cheap_pass": n}（供 ROI）；缺省从矩阵外由调用方传入

    Returns:
        {"quality": Q|None, "efficiency": E|None, "gain": G|None,
         "roi": R|None, "unit_cost": u|None}
        全部遵守：比率 ∈ [0,1] 或 None；unit_cost 为原始量（≥1 或 None）。
    """
    q_metrics: List[Dict[str, Any]] = []
    e_metrics: List[Dict[str, Any]] = []
    g_metrics: List[Dict[str, Any]] = []
    for dims in (step_matrix or {}).values():
        q_metrics.extend(dims.get("quality") or [])
        e_metrics.extend(dims.get("efficiency") or [])
        g_metrics.extend(dims.get("gain") or [])

    counts = counts or {}
    cheap = counts.get("cheap_pass")
    backtested = counts.get("backtested")
    roi = safe_rate(cheap, backtested)
    unit_cost = None
    if cheap not in (None, 0) and backtested is not None:
        try:
            unit_cost = float(backtested) / float(cheap)
        except (TypeError, ValueError, ZeroDivisionError):
            unit_cost = None

    return {
        "quality": score_metrics(q_metrics),
        "efficiency": score_metrics(e_metrics),
        "gain": score_metrics(g_metrics),
        "roi": roi,
        "unit_cost": unit_cost,
    }
