# -*- coding: utf-8 -*-
"""superalpha 节点：SuperAlpha 构建与提交.

替代 wq-brain-superalpha 的四子命令 PowerShell 模板。
"""

import logging
import os
import subprocess
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def run(
    region: str,
    components: List[str],
    selection: Optional[str] = None,
    combo: Optional[str] = None,
    neutralization: str = "SUBINDUSTRY",
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
        dry_run: 是否干跑
        _context: 执行上下文

    Returns:
        执行结果字典
    """
    ctx = _context or {}
    store = ctx.get("store")

    # 验证组件数量
    if len(components) < 10:
        return {
            "success": False,
            "error": f"Need at least 10 components, got {len(components)}",
            "region": region,
            "components_count": len(components),
        }

    # 默认 selection/combo 模板
    if not selection:
        selection = (
            "(1 + 0 * (prod_correlation > 0)) * "
            "(0.7 - prod_correlation) * "
            "(self_correlation < 0.55) * "
            "(turnover > 0.01) * (turnover < 0.5)"
        )

    if not combo:
        combo = "1 - maxCorr"

    result = {
        "region": region,
        "components": components,
        "components_count": len(components),
        "selection": selection,
        "combo": combo,
        "neutralization": neutralization,
        "steps": [],
        "success": False,
    }

    # Step 1: 探针检查（sa_probe）
    probe_result = _run_sa_probe(region, components, dry_run)
    result["steps"].append(probe_result)

    if not probe_result.get("success"):
        result["error"] = "SA probe failed"
        return result

    # Step 2: 创建 SUPER simulation（super_build select）
    if not dry_run:
        select_result = _run_super_build("select", region, {
            "components": components,
            "selection": selection,
            "combo": combo,
            "neutralization": neutralization,
        })
        result["steps"].append(select_result)

        if not select_result.get("success"):
            result["error"] = "Super build select failed"
            return result

        alpha_id = select_result.get("alpha_id")
        result["alpha_id"] = alpha_id

        # Step 3: 状态检查（super_build status）
        status_result = _run_super_build("status", region, {"alpha_id": alpha_id})
        result["steps"].append(status_result)

        # Step 4: 双闸探针（super_build probe）
        probe2_result = _run_super_build("probe", region, {"alpha_id": alpha_id})
        result["steps"].append(probe2_result)

        # Step 5: 提交（super_build submit）
        submit_result = _run_super_build("submit", region, {"alpha_id": alpha_id})
        result["steps"].append(submit_result)

        result["success"] = submit_result.get("success", False)
    else:
        result["steps"].append({
            "step": "dry_run",
            "success": True,
            "message": "Would execute super_build select/status/probe/submit",
        })
        result["success"] = True

    # 保存到 DB
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


def _run_sa_probe(region: str, components: List[str], dry_run: bool) -> Dict[str, Any]:
    """运行 SA 组件池探针."""
    if dry_run:
        return {
            "step": "sa_probe",
            "success": True,
            "dry_run": True,
            "message": f"Would probe {len(components)} components in {region}",
        }

    # 检查组件是否 ACTIVE
    # 实际实现应调用 mcp__wq-brain-http__get_alpha_details 逐个检查
    active_count = len(components)  # 模拟

    return {
        "step": "sa_probe",
        "success": active_count >= 10,
        "active_count": active_count,
        "required": 10,
        "components": components,
    }


def _run_super_build(subcommand: str, region: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """运行 super_build 子命令."""
    # 查找工具路径
    tools_dir = _find_tools_dir()
    if not tools_dir:
        return {
            "step": f"super_build_{subcommand}",
            "success": False,
            "error": "tools/ directory not found",
        }

    super_build_script = os.path.join(tools_dir, "super_build.py")
    if not os.path.exists(super_build_script):
        return {
            "step": f"super_build_{subcommand}",
            "success": False,
            "error": f"super_build.py not found at {super_build_script}",
        }

    # 构建命令
    wq_py = os.environ.get("WQ_PY", "python")
    cmd = [wq_py, super_build_script, subcommand]

    # 添加参数
    for key, value in params.items():
        if isinstance(value, list):
            cmd.extend([f"--{key}", ",".join(value)])
        else:
            cmd.extend([f"--{key}", str(value)])

    logger.info(f"Executing: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
            cwd=tools_dir,
        )

        return {
            "step": f"super_build_{subcommand}",
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout[-1000:] if result.stdout else "",
            "stderr": result.stderr[-1000:] if result.stderr else "",
        }

    except Exception as e:
        logger.exception(f"super_build {subcommand} failed")
        return {
            "step": f"super_build_{subcommand}",
            "success": False,
            "error": str(e),
        }


def _find_tools_dir() -> Optional[str]:
    """查找 tools/ 目录."""
    # 从当前工作目录向上查找
    cwd = os.getcwd()
    for _ in range(5):
        candidate = os.path.join(cwd, "tools")
        if os.path.exists(candidate):
            return candidate
        cwd = os.path.dirname(cwd)

    # 默认路径
    default = "d:/coding/traeCN_project/wqb/tools"
    if os.path.exists(default):
        return default

    return None
