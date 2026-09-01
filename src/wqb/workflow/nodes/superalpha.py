# -*- coding: utf-8 -*-
"""superalpha 节点：SuperAlpha 构建与提交.

替代 wq-brain-superalpha 的四子命令 PowerShell 模板。

职责边界（2026-08-31 修复）：
  - 旧实现 `_run_sa_probe` 把 active_count 直接设为 len(components)，从不检查组件
    是否 ACTIVE，导致无效组件被送去建 SUPER。
  - 现改为真实调用 tools/sa_probe.py 的 fetch_pool 探针，统计同区域 ACTIVE/IS/OS
    REGULAR 组件数（≥10 硬前置），不满足即 GO/BLOCKED。
  - super_build 各子命令改用共享路径解析定位 tools/，不再硬编码绝对路径。
  - 提交是敏感决策：默认仅 select（建 simulation），不自动 submit。
"""
from __future__ import annotations

import asyncio
import logging
import os
import subprocess
from datetime import datetime
from typing import Any, Dict, List, Optional

from .._common import resolve_tools_dir, wq_py

logger = logging.getLogger(__name__)

_MIN_COMPONENTS = 10


def _get_brain_client():
    import sys
    import os as _os
    mcp_dir = _os.path.join(_os.path.dirname(__file__), "..", "..", "..", "..",
                            "world-quant-brain-mcp")
    mcp_dir = _os.path.abspath(mcp_dir)
    if mcp_dir not in sys.path:
        sys.path.insert(0, mcp_dir)
    from brain_api import brain_client  # noqa
    return brain_client


def _run_async(coro):
    try:
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()
    except Exception as e:
        logger.warning(f"async brain call failed: {e}")
        return {"__error__": str(e)}


