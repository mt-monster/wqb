# -*- coding: utf-8 -*-
"""auto_pyramid 节点：自动化点塔进度回写（S6 增强）.

自动化点塔进度回写：
1. 自动查询点塔进度
2. 自动嵌入 wave_result.key_findings
3. 自动生成点塔报告
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

from wqb.db_conn import connect as db_connect  # 规范工厂（2026-09-20 L1 收口）
logger = logging.getLogger(__name__)


def run(
    region: str,
    wave: str,
    delay: int = 1,
    auto_embed: bool = True,
    auto_report: bool = True,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """执行自动化点塔进度回写.

    Args:
        region: 区域代码
        wave: 波次号
        delay: 延迟（默认 1）
        auto_embed: 是否自动嵌入 wave_result.key_findings（默认 True）
        auto_report: 是否自动生成点塔报告（默认 True）
        _context: 执行上下文

    Returns:
        执行结果字典
    """
    ctx = _context or {}
    result = {
        "region": region,
        "wave": wave,
        "delay": delay,
        "success": False,
        "steps": [],
    }

    # 步骤 1：自动查询点塔进度
    result["steps"].append({
        "step": "auto_query_pyramid",
        "success": True,
        "description": "自动查询点塔进度",
    })

    # 步骤 2：自动嵌入 wave_result.key_findings
    if auto_embed:
        result["steps"].append({
            "step": "auto_embed",
            "success": True,
            "description": "自动嵌入 wave_result.key_findings",
        })

    # 步骤 3：自动生成点塔报告
    if auto_report:
        result["steps"].append({
            "step": "auto_report",
            "success": True,
            "description": "自动生成点塔报告",
        })

    # 如果是 dry-run，到此为止
    # dry-run：走完零成本前置——构建真实命令（campaign_intel.py pyramid）→ 到此为止。
    # 不 subprocess、不写库（禁止假 dry-run：不构建命令却报 success）。
    if ctx.get("dry_run"):
        tools_dir = resolve_tools_dir()
        py = wq_py()
        script = os.path.join(tools_dir, "campaign_intel.py")
        pyramid_cmd = [
            py, script, "pyramid",
            "--region", region,
            "--delay", str(delay),
        ]
        if not os.path.exists(script):
            result["steps"].append({
                "step": "find_campaign_intel", "success": False,
                "error": f"campaign_intel.py not found: {script}",
            })
            result["error"] = f"campaign_intel.py not found: {script}"
            return result
        result["command"] = " ".join(pyramid_cmd)
        result["plan"] = {
            "region": region, "wave": wave, "delay": delay,
            "auto_embed": auto_embed, "auto_report": auto_report,
            "tool": script,
            "steps": [
                "1. campaign_intel.py pyramid --region --delay 查询点塔进度快照",
                "2. 解析 stdout 尾部 [key_findings] 单行",
                "3. (auto_embed) 嵌入 wave_results.key_findings",
                "4. (auto_report) 生成点塔报告",
            ],
        }
        result["steps"].append({
            "step": "build_command", "success": True, "command": " ".join(pyramid_cmd),
        })
        result["success"] = True
        result["dry_run"] = True
        result["note"] = "dry-run：命令已构建，未执行"
        return result

    # 执行自动化点塔进度回写
    try:
        tools_dir = resolve_tools_dir()
        py = wq_py()

        # 步骤 1：自动查询点塔进度
        pyramid_cmd = [
            py,
            os.path.join(tools_dir, "campaign_intel.py"),
            "pyramid",
            "--region", region,
            "--delay", str(delay),
        ]

        logger.info(f"Executing pyramid query: {' '.join(pyramid_cmd)}")
        pyramid_proc = subprocess.run(
            pyramid_cmd,
            capture_output=True,
            text=True,
            timeout=300,
            cwd=str(REPO_ROOT),
        )

        result["steps"][0]["returncode"] = pyramid_proc.returncode
        result["steps"][0]["stdout_tail"] = (pyramid_proc.stdout or "")[-2000:]
        result["steps"][0]["stderr_tail"] = (pyramid_proc.stderr or "")[-500:]

        if pyramid_proc.returncode != 0:
            result["error"] = f"Pyramid query failed with returncode {pyramid_proc.returncode}"
            return result

        # 解析点塔进度
        pyramid_output = pyramid_proc.stdout or ""
        pyramid_progress = _parse_pyramid_output(pyramid_output)

        # 步骤 2：自动嵌入 wave_result.key_findings
        if auto_embed:
            db_path = resolve_db_path()
            conn = db_connect(db_path)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            # 查询 wave_result
            c.execute(
                "SELECT * FROM wave_results WHERE region=? AND wave_number=?",
                (region, wave),
            )
            wave_result = c.fetchone()

            if wave_result:
                # 解析 key_findings
                key_findings = json.loads(wave_result["key_findings"]) if wave_result["key_findings"] else []

                # 嵌入点塔进度
                key_findings.append(f"[pyramid] {pyramid_progress}")

                # 更新 wave_result
                c.execute(
                    "UPDATE wave_results SET key_findings=?, updated_at=? WHERE region=? AND wave_number=?",
                    (json.dumps(key_findings, ensure_ascii=False),
                     datetime.now().isoformat(timespec="seconds"),
                     region, wave),
                )
                conn.commit()

            conn.close()

            result["steps"][1]["embedded"] = True

        # 步骤 3：自动生成点塔报告
        if auto_report:
            report = _generate_pyramid_report(pyramid_progress)
            result["steps"][2]["report"] = report

        result["success"] = True
        result["pyramid_progress"] = pyramid_progress
        result["message"] = f"Auto pyramid completed: {region}/{wave}"

    except subprocess.TimeoutExpired:
        result["error"] = "Auto pyramid timeout"
    except Exception as e:
        result["error"] = f"Auto pyramid failed: {e}"
        logger.exception("Auto pyramid failed")

    return result


def _parse_pyramid_output(output: str) -> Dict[str, Any]:
    """解析点塔进度输出."""
    # 提取 [key_findings] 单行
    key_findings_line = ""
    for line in output.split("\n"):
        if line.startswith("[key_findings]"):
            key_findings_line = line
            break

    # 解析点塔进度
    progress = {
        "key_findings_line": key_findings_line,
        "output_tail": output[-2000:],
    }

    return progress


def _generate_pyramid_report(pyramid_progress: Dict[str, Any]) -> Dict[str, Any]:
    """自动生成点塔报告."""
    return {
        "pyramid_progress": pyramid_progress,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }
