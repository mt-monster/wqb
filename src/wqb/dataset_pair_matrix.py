# -*- coding: utf-8 -*-
"""数据集对矩阵分析（2026-10-01 新增；2026-10-02 从 tools/ 迁入 src/wqb/）。

基于论坛文章《从一张丑表到一个 PROD=0 的提交：flag 减杠杆的完整过程》的核心洞察：
- 数据集对独立性 > 字段使用频率
- 数据集对矩阵是挖掘地图（找空格进行挖掘）

功能：
1. 分析数据集对矩阵（数据集×数据集的提交历史）
2. 找出空白格子（未提交过的数据集对）
3. 推荐挖掘的数据集对（按金字塔点亮价值排序）

注：本模块位于 src/wqb/（规范核心包），仅向下依赖 wqb.db_conn，不反向依赖 tools/，
满足「依赖只允许向下」约定。
"""
from __future__ import annotations

import json
import re
import sqlite3
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import sys as _sys, os as _os
_sys.path.insert(0, str(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..")))
from wqb.db_conn import connect as db_connect  # noqa: E402  规范工厂（禁裸 sqlite3.connect）

# 数据库路径（与 wqb.db 同库）；测试可 monkeypatch 本常量指向临时库
DB_PATH = Path(__file__).resolve().parents[2] / "data" / "wqb.db"


def _conn() -> sqlite3.Connection:
    """获取数据库连接（row_factory=Row）——走规范工厂统一 PRAGMA。"""
    return db_connect(str(DB_PATH), row_factory=sqlite3.Row)


def _extract_dataset_from_expression(expr: str) -> Optional[str]:
    """从表达式中提取数据集 ID（如 anl4_capex_flag → anl4）。"""
    if not expr:
        return None
    # 匹配数据集前缀（如 anl4_ / fnd6_ / pv1_ / model10_）
    # 注意：数据集前缀可能不带下划线（如 anl4_capex_flag 中的 anl4）
    m = re.search(r"\b(anl\d+|fnd\d+|pv\d+|model\d+|news\d+|insider\d+|shortinterest\d+|risk\d+|option\d+)(?:_|\b)", expr)
    return m.group(1) if m else None


def _extract_dataset_pairs(expr: str) -> List[Tuple[str, str]]:
    """从表达式中提取数据集对（如 rank(anl4_capex_flag) - rank(assets/liabilities_curr) → [(anl4, fundamental6)]）。

    注意：assets/liabilities_curr 是 fundamental6 的字段，但表达式中没有 fundamental6 前缀。
    这里简化处理：只提取表达式中明确出现的数据集前缀。
    """
    if not expr:
        return []
    # 提取所有数据集前缀
    datasets = set()
    for m in re.finditer(r"\b(anl\d+|fnd\d+|pv\d+|model\d+|news\d+|insider\d+|shortinterest\d+|risk\d+|option\d+)(?:_|\b)", expr):
        datasets.add(m.group(1))
    # 生成数据集对（笛卡尔积，去重）
    datasets = sorted(datasets)
    pairs = []
    for i, ds_a in enumerate(datasets):
        for ds_b in datasets[i+1:]:
            pairs.append((ds_a, ds_b))
    return pairs


def analyze_dataset_pair_matrix(region: str) -> Dict[str, Any]:
    """分析数据集对矩阵（数据集×数据集的提交历史）。

    Args:
        region: 区域（如 KOR/USA/EUR）

    Returns:
        {
            "matrix": {dataset_a: {dataset_b: count}},  # 数据集对矩阵
            "empty_cells": [(dataset_a, dataset_b), ...],  # 空白格子列表
            "recommendations": [  # 推荐挖掘的数据集对
                {
                    "dataset_a": "analyst4",
                    "dataset_b": "fundamental6",
                    "reason": "金字塔点亮价值高（analyst ×1.2 + fundamental ×1.1）",
                    "priority": "high",
                },
                ...
            ],
            "total_datasets": 10,  # 总数据集数
            "total_pairs": 45,  # 总数据集对数
            "filled_pairs": 12,  # 已填充数据集对数
            "empty_pairs": 33,  # 空白数据集对数
        }
    """
    conn = _conn()
    c = conn.cursor()

    # 1. 从 backtest_results 表读取所有历史提交
    c.execute("""
        SELECT DISTINCT code FROM backtest_results WHERE region=? AND code IS NOT NULL
    """, (region,))
    expressions = [row[0] for row in c.fetchall()]

    # 2. 提取每个表达式的数据集对
    pair_counts = defaultdict(int)
    all_datasets = set()
    for expr in expressions:
        pairs = _extract_dataset_pairs(expr)
        for ds_a, ds_b in pairs:
            pair_counts[(ds_a, ds_b)] += 1
            all_datasets.add(ds_a)
            all_datasets.add(ds_b)

    # 3. 构建数据集对矩阵
    matrix = defaultdict(dict)
    for (ds_a, ds_b), count in pair_counts.items():
        matrix[ds_a][ds_b] = count
        matrix[ds_b][ds_a] = count  # 对称矩阵

    # 4. 找出空白格子（未提交过的数据集对）
    all_datasets = sorted(all_datasets)
    empty_cells = []
    for i, ds_a in enumerate(all_datasets):
        for ds_b in all_datasets[i+1:]:
            if (ds_a, ds_b) not in pair_counts and (ds_b, ds_a) not in pair_counts:
                empty_cells.append((ds_a, ds_b))

    # 5. 推荐挖掘的数据集对（按金字塔点亮价值排序）
    # 金字塔点亮价值：analyst ×1.2 + fundamental ×1.1（文章里的经验）
    pyramid_values = {
        "analyst": 1.2,
        "fundamental": 1.1,
        "model": 1.0,
        "news": 1.0,
        "pv": 1.0,
        "insider": 1.0,
        "shortinterest": 1.0,
        "risk": 1.0,
        "option": 1.0,
    }

    recommendations = []
    for ds_a, ds_b in empty_cells:
        # 计算金字塔点亮价值
        value_a = pyramid_values.get(ds_a.rstrip("0123456789"), 1.0)
        value_b = pyramid_values.get(ds_b.rstrip("0123456789"), 1.0)
        total_value = value_a + value_b

        # 推荐优先级
        if total_value >= 2.2:
            priority = "high"
        elif total_value >= 2.0:
            priority = "medium"
        else:
            priority = "low"

        recommendations.append({
            "dataset_a": ds_a,
            "dataset_b": ds_b,
            "reason": f"金字塔点亮价值高（{ds_a.rstrip('0123456789')} ×{value_a} + {ds_b.rstrip('0123456789')} ×{value_b}）",
            "priority": priority,
            "pyramid_value": total_value,
        })

    # 按金字塔点亮价值排序
    recommendations.sort(key=lambda x: x["pyramid_value"], reverse=True)

    conn.close()

    return {
        "matrix": dict(matrix),
        "empty_cells": empty_cells,
        "recommendations": recommendations,
        "total_datasets": len(all_datasets),
        "total_pairs": len(all_datasets) * (len(all_datasets) - 1) // 2,
        "filled_pairs": len(pair_counts),
        "empty_pairs": len(empty_cells),
    }


def get_dataset_pair_recommendations(
    region: str,
    top_n: int = 10,
    priority: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """获取推荐挖掘的数据集对（按金字塔点亮价值排序）。

    Args:
        region: 区域
        top_n: 返回数量上限
        priority: 优先级过滤（high/medium/low，None=全部）

    Returns:
        推荐挖掘的数据集对列表
    """
    result = analyze_dataset_pair_matrix(region)
    recommendations = result["recommendations"]

    if priority:
        recommendations = [r for r in recommendations if r["priority"] == priority]

    return recommendations[:top_n]
