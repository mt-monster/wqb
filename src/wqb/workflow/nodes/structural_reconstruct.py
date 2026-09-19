# -*- coding: utf-8 -*-
"""structural_reconstruct 节点：结构重构变体生成与效果追踪.

针对「修订信号 vs 短期反转」等结构性权衡问题，提供：
  1. 变体生成：基于四种策略生成合规重构表达式
  2. 预检集成：在 wave_gate 阶段检测 add(A,B) 模式并建议重构
  3. 效果追踪：记录变体回测结果，与原始表达式对比

合规约束（记忆 7c2651ad）：
  - 禁止 add(A,B) 混信号调参
  - 禁止权重网格扫描
  - 允许：换字段组合、换信号概念、换算子几何、换分组轴、单信号结构化

用法:
    # 生成变体
    result = execute("structural_reconstruct", {
        "action": "generate",
        "base_signal": "rank(anl45_est_revision)",
        "conflict_signal": "rank(ts_delta(close, 5))",
        "region": "DEU",
    })

    # 记录回测结果
    result = execute("structural_reconstruct", {
        "action": "record",
        "region": "DEU",
        "wave": 95,
        "variant_id": "geo_spread_rank",
        "original_expr": "add(rank(A), rank(B))",
        "variant_expr": "subtract(rank(A), rank(B))",
        "strategy": "geometric",
        "alpha_id": "abc123",
        "metrics": {"sharpe": 1.45, "fitness": 0.92},
    })

    # 生成对比报告
    result = execute("structural_reconstruct", {
        "action": "report",
        "region": "DEU",
        "wave": 95,
    })
"""

import json
import logging
from typing import Any, Dict, List, Optional

from ..mcp_check import require_mcp_tools
from .._common import (
    get_brain_client as _get_brain_client,
    persist_workflow_record,
    resolve_db_path,
    run_async as _run_async,
)
from ..structural_variants import (
    ReconstructionStrategy,
    StructuralVariantGenerator,
    detect_structural_conflict,
    generate_reconstruction_report,
)
from ..structural_variant_tracker import StructuralVariantTracker

logger = logging.getLogger(__name__)


