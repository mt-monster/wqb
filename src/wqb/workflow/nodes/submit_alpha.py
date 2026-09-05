# -*- coding: utf-8 -*-
"""submit_alpha 节点：提交路由与状态确认.

真实调用 brain_client（submit_alpha / set_alpha_properties / get_alpha_details），
替代 worldquant-submit-alpha 的 PowerShell 命令模板。

职责边界（2026-08-31 修复）：
  - 旧实现三个 `_call_mcp_*` 全部返回硬编码模拟值，会虚报"提交成功"。
  - 现改为真实调用 brain_client 单例；凭据解析与 MCP 服务一致。
  - 提交是敏感决策：默认仅做预检 + 状态查询，只有 confirm_submit=True
    才真正 POST submit（与"judge READY 后停等确认"纪律一致）。
"""
from __future__ import annotations

import logging
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from .._common import (
    get_brain_client as _get_brain_client,
    persist_workflow_record,
    run_async as _run_async,
)

logger = logging.getLogger(__name__)

_POLL_INTERVAL_SEC = 5


def _client_ok():
    """零网络地确认 brain_client 可导入（dry-run 用）。

    注意：只反映「当前解释器」能否导入，节点真实运行在 MCP venv 里；
    这里失败通常是干跑用的解释器缺依赖，属提示而非阻断。
    """
    try:
        _get_brain_client()
        return True, None
    except Exception as e:  # pragma: no cover - 环境相关
        return False, str(e)


def run(
    alpha_id: str,
    name: Optional[str] = None,
    color: str = "GREEN",
    tags: Optional[List[str]] = None,
    descriptions: Optional[str] = None,
    force: bool = False,
    confirm_submit: bool = False,
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
        force: 是否跳过本地预检（仅当 confirm_submit=True 时有意义）
        confirm_submit: 是否真正 POST submit（默认 False，只做预检+状态查询）
        verify_timeout: 提交后状态确认超时（秒）
        _context: 执行上下文

    Returns:
        执行结果字典（含预检/提交/状态确认各步明细）
    """
    ctx = _context or {}
    store = ctx.get("store")
    if tags is None:
        tags = ["PowerPoolSelected"]

    # dry-run：构建到提交流程计划即停，不触碰 network / 不写库
    # （2026-09-01 缺陷 A 修复：此前 dry_run 仍真实调用 get_alpha_details 等）。
    if ctx.get("dry_run"):
        _dry_client_ok, _dry_client_err = _client_ok()
        return {
            "alpha_id": alpha_id,
            "success": True,
            "dry_run": True,
            "submitted": False,
            "note": "dry-run：请求计划已构建，未调用平台",
            "steps": [{
                "step": "resolve_client",
                "success": _dry_client_ok,
                "warning": _dry_client_err,
            }],
            "plan": {
                "alpha_id": alpha_id,
                "name": name,
                "color": color,
                "tags": tags,
                "confirm_submit": confirm_submit,
                "force": force,
                "verify_timeout": verify_timeout,
                "calls": (
                    ["get_alpha_details(alpha_id)", "pre_submit_check(alpha_id)"]
                    + ([
                        "set_alpha_properties(alpha_id, name/color/tags/descriptions)",
                        "POST /alphas/{id}/submit",
                        f"poll get_alpha_details until OS/ACTIVE (<= {verify_timeout}s)",
                    ] if confirm_submit else [])
                ),
                "note": (
                    "confirm_submit=False：仅预检与查状态，不会 POST submit"
                    if not confirm_submit else
                    "confirm_submit=True：会真实提交——必须已有用户明确确认"
                ),
            },
        }

    result: Dict[str, Any] = {
        "alpha_id": alpha_id,
        "steps": [],
        "success": False,
        "submitted": False,
    }

    client = _get_brain_client()

    # Step 1: 预检（get_alpha_details + pre_submit_check）
    precheck = _run_async(client.get_alpha_details(alpha_id))
    check = _run_precheck(client, precheck)
    result["steps"].append(check)

    if check.get("blocked") and not force:
        result["reason"] = "pre_submit_check blocked"
        result["blocked"] = True
        return _finalize(result, store, alpha_id)

    # Step 2: 设置属性（仅在实际提交前做，避免空改）
    if confirm_submit:
        props = _run_async(client.set_alpha_properties(
            alpha_id, name=name, color=color, tags=tags, descriptions=descriptions))
        result["steps"].append({
            "step": "set_properties",
            "success": not isinstance(props, dict) or not props.get("__error__"),
            "result": props,
        })
    else:
        result["steps"].append({
            "step": "set_properties",
            "success": True,
            "skipped": True,
            "note": "confirm_submit=False，跳过属性设置",
        })

    # Step 3: 提交（敏感决策，需 confirm_submit=True）
    if confirm_submit:
        submit = _run_async(client.submit_alpha(alpha_id))
        result["steps"].append({
            "step": "submit",
            "success": bool(isinstance(submit, dict) and submit.get("success")),
            "result": submit,
        })
        result["submitted"] = bool(isinstance(submit, dict) and submit.get("success"))
    else:
        result["steps"].append({
            "step": "submit",
            "success": True,
            "skipped": True,
            "note": "confirm_submit=False，未真正提交（仅预检）",
        })
        # 未提交时：返回当前状态即结束
        status = _current_status(client, alpha_id)
        result["final_status"] = status
        result["success"] = True
        return _finalize(result, store, alpha_id)

    # Step 4: 提交后状态确认
    final_status = _poll_status(client, alpha_id, verify_timeout)
    result["steps"].append({
        "step": "verify",
        "success": final_status is not None,
        "status": final_status,
    })
    result["final_status"] = final_status
    result["success"] = final_status in ("ACTIVE", "SUBMITTED")

    return _finalize(result, store, alpha_id)


def _run_precheck(client, details: Dict[str, Any]) -> Dict[str, Any]:
    """包装 pre_submit_check（本地启发式），失败不抛异常。"""
    try:
        cr = client.pre_submit_check(details)
        return {
            "step": "pre_submit_check",
            "success": True,
            "passed": bool(cr.get("passed")),
            "blocked": not bool(cr.get("passed")),
            "check_result": cr,
        }
    except Exception as e:
        logger.warning(f"pre_submit_check failed: {e}")
        return {"step": "pre_submit_check", "success": False, "error": str(e),
                "blocked": False, "check_result": None}


def _current_status(client, alpha_id: str) -> Optional[str]:
    """查询当前 alpha 状态（不轮询）。"""
    details = _run_async(client.get_alpha_details(alpha_id))
    if isinstance(details, dict) and not details.get("__error__"):
        return details.get("status")
    return None


def _poll_status(client, alpha_id: str, timeout: int) -> Optional[str]:
    """轮询 alpha 状态直到脱离 UNSUBMITTED 或超时。"""
    deadline = time.time() + timeout
    while time.time() < deadline:
        status = _current_status(client, alpha_id)
        if status and status != "UNSUBMITTED":
            return status
        time.sleep(_POLL_INTERVAL_SEC)
    return None


def _finalize(result: Dict[str, Any], store, alpha_id: str) -> Dict[str, Any]:
    """保存提交记录到台账并返回（容错与告警由 persist_workflow_record 承担）。"""
    persist_workflow_record(store, "submit", alpha_id, {
        "submitted_at": datetime.now().isoformat(),
        "submitted": result.get("submitted", False),
        "final_status": result.get("final_status"),
        "steps": result.get("steps"),
    })
    return result
