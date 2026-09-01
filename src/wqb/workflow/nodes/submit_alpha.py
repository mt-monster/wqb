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

import asyncio
import logging
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_POLL_INTERVAL_SEC = 5


def _get_brain_client():
    """延迟导入 brain_client 单例（避免循环依赖与启动开销）。"""
    import sys
    import os
    mcp_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..",
                           "world-quant-brain-mcp")
    mcp_dir = os.path.abspath(mcp_dir)
    if mcp_dir not in sys.path:
        sys.path.insert(0, mcp_dir)
    from brain_api import brain_client  # noqa
    return brain_client


def _run_async(coro):
    """在同步节点里执行异步 brain_client 方法（无事件循环时新建，有则用 thread）。"""
    try:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(coro)
            finally:
                loop.close()
        # 已在运行中的事件循环（如 MCP async 工具上下文）：用独立线程跑
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            return pool.submit(lambda: asyncio.run(coro)).result()
    except Exception as e:
        logger.warning(f"async brain call failed: {e}")
        return {"__error__": str(e)}


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
        return {
            "alpha_id": alpha_id,
            "success": True,
            "dry_run": True,
            "submitted": False,
            "steps": [{
                "step": "dry_run",
                "success": True,
                "message": (
                    "Would run submit flow: get_alpha_details → pre_submit_check → "
                    f"[set_properties → submit → poll]（confirm_submit={confirm_submit}）"
                ),
            }],
            "plan": {
                "alpha_id": alpha_id,
                "name": name,
                "color": color,
                "tags": tags,
                "confirm_submit": confirm_submit,
                "force": force,
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
    """保存提交记录到台账并返回。"""
    if store:
        try:
            store.upsert_ledger("WORKFLOW", f"submit_{alpha_id}", {
                "submitted_at": datetime.now().isoformat(),
                "submitted": result.get("submitted", False),
                "final_status": result.get("final_status"),
                "steps": result.get("steps"),
            })
        except Exception as e:
            logger.warning(f"Failed to save submit record: {e}")
    return result
