# -*- coding: utf-8 -*-
"""field_understanding 节点：自动化字段理解流程（S1 增强）.

自动化字段理解流程：
1. 分析字段特征（覆盖率、非零值、更新频率、取值范围、中心趋势、分布形态）
2. 生成字段理解报告
3. 自动分类字段（主信号/辅助信号/group/bucket）
4. 识别高价值字段
"""

import json
import logging
import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional

from .._common import (
    REPO_ROOT,
    resolve_campaign_dir,
    resolve_db_path,
    resolve_tools_dir,
    wq_py,
)

logger = logging.getLogger(__name__)


def run(
    region: str,
    dataset: str,
    delay: int = 1,
    auto_classify: bool = True,
    identify_high_value: bool = True,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """执行自动化字段理解.

    Args:
        region: 区域代码
        dataset: 数据集 ID
        delay: 延迟（默认 1）
        auto_classify: 是否自动分类字段（默认 True）
        identify_high_value: 是否识别高价值字段（默认 True）
        _context: 执行上下文

    Returns:
        执行结果字典
    """
    ctx = _context or {}
    result = {
        "region": region,
        "dataset": dataset,
        "delay": delay,
        "success": False,
        "steps": [],
    }

    # 步骤 1：分析字段特征
    result["steps"].append({
        "step": "analyze_field_features",
        "success": True,
        "description": "分析字段覆盖率、非零值、更新频率、取值范围、中心趋势、分布形态",
    })

    # 步骤 2：生成字段理解报告
    result["steps"].append({
        "step": "generate_understanding_report",
        "success": True,
        "description": "生成字段理解报告",
    })

    # 步骤 3：自动分类字段
    if auto_classify:
        result["steps"].append({
            "step": "auto_classify_fields",
            "success": True,
            "description": "自动分类字段为主信号/辅助信号/group/bucket",
        })

    # 步骤 4：识别高价值字段
    if identify_high_value:
        result["steps"].append({
            "step": "identify_high_value_fields",
            "success": True,
            "description": "识别高价值字段",
        })

    # 如果是 dry-run，到此为止
    if ctx.get("dry_run"):
        result["success"] = True
        result["dry_run"] = True
        result["note"] = "dry-run：字段理解流程已构建，未执行"
        return result

    # 执行字段理解
    try:
        # 从 DB 读取字段目录
        db_path = resolve_db_path()
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        # 查询字段目录
        c.execute(
            "SELECT * FROM field_catalog WHERE region=? AND dataset=?",
            (region, dataset),
        )
        catalog_row = c.fetchone()

        if not catalog_row:
            result["error"] = f"Field catalog not found: {region}/{dataset}"
            conn.close()
            return result

        catalog = json.loads(catalog_row["catalog"])
        fields = catalog.get("fields", [])

        # 分析字段特征
        field_features = []
        for field in fields:
            features = _analyze_field_features(field)
            field_features.append(features)

        # 自动分类字段
        if auto_classify:
            field_features = _auto_classify_fields(field_features)

        # 识别高价值字段
        if identify_high_value:
            field_features = _identify_high_value_fields(field_features)

        # 生成字段理解报告
        report = _generate_understanding_report(field_features)

        # 写回 DB
        c.execute(
            """INSERT OR REPLACE INTO field_understanding
               (region, dataset, delay, report, created_at)
               VALUES (?,?,?,?,?)""",
            (region, dataset, delay, json.dumps(report, ensure_ascii=False),
             datetime.now().isoformat(timespec="seconds")),
        )
        conn.commit()
        conn.close()

        result["success"] = True
        result["field_count"] = len(fields)
        result["report"] = report
        result["message"] = f"Field understanding completed: {len(fields)} fields analyzed"

    except Exception as e:
        result["error"] = f"Field understanding failed: {e}"
        logger.exception("Field understanding failed")

    return result


def _analyze_field_features(field: Dict[str, Any]) -> Dict[str, Any]:
    """分析字段特征."""
    return {
        "field_id": field.get("id"),
        "field_name": field.get("name"),
        "coverage": field.get("coverage", 0.0),
        "non_zero_ratio": field.get("non_zero_ratio", 0.0),
        "update_frequency": field.get("update_frequency", "unknown"),
        "value_range": field.get("value_range", {}),
        "central_tendency": field.get("central_tendency", {}),
        "distribution_shape": field.get("distribution_shape", "unknown"),
        "users": field.get("users", 0),
        "type": field.get("type", "unknown"),
    }


def _auto_classify_fields(field_features: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """自动分类字段."""
    for features in field_features:
        # 根据字段特征自动分类
        field_name = features.get("field_name", "").lower()
        field_type = features.get("type", "").lower()
        users = features.get("users", 0)

        # 分类逻辑
        if "group" in field_name or "sector" in field_name or "industry" in field_name:
            features["category"] = "group"
        elif "bucket" in field_name or "quantile" in field_name:
            features["category"] = "bucket"
        elif users >= 50:
            features["category"] = "main_signal"  # 高使用率字段作为主信号
        elif users >= 10:
            features["category"] = "auxiliary_signal"  # 中使用率字段作为辅助信号
        else:
            features["category"] = "exploration"  # 低使用率字段作为探索信号

    return field_features


def _identify_high_value_fields(field_features: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """识别高价值字段."""
    for features in field_features:
        # 高价值字段判定逻辑
        coverage = features.get("coverage", 0.0)
        non_zero_ratio = features.get("non_zero_ratio", 0.0)
        users = features.get("users", 0)

        # 高价值字段：覆盖率高、非零值比例高、用户使用率低（避免高 prod_corr）
        is_high_value = (
            coverage >= 0.8 and
            non_zero_ratio >= 0.5 and
            users <= 9  # 用户使用率低，prod_corr 低
        )

        features["is_high_value"] = is_high_value
        features["value_score"] = _calculate_value_score(features)

    return field_features


def _calculate_value_score(features: Dict[str, Any]) -> float:
    """计算字段价值得分."""
    coverage = features.get("coverage", 0.0)
    non_zero_ratio = features.get("non_zero_ratio", 0.0)
    users = features.get("users", 0)

    # 价值得分 = 覆盖率 * 0.4 + 非零值比例 * 0.3 + (1 - 用户使用率/100) * 0.3
    user_score = max(0, 1 - users / 100)
    value_score = coverage * 0.4 + non_zero_ratio * 0.3 + user_score * 0.3

    return round(value_score, 4)


def _generate_understanding_report(field_features: List[Dict[str, Any]]) -> Dict[str, Any]:
    """生成字段理解报告."""
    total_fields = len(field_features)
    high_value_fields = [f for f in field_features if f.get("is_high_value", False)]

    # 按分类统计
    category_stats = {}
    for features in field_features:
        category = features.get("category", "unknown")
        category_stats[category] = category_stats.get(category, 0) + 1

    # 按价值得分排序
    sorted_fields = sorted(
        field_features,
        key=lambda f: f.get("value_score", 0),
        reverse=True,
    )

    return {
        "total_fields": total_fields,
        "high_value_fields": len(high_value_fields),
        "category_stats": category_stats,
        "top_fields": sorted_fields[:20],  # 前 20 个高价值字段
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }
