# -*- coding: utf-8 -*-
"""wave_gate 节点：S2→S3 门禁（ra-pipeline 步 5）。

包装仓库根 `tools/wave_gate.py` —— 语法 + toolkit `gate.py` 8 闸 + 体检硬门
（`field_inspect_gate.py`）+ 多样性，一键落盘 `gate_results`。

为什么新增（2026-09-11 审计）：此前步 5 **没有 workflow 节点**，SOP 只能注明
"本步不在 MCP，必须走 CLI"，于是"九步整链交给 workflow_chain"无法覆盖门禁 ——
链最多走到步 4（生成）就断了。补上本节点后，整链可覆盖 步 2/3/4/5/6。

dry-run 契约（与其余节点一致）：走完**零成本前置**（脚本存在性、战役目录解析、
argv 契约校验）后返回将要执行的命令与请求计划，**不 subprocess、不写库**。
"""
from __future__ import annotations

import logging
import os
import subprocess
from typing import Any, Dict, Optional

from .._common import (REPO_ROOT, resolve_campaign_dir, run_logged_subprocess, unbuffered_env,
                       validate_argv, wq_py)

logger = logging.getLogger(__name__)

#: wave_gate.py 在仓库根 tools/（不在 toolkit scripts/，见 ra-pipeline 步 5 脚本归属注）
_WAVE_GATE = os.path.join(str(REPO_ROOT), "tools", "wave_gate.py")

#: 门禁子进程默认超时（秒）。本地零配额脚本，实测 <1s～2min；可用节点参数
#: timeout_sec 或环境变量 WQB_WAVE_GATE_TIMEOUT_SEC 覆盖。
DEFAULT_TIMEOUT_SEC = 600.0


