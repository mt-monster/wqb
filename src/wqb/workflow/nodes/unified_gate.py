# -*- coding: utf-8 -*-
"""unified_gate 节点：合并重复门禁检查（S2→S3 增强）.

合并重复门禁检查：
1. 幽灵算子硬闸
2. 多样性守卫
3. 体检→表达式硬门
4. 8 闸预检（合并重复闸门）
"""

import json
import logging
import os
import sqlite3
import subprocess
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
    wave: str,
    exprs_file: Optional[str] = None,
    from_db: bool = True,
    skip_diversity_gate: bool = False,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """执行合并重复门禁检查.

    Args:
        region: 区域代码
        dataset: 数据集 ID
        wave: 波次号
        exprs_file: 表达式文件路径（可选）
        from_db: 是否从 DB 读取表达式（默认 True）
        skip_diversity_gate: 是否跳过多样性闸（默认 False）
        _context: 执行上下文

    Returns:
        执行结果字典
    """
    ctx = _context or {}
    result = {
        "region": region,
        "dataset": dataset,
        "wave": wave,
        "success": False,
        "steps": [],
    }

    # 步骤 1：幽灵算子硬闸
    result["steps"].append({
        "step": "ghost_operator_gate",
        "success": True,
        "description": "幽灵算子硬闸",
    })

    # 步骤 2：多样性守卫
    if not skip_diversity_gate:
        result["steps"].append({
            "step": "diversity_gate",
            "success": True,
            "description": "多样性守卫",
        })

    # 步骤 3：体检→表达式硬门
    result["steps"].append({
        "step": "field_inspect_gate",
        "success": True,
        "description": "体检→表达式硬门",
    })

    # 步骤 4：8 闸预检（合并重复闸门）
    result["steps"].append({
        "step": "unified_gate_check",
        "success": True,
        "description": "8 闸预检（合并重复闸门）",
    })

    # 如果是 dry-run，到此为止
    if ctx.get("dry_run"):
        result["success"] = True
        result["dry_run"] = True
        result["note"] = "dry-run：合并重复门禁检查流程已构建，未执行"
        return result

    # 执行合并重复门禁检查
    try:
        tools_dir = resolve_tools_dir()
        py = wq_py()

        # 步骤 1：幽灵算子硬闸
        ghost_cmd = [
            py,
            os.path.join(tools_dir, "campaign_intel.py"),
            "ghost-audit",
            "--region", region,
        ]
        if exprs_file:
            ghost_cmd.extend(["--exprs-file", exprs_file])

        logger.info(f"Executing ghost operator gate: {' '.join(ghost_cmd)}")
        ghost_proc = subprocess.run(
            ghost_cmd,
            capture_output=True,
            text=True,
            timeout=300,
            cwd=str(REPO_ROOT),
        )

        result["steps"][0]["returncode"] = ghost_proc.returncode
        result["steps"][0]["stdout_tail"] = (ghost_proc.stdout or "")[-2000:]
        result["steps"][0]["stderr_tail"] = (ghost_proc.stderr or "")[-500:]

        if ghost_proc.returncode != 0:
            result["error"] = f"Ghost operator gate failed with returncode {ghost_proc.returncode}"
            return result

        # 步骤 2-4：统一门禁检查（调用 wave_gate.py，它已包含多样性守卫、体检硬门和 8 闸预检）
        gate_cmd = [
            py,
            os.path.join(tools_dir, "wave_gate.py"),
            "--campaign-dir", resolve_campaign_dir(region),
            "--dataset", dataset,
            "--wave", wave,
        ]
        if from_db:
            gate_cmd.append("--from-db")
        if skip_diversity_gate:
            gate_cmd.append("--skip-diversity-gate")

        logger.info(f"Executing unified gate check: {' '.join(gate_cmd)}")
        gate_proc = subprocess.run(
            gate_cmd,
            capture_output=True,
            text=True,
            timeout=600,
            cwd=str(REPO_ROOT),
        )

        result["steps"][-1]["returncode"] = gate_proc.returncode
        result["steps"][-1]["stdout_tail"] = (gate_proc.stdout or "")[-2000:]
        result["steps"][-1]["stderr_tail"] = (gate_proc.stderr or "")[-500:]

        if gate_proc.returncode != 0:
            result["error"] = f"Unified gate check failed with returncode {gate_proc.returncode}"
            return result

        # 读取门禁结果
        db_path = resolve_db_path()
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute(
            "SELECT * FROM gate_results WHERE region=? AND wave=? AND dataset=?",
            (region, wave, dataset),
        )
        gate_result = c.fetchone()
        conn.close()

        if gate_result:
            result["gate_result"] = json.loads(gate_result["report"])

        result["success"] = True
        result["message"] = f"Unified gate check completed: {region}/{dataset}/{wave}"

    except subprocess.TimeoutExpired:
        result["error"] = "Unified gate check timeout"
    except Exception as e:
        result["error"] = f"Unified gate check failed: {e}"
        logger.exception("Unified gate check failed")

    return result
