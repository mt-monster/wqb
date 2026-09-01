# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
"""harvest_multisim.py — multisim 批次完成后收批工具（系统性通用工具）。

功能：
  1. 拉取 multisim children（get_multisimulation_children）
  2. 对每个 child 拉取完整指标（get_alpha_details）
  3. 按 alpha_id 关联 expressions 表中的 expression_id
  4. 返回结构化结果 [{alpha_id, expression_id, sharpe, fitness, turnover, checks, ...}]
  5. 可选 --auto-upsert 直接写回 backtest_rows 表

用法:
  # 单 multisim 收批
  python tools/harvest_multisim.py --multisim-id 3D0QTR5Dv4NjbjDYx1qyD6b

  # 多 multisim 批量收
  python tools/harvest_multisim.py --multisim-ids A1b2c3 B4d5e6

  # 按 wave 自动发现（从 checkpoint 或 ledger）
  python tools/harvest_multisim.py --wave 53 --region GBR

  # 只拉 IDs 不拉详情（快速模式）
  python tools/harvest_multisim.py --multisim-id X1 --ids-only

  # 自动写回 DB
  python tools/harvest_multisim.py --multisim-id X1 --wave 53 --region GBR --auto-upsert

  # 失败 children 重试
  python tools/harvest_multisim.py --multisim-id X1 --retry-failed

退出码: 0=全部成功, 1=存在失败/错误
运行环境: 使用 MCP venv（`$WQ_PY` 或 world-quant-brain-mcp/.venv），依赖 brain_api。
"""
import argparse
import asyncio
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional


def _mcp_venv_python():
    env = os.environ.get("WQ_PY")
    cands = [env, r"d:\coding\traeCN_project\wqb\world-quant-brain-mcp\.venv\Scripts\python.exe"]
    for c in cands:
        if c and os.path.isfile(c):
            return c
    return sys.executable


def _bootstrap():
    """路径引导：优先 MCP venv 解释器重启，否则把工作区 MCP 包加入 sys.path。"""
    py = _mcp_venv_python()
    if py and os.path.normcase(os.path.abspath(py)) != os.path.normcase(os.path.abspath(sys.executable)):
        os.execv(py, [py] + sys.argv)
    mcp = os.environ.get("WQ_MCP_DIR", r"d:\coding\traeCN_project\wqb\world-quant-brain-mcp")
    sys.path.insert(0, mcp)
    from brain_api import BrainApiClient  # noqa: F401
    return mcp


TERMINAL = {"DONE", "ERROR", "CANCELLED", "FAILED"}


def _shape_url(base, loc):
    if loc.startswith("http"):
        return loc
    if loc.startswith("/"):
        return base + loc
    return f"{base}/simulations/{loc}"


async def fetch_child_status(brain, child_loc: str) -> Dict[str, Any]:
    """拉取单个 child simulation 的状态与 alpha_id。"""
    resp = await brain._request("GET", child_loc)
    if resp.status_code != 200:
        return {"error": f"HTTP {resp.status_code}", "location": child_loc}
    data = resp.json() if resp.text else {}
    err = brain._simulation_error_message(data)
    if not data.get("alpha") and err == "Unknown error":
        err = ""
    return {
        "location": child_loc,
        "status": data.get("status"),
        "alpha_id": data.get("alpha"),
        "error": err,
    }


