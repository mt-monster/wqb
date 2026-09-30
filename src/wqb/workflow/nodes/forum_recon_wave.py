# -*- coding: utf-8 -*-
"""forum_recon_wave 节点：本波自动论坛取证（2026-09-29 新增）。

为什么需要它（用户定案「确保默认能走到」）：
    此前 forum_recon 的 4 个集成点（步 4 机制枯竭 / 步 5 门禁回补 / 步 7 卡墙找武器 /
    S6 判死核对）**全部写在 SKILL.md 里靠 Agent 记得触发**，无代码强制 —— 默认路径走不到。
    实测后果：判死前取证常缺失，而 `seal_dead_end` 的判死取证闸（2026-09-29 fail-closed）
    要求 `payload.forum_recon` 有真实结论，两者一叠加就会卡住判死。

    本节点把 recon 变成**波级默认动作**：每波收批时自动派生一个决策问题并取证，
    结果落 ledger（`forum_recon_<qkey>` 有解 / `forum_recon_negative_<qkey>` 无解 /
    `forum_recon_error_<qkey>` 故障），供后续步 4/5/7 与 S6 判死直接消费。

节流：
    - 每波默认最多 1 次（`max_recon`，与 SKILL.md 步 7「每波 ≤1 次」一致）；
    - 同问题 7 天缓存由 `tools/forum_recon.py` 内部自动复用，不重复 live 查；
    - **故障结论不缓存**（forum_recon 侧保证），故故障后可立即重试。

为什么复用而非重跑：
    直接调同包 `forum_recon.run()`，复用其脚本存在性 / 参数 / argv 契约校验、
    超时杀进程树与退出码语义（0 有货 / 2 无解 / 3 未取证）。

dry-run 契约（与其余节点一致）：派生问题 → 构建计划 → 到此为止，
**不 subprocess、不写库、不触网**。
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from . import forum_recon as _fr_node

logger = logging.getLogger(__name__)


def run(
    region: str,
    wave: str,
    dataset: Optional[str] = None,
    question: Optional[str] = None,
    out: str = "negative",
    limit: int = 3,
    max_search_rounds: int = 8,
    max_recon: int = 1,
    timeout_sec: Optional[float] = None,
    dry_run: bool = False,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """本波自动论坛取证。

    Args:
        region: 区域代码（如 KOR）
        wave: 波次号
        dataset: 数据集 ID（可选，进入 context 与派生问题）
        question: 显式决策问题；不给则按 region/dataset/wave 派生
        out: 产出落点 `kb|ledger|negative`（判死取证用 negative）
        limit: 目标有效文章数
        max_search_rounds: 防失控安全上限
        max_recon: 本波最多取证次数（默认 1；>1 时按分号拆分 question 逐条跑）
        timeout_sec: 子进程超时秒数
        dry_run: 干跑（由 executor 经 _context 注入）
        _context: 执行上下文

    Returns:
        {"node", "success", "dry_run", "region", "wave", "recons": [...], "steps": [...]}
        单条时额外平铺 `found` / `sink`，便于调用方直接判定。
    """
    ctx = _context or {}
    dry_run = bool(ctx.get("dry_run", dry_run))

    result: Dict[str, Any] = {
        "node": "forum_recon_wave",
        "success": False,
        "dry_run": dry_run,
        "region": region,
        "wave": str(wave),
        "dataset": dataset,
        "steps": [],
        "recons": [],
    }

    # ---- 零成本前置 1：参数校验 ----
    if not str(region or "").strip():
        result["step"] = "validate_params"
        result["error"] = "region 不能为空"
        return result
    if not str(wave or "").strip():
        result["step"] = "validate_params"
        result["error"] = "wave 不能为空"
        return result
    if out not in ("kb", "ledger", "negative"):
        result["step"] = "validate_params"
        result["error"] = f"out 必须是 kb|ledger|negative，收到 {out!r}"
        return result
    result["steps"].append({"step": "validate_params", "success": True})

    context = f"region={region},wave={wave}" + (f",dataset={dataset}" if dataset else "")

    # ---- 零成本前置 2：派生决策问题（未显式给出时）----
    questions: list[str] = []
    if question:
        questions = [q.strip() for q in str(question).split(";") if q.strip()]
    else:
        target = f"{dataset} " if dataset else ""
        questions = [f"{region} {target}波次{wave} 卡墙/判死：有无社区已验证的解法或破墙配方"]
    questions = questions[: max(1, int(max_recon))]
    result["questions"] = questions
    result["steps"].append({"step": "derive_questions", "success": True, "count": len(questions)})

    if dry_run:
        result["success"] = True
        result["plan"] = [
            {"question": q, "context": context, "out": out,
             "limit": limit, "max_search_rounds": max_search_rounds}
            for q in questions
        ]
        result["steps"].append({
            "step": "dry_run", "success": True,
            "message": f"已派生 {len(questions)} 个决策问题并构建检索计划，未执行（零网络、零写库）",
        })
        return result

    # ---- 实跑（逐条，复用 forum_recon 节点的校验与超时语义）----
    ok_any = False
    for q in questions:
        single = _fr_node.run(
            question=q,
            context=context,
            out=out,
            limit=limit,
            max_search_rounds=max_search_rounds,
            timeout_sec=timeout_sec,
            dry_run=False,
        )
        result["recons"].append({
            "question": q,
            "found": single.get("found"),
            "returncode": single.get("returncode"),
            "sink": single.get("sink") or single.get("plan"),
            "error": single.get("error"),
        })
        if single.get("success"):
            ok_any = True

    first = result["recons"][0] if result["recons"] else {}
    result["found"] = first.get("found")
    result["sink"] = first.get("sink")
    result["success"] = ok_any
    result["steps"].append({"step": "run_forum_recon", "success": ok_any,
                            "count": len(result["recons"])})
    if not ok_any and len(result["recons"]) == 1:
        # 单条且失败：把原因平铺出来，避免调用方只看到 success=False
        result["error"] = first.get("error") or "forum_recon 未取证（工具故障）"
    return result
