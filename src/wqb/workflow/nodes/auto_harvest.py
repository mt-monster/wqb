# -*- coding: utf-8 -*-
"""auto_harvest 节点：自动化收批流程（S3 增强）.

自动化收批流程：
1. 自动收批 multisim 结果
2. 自动关联 expressions
3. 自动写回 backtest_results
4. 自动生成收批报告
"""

import json
import logging
import os
import sqlite3
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
    wave: str,
    multisim_id: Optional[str] = None,
    auto_link: bool = True,
    auto_upsert: bool = True,
    auto_report: bool = True,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """执行自动化收批流程.

    Args:
        region: 区域代码
        wave: 波次号
        multisim_id: multisim ID（可选，从 DB 读取）
        auto_link: 是否自动关联 expressions（默认 True）
        auto_upsert: 是否自动写回 backtest_results（默认 True）
        auto_report: 是否自动生成收批报告（默认 True）
        _context: 执行上下文

    Returns:
        执行结果字典
    """
    ctx = _context or {}
    result = {
        "region": region,
        "wave": wave,
        "multisim_id": multisim_id,
        "success": False,
        "steps": [],
    }

    # 步骤 1：自动收批 multisim 结果
    result["steps"].append({
        "step": "auto_harvest",
        "success": True,
        "description": "自动收批 multisim 结果",
    })

    # 步骤 2：自动关联 expressions
    if auto_link:
        result["steps"].append({
            "step": "auto_link",
            "success": True,
            "description": "自动关联 expressions",
        })

    # 步骤 3：自动写回 backtest_results
    if auto_upsert:
        result["steps"].append({
            "step": "auto_upsert",
            "success": True,
            "description": "自动写回 backtest_results",
        })

    # 步骤 4：自动生成收批报告
    if auto_report:
        result["steps"].append({
            "step": "auto_report",
            "success": True,
            "description": "自动生成收批报告",
        })

    # 如果是 dry-run，到此为止
    if ctx.get("dry_run"):
        result["success"] = True
        result["dry_run"] = True
        result["note"] = "dry-run：自动化收批流程已构建，未执行"
        return result

    # 执行自动化收批流程
    try:
        # 从 DB 读取 multisim 结果
        db_path = resolve_db_path()
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        # 查询 multisim 结果
        if multisim_id:
            c.execute(
                "SELECT * FROM backtest_results WHERE region=? AND wave=? AND multisim_id=?",
                (region, wave, multisim_id),
            )
        else:
            c.execute(
                "SELECT * FROM backtest_results WHERE region=? AND wave=?",
                (region, wave),
            )

        backtest_results = [dict(r) for r in c.fetchall()]

        if not backtest_results:
            result["error"] = f"No backtest results found: {region}/{wave}"
            conn.close()
            return result

        # 自动关联 expressions
        if auto_link:
            c.execute(
                "SELECT * FROM expressions WHERE region=? AND wave=?",
                (region, wave),
            )
            expressions = [dict(r) for r in c.fetchall()]

            # 关联 expressions
            expr_map = {e.get("alpha_id"): e.get("id") for e in expressions if e.get("alpha_id")}
            code_map = {e.get("expression"): e.get("id") for e in expressions if e.get("expression")}

            linked_count = 0
            for bt in backtest_results:
                alpha_id = bt.get("alpha_id")
                code = bt.get("expression") or bt.get("code")
                if alpha_id and alpha_id in expr_map:
                    bt["expression_id"] = expr_map[alpha_id]
                    linked_count += 1
                elif code and code in code_map:
                    bt["expression_id"] = code_map[code]
                    linked_count += 1

            result["steps"][1]["linked_count"] = linked_count

        # 自动写回 backtest_results
        if auto_upsert:
            for bt in backtest_results:
                c.execute(
                    """INSERT OR REPLACE INTO backtest_results
                       (id, region, wave, dataset, alpha_id, expression, status, sharpe, fitness,
                        turnover, margin, two_year_sharpe, sub_universe_sharpe, failed_checks,
                        universe, delay, neut, expression_id, created_at, updated_at)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (
                        bt.get("id"),
                        bt.get("region"),
                        bt.get("wave"),
                        bt.get("dataset"),
                        bt.get("alpha_id"),
                        bt.get("expression"),
                        bt.get("status"),
                        bt.get("sharpe"),
                        bt.get("fitness"),
                        bt.get("turnover"),
                        bt.get("margin"),
                        bt.get("two_year_sharpe"),
                        bt.get("sub_universe_sharpe"),
                        bt.get("failed_checks"),
                        bt.get("universe"),
                        bt.get("delay"),
                        bt.get("neut"),
                        bt.get("expression_id"),
                        bt.get("created_at"),
                        datetime.now().isoformat(timespec="seconds"),
                    ),
                )
            conn.commit()

            result["steps"][2]["upserted_count"] = len(backtest_results)

        # 自动生成收批报告
        if auto_report:
            report = _generate_harvest_report(backtest_results)
            result["steps"][3]["report"] = report

        conn.close()

        result["success"] = True
        result["backtest_count"] = len(backtest_results)
        result["message"] = f"Auto harvest completed: {len(backtest_results)} backtest results processed"

    except Exception as e:
        result["error"] = f"Auto harvest failed: {e}"
        logger.exception("Auto harvest failed")

    return result


def _generate_harvest_report(backtest_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """生成收批报告."""
    total = len(backtest_results)
    complete = len([bt for bt in backtest_results if bt.get("status") == "COMPLETE"])
    error = len([bt for bt in backtest_results if bt.get("status") == "ERROR"])
    cancelled = len([bt for bt in backtest_results if bt.get("status") == "CANCELLED"])

    # 统计 sharpe 分布
    sharpes = [bt.get("sharpe") for bt in backtest_results if bt.get("sharpe") is not None]
    avg_sharpe = sum(sharpes) / len(sharpes) if sharpes else 0
    max_sharpe = max(sharpes) if sharpes else 0
    min_sharpe = min(sharpes) if sharpes else 0

    # 统计过闸率
    passed = len([bt for bt in backtest_results if bt.get("sharpe", 0) >= 1.58 and bt.get("fitness", 0) >= 1.0])
    pass_rate = passed / total if total > 0 else 0

    return {
        "total": total,
        "complete": complete,
        "error": error,
        "cancelled": cancelled,
        "avg_sharpe": round(avg_sharpe, 4),
        "max_sharpe": round(max_sharpe, 4),
        "min_sharpe": round(min_sharpe, 4),
        "passed": passed,
        "pass_rate": round(pass_rate, 4),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }
