# -*- coding: utf-8 -*-
"""MCP 工具检查模块：确保关键节点优先使用 MCP 工具而非手写脚本.

规约来源：AGENTS.md §5 层 0 — 结构化数据读写首选 wqb-db MCP 工具。
"""

import functools
import logging
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)

# 关键 MCP 工具清单（按用途分类）
MCP_TOOLS = {
    "db_read": [
        "get_wave_result",
        "get_ledger_key",
        "list_expressions",
        "get_field_catalog",
        "list_wave_results",
        "get_latest_wave",
        "get_region_config",
        "get_dead_ends",
        "get_campaigns",
        "get_cross_region_lessons",
        "get_submit_ready",
        "get_dead_datasets",
        "get_alpha_by_id",
        "list_alphas_by_wave",
        "search_alphas_by_sharpe",
        "get_campaign_summary",
        "get_region_overview",
    ],
    "db_write": [
        "upsert_ledger_key",
        "upsert_wave_result",
        "upsert_registry_empirical",
        "upsert_expressions",
        "upsert_field_catalog",
        "upsert_backtest_rows",
        "upsert_gate_result",
    ],
    "brain_api": [
        "get_alpha_details",
        "get_alpha_pnl",
        "get_user_alphas",
        "get_alpha_yearly_stats",
        "check_correlation",
        "check_self_correlation",
        "compute_mutual_correlation",
        "create_simulation",
        "create_multi_simulation",
        "batch_create_simulations",
        "submit_alpha",
        "get_datasets",
        "get_datafields",
        "get_operators",
        "validate_expressions",
    ],
    "workflow": [
        "workflow_list_nodes",
        "workflow_execute",
        "workflow_batch_track",
        "workflow_submit_alpha",
        "workflow_superalpha",
        "workflow_judge",
        "workflow_gem",
        "workflow_campaign",
    ],
}

# 节点执行前必须检查的 MCP 工具映射
NODE_MCP_REQUIREMENTS = {
    "batch_track": {
        "required": ["list_expressions", "upsert_backtest_rows"],
        "recommended": ["get_wave_result", "upsert_wave_result"],
        "description": "批量回测跟踪：从 DB 读表达式，结果写回 DB",
    },
    "gem": {
        "required": ["upsert_expressions"],
        "recommended": ["get_ledger_key", "upsert_ledger_key"],
        "description": "GEM 表达式生成：结果写 DB，ledger 追踪",
    },
    "campaign": {
        "required": ["upsert_wave_result", "upsert_gate_result"],
        "recommended": ["get_campaign_summary", "get_region_config"],
        "description": "战役执行：波次结果与闸门状态入库",
    },
    "judge": {
        "required": ["get_alpha_details"],
        "recommended": ["check_correlation", "check_self_correlation"],
        "description": "Alpha 评审：拉取平台指标与相关性",
    },
    "feature_engineering": {
        "required": ["upsert_ledger_key"],
        "recommended": ["get_field_catalog", "upsert_field_catalog"],
        "description": "特征工程：S1-S3 结果写 ledger",
    },
}


def check_mcp_tools(node_name: str) -> Dict[str, Any]:
    """检查节点所需的 MCP 工具是否可用.

    Args:
        node_name: 节点名称

    Returns:
        检查结果字典，包含 available/missing/recommendations
    """
    requirements = NODE_MCP_REQUIREMENTS.get(node_name, {})
    required = requirements.get("required", [])
    recommended = requirements.get("recommended", [])

    # 这里不实际调用 MCP，而是返回检查清单
    # 实际可用性由 MCP 客户端在调用时验证
    return {
        "node": node_name,
        "required_tools": required,
        "recommended_tools": recommended,
        "description": requirements.get("description", ""),
        "all_tools": required + recommended,
        "check_passed": True,  # 静态检查通过，运行时验证
    }


def require_mcp_tools(node_name: str):
    """装饰器：标记节点需要 MCP 工具检查.

    在节点执行前打印 MCP 工具清单，提醒优先使用 MCP 而非手写脚本。

    Usage:
        @require_mcp_tools("batch_track")
        def run(...):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            check_result = check_mcp_tools(node_name)
            logger.info(
                f"[MCP Check] {node_name}: "
                f"required={check_result['required_tools']}, "
                f"recommended={check_result['recommended_tools']}"
            )
            # 将 MCP 检查结果注入上下文
            if "_context" in kwargs and kwargs["_context"] is not None:
                kwargs["_context"]["mcp_check"] = check_result
            elif "_context" not in kwargs:
                kwargs["_context"] = {"mcp_check": check_result}
            return func(*args, **kwargs)
        return wrapper
    return decorator


def get_mcp_tool_for_task(task_type: str) -> List[str]:
    """获取特定任务类型推荐的 MCP 工具.

    Args:
        task_type: 任务类型（db_read/db_write/brain_api/workflow）

    Returns:
        推荐的 MCP 工具列表
    """
    return MCP_TOOLS.get(task_type, [])


def format_mcp_reminder(node_name: str) -> str:
    """格式化 MCP 工具提醒消息.

    Args:
        node_name: 节点名称

    Returns:
        格式化的提醒消息
    """
    check = check_mcp_tools(node_name)
    lines = [
        f"=== MCP 工具提醒: {node_name} ===",
        f"描述: {check['description']}",
        f"必需工具: {', '.join(check['required_tools']) or '无'}",
        f"推荐工具: {', '.join(check['recommended_tools']) or '无'}",
        "",
        "规约提醒（AGENTS.md §5 层 0）:",
        "  - 结构化数据读写首选 wqb-db MCP 工具",
        "  - 禁止手写 requests 脚本调用平台 API",
        "  - 网络工具统一走 BrainApiClient（自带 429 退避）",
        "=" * 40,
    ]
    return "\n".join(lines)
