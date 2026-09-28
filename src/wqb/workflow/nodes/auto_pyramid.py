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

from ...wave_results_contract import upsert_wave_result
from .._common import (
    REPO_ROOT,
    resolve_campaign_dir,
    resolve_db_path,
    resolve_tools_dir,
    wq_py,
)

from wqb.db_conn import connect as db_connect  # 规范工厂（2026-09-20 L1 收口）
logger = logging.getLogger(__name__)

#: 本节点写进 key_findings 的行的前缀（重跑时整行替换；评审重跑与收批级联都保留它）
PYRAMID_PREFIX = "[pyramid]"


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
            embed = _embed_pyramid(region, wave, pyramid_progress.get("key_findings_line", ""))
            _step(result, "auto_embed").update(embed)
            if not embed["embedded"]:
                result["error"] = f"点塔进度未嵌入 wave_results：{embed.get('error') or embed.get('note')}"
        # 步骤 3：自动生成点塔报告
        if auto_report:
            report = _generate_pyramid_report(pyramid_progress)
            _step(result, "auto_report")["report"] = report

        result["success"] = "error" not in result
        result["pyramid_progress"] = pyramid_progress
        result["message"] = f"Auto pyramid {'completed' if result['success'] else 'incomplete'}: {region}/{wave}"

    except subprocess.TimeoutExpired:
        result["error"] = "Auto pyramid timeout"
    except Exception as e:
        result["error"] = f"Auto pyramid failed: {e}"
        logger.exception("Auto pyramid failed")

    return result


def _step(result: Dict[str, Any], name: str) -> Dict[str, Any]:
    # 按名字取步骤：此前按下标取，auto_embed=False 时 steps[2] 不存在（IndexError → 整个节点失败）
    return next(s for s in result["steps"] if s.get("step") == name)


def _embed_pyramid(region: str, wave: str, key_findings_line: str) -> Dict[str, Any]:
    """把 campaign_intel `[key_findings]` 单行以 `[pyramid] …` 写进该波 wave_results.key_findings。

    2026-09-27 N30：走写入契约（合并式 upsert，只写 key_findings；verdict / status / created_at 不动），
    此前是直写 UPDATE，且写进去的是整个进度 dict 的 repr（含 2000 字输出尾巴）。本节点自己的
    `[pyramid]` 行整行替换（此前每跑一次追加一条）。以下情况如实返回 embedded=False、不写库：
    没有 `[key_findings]` 单行；本波还没有结论行；契约拒写（结案却没有 verdict 的旧空壳行）。
    """
    line = key_findings_line.strip()
    if line.startswith("[key_findings]"):
        line = line[len("[key_findings]"):].strip()
    if not line:
        return {"embedded": False, "success": False,
                "note": "campaign_intel pyramid 输出里没有 [key_findings] 单行"}
    wave_id = str(wave).strip()
    conn = db_connect(resolve_db_path())
    try:
        row = conn.execute("SELECT key_findings FROM wave_results WHERE region=? AND wave_number=?",
                           (region, wave_id)).fetchone()
        if row is None:
            return {"embedded": False, "success": False,
                    "note": f"wave_results 没有 {region}/{wave_id} 这一行：先由评审入库或 upsert_wave_result 写结论"}
        try:
            findings = json.loads(row[0]) if row[0] else []
        except (TypeError, ValueError):
            findings = [row[0]]
        findings = [f for f in (findings if isinstance(findings, list) else [findings])
                    if not str(f).startswith(PYRAMID_PREFIX)]
        findings.append(f"{PYRAMID_PREFIX} {line}")
        res = upsert_wave_result(conn, region, wave_id, datetime.now().isoformat(timespec="seconds"),
                                 key_findings=findings)
        if "error" in res:
            return {"embedded": False, "success": False, "error": res["error"]}
        conn.commit()
        return {"embedded": True, "success": True, "finding": f"{PYRAMID_PREFIX} {line}"}
    finally:
        conn.close()


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
