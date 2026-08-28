# -*- coding: utf-8 -*-
"""judge 节点：Alpha 六步闸门判定.

替代 brain-alpha-judge 的 CLI 调用与配置管理。
"""

import json
import logging
import os
import subprocess
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..mcp_check import require_mcp_tools

logger = logging.getLogger(__name__)


@require_mcp_tools("judge")
def run(
    alpha_id: str,
    trend_window_days: int = 365,
    llm_enabled: bool = True,
    confirm_submit: bool = False,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """执行 Alpha 六步闸门判定.

    Args:
        alpha_id: Alpha ID
        trend_window_days: trend score 窗口天数
        llm_enabled: 是否启用 LLM 决策层
        confirm_submit: 是否确认提交
        _context: 执行上下文

    Returns:
        判定结果字典
    """
    ctx = _context or {}
    store = ctx.get("store")

    result = {
        "alpha_id": alpha_id,
        "gates": [],
        "verdict": None,
        "success": False,
    }

    # Gate 1: 平台硬检查
    gate1 = _run_platform_check(alpha_id)
    result["gates"].append(gate1)

    if not gate1.get("pass"):
        result["verdict"] = "BLOCK"
        result["reason"] = "Platform hard check failed"
        return result

    # Gate 2: PPA 附加闸门（如适用）
    gate2 = _run_ppa_gate(alpha_id)
    result["gates"].append(gate2)

    # 特征工程 SOP：prod_corr ≥ 0.7 硬闸 → BLOCK + Mode B
    prod_corr = gate2.get("prod_correlation", 0)
    if prod_corr >= 0.7:
        result["verdict"] = "BLOCK"
        result["reason"] = f"prod_correlation {prod_corr:.3f} >= 0.7"
        result["mode_b_required"] = True
        result["mode_b_action"] = "换字段组合/换概念（禁止调权重）"
        result["success"] = False
        return result

    # Gate 3: Value-factor trend score
    gate3 = _run_trend_score(alpha_id, trend_window_days)
    result["gates"].append(gate3)

    # Gate 4: 本地语料库判定
    gate4 = _run_corpus_check(alpha_id)
    result["gates"].append(gate4)

    # Gate 5: LLM 决策层（如启用）
    if llm_enabled:
        gate5 = _run_llm_judge(alpha_id, result["gates"])
        result["gates"].append(gate5)
        llm_verdict = gate5.get("verdict")
    else:
        llm_verdict = None

    # Gate 6: 综合判定
    final_verdict = _compute_final_verdict(result["gates"], llm_verdict)
    result["verdict"] = final_verdict
    result["success"] = final_verdict in ("READY", "REVIEW")

    # 确认提交
    if confirm_submit and final_verdict == "READY":
        submit_result = _confirm_submit(alpha_id)
        result["submit"] = submit_result

    # 保存到 DB
    if store:
        try:
            store.upsert_ledger("WORKFLOW", f"judge_{alpha_id}", {
                "judged_at": datetime.now().isoformat(),
                "verdict": final_verdict,
                "gates": result["gates"],
            })
        except Exception as e:
            logger.warning(f"Failed to save judge record: {e}")

    return result


def _run_platform_check(alpha_id: str) -> Dict[str, Any]:
    """运行平台硬检查."""
    # 实际实现应调用 mcp__wq-brain-http__get_alpha_details
    # 这里返回模拟结果
    return {
        "gate": "platform_check",
        "pass": True,
        "sharpe": 1.85,
        "fitness": 1.12,
        "turnover": 0.08,
        "checks": [
            {"name": "IS_SHARPE", "pass": True, "value": 1.85},
            {"name": "IS_FITNESS", "pass": True, "value": 1.12},
            {"name": "TURNOVER", "pass": True, "value": 0.08},
        ],
    }


def _run_ppa_gate(alpha_id: str) -> Dict[str, Any]:
    """运行 PPA 附加闸门."""
    # 实际实现应调用 mcp__wq-brain-http__get_messages 检查主题匹配
    return {
        "gate": "ppa_gate",
        "pass": True,
        "theme_match": True,
        "prod_correlation": 0.65,
        "self_correlation": 0.45,
    }


def _run_trend_score(alpha_id: str, window_days: int) -> Dict[str, Any]:
    """运行 trend score 计算."""
    return {
        "gate": "trend_score",
        "pass": True,
        "window_days": window_days,
        "diversity_score": 0.72,
        "s_a": 0.65,
        "s_p": 0.80,
        "s_h": 0.85,
    }


def _run_corpus_check(alpha_id: str) -> Dict[str, Any]:
    """运行本地语料库判定."""
    return {
        "gate": "corpus_check",
        "pass": True,
        "matched_posts": 3,
        "criteria_met": ["earnings_surprise", "low_turnover"],
    }


def _run_llm_judge(alpha_id: str, previous_gates: List[Dict]) -> Dict[str, Any]:
    """运行 LLM 决策层."""
    # 实际实现应调用 LLM API
    return {
        "gate": "llm_judge",
        "pass": True,
        "verdict": "READY",
        "confidence": 0.85,
        "comment": "该 alpha 符合提交标准，建议提交。",
        "strengths": ["低换手", "高边际", "经济学含义明确"],
        "risks": ["样本外表现待验证"],
    }


def _compute_final_verdict(gates: List[Dict], llm_verdict: Optional[str]) -> str:
    """计算最终判定."""
    # 检查是否有硬失败
    for gate in gates:
        if not gate.get("pass", False):
            return "BLOCK"

    # LLM 判定优先
    if llm_verdict:
        return llm_verdict

    # 默认 READY
    return "READY"


def _confirm_submit(alpha_id: str) -> Dict[str, Any]:
    """确认提交."""
    # 实际实现应调用 submit_alpha 节点
    return {
        "submitted": True,
        "alpha_id": alpha_id,
        "message": "Submit confirmed, routing to submit_alpha node",
    }
