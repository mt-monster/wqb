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

# Mode B 资格线（2026-09-01 明令，Dry-Run 2.0 优化：从 thresholds.json + ledger_kv 读取）
_MODE_B_QUALIFICATION_DEFAULT = {"sharpe_min": 1.25, "fitness_min": 0.8}


from .._common import (
    get_brain_client as _get_brain_client,
    persist_workflow_record,
    run_async as _run_async,
)


@require_mcp_tools("judge")
def run(
    alpha_id: str,
    trend_window_days: int = 365,
    llm_enabled: bool = True,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """执行 Alpha 六步闸门判定（真实平台数据）——**只判定，不提交**。

    2026-09-05 收口：删除「确认后直接提交」分支。brain-alpha-judge 已于
    2026-08-31 自我弃用最终判定权，提交判定唯一权威 = tools/submit_verdict.py
    （MCP: submit_verdict）。本节点原先的提交路径会绕过 submit_verdict、绕过
    robustness 必经闸、绕过 ra-pipeline 步 8 的用户确认，属越权路径。提交一律走
    submit_alpha 节点（MCP: workflow_submit_alpha），且需用户明确确认。

    success 语义（2026-09-05 修正）：表示「判定是否跑完」，不是「结论好不好」。
    此前按 verdict 是否 READY/REVIEW 取值，会让正常产出的 BLOCK 结论被
    execute_chain 当作节点执行失败而停链。

    Args:
        alpha_id: Alpha ID
        trend_window_days: trend score 窗口天数
        llm_enabled: 是否启用 LLM 决策层（当前为规则层占位，无 LLM key 时自动跳过）
        _context: 执行上下文

    Returns:
        判定结果字典（含各 gate 明细与最终 verdict）
    """
    ctx = _context or {}
    store = ctx.get("store")

    # dry-run：构建到六步闸判定计划即停，不触碰 network / 不写库
    # （2026-09-01 缺陷 A 修复：此前 dry_run 仍真实调用 get_alpha_details 等）。
    if ctx.get("dry_run"):
        # 无子进程可构建 —— 干跑给出「会发哪些平台请求 + 用哪些阈值判」，
        # 并顺带验证 brain_client 可导入（零网络）。
        client_ok, client_err = True, None
        try:
            _get_brain_client()
        except Exception as e:  # pragma: no cover - 环境相关
            client_ok, client_err = False, str(e)
        return {
            "alpha_id": alpha_id,
            "success": True,
            "dry_run": True,
            "note": "dry-run：请求计划已构建，未调用平台",
            "verdict": None,
            "gates": [],
            "steps": [{
                # 只反映「当前解释器」能否导入 brain_client；节点真实运行在 MCP venv 里，
                # 干跑解释器缺依赖属提示而非阻断，故记 warning 不记 error。
                "step": "resolve_client",
                "success": client_ok,
                "warning": client_err,
            }],
            "plan": {
                "alpha_id": alpha_id,
                "trend_window_days": trend_window_days,
                "calls": [
                    "get_alpha_details(alpha_id)",
                    f"check_correlation(alpha_id, type=both, threshold={_PROD_MAX})",
                    "get_alpha_yearly_stats(alpha_id)",
                    f"value_factor_trendScore(alpha_id, window={trend_window_days}d)",
                ],
                "gates": [
                    f"G1 平台硬检查 sharpe>={_SHARPE_MIN} fitness>={_FITNESS_MIN}（Mode B 资格线按区域覆盖）",
                    f"G2 相关性 prod<{_PROD_MAX} self<{_SELF_MAX}",
                    "G3 逐年归因（弱年/负年）",
                    "G4 trend score（失败降级，不阻断）",
                    "G5 综合判定 → READY / REVIEW / BLOCK",
                ],
                "note": "judge 不提交；最终判定走 submit_verdict，提交走 workflow_submit_alpha（需用户确认）",
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
    if isinstance(details, dict) and details.get("__error__"):
        # 取不到平台详情 = 判定没跑起来（真失败），区别于「跑完了但结论是 BLOCK」
        result["reason"] = f"get_alpha_details failed: {details['__error__']}"
        result["error"] = result["reason"]
        return _finalize(result, store, alpha_id)

    # 2026-09-04 方案 A 修复：region 从 alpha 详情取（原硬编码 region="KOR" 导致
    # EUR/IND/USA 等区域的 judge 全读 KOR 的 1.25/0.8 资格线，区域特性错配）。
    alpha_region = _extract_region(details) or "KOR"
    mode_b_qual = _load_mode_b_qualification(store, region=alpha_region)

    gate1 = _eval_platform_check(details, mode_b_qual=mode_b_qual)
    result["gates"].append(gate1)
    if not gate1.get("pass"):
        result["verdict"] = "BLOCK"
        result["reason"] = gate1.get("reason", "Platform hard check failed")
        result["success"] = True  # 判定跑完了，结论是 BLOCK
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
        result["success"] = True  # 判定跑完了，结论是 BLOCK
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
    result["success"] = True  # 判定跑完即成功；结论看 verdict

    # 提交路径已移除（2026-09-05）：judge 不是提交判定权威，也不执行提交。
    # READY 只是评审参考——最终判定走 submit_verdict，提交走 workflow_submit_alpha
    # 且必须有用户明确确认（ra-pipeline 步 8）。
    result["next_step"] = (
        "submit_verdict(alpha_id) 判定 → 用户确认 → workflow_submit_alpha"
        if final_verdict == "READY" else "回步 7（S4）Mode B 改进"
    )

    return _finalize(result, store, alpha_id)


def _finalize(result: Dict[str, Any], store, alpha_id: str) -> Dict[str, Any]:
    """保存判定记录到台账并返回（容错与告警由 persist_workflow_record 承担）。"""
    persist_workflow_record(store, "judge", alpha_id, {
        "judged_at": datetime.now().isoformat(),
        "verdict": result.get("verdict"),
        "gates": result.get("gates"),
    })
    return result


def _extract_region(details: Dict[str, Any]) -> Optional[str]:
    """从 get_alpha_details 返回提取 region（2026-09-04 方案 A）.

    brain_client 返回可能是 {"result": {...}} 或直接 {...}；region 在 settings.region。
    """
    if not isinstance(details, dict) or details.get("__error__"):
        return None
    d = details.get("result", details)
    if not isinstance(d, dict):
        return None
    settings = d.get("settings", {})
    if isinstance(settings, dict):
        region = settings.get("region")
        if region:
            return str(region).upper()
    # 兑底：顶层 region 字段
    region = d.get("region")
    return str(region).upper() if region else None


def _load_mode_b_qualification(store, region: str = "KOR") -> Dict[str, float]:
    """从 thresholds.json + ledger_kv 加载 Mode B 资格线（Dry-Run 2.0 优化）.

    优先级：ledger_kv > thresholds.json > 默认值。
    """
    # 1. 尝试从 ledger_kv 读取
    if store:
        try:
            cached = store.get_ledger(region, "mode_b_qualification")
            if cached and isinstance(cached, dict):
                sharpe_min = cached.get("sharpe_min")
                fitness_min = cached.get("fitness_min")
                if sharpe_min is not None and fitness_min is not None:
                    return {"sharpe_min": float(sharpe_min), "fitness_min": float(fitness_min)}
        except Exception as e:
            logger.warning(f"Failed to load mode_b_qualification from ledger: {e}")

    # 2. 尝试从 thresholds.json 读取
    try:
        import json
        import os
        thresholds_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "..",
            "tracking", region, "config", "thresholds.json"
        )
        thresholds_path = os.path.abspath(thresholds_path)
        if os.path.exists(thresholds_path):
            with open(thresholds_path, "r", encoding="utf-8") as f:
                thresholds = json.load(f)
            mbq = thresholds.get("mode_b_qualification", {})
            if isinstance(mbq, dict):
                sharpe_min = mbq.get("sharpe_min")
                fitness_min = mbq.get("fitness_min")
                if sharpe_min is not None and fitness_min is not None:
                    return {"sharpe_min": float(sharpe_min), "fitness_min": float(fitness_min)}
    except Exception as e:
        logger.warning(f"Failed to load mode_b_qualification from thresholds.json: {e}")

    # 3. 返回默认值
    return _MODE_B_QUALIFICATION_DEFAULT.copy()


def _eval_platform_check(details: Dict[str, Any], mode_b_qual: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """评估平台硬检查：checks.fail 为空 + sharpe/fitness/2y 数值硬闸.

    Args:
        details: get_alpha_details 返回结果
        mode_b_qual: Mode B 资格线（sharpe_min/fitness_min），从 thresholds.json + ledger_kv 加载
    """
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

    # Mode B 资格线检查（Dry-Run 2.0 优化）
    mode_b_eligible = None
    if mode_b_qual and sharpe is not None and fitness is not None:
        mb_sharpe_min = mode_b_qual.get("sharpe_min", 1.25)
        mb_fitness_min = mode_b_qual.get("fitness_min", 0.8)
        mode_b_eligible = sharpe >= mb_sharpe_min and fitness >= mb_fitness_min
        if not mode_b_eligible:
            reasons.append(
                f"Mode B 资格线未达: sharpe {sharpe:.2f} < {mb_sharpe_min} 或 "
                f"fitness {fitness:.2f} < {mb_fitness_min}（整波判死，禁止 Mode B）"
            )

    return {
        "gate": "platform_check",
        "pass": len(reasons) == 0,
        "sharpe": sharpe,
        "fitness": fitness,
        "two_year_sharpe": two_year,
        "fail_checks": fail_names,
        "mode_b_eligible": mode_b_eligible,
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