def run(
    region: str,
    dataset: str,
    wave: str,
    datasets: Optional[str] = None,
    exprs_file: Optional[str] = None,
    candidates: Optional[str] = None,
    expr: Optional[str] = None,
    from_db: bool = True,
    skip_diversity_gate: bool = False,
    fix: bool = False,
    campaign_dir: Optional[str] = None,
    inspect_mode: Optional[str] = None,
    prod_family_gate: bool = True,
    timeout_sec: Optional[float] = None,
    dry_run: bool = False,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """执行 S2→S3 门禁（语法 + 8 闸 + 体检硬门 + 多样性）。

    调用契约（2026-09-27 固化，守护见 tests/unit/test_wave_gate_auto_insert_contract.py）：
    ① **节点参数 ⊆ CLI 参数** —— 新增节点参数必须确认 `tools/wave_gate.py` 有对应 `--flag`
       （`validate_argv` 会静态校验）；
    ② **调用侧不得传入 run() 不接受的参数** —— `world-quant-brain-mcp/tools_workflow.py`
       对 `gem → batch_track` 链的自动插入节点会带 `prod_family_gate`，此前 run() 无此形参
       → 该类链 100% `TypeError`（2026-09-27 dry-run 实证），故此处补上并透传。

    Args:
        region: 区域代码（如 KOR）
        dataset: 数据集 ID
        datasets: 逗号分隔的**额外**数据集，与 `dataset` 合并闸2 字段白名单
            （透传 wave_gate.py --datasets）。跨金字塔表达式必须带：主信号在 A、
            条件/分组腿字段在 B 时，只报 A 会让闸2 判 B 的字段"未验证"整条拦下
            （2026-09-27 GLB dl20d×risk70/fundamental44 门控波 7/8 被误拦）。
        wave: 波次号（**字符串**，支持 `97` 与 `s2_xxx_d1` 两种形态）
        exprs_file: 每行一条表达式的 txt（候选不在库时用）
        candidates: 候选 JSON（兼容参数）
        expr: 单条表达式（自查用）
        from_db: 从 `expressions` 表读候选（默认 True，推荐）
        skip_diversity_gate: 跳过闸6 多样性（repair 批逃生阀，须在台账记因）
        fix: VECTOR 数据集自动裹 `vec_*` 后再检测（透传 toolkit gate.py）
        campaign_dir: 战役目录（可选，默认按 region 解析）
        inspect_mode: 体检硬门**缺包**时行为 `off|warn|enforce`（缺省读
            `WQB_INSPECT_MODE`，再兜底 `warn`）。开新数据集/新区域建议传 `enforce`
            —— 缺体检包即整波 fail-closed，避免低覆盖/厚尾/稀疏事件预处理约束裸奔。
        prod_family_gate: 闸 PF（骨架级 prod 死路预检，透传 `--prod-family-gate`，默认开；
            关则透传 `--no-prod-family-gate`）。与 CLI 默认值一致，故自动插入侧传 True 时幂等。
        timeout_sec: 子进程超时秒数（缺省 WQB_WAVE_GATE_TIMEOUT_SEC，再兜底 600）。
            超时会杀整棵进程树并返回 log_path + 输出尾部，不再静默吞掉。
        dry_run: 干跑（由 executor 经 _context 注入）
        _context: 执行上下文（由 executor 注入）

    Returns:
        执行结果字典（含 success / cmd / gate 结论）
    """
    ctx = _context or {}
    dry_run = bool(ctx.get("dry_run", dry_run))

    result: Dict[str, Any] = {
        "node": "wave_gate",
        "success": False,
        "dry_run": dry_run,
        "region": region,
        "dataset": dataset,
        "wave": str(wave),
        "steps": [],
    }

    # ---- 零成本前置 1：脚本存在性 ----
    if not os.path.isfile(_WAVE_GATE):
        result["step"] = "find_wave_gate"
        result["error"] = f"wave_gate.py 不存在：{_WAVE_GATE}"
        return result
    result["steps"].append({"step": "find_wave_gate", "success": True})

    # ---- 零成本前置 2：战役目录 ----
    camp = campaign_dir or resolve_campaign_dir(region)
    if not camp:
        result["step"] = "resolve_campaign_dir"
        result["error"] = f"找不到战役目录（region={region}）；请传 campaign_dir 或先建 tracking/{region}/config"
        return result
    result["steps"].append({"step": "resolve_campaign_dir", "success": True, "campaign_dir": camp})

    # ---- 零成本前置 3：候选来源至少要有一个 ----
    if not from_db and not any((exprs_file, candidates, expr)):
        result["step"] = "candidate_source"
        result["error"] = "from_db=False 时必须给 exprs_file / candidates / expr 之一"
        return result

    # ---- 构建命令 ----
    cmd = [
        wq_py(), "-u", _WAVE_GATE,
        "--campaign-dir", camp,
        "--region", region,
        "--dataset", dataset,
        *(["--datasets", str(datasets)] if datasets else []),
        "--wave", str(wave),
    ]
    if from_db:
        cmd.append("--from-db")
    if exprs_file:
        cmd += ["--exprs-file", exprs_file]
    if candidates:
        cmd += ["--candidates", candidates]
    if expr:
        cmd += ["--expr", expr]
    if skip_diversity_gate:
        cmd.append("--skip-diversity-gate")
    if fix:
        cmd.append("--fix")
    if inspect_mode:
        cmd += ["--inspect-mode", str(inspect_mode)]
    # 闸 PF：CLI 侧 --prod-family-gate 默认开，节点侧显式透传（保证调用侧显式值生效）
    cmd.append("--prod-family-gate" if prod_family_gate else "--no-prod-family-gate")

    # ---- 零成本前置 4：argv 契约校验（逮住脚本没声明过的 --flag / 子命令）----
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
        result["steps"].append({"step": "dry_run", "success": True, "message": "已构建命令并过契约校验，未执行"})
        return result

    # ---- 实跑（2026-09-20 改：日志文件 + 进程树超时，见 _common.run_logged_subprocess）----
    # 此前 subprocess.run(capture_output=True, timeout=1800)：GLB s2_ipv_families_d1 实测
    # 在 MCP 服务内卡满 1800s 才回"超时"，同一命令终端 <1s；超时后输出全丢、孤儿不杀。
    # 门禁是本地零配额短脚本，默认 600s 已远超正常耗时；超时即杀整棵树并回日志尾。
    try:
        _to = float(timeout_sec or os.environ.get("WQB_WAVE_GATE_TIMEOUT_SEC") or DEFAULT_TIMEOUT_SEC)
    except (TypeError, ValueError):
        _to = DEFAULT_TIMEOUT_SEC
    run_info = run_logged_subprocess(
        cmd,
        log_name=f"wave_gate_{region}_{dataset}_{wave}",
        timeout_sec=_to,
        cwd=str(REPO_ROOT),
        env=unbuffered_env(),
    )
    result["log_path"] = run_info["log_path"]
    result["elapsed_sec"] = run_info["elapsed_sec"]
    result["stdout_tail"] = run_info["tail"]
    if run_info["timed_out"]:
        result["step"] = "run_wave_gate"
        result["timed_out"] = True
        result["error"] = (
            f"wave_gate 超时（{int(_to)}s，已杀整棵进程树）。完整输出见 {run_info['log_path']}；"
            "等价 CLI：" + subprocess.list2cmdline(cmd)
        )
        result["steps"].append({"step": "run_wave_gate", "success": False, "timed_out": True})
        return result

    proc_rc = run_info["returncode"]
    result["returncode"] = proc_rc
    result["success"] = proc_rc == 0
    result["inspect_mode"] = str(inspect_mode or os.environ.get("WQB_INSPECT_MODE") or "warn")
    # 体检硬门状态自报（2026-09-17 P1-1）：未生效 / fail-closed 拦截都单列出来，
    # 便于 Agent 直接提示用户「先补体检包」而不是让约束静默裸奔。
    _tail = (result.get("stdout_tail") or "") + (result.get("stderr_tail") or "")
    if "体检硬门未生效" in _tail:
        result["inspect_status"] = "unavailable"
        result["warning"] = (
            "本波体检硬门未生效（缺 field_inspect 包）——预处理约束无人把关。"
            "开新数据集前先生成：python tools/gen_field_inspect_packs.py "
            "--region <REGION> --delay <D>"
        )
    elif "体检硬门 fail-closed 拦截" in _tail:
        result["inspect_status"] = "enforced_block"
        result["warning"] = "本波被体检 fail-closed 拦截（缺体检包，inspect-mode=enforce）"
    elif result["success"]:
        result["inspect_status"] = "ok"
    result["steps"].append({"step": "run_wave_gate", "success": result["success"]})
    return result
