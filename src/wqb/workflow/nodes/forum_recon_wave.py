# -*- coding: utf-8 -*-
"""forum_recon_wave 节点：波级默认取证（收批时对本波共同卡住的墙问一次论坛）。

包装仓库根 `tools/forum_recon_wave.py`：本波回测结果 → 机械派生决策问题（墙问题 / 全灭时的「有无解法」/ 不问）
→ 交给 `tools/forum_recon.py` 检索 → 落 ledger（`forum_recon_<qkey>` 有解 / `forum_recon_negative_<qkey>` 无解 /
`forum_recon_error_<qkey>` 故障）+ 完成标记 `forum_recon_wave_<wave>`。派生规则见 `src/wqb/recon_wave.py`。

为什么有它：ra-pipeline 步 4 / 7 / 9 的论坛触发点原本要 Agent 记得去查；「卡墙时想起来」不可靠，
所以收批时由代码替 Agent 问一次，之后 Mode B 找武器、判死取证（`seal_dead_end` 的取证闸）先读这条 ledger 记录。
每波 ≤ 1 次：可靠结局（有货 / 无解）占用本波额度；**工具故障不占额度**（故障 ≠ 取证，修好后同一波可重跑）。

dry-run 契约（与其余节点一致）：走完零成本前置（参数校验、脚本存在性、argv 契约校验）后返回将要执行的命令，
**不 subprocess、不读写库、不触网**——要看派生出的问题请用 `python tools/forum_recon_wave.py --dry-run`（只读库，零网络零写库）。
"""
from __future__ import annotations

import json
import os
import subprocess
from typing import Any, Dict, Optional

from ... import recon_evidence as RE
from .._common import REPO_ROOT, run_logged_subprocess, unbuffered_env, validate_argv, wq_py

_TOOL = os.path.join(str(REPO_ROOT), "tools", "forum_recon_wave.py")

#: 子进程默认超时（秒）：与 forum_recon 同口径——限速抓取下 8 轮检索可达数分钟；超时杀整棵进程树。
DEFAULT_TIMEOUT_SEC = 900.0


def _parse_tool_json(tail: str) -> Optional[Dict[str, Any]]:
    """从工具输出尾部取最后一行 `{"tool": "forum_recon_wave", ...}`（工具约定：最后一行是单行 JSON）。"""
    for line in reversed(str(tail or "").splitlines()):
        line = line.strip()
        if line.startswith('{"tool": "forum_recon_wave"'):
            try:
                obj = json.loads(line)
            except ValueError:
                return None
            return obj if isinstance(obj, dict) else None
    return None


