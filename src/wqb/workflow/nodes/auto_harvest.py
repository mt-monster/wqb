# -*- coding: utf-8 -*-
"""auto_harvest 节点：收批核对与报告（S3 增强，只读）.

读库里本波（给了 multisim_id 时只取该批）的回测行：
1. auto_harvest：取行
2. auto_link：关联诊断——多少行挂上了 expressions
3. auto_upsert：本节点不写库。平台结果入库走 wqb-db `harvest_multisim_results`，或
   `workflow_auto_harvest(alphas=…)`（先入库、再调本节点出报告）——同一实现，经 CampaignStore 写
4. auto_report：收批报告

2026-09-27 N31：此前第 1、3 步按不存在的列读写（backtest_results 没有 multisim_id / expression /
failed_checks / universe / delay / neut / updated_at），并把刚读出的行 INSERT OR REPLACE 整行重写；
步骤按下标取，auto_upsert=False 时 IndexError——三种调用方式全部报错。现只读，按真实表结构取数。
"""

import logging
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional

from .._common import connect_db_readonly

from wqb.db_conn import connect as db_connect  # 规范工厂（2026-09-20 L1 收口）
logger = logging.getLogger(__name__)

#: 报告里"过闸"的口径（sharpe ≥ 1.58 且 fitness ≥ 1.0，与收批级联的硬闸前两项一致）
_PASS_SHARPE, _PASS_FITNESS = 1.58, 1.0


def run(
    region: str,
    wave: str,
    multisim_id: Optional[str] = None,
    auto_link: bool = True,
    auto_upsert: bool = True,
    auto_report: bool = True,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """收批核对与报告（只读）.

    Args:
        region: 区域代码
        wave: 波次号（原字符串）
        multisim_id: 只取这一批（按回测行 payload_json 里的 multisim_id；经 harvest_multisim_results /
            workflow_auto_harvest 带 multisim_id 入库的行才有这个标记）
        auto_link: 是否给出关联诊断（默认 True）
        auto_upsert: 保留参数；本节点不写库，入库见模块说明
        auto_report: 是否生成收批报告（默认 True）
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
        "steps": [{"step": "auto_harvest", "success": True, "description": "读取本波（或该批）的回测行"}],
    }
    if auto_link:
        result["steps"].append({"step": "auto_link", "success": True,
                                "description": "关联诊断：回测行是否挂上 expressions"})
    if auto_upsert:
        result["steps"].append({"step": "auto_upsert", "success": True,
                                "skipped": "本节点不写库：入库走 wqb-db harvest_multisim_results"
                                           "（或 workflow_auto_harvest 带 alphas），经 CampaignStore 写"})
    if auto_report:
        result["steps"].append({"step": "auto_report", "success": True, "description": "生成收批报告"})

    # 如果是 dry-run，到此为止
    if ctx.get("dry_run"):
        result["success"] = True
        result["dry_run"] = True
        result["note"] = "dry-run：收批核对流程已构建，未读库"
        return result

    sql = ("SELECT b.*, e.id AS linked_expression_id FROM backtest_results b "
           "LEFT JOIN expressions e ON e.id = b.expression_id WHERE b.region=? AND b.wave=?")
    args: List[Any] = [region, str(wave)]
    if multisim_id:
        sql += " AND json_extract(b.payload_json, '$.multisim_id') = ?"
        args.append(str(multisim_id))
    try:
        conn = connect_db_readonly()
    except sqlite3.Error as e:
        result["error"] = f"打不开战役库（只读）：{e}"
        return result
    try:
        conn.row_factory = sqlite3.Row
        rows = [dict(r) for r in conn.execute(sql, args)]
    except sqlite3.Error as e:
        logger.exception("Auto harvest failed")
        result["error"] = f"读回测行失败：{e}"
        return result
    finally:
        conn.close()

    if not rows:
        where = f"{region}/{wave}" + (f" multisim_id={multisim_id}" if multisim_id else "")
        result["error"] = (f"库里没有 {where} 的回测行"
                           + ("（只有经 harvest_multisim_results / workflow_auto_harvest 带 multisim_id "
                              "入库的行才有这个标记）" if multisim_id else ""))
        return result

    _step(result, "auto_harvest")["rows"] = len(rows)
    if auto_link:
        linked = sum(1 for r in rows if r.get("linked_expression_id") is not None)
        _step(result, "auto_link").update(linked_count=linked, unlinked_count=len(rows) - linked)
    if auto_report:
        _step(result, "auto_report")["report"] = _generate_harvest_report(rows)

    result["success"] = True
    result["backtest_count"] = len(rows)
    result["message"] = f"收批核对完成：{len(rows)} 条回测行"
    return result


def _step(result: Dict[str, Any], name: str) -> Dict[str, Any]:
    return next(s for s in result["steps"] if s.get("step") == name)


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

    # 统计过闸率（指标缺失按 0 计：ERROR 行没有指标）
    passed = len([bt for bt in backtest_results
                  if (bt.get("sharpe") or 0) >= _PASS_SHARPE and (bt.get("fitness") or 0) >= _PASS_FITNESS])
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