@require_mcp_tools("structural_reconstruct")
def run(
    action: str,
    base_signal: Optional[str] = None,
    conflict_signal: Optional[str] = None,
    strategy: Optional[str] = None,
    region: Optional[str] = None,
    wave: Optional[int] = None,
    variant_id: Optional[str] = None,
    original_expr: Optional[str] = None,
    variant_expr: Optional[str] = None,
    alpha_id: Optional[str] = None,
    metrics: Optional[Dict[str, Any]] = None,
    status: Optional[str] = None,
    expression: Optional[str] = None,  # 用于 detect 模式
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """结构重构节点主入口.

    Args:
        action: 操作类型
            - "generate": 生成结构重构变体
            - "detect": 检测表达式是否存在结构性冲突
            - "record": 记录变体回测结果
            - "report": 生成对比报告
            - "stats": 获取策略统计
        base_signal: 基础信号表达式（generate 模式必填）
        conflict_signal: 冲突信号表达式（generate 模式必填）
        strategy: 重构策略过滤（可选）
        region: 区域代码
        wave: 波次号（record/report 模式必填）
        variant_id: 变体标识（record 模式必填）
        original_expr: 原始表达式（record 模式必填）
        variant_expr: 变体表达式（record 模式必填）
        alpha_id: 平台 alpha id（record 模式可选）
        metrics: 回测指标（record 模式可选）
        status: 状态（record 模式可选）
        expression: 待检测表达式（detect 模式必填）
        _context: 执行上下文

    Returns:
        操作结果字典
    """
    ctx = _context or {}
    store = ctx.get("store")

    # dry-run：只返回执行计划
    if ctx.get("dry_run"):
        return {
            "action": action,
            "success": True,
            "dry_run": True,
            "note": "dry-run：执行计划已构建，未执行实际操作",
            "plan": _build_plan(action, {
                "base_signal": base_signal,
                "conflict_signal": conflict_signal,
                "strategy": strategy,
                "region": region,
                "wave": wave,
                "expression": expression,
            }),
        }

    # 路由到具体操作
    if action == "generate":
        return _action_generate(
            base_signal=base_signal,
            conflict_signal=conflict_signal,
            strategy=strategy,
            region=region,
            store=store,
        )
    elif action == "detect":
        return _action_detect(expression=expression)
    elif action == "record":
        return _action_record(
            region=region,
            wave=wave,
            variant_id=variant_id,
            original_expr=original_expr,
            variant_expr=variant_expr,
            strategy=strategy,
            alpha_id=alpha_id,
            metrics=metrics,
            status=status,
            store=store,
        )
    elif action == "report":
        return _action_report(region=region, wave=wave, store=store)
    elif action == "stats":
        return _action_stats(region=region, store=store)
    else:
        return {
            "action": action,
            "success": False,
            "error": f"未知操作类型: {action}。支持: generate/detect/record/report/stats",
        }


def _build_plan(action: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """构建执行计划（dry-run 用）."""
    plans = {
        "generate": {
            "description": "生成结构重构变体",
            "steps": [
                "1. 解析基础信号与冲突信号",
                "2. 按策略生成变体（geometric/neutralization/temporal/orthogonal/conditional）",
                "3. 按优先级排序并推荐",
                "4. 生成 Markdown 报告",
            ],
        },
        "detect": {
            "description": "检测结构性冲突",
            "steps": [
                "1. 匹配 add(A,B) 模式",
                "2. 匹配加权 add 模式（函数式/中缀式）",
                "3. 返回冲突结构信息",
            ],
        },
        "record": {
            "description": "记录变体回测结果",
            "steps": [
                "1. 校验必填参数",
                "2. 写入 structural_variant_results 表",
                "3. 返回记录摘要",
            ],
        },
        "report": {
            "description": "生成对比报告",
            "steps": [
                "1. 读取波次所有变体结果",
                "2. 与原始表达式对比",
                "3. 计算改进幅度",
                "4. 生成 Markdown 报告",
            ],
        },
        "stats": {
            "description": "获取策略统计",
            "steps": [
                "1. 按策略分组统计",
                "2. 计算成功率与平均指标",
                "3. 返回统计结果",
            ],
        },
    }
    return plans.get(action, {"description": "未知操作", "steps": []})


def _action_generate(
    base_signal: Optional[str],
    conflict_signal: Optional[str],
    strategy: Optional[str],
    region: Optional[str],
    store,
) -> Dict[str, Any]:
    """生成结构重构变体."""
    if not base_signal or not conflict_signal:
        return {
            "action": "generate",
            "success": False,
            "error": "generate 模式需要 base_signal 和 conflict_signal 参数",
        }

    # 解析策略
    strat_enum = None
    if strategy:
        try:
            strat_enum = ReconstructionStrategy(strategy)
        except ValueError:
            return {
                "action": "generate",
                "success": False,
                "error": f"未知策略: {strategy}。支持: {[s.value for s in ReconstructionStrategy]}",
            }

    # 生成变体
    generator = StructuralVariantGenerator()
    result = generator.generate(
        base_signal=base_signal,
        conflict_signal=conflict_signal,
        strategy=strat_enum,
        region=region,
    )

    # 生成报告
    report_md = generate_reconstruction_report(result)

    # 持久化（可选）
    if store:
        persist_workflow_record(store, "structural_reconstruct", f"generate_{region or 'unknown'}", {
            "action": "generate",
            "base_signal": base_signal[:100],
            "conflict_signal": conflict_signal[:100],
            "variants_count": len(result.variants),
            "recommended": result.recommended.expression[:100] if result.recommended else None,
        })

    return {
        "action": "generate",
        "success": True,
        "base_expression": result.base_expression,
        "variants": [
            {
                "strategy": v.strategy.value,
                "expression": v.expression,
                "description": v.description,
                "expected_effect": v.expected_effect,
                "risk_note": v.risk_note,
                "priority": v.priority,
                "metadata": v.metadata,
            }
            for v in result.variants
        ],
        "recommended": {
            "expression": result.recommended.expression,
            "strategy": result.recommended.strategy.value,
            "description": result.recommended.description,
        } if result.recommended else None,
        "rationale": result.rationale,
        "report_markdown": report_md,
    }


def _action_detect(expression: Optional[str]) -> Dict[str, Any]:
    """检测结构性冲突."""
    if not expression:
        return {
            "action": "detect",
            "success": False,
            "error": "detect 模式需要 expression 参数",
        }

    conflict = detect_structural_conflict(expression)

    if conflict:
        return {
            "action": "detect",
            "success": True,
            "has_conflict": True,
            "conflict_info": conflict,
            "suggestion": "检测到 add(A,B) 结构性冲突模式，建议使用 structural_reconstruct generate 生成重构变体",
        }
    else:
        return {
            "action": "detect",
            "success": True,
            "has_conflict": False,
            "message": "未检测到结构性冲突模式",
        }


def _action_record(
    region: Optional[str],
    wave: Optional[int],
    variant_id: Optional[str],
    original_expr: Optional[str],
    variant_expr: Optional[str],
    strategy: Optional[str],
    alpha_id: Optional[str],
    metrics: Optional[Dict[str, Any]],
    status: Optional[str],
    store,
) -> Dict[str, Any]:
    """记录变体回测结果."""
    required = {
        "region": region,
        "wave": wave,
        "variant_id": variant_id,
        "original_expr": original_expr,
        "variant_expr": variant_expr,
        "strategy": strategy,
    }
    missing = [k for k, v in required.items() if v is None]
    if missing:
        return {
            "action": "record",
            "success": False,
            "error": f"record 模式缺少必填参数: {missing}",
        }

    # 初始化追踪器
    db_path = resolve_db_path() if store is None else None
    tracker = StructuralVariantTracker(store=store, db_path=db_path)

    # 记录结果
    result = tracker.record_variant_result(
        region=region,
        wave=wave,
        variant_id=variant_id,
        original_expr=original_expr,
        variant_expr=variant_expr,
        strategy=strategy,
        alpha_id=alpha_id,
        metrics=metrics,
        status=status or ("complete" if metrics else "pending"),
    )

    return {
        "action": "record",
        "success": True,
        "recorded": result,
    }


def _action_report(
    region: Optional[str],
    wave: Optional[int],
    store,
) -> Dict[str, Any]:
    """生成对比报告."""
    if not region or wave is None:
        return {
            "action": "report",
            "success": False,
            "error": "report 模式需要 region 和 wave 参数",
        }

    db_path = resolve_db_path() if store is None else None
    tracker = StructuralVariantTracker(store=store, db_path=db_path)

    # 生成对比
    comparison = tracker.compare_with_original(region, wave)
    report_md = tracker.generate_comparison_report(region, wave)

    return {
        "action": "report",
        "success": True,
        "region": region,
        "wave": wave,
        "verdict": comparison.verdict,
        "recommendation": comparison.recommendation,
        "improvement": comparison.improvement,
        "best_variant": {
            "variant_id": comparison.best_variant.variant_id,
            "strategy": comparison.best_variant.strategy,
            "expression": comparison.best_variant.variant_expression,
            "alpha_id": comparison.best_variant.alpha_id,
            "metrics": comparison.best_variant.metrics.to_dict(),
        } if comparison.best_variant else None,
        "variants_count": len(comparison.variants),
        "report_markdown": report_md,
    }


def _action_stats(
    region: Optional[str],
    store,
) -> Dict[str, Any]:
    """获取策略统计."""
    db_path = resolve_db_path() if store is None else None
    tracker = StructuralVariantTracker(store=store, db_path=db_path)

    stats = tracker.get_strategy_stats(region=region)

    return {
        "action": "stats",
        "success": True,
        "region": region,
        "strategy_stats": stats,
    }
