# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _pyenv  # noqa: E402  跨平台解释器/MCP 目录解析（tools/_pyenv.py；2026-09-29 替换各脚本抄写的 Windows 盘符兜底）
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
    return _pyenv.venv_python()


def _bootstrap():
    """路径引导：非 MCP venv 解释器时 re-exec 到 venv；把 MCP 目录与 src 加入 sys.path（跨平台）。"""
    _pyenv.reexec_under_venv()
    _pyenv.bootstrap_paths()
    from brain_api import BrainApiClient  # noqa: F401
    return str(_pyenv.mcp_dir())


TERMINAL = {"DONE", "COMPLETE", "ERROR", "CANCELLED", "FAILED"}
SUCCESS_STATUS = {"DONE", "COMPLETE"}


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
    status = (data.get("status") or "").upper()
    # 平台对成功 child 会回显状态字符串（如 "COMPLETE"）当作 message，
    # 不能当错误；已拿到 alpha 或状态为成功态则清空。
    if not data.get("alpha") and err == "Unknown error":
        err = ""
    if data.get("alpha") or status in SUCCESS_STATUS:
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


def _pick_checks(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """从 alpha 详情中提取 checks 列表。

    平台返回的 checks 可能在多个位置，依端点不同而异。**2026-09-19 实测更正**：
    真实位置是**顶层 `is.checks`**（alpha 详情顶层键含 `is`，checks 在其内），
    而非 `data.checks` / `data.raw.checks` / `data.raw.is.checks`。
    此前的路径全部落空 → 本函数恒返回 `[]` → 所有 checks 派生列采集不到
    （实测：`alphas.cluster_test` 0/4,926、`concentrated_weight` 0/4,926，
    而直接读 `is.*` 的列正常：`two_year_sharpe` 86.1%）。
    证据：IND/QPGbAOn5 的 `is.checks` 含 `{name: CLUSTER_TEST, result: PASS, limit: 1, value: 2.59}`。
    """
    # 1) 顶层 is.checks（2026-09-19 实测的真实位置，放最前）
    is_top = data.get("is") or {}
    checks = is_top.get("checks")
    if isinstance(checks, list) and checks:
        return checks
    # 2) 顶层 checks（部分瘦身端点会平铺出来）
    checks = data.get("checks")
    if isinstance(checks, list) and checks:
        return checks
    # 3) raw.checks（历史端点嵌套）
    raw = data.get("raw") or {}
    checks = raw.get("checks")
    if isinstance(checks, list) and checks:
        return checks
    # 4) raw.is.checks（再嵌套一层）
    is_raw = raw.get("is") or {}
    checks = is_raw.get("checks")
    if isinstance(checks, list) and checks:
        return checks
    return []


def _ra_failed_names(checks: List[Dict[str, Any]]) -> Optional[List[str]]:
    """RA 资格门失败项名，口径取 wqb.config（唯一定义，R3）；拿不到 wqb 包时返回 None（入库时按 failed_checks 回落）。"""
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
    if src not in sys.path:
        sys.path.insert(0, src)
    try:
        from wqb.config import compute_webdata_failed_counts
    except ImportError:
        return None
    return compute_webdata_failed_counts(checks)["ra_failed_names"]


def _extract_check_value(checks: List[Dict[str, Any]], name: str) -> Optional[float]:
    """从 checks 列表中提取指定硬闸的 value。"""
    for c in checks:
        if isinstance(c, dict) and c.get("name") == name:
            v = c.get("value")
            if v is not None:
                try:
                    return float(v)
                except (TypeError, ValueError):
                    return None
    return None


def _extract_two_year_sharpe(is_data: Dict[str, Any], checks: List[Dict[str, Any]] = None) -> Optional[float]:
    """提取 two_year_sharpe。

    修复 (2026-08-28): 复合表达式(含 add/subtract/multiply/divide)的
    twoYearSharpe 在 metrics 中可能缺失，需从 is.ladder.sharpe 抓最近两年均值。
    与 tools/parse_simresult.py._extract_two_year_sharpe 逻辑保持一致。

    增强 (2026-09-02): 优先从 checks 里读 LOW_2Y_SHARPE 的 value（平台口径最可靠）。
    """
    # 0) checks 里 LOW_2Y_SHARPE（平台已算好的值，最可靠）
    if checks:
        v = _extract_check_value(checks, "LOW_2Y_SHARPE")
        if v is not None:
            return v
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


def _extract_is_ladder_sharpe(is_data: Dict[str, Any], checks: List[Dict[str, Any]] = None) -> Optional[float]:
    """提取 IS_LADDER_SHARPE（提交硬闸之一，2026-08-29 新增字段）。

    优先取平台 checks 里已算好的 IS_LADDER_SHARPE 值（平台口径最可靠）；
    缺失时回退 is.ladder.sharpe 最近两年均值（与 _extract_two_year_sharpe 同源结构）。

    背景：omqEEgd2 提交被此闸拦截（1.46 < 1.58）——此前 DB 无字段可存，
    无法从库内预判，与 prod_correlation 当年同一类问题（2026-08-29 修复）。
    """
    # 0) checks 参数传入（从 _pick_checks 统一提取）
    if checks:
        v = _extract_check_value(checks, "IS_LADDER_SHARPE")
        if v is not None:
            return v
    # 1) is_data.checks 直读
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
        # 统一从 _pick_checks 提取 checks（可能在顶层/raw/raw.is 三层嵌套）
        data_with_raw = dict(data)
        data_with_raw["raw"] = data  # 自引用，让 _pick_checks 能查到 raw.checks
        checks = _pick_checks(data_with_raw)
        failed_checks = [c.get("name") for c in checks if c.get("result") == "FAIL"]
        ra_failed_checks = _ra_failed_names(checks)   # 2026-09-28：只含 RA 项，入 backtest_results 同名列
        # 从 checks 提取全硬闸值（2026-09-02 优化点②：收割即带全闸画像）
        two_year = _extract_two_year_sharpe(is_, checks)
        is_ladder = _extract_is_ladder_sharpe(is_, checks)
        sub_universe = is_.get("subUniverseSharpe") or m.get("subUniverseSharpe")
        if sub_universe is None:
            sub_universe = _extract_check_value(checks, "LOW_SUB_UNIVERSE_SHARPE")
        prod_corr = is_.get("prodCorrelation")
        if prod_corr is None:
            prod_corr = _extract_check_value(checks, "PROD_CORRELATION")
        self_corr = is_.get("selfCorrelation")
        if self_corr is None:
            self_corr = _extract_check_value(checks, "SELF_CORRELATION")
        concentrated_weight = _extract_check_value(checks, "CONCENTRATED_WEIGHT")
        cluster_test = _extract_check_value(checks, "CLUSTER_TEST")
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
            "returns": is_.get("returns") or m.get("returns"),
            "drawdown": is_.get("drawdown") or m.get("drawdown"),
            # 持仓广度 / 规模字段（is 优先，非 None 即止；0 不能被 or 吞成 None）
            "long_count": is_.get("longCount") if is_.get("longCount") is not None else m.get("longCount"),
            "short_count": is_.get("shortCount") if is_.get("shortCount") is not None else m.get("shortCount"),
            "pnl": is_.get("pnl") if is_.get("pnl") is not None else m.get("pnl"),
            "book_size": is_.get("bookSize") if is_.get("bookSize") is not None else m.get("bookSize"),
            "two_year_sharpe": two_year,
            "is_ladder_sharpe": is_ladder,
            "sub_universe_sharpe": sub_universe,
            "prod_correlation": prod_corr,
            "self_correlation": self_corr,
            "concentrated_weight": concentrated_weight,
            "cluster_test": cluster_test,
            "checks": checks,
            "failed_checks": failed_checks,
            "ra_failed_checks": ra_failed_checks,
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

    # 1) 拉取 children —— 带重试（2026-09-28 实证）
    #
    # ⚠ 关键经验：`GET /simulations/{multisim_id}` 在**并发读同一 multisim 时返回 404**，
    # 而不是 409/423。实证：pipeline（batch_track）正在轮询这批 multisim 的同一时刻
    # 另起本 CLI 收批，21 个 ID 里 20 个报 HTTP 404；等 pipeline 结束后用**同样的 ID、
    # 同样的拼法**重跑，全部 200（含当时被误判为"孤儿批"的那只）。直连复现同样 200，
    # 说明 URL 构造无误，404 是平台侧的瞬态并发假象。
    # 此前本函数零重试 → 直接把瞬态 404 当成"该批不存在"，配合上层 `--auto-upsert`
    # 会静默丢整批数据（本次差点丢 160/168 条）。
    # 故：404 / 5xx / 异常一律按可重试处理（4 次，2s·4s·8s 退避），
    # 只有 4 次后仍失败才判错，并在 message 里注明"可能是并发抢占，建议 pipeline 结束后重跑"。
    resp = None
    last_err = None
    _RETRY_STATUS = {404, 429, 500, 502, 503, 504}
    for _attempt in range(4):
        try:
            resp = await brain._request("GET", loc)
        except Exception as e:  # 连接瞬断同样可重试
            last_err = f"exc: {e}"
            resp = None
        if resp is not None and resp.status_code == 200:
            break
        code = getattr(resp, "status_code", None)
        last_err = f"HTTP {code}" if code else (last_err or "no response")
        if code is not None and code not in _RETRY_STATUS:
            break  # 401/403 等是确定性失败，重试无益
        if _attempt < 3:
            await asyncio.sleep(2 ** (_attempt + 1))

    if resp is None or resp.status_code != 200:
        hint = ""
        if (getattr(resp, "status_code", None) == 404 or "404" in str(last_err)):
            hint = "（404 在并发读同一 multisim 时为瞬态假象；建议 pipeline 进程结束后重跑本批）"
        return {"multisim_id": multisim_id, "error": f"{last_err}{hint}", "transient_404": "404" in str(last_err)}

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
    done_children = [c for c in terminal_children
                     if (c.get("status") or "").upper() in SUCCESS_STATUS]

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
            if (new_child.get("status") or "").upper() in SUCCESS_STATUS and new_child.get("alpha_id"):
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
            "ra_failed_checks": a.get("ra_failed_checks"),
            # 透传 PROD/SELF 相关性 → campaign.upsert_backtest_rows 写入 alphas
            "prod_correlation": a.get("prod_correlation"),
            "self_correlation": a.get("self_correlation"),
            # 2026-09-18（设计文档 §2.2 改动#5）：补齐与 MCP 路径一致的全指标
            "risk_neutralized_sharpe": a.get("risk_neutralized_sharpe"),
            "returns": a.get("returns"),
            "drawdown": a.get("drawdown"),
            "long_count": a.get("long_count"),
            "short_count": a.get("short_count"),
            "pnl": a.get("pnl"),
            "book_size": a.get("book_size"),
            # 2026-09-02 优化点②：全硬闸画像入库
            "concentrated_weight": a.get("concentrated_weight"),
            "cluster_test": a.get("cluster_test"),
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
    ap.add_argument("--no-queue", action="store_true",
                    help="关闭「过闸候选自动入队 submit_ready」（默认开启，随 --auto-upsert）")
    ap.add_argument("--retry-failed", action="store_true", help="重试失败的 children")
    ap.add_argument("--json", dest="json_out", help="结果落盘 JSON 路径")
    a = ap.parse_args()

    if not a.multisim_id and not a.multisim_ids and not (a.wave and a.region):
        print("错误：必须提供 --multisim-id / --multisim-ids 或 --wave + --region")
        sys.exit(1)

    _bootstrap()
    from brain_api import BrainApiClient  # noqa: F402
    brain = BrainApiClient()
    await brain.ensure_authenticated()

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
        print(f"  children={r.get('child_count', 0)} terminal={r.get('terminal_count', 0)} "
              f"done={r.get('done_count', 0)} error={r.get('error_count', 0)}"
              + (f" [err] {r['error']}" if r.get("error") else ""))
        if r.get("alphas"):
            for alpha in r["alphas"]:
                mark = "✓" if not alpha.get("error") else "✗"
                # 2026-09-02 优化点②：收割即显示全闸画像
                tys = alpha.get('two_year_sharpe')
                prod = alpha.get('prod_correlation')
                tys_str = f"{tys:.2f}" if tys is not None else "N/A"
                prod_str = f"{prod:.2f}" if prod is not None else "N/A"
                print(f"    {mark} {alpha.get('alpha_id')}  sh={alpha.get('sharpe')} "
                      f"fit={alpha.get('fitness')} to={alpha.get('turnover')} "
                      f"2Y={tys_str} prod={prod_str}")

    # 关联 expressions 并 upsert
    if a.auto_upsert and a.wave and a.region:
        sys.path.insert(0, str(os.path.join(os.path.dirname(__file__), "..", "src")))
        from wqb.store import CampaignStore
        # L3 写库互斥（2026-09-20）：收批批量 upsert 排队（短锁，只包写库段）
        from wqb.db_write_lock import write_lock as _wlock
        db_path = os.path.join(os.path.dirname(__file__), "..", "data", "wqb.db")
        store = CampaignStore(db_path)
        try:
          with _wlock(tag="dbwrite_harvest", ttl_sec=600, wait_timeout=120):
            for r in results:
                if r.get("alphas"):
                    # 关联 expression_id
                    r["alphas"] = _link_expressions(store, a.region, a.wave, r["alphas"])
                    # 转换为 backtest_rows 并 upsert
                    rows = _to_backtest_rows(r["alphas"])
                    n = store.upsert_backtest_rows(a.region, str(a.wave), rows)
                    print(f"  [upsert] {n} rows → backtest_results (region={a.region} wave={a.wave})")

                    # --- 自动入队：把本轮过闸候选写入 submit_ready（2026-09-20）---
                    # 解决"回测找到可提交项但不当天提交就遗忘"。阈值用提交层口径，
                    # 未过闸者会被标 DEAD 自动排除，故可直接全量喂入。
                    if not a.no_queue:
                        try:
                            sys.path.insert(0, str(os.path.join(
                                os.path.dirname(__file__), "..", "src")))
                            from wqb.store.submit_queue import enqueue_from_alphas
                            nq = enqueue_from_alphas(
                                region=a.region, min_sharpe=1.58, min_fitness=1.0,
                                note=f"auto-enqueue wave={a.wave}")
                            print(f"  [queue] {nq} 条过闸候选 → submit_ready")
                        except Exception as e:  # 队列记账失败绝不阻断收批
                            print(f"  [queue] 入队跳过：{e}")
                    # 2026-09-18（设计文档 §2.2 改动#5）：相关性来源标记。
                    # 2026-09-28 N35：upsert_backtest_rows 写相关性时已一并记 prod_corr_source=platform_sync
                    # 与 corr_checked_at（行里没带就不动已有值），这里的补写通常是空操作，留作兜底。
                    for row in rows:
                        if row.get("alpha_id") and (
                            row.get("prod_correlation") is not None
                            or row.get("self_correlation") is not None
                        ):
                            try:
                                store.persist_correlation(
                                    alpha_id=row["alpha_id"],
                                    prod=row.get("prod_correlation"),
                                    self_=row.get("self_correlation"),
                                    source="platform_sync",
                                )
                            except Exception:
                                pass

            # --- 触发 salvage_pool（全 RED 时自动分层） ---
            try:
                # 导入 wqb_db_mcp 中的 salvage 函数（模块在仓库根，非 tools/）
                sys.path.insert(0, str(os.path.join(os.path.dirname(__file__), "..")))
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
                        # 2026-09-28 修：原先强转 int(a.wave)，而 SOP 全链路的波号是
                        # **字符串**（支持 `97` 与 `s2_<ds>_d1` 两种形态）→ 传
                        # `s2_fundamental17_d1` 时抛 `invalid literal for int()`，
                        # salvage 步骤被 except 吞成 `skipped`，整波残值静默不入池。
                        # `_salvage_to_pool` 的 wave_number 声明为 Any 且仅作存档字段，直传字符串即可。
                        _salvage_to_pool(a.region, a.wave, all_alphas)
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
