# -*- coding: utf-8 -*-
"""wqb.diagnostics — 论坛实证的两组零成本预检（ProdCorr 下限 / 过拟合四信号）。

来源：WorldQuant BRAIN 中文社区论坛高赞实战帖（2026-09-13 汇总落地）：
  - `prod_corr_lower_bound`：`[31431137051927]`「本地 Corr 增强版：预估 ProdCorr 下限」(68 赞)
  - `overfit_signals`：`[42018671130391]` 过拟合三信号 + 评论区补第 4 信号（逐年 corr 跳变）

定位：**提交前 / 上平台查相关前的零成本剪枝**。两条都不触平台、不耗配额，
目的是在昂贵的 `check_correlation` 之前就把明显没戏的候选筛掉。

纪律：只做诊断，不替研究者做决定；阈值可按区域/数据集覆写。
"""
from __future__ import annotations

import math
import statistics
from typing import Dict, Iterable, Optional, Sequence

# 平台 ProdCorr 硬闸（regular alpha）
PROD_CORR_LIMIT = 0.7

OVERFIT_THRESHOLDS: Dict[str, float] = {
    # decay 后 sharpe / 基准 sharpe < 此值 → 断崖（原贴实证：decay=5 即 1.8→0.8，比值 0.44）
    "decay_cliff_ratio": 0.55,
    # 年份间 Sharpe 方差上限（正常 0.3–0.5，>1.0 = 单年行情驱动）
    "yearly_sharpe_var_max": 1.0,
    # 去掉 top/bottom 10% 后 Sharpe / 原 Sharpe < 此值 → 腰斩（赌 outlier）
    "tail_trim_halve_ratio": 0.55,
    # 相邻两年信号相关性跳变上限（>0.4 = 训练窗覆盖独特 regime）
    "yearly_corr_jump_max": 0.4,
}


def prod_corr_lower_bound(y: Optional[float], know_corr: Optional[float]) -> Optional[float]:
    """用「相关性传递不等式」预估待检 alpha 的 ProdCorr **下限**。

    原理：已知 alpha A 的平台 ProdCorr = `know_corr`，待检 alpha B 与 A 的
    PnL 相关系数 = `y`，则 B 与生产池的相关系数存在下界：

        corr_min = y·k − √(1−k²)·√(1−y²)      （k = know_corr）

    **用途**：若 `corr_min > 0.7`，则无论 B 与池中其它 alpha 关系如何，
    其 ProdCorr 必然超标 → 直接放弃上平台查相关，省一次限流名额。

    Args:
        y: B 与 A 的 PnL 相关系数（-1~1）。
        know_corr: A 已实测的平台 ProdCorr（-1~1）。

    Returns:
        下限估计值（[-1, 1]），或 None（入参缺失）。

    Note:
        这是**保守**下界——实测 y=0.95/k=0.85 时下限仅 0.643（未超限），
        需 y≥0.99 且 k≥0.9 才会超过 0.7。所以它只能"确定性劝退"，
        不能用来"确定性放行"；下限未超限时仍需上平台实测。
    """
    if y is None or know_corr is None:
        return None
    y = max(-1.0, min(1.0, float(y)))
    k = max(-1.0, min(1.0, float(know_corr)))
    return y * k - math.sqrt(max(0.0, 1.0 - k * k)) * math.sqrt(max(0.0, 1.0 - y * y))


def should_skip_prod_check(y: Optional[float], know_corr: Optional[float],
                           limit: float = PROD_CORR_LIMIT) -> Optional[bool]:
    """下限已超限时返回 True（应跳过平台查相关）；入参缺失返回 None。"""
    lb = prod_corr_lower_bound(y, know_corr)
    if lb is None:
        return None
    return lb > limit


def overfit_signals(
    yearly_sharpe: Optional[Sequence[float]] = None,
    decay_sharpe: Optional[Dict[int, float]] = None,
    yearly_corr: Optional[Sequence[float]] = None,
    sharpe_full: Optional[float] = None,
    sharpe_trimmed: Optional[float] = None,
    thresh: Optional[Dict[str, float]] = None,
) -> Dict[str, object]:
    """过拟合四信号检测（任一命中即应拒绝提交）。

    Args:
        yearly_sharpe: 逐年 Sharpe 列表（≥3 个才判方差）。
        decay_sharpe: {decay 值: sharpe}；以 decay=0（否则最小 decay）为基准比对最差值。
        yearly_corr: 逐年信号相关性序列；判相邻两年跳变。
        sharpe_full / sharpe_trimmed: 全样本 Sharpe 与去掉头尾 10% 后的 Sharpe。
        thresh: 覆盖 OVERFIT_THRESHOLDS。

    Returns:
        {"hits": {信号: 实测值}, "verdict": "REJECT"|"PASS", "n_signals": int,
         "thresholds": {...}}
    """
    t = dict(OVERFIT_THRESHOLDS)
    if thresh:
        t.update(thresh)
    hits: Dict[str, float] = {}

    # ① Sharpe 随 decay 断崖下跌
    if decay_sharpe:
        vals = {int(k): float(v) for k, v in decay_sharpe.items() if v is not None}
        if vals:
            base = vals.get(0)
            if base is None:
                base = vals[min(vals)]
            if base and base > 0:
                worst = min(vals.values())
                ratio = worst / base
                if ratio < t["decay_cliff_ratio"]:
                    hits["decay_cliff"] = round(ratio, 3)

    # ② 年份间 Sharpe 方差过大
    if yearly_sharpe and len(yearly_sharpe) >= 3:
        var = statistics.pvariance([float(x) for x in yearly_sharpe])
        if var > t["yearly_sharpe_var_max"]:
            hits["yearly_sharpe_var"] = round(var, 3)

    # ③ 去头尾 10% 后 Sharpe 腰斩
    if sharpe_full and sharpe_trimmed is not None:
        ratio = float(sharpe_trimmed) / float(sharpe_full)
        if ratio < t["tail_trim_halve_ratio"]:
            hits["tail_trim_halved"] = round(ratio, 3)

    # ④ 相邻两年相关性跳变（只看汇总 Sharpe 看不出）
    if yearly_corr and len(yearly_corr) >= 2:
        seq = [float(x) for x in yearly_corr]
        jump = max(abs(seq[i + 1] - seq[i]) for i in range(len(seq) - 1))
        if jump > t["yearly_corr_jump_max"]:
            hits["yearly_corr_jump"] = round(jump, 3)

    return {
        "hits": hits,
        "verdict": "REJECT" if hits else "PASS",
        "n_signals": len(hits),
        "thresholds": t,
    }


def iter_prune(alphas: Iterable[Dict], corr_fn, corr_threshold: float = 0.7,
               key: str = "sharpe"):
    """基于相关性的候选剪枝（HQ17963「Gold→GrandMaster」帖方法）。

    假设：高相关的 1 阶因子经同一次变换后仍高相关 → 只需测其中一个的变体。

    Args:
        alphas: 候选 dict 列表（含 `key` 指标）。
        corr_fn: (a, b) -> 相关系数。
        corr_threshold: 相关系数高于此值的候选被剪掉。

    Yields:
        剪枝后保留的候选（按 `key` 降序贪心选取）。
    """
    pool = sorted([a for a in alphas if isinstance(a, dict)],
                  key=lambda a: -(a.get(key) or float("-inf")))
    kept: list = []
    for cand in pool:
        if any(abs(corr_fn(cand, k)) > corr_threshold for k in kept):
            continue
        kept.append(cand)
        yield cand
