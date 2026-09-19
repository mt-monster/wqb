# -*- coding: utf-8 -*-
"""hypothesis_round 节点：饱和数据集的假设优先实验轮次构建（brain-alpha-research-hypothesis-first）。

包装 `src/wqb/research/hypothesis_miner.py::run_hypothesis_round` —— 每个选中假设派发
4 条表达式（主假设 / 去门控消融 / 常数对照 / 变体），用于把"模板遍历"切换为
"可证伪假设驱动"（对照/消融设计天然产出与 book 正交的证据链）。

为什么新增（2026-09-12 全量精读）：存量信号空间饱和（SELF/PROD 双闸 + 模板到顶）
是当前第一瓶颈，而 hypothesis-first 是唯一直接对准它的方法论——此前代码真实存在
但无 SOP 站位、无节点、从未被战役消费。补上本节点后，ra-pipeline 步 2 可按
路由条件（dataset alphaCount≥1 万 或连续 2 波模板全灭）切入假设优先工作流。

dry-run 契约（与其余节点一致）：走完**零成本前置**（catalog 存在性/可解析性、
假设数量与必填字段校验）后返回将要构建的实验计划，**不 subprocess、不写库、
不发起任何平台请求**（表达式构建本身也是纯本地）。
"""
from __future__ import annotations

import logging
import os
from typing import Any, Dict, Optional

from .._common import REPO_ROOT

logger = logging.getLogger(__name__)

#: 默认假设目录（与 brain-alpha-research-hypothesis-first 的约定一致）
_CATALOG_DIR = os.path.join(str(REPO_ROOT), "data", "hypothesis_catalog")


def _default_catalog(dataset_id: str) -> str:
    return os.path.join(_CATALOG_DIR, f"{dataset_id}_hypotheses.json")


def run(
    dataset_id: str,
    catalog_path: Optional[str] = None,
    max_hypotheses: int = 1,
    region: str = "",
    delay: int = 1,
    session_id: Optional[str] = None,
    save_ledger: bool = False,
    dry_run: bool = False,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """构建一轮假设优先实验（每假设 4 条表达式，零平台成本）。

    Args:
        dataset_id: 数据集 ID（用于默认 catalog 路径 `data/hypothesis_catalog/<ds>_hypotheses.json`）
        catalog_path: 假设目录 JSON 显式路径（缺省按 dataset_id 推导）
        max_hypotheses: 本轮选取的假设数（默认 1；每个假设派发 4 条表达式）
        region: 区域（仅透传记录，用于台账键）
        delay: 延迟（仅透传记录）
        session_id: 台账 session 标识（save_ledger=True 时必填语义）
        save_ledger: 实跑后把轮次记录追加到 tracking/hypotheses/ledger.jsonl
        dry_run: 干跑（由 executor 经 _context 注入）
        _context: 执行上下文（由 executor 注入）

    Returns:
        执行结果字典（含 success / experiments / catalog 信息）
    """
    steps: list = []
    # dry_run 与 executor 约定一致：显式参数或 _context 注入皆可（wave_gate 同款）
    dry_run = bool(dry_run or (_context or {}).get("dry_run"))

    # ---- 零成本前置 1：catalog 解析 ----
    path = catalog_path or _default_catalog(dataset_id)
    if not os.path.exists(path):
        return {
            "success": False,
            "error": (f"假设目录不存在：{path}。请先按 brain-alpha-research-hypothesis-first "
                      f"构建 ≥20 条可证伪假设（data/hypothesis_catalog/{dataset_id}_hypotheses.json，"
                      "load_catalog 仅支持 JSON——SKILL 中的 YAML 为规划格式，需先转换）。"),
            "catalog_path": path,
            "steps": steps,
        }
    steps.append({"step": "catalog_exists", "success": True, "path": path})

    # ---- 零成本前置 2：解析与数量校验 ----
    try:
        from wqb.research.hypothesis_miner import load_catalog, run_hypothesis_round

        hypotheses = load_catalog(path)
    except Exception as e:  # noqa: BLE001 — 节点边界要兜住一切解析错误
        return {"success": False, "error": f"假设目录解析失败：{e}", "catalog_path": path,
                "steps": steps}
    steps.append({"step": "catalog_parsed", "success": True, "hypotheses": len(hypotheses)})
    if not hypotheses:
        return {"success": False, "error": "假设目录为空（需 ≥20 条）", "catalog_path": path,
                "steps": steps}

    plan = {
        "dataset_id": dataset_id,
        "region": region,
        "delay": delay,
        "selected": min(max_hypotheses, len(hypotheses)),
        "expressions_per_hypothesis": 4,
        "total_expressions": 4 * min(max_hypotheses, len(hypotheses)),
        "hypothesis_ids": [h.hypothesis_id for h in hypotheses[:max_hypotheses]],
        "note": "主假设 / 去门控消融 / 常数对照 / 变体；回测后交 hypothesis_miner.judge 四态判定",
    }
    steps.append({"step": "plan_built", "success": True, "plan": plan})

    if dry_run:
        return {"success": True, "dry_run": True, "catalog_path": path,
                "plan": plan, "steps": steps}

    # ---- 实跑：纯本地表达式构建（不触平台、不写 expressions 表——入库走 S3 --from-db 通道） ----
    try:
        experiments = run_hypothesis_round(path, max_hypotheses=max_hypotheses)
    except Exception as e:  # noqa: BLE001
        return {"success": False, "error": f"实验轮次构建失败：{e}", "catalog_path": path,
                "steps": steps}
    steps.append({"step": "round_built", "success": True,
                  "experiments": len(experiments)})

    ledger_path = None
    if save_ledger:
        try:
            from wqb.research.hypothesis_miner import save_to_ledger

            sid = session_id or f"{dataset_id}_{region}_d{delay}"
            ledger_path = save_to_ledger(
                {"status": "ROUND_BUILT", "reason": "hypothesis_round node",
                 "diagnostics": plan}, sid)
            steps.append({"step": "ledger_saved", "success": True, "path": ledger_path})
        except Exception as e:  # noqa: BLE001
            steps.append({"step": "ledger_saved", "success": False, "error": str(e)})

    return {
        "success": True,
        "dry_run": False,
        "catalog_path": path,
        "plan": plan,
        "experiments": experiments,
        "ledger_path": ledger_path,
        "steps": steps,
    }
