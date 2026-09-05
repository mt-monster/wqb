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


def _get_chain_executor():
    """延迟导入链式执行器."""
    import sys
    import os
    src_path = os.path.join(os.path.dirname(__file__), "..", "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    from wqb.workflow import execute_chain
    return execute_chain


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
    output_csv: Optional[str] = None,
    campaign_dir: Optional[str] = None,
    detached: bool = True,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """S3 批量回测跟踪（batch_track 节点快捷方式）.

    Args:
        region: 区域代码（如 KOR）
        wave: 波次号（如 36A）
        dataset: 数据集 ID
        concurrency: 并发数（默认 7，七槽填槽）
        max_rounds: 最大轮次
        output_csv: 输出 CSV 路径（默认自动生成）
        campaign_dir: 战役目录（默认自动解析）
        detached: 是否后台执行（默认 True，立即返回 task_id/log_path，避免 MCP 客户端超时；
                  False 为旧同步模式，subprocess.run 阻塞至完成或 1h 超时）
        dry_run: 是否干跑

    Returns:
        批量回测结果（detached=True 时含 task_id/stdout_log，供轮询）
    """
    execute, _ = _get_workflow_executor()
    result = execute("batch_track", {
        "region": region,
        "wave": wave,
        "dataset": dataset,
        "concurrency": concurrency,
        "max_rounds": max_rounds,
        "output_csv": output_csv,
        "campaign_dir": campaign_dir,
        "detached": detached,
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
        "tags": tags,
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
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Alpha 六步闸门判定（judge 节点快捷方式）——**只判定，不提交**。

    参考评审层，非提交判定权威。最终「是否可提交」以 `submit_verdict` 为准；
    提交动作走 `workflow_submit_alpha` 且必须有用户明确确认（ra-pipeline 步 8）。
    2026-09-05 移除了本工具的提交开关——它原先会绕过 submit_verdict、绕过
    robustness 必经闸、绕过用户确认直接提交。

    返回的 success 表示「判定是否跑完」；结论看 output.verdict
    （READY / REVIEW / BLOCK）。

    Args:
        alpha_id: Alpha ID
        trend_window_days: trend score 窗口天数
        llm_enabled: 是否启用 LLM 决策层
        dry_run: 是否干跑

    Returns:
        判定结果
    """
    execute, _ = _get_workflow_executor()
    result = execute("judge", {
        "alpha_id": alpha_id,
        "trend_window_days": trend_window_days,
        "llm_enabled": llm_enabled,
    }, dry_run=dry_run)
    return result.to_dict()


@mcp.tool()
def workflow_gem(
    region: str,
    dataset_id: str,
    delay: int,
    universe: str,
    data_category: Optional[str] = None,
    instrument_type: str = "EQUITY",
    data_type: str = "MATRIX",
    priors_file: Optional[str] = None,
    priors_from_db: bool = True,
    ideas_file: Optional[str] = None,
    detached: bool = True,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """GEM 表达式生成（gem 节点快捷方式）.

    2026-09-05 补齐：此前 MCP 层缺 data_type / instrument_type / priors_from_db，
    而 ra-pipeline 步 3 明写「步 4 必须传对 data_type」——传不进去只能退回
    workflow_execute("gem", ...)。现与 gem 节点签名一致。

    Args:
        region: 区域代码
        dataset_id: 数据集 ID
        delay: 延迟（0 或 1）
        universe: 宇宙（如 TOP3000）
        data_category: 数据类别（缺省时按平台 category 自动推断）
        instrument_type: 工具类型（默认 EQUITY）
        data_type: 数据类型 MATRIX / VECTOR——必须与 S1 get_datafields 确认的
            字段类型一致，传错会导致整批表达式类型不匹配
        priors_file: priors.json 路径（显式指定时优先于 DB 快照）
        priors_from_db: 从 DB ledger priors_snapshot_<region> 直读 priors
            （默认 True，与 SOP「DB 为单一事实源」对齐）
        ideas_file: ideas.md 路径（显式指定，覆盖 S1 ledger 自动注入）
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
        "instrument_type": instrument_type,
        "data_type": data_type,
        "priors_file": priors_file,
        "priors_from_db": priors_from_db,
        "ideas_file": ideas_file,
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
    calibrate: bool = False,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """S1-S6 战役阶段执行（campaign 节点快捷方式）.

    Args:
        region: 区域代码
        stage: 阶段（S0/S1/S2/S3/S4/S5/S6）
        dataset: 数据集 ID
        wave: 波次号
        subcommand: 子命令（assemble-priors/diversity-extract/ledger/registry/wave）
        extra_args: 额外参数
        calibrate: S0 专用——是否运行 calibrate 交互审批
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
        "calibrate": calibrate,
    }, dry_run=dry_run)
    return result.to_dict()


@mcp.tool()
def workflow_feature_engineering(
    region: str,
    dataset_id: str,
    delay: int,
    universe: str,
    data_category: Optional[str] = None,
    force_regen: bool = False,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """S1-S3 特征工程流程（feature_engineering 节点快捷方式）.

    Args:
        region: 区域代码
        dataset_id: 数据集 ID
        delay: 延迟（0 或 1）
        universe: 宇宙（如 TOP3000）
        data_category: 数据类别
        force_regen: 是否强制重新生成（忽略已有 ledger）
        dry_run: 是否干跑

    Returns:
        特征工程结果，含 s1_ledger_key 和 ideas_md_path
    """
    execute, _ = _get_workflow_executor()
    result = execute("feature_engineering", {
        "region": region,
        "dataset_id": dataset_id,
        "delay": delay,
        "universe": universe,
        "data_category": data_category,
        "force_regen": force_regen,
    }, dry_run=dry_run)
    return result.to_dict()


@mcp.tool()
def workflow_chain(
    chain: List[Dict[str, Any]],
    dry_run: bool = False,
    stop_on_failure: bool = True,
) -> Dict[str, Any]:
    """按顺序执行一串 workflow 节点（execute_chain 的 MCP 入口）.

    2026-09-05 新增：wqb.workflow.execute_chain 此前导出了却零调用方、也没有
    MCP 暴露 —— 九步流水线本身就是一条链，却只能一个节点一个节点手工调。

    典型用法（先干跑看命令，确认后再实跑）：

        workflow_chain(chain=[
            {"node": "campaign", "params": {"region": "KOR", "stage": "S0"}},
            {"node": "feature_engineering", "params": {...}},
            {"node": "gem", "params": {...}},
        ], dry_run=True)

    注意：链里不要放 confirm_submit=True 的 submit_alpha / superalpha ——
    提交必须有用户明确确认（ra-pipeline 步 8），不走自动链。

    Args:
        chain: [{"node": "<节点名>", "params": {...}}, ...]
        dry_run: 是否整链干跑（每个节点只构建计划/命令，不执行、不写库）
        stop_on_failure: 某节点失败时是否中止后续（默认 True）

    Returns:
        {"success": 全链是否成功, "results": [每个节点的 WorkflowResult dict],
         "executed": 实际执行节点数, "failed_at": 首个失败节点名或 None}
    """
    execute_chain = _get_chain_executor()
    results = execute_chain(chain, dry_run=dry_run, stop_on_failure=stop_on_failure)
    payload = [r.to_dict() for r in results]
    failed_at = next((r["node"] for r in payload if not r["success"]), None)
    return {
        "success": failed_at is None,
        "results": payload,
        "executed": len(payload),
        "requested": len(chain),
        "failed_at": failed_at,
        "dry_run": dry_run,
    }
