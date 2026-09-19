# -*- coding: utf-8 -*-
"""campaign 节点：S1-S6 战役阶段执行.

包装 wq-brain-campaign-toolkit 的各阶段脚本，消除 --campaign-dir 手工传递。

2026-09-03 根治：subprocess.run → Popen 异步化，避免 MCP 客户端超时。
子进程在后台运行，结果写入临时 JSON，调用方通过 task_file 轮询。
"""

import json
import logging
import os
import re
import sqlite3
import subprocess
import threading
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..mcp_check import require_mcp_tools
from .._common import (
    REPO_ROOT,
    resolve_campaign_dir,
    resolve_db_path,
    resolve_toolkit_dir,
    resolve_tools_dir,
    unbuffered_env,
    validate_argv,
    wq_py,
)

#: 走 campaign.py 子命令路由的 subcommand——**subcommand 优先于 stage**（见 run() 内
#: `if subcommand and subcommand in subcommand_script_map`）。因此传什么 stage 都能路由到
#: campaign.py，stage 只决定超时预算。约定：assemble-priors 属 S2（priors 是 S2 上游产物）、
#: diversity-extract 属 S2、ledger/registry/wave 属 S6；不要因 stage 分支再 append 一次。
_SUBCOMMAND_ROUTED = ("assemble-priors", "diversity-extract")

logger = logging.getLogger(__name__)

#: 每阶段子进程超时预算（秒）。2026-09-06 修复：此前一律 3600s ——
#: S0 校准是纯本地计算（EUR/USA 实测 <1s），却能把整整一小时烧在"看不见的挂起"上。
#: 预算按各阶段的实测量级给足余量：跑不完说明卡住了，早停早暴露。
_STAGE_TIMEOUTS = {
    "S0": 900,    # 评分走平台分页（EUR 实测 49s）；--calibrate 纯本地
    "S1": 1800,   # scan_fields 全字段扫描（字段多的区域偏慢）
    "S2": 900,    # build_wave 组波
    "S3": 3600,   # pipeline 回测编排（七槽填槽，最长的一档）
    "S4": 900,    # review_wave
    "S5": 600,    # quota
    "S6": 600,    # ledger/registry/wave 回写
}
_CALIBRATE_TIMEOUT = 600      # S0 --calibrate：脚本自身 300s 软超时，外层再留一倍兜底
_DEFAULT_TIMEOUT = 3600
_LOG_TAIL_CHARS = 2000
_LOG_READ_CAP = 4 * 1024 * 1024  # 读回子进程日志的上限，防止异常刷屏撑爆内存


def _stage_timeout(stage: str, calibrate: bool = False) -> int:
    """按阶段返回子进程超时预算（WQB_CAMPAIGN_TIMEOUT 可全局覆盖）。"""
    env = os.environ.get("WQB_CAMPAIGN_TIMEOUT")
    if env:
        try:
            return max(1, int(float(env)))
        except ValueError:
            logger.warning(f"Invalid WQB_CAMPAIGN_TIMEOUT={env!r}, falling back to stage default")
    if stage == "S0" and calibrate:
        return _CALIBRATE_TIMEOUT
    return _STAGE_TIMEOUTS.get(stage, _DEFAULT_TIMEOUT)


def _read_log(path: str, tail: Optional[int] = None) -> str:
    """读回子进程日志。子进程直写文件，因此超时被杀后输出依然留存。"""
    try:
        size = os.path.getsize(path)
        with open(path, "rb") as f:
            if size > _LOG_READ_CAP:
                f.seek(size - _LOG_READ_CAP)
            raw = f.read()
    except OSError:
        return ""
    # 统一换行：原先走 text=True 时由 universal newlines 归一，改文件捕获后
    # 需显式归一，否则 Windows 的 CRLF 会混进摘要提取与 ledger 里的 stdout_tail。
    text = raw.decode("utf-8", "replace")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text[-tail:] if tail else text


def _fail_step(result: Dict[str, Any], step: str, error: str) -> Dict[str, Any]:
    """记录失败步骤，并同步写顶层 success/error。

    2026-09-05 修复：此前失败原因只进 result["steps"][-1]，顶层仅 success=False，
    直连调用方（不经 executor）拿不到任何原因。现两处都写。
    """
    result["steps"].append({"step": step, "success": False, "error": error})
    result["success"] = False
    result["error"] = error
    return result