def run(
    region: str,
    wave: str,
    dataset: Optional[str] = None,
    force: bool = False,
    limit: int = 3,
    max_search_rounds: int = 8,
    timeout_sec: Optional[float] = None,
    dry_run: bool = False,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """波级默认取证：本波共同卡住的墙 → 问一次论坛 → 落 ledger（每波 ≤ 1 次）。

    Args:
        region: 区域（如 KOR）
        wave: 波号（整数或字符串波号，如 97 / s2_<ds>_d1）
        dataset: 数据集；缺省取本波回测行里最多的那个
        force: 忽略本波已有的完成标记，重新取证
        limit: 目标有效文章数（透传 forum_recon，默认 3；额度以查出有效文章为标准）
        max_search_rounds: 防失控安全上限（透传 forum_recon，默认 8）
        timeout_sec: 子进程超时秒数（缺省 WQB_FORUM_RECON_TIMEOUT_SEC，再兜底 900）
        dry_run: 干跑（由 executor 经 _context 注入）
        _context: 执行上下文（由 executor 注入）

    Returns:
        执行结果字典（success / found / status / skipped / reason / question / question_key / wall / returncode / cmd）。
        退出码语义同 forum_recon：0 = 有货，或本波没有需要问的问题（`skipped=True`，`reason` 给原因）；
        2 = 可靠的「论坛无解」（success=True, found=False）；其它 = **工具故障**（success=False, found=None,
        status=error）——不是「论坛无解」，不得当判死证据。
    """
    ctx = _context or {}
    dry_run = bool(ctx.get("dry_run", dry_run))

    result: Dict[str, Any] = {
        "node": "forum_recon_wave",
        "success": False,
        "dry_run": dry_run,
        "region": region,
        "wave": wave,
        "steps": [],
    }

    # ---- 零成本前置 1：脚本存在性 ----
    if not os.path.isfile(_TOOL):
        result["step"] = "find_forum_recon_wave"
        result["error"] = f"forum_recon_wave.py 不存在：{_TOOL}"
        return result
    result["steps"].append({"step": "find_forum_recon_wave", "success": True})

    # ---- 零成本前置 2：参数校验 ----
    if not str(region or "").strip():
        result["step"] = "validate_params"
        result["error"] = "region 不能为空"
        return result
    if not str(wave or "").strip():
        result["step"] = "validate_params"
        result["error"] = "wave 不能为空（波级取证按波落完成标记）"
        return result
    result["steps"].append({"step": "validate_params", "success": True})

    # ---- 构建命令 ----
    cmd = [
        wq_py(), "-u", _TOOL,
        "--region", str(region).strip(),
        "--wave", str(wave).strip(),
        "--limit", str(int(limit)),
        "--max-search-rounds", str(int(max_search_rounds)),
    ]
    if dataset:
        cmd += ["--dataset", str(dataset)]
    if force:
        cmd.append("--force")

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
            "message": "已构建命令并过契约校验，未执行（零网络、零读写库）；要看派生出的问题："
                       "在命令后加 --dry-run 直接跑工具（只读库）",
        })
        return result

    # ---- 实跑（日志文件 + 进程树超时，与 forum_recon 节点同源）----
    try:
        _to = float(timeout_sec or os.environ.get("WQB_FORUM_RECON_TIMEOUT_SEC") or DEFAULT_TIMEOUT_SEC)
    except (TypeError, ValueError):
        _to = DEFAULT_TIMEOUT_SEC
    run_info = run_logged_subprocess(
        cmd,
        log_name=f"forum_recon_wave_{region}_{wave}",
        timeout_sec=_to,
        cwd=str(REPO_ROOT),
        env=unbuffered_env(),
    )
    result["log_path"] = run_info["log_path"]
    result["elapsed_sec"] = run_info["elapsed_sec"]
    result["stdout_tail"] = run_info["tail"]
    if run_info["timed_out"]:
        result["step"] = "run_forum_recon_wave"
        result["timed_out"] = True
        result["found"] = None                       # 超时 = 没拿到结论，不是「无解」
        result["status"] = RE.STATUS_ERROR
        result["error"] = (
            f"forum_recon_wave 超时（{int(_to)}s，已杀整棵进程树）。完整输出见 {run_info['log_path']}；"
            "等价 CLI：" + subprocess.list2cmdline(cmd)
        )
        result["steps"].append({"step": "run_forum_recon_wave", "success": False, "timed_out": True})
        return result

    proc_rc = run_info["returncode"]
    result["returncode"] = proc_rc
    tool = _parse_tool_json(run_info["tail"])
    if tool:
        for k in ("kind", "wall", "dataset", "question", "question_key", "skipped", "reason", "sink", "marker",
                  "from_cache", "n_useful", "basis", "note", "marker_error"):
            if tool.get(k) is not None:
                result[k] = tool[k]
    if proc_rc == 0:
        # 0 = 有货，或本波没有需要问的问题（skipped）；输出里的单行 JSON 说明是哪一种
        result["success"] = True
        found = (tool or {}).get("found")
        result["found"] = True if found is True else None
        if tool is None:
            result["parse_warning"] = "工具退出码 0，但没能从输出尾部解析出结构化结果（最后一行 JSON）"
        result["status"] = (RE.STATUS_OK if found is True
                            else "skipped" if (tool or {}).get("skipped") else "unknown")
    elif proc_rc == 2:
        # 无解也是合法结局：检索可靠完成，负结果已落 forum_recon_negative_*
        result["success"] = True
        result["found"] = False
        result["status"] = RE.STATUS_NO_RESULT
        result["note"] = result.get("note") or "无解（检索可靠完成，负结果已入库）——可作「论坛无解」判死证据"
    else:
        # 故障 ≠ 无解：found 必须是 None，绝不能是 False（否则下游会把它当负结果）
        result["success"] = False
        result["found"] = None
        result["status"] = RE.STATUS_ERROR
        qk = result.get("question_key")
        result["error"] = (f"forum_recon_wave 工具故障（exit {proc_rc}），见 {run_info['log_path']}——"
                           f"**不是「论坛无解」**，不得当判死证据"
                           + (f"；故障记录：ledger {RE.key_error(qk)}" if qk else ""))
    result["steps"].append({"step": "run_forum_recon_wave", "success": result["success"]})
    return result
