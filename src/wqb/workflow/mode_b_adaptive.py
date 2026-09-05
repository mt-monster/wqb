# -*- coding: utf-8 -*-
"""Mode B 资格线自适应学习（方案 C，2026-09-04）.

从 registry_empirical 的 win/dead_end 历史学习本区域 Mode B 成功率 vs 起点 sharpe/fitness，
用 logistic 拟合"成功率 >= 30%"的阈值，S6 回写后自动更新 ledger_kv 的 mode_b_qualification。

样本不足（<5 波）时回落 thresholds.json 静态值。
"""
import json
import logging
import math
import os
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# 自适应学习参数
MIN_SAMPLES = 5  # 最少样本波数（不足则回落静态值）
TARGET_SUCCESS_RATE = 0.3  # 目标成功率（30%）
LEARNING_RATE = 0.1  # 阈值调整步长（指数平滑）


def learn_mode_b_threshold(
    store,
    region: str,
    lookback_waves: int = 20,
) -> Optional[Dict[str, float]]:
    """从 registry_empirical 学习 Mode B 资格线阈值.

    Args:
        store: CampaignStore 实例
        region: 区域代码
        lookback_waves: 回看波数（默认 20）

    Returns:
        {"sharpe_min": float, "fitness_min": float, "sample_count": int, "learned": True}
        或 None（样本不足）
    """
    if not store:
        return None

    # 1. 从 registry_empirical 拉本区域近 N 波的 win/dead_end 记录
    try:
        conn = store.connection
        cur = conn.cursor()
        # win 层
        cur.execute(
            "SELECT payload FROM registry_empirical "
            "WHERE region=? AND layer='win' ORDER BY id DESC LIMIT ?",
            (region, lookback_waves),
        )
        wins = [{"payload": row[0]} for row in cur.fetchall()]
        # dead_end 层
        cur.execute(
            "SELECT payload FROM registry_empirical "
            "WHERE region=? AND layer='dead_end' ORDER BY id DESC LIMIT ?",
            (region, lookback_waves),
        )
        dead_ends = [{"payload": row[0]} for row in cur.fetchall()]
    except Exception as e:
        logger.warning(f"Failed to load registry for {region}: {e}")
        return None

    # 2. 提取样本：(起点 sharpe, 起点 fitness, 是否成功)
    samples = _extract_samples(wins, dead_ends)
    if len(samples) < MIN_SAMPLES:
        logger.info(
            f"Insufficient samples for {region}: {len(samples)} < {MIN_SAMPLES}, "
            f"fallback to static threshold"
        )
        return None

    # 3. 拟合"成功率 >= 30%"的 sharpe/fitness 阈值
    sharpe_threshold = _fit_threshold(
        [(s[0], s[2]) for s in samples], target_rate=TARGET_SUCCESS_RATE
    )
    fitness_threshold = _fit_threshold(
        [(s[1], s[2]) for s in samples], target_rate=TARGET_SUCCESS_RATE
    )

    if sharpe_threshold is None or fitness_threshold is None:
        return None

    return {
        "sharpe_min": round(sharpe_threshold, 2),
        "fitness_min": round(fitness_threshold, 2),
        "sample_count": len(samples),
        "learned": True,
    }


def _extract_samples(
    wins: List[Dict[str, Any]],
    dead_ends: List[Dict[str, Any]],
) -> List[Tuple[float, float, bool]]:
    """从 win/dead_end 记录提取 (sharpe, fitness, success) 样本.

    win 记录：payload 含 sharpe/fitness 字段 → success=True
    dead_end 记录：payload 含 best_sharpe/best_fitness 字段 → success=False
    """
    samples = []

    for w in wins:
        payload = w.get("payload", {})
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except Exception:
                continue
        sharpe = payload.get("sharpe") or payload.get("best_sharpe")
        fitness = payload.get("fitness") or payload.get("best_fitness")
        if sharpe is not None and fitness is not None:
            samples.append((abs(float(sharpe)), float(fitness), True))

    for d in dead_ends:
        payload = d.get("payload", {})
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except Exception:
                continue
        sharpe = payload.get("best_sharpe") or payload.get("sharpe")
        fitness = payload.get("best_fitness") or payload.get("fitness")
        if sharpe is not None and fitness is not None:
            samples.append((abs(float(sharpe)), float(fitness), False))

    return samples


