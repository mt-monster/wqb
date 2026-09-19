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
from ..mode_b_config import evaluate_mode_b as _evaluate_mode_b
from ..mode_b_config import load_mode_b_config as _load_mode_b_config

logger = logging.getLogger(__name__)

# 硬闸阈值（与战役口径一致）
_SHARPE_MIN = 1.58
_FITNESS_MIN = 1.0
_2Y_MIN = 1.58
_PROD_MAX = 0.7
_SELF_MAX = 0.7


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
        # 无子进程可构建 —— 干跑只给出「会发哪些平台请求 + 用哪些阈值判」。
        # 2026-09-05 修复：不再尝试解析 brain_client。解析动作会 import 依赖、
        # 可能建立连接，与「干跑零副作用」契约冲突；其成功与否也只反映干跑用的
        # 解释器（通常是根 venv），对节点真实运行的 MCP venv 没有参考价值。
        return {
            "alpha_id": alpha_id,
            "success": True,
            "dry_run": True,
            "note": "dry-run：请求计划已构建，未调用平台",
            "verdict": None,
            "gates": [],
            "steps": [{
                "step": "plan_only",
                "success": True,
                "skipped": True,
                "note": "dry-run 不解析 brain_client，避免触碰网络与子进程",
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
    # 2026-09-09：同时加载完整配置（含旁路/判死线）供 _eval_platform_check 判定
    mode_b_cfg = _load_mode_b_config(store, region=alpha_region)

    gate1 = _eval_platform_check(details, mode_b_qual=mode_b_qual, mode_b_cfg=mode_b_cfg)
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

    # ---- 2026-09-17 P3：三态 → 逐闸清单（附加字段，不改既有返回契约）----
    # 动机：`verdict` 是**聚合结论**，极易被读成提交裁决；本节点其实只是参考层
    # （权威 = submit_verdict）。故额外给出逐闸**清单**，让调用方据事实自行判断。
    # 特别地：`unavailable`（降级/取不到数）此前与"通过"在聚合结论里无法区分 ——
    # 例如 correlation 降级时 `pass=True`，可静默凑出 READY。清单把降级显式列出。
    result["checklist"] = build_checklist(result["gates"])
    result["degraded_gates"] = [
        g.get("gate") for g in result["gates"] if g.get("unavailable")
    ]
    if result["degraded_gates"]:
        result["warning"] = (
            f"以下闸未取到数（降级，结论未包含其判定）："
            f"{'、'.join(str(x) for x in result['degraded_gates'])}；"
            f"verdict={final_verdict} 不足以作为提交依据，请以 submit_verdict 为准"
        )

    return _finalize(result, store, alpha_id)


def build_checklist(gates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """把 gate 结构摊平为**逐闸清单**（事实清单，非聚合裁决）。

    只保留标量字段（int/float/str/bool/None），跳过嵌套结构，避免清单臃肿；
    `gate` / `pass` / `unavailable` 三个键固定在最前，便于逐行比对。

    与 `_compute_final_verdict` 的分工：后者给聚合结论，本函数给事实底座。
    调用方（含 Agent）应**优先读清单**，`verdict` 仅作摘要。
    """
    out: List[Dict[str, Any]] = []
    for g in gates or []:
        if not isinstance(g, dict):
            continue
        row: Dict[str, Any] = {
            "gate": g.get("gate"),
            "pass": bool(g.get("pass", False)),
            "unavailable": bool(g.get("unavailable", False)),
        }
        for k, v in g.items():
            if k in ("gate", "pass", "unavailable"):
                continue
            if isinstance(v, (int, float, str, bool, type(None))):
                row[k] = v
        out.append(row)
    return out


def _finalize(result: Dict[str, Any], store, alpha_id: str) -> Dict[str, Any]:
    """保存判定记录到台账并返回（容错与告警由 persist_workflow_record 承担）。"""
    persist_workflow_record(store, "judge", alpha_id, {
        "judged_at": datetime.now().isoformat(),
        "verdict": result.get("verdict"),
        "gates": result.get("gates"),
        # 2026-09-17 P3：清单与降级闸一并落台账，便于事后复核"当时的结论有没有缺闸"
        "checklist": result.get("checklist"),
        "degraded_gates": result.get("degraded_gates"),
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
    """加载 Mode B 主闸资格线（sharpe_min/fitness_min）。

    2026-09-09 起委托统一加载器 mode_b_config.load_mode_b_config（解析 $ref /
    全局权威 / 区域覆盖 / 自适应学习区域 ledger）。本函数只返回主闸双标量，
    保持与既有调用点/测试的返回契约兼容；旁路与判死线由 _eval_platform_check
    经 evaluate_mode_b 单独取。
    """
    cfg = _load_mode_b_config(store, region=region)
    main = cfg.get("main_gate") or {}
    return {
        "sharpe_min": float(main.get("sharpe_min", 1.25)),
        "fitness_min": float(main.get("fitness_min", 0.8)),
    }


def _eval_platform_check(details: Dict[str, Any], mode_b_qual: Optional[Dict[str, float]] = None,
                         mode_b_cfg: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """评估平台硬检查：checks.fail 为空 + sharpe/fitness/2y 数值硬闸.

    Args:
        details: get_alpha_details 返回结果
        mode_b_qual: Mode B 主闸双标量（sharpe_min/fitness_min），兼容旧调用
        mode_b_cfg: 完整 Mode B 配置（主闸+旁路+判死线），优先于 mode_b_qual
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
    # 旁路判定用的补充指标（2026-09-09 主闸+旁路结构）
    margin = metrics.get("margin")
    turnover = metrics.get("turnover")
    returns = metrics.get("returns")

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

    # Mode B 资格判定（2026-09-09 主闸+旁路结构，委托 mode_b_config.evaluate_mode_b）
    # mode_b_qual 为 _load_mode_b_qualification 返回的主闸双标量（兼容旧调用）；
    # 完整配置（含旁路/判死线）由调用方 run() 经 _load_mode_b_config 提供，
    # 这里从 mode_b_qual 重建最小 cfg 兜底，保证单测直调本函数也能跑。
    mode_b_eligible = None
    mode_b_verdict = None
    mode_b_bypass = None
    mode_b_action = None
    if mode_b_qual and sharpe is not None and fitness is not None:
        # 优先用完整配置（含旁路）；缺省从主闸双标量重建最小 cfg（旁路走默认）
        if mode_b_cfg:
            cfg = mode_b_cfg
        else:
            mb_sharpe_min = mode_b_qual.get("sharpe_min", 1.25)
            mb_fitness_min = mode_b_qual.get("fitness_min", 0.8)
            cfg = {"main_gate": {"sharpe_min": mb_sharpe_min, "fitness_min": mb_fitness_min}}
        verdict = _evaluate_mode_b(
            cfg,
            sharpe=sharpe, fitness=fitness, two_year_sharpe=two_year,
            margin=margin, turnover=turnover, returns=returns,
        )
        mode_b_eligible = verdict["eligible"]
        mode_b_verdict = verdict["verdict"]
        mode_b_bypass = verdict.get("bypass")
        mode_b_action = verdict.get("mode_b_action")
        if not mode_b_eligible:
            reasons.append(verdict["reason"])

    return {
        "gate": "platform_check",
        "pass": len(reasons) == 0,
        "sharpe": sharpe,
        "fitness": fitness,
        "two_year_sharpe": two_year,
        "fail_checks": fail_names,
        "mode_b_eligible": mode_b_eligible,
        "mode_b_verdict": mode_b_verdict,
        "mode_b_bypass": mode_b_bypass,
        "mode_b_action": mode_b_action,
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
