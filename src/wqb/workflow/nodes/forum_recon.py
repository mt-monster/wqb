# -*- coding: utf-8 -*-
"""forum_recon 节点：论坛问题驱动只读检索（recon，2026-09-28 P4 节点化）。

包装仓库根 `tools/forum_recon.py` —— 单问题 → 有效文章 → 入库（`KB/community_tpl_kb`
或 ledger `forum_recon_<qkey>`；无解落 `forum_recon_negative_*` 作「论坛无解」判死证据）。

为什么节点化（P4）：ra-pipeline 步 4/5/7/9 的 recon 触发点此前只能走 CLI；
节点化后可经 `workflow_execute(node="forum_recon")` 调用，
额度口径不变：**以能查出有效文章为标准**（自适应扩关键词，`max_search_rounds` 仅安全上限）。

dry-run 契约（与其余节点一致）：走完零成本前置（脚本存在性、参数校验、argv 契约校验）
后返回将要执行的命令与检索计划，**不 subprocess、不写库、不触网**。
"""
from __future__ import annotations

import logging
import os
import subprocess
from typing import Any, Dict, Optional

from .._common import REPO_ROOT, run_logged_subprocess, unbuffered_env, validate_argv, wq_py

logger = logging.getLogger(__name__)

_FORUM_RECON = os.path.join(str(REPO_ROOT), "tools", "forum_recon.py")

#: recon 子进程默认超时（秒）：限速抓取下 8 轮检索可达数分钟；超时杀整棵进程树。
DEFAULT_TIMEOUT_SEC = 900.0


def run(
    question: str,
    context: Optional[str] = None,
    out: str = "ledger",
    limit: int = 3,
    max_search_rounds: int = 8,
    queries: Optional[str] = None,
    timeout_sec: Optional[float] = None,
    dry_run: bool = False,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """执行论坛 recon 检索（问题驱动、只读、产出必入库）。

    Args:
        question: 具体决策问题（如 "GLB model264 慢基本面强度墙有无破墙配方"）
        context: 语境串 `k=v,k=v`（region/dataset/wall/family），透传 --context
        out: 产出落点 `kb|ledger|negative`（found=false 时工具内部强制负结果落库）
        limit: 目标**有效文章**数（额度以查出有效文章为标准；默认 3）
        max_search_rounds: 防失控安全上限（默认 8）；实际轮数由有效文章数决定
        queries: 显式关键词包（逗号分隔），覆盖机械派生
        timeout_sec: 子进程超时秒数（缺省 WQB_FORUM_RECON_TIMEOUT_SEC，再兜底 900）
        dry_run: 干跑（由 executor 经 _context 注入）
        _context: 执行上下文（由 executor 注入）

    Returns:
        执行结果字典（success / found / returncode / cmd / 计划）。
        退出码语义：0=有货（success=True, found=True）；2=无解（success=True,
        found=False —— 负结果已入库，是合法结局）；其它=工具异常（success=False）。
    """
    ctx = _context or {}
    dry_run = bool(ctx.get("dry_run", dry_run))

    result: Dict[str, Any] = {
        "node": "forum_recon",
        "success": False,
        "dry_run": dry_run,
        "question": question,
        "steps": [],
    }

    # ---- 零成本前置 1：脚本存在性 ----
    if not os.path.isfile(_FORUM_RECON):
        result["step"] = "find_forum_recon"
        result["error"] = f"forum_recon.py 不存在：{_FORUM_RECON}"
        return result
    result["steps"].append({"step": "find_forum_recon", "success": True})

    # ---- 零成本前置 2：参数校验 ----
    if not str(question or "").strip():
        result["step"] = "validate_params"
        result["error"] = "question 不能为空（recon 必须是具体决策问题，不做无目的浏览）"
        return result
    if out not in ("kb", "ledger", "negative"):
        result["step"] = "validate_params"
        result["error"] = f"out 必须是 kb|ledger|negative，收到 {out!r}"
        return result
    result["steps"].append({"step": "validate_params", "success": True})

    # ---- 构建命令 ----
    cmd = [
        wq_py(), "-u", _FORUM_RECON,
        "--question", str(question),
        "--out", str(out),
        "--limit", str(int(limit)),
        "--max-search-rounds", str(int(max_search_rounds)),
    ]
    if context:
        cmd += ["--context", str(context)]
    if queries:
        cmd += ["--queries", str(queries)]

    # ---- 零成本前置 3：argv 契约校验（逮住脚本没声明过的 --flag）----
    ok, err = validate_argv(cmd)
    if not ok:
        result["step"] = "validate_argv"
        result["error"] = f"argv 契约校验失败：{err}"
        result["cmd"] = cmd
        return result
    result["steps"].append({"step": "validate_argv", "success": True})
    result["cmd"] = cmd

    if dry_run:
        result["success"] = True
        result["plan"] = "；".join(cmd)
        result["steps"].append({
            "step": "dry_run", "success": True,
            "message": "已构建命令并过契约校验，未执行（零网络、零写库）",
        })
        return result

    # ---- 实跑（日志文件 + 进程树超时，与 wave_gate 节点同源）----
    try:
        _to = float(timeout_sec or os.environ.get("WQB_FORUM_RECON_TIMEOUT_SEC") or DEFAULT_TIMEOUT_SEC)
    except (TypeError, ValueError):
        _to = DEFAULT_TIMEOUT_SEC
    run_info = run_logged_subprocess(
        cmd,
        log_name="forum_recon_" + str(abs(hash(str(question))) % 100000),
        timeout_sec=_to,
        cwd=str(REPO_ROOT),
        env=unbuffered_env(),
    )
    result["log_path"] = run_info["log_path"]
    result["elapsed_sec"] = run_info["elapsed_sec"]
    result["stdout_tail"] = run_info["tail"]
    if run_info["timed_out"]:
        result["step"] = "run_forum_recon"
        result["timed_out"] = True
        result["error"] = (
            f"forum_recon 超时（{int(_to)}s，已杀整棵进程树）。完整输出见 {run_info['log_path']}；"
            "等价 CLI：" + subprocess.list2cmdline(cmd)
        )
        result["steps"].append({"step": "run_forum_recon", "success": False, "timed_out": True})
        return result

    proc_rc = run_info["returncode"]
    result["returncode"] = proc_rc
    if proc_rc == 0:
        result["success"] = True
        result["found"] = True
    elif proc_rc == 2:
        # 无解也是合法结局：负结果已落 forum_recon_negative_*（判死取证）
        result["success"] = True
        result["found"] = False
        result["note"] = "无解（负结果已入库）——可作「论坛无解」判死证据"
    else:
        result["success"] = False
        result["found"] = False
        result["error"] = f"forum_recon 工具异常（exit {proc_rc}），见 {run_info['log_path']}"
    result["steps"].append({"step": "run_forum_recon", "success": result["success"]})
    return result