def _fit_threshold(
    samples: List[Tuple[float, bool]],
    target_rate: float = TARGET_SUCCESS_RATE,
) -> Optional[float]:
    """拟合"成功率 >= target_rate"的阈值（分位数法）.

    逻辑：找最大的阈值 T，使得 P(success | value >= T) >= target_rate。
    实现：按 value 降序排序，逐个考察每个候选阈值，记录满足条件的最大 T。
    """
    if not samples:
        return None

    # 按 value 降序排序
    sorted_samples = sorted(samples, key=lambda x: x[0], reverse=True)

    # 逐个考察每个候选阈值（从高到低），找满足成功率条件的最大 T
    for i in range(len(sorted_samples)):
        threshold = sorted_samples[i][0]
        # 子集 = value >= threshold 的所有样本
        subset = [s for s in sorted_samples if s[0] >= threshold]
        success_rate = sum(1 for s in subset if s[1]) / len(subset)
        if success_rate >= target_rate:
            return threshold  # 找到最大的满足条件的 T（降序遍历，首个即最大）

    return None  # 所有阈值都不满足（成功率全低于 target_rate）


def update_mode_b_qualification(
    store,
    region: str,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """S6 回写后自动更新 ledger_kv 的 mode_b_qualification（方案 C 入口）.

    Args:
        store: CampaignStore 实例
        region: 区域代码
        dry_run: 是否干跑（只计算不写入）

    Returns:
        {"updated": bool, "old": dict, "new": dict, "reason": str}
    """
    # 1. 学习新阈值
    learned = learn_mode_b_threshold(store, region)
    if not learned:
        return {
            "updated": False,
            "reason": f"样本不足（<{MIN_SAMPLES} 波），保持静态值",
        }

    # 2. 读旧值（ledger_kv > thresholds.json > 默认）
    old = _load_current_threshold(store, region)

    # 3. 指数平滑（避免单次波动剧烈调整）
    new_sharpe = old["sharpe_min"] * (1 - LEARNING_RATE) + learned["sharpe_min"] * LEARNING_RATE
    new_fitness = old["fitness_min"] * (1 - LEARNING_RATE) + learned["fitness_min"] * LEARNING_RATE
    new = {
        "sharpe_min": round(new_sharpe, 2),
        "fitness_min": round(new_fitness, 2),
        "learned_from": learned["sample_count"],
        "learned_at": datetime.now().isoformat(),
    }

    # 4. 写入 ledger_kv
    if not dry_run:
        try:
            store.upsert_ledger(region, "mode_b_qualification", new)
            logger.info(
                f"Updated mode_b_qualification for {region}: "
                f"{old} -> {new} (learned from {learned['sample_count']} samples)"
            )
        except Exception as e:
            logger.warning(f"Failed to update ledger: {e}")
            return {"updated": False, "reason": f"ledger write failed: {e}"}

    return {"updated": True, "old": old, "new": new, "reason": "learned from registry"}


def _load_current_threshold(store, region: str) -> Dict[str, float]:
    """读当前阈值（ledger_kv > thresholds.json > 默认）."""
    # 1. ledger_kv
    if store:
        try:
            cached = store.get_ledger(region, "mode_b_qualification")
            if cached and isinstance(cached, dict):
                sharpe_min = cached.get("sharpe_min")
                fitness_min = cached.get("fitness_min")
                if sharpe_min is not None and fitness_min is not None:
                    return {"sharpe_min": float(sharpe_min), "fitness_min": float(fitness_min)}
        except Exception:
            pass

    # 2. thresholds.json
    try:
        thresholds_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "..",
            "tracking", region, "config", "thresholds.json"
        )
        thresholds_path = os.path.abspath(thresholds_path)
        if os.path.exists(thresholds_path):
            with open(thresholds_path, "r", encoding="utf-8") as f:
                thresholds = json.load(f)
            mbq = thresholds.get("mode_b_qualification", {})
            if isinstance(mbq, dict):
                sharpe_min = mbq.get("sharpe_min")
                fitness_min = mbq.get("fitness_min")
                if sharpe_min is not None and fitness_min is not None:
                    return {"sharpe_min": float(sharpe_min), "fitness_min": float(fitness_min)}
    except Exception:
        pass

    # 3. 默认
    return {"sharpe_min": 1.25, "fitness_min": 0.8}


# 避免循环导入
from datetime import datetime
