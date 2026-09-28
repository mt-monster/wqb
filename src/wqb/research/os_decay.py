# -*- coding: utf-8 -*-
"""os_decay.py — IS→OS 衰减校准（步 7 评审的实证折算层）。

## 为什么需要

2026-09-20 实测 124 个有 OS 样本的已提交 alpha（USA）：

| 指标 | 值 |
|---|---|
| IS sharpe 均值 | 1.53 |
| OS sharpe 均值 | 0.55 |
| osISSharpeRatio 均值 | **0.358**（保留约 36%） |
| OS <= 0 占比 | **21.8%** |

**关键发现：IS sharpe 与 OS sharpe 的 Spearman 秩相关仅 +0.086** ——
在已过 IS 闸的样本里，IS 高低几乎不能预测 OS 高低（IS 低半 OS 均值 0.50
vs 高半 0.60，OS>0 率 79% vs 77%）。因此本模块**不**用来抬高 IS 阈值
（那是错误用法），而是提供两件事：

1. **预期产出折算**（`expected_os_sharpe`）：把候选的 IS 指标折算成预期 OS 水位，
   用于提交排序与「这颗值不值得占配额」的期望值判断；
2. **存活率提示**（`survival_hint`）：该候选所属区间的历史 OS>0 概率，
   用于风险提示（不是硬闸）。

## 用法

    from wqb.research.os_decay import load_baseline, calibrate_review
    base = load_baseline(store)              # 读 DB 实证基线
    info = calibrate_review(candidate_row, base)
    # -> {"expected_os_sharpe": 0.63, "expected_os_fitness": ..., "survival_rate": 0.78,
    #     "decay_ratio": 0.358, "basis": "USA n=124", "note": "..."}

基线缺失（新工作区/未同步）时全部返回 None 并带 `basis="no_sample"`，
调用方应据此跳过折算（fail-open，不阻断评审）。
"""
from __future__ import annotations

from typing import Any, Dict, Optional

#: 平台提交硬线（与 config.GATES 一致；此模块不重复定义阈值，仅作折算锚点）
SUBMIT_GATE_SHARPE = 1.58

#: 基线样本量下限：低于此值不折算（统计不可靠）
MIN_SAMPLE = 30

#: 默认衰减比（DB 无样本时的保守兜底；来源：2026-09-20 USA 124 例实测 0.358）
DEFAULT_DECAY_RATIO = 0.358


def load_baseline(store: Any, region: Optional[str] = None) -> Dict[str, Any]:
    """从 DB 读 OS 衰减基线（薄封装 store.os_decay_baseline）。

    返回 dict 至少含 `n`；n < MIN_SAMPLE 时调用方应视为无样本。
    """
    try:
        base = store.os_decay_baseline(region)
    except Exception as e:  # noqa: BLE001 — 基线不可得不应阻断评审
        return {"n": 0, "error": str(e)}
    return base or {"n": 0}


def calibrate_review(row: Dict[str, Any], baseline: Optional[Dict[str, Any]],
                     region: Optional[str] = None) -> Dict[str, Any]:
    """把一行评审候选按 OS 衰减基线折算。

    Args:
        row: 评审行（含 sharpe / fitness / two_year_sharpe 等 IS 指标）
        baseline: load_baseline() 的返回值；None 或样本不足则只返回 note
        region: 区域名（仅用于 basis 标注）

    Returns:
        {
          "expected_os_sharpe": float|None,   # IS sharpe × 衰减比
          "expected_os_fitness": float|None,  # IS fitness × 衰减比
          "survival_rate": float|None,        # 该区历史 OS>0 概率
          "decay_ratio": float|None,
          "basis": str,                       # 样本来源说明
          "note": str,                        # 人读结论
        }
    """
    out: Dict[str, Any] = {
        "expected_os_sharpe": None, "expected_os_fitness": None,
        "survival_rate": None, "decay_ratio": None,
        "basis": "no_sample", "note": "",
    }
    n = int((baseline or {}).get("n") or 0)
    if n < MIN_SAMPLE:
        out["note"] = (f"OS 基线样本不足（n={n} < {MIN_SAMPLE}），跳过折算；"
                       "先跑 tools/sync_platform_alphas.py 同步平台 OS 池")
        return out

    ratio = float(baseline.get("os_is_sharpe_ratio_mean") or DEFAULT_DECAY_RATIO)
    # 存活率 = 1 - OS<=0 占比（基线里是百分数）
    nonpos_pct = baseline.get("non_positive_pct")
    survival = None
    if nonpos_pct is not None:
        survival = round(1.0 - float(nonpos_pct) / 100.0, 4)

    out["decay_ratio"] = round(ratio, 4)
    out["survival_rate"] = survival
    out["basis"] = f"{region or baseline.get('region') or 'ALL'} n={n}"

    sh = row.get("sharpe")
    if isinstance(sh, (int, float)):
        out["expected_os_sharpe"] = round(float(sh) * ratio, 4)
    fit = row.get("fitness")
    if isinstance(fit, (int, float)):
        out["expected_os_fitness"] = round(float(fit) * ratio, 4)

    exp = out["expected_os_sharpe"]
    if exp is not None:
        gap = SUBMIT_GATE_SHARPE - exp
        if exp >= SUBMIT_GATE_SHARPE:
            verdict = f"预期 OS {exp:.2f} ≥ 提交线 {SUBMIT_GATE_SHARPE}（历史罕见，仅 11% 做到）"
        elif exp >= 1.0:
            verdict = f"预期 OS {exp:.2f}（过 1.0 但低于提交线，差 {gap:.2f}）"
        else:
            verdict = f"预期 OS {exp:.2f}（低于 1.0，样本外大概率平庸）"
        out["note"] = (
            f"{verdict}。折算口径：IS sharpe × {ratio:.3f}（{out['basis']} 实测衰减比）；"
            f"历史存活率（OS>0）约 {survival:.0%}。" if survival is not None else
            f"{verdict}。折算口径：IS sharpe × {ratio:.3f}（{out['basis']}）。"
        )
        # 重要提示：IS 与 OS 秩相关仅 +0.086，折算只给期望值、不构成排序依据
        out["caveat"] = ("IS 与 OS 的秩相关仅 +0.086（实测）：折算值反映期望水位，"
                         "不能据此判定单个候选优劣；提高 IS 阈值不会提升 OS 存活率。")
    return out


def annotate_rows(rows: list, baseline: Optional[Dict[str, Any]],
                  region: Optional[str] = None) -> Dict[str, Any]:
    """给一批评审行就地追加 os_calibration 字段（供 review_wave 打印/入库）。

    Returns: {"annotated": n, "basis": ..., "decay_ratio": ...}
    """
    annotated = 0
    for r in rows or []:
        try:
            info = calibrate_review(r, baseline, region)
            r["os_calibration"] = info
            if info.get("expected_os_sharpe") is not None:
                annotated += 1
        except Exception:  # noqa: BLE001 — 单行失败不影响整批
            r["os_calibration"] = {"basis": "error"}
    return {"annotated": annotated,
            "basis": (baseline or {}).get("n", 0) and f"n={(baseline or {}).get('n')}" or "no_sample",
            "decay_ratio": (baseline or {}).get("os_is_sharpe_ratio_mean")}
