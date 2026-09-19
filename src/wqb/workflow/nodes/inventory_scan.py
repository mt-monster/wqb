# -*- coding: utf-8 -*-
"""inventory_scan 节点：自动化库存盘点（S-PRE 增强）.

自动化库存盘点流程：
1. 枚举已有 IS alpha
2. 资格门复算
3. 写回过闸率先验
4. 去参数网格 + OS 撞车预筛 + 篮内正交 + 平台复核
"""

import json
import logging
import os
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
    target: int = 20,
    regions: Optional[List[str]] = None,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """执行自动化库存盘点.

    Args:
        region: 区域代码
        target: 目标候选数（默认 20）
        regions: 要盘点的区域列表（默认 all）
        _context: 执行上下文

    Returns:
        执行结果字典
    """
    ctx = _context or {}
    result = {
        "region": region,
        "target": target,
        "regions": regions or ["all"],
        "success": False,
        "steps": [],
    }

    # 构建命令
    tools_dir = resolve_tools_dir()
    py = wq_py()

    # 步骤 1：枚举 + 资格门复算 + 写回过闸率先验
    step1_cmd = [
        py,
        os.path.join(tools_dir, "build_gate_prior_from_inventory.py"),
        "--regions", ",".join(regions or ["all"]),
        "--emit-candidates", "cache/candidates.json",
        "--write-priors",
    ]

    result["steps"].append({
        "step": "build_gate_prior",
        "command": " ".join(step1_cmd),
        "success": True,
    })

    # 步骤 2：去参数网格 + OS 撞车预筛 + 篮内正交 + 平台复核
    step2_cmd = [
        py,
        os.path.join(tools_dir, "select_ra_basket.py"),
        "cache/candidates.json",
        "--target", str(target),
        "--out", "cache/basket.json",
    ]

    result["steps"].append({
        "step": "select_ra_basket",
        "command": " ".join(step2_cmd),
        "success": True,
    })

    # 如果是 dry-run，到此为止
    if ctx.get("dry_run"):
        result["success"] = True
        result["dry_run"] = True
        result["note"] = "dry-run：命令已构建，未执行"
        return result

    # 执行命令
    try:
        # 执行步骤 1
        logger.info(f"Executing inventory scan step 1: {' '.join(step1_cmd)}")
        proc1 = subprocess.run(
            step1_cmd,
            capture_output=True,
            text=True,
            timeout=600,
            cwd=str(REPO_ROOT),
        )

        result["steps"][0]["returncode"] = proc1.returncode
        result["steps"][0]["stdout_tail"] = (proc1.stdout or "")[-2000:]
        result["steps"][0]["stderr_tail"] = (proc1.stderr or "")[-500:]

        if proc1.returncode != 0:
            result["error"] = f"Step 1 failed with returncode {proc1.returncode}"
            return result

        # 执行步骤 2
        logger.info(f"Executing inventory scan step 2: {' '.join(step2_cmd)}")
        proc2 = subprocess.run(
            step2_cmd,
            capture_output=True,
            text=True,
            timeout=300,
            cwd=str(REPO_ROOT),
        )

        result["steps"][1]["returncode"] = proc2.returncode
        result["steps"][1]["stdout_tail"] = (proc2.stdout or "")[-2000:]
        result["steps"][1]["stderr_tail"] = (proc2.stderr or "")[-500:]

        if proc2.returncode != 0:
            result["error"] = f"Step 2 failed with returncode {proc2.returncode}"
            return result

        # 读取结果
        basket_path = os.path.join(REPO_ROOT, "cache", "basket.json")
        if os.path.exists(basket_path):
            with open(basket_path, "r", encoding="utf-8") as f:
                basket = json.load(f)
            result["basket"] = basket
            result["candidate_count"] = len(basket.get("candidates", []))

        result["success"] = True
        result["message"] = f"Inventory scan completed: {result.get('candidate_count', 0)} candidates found"

    except subprocess.TimeoutExpired:
        result["error"] = "Inventory scan timeout"
    except Exception as e:
        result["error"] = f"Inventory scan failed: {e}"
        logger.exception("Inventory scan failed")

    return result