@require_mcp_tools("campaign")
def run(
    region: str,
    stage: str,
    dataset: Optional[str] = None,
    wave: Optional[str] = None,
    subcommand: Optional[str] = None,
    extra_args: Optional[List[str]] = None,
    calibrate: bool = False,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """执行战役阶段.

    Args:
        region: 区域代码
        stage: 阶段（S0/S1/S2/S3/S4/S5/S6）
        dataset: 数据集 ID（如需要）
        wave: 波次号（如需要）
        subcommand: 子命令（如 ledger/registry/wave/assemble-priors/diversity-extract）
        extra_args: 额外参数列表
        calibrate: S0 专用——是否运行 calibrate 交互审批
        _context: 执行上下文

    Returns:
        执行结果字典
    """
    ctx = _context or {}
    store = ctx.get("store")

    # 构建 campaign-dir（基于仓库根，避免相对路径依赖 cwd）
    campaign_dir = resolve_campaign_dir(region)

    result = {
        "region": region,
        "stage": stage,
        "dataset": dataset,
        "wave": wave,
        "campaign_dir": campaign_dir,
        "steps": [],
        "success": False,
    }

    # 验证战役目录
    if not campaign_dir:
        return _fail_step(
            result,
            "validate_campaign_dir",
            f"Cannot resolve campaign_dir for region={region}. "
            "Set WQB_CAMPAIGN_DIR or WQB_WORKSPACE_ROOT, or create tracking/<region>/.",
        )
    if not os.path.exists(campaign_dir):
        return _fail_step(result, "validate_campaign_dir", f"Campaign directory not found: {campaign_dir}")

    # 阶段必填参数校验（2026-09-15 审计缺陷 B）：registry 层 required_params 只有
    # region/stage，dataset 是 optional —— S1 缺 dataset 会构建出无对象的
    # scan_fields 命令，dry-run 放行、实跑静默空转。此处按 stage 细化：
    # S1 必须有 dataset（扫描对象）；S2 的 dataset 合法可选（build_wave 可从库
    # 跨集重取，无 dataset 时 preflight 走 warning-skip，既有契约）；
    # S4 的 wave 必填在下方 S4 分支已有显式检查。subcommand 路由
    # （assemble-priors 等）不依赖 dataset/wave，不受此校验约束。
    if subcommand not in _SUBCOMMAND_ROUTED:
        _stage_required = {"S1": ("dataset",)}
        _missing = [p for p in _stage_required.get(stage, ()) if not locals().get(p)]
        if _missing:
            return _fail_step(
                result,
                "validate_stage_params",
                f"stage={stage} 缺少必填参数: {', '.join(_missing)}。"
                f"（S1=字段扫描需 dataset；S2 的 dataset 可选——build_wave 可从库重取）",
            )

    result["steps"].append({
        "step": "validate_campaign_dir",
        "success": True,
        "campaign_dir": campaign_dir,
    })

    # 自动创建 config/settings.json（缺省时从 DB ledger 推导，P0 修复）
    _ensure_campaign_config(campaign_dir, region, result)

    # 定位 toolkit
    toolkit_dir = resolve_toolkit_dir()
    if not toolkit_dir:
        return _fail_step(result, "find_toolkit", "wq-brain-campaign-toolkit not found")

    # 根据 stage 路由到对应脚本
    script_map = {
        "S0": "score_datasets.py",
        "S1": "scan_fields.py",
        "S2": "build_wave.py",
        "S3": "pipeline.py",
        "S4": "review_wave.py",
        "S5": "pipeline.py",  # quota
        "S6": "campaign.py",  # ledger/registry/wave
    }

    # subcommand 路由：S6 的 ledger/registry/wave + S2 的 assemble-priors/diversity-extract
    subcommand_script_map = {
        "assemble-priors": "campaign.py",
        "diversity-extract": "campaign.py",
    }

    # ── 缓存检查：calibrate / assemble-priors 结果缓存到 ledger（Dry-Run 2.0 优化） ──
    if store and not ctx.get("dry_run"):
        cache_key = None
        if stage == "S0" and calibrate:
            cache_key = f"s0_calibrate_{region}"
        elif subcommand == "assemble-priors":
            # 2026-09-17 P2-12：本键原为 `priors_snapshot_{region}`，与
            # `assemble_priors.py` 落的**真实 payload** 键 `priors_snapshot_<region.lower()>`
            # 仅大小写之差 → 同名不同物（本处是 cache marker，payload 在另一键），
            # 查询 `priors_snapshot_<REGION>` 会拿到不含 wins/dead_ends 的缓存标记。
            # 改为独立命名，与 `s0_calibrate_*` 同族，彻底消除大小写撞键。
            cache_key = f"assemble_priors_cache_{region}"

        if cache_key:
            try:
                cached = store.get_ledger(region, cache_key)
                if cached and cached.get("value"):
                    result["steps"].append({
                        "step": "cache_hit",
                        "success": True,
                        "cache_key": cache_key,
                        "message": f"Using cached {cache_key} from ledger",
                    })
                    result["success"] = True
                    result["cached"] = True
                    result["cache_key"] = cache_key
                    return result
            except Exception as e:
                logger.warning(f"Failed to check cache {cache_key}: {e}")

    if subcommand and subcommand in subcommand_script_map:
        script_name = subcommand_script_map[subcommand]
    else:
        script_name = script_map.get(stage)
    if not script_name:
        return _fail_step(result, "route_stage", f"Unknown stage: {stage}")

    script_path = os.path.join(toolkit_dir, script_name)
    if not os.path.exists(script_path):
        return _fail_step(result, "route_stage", f"Script not found: {script_path}")

    # 构建命令
    # 2026-09-08：解释器加 `-u`（与 batch_track 同源修复）。子进程 stdout 重定向到
    # <task_id>.out，Python 默认块缓冲 —— 长跑阶段（S3 最长 3600s）运行中 tail 不到
    # 任何东西，进程被超时 kill 时未满的缓冲还会整段丢失。
    cmd = [wq_py(), "-u", script_path, "--campaign-dir", campaign_dir]

    # 添加 stage 特定参数
    if stage == "S0":
        # score_datasets.py 只认 --campaign-dir，region 从 campaign-dir 推导
        # 删除多余的 --region 参数（2026-09-03 修复 returncode 2 根因）
        if calibrate:
            cmd.append("--calibrate")
    elif stage == "S1":
        if dataset:
            cmd.extend(["--dataset", dataset])
        # 添加缓存参数支持
        if extra_args:
            # 检查是否包含缓存相关参数
            if "--force-refresh" in extra_args:
                cmd.append("--force-refresh")
            if "--cache-ttl" in extra_args:
                # 找到 --cache-ttl 参数的值
                try:
                    ttl_idx = extra_args.index("--cache-ttl")
                    if ttl_idx + 1 < len(extra_args):
                        ttl_value = extra_args[ttl_idx + 1]
                        cmd.extend(["--cache-ttl", ttl_value])
                except (ValueError, IndexError):
                    pass  # 如果参数格式不正确，忽略
            # 移除已处理的缓存参数，避免重复传递
            extra_args = [arg for arg in extra_args if arg not in ["--force-refresh", "--cache-ttl"]]
            # 移除 --cache-ttl 的值
            if "--cache-ttl" in extra_args:
                try:
                    ttl_idx = extra_args.index("--cache-ttl")
                    if ttl_idx + 1 < len(extra_args):
                        extra_args.pop(ttl_idx + 1)  # 移除值
                    extra_args.pop(ttl_idx)  # 移除参数名
                except (ValueError, IndexError):
                    pass
    elif stage == "S2":
        # 信号天花板闸：纯 DB 判定、零配额，故 dry-run 也走 —— 干跑就该回答
        # "这个区还值不值得继续开波"。
        floor_result = _run_signal_floor_gate(region, dataset, campaign_dir)
        result["steps"].append(floor_result)
        if not floor_result.get("success", True):
            result["success"] = False
            result["error"] = floor_result.get("error")
            return result
        # 停止规则（2026-09-15 ⑦）：yield=0@≥100 / 连续 3 波 FAIL，同样零配额、干跑也走
        stop_result = _run_stop_rules_gate(region, dataset, campaign_dir)
        result["steps"].append(stop_result)
        if not stop_result.get("success", True):
            result["success"] = False
            result["error"] = stop_result.get("error")
            return result
        # 积压闸（2026-09-15 行动 3）：conversion/积压比前置判定，零配额，干跑也走
        backlog_result = _run_backlog_gate(region, dataset, campaign_dir)
        result["steps"].append(backlog_result)
        if not backlog_result.get("success", True):
            result["success"] = False
            result["error"] = backlog_result.get("error")
            return result

        # S2 前强制前置条件预检（S0/S1 产物门禁）。
        # dry-run 下跳过预检子进程（零副作用），仅构建 build_wave 命令。
        if not ctx.get("dry_run"):
            preflight_result = _run_preflight(
                region=region,
                dataset=dataset,
                wave=wave,
                campaign_dir=campaign_dir,
                py=wq_py(),
                store=store,
            )
            result["steps"].append(preflight_result)

            # 预检 FAIL（前置产物缺失）则中止，禁止带着缺白名单的状态烧配额
            if not preflight_result.get("success", False):
                error = preflight_result.get("error", "Preflight failed")
                result["steps"].append({
                    "step": "preflight_block",
                    "success": False,
                    "error": error,
                    "preflight": preflight_result,
                })
                result["success"] = False
                result["error"] = error
                return result

        # 2026-09-12 修复(2)：S2 的 script_map 指向 build_wave.py **本体**，它没有
        # `build-wave` 子命令（那是 campaign.py 分发器的入口名）。此前无条件追加
        # `["build-wave", "--from-db"]` 拼出 `build_wave.py ... --wave W build-wave --from-db`，
        # 多出的位置参数被 argparse 拒绝（rc=2）；而 validate_argv 只校验子命令/选项、
        # 不校验多余位置参数，干跑也放行。subcommand 路由（assemble-priors 等）时脚本
        # 已切到 campaign.py，本分支不得再拼任何 build_wave 参数，交给下方路由块。
        if subcommand not in _SUBCOMMAND_ROUTED:
            if dataset:
                cmd.extend(["--dataset", dataset])
            if wave:
                cmd.extend(["--wave", wave])
            cmd.append("--from-db")
    elif stage == "S3":
        # 信号天花板闸（同 S2：纯 DB 判定，dry-run 也走）
        floor_result = _run_signal_floor_gate(region, dataset, campaign_dir)
        result["steps"].append(floor_result)
        if not floor_result.get("success", True):
            result["success"] = False
            result["error"] = floor_result.get("error")
            return result
        stop_result = _run_stop_rules_gate(region, dataset, campaign_dir)
        result["steps"].append(stop_result)
        if not stop_result.get("success", True):
            result["success"] = False
            result["error"] = stop_result.get("error")
            return result
        # 积压闸（同 S2：conversion/积压比前置判定，零配额，干跑也走）
        backlog_result = _run_backlog_gate(region, dataset, campaign_dir)
        result["steps"].append(backlog_result)
        if not backlog_result.get("success", True):
            result["success"] = False
            result["error"] = backlog_result.get("error")
            return result

        # S3 前强制质量闸（特征工程 SOP 阶段6）。
        # dry-run 下跳过质量闸子进程（零副作用），仅构建 pipeline run 命令。
        if not ctx.get("dry_run"):
            quality_gate_result = _run_quality_gate(
                region=region,
                dataset=dataset,
                wave=wave,
                campaign_dir=campaign_dir,
                py=wq_py(),
            )
            result["steps"].append(quality_gate_result)

            # 如果质量闸失败且要求 block，则中止
            if not quality_gate_result.get("success", False):
                error = "Quality gate failed, blocking S3 execution"
                result["steps"].append({
                    "step": "quality_gate_block",
                    "success": False,
                    "error": error,
                    "quality_gate": quality_gate_result,
                })
                result["success"] = False
                result["error"] = error
                return result

        # 质量闸通过，继续 pipeline.py
        cmd.append("run")
        if dataset:
            cmd.extend(["--dataset", dataset])
        if wave:
            cmd.extend(["--wave", wave])
        cmd.extend(["--review", "--write-ledger"])
    elif stage == "S4":
        # 2026-09-15 ④：review_wave.py 要求 --multisim 或 --alphas，此前节点只传 --tag，
        # 实跑必 `error: need --multisim or --alphas`（rc=2，campaign_USA_S4_20260903 实证）
        # 而干跑因 argv 静态契约通过而报 success。现从库解析本波 alpha_id 再拼命令。
        if not wave:
            result["steps"].append({
                "step": "resolve_s4_alphas", "success": False,
                "error": "S4 需要 wave（用于从 backtest_results 解析本波 alpha_id）",
            })
            result["success"] = False
            result["error"] = "S4 requires wave"
            return result
        alpha_ids, resolved_wave, available = _resolve_wave_alpha_ids(region, wave, dataset)
        if not alpha_ids:
            hint = f"该 region 最近的波次: {available[:10]}" if available else "该 region 尚无 backtest_results"
            result["steps"].append({
                "step": "resolve_s4_alphas", "success": False,
                "error": f"backtest_results 中找不到 region={region} wave={wave} 的 alpha（{hint}）；"
                         "先跑步 6 回测，或用 review_wave.py --multisim <id> 手动评审",
            })
            result["success"] = False
            result["error"] = f"no backtest alphas for {region}/{wave}"
            return result
        result["steps"].append({
            "step": "resolve_s4_alphas", "success": True,
            "wave": resolved_wave, "alpha_count": len(alpha_ids),
        })
        cmd.extend(["--alphas", *alpha_ids])
        cmd.extend(["--tag", str(resolved_wave)])
        cmd.append("--write-ledger")
    elif stage == "S5":
        cmd.append("quota")
    elif stage == "S6":
        # 2026-09-06 修复：此处原本无条件 append(subcommand)，下面的 subcommand
        # 路由块又 append 一次 —— ra-pipeline 步 4 的
        # `workflow_campaign(stage="S6", subcommand="assemble-priors")`
        # 实际生成 `campaign.py ... assemble-priors assemble-priors`。
        # 现在 assemble-priors / diversity-extract 统一交给下面的路由块处理，
        # 本分支只处理 S6 自有子命令（ledger / registry / wave）。
        if subcommand and subcommand not in _SUBCOMMAND_ROUTED:
            cmd.append(subcommand)
        if wave and subcommand not in _SUBCOMMAND_ROUTED:
            cmd.extend(["--wave", wave])

    # subcommand 路由：assemble-priors / diversity-extract（走 campaign.py 子命令）
    if subcommand in _SUBCOMMAND_ROUTED:
        cmd.append(subcommand)
        if dataset:
            cmd.extend(["--dataset", dataset])
        if wave:
            cmd.extend(["--wave", wave])

    # 添加额外参数
    if extra_args:
        cmd.extend(extra_args)

    # argv 契约校验：命令必须能被目标脚本的 argparse 接受。
    # 干跑与实跑都走 —— 干跑时这是本节点最有价值的一次检查
    # （本次审计正是靠它暴露了 assemble-priors 的重复 append）。
    argv_ok, argv_error = validate_argv(cmd)
    if not argv_ok:
        result["steps"].append({
            "step": "validate_argv",
            "success": False,
            "error": argv_error,
            "command": " ".join(cmd),
        })
        result["success"] = False
        result["error"] = argv_error
        return result

    result["steps"].append({
        "step": "build_command",
        "success": True,
        "command": " ".join(cmd),
    })

    # 2026-09-01 dry-run 支持：_context.dry_run=True 时构建到命令即停，
    # 返回待执行命令与工作目录（不 subprocess、不写库）。
    if ctx.get("dry_run"):
        result["success"] = True
        result["dry_run"] = True
        result["note"] = "dry-run：命令已构建，未执行"
        return result

    # 2026-09-03 根治：异步执行 — Popen 启动子进程后立即返回，
    # 后台线程等待完成并写入结果文件。避免 MCP 客户端超时（原 subprocess.run 阻塞 3600s）。
    task_id = f"campaign_{region}_{stage}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    # 2026-09-04 修复：任务目录支持 WQB_TASK_ROOT 注入（单测隔离，默认仓库 logs/_async_tasks）
    task_dir = os.environ.get("WQB_TASK_ROOT") or os.path.join(REPO_ROOT, "logs", "_async_tasks")
    os.makedirs(task_dir, exist_ok=True)
    task_file = os.path.join(task_dir, f"{task_id}.json")

    # 2026-09-06 修复：子进程输出直写文件而非 PIPE。三个收益：
    #   ① 运行中可实时 tail，不必等进程结束才知道跑到哪一步（此前挂起一小时零可见输出）；
    #   ② 超时被 kill 后输出仍在盘上 —— 原实现在 TimeoutExpired 分支丢弃 communicate
    #      的输出，"零 stdout" 于是既非证据也无从复盘；
    #   ③ 从根上消除 PIPE 缓冲区写满导致的父子互锁。
    stdout_log = os.path.join(task_dir, f"{task_id}.out")
    stderr_log = os.path.join(task_dir, f"{task_id}.err")
    timeout_sec = _stage_timeout(stage, calibrate=calibrate)

    try:
        logger.info(f"Executing campaign {stage} (async, timeout={timeout_sec}s): {' '.join(cmd)}")

        # 子进程 stdout 编码固定 UTF-8：重定向到文件时 Python 默认走 locale 编码
        # （本机 cp936），中文结论行会因编码不一致读成乱码。
        # PYTHONUNBUFFERED 由 unbuffered_env 注入（连子进程再 spawn 的进程一起管住），
        # 它同时把 BRAIN 凭证桥接成 toolkit 认的 WQ_USERNAME/WQ_PASSWORD ——
        # S3 路由到 pipeline.py，那条链要登录平台。
        child_env = unbuffered_env({"PYTHONIOENCODING": "utf-8"})
        popen_kwargs: Dict[str, Any] = {
            # stdin 显式断开：不继承 MCP 服务进程的 stdin，杜绝子进程误读标准输入永久阻塞
            "stdin": subprocess.DEVNULL,
            "cwd": toolkit_dir,
            "env": child_env,
        }
        if os.name == "nt":
            # 2026-09-04 修复：脱离父进程组——MCP 服务进程退出不带走后台子进程
            popen_kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
        out_f = err_f = None
        try:
            out_f = open(stdout_log, "wb")
            err_f = open(stderr_log, "wb")
            process = subprocess.Popen(cmd, stdout=out_f, stderr=err_f, **popen_kwargs)
        finally:
            # 父进程侧句柄用完即关（子进程已各自持有副本），避免 Windows 上占着文件；
            # 开第二个文件或 Popen 失败时同样要收回已开的句柄
            for fh in (out_f, err_f):
                if fh is not None:
                    try:
                        fh.close()
                    except OSError:
                        pass

        # 2026-09-04 修复：主线程先写 running 占位——即使收尾线程随 MCP 进程退出被杀，
        # 轮询方也能读到 status=running 而非"任务文件不存在"（收尾线程完成时覆盖终态）。
        try:
            with open(task_file, "w", encoding="utf-8") as f:
                json.dump({
                    "task_id": task_id,
                    "status": "running",
                    "pid": process.pid,
                    "started_at": datetime.now().isoformat(),
                    "timeout_sec": timeout_sec,
                    "stdout_log": stdout_log,
                    "stderr_log": stderr_log,
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.warning(f"Failed to write running placeholder {task_file}: {e}")

        # 后台线程：等待进程完成并收集结果
        def _wait_and_collect():
            try:
                # stdout/stderr 已重定向到文件，communicate 只用于等待+回收；
                # 返回值在真实路径下为 None，测试替身会给字符串，两者都兼容。
                pipe_out, pipe_err = process.communicate(timeout=timeout_sec)
                stdout = pipe_out if pipe_out else _read_log(stdout_log)
                stderr = pipe_err if pipe_err else _read_log(stderr_log)
                success = process.returncode == 0
                exec_result = {
                    "task_id": task_id,
                    "success": success,
                    "returncode": process.returncode,
                    "stdout_tail": stdout[-_LOG_TAIL_CHARS:] if stdout else "",
                    "stderr_tail": stderr[-_LOG_TAIL_CHARS:] if stderr else "",
                    "stdout_log": stdout_log,
                    "stderr_log": stderr_log,
                    "timeout_sec": timeout_sec,
                    "finished_at": datetime.now().isoformat(),
                }
                # 结构化摘要
                summary = _extract_structured_summary(stdout or "", stage)
                if summary:
                    exec_result["structured_summary"] = summary

                # S4 walls 诊断
                if stage == "S4":
                    walls = _extract_walls_summary(stdout or "")
                    if walls:
                        exec_result["walls"] = walls

            except subprocess.TimeoutExpired:
                # 2026-09-04 修复：超时后 kill 子进程并回收——否则孤儿进程继续占平台槽位
                try:
                    process.kill()
                    process.communicate(timeout=30)
                except Exception:
                    pass
                # 2026-09-06 修复：保留被杀前已写盘的输出。原实现在这里什么都不留，
                # 于是 campaign_USA_S0_20260905_222757 只剩一行 "Timeout after 3600s"，
                # 既无法判断卡在哪一步、也无法证明子进程到底有没有产出。
                exec_result = {
                    "task_id": task_id,
                    "success": False,
                    "error": f"Timeout after {timeout_sec}s (process killed)",
                    "returncode": process.returncode,
                    "partial_output": True,
                    "stdout_tail": _read_log(stdout_log, _LOG_TAIL_CHARS),
                    "stderr_tail": _read_log(stderr_log, _LOG_TAIL_CHARS),
                    "stdout_log": stdout_log,
                    "stderr_log": stderr_log,
                    "timeout_sec": timeout_sec,
                    "finished_at": datetime.now().isoformat(),
                }
            except Exception as e:
                exec_result = {
                    "task_id": task_id,
                    "success": False,
                    "error": str(e),
                    "finished_at": datetime.now().isoformat(),
                }

            # 写入结果文件
            try:
                with open(task_file, "w", encoding="utf-8") as f:
                    json.dump(exec_result, f, indent=2, ensure_ascii=False)
            except Exception as e:
                logger.error(f"Failed to write task result {task_file}: {e}")

            # 2026-09-04 修复：收尾线程重建独立 sqlite 连接（复用主线程连接跨线程使用
            # 会抛 sqlite3.ProgrammingError，fe ledger_error 实证）。闭包内用原参数名
            # 重赋值会把 store 解析为局部变量并 UnboundLocalError，故用 thread_store。
            thread_store = None
            if store is not None and hasattr(store, "path"):
                try:
                    thread_store = store.__class__(store.path)
                except Exception as e:
                    logger.warning(f"Failed to reopen store in collector thread: {e}")

            # 保存到 DB
            if thread_store and exec_result.get("success"):
                try:
                    thread_store.upsert_ledger("WORKFLOW", f"campaign_{region}_{stage}_{datetime.now().strftime('%Y%m%d')}", {
                        "executed_at": datetime.now().isoformat(),
                        "region": region,
                        "stage": stage,
                        "dataset": dataset,
                        "wave": wave,
                        "task_id": task_id,
                    })
                except Exception as e:
                    logger.warning(f"Failed to save campaign record: {e}")

            # 缓存 calibrate / assemble-priors 结果到 ledger
            if thread_store and exec_result.get("success"):
                try:
                    if stage == "S0" and calibrate:
                        thread_store.upsert_ledger(region, f"s0_calibrate_{region}", {
                            "calibrated_at": datetime.now().isoformat(),
                            "region": region,
                            "stdout_tail": exec_result.get("stdout_tail", ""),
                        })
                    elif subcommand == "assemble-priors":
                        # 与上方 cache_key 同名（2026-09-17 P2-12：不再用 priors_snapshot_{region}）
                        thread_store.upsert_ledger(region, f"assemble_priors_cache_{region}", {
                            "assembled_at": datetime.now().isoformat(),
                            "region": region,
                            "stdout_tail": exec_result.get("stdout_tail", ""),
                        })
                except Exception as e:
                    logger.warning(f"Failed to cache result: {e}")

            # 2026-09-04 方案 C：S6 回写后自动学习 Mode B 资格线（证据驱动自适应）
            if thread_store and exec_result.get("success") and stage == "S6":
                try:
                    from ..mode_b_adaptive import update_mode_b_qualification
                    mbq_update = update_mode_b_qualification(thread_store, region, dry_run=False)
                    if mbq_update.get("updated"):
                        logger.info(
                            f"Mode B qualification auto-updated for {region}: "
                            f"{mbq_update.get('old')} -> {mbq_update.get('new')}"
                        )
                except Exception as e:
                    logger.warning(f"Failed to auto-update mode_b_qualification: {e}")

            # S4 walls 诊断入库
            if thread_store and exec_result.get("success") and stage == "S4":
                try:
                    walls_summary = exec_result.get("walls")
                    if walls_summary:
                        thread_store.upsert_ledger(region, f"s4_walls_{region}_{wave or 'unknown'}", {
                            "reviewed_at": datetime.now().isoformat(),
                            "region": region,
                            "wave": wave,
                            "walls": walls_summary,
                        })
                except Exception as e:
                    logger.warning(f"Failed to save walls summary: {e}")

        bg_thread = threading.Thread(target=_wait_and_collect, daemon=True)
        bg_thread.start()

        result["steps"].append({
            "step": "execute",
            "success": True,
            "async": True,
            "pid": process.pid,
            "task_id": task_id,
            "task_file": task_file,
            "stdout_log": stdout_log,
            "stderr_log": stderr_log,
            "timeout_sec": timeout_sec,
            "message": (f"Campaign {stage} launched in background (pid={process.pid}, "
                        f"timeout={timeout_sec}s). Poll {task_file} for result; "
                        f"tail {stdout_log} / {stderr_log} for live progress."),
        })
        result["success"] = True
        result["async"] = True
        result["task_id"] = task_id
        result["task_file"] = task_file
        result["stdout_log"] = stdout_log
        result["stderr_log"] = stderr_log
        result["timeout_sec"] = timeout_sec
        result["pid"] = process.pid

    except Exception as e:
        logger.exception(f"Campaign {stage} launch failed")
        result["steps"].append({
            "step": "execute",
            "success": False,
            "error": str(e),
        })

    return result


# _find_toolkit_dir 已迁至 _common.resolve_toolkit_dir（单一事实源）


def _run_preflight(
    region: str,
    dataset: Optional[str],
    wave: Optional[str],
    campaign_dir: str,
    py: str,
    store: Any = None,
) -> Dict[str, Any]:
    """波次前置条件预检（S0/S1 产物门禁，S2/S3 前强制）.

    校验字段 catalog（文件 + DB 单一事实源）、新鲜度与判死清单。
    通用修复入口：FAIL 时按 remediation 跑 tools/preflight_wave.py --repair。
    
    2026-09-12 增强：预检成功后自动补录 S2 合规记录（如缺失）。
    """
    result = {
        "step": "preflight",
        "success": True,
        "preflight_output": None,
    }

    if not dataset:
        result["warning"] = "no dataset specified, skip preflight"
        return result

    # 脚本路径基于 REPO_ROOT（单一事实源）；勿用 __file__ 逐级 dirname
    # ——src/wqb/workflow/nodes/ 距仓库根 4 层，少一层会指到 src/ 导致门禁静默失效。
    preflight_script = os.path.join(resolve_tools_dir(), "preflight_wave.py")
    if not os.path.exists(preflight_script):
        result["warning"] = f"preflight script not found: {preflight_script}"
        return result

    cmd = [py, preflight_script, "--campaign-dir", campaign_dir,
           "--dataset", dataset, "--quiet"]
    if wave:
        cmd.extend(["--wave", str(wave)])

    try:
        logger.info(f"Running preflight: {' '.join(cmd)}")
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
            cwd=str(REPO_ROOT),
        )
        tail = (proc.stdout or "")[-2000:]
        result["preflight_output"] = {
            "returncode": proc.returncode,
            "stdout_tail": tail,
            "stderr_tail": (proc.stderr or "")[-500:],
        }
        if proc.returncode != 0:
            result["success"] = False
            result["error"] = (
                "Preflight FAIL: S0/S1 前置产物缺失，禁止进入 S2/S3 烧配额。"
                f"修复: {py} {preflight_script} --campaign-dir {campaign_dir} "
                f"--dataset {dataset} --repair"
            )
            return result
        
        # 2026-09-12 增强：预检成功后自动补录 S2 合规记录（如缺失）
        if wave and store:
            s2_key = f"s2_compliance_w{wave}"
            try:
                existing = store.get_ledger(region, s2_key)
                if not existing:
                    # 从 S1 ledger 读取 ideas_md_path
                    s1_key = f"s1_{dataset}_d1"  # 默认 delay=1
                    s1_record = store.get_ledger(region, s1_key)
                    if s1_record and s1_record.get("ideas_md_path"):
                        s2_data = {
                            "wave": wave,
                            "feature_engineering_doc": s1_record["ideas_md_path"],
                            "candidate_pool_source": "skill",
                            "marked_at": datetime.now().isoformat(),
                            "notes": "auto-marked by preflight (S2 compliance auto-fix)",
                        }
                        store.upsert_ledger(region, s2_key, s2_data)
                        result["s2_compliance_auto_marked"] = True
                        logger.info(f"Auto-marked S2 compliance: {s2_key}")
            except Exception as e:
                logger.warning(f"Failed to auto-mark S2 compliance: {e}")
                # 不阻断流程，仅记录警告
                result["s2_compliance_warning"] = str(e)
                
    except subprocess.TimeoutExpired:
        # 预检自身超时不阻断战役（避免检查器故障锁死流水线），仅记录
        result["warning"] = "Preflight timeout after 300s, proceeding"
    except Exception as e:
        result["warning"] = f"Preflight error (not blocking): {e}"

    return result


def _run_quality_gate(
    region: str,
    dataset: Optional[str],
    wave: Optional[str],
    campaign_dir: str,
    py: str,
) -> Dict[str, Any]:
    """运行质量闸（特征工程 SOP 阶段6，S3 前强制）.

    调用 tools/wave_gate.py --quality-block 进行零配额预检。
    如果存在 EXPECTED_BLOCK 候选，则阻止 S3 执行。
    """
    result = {
        "step": "quality_gate",
        "success": True,
        "expected_block_count": 0,
        "gate_output": None,
    }

    # 构建 wave_gate.py 命令（绝对路径，避免依赖 subprocess cwd）
    # 2026-09-17 优化：去掉 --quality-block（质量预估降级为仅标注）。
    # 根因：质量预估模型不准（model32 预估 WEAK=27/HARD=29 实测 S=1.33；
    # model252 预估 WEAK=10/HARD=24 实测 S=2.37），硬拦截会错过有信号的数据集。
    gate_cmd = [
        py, os.path.join(resolve_tools_dir(), "wave_gate.py"),
        "--campaign-dir", campaign_dir,
        "--from-db",
        # 不再传 --quality-block：质量预估仅标注不拦截
    ]

    if dataset:
        gate_cmd.extend(["--dataset", dataset])
    if wave:
        gate_cmd.extend(["--wave", wave])

    try:
        logger.info(f"Running quality gate: {' '.join(gate_cmd)}")

        gate_proc = subprocess.run(
            gate_cmd,
            capture_output=True,
            text=True,
            timeout=600,
            cwd=str(REPO_ROOT),
        )

        result["gate_output"] = {
            "returncode": gate_proc.returncode,
            "stdout_tail": gate_proc.stdout[-2000:] if gate_proc.stdout else "",
            "stderr_tail": gate_proc.stderr[-2000:] if gate_proc.stderr else "",
        }

        # wave_gate.py 在默认模式（无 --quality-block）下不会因质量预估返回非零。
        # 只有语法/字段/毒模式等硬闸失败才返回非零。
        if gate_proc.returncode != 0:
            result["success"] = False
            result["error"] = "Quality gate blocked: EXPECTED_BLOCK candidates found"

            # 尝试从输出中解析 block 数量
            if gate_proc.stdout:
                import re
                match = re.search(r"EXPECTED_BLOCK[:\：]\s*(\d+)", gate_proc.stdout)
                if match:
                    result["expected_block_count"] = int(match.group(1))

    except subprocess.TimeoutExpired:
        result["success"] = False
        result["error"] = "Quality gate timeout after 600s"
    except Exception as e:
        logger.warning(f"Quality gate failed: {e}")
        # 质量闸失败不阻止执行，只记录警告
        result["warning"] = str(e)

    return result


def _resolve_wave_alpha_ids(region: str, wave: str, dataset: Optional[str]):
    """从 backtest_results 解析本波 alpha_id（S4 评审输入）。

    wave 两套命名并存（战役编号 "61" / GEM 标签 "s2_<ds>_d<delay>"），按序尝试：
    精确匹配 → 有 dataset 时 `s2_<dataset>_d%` 标签。返回 (ids, 命中的 wave, 该区最近波次列表)。
    """
    db_path = resolve_db_path()
    ids: List[str] = []
    hit = str(wave)
    recent: List[str] = []
    try:
        conn = sqlite3.connect(db_path)
        try:
            rows = conn.execute(
                "SELECT DISTINCT alpha_id FROM backtest_results WHERE region=? AND wave=? "
                "AND alpha_id IS NOT NULL AND alpha_id != '' ORDER BY id", (region, str(wave)),
            ).fetchall()
            ids = [r[0] for r in rows]
            if not ids and dataset:
                rows = conn.execute(
                    "SELECT DISTINCT alpha_id, wave FROM backtest_results WHERE region=? "
                    "AND wave LIKE ? AND alpha_id IS NOT NULL AND alpha_id != '' ORDER BY id",
                    (region, f"s2_{dataset}_d%"),
                ).fetchall()
                ids = [r[0] for r in rows]
                if rows:
                    hit = str(rows[-1][1])
            recent = [
                str(w) for (w,) in conn.execute(
                    "SELECT wave FROM backtest_results WHERE region=? AND wave IS NOT NULL "
                    "GROUP BY wave ORDER BY MAX(id) DESC LIMIT 10", (region,))
            ]
        finally:
            conn.close()
    except Exception as e:  # 库不可读 → 当作无结果，由调用方给提示
        logger.warning(f"_resolve_wave_alpha_ids failed: {e}")
    return ids, hit, recent


#: 停止规则默认参数（区域 thresholds.json `diversity.stop_rules` 可覆盖；enabled=false 关闭）
STOP_RULES_DEFAULTS = {
    "enabled": True,
    "yield_min_backtests": 100,     # 区级：回测 ≥N 且达标 0 → 停区
    "consecutive_fail_waves": 3,    # 区级：最近 K 个 closed 波 verdict 全 FAIL → 停区
    "sharpe_min": 1.58,
    "fitness_min": 1.0,
    # ---- 2026-09-17 加固（P0-3 停止闸输入完整性）----
    # verdict 已归一化（见 _normalize_verdict）：自由文本 `0/8 过硬闸` 现算 FAIL，
    # 空值算 UNKNOWN。以下两项控制更严/更保守的可选口径，默认不改变既有拦截面。
    "strict_no_pass": False,        # True → 最近 K 个 closed 波"无任何 PASS"即停区（严于全 FAIL）
    "unknown_warn": True,           # verdict 空/不可识别 → 输出 WARN，但不当作"通过"也不据此拦截
}


#: 积压闸默认参数（区域 thresholds.json `diversity.backlog_gate` 可覆盖；enabled=false 关闭）
BACKLOG_GATE_DEFAULTS = {
    "enabled": True,
    "conversion_min": 0.10,       # 区级 conversion（已回测/已生成）低于此值 → 拦截
    "pending_gated_ratio_max": 0.30,  # pending+gated 占比超此值 → 拦截
    "min_expressions": 200,       # 表达式总量低于此值的新区不判（样本不足）
    # ---- 2026-09-17 P0-2：补齐"未消费"口径 ----
    # 旧口径只算 pending+gated，**漏掉 gem/selected**（数量最大的两类积压）。
    # 实测：DEU pending+gated 仅 6.6% 过闸，但其 gem 存量占全区表达式 72% → 假通过；
    # JPN 首日 gem=1640/pending+gated=0，若非 conversion=0 恰好命中，积压完全不可见。
    "unconsumed_ratio_max": 0.30,     # (gem+selected+pending+gated) 占比上限
    "unconsumed_enforce": False,      # 灰度：默认只报不拦；经确认清单后再置 True
}


def _run_backlog_gate(
    region: str,
    dataset: Optional[str],
    campaign_dir: str,
) -> Dict[str, Any]:
    """区级积压闸（2026-09-15 审计行动 3；S2/S3 前置，零配额）。

    ra-pipeline 步 6「积压清理」与步 1 产出率读法（conversion <10% 的区先清积压
    再开新波）此前只是 prose，DB 实证 7 区违反仍在开新波（GLB 0%、EUR 1%、
    GBR/ASI 3%、CHN/KOR 7%、USA 9%）。本闸把它变成 S2/S3 开波前置硬判定：

      - conversion（status 含 backtested/submitted/completed ÷ 总数）< conversion_min
        且总量 ≥ min_expressions → 拦截（提示先消化近闸积压）
      - pending+gated 占比 > pending_gated_ratio_max 且总量 ≥ min_expressions
        → 拦截（S2→S3 断链，堆库不消化）

    只看库、零平台调用。命中时与 stop_rules 同样支持 ledger `backlog_gate_override`
    {"reason","until"} 显式放行留痕。
    """
    result: Dict[str, Any] = {"step": "backlog_gate", "success": True}
    # 测试/沙箱隔离口：WQB_DISABLE_BACKLOG_GATE=1 时跳过（与 signal_floor 的
    # thresholds 关闭口并行；单测不封库时用，生产路径不受影响）
    if os.environ.get("WQB_DISABLE_BACKLOG_GATE") == "1":
        result["skipped"] = "WQB_DISABLE_BACKLOG_GATE=1"
        return result
    cfg = dict(BACKLOG_GATE_DEFAULTS)
    thresholds_path = os.path.join(campaign_dir, "config", "thresholds.json")
    try:
        with open(thresholds_path, "r", encoding="utf-8") as f:
            thresholds = json.load(f)
        cfg.update((thresholds.get("diversity") or {}).get("backlog_gate") or {})
    except (OSError, json.JSONDecodeError):
        pass
    if cfg.get("enabled") is False:
        result["skipped"] = "backlog_gate disabled in thresholds.json"
        return result

    db_path = resolve_db_path()
    try:
        conn = sqlite3.connect(db_path)
        try:
            row = conn.execute(
                "SELECT value FROM ledger_kv WHERE region=? AND key='backlog_gate_override'",
                (region,),
            ).fetchone()
            override = None
            if row and row[0]:
                try:
                    override = json.loads(row[0]) if isinstance(row[0], (str, bytes)) else row[0]
                except Exception:
                    override = None
            if isinstance(override, dict) and override.get("reason"):
                until = str(override.get("until") or "")
                if not until or until >= datetime.now().strftime("%Y-%m-%d"):
                    result["override"] = {"reason": override.get("reason"), "until": until or None}

            total, bt, pending_gated, gem_n, selected_n = conn.execute(
                "SELECT COUNT(*), "
                "SUM(CASE WHEN status IN ('backtested','submitted','completed') THEN 1 ELSE 0 END), "
                "SUM(CASE WHEN status IN ('pending','gated') THEN 1 ELSE 0 END), "
                "SUM(CASE WHEN status='gem' THEN 1 ELSE 0 END), "
                "SUM(CASE WHEN status='selected' THEN 1 ELSE 0 END) "
                "FROM expressions WHERE region=?",
                (region,),
            ).fetchone()
        finally:
            conn.close()
    except Exception as e:
        result["warning"] = f"backlog gate could not read DB: {e}"
        return result

    total = int(total or 0)
    bt = int(bt or 0)
    pending_gated = int(pending_gated or 0)
    gem_n = int(gem_n or 0)
    selected_n = int(selected_n or 0)
    conversion = bt / total if total else 1.0
    pg_ratio = pending_gated / total if total else 0.0
    # 2026-09-17 P0-2：未消费 = gem + selected + pending + gated（回测之后才叫"已消费"）
    unconsumed = gem_n + selected_n + pending_gated
    uc_ratio = unconsumed / total if total else 0.0
    result["evidence"] = {
        "total": total, "backtested": bt, "pending_gated": pending_gated,
        "gem": gem_n, "selected": selected_n, "unconsumed": unconsumed,
        "conversion": round(conversion, 4), "pending_gated_ratio": round(pg_ratio, 4),
        "unconsumed_ratio": round(uc_ratio, 4),
        "unconsumed_enforced": bool(cfg.get("unconsumed_enforce")),
    }

    # 样本不足的新区不判
    if total < int(cfg["min_expressions"]):
        result["skipped"] = f"expression sample {total} < min {cfg['min_expressions']}"
        return result

    hits = []
    if conversion < float(cfg["conversion_min"]):
        hits.append(
            f"conversion={conversion:.1%}（{bt}/{total}）< {float(cfg['conversion_min']):.0%}："
            f"生成远超回测吞吐（S2→S3 断链），先消化近闸积压再开新波"
        )
    if pg_ratio > float(cfg["pending_gated_ratio_max"]):
        hits.append(
            f"pending+gated={pending_gated}/{total}（{pg_ratio:.0%}）> "
            f"{float(cfg['pending_gated_ratio_max']):.0%}：积压超限，本波应优先 "
            f"build_wave --from-db 重取近闸积压，而非新建表达式堆库"
        )
    uc_hit = uc_ratio > float(cfg["unconsumed_ratio_max"])
    if uc_hit:
        _msg = (
            f"未消费积压={unconsumed}/{total}（{uc_ratio:.0%}，其中 gem={gem_n} selected={selected_n} "
            f"pending+gated={pending_gated}）> {float(cfg['unconsumed_ratio_max']):.0%}："
            f"连最早期积压（gem/selected）也未被回测消化"
        )
        if cfg.get("unconsumed_enforce"):
            hits.append(_msg)
        else:
            # 灰度阶段：只记录不拦截（可经 thresholds 置 unconsumed_enforce=true 转为硬闸）
            result.setdefault("warnings", []).append(f"[灰度·未拦截] {_msg}")
    if not hits:
        return result
    result["hits"] = hits
    if result.get("override"):
        result["note"] = (f"积压闸命中但已被 ledger backlog_gate_override 放行："
                          f"{result['override']['reason']}")
        return result
    result["success"] = False
    result["error"] = (
        f"积压闸拦截（{region}）：{'；'.join(hits)}。消化积压后再开新波；"
        f"确需继续（用户显式指令）请写台账 "
        f"mcp__wqb-db__upsert_ledger_key(region={region!r}, key='backlog_gate_override', "
        f"value={{'reason': '<用户指令与理由>', 'until': 'YYYY-MM-DD'}})，或在 "
        f"{thresholds_path} 的 diversity.backlog_gate 调阈值。"
    )
    return result


#: 自由文本 verdict 形态：`0/8 过硬闸, 新高 0.43`（早期波次的写入格式）
_VERDICT_ZERO_RE = re.compile(r"^\s*0\s*/\s*\d+\s*过硬闸")
_VERDICT_N_OF_M_RE = re.compile(r"^\s*(\d+)\s*/\s*\d+\s*过硬闸")


def _normalize_verdict(raw: Any) -> str:
    """把 `wave_results.verdict` 归一到 PASS|FAIL|PARTIAL|UNKNOWN（2026-09-17 P0-3）.

    背景（实测 2026-09-17）：verdict 列**不是干净枚举**。除 FAIL/PARTIAL/PASS 外还存有
    `0/6 过硬闸, 新高 0.31` / `0/8 过硬闸, 新高 0.43` 这类自由文本，以及 None / ''。
    旧规则 B 用 `all(v == "FAIL")` 判定，上述形态一律静默"不算 FAIL" → **停止闸失效**；
    JPN wave1 的 `verdict=None` 同理（`str(None or "")=""`）。

    语义澄清（避免与 IS 达标混淆）：`N/M 过硬闸` 中的 N 是**通过提交层硬闸**的条数，
    与 IS 的 sharpe/fitness 达标数**不是一回事** —— 实测 IND wave143 `verdict=FAIL`
    仍有 6 条 sharpe>1.58&fitness>1.0 的回测。故本函数只做**字符串语义归一**，
    不去 join 回测结果反推达标数（且 `backtest_results.wave` 在 DEU 写的是数据集名，
    join 不可靠）。
    """
    s = str(raw or "").strip()
    if not s:
        return "UNKNOWN"
    up = s.upper()
    if up in ("PASS", "FAIL", "PARTIAL"):
        return up
    if _VERDICT_ZERO_RE.match(s):
        return "FAIL"          # 0 条过硬闸 = 全数被硬闸拦下
    m = _VERDICT_N_OF_M_RE.match(s)
    if m:
        return "PARTIAL" if int(m.group(1)) > 0 else "FAIL"
    return "UNKNOWN"


def _run_stop_rules_gate(
    region: str,
    dataset: Optional[str],
    campaign_dir: str,
) -> Dict[str, Any]:
    """区域停止规则（2026-09-15 ⑦ SQL 化；S2/S3 前置，零配额）。

    ra-pipeline「循环与停止」表里两条规则此前只是 prose，从未被任何代码判定：
      A. yield=0 且样本 ≥100 的区不要再投槽位（GBR 0/327 本应触发）
      B. 连续 3 波全 FAIL → 暂停该区
    现按库判定。用户显式覆盖：ledger `stop_rules_override`
    {"reason": "...", "until": "YYYY-MM-DD"(可选)} —— 命中即放行并记录覆盖原因
    （SOP：用户指令优先，但要在台账留痕）。

    2026-09-17 加固（P0-3）：规则 B 的输入先经 `_normalize_verdict` 归一 ——
    自由文本 `0/N 过硬闸` 归 FAIL，空值归 UNKNOWN。UNKNOWN 既不当作"通过"
    （会 WARN 提示补写），也不据此拦截（避免因台账缺写误停区域）。
    可选更严口径 `strict_no_pass=True`：最近 K 波"无任何 PASS"即停。
    """
    result: Dict[str, Any] = {"step": "stop_rules_gate", "success": True}
    # 测试/沙箱隔离口：WQB_DISABLE_STOP_RULES_GATE=1 时跳过（与 backlog 闸的
    # WQB_DISABLE_BACKLOG_GATE 并行）。本闸读真库 wave_results/backtest_results，
    # 命令拼装类单测不封库时会被 USA 等区的真实数据拦截（与被测行为无关的污染）。
    if os.environ.get("WQB_DISABLE_STOP_RULES_GATE") == "1":
        result["skipped"] = "WQB_DISABLE_STOP_RULES_GATE=1"
        return result
    cfg = dict(STOP_RULES_DEFAULTS)
    thresholds_path = os.path.join(campaign_dir, "config", "thresholds.json")
    try:
        with open(thresholds_path, "r", encoding="utf-8") as f:
            thresholds = json.load(f)
        cfg.update((thresholds.get("diversity") or {}).get("stop_rules") or {})
    except (OSError, json.JSONDecodeError):
        pass
    if cfg.get("enabled") is False:
        result["skipped"] = "stop_rules disabled in thresholds.json"
        return result

    db_path = resolve_db_path()
    try:
        conn = sqlite3.connect(db_path)
        try:
            # 覆盖键
            row = conn.execute(
                "SELECT value FROM ledger_kv WHERE region=? AND key='stop_rules_override'", (region,)
            ).fetchone()
            override = None
            if row and row[0]:
                try:
                    override = json.loads(row[0]) if isinstance(row[0], (str, bytes)) else row[0]
                except Exception:
                    override = None
            if isinstance(override, dict) and override.get("reason"):
                until = str(override.get("until") or "")
                if not until or until >= datetime.now().strftime("%Y-%m-%d"):
                    result["override"] = {"reason": override.get("reason"), "until": until or None}
            # A. 区级产出率
            bt, passed = conn.execute(
                "SELECT COUNT(*), SUM(CASE WHEN sharpe > ? AND fitness > ? THEN 1 ELSE 0 END) "
                "FROM backtest_results WHERE region=? AND sharpe IS NOT NULL",
                (float(cfg["sharpe_min"]), float(cfg["fitness_min"]), region),
            ).fetchone()
            passed = int(passed or 0)
            # B. 最近 K 个 closed 波的 verdict（原样取出，归一化统一在下方做）
            k = int(cfg["consecutive_fail_waves"])
            raw_verdicts = [v for (v,) in conn.execute(
                "SELECT verdict FROM wave_results WHERE region=? AND status='closed' "
                "ORDER BY datetime(COALESCE(updated_at, created_at)) DESC LIMIT ?", (region, k))]
        finally:
            conn.close()
    except Exception as e:
        result["warning"] = f"stop_rules gate could not read DB: {e}"
        return result

    # 2026-09-17 加固：先归一化 verdict 再判定（自由文本/空值不再静默漏判）
    verdicts = [_normalize_verdict(v) for v in raw_verdicts]
    result["evidence"] = {
        "backtested": int(bt or 0),
        "passed": passed,
        "recent_closed_verdicts": verdicts,
        "recent_closed_verdicts_raw": [None if v is None else str(v) for v in raw_verdicts],
    }
    hits = []
    if int(bt or 0) >= int(cfg["yield_min_backtests"]) and passed == 0:
        hits.append(f"A: {region} 已回测 {bt} 条、达标 0（≥{cfg['yield_min_backtests']} 样本零产出）")
    # B：归一化后判定。
    #   默认口径 = 全 FAIL（与原语义一致，只是现在能识别 `0/N 过硬闸` 等自由文本形态）。
    #   UNKNOWN（空/不可识别）出现时**不**据此拦截，只 WARN —— 既不把"没写"当"通过"，
    #   也不因台账缺写误停区域。
    unknowns = [v for v in verdicts if v == "UNKNOWN"]
    if len(verdicts) >= k and not unknowns:
        if cfg.get("strict_no_pass"):
            if not any(v == "PASS" for v in verdicts):
                hits.append(f"B: 最近 {k} 个 closed 波无任何 PASS（{'/'.join(verdicts)}）")
        elif all(v == "FAIL" for v in verdicts):
            hits.append(f"B: 最近 {k} 个 closed 波 verdict 全 FAIL")
    if unknowns and cfg.get("unknown_warn", True):
        result["warning"] = (
            f"{len(unknowns)}/{len(verdicts)} 个最近 closed 波 verdict 为空或不可识别"
            f"（{len(unknowns)} 个）——规则 B 本次不据此拦截；"
            f"请回写 verdict（探针/全灭波也应写 FAIL，勿留空壳 closed 记录）。"
        )
    if not hits:
        return result
    result["hits"] = hits
    if result.get("override"):
        result["note"] = (f"停止规则命中但已被 ledger stop_rules_override 放行："
                          f"{result['override']['reason']}")
        return result
    result["success"] = False
    result["error"] = (
        f"停止规则拦截（{region}）：{'；'.join(hits)}。继续开波只会重复烧槽位——"
        f"换区域/换 universe/换数据集；确需继续（用户显式指令）请写台账 "
        f"mcp__wqb-db__upsert_ledger_key(region={region!r}, key='stop_rules_override', "
        f"value={{'reason': '<用户指令与理由>', 'until': 'YYYY-MM-DD'}})，或在 "
        f"{thresholds_path} 的 diversity.stop_rules 调阈值。"
    )
    return result


#: 信号天花板闸默认参数（区域 thresholds.json `diversity.signal_floor` 可覆盖）
#: 2026-09-17 #8：整节缺失时**不再静默放行**，改为回落本默认值继续判定（fail-closed）。
SIGNAL_FLOOR_DEFAULTS = {
    "enabled": True,
    "max_sharpe_floor": 0.5,
    "min_batches": 2,
}


def _run_signal_floor_gate(
    region: str,
    dataset: Optional[str],
    campaign_dir: str,
) -> Dict[str, Any]:
    """区域信号天花板闸（S2/S3 前置，2026-09-06 接线）.

    背景：`tracking/<REGION>/config/thresholds.json` 的 `diversity.signal_floor`
    早就写好了参数与语义——"连续 min_batches 批 max|sharpe| < floor 即判信号
    天花板，停止生成/增强并转区域决策"——实现也在
    `wqb.expression._enhancer.signal_evidence_gate()`，但**没有任何调用方**：
    不在 toolkit 脚本里、不在节点里、也没有 skill 引用，配置项从头到尾没人读。

    代价是实测出来的：GBR 按自己的配置该在第 2 批停，实际跑了 180 条回测、
    max|sharpe|=1.04、avg=0.41、达标 0 条。本函数把这道闸接进真正的执行路径。

    判定只用已落库的回测结果（零平台调用、零配额）。

    2026-09-17 #8 加固（fail-open → fail-closed）：旧行为是"缺 `signal_floor` 整节
    即静默放行"，与停止闸使命矛盾（GBR 曾因此跑满 180 条回测、max|sharpe|=1.04、
    达标 0 条）。现改为：读不到 thresholds.json 或整节缺失时，**回落
    `SIGNAL_FLOOR_DEFAULTS` 继续判定**并输出 `warning` 提示补配置；
    只有显式 `enabled: false` 才放行。
    """
    result: Dict[str, Any] = {"step": "signal_floor_gate", "success": True}
    # 测试/沙箱隔离口：WQB_DISABLE_SIGNAL_FLOOR_GATE=1 时跳过（与 backlog/stop_rules
    # 闸的 WQB_DISABLE_* 并行）。本闸读真库最近批次的回测 sharpe——USA 真实数据
    # 近 2 批 max=0.88 会触发天花板判定，让命令拼装类单测因环境而非行为失败。
    # （旧注释自述"只能靠'无回测证据即跳过'侥幸不爆"，此开关补齐三闸隔离的最后一环。）
    if os.environ.get("WQB_DISABLE_SIGNAL_FLOOR_GATE") == "1":
        result["skipped"] = "WQB_DISABLE_SIGNAL_FLOOR_GATE=1"
        return result

    thresholds_path = os.path.join(campaign_dir, "config", "thresholds.json")
    thresholds: Dict[str, Any] = {}
    try:
        with open(thresholds_path, "r", encoding="utf-8") as f:
            thresholds = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        result["warning"] = (
            f"thresholds.json 不可读（{type(e).__name__}）——已回落默认 signal_floor "
            f"{SIGNAL_FLOOR_DEFAULTS}（fail-closed），请补 {thresholds_path}"
        )

    cfg = dict(SIGNAL_FLOOR_DEFAULTS)
    configured = (thresholds.get("diversity") or {}).get("signal_floor")
    if isinstance(configured, dict):
        cfg.update(configured)
    elif configured is None:
        result["warning"] = (
            (result.get("warning") + "；" if result.get("warning") else "")
            + f"thresholds.json 缺 diversity.signal_floor 整节——已按默认 "
              f"floor={SIGNAL_FLOOR_DEFAULTS['max_sharpe_floor']} / "
              f"min_batches={SIGNAL_FLOOR_DEFAULTS['min_batches']} 判定（fail-closed）；"
              f"如需关闭请显式设 enabled:false"
        )
    if cfg.get("enabled") is False:
        result["skipped"] = "signal_floor disabled in thresholds.json"
        return result

    floor = float(cfg.get("max_sharpe_floor", 0.5))
    min_batches = int(cfg.get("min_batches", 2))

    # 取该 region（有 dataset 则再限定 dataset）最近若干波的回测结果。
    # 每个 wave 记为一"批"，与 signal_evidence_gate 的 batch_idx 语义对齐。
    # 口径：thresholds.json 说的是"**连续** min_batches 批"，不是全历史。
    # 取全历史会让闸永不触发 —— GBR 跑了 20 批、全局 max|sharpe|=1.04 > floor 0.5，
    # 哪怕最近 10 批全是 0.3 也照样判 ok。所以只看最近 min_batches 个波次。
    # 2026-09-17 一致性修复：改用 resolve_db_path()，与另两道闸及 WQB_DB_PATH 契约对齐。
    # 此前硬编码 REPO_ROOT/data/wqb.db，导致设了 WQB_DB_PATH 的单测/沙箱仍读真库
    #（本闸因此在 tests 里无法隔离，只能靠"无回测证据即跳过"侥幸不爆）。
    db_path = resolve_db_path()
    rows: List[Dict[str, Any]] = []
    recent_waves: List[str] = []
    try:
        conn = sqlite3.connect(db_path)
        try:
            where = "region=? AND sharpe IS NOT NULL"
            params: List[Any] = [region]
            if dataset:
                where += " AND dataset=?"
                params.append(dataset)

            # 最近 min_batches 个波次（按该波最后一条回测的时间排序）
            recent_waves = [
                str(w) for (w,) in conn.execute(
                    f"SELECT wave FROM backtest_results WHERE {where} AND wave IS NOT NULL "
                    f"GROUP BY wave ORDER BY MAX(id) DESC LIMIT ?",
                    params + [min_batches],
                )
            ]
            if recent_waves:
                placeholders = ",".join("?" * len(recent_waves))
                query_params = params + recent_waves
                for sharpe, wave_id in conn.execute(
                    f"SELECT sharpe, wave FROM backtest_results "
                    f"WHERE {where} AND wave IN ({placeholders})",
                    query_params,
                ):
                    rows.append({"sharpe": sharpe, "batch_idx": wave_id})
        finally:
            conn.close()
    except Exception as e:  # DB 不可读不阻断，只记录
        result["warning"] = f"signal_floor gate could not read DB: {e}"
        return result

    if not rows:
        result["skipped"] = "no backtest evidence yet"
        return result

    result["window"] = {"recent_waves": recent_waves, "results": len(rows)}

    # 证据不足以构成"连续 N 批"时不判死（新区域/新数据集应当有试探空间）
    if len(recent_waves) < min_batches:
        result["skipped"] = (
            f"evidence only spans {len(recent_waves)} batch(es), "
            f"need {min_batches} to judge a ceiling"
        )
        return result

    try:
        # 走 diversity_enhancer 门面而非 _enhancer 私有模块：后者被 _metrics
        # 在模块底部反向 import，直接进 _enhancer 会撞循环导入。
        from wqb.expression.diversity_enhancer import signal_evidence_gate
    except ImportError as e:
        result["warning"] = f"signal_evidence_gate unavailable: {e}"
        return result

    verdict = signal_evidence_gate(rows, max_sharpe_floor=floor, min_batches=min_batches)
    result["verdict"] = verdict
    result["scope"] = f"{region}/{dataset}" if dataset else region
    if not verdict.get("passed", True):
        result["success"] = False
        result["error"] = (
            f"信号天花板闸拦截（{result['scope']}）：{verdict.get('message')}。"
            f"继续生成/回测只会重复烧槽位——请换 universe / 换数据集 / 换区域，"
            f"或在 {thresholds_path} 里把 diversity.signal_floor.enabled 设为 false "
            f"并在台账记录理由。"
        )
    return result


def _ensure_campaign_config(campaign_dir: str, region: str, result: Dict[str, Any]) -> None:
    """自动创建 config/settings.json（缺省时从 DB ledger 推导，P0 修复）.

    KOR 等早期战役目录缺 config/ 子目录，导致 S0/S2/S3 脚本无法读取 settings。
    本函数在 validate_campaign_dir 通过后自动补建，从 DB ledger 推导 region/delay/universe。
    """
    config_dir = os.path.join(campaign_dir, "config")
    settings_path = os.path.join(config_dir, "settings.json")

    if os.path.exists(settings_path):
        return  # 已存在，不覆盖

    try:
        os.makedirs(config_dir, exist_ok=True)

        # 从 DB ledger 推导配置
        import sqlite3
        db_path = os.path.join(REPO_ROOT, "data", "wqb.db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # 读 s0_whitelist 获取 delay/universe（2026-09-17 P0-4 修复）
        # 旧实现只认 `filter_criteria.{delay,universe}` —— 实测全 13 个区域的白名单
        # 均无 `filter_criteria` 键（`value LIKE '%filter_criteria%'` 返回空），
        # 属**死代码**：白名单锁定的 universe 从未被本节点消费，恒回落
        # delay=1 / universe="TOP3000" 再被 regions 表 legal[0] 覆盖。
        # 现改用 wqb.ledger_whitelist 的容错归一（覆盖 candidates/whitelist/datasets/
        # 推断/损坏抢救 共 5 种历史形态），解析失败**显式告警**而非静默回落。
        delay, universe = 1, "TOP3000"
        c.execute("SELECT value FROM ledger_kv WHERE region=? AND key='s0_whitelist'", (region,))
        row = c.fetchone()
        if row:
            try:
                from ...ledger_whitelist import normalize as _norm_wl
                _wl = _norm_wl(row[0])
                if _wl.get("delay") is not None:
                    delay = _wl["delay"]
                if _wl.get("universe"):
                    universe = _wl["universe"]
                if _wl.get("schema") in ("inferred", "recovered"):
                    logger.warning(
                        f"_ensure_campaign_config({region}): s0_whitelist 形态="
                        f"{_wl['schema']}（{_wl.get('reason')}）")
                elif not _wl.get("ok"):
                    logger.warning(
                        f"_ensure_campaign_config({region}): s0_whitelist 无法解析"
                        f"（{_wl.get('reason')}）——回落 delay={delay}/universe={universe}")
            except Exception as e:
                logger.warning(
                    f"_ensure_campaign_config({region}): s0_whitelist 归一失败 "
                    f"{type(e).__name__}: {e}")

        # 从 regions 表获取 universe_legal/delay_legal
        c.execute("SELECT universe_legal, delay_legal FROM regions WHERE name=?", (region,))
        row2 = c.fetchone()
        if row2:
            try:
                import json as _json
                ul = _json.loads(row2[0]) if row2[0] else []
                dl = _json.loads(row2[1]) if row2[1] else []
                if ul and universe not in ul:
                    universe = ul[0]
                if dl and delay not in dl:
                    delay = dl[0]
            except Exception:
                pass

        conn.close()

        # 区域默认中性化（从 profile 或实证推导）
        neut_map = {
            "KOR": "STATISTICAL", "IND": "STATISTICAL", "MEA": "SUBINDUSTRY",
            "USA": "SUBINDUSTRY", "EUR": "SUBINDUSTRY", "GBR": "SUBINDUSTRY",
            "ASI": "SUBINDUSTRY", "HKG": "SUBINDUSTRY", "GLB": "SUBINDUSTRY",
            "CHN": "SUBINDUSTRY", "TWN": "SUBINDUSTRY",
        }
        neutralization = neut_map.get(region, "SUBINDUSTRY")

        settings = {
            "_doc": f"{region} 战役仿真设置（自动创建，从 DB ledger 推导）。",
            "instrumentType": "EQUITY",
            "region": region,
            "universe": universe,
            "delay": delay,
            "neutralization": neutralization,
            "decay": 4,
            "truncation": 0.08,
            "pasteurization": "ON",
            "unitHandling": "VERIFY",
            "nanHandling": "OFF",
            "maxTrade": "OFF",
            "language": "FASTEXPR",
            "visualization": False,
            "startDate": "2013-01-01",
            "endDate": "2023-12-31",
        }

        import json as _json
        with open(settings_path, "w", encoding="utf-8") as f:
            _json.dump(settings, f, indent=2, ensure_ascii=False)

        result["steps"].append({
            "step": "auto_create_config",
            "success": True,
            "settings_path": settings_path,
            "region": region,
            "universe": universe,
            "delay": delay,
            "neutralization": neutralization,
        })
        logger.info(f"Auto-created config/settings.json for {region}: universe={universe}, delay={delay}")

    except Exception as e:
        result["steps"].append({
            "step": "auto_create_config",
            "success": False,
            "error": str(e),
        })
        logger.warning(f"Failed to auto-create config for {region}: {e}")


def _extract_structured_summary(stdout: str, stage: str) -> Optional[Dict[str, Any]]:
    """从 stdout 提取结构化摘要（Dry-Run 2.0 优化：减少 token 消耗）.

    根据 stage 提取关键指标，替代纯文本截断。
    """
    if not stdout:
        return None

    summary: Dict[str, Any] = {}
    lines = stdout.split("\n")

    if stage == "S0":
        # 提取白名单/排除集计数
        whitelist_count = sum(1 for l in lines if "whitelist" in l.lower() or "白名单" in l)
        excluded_count = sum(1 for l in lines if "excluded" in l.lower() or "排除" in l)
        if whitelist_count or excluded_count:
            summary["whitelist_mentions"] = whitelist_count
            summary["excluded_mentions"] = excluded_count

    elif stage == "S2":
        # 提取表达式计数
        import re
        expr_match = re.search(r"(\d+)\s*(?:expressions?|表达式)", stdout, re.IGNORECASE)
        if expr_match:
            summary["expression_count"] = int(expr_match.group(1))

    elif stage == "S3":
        # 提取 COMPLETE/ERROR/CANCELLED 计数
        complete_count = stdout.count("COMPLETE")
        error_count = stdout.count("ERROR")
        cancelled_count = stdout.count("CANCELLED")
        if complete_count or error_count or cancelled_count:
            summary["complete"] = complete_count
            summary["error"] = error_count
            summary["cancelled"] = cancelled_count

    elif stage == "S4":
        # 提取 walls 诊断关键词
        walls_keywords = ["structural", "robust", "coverage", "turnover", "concentration"]
        found_walls = [kw for kw in walls_keywords if kw in stdout.lower()]
        if found_walls:
            summary["walls_detected"] = found_walls

    return summary if summary else None


def _extract_walls_summary(stdout: str) -> Optional[Dict[str, Any]]:
    """从 review_wave.py 输出提取 walls 诊断摘要（Dry-Run 2.0 优化）.

    识别 structural/robust/coverage/turnover/concentration 等墙类型。
    """
    if not stdout:
        return None

    walls: Dict[str, Any] = {}
    lower = stdout.lower()

    # 检测各类墙
    wall_types = {
        "structural": ["structural", "结构"],
        "robust": ["robust", "稳健"],
        "coverage": ["coverage", "覆盖"],
        "turnover": ["turnover", "换手"],
        "concentration": ["concentration", "集中"],
    }

    for wall_name, keywords in wall_types.items():
        for kw in keywords:
            if kw in lower:
                walls[wall_name] = True
                break

    # 提取 sharpe/fitness 数值（如有）
    import re
    sharpe_match = re.search(r"sharpe[=:]\s*([\d.]+)", lower)
    if sharpe_match:
        walls["sharpe"] = float(sharpe_match.group(1))
    fitness_match = re.search(r"fitness[=:]\s*([\d.]+)", lower)
    if fitness_match:
        walls["fitness"] = float(fitness_match.group(1))

    return walls if walls else None
