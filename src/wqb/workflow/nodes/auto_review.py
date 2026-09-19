# -*- coding: utf-8 -*-
"""auto_review 节点：自动化评审流程（S4 增强）.

自动化评审流程：
1. 自动 S4 预筛
2. 自动 walls 诊断
3. 自动卡闸辅助腿检索
4. 自动生成评审报告
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
    wave: str,
    dataset: Optional[str] = None,
    auto_prescreen: bool = True,
    auto_walls: bool = True,
    auto_salvage: bool = True,
    auto_report: bool = True,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """执行自动化评审流程.

    Args:
        region: 区域代码
        wave: 波次号
        dataset: 数据集 ID（可选）
        auto_prescreen: 是否自动 S4 预筛（默认 True）
        auto_walls: 是否自动 walls 诊断（默认 True）
        auto_salvage: 是否自动卡闸辅助腿检索（默认 True）
        auto_report: 是否自动生成评审报告（默认 True）
        _context: 执行上下文

    Returns:
        执行结果字典
    """
    ctx = _context or {}
    result = {
        "region": region,
        "wave": wave,
        "dataset": dataset,
        "success": False,
        "steps": [],
    }

    # 步骤 1：自动 S4 预筛
    if auto_prescreen:
        result["steps"].append({
            "step": "auto_prescreen",
            "success": True,
            "description": "自动 S4 预筛",
        })

    # 步骤 2：自动 walls 诊断
    if auto_walls:
        result["steps"].append({
            "step": "auto_walls",
            "success": True,
            "description": "自动 walls 诊断",
        })

    # 步骤 3：自动卡闸辅助腿检索
    if auto_salvage:
        result["steps"].append({
            "step": "auto_salvage",
            "success": True,
            "description": "自动卡闸辅助腿检索",
        })

    # 步骤 4：自动生成评审报告
    if auto_report:
        result["steps"].append({
            "step": "auto_report",
            "success": True,
            "description": "自动生成评审报告",
        })

    # 如果是 dry-run，到此为止
    if ctx.get("dry_run"):
        result["success"] = True
        result["dry_run"] = True
        result["note"] = "dry-run：自动化评审流程已构建，未执行"
        return result

    # 执行自动化评审流程
    try:
        tools_dir = resolve_tools_dir()
        py = wq_py()

        # 从 DB 读取回测结果
        db_path = resolve_db_path()
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute(
            "SELECT * FROM backtest_results WHERE region=? AND wave=?",
            (region, wave),
        )
        backtest_results = [dict(r) for r in c.fetchall()]

        if not backtest_results:
            result["error"] = f"No backtest results found: {region}/{wave}"
            conn.close()
            return result

        # 步骤 1：自动 S4 预筛
        if auto_prescreen:
            # 调用 s4-prescreen
            alpha_ids = [bt.get("alpha_id") for bt in backtest_results if bt.get("alpha_id")]
            if alpha_ids:
                # 写入临时文件
                ids_file = os.path.join(REPO_ROOT, "logs", f"_tmp_s4_ids_{wave}.txt")
                with open(ids_file, "w") as f:
                    for aid in alpha_ids:
                        f.write(f"{aid}\n")

                prescreen_cmd = [
                    py,
                    os.path.join(tools_dir, "campaign_intel.py"),
                    "s4-prescreen",
                    "--ids-file", ids_file,
                ]

                logger.info(f"Executing S4 prescreen: {' '.join(prescreen_cmd)}")
                prescreen_proc = subprocess.run(
                    prescreen_cmd,
                    capture_output=True,
                    text=True,
                    timeout=300,
                    cwd=str(REPO_ROOT),
                )

                result["steps"][0]["returncode"] = prescreen_proc.returncode
                result["steps"][0]["stdout_tail"] = (prescreen_proc.stdout or "")[-2000:]
                result["steps"][0]["stderr_tail"] = (prescreen_proc.stderr or "")[-500:]

                # 清理临时文件
                os.remove(ids_file)

        # 步骤 2：自动 walls 诊断
        if auto_walls:
            walls = _diagnose_walls(backtest_results)
            result["steps"][1]["walls"] = walls

        # 步骤 3：自动卡闸辅助腿检索
        if auto_salvage:
            salvage_legs = _retrieve_salvage_legs(region, backtest_results)
            result["steps"][2]["salvage_legs"] = salvage_legs

        # 步骤 4：自动生成评审报告
        if auto_report:
            report = _generate_review_report(backtest_results, result["steps"])
            result["steps"][3]["report"] = report

            # 写回 DB
            c.execute(
                """INSERT OR REPLACE INTO review_results
                   (region, wave, dataset, report, created_at)
                   VALUES (?,?,?,?,?)""",
                (region, wave, dataset, json.dumps(report, ensure_ascii=False),
                 datetime.now().isoformat(timespec="seconds")),
            )
            conn.commit()

        conn.close()

        result["success"] = True
        result["backtest_count"] = len(backtest_results)
        result["message"] = f"Auto review completed: {len(backtest_results)} backtest results reviewed"

    except Exception as e:
        result["error"] = f"Auto review failed: {e}"
        logger.exception("Auto review failed")

    return result


def _diagnose_walls(backtest_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """自动 walls 诊断."""
    walls = {
        "structural": False,
        "robust": False,
        "coverage": False,
        "turnover": False,
        "concentration": False,
        "rn_exposure": False,
    }

    for bt in backtest_results:
        # 检查 RN_EXPOSURE 墙
        rn_sharpe = bt.get("risk_neutralized_sharpe")
        if rn_sharpe is not None and rn_sharpe <= 0 and bt.get("sharpe", 0) >= 1.58:
            walls["rn_exposure"] = True

        # 检查其他墙
        if bt.get("sharpe", 0) < 1.0:
            walls["structural"] = True
        if bt.get("turnover", 0) > 0.7:
            walls["turnover"] = True
        if bt.get("coverage", 0) < 0.5:
            walls["coverage"] = True

    return walls


def _retrieve_salvage_legs(region: str, backtest_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """自动卡闸辅助腿检索."""
    # 从 salvage_pool 检索辅助腿
    db_path = resolve_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute(
        "SELECT value FROM ledger_kv WHERE region=? AND key='salvage_pool'",
        (region,),
    )
    row = c.fetchone()
    conn.close()

    if not row:
        return []

    pool = json.loads(row[0])
    entries = pool.get("entries", [])

    # 根据卡闸维度筛选辅助腿
    salvage_legs = []
    for bt in backtest_results:
        if bt.get("sharpe", 0) >= 1.58:
            continue  # 已过闸，不需要辅助腿

        # 卡 2Y 闸
        if bt.get("two_year_sharpe", 0) < 1.58:
            legs = [e for e in entries if "boost_2y" in e.get("boost_dims", [])]
            salvage_legs.extend(legs)

        # 卡 CW/子宇宙闸
        if bt.get("sub_universe_sharpe", 0) < 0.5:
            legs = [e for e in entries if "boost_cw" in e.get("boost_dims", [])]
            salvage_legs.extend(legs)

        # 卡 tvr 闸
        if bt.get("turnover", 0) > 0.25:
            legs = [e for e in entries if "boost_tvr" in e.get("boost_dims", [])]
            salvage_legs.extend(legs)

    # 去重
    seen = set()
    unique_legs = []
    for leg in salvage_legs:
        leg_id = leg.get("alpha_id")
        if leg_id not in seen:
            seen.add(leg_id)
            unique_legs.append(leg)

    return unique_legs


def _generate_review_report(backtest_results: List[Dict[str, Any]], steps: List[Dict[str, Any]]) -> Dict[str, Any]:
    """自动生成评审报告."""
    total = len(backtest_results)
    passed = len([bt for bt in backtest_results if bt.get("sharpe", 0) >= 1.58 and bt.get("fitness", 0) >= 1.0])
    pass_rate = passed / total if total > 0 else 0

    # 统计 walls
    walls = {}
    for step in steps:
        if step.get("step") == "auto_walls" and "walls" in step:
            walls = step["walls"]
            break

    # 统计 salvage legs
    salvage_legs = []
    for step in steps:
        if step.get("step") == "auto_salvage" and "salvage_legs" in step:
            salvage_legs = step["salvage_legs"]
            break

    return {
        "total": total,
        "passed": passed,
        "pass_rate": round(pass_rate, 4),
        "walls": walls,
        "salvage_legs_count": len(salvage_legs),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }
