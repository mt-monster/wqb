# -*- coding: utf-8 -*-
"""batch_track 节点：S3 批量回测与跟踪.

替代 brain-simAlphasinBatch-and-track 的 PowerShell 命令模板。
"""

import logging
import os
import subprocess
import time
from datetime import datetime
from typing import Any, Dict, Optional

from ..mcp_check import require_mcp_tools
from .._common import resolve_campaign_dir, resolve_toolkit_dir, wq_py

logger = logging.getLogger(__name__)


@require_mcp_tools("batch_track")
def run(
    region: str,
    wave: str,
    dataset: str,
    concurrency: int = 7,
    max_rounds: int = 3,
    dry_run: bool = False,
    output_csv: Optional[str] = None,
    campaign_dir: Optional[str] = None,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """执行批量回测跟踪.

    Args:
        region: 区域代码（如 KOR）
        wave: 波次号（如 36A）
        dataset: 数据集 ID
        concurrency: 并发数（默认 7，七槽填槽）
        max_rounds: 最大轮次
        dry_run: 是否干跑
        output_csv: 输出 CSV 路径（默认自动生成）
        campaign_dir: 战役目录（可选，默认自动解析）
        _context: 执行上下文（由 executor 注入）

    Returns:
        执行结果字典
    """
    ctx = _context or {}
    store = ctx.get("store")

    # 生成输出路径
    if not output_csv:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_csv = f"outputs/simulation_status_{region}_{wave}_{timestamp}.csv"

    # 解析 campaign-dir（优先级：参数 > 环境变量 > 自动探测）
    if not campaign_dir:
        campaign_dir = resolve_campaign_dir(region)
    
    if not campaign_dir:
        return {
            "success": False,
            "error": f"Cannot resolve campaign_dir for region={region}. "
                     "Set WQB_CAMPAIGN_DIR env var or pass campaign_dir parameter.",
            "region": region,
            "wave": wave,
            "dataset": dataset,
        }

    # 验证战役目录
    if not os.path.exists(campaign_dir):
        return {
            "success": False,
            "error": f"Campaign directory not found: {campaign_dir}",
            "region": region,
            "wave": wave,
            "dataset": dataset,
            "campaign_dir": campaign_dir,
        }

    # 读取表达式（从 DB）
    expressions = []
    if store:
        try:
            expressions = store.list_expressions(region, wave, dataset)
        except Exception as e:
            logger.warning(f"Failed to list expressions from DB: {e}")

    if not expressions:
        return {
            "success": False,
            "error": f"No expressions found for {region}/{wave}/{dataset}",
            "region": region,
            "wave": wave,
            "dataset": dataset,
        }

    # 干跑模式：返回执行计划
    if dry_run:
        return {
            "success": True,
            "dry_run": True,
            "plan": {
                "region": region,
                "wave": wave,
                "dataset": dataset,
                "expression_count": len(expressions),
                "concurrency": concurrency,
                "max_rounds": max_rounds,
                "output_csv": output_csv,
                "campaign_dir": campaign_dir,
            },
            "message": f"Would execute batch track for {len(expressions)} expressions",
        }

    # 实际执行：调用 toolkit pipeline.py
    toolkit_dir = resolve_toolkit_dir()

    if not toolkit_dir or not os.path.exists(toolkit_dir):
        return {
            "success": False,
            "error": "WQ_TOOLKIT_DIR not found. Set env var or install wq-brain-campaign-toolkit skill.",
            "region": region,
            "wave": wave,
            "dataset": dataset,
        }

    pipeline_script = os.path.join(toolkit_dir, "pipeline.py")
    if not os.path.exists(pipeline_script):
        return {
            "success": False,
            "error": f"pipeline.py not found at {pipeline_script}",
            "region": region,
            "wave": wave,
            "dataset": dataset,
        }

    # 构建命令
    cmd = [
        wq_py(),
        pipeline_script,
        "--campaign-dir", campaign_dir,
        "run",
        "--dataset", dataset,
        "--wave", wave,
        "--max-rounds", str(max_rounds),
        "--review",
        "--write-ledger",
    ]

    logger.info(f"Executing: {' '.join(cmd)}")

    # 执行
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3600,  # 1 小时超时
            cwd=toolkit_dir,
        )

        success = result.returncode == 0
        output = {
            "success": success,
            "returncode": result.returncode,
            "stdout": result.stdout[-2000:] if result.stdout else "",  # 截断
            "stderr": result.stderr[-2000:] if result.stderr else "",
            "region": region,
            "wave": wave,
            "dataset": dataset,
            "expression_count": len(expressions),
            "output_csv": output_csv,
        }

        # 保存 checkpoint
        if store and success:
            try:
                store.upsert_ledger("WORKFLOW", f"batch_track_{region}_{wave}", {
                    "completed_at": datetime.now().isoformat(),
                    "expression_count": len(expressions),
                    "output_csv": output_csv,
                })
            except Exception as e:
                logger.warning(f"Failed to save checkpoint: {e}")

        return output

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Execution timeout (3600s)",
            "region": region,
            "wave": wave,
            "dataset": dataset,
        }
    except Exception as e:
        logger.exception("batch_track execution failed")
        return {
            "success": False,
            "error": str(e),
            "region": region,
            "wave": wave,
            "dataset": dataset,
        }


# _resolve_campaign_dir 已迁至 _common.resolve_campaign_dir（单一事实源）
