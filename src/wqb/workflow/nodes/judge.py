# -*- coding: utf-8 -*-
"""judge 节点：Alpha 六步闸门判定（真实平台调用版）.

替代 brain-alpha-judge 的 CLI 调用与配置管理。
S4 评审链单次封装：平台硬检查 → 相关性(prod/self) → 归因(逐年) →
稳健性闸 → trend score → 综合判定。

注意职责边界：本节点为评审参考，产出 READY/REVIEW/BLOCK 三态仅供人工参考；
最终提交判定唯一权威 = tools/submit_verdict.py（403 盲区检测），勿以本节点结果直接提交。

通过 brain_client 单例真实调用 BRAIN 平台（异步方法用 asyncio 包装）。
凭据解析顺序与 MCP 服务一致（world-quant-brain-mcp/.env 等）；
无凭据/网络失败时对应 gate 标记为 unavailable 并降级，不崩溃。
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..mcp_check import require_mcp_tools

logger = logging.getLogger(__name__)

# 硬闸阈值（与战役口径一致）
_SHARPE_MIN = 1.58
_FITNESS_MIN = 1.0
_2Y_MIN = 1.58
_PROD_MAX = 0.7
_SELF_MAX = 0.7


def _get_brain_client():
    """延迟导入 brain_client 单例（避免循环依赖与启动开销）."""
    import sys
    import os
    mcp_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "world-quant-brain-mcp")
    mcp_dir = os.path.abspath(mcp_dir)
    if mcp_dir not in sys.path:
        sys.path.insert(0, mcp_dir)
    from brain_api import brain_client  # noqa
    return brain_client


def _run_async(coro):
    """在同步节点里执行异步 brain_client 方法（无事件循环时新建，有则用线程）。"""
    try:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(coro)
            finally:
                loop.close()
        # 已在运行中的事件循环（如 MCP async 工具上下文）：用独立线程跑
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            return pool.submit(lambda: asyncio.run(coro)).result()
    except Exception as e:
        logger.warning(f"async brain call failed: {e}")
        return {"__error__": str(e)}


@require_mcp_tools("judge")
def run(
    alpha_id: str,
    trend_window_days: int = 365,
    llm_enabled: bool = True,
    confirm_submit: bool = False,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """执行 Alpha 六步闸门判定（真实平台数据）.

    Args:
        alpha_id: Alpha ID
        trend_window_days: trend score 窗口天数
        llm_enabled: 是否启用 LLM 决策层（当前为规则层占位，无 LLM key 时自动跳过）
        confirm_submit: 是否确认提交
        _context: 执行上下文

    Returns:
        判定结果字典（含各 gate 明细与最终 verdict）
    """
    ctx = _context or {}
    store = ctx.get("store")

    # dry-run：构建到六步闸判定计划即停，不触碰 network / 不写库
    # （2026-09-01 缺陷 A 修复：此前 dry_run 仍真实调用 get_alpha_details 等）。
    if ctx.get("dry_run"):
        return {
            "alpha_id": alpha_id,
            "success": True,
            "dry_run": True,
            "verdict": None,
            "gates": [],
            "steps": [{
                "step": "dry_run",
                "success": True,
                "message": (
                    "Would run six-gate judge: platform_check → correlation(prod/self) "
                    "→ yearly_attribution → trend_score → final verdict"
                ),
            }],
            "plan": {
                "alpha_id": alpha_id,
                "trend_window_days": trend_window_days,
                "confirm_submit": confirm_submit,
            },
        }

    result: Dict[str, Any] = {
        "alpha_id": alpha_id,
        "gates": [],
        "verdict": None,
        "success": False,
    }

    client = _get_brain_client()

    # ---- Gate 1: 平台硬检查（get_alpha_details → checks.fail 必须为空 + 数值硬闸） ----
    details = _run_async(client.get_alpha_details(alpha_id))
    gate1 = _eval_platform_check(details)
    result["gates"].append(gate1)
    if not gate1.get("pass"):
        result["verdict"] = "BLOCK"
        result["reason"] = gate1.get("reason", "Platform hard check failed")
        return _finalize(result, store, alpha_id)

    # ---- Gate 2: 相关性闸（prod + self，逐个顺序避免限流） ----
    corr = _run_async(client.check_correlation(alpha_id, correlation_type="both", threshold=_PROD_MAX))
    gate2 = _eval_correlation(corr)
    result["gates"].append(gate2)
    prod_corr = gate2.get("prod_correlation")
    if prod_corr is not None and prod_corr >= _PROD_MAX:
        result["verdict"] = "BLOCK"
        result["reason"] = f"prod_correlation {prod_corr:.3f} >= {_PROD_MAX}"
        result["mode_b_required"] = True
        result["mode_b_action"] = "换字段组合/换概念（禁止调权重）"
        return _finalize(result, store, alpha_id)

    # ---- Gate 3: 归因（逐年稳健性，识别弱年/负年） ----
    yearly = _run_async(client.get_alpha_yearly_stats(alpha_id))
    gate3 = _eval_yearly(yearly)
    result["gates"].append(gate3)

    # ---- Gate 4: trend score 上下文（可选，失败降级） ----
    gate4 = _eval_trend_score(client, alpha_id, trend_window_days)
    result["gates"].append(gate4)

    # ---- Gate 5: 综合判定（规则层；LLM 层无 key 时跳过） ----
    final_verdict = _compute_final_verdict(result["gates"])
    result["verdict"] = final_verdict
    result["success"] = final_verdict in ("READY", "REVIEW")

    # 确认提交
    if confirm_submit and final_verdict == "READY":
        submit = _run_async(client.submit_alpha(alpha_id))
        result["submit"] = submit

    return _finalize(result, store, alpha_id)


def _finalize(result: Dict[str, Any], store, alpha_id: str) -> Dict[str, Any]:
    """保存判定记录到台账并返回."""
    if store:
        try:
            store.upsert_ledger("WORKFLOW", f"judge_{alpha_id}", {
                "judged_at": datetime.now().isoformat(),
                "verdict": result.get("verdict"),
                "gates": result.get("gates"),
            })
        except Exception as e:
            logger.warning(f"Failed to save judge record: {e}")
    return result


def _eval_platform_check(details: Dict[str, Any]) -> Dict[str, Any]:
    """评估平台硬检查：checks.fail 为空 + sharpe/fitness/2y 数值硬闸."""
    if not isinstance(details, dict) or details.get("__error__"):
        return {"gate": "platform_check", "pass": False, "unavailable": True,
                "reason": f"get_alpha_details unavailable: {details.get('__error__', 'unknown')}"}

    # brain_client 返回可能是 {"result": {...}} 或直接 {...}
    d = details.get("result", details) if isinstance(details, dict) else {}
    isd = d.get("is", d) if isinstance(d, dict) else {}
    metrics = isd if isinstance(isd, dict) else {}

    sharpe = metrics.get("sharpe")
    fitness = metrics.get("fitness")
    two_year = metrics.get("two_year_sharpe") or metrics.get("twoYearSharpe")

    # checks.fail 列表
    checks = isd.get("checks") if isinstance(isd, dict) else None
    fail_names: List[str] = []
    if isinstance(checks, list):
        for c in checks:
            if isinstance(c, dict) and c.get("result") == "FAIL":
                fail_names.append(c.get("name"))
    elif isinstance(checks, dict):
        for c in checks.get("fail", []) or []:
            if isinstance(c, dict):
                fail_names.append(c.get("name"))

    reasons = []
    if fail_names:
        reasons.append(f"checks.fail={fail_names}")
    if sharpe is not None and sharpe < _SHARPE_MIN:
        reasons.append(f"sharpe {sharpe:.2f} < {_SHARPE_MIN}")
    if fitness is not None and fitness < _FITNESS_MIN:
        reasons.append(f"fitness {fitness:.2f} < {_FITNESS_MIN}")
    if two_year is not None and two_year < _2Y_MIN:
        reasons.append(f"2y_sharpe {two_year:.2f} < {_2Y_MIN}")

    return {
        "gate": "platform_check",
        "pass": len(reasons) == 0,
        "sharpe": sharpe,
        "fitness": fitness,
        "two_year_sharpe": two_year,
        "fail_checks": fail_names,
        "reason": "; ".join(reasons) if reasons else None,
    }


def _eval_correlation(corr: Dict[str, Any]) -> Dict[str, Any]:
    """评估相关性闸：prod/self 双双 < 阈值."""
    if not isinstance(corr, dict) or corr.get("__error__"):
        return {"gate": "correlation", "pass": True, "unavailable": True,
                "reason": f"check_correlation unavailable: {corr.get('__error__', 'unknown')}"}

    d = corr.get("result", corr)
    checks = d.get("checks", {}) if isinstance(d, dict) else {}
    prod = checks.get("production", {}) if isinstance(checks, dict) else {}
    selfc = checks.get("self", {}) if isinstance(checks, dict) else {}

    prod_max = prod.get("max_correlation") if isinstance(prod, dict) else None
    self_max = selfc.get("max_correlation") if isinstance(selfc, dict) else None

    reasons = []
    if prod_max is not None and prod_max >= _PROD_MAX:
        reasons.append(f"prod {prod_max:.3f} >= {_PROD_MAX}")
    if self_max is not None and self_max >= _SELF_MAX:
        reasons.append(f"self {self_max:.3f} >= {_SELF_MAX}")

    return {
        "gate": "correlation",
        "pass": len(reasons) == 0,
        "prod_correlation": prod_max,
        "self_correlation": self_max,
        "reason": "; ".join(reasons) if reasons else None,
    }


def _eval_yearly(yearly: Dict[str, Any]) -> Dict[str, Any]:
    """评估逐年稳健性：统计正年/负年/弱年."""
    if not isinstance(yearly, dict) or yearly.get("__error__"):
        return {"gate": "yearly_attribution", "pass": True, "unavailable": True,
                "reason": f"get_alpha_yearly_stats unavailable: {yearly.get('__error__', 'unknown')}"}

    d = yearly.get("result", yearly)
    records = d.get("records", []) if isinstance(d, dict) else []

    years = []
    neg_years = []
    weak_years = []  # sharpe < 0.5
    for r in records:
        if not isinstance(r, dict):
            continue
        yr = r.get("year")
        sh = r.get("sharpe")
        if yr is None:
            continue
        years.append({"year": yr, "sharpe": sh})
        if isinstance(sh, (int, float)):
            if sh < 0:
                neg_years.append(yr)
            elif sh < 0.5:
                weak_years.append(yr)

    total = len(years)
    pos = total - len(neg_years)
    return {
        "gate": "yearly_attribution",
        "pass": True,  # 归因是信息性 gate，不硬拦
        "total_years": total,
        "positive_years": pos,
        "negative_years": neg_years,
        "weak_years": weak_years,
        "all_positive": len(neg_years) == 0 and total > 0,
        "years": years,
    }


def _eval_trend_score(client, alpha_id: str, window_days: int) -> Dict[str, Any]:
    """评估 value-factor trend score 上下文（失败降级）."""
    try:
        from datetime import datetime, timedelta
        end = datetime.now()
        start = end - timedelta(days=window_days)
        ts = _run_async(client.value_factor_trendScore(
            start.strftime("%Y-%m-%dT00:00:00Z"),
            end.strftime("%Y-%m-%dT00:00:00Z"),
        ))
        if isinstance(ts, dict) and ts.get("__error__"):
            return {"gate": "trend_score", "pass": True, "unavailable": True,
                    "reason": ts.get("__error__")}
        d = ts.get("result", ts) if isinstance(ts, dict) else {}
        return {
            "gate": "trend_score",
            "pass": True,
            "window_days": window_days,
            "diversity_score": d.get("diversity_score"),
            "s_a": d.get("S_A"),
            "s_p": d.get("S_P"),
            "s_h": d.get("S_H"),
        }
    except Exception as e:
        return {"gate": "trend_score", "pass": True, "unavailable": True, "reason": str(e)}


def _compute_final_verdict(gates: List[Dict[str, Any]]) -> str:
    """计算最终判定（规则层）.

    - 任一硬 gate（platform/correlation）失败 → BLOCK
    - 平台硬闸全过但有负年 → REVIEW（提示弱年风险）
    - 全过且逐年全正 → READY
    """
    hard_fail = False
    has_negative_year = False
    for g in gates:
        name = g.get("gate")
        if name in ("platform_check", "correlation") and not g.get("pass", False):
            hard_fail = True
        if name == "yearly_attribution" and g.get("negative_years"):
            has_negative_year = True

    if hard_fail:
        return "BLOCK"
    if has_negative_year:
        return "REVIEW"
    return "READY"
