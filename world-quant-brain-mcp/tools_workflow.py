# -*- coding: utf-8 -*-
"""tools_workflow — Workflow 引擎 MCP 工具注册.

将 wqb.workflow 的 6 个节点暴露为 MCP 工具，供 Agent 直接调用。
"""

import json
import logging
from typing import Any, Dict, List, Optional

from mcp_core import mcp

logger = logging.getLogger("tools_workflow")


def _get_workflow_executor():
    """延迟导入 workflow 执行器（避免启动时循环依赖）."""
    import sys
    import os
    # 确保 src 在 path 中
    src_path = os.path.join(os.path.dirname(__file__), "..", "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    from wqb.workflow import execute, get_registry
    return execute, get_registry


@mcp.tool()
def workflow_list_nodes() -> Dict[str, Any]:
    """列出所有可用的 workflow 节点及其元数据.

    Returns:
        节点列表，含 name/description/category/phase/required_params
    """
    _, get_registry = _get_workflow_executor()
    registry = get_registry()
    nodes = registry.list_nodes()
    result = []
    for node in nodes:
        meta = registry.get_meta(node)
        result.append({
            "name": meta.name,
            "description": meta.description,
            "category": meta.category,
            "phase": meta.phase,
            "required_params": meta.required_params,
            "optional_params": meta.optional_params,
        })
    return {"nodes": result, "count": len(result)}


@mcp.tool()
def workflow_execute(
    node: str,
    params: Dict[str, Any],
    dry_run: bool = False,
) -> Dict[str, Any]:
    """执行指定 workflow 节点.

    Args:
        node: 节点名称（batch_track/submit_alpha/superalpha/judge/gem/campaign）
        params: 节点参数字典（按节点要求）
        dry_run: 是否干跑（不实际执行，仅验证参数与流程）

    Returns:
        执行结果，含 success/output/error/duration_sec
    """
    execute, _ = _get_workflow_executor()
    result = execute(node, params, dry_run=dry_run)
    return result.to_dict()


@mcp.tool()
def workflow_batch_track(
    region: str,
    wave: str,
    dataset: str,
    concurrency: int = 7,
    max_rounds: int = 3,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """S3 批量回测跟踪（batch_track 节点快捷方式）.

    Args:
        region: 区域代码（如 KOR）
        wave: 波次号（如 36A）
        dataset: 数据集 ID
        concurrency: 并发数（默认 7，七槽填槽）
        max_rounds: 最大轮次
        dry_run: 是否干跑

    Returns:
        批量回测结果
    """
    execute, _ = _get_workflow_executor()
    result = execute("batch_track", {
        "region": region,
        "wave": wave,
        "dataset": dataset,
        "concurrency": concurrency,
        "max_rounds": max_rounds,
    }, dry_run=dry_run)
    return result.to_dict()


@mcp.tool()
def workflow_submit_alpha(
    alpha_id: str,
    name: Optional[str] = None,
    color: str = "GREEN",
    tags: Optional[List[str]] = None,
    descriptions: Optional[str] = None,
    force: bool = False,
    confirm_submit: bool = False,
    verify_timeout: int = 180,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """提交 Alpha 到平台（submit_alpha 节点快捷方式）.

    Args:
        alpha_id: Alpha ID
        name: 名称（建议基于 prod correlation）
        color: 颜色标记
        tags: 标签列表
        descriptions: 描述文本（三段式）
        force: 是否跳过本地预检
        confirm_submit: 是否真正 POST submit（默认 False，仅预检+查状态，不提交）
        verify_timeout: 状态确认超时（秒）
        dry_run: 是否干跑

    Returns:
        提交结果
    """
    execute, _ = _get_workflow_executor()
    result = execute("submit_alpha", {
        "alpha_id": alpha_id,
        "name": name,
        "color": color,
        "tags": tags or [],
        "descriptions": descriptions,
        "force": force,
        "confirm_submit": confirm_submit,
        "verify_timeout": verify_timeout,
    }, dry_run=dry_run)
    return result.to_dict()


@mcp.tool()
def workflow_superalpha(
    region: str,
    components: List[str],
    selection: Optional[str] = None,
    combo: Optional[str] = None,
    neutralization: str = "SUBINDUSTRY",
    confirm_submit: bool = False,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """构建并提交 SuperAlpha（superalpha 节点快捷方式）.

    Args:
        region: 区域代码
        components: 组件 alpha ID 列表（≥10 个 ACTIVE REGULAR）
        selection: selection 表达式（默认自动生成）
        combo: combo 表达式（默认自动生成）
        neutralization: 中性化方式（默认 SUBINDUSTRY）
        confirm_submit: 是否真正提交（默认 False，仅建 simulation + 探针）
        dry_run: 是否干跑

    Returns:
        SuperAlpha 构建结果
    """
    execute, _ = _get_workflow_executor()
    result = execute("superalpha", {
        "region": region,
        "components": components,
        "selection": selection,
        "combo": combo,
        "neutralization": neutralization,
        "confirm_submit": confirm_submit,
    }, dry_run=dry_run)
    return result.to_dict()


@mcp.tool()
def workflow_judge(
    alpha_id: str,
    trend_window_days: int = 365,
    llm_enabled: bool = True,
    confirm_submit: bool = False,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Alpha 六步闸门判定（judge 节点快捷方式）.

    Args:
        alpha_id: Alpha ID
        trend_window_days: trend score 窗口天数
        llm_enabled: 是否启用 LLM 决策层
        confirm_submit: 是否确认提交
        dry_run: 是否干跑

    Returns:
        判定结果
    """
    execute, _ = _get_workflow_executor()
    result = execute("judge", {
        "alpha_id": alpha_id,
        "trend_window_days": trend_window_days,
        "llm_enabled": llm_enabled,
        "confirm_submit": confirm_submit,
    }, dry_run=dry_run)
    return result.to_dict()


@mcp.tool()
def workflow_gem(
    region: str,
    dataset_id: str,
    delay: int,
    universe: str,
    data_category: Optional[str] = None,
    priors_file: Optional[str] = None,
    detached: bool = True,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """GEM 表达式生成（gem 节点快捷方式）.

    Args:
        region: 区域代码
        dataset_id: 数据集 ID
        delay: 延迟（0 或 1）
        universe: 宇宙（如 TOP3000）
        data_category: 数据类别
        priors_file: priors.json 路径
        detached: 是否后台执行
        dry_run: 是否干跑

    Returns:
        GEM 生成结果
    """
    execute, _ = _get_workflow_executor()
    result = execute("gem", {
        "region": region,
        "dataset_id": dataset_id,
        "delay": delay,
        "universe": universe,
        "data_category": data_category,
        "priors_file": priors_file,
        "detached": detached,
    }, dry_run=dry_run)
    return result.to_dict()


@mcp.tool()
def workflow_campaign(
    region: str,
    stage: str,
    dataset: Optional[str] = None,
    wave: Optional[str] = None,
    subcommand: Optional[str] = None,
    extra_args: Optional[List[str]] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """S1-S6 战役阶段执行（campaign 节点快捷方式）.

    Args:
        region: 区域代码
        stage: 阶段（S0/S1/S2/S3/S4/S5/S6）
        dataset: 数据集 ID
        wave: 波次号
        subcommand: 子命令
        extra_args: 额外参数
        dry_run: 是否干跑

    Returns:
        战役阶段执行结果
    """
    execute, _ = _get_workflow_executor()
    result = execute("campaign", {
        "region": region,
        "stage": stage,
        "dataset": dataset,
        "wave": wave,
        "subcommand": subcommand,
        "extra_args": extra_args or [],
    }, dry_run=dry_run)
    return result.to_dict()
