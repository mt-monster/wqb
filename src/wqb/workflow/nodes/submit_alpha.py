# -*- coding: utf-8 -*-
"""submit_alpha 节点：提交路由与状态确认.

替代 worldquant-submit-alpha 的 PowerShell 命令模板与 fallback 脚本。
"""

import logging
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def run(
    alpha_id: str,
    name: Optional[str] = None,
    color: str = "GREEN",
    tags: Optional[List[str]] = None,
    descriptions: Optional[str] = None,
    force: bool = False,
    verify_timeout: int = 180,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """执行 alpha 提交流程.

    Args:
        alpha_id: Alpha ID
        name: 名称（建议基于 prod correlation）
        color: 颜色标记
        tags: 标签列表
        descriptions: 描述文本（三段式）
        force: 是否跳过本地预检
        verify_timeout: 状态确认超时（秒）
        _context: 执行上下文

    Returns:
        执行结果字典
    """
    ctx = _context or {}
    store = ctx.get("store")

    # 默认标签
    if tags is None:
        tags = ["PowerPoolSelected"]

    # 构建结果
    result = {
        "alpha_id": alpha_id,
        "steps": [],
        "success": False,
    }

    # Step 1: 设置属性（通过 MCP）
    try:
        # 尝试使用 MCP 工具
        mcp_result = _call_mcp_set_properties(
            alpha_id=alpha_id,
            name=name,
            color=color,
            tags=tags,
            descriptions=descriptions,
        )
        result["steps"].append({
            "step": "set_properties",
            "success": True,
            "method": "mcp",
            "result": mcp_result,
        })
    except Exception as e:
        logger.warning(f"MCP set_properties failed, trying fallback: {e}")
        # Fallback: 记录需要手工执行
        result["steps"].append({
            "step": "set_properties",
            "success": False,
            "method": "fallback_required",
            "error": str(e),
            "fallback_cli": f"mcp__wq-brain-http__set_alpha_properties(alpha_id='{alpha_id}', ...)",
        })

    # Step 2: 提交（通过 MCP）
    try:
        submit_result = _call_mcp_submit(alpha_id=alpha_id, force=force)
        result["steps"].append({
            "step": "submit",
            "success": True,
            "method": "mcp",
            "result": submit_result,
        })
    except Exception as e:
        logger.warning(f"MCP submit failed: {e}")
        result["steps"].append({
            "step": "submit",
            "success": False,
            "method": "fallback_required",
            "error": str(e),
            "fallback_cli": f"mcp__wq-brain-http__submit_alpha(alpha_id='{alpha_id}', force={force})",
        })

    # Step 3: 状态确认
    verify_start = time.time()
    final_status = None

    while time.time() - verify_start < verify_timeout:
        try:
            details = _call_mcp_get_details(alpha_id)
            status = details.get("status")

            if status and status != "UNSUBMITTED":
                final_status = status
                result["steps"].append({
                    "step": "verify",
                    "success": True,
                    "status": status,
                    "date_submitted": details.get("dateSubmitted"),
                })
                break

            time.sleep(5)

        except Exception as e:
            logger.warning(f"Status check failed: {e}")
            time.sleep(5)

    if final_status is None:
        result["steps"].append({
            "step": "verify",
            "success": False,
            "error": f"Timeout after {verify_timeout}s, status still UNSUBMITTED",
        })
    else:
        result["success"] = final_status in ("ACTIVE", "SUBMITTED")
        result["final_status"] = final_status

    # 保存到 DB
    if store:
        try:
            store.upsert_ledger("WORKFLOW", f"submit_{alpha_id}", {
                "submitted_at": datetime.now().isoformat(),
                "final_status": final_status,
                "steps": result["steps"],
            })
        except Exception as e:
            logger.warning(f"Failed to save submit record: {e}")

    return result


def _call_mcp_set_properties(
    alpha_id: str,
    name: Optional[str],
    color: str,
    tags: List[str],
    descriptions: Optional[str],
) -> Dict[str, Any]:
    """调用 MCP set_alpha_properties.

    注意：此函数在 Agent 会话中由 MCP 工具直接调用，
    此处为模拟实现，实际执行时由 executor 替换为真实 MCP 调用。
    """
    # 实际实现应通过 MCP 协议调用
    # 这里返回模拟结果
    return {
        "alpha_id": alpha_id,
        "name": name,
        "color": color,
        "tags": tags,
        "descriptions_set": descriptions is not None,
    }


def _call_mcp_submit(alpha_id: str, force: bool) -> Dict[str, Any]:
    """调用 MCP submit_alpha."""
    return {
        "alpha_id": alpha_id,
        "force": force,
        "submitted": True,
    }


def _call_mcp_get_details(alpha_id: str) -> Dict[str, Any]:
    """调用 MCP get_alpha_details."""
    return {
        "alpha_id": alpha_id,
        "status": "ACTIVE",  # 模拟
        "dateSubmitted": datetime.now().isoformat(),
    }