def _is_composite_expr(code: str) -> bool:
    """判断是否为复合表达式(含 add/subtract/multiply 等组合算子)。"""
    composite_ops = {"add", "subtract", "multiply", "divide"}
    fns = set(re.findall(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", code or ""))
    return bool(fns & composite_ops)


def _extract_two_year_sharpe(is_data: Dict[str, Any]) -> Optional[float]:
    """提取 two_year_sharpe。

    修复 (2026-08-28): 复合表达式(含 add/subtract/multiply/divide)的
    twoYearSharpe 在 metrics 中可能缺失，需从 is.ladder.sharpe 抓最近两年均值。
    与 tools/parse_simresult.py._extract_two_year_sharpe 逻辑保持一致。
    """
    # 1) is.twoYearSharpe 直读
    tys = is_data.get("twoYearSharpe")
    if tys is not None:
        return tys
    # 2) is.metrics.twoYearSharpe
    m = is_data.get("metrics") or {}
    tys = m.get("twoYearSharpe")
    if tys is not None:
        return tys
    # 3) 复合表达式: is.ladder.sharpe 最近两年均值
    ladder = is_data.get("ladder") or {}
    if isinstance(ladder, dict):
        sharpe_list = ladder.get("sharpe") or []
        if isinstance(sharpe_list, list) and len(sharpe_list) >= 2:
            recent = sharpe_list[-2:]
            values = [s.get("value") for s in recent if isinstance(s, dict) and s.get("value") is not None]
            if values:
                return sum(values) / len(values)
    return None


def _extract_is_ladder_sharpe(is_data: Dict[str, Any]) -> Optional[float]:
    """提取 IS_LADDER_SHARPE（提交硬闸之一，2026-08-29 新增字段）。

    优先取平台 checks 里已算好的 IS_LADDER_SHARPE 值（平台口径最可靠）；
    缺失时回退 is.ladder.sharpe 最近两年均值（与 _extract_two_year_sharpe 同源结构）。

    背景：omqEEgd2 提交被此闸拦截（1.46 < 1.58）——此前 DB 无字段可存，
    无法从库内预判，与 prod_correlation 当年同一类问题（2026-08-29 修复）。
    """
    for c in (is_data.get("checks") or []):
        if isinstance(c, dict) and c.get("name") == "IS_LADDER_SHARPE":
            v = c.get("value")
            if v is not None:
                try:
                    return float(v)
                except (TypeError, ValueError):
                    return None
    # fallback：ladder 年度结构最近两年均值
    ladder = is_data.get("ladder") or {}
    if isinstance(ladder, dict):
        sharpe_list = ladder.get("sharpe") or []
        if isinstance(sharpe_list, list) and len(sharpe_list) >= 2:
            recent = sharpe_list[-2:]
            values = [s.get("value") for s in recent if isinstance(s, dict) and s.get("value") is not None]
            if values:
                return sum(values) / len(values)
    return None


async def fetch_alpha_details(brain, alpha_id: str) -> Dict[str, Any]:
    """拉取 alpha 完整指标。"""
    try:
        resp = await brain._request("GET", f"/alphas/{alpha_id}")
        if resp.status_code != 200:
            return {"alpha_id": alpha_id, "error": f"HTTP {resp.status_code}"}
        data = resp.json() if resp.text else {}
        is_ = data.get("is") or {}
        m = is_.get("metrics") or {}
        checks = data.get("checks") or []
        failed_checks = [c.get("name") for c in checks if c.get("result") == "FAIL"]
        return {
            "alpha_id": alpha_id,
            # alphas.status 用本地语义（COMPLETE/UNSUBMITTED）；平台 status 另存 platform_status
            "status": data.get("status"),
            "platform_status": data.get("status"),
            "stage": data.get("stage"),              # IS | OS
            "alpha_type": data.get("type"),          # REGULAR | SUPER
            "date_submitted": data.get("dateSubmitted"),
            "sharpe": is_.get("sharpe") or m.get("sharpe"),
            "fitness": is_.get("fitness") or m.get("fitness"),
            "turnover": is_.get("turnover") or m.get("turnover"),
            "margin": is_.get("margin") or m.get("margin"),
            "two_year_sharpe": _extract_two_year_sharpe(is_),
            "is_ladder_sharpe": _extract_is_ladder_sharpe(is_),
            "sub_universe_sharpe": is_.get("subUniverseSharpe") or m.get("subUniverseSharpe"),
            # 提交硬闸决策字段（PROD/SELF 相关性）。此前从未提取 → alphas 两列恒 NULL（0/952）。
            # 平台 IS 阶段未计算时为 None，属正常。
            "prod_correlation": is_.get("prodCorrelation"),
            "self_correlation": is_.get("selfCorrelation"),
            "checks": checks,
            "failed_checks": failed_checks,
            "expression": data.get("regular", {}).get("code") if isinstance(data.get("regular"), dict) else None,
            "settings": {
                "universe": data.get("settings", {}).get("universe"),
                "delay": data.get("settings", {}).get("delay"),
                "neutralization": data.get("settings", {}).get("neutralization"),
                "decay": data.get("settings", {}).get("decay"),
                "truncation": data.get("settings", {}).get("truncation"),
            },
            "raw": data,
        }
    except Exception as e:
        return {"alpha_id": alpha_id, "error": str(e)}


async def harvest_one_multisim(
    brain,
    multisim_id: str,
    ids_only: bool = False,
    retry_failed: bool = False,
) -> Dict[str, Any]:
    """收批单个 multisim，返回结构化结果。"""
    base = brain.base_url
    loc = _shape_url(base, multisim_id)

    # 1. 拉取 children
    resp = await brain._request("GET", loc)
    if resp.status_code != 200:
        return {"multisim_id": multisim_id, "error": f"HTTP {resp.status_code}"}
    data = resp.json() if resp.text else {}
    children = data.get("children") or []

    if not children:
        return {
            "multisim_id": multisim_id,
            "error": "no children found",
            "child_count": 0,
            "children": [],
        }

    # 2. 拉取每个 child 状态
    child_results = []
    for c in children:
        cloc = _shape_url(base, c if isinstance(c, str) else c.get("location"))
        child = await fetch_child_status(brain, cloc)
        child_results.append(child)

    # 3. 过滤 terminal 状态的 children
    terminal_children = [c for c in child_results if (c.get("status") or "").upper() in TERMINAL]
    error_children = [c for c in child_results if c.get("error")]
    done_children = [c for c in terminal_children if (c.get("status") or "").upper() == "DONE"]

    # 4. 拉取 alpha 详情（除非 ids_only）
    alpha_details = []
    if not ids_only:
        for child in done_children:
            alpha_id = child.get("alpha_id")
            if alpha_id:
                details = await fetch_alpha_details(brain, alpha_id)
                details["child_location"] = child["location"]
                alpha_details.append(details)

    # 5. 失败重试逻辑
    retried = []
    if retry_failed and error_children:
        for child in error_children:
            cloc = child["location"]
            # 重新拉取状态（可能已恢复）
            new_child = await fetch_child_status(brain, cloc)
            if (new_child.get("status") or "").upper() == "DONE" and new_child.get("alpha_id"):
                details = await fetch_alpha_details(brain, new_child["alpha_id"])
                details["child_location"] = cloc
                details["retried"] = True
                alpha_details.append(details)
                retried.append(cloc)

    return {
        "multisim_id": multisim_id,
        "child_count": len(child_results),
        "terminal_count": len(terminal_children),
        "done_count": len(done_children),
        "error_count": len(error_children),
        "retried_count": len(retried),
        "children": child_results,
        "alphas": alpha_details,
        "all_terminal": len(terminal_children) == len(child_results),
    }


def _link_expressions(store, region: str, wave: str, alphas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """关联 expressions 表中的 expression_id。"""
    if not alphas:
        return alphas
    # 拉取本波 expressions
    exprs = store.list_expressions(region, str(wave))
    expr_map = {e.get("alpha_id"): e.get("id") for e in exprs if e.get("alpha_id")}
    code_map = {e.get("expression"): e.get("id") for e in exprs if e.get("expression")}

    for a in alphas:
        alpha_id = a.get("alpha_id")
        code = a.get("expression")
        # 优先按 alpha_id 关联
        if alpha_id and alpha_id in expr_map:
            a["expression_id"] = expr_map[alpha_id]
        # 其次按 expression 代码关联
        elif code and code in code_map:
            a["expression_id"] = code_map[code]
        else:
            a["expression_id"] = None
    return alphas


def _to_backtest_rows(alphas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """将 alpha 详情转换为 backtest_rows 格式。"""
    rows = []
    for a in alphas:
        row = {
            "alpha_id": a.get("alpha_id"),
            "code": a.get("expression"),
            "status": "COMPLETE" if not a.get("error") else "ERROR",
            "sharpe": a.get("sharpe"),
            "fitness": a.get("fitness"),
            "turnover": a.get("turnover"),
            "margin": a.get("margin"),
            "two_year_sharpe": a.get("two_year_sharpe"),
            "is_ladder_sharpe": a.get("is_ladder_sharpe"),
            "sub_universe_sharpe": a.get("sub_universe_sharpe"),
            "failed_checks": a.get("failed_checks"),
            # 透传 PROD/SELF 相关性 → campaign.upsert_backtest_rows 写入 alphas
            "prod_correlation": a.get("prod_correlation"),
            "self_correlation": a.get("self_correlation"),
            # 平台状态/类型/提交时间（审计 P0-2 新增列）
            "platform_status": a.get("platform_status"),
            "stage": a.get("stage"),
            "alpha_type": a.get("alpha_type"),
            "date_submitted": a.get("date_submitted"),
            "universe": a.get("settings", {}).get("universe"),
            "delay": a.get("settings", {}).get("delay"),
            "neut": a.get("settings", {}).get("neutralization"),
        }
        rows.append(row)
    return rows


async def main():
    ap = argparse.ArgumentParser(description="multisim 批次收批工具")
    ap.add_argument("--multisim-id", help="单个 multisim id")
    ap.add_argument("--multisim-ids", nargs="+", help="多个 multisim id")
    ap.add_argument("--wave", help="wave 编号（用于关联 expressions 与自动发现）")
    ap.add_argument("--region", help="区域（用于关联 expressions 与 upsert）")
    ap.add_argument("--ids-only", action="store_true", help="只拉 alpha IDs，不拉详情")
    ap.add_argument("--auto-upsert", action="store_true", help="自动写回 backtest_rows")
    ap.add_argument("--retry-failed", action="store_true", help="重试失败的 children")
    ap.add_argument("--json", dest="json_out", help="结果落盘 JSON 路径")
    a = ap.parse_args()

    if not a.multisim_id and not a.multisim_ids and not (a.wave and a.region):
        print("错误：必须提供 --multisim-id / --multisim-ids 或 --wave + --region")
        sys.exit(1)

    _bootstrap()
    from brain_api import BrainApiClient  # noqa: F402
    brain = BrainApiClient()

    # 收集 multisim ids
    msids = []
    if a.multisim_id:
        msids.append(a.multisim_id)
    if a.multisim_ids:
        msids.extend(a.multisim_ids)

    # TODO: 从 wave/region 自动发现 multisim ids（查 checkpoint 或 ledger）
    if not msids and a.wave and a.region:
        print(f"[warn] 从 wave={a.wave} region={a.region} 自动发现 multisim ids 功能待实现")
        print("请显式提供 --multisim-id 或 --multisim-ids")
        sys.exit(1)

    # 收批
    results = []
    for msid in msids:
        print(f"\n[harvest] {msid} ...")
        r = await harvest_one_multisim(brain, msid, ids_only=a.ids_only, retry_failed=a.retry_failed)
        results.append(r)
        print(f"  children={r['child_count']} terminal={r['terminal_count']} "
              f"done={r['done_count']} error={r['error_count']}")
        if r.get("alphas"):
            for alpha in r["alphas"]:
                mark = "✓" if not alpha.get("error") else "✗"
                print(f"    {mark} {alpha.get('alpha_id')}  sh={alpha.get('sharpe')} "
                      f"fit={alpha.get('fitness')} to={alpha.get('turnover')}")

    # 关联 expressions 并 upsert
    if a.auto_upsert and a.wave and a.region:
        sys.path.insert(0, str(os.path.join(os.path.dirname(__file__), "..", "src")))
        from wqb.store import CampaignStore
        db_path = os.path.join(os.path.dirname(__file__), "..", "data", "wqb.db")
        store = CampaignStore(db_path)
        try:
            for r in results:
                if r.get("alphas"):
                    # 关联 expression_id
                    r["alphas"] = _link_expressions(store, a.region, a.wave, r["alphas"])
                    # 转换为 backtest_rows 并 upsert
                    rows = _to_backtest_rows(r["alphas"])
                    n = store.upsert_backtest_rows(a.region, str(a.wave), rows)
                    print(f"  [upsert] {n} rows → backtest_results (region={a.region} wave={a.wave})")

            # --- 触发 salvage_pool（全 RED 时自动分层） ---
            try:
                # 导入 wqb_db_mcp 中的 salvage 函数
                sys.path.insert(0, str(os.path.dirname(__file__)))
                from wqb_db_mcp import _salvage_to_pool, _get_ledger_raw

                # 汇总所有 alphas 检查是否全 RED
                all_alphas = []
                for r in results:
                    if r.get("alphas"):
                        all_alphas.extend(r["alphas"])

                if all_alphas:
                    # 检查是否全 RED（无 GREEN）
                    green_count = sum(1 for a in all_alphas if a.get("sharpe") and a.get("sharpe") >= 1.58 and a.get("fitness") and a.get("fitness") >= 1.0)
                    if green_count == 0:
                        # 全 RED，触发 salvage
                        _salvage_to_pool(a.region, int(a.wave), all_alphas)
                        pool = _get_ledger_raw(a.region, "salvage_pool") or {"entries": []}
                        print(f"  [salvage] all RED, pool entries: {len(pool.get('entries', []))}")
            except Exception as e:
                print(f"  [salvage] skipped: {e}")
        finally:
            store.close()

    # 输出 JSON
    if a.json_out:
        os.makedirs(os.path.dirname(a.json_out) or ".", exist_ok=True)
        json.dump(results, open(a.json_out, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
        print(f"\n[out] {a.json_out}")

    # 退出码
    all_ok = all(r.get("all_terminal") and not r.get("error") for r in results)
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    asyncio.run(main())