def run(
    region: str,
    components: List[str],
    selection: Optional[str] = None,
    combo: Optional[str] = None,
    neutralization: str = "SUBINDUSTRY",
    confirm_submit: bool = False,
    dry_run: bool = False,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """执行 SuperAlpha 构建流程.

    Args:
        region: 区域代码
        components: 组件 alpha ID 列表（≥10 个 ACTIVE REGULAR）
        selection: selection 表达式（默认自动生成）
        combo: combo 表达式（默认自动生成）
        neutralization: 中性化方式（默认 SUBINDUSTRY）
        confirm_submit: 是否真正提交（默认 False，仅建 simulation）
        dry_run: 是否干跑
        _context: 执行上下文

    Returns:
        执行结果字典
    """
    ctx = _context or {}
    store = ctx.get("store")

    result: Dict[str, Any] = {
        "region": region,
        "components": components,
        "components_count": len(components),
        "selection": selection,
        "combo": combo,
        "neutralization": neutralization,
        "steps": [],
        "success": False,
    }

    if len(components) < _MIN_COMPONENTS:
        result["error"] = f"Need at least {_MIN_COMPONENTS} components, got {len(components)}"
        return result

    # Step 1: SA 组件池探针（真实统计同区域 ACTIVE/IS/OS REGULAR 数）
    probe_result = _probe_sa_pool(region, dry_run)
    result["steps"].append(probe_result)
    if not probe_result.get("success"):
        result["error"] = probe_result.get("error", "SA probe failed")
        return result

    if dry_run:
        result["steps"].append({
            "step": "dry_run",
            "success": True,
            "message": "Would run super_build select/status/probe[/submit]",
        })
        result["success"] = True
        return result

    # Step 2: select（创建 SUPER simulation）
    select_result = _run_super_build("select", {
        "region": region,
        "universe": _default_universe(region),
        "neutralization": neutralization,
    })
    result["steps"].append(select_result)
    if not select_result.get("success"):
        result["error"] = "super_build select failed"
        return result

    alpha_id = select_result.get("alpha_id")
    result["alpha_id"] = alpha_id
    if not alpha_id:
        result["error"] = "select 未返回 alpha_id"
        return result

    # Step 3: status
    status_result = _run_super_build("status", {"alpha_id": alpha_id})
    result["steps"].append(status_result)

    # Step 4: probe（双闸探针）
    probe2_result = _run_super_build("probe", {"alpha_id": alpha_id})
    result["steps"].append(probe2_result)

    # Step 5: 提交（敏感决策，需 confirm_submit=True）
    if confirm_submit:
        submit_result = _run_super_build("submit", {
            "alpha_id": alpha_id,
            "name": _default_name(region),
            "region": region,
        })
        # 归一步名：_run_super_build 返回 "super_build_submit"，此处统一为 "submit"，
        # 与 confirm_submit=False 的 skipped 分支同名，下游可按 step 名一致判定提交状态。
        submit_result["step"] = "submit"
        submit_result["subcommand"] = "super_build_submit"
        result["steps"].append(submit_result)
        result["success"] = submit_result.get("success", False)
    else:
        result["steps"].append({
            "step": "submit",
            "success": True,
            "skipped": True,
            "note": "confirm_submit=False，未提交（仅建 simulation + 探针）",
        })
        result["success"] = True

    if store and result["success"]:
        try:
            store.upsert_ledger("WORKFLOW", f"superalpha_{region}_{datetime.now().strftime('%Y%m%d')}", {
                "created_at": datetime.now().isoformat(),
                "region": region,
                "components_count": len(components),
                "alpha_id": result.get("alpha_id"),
            })
        except Exception as e:
            logger.warning(f"Failed to save superalpha record: {e}")

    return result


def _probe_sa_pool(region: str, dry_run: bool) -> Dict[str, Any]:
    """真实 SA 组件池探针：调用 tools/sa_probe.py 的 fetch_pool。"""
    if dry_run:
        return {"step": "sa_probe", "success": True, "dry_run": True,
                "message": f"Would probe {region} REGULAR pool (need >= {_MIN_COMPONENTS} ACTIVE)"}

    try:
        import sys
        tools_dir = resolve_tools_dir()
        if tools_dir not in sys.path:
            sys.path.insert(0, tools_dir)
        from sa_probe import fetch_pool  # 真实拉取组件池

        brain = _get_brain_client()
        pool = _run_async(fetch_pool(brain, region, limit_hint=950))
        if isinstance(pool, dict) and pool.get("__error__"):
            return {"step": "sa_probe", "success": False, "error": pool["__error__"]}

        eligible = [p for p in pool if p.get("status") == "ACTIVE" or p.get("stage") in ("IS", "OS")]
        ok = len(eligible) >= _MIN_COMPONENTS
        return {
            "step": "sa_probe",
            "success": ok,
            "total": len(pool),
            "eligible": len(eligible),
            "required": _MIN_COMPONENTS,
            "verdict": "GO" if ok else "BLOCKED",
            "error": None if ok else f"仅 {len(eligible)} 颗 eligible（需 ≥{_MIN_COMPONENTS}）",
        }
    except Exception as e:
        logger.warning(f"sa_probe failed: {e}")
        return {"step": "sa_probe", "success": False, "error": str(e)}


def _run_super_build(subcommand: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """运行 tools/super_build.py 子命令。"""
    tools_dir = resolve_tools_dir()
    super_build_script = os.path.join(tools_dir, "super_build.py")
    if not os.path.exists(super_build_script):
        return {"step": f"super_build_{subcommand}", "success": False,
                "error": f"super_build.py not found at {super_build_script}"}

    cmd = [wq_py(), super_build_script, subcommand]
    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, list):
            cmd.extend([f"--{key.replace('_', '-')}", ",".join(value)])
        else:
            cmd.extend([f"--{key.replace('_', '-')}", str(value)])

    logger.info(f"Executing: {' '.join(cmd)}")
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900, cwd=tools_dir)
        out = {
            "step": f"super_build_{subcommand}",
            "success": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": (proc.stdout or "")[-1000:],
            "stderr": (proc.stderr or "")[-1000:],
        }
        # select 子命令从 stdout 提取 alpha id
        if subcommand == "select" and proc.returncode == 0:
            import re
            m = re.search(r"alpha id = (\w+)", proc.stdout or "")
            if m:
                out["alpha_id"] = m.group(1)
        return out
    except subprocess.TimeoutExpired:
        return {"step": f"super_build_{subcommand}", "success": False, "error": "timeout after 900s"}
    except Exception as e:
        logger.exception(f"super_build {subcommand} failed")
        return {"step": f"super_build_{subcommand}", "success": False, "error": str(e)}


def _default_universe(region: str) -> str:
    try:
        from wqb.config import default_universe
        return default_universe(region)
    except Exception:
        return "TOP3000"


def _default_name(region: str) -> str:
    """提交命名约定：用 prodCorrelation 最大值（此处在无探针值时用占位，由 super_build submit 实际约定）。"""
    return region
