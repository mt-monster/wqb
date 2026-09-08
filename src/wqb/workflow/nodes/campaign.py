# -*- coding: utf-8 -*-
"""campaign 节点：S1-S6 战役阶段执行.

包装 wq-brain-campaign-toolkit 的各阶段脚本，消除 --campaign-dir 手工传递。

2026-09-03 根治：subprocess.run → Popen 异步化，避免 MCP 客户端超时。
子进程在后台运行，结果写入临时 JSON，调用方通过 task_file 轮询。
"""

import json
import logging
import os
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
    resolve_toolkit_dir,
    resolve_tools_dir,
    unbuffered_env,
    validate_argv,
    wq_py,
)

#: 走 campaign.py 子命令路由的 subcommand（不由 stage 分支自行 append，
#: 否则 S6 + assemble-priors 会被拼两次）
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
            cache_key = f"priors_snapshot_{region}"

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
    elif stage == "S2":
        # 信号天花板闸：纯 DB 判定、零配额，故 dry-run 也走 —— 干跑就该回答
        # "这个区还值不值得继续开波"。
        floor_result = _run_signal_floor_gate(region, dataset, campaign_dir)
        result["steps"].append(floor_result)
        if not floor_result.get("success", True):
            result["success"] = False
            result["error"] = floor_result.get("error")
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
        if wave:
            cmd.extend(["--tag", wave])
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
                        thread_store.upsert_ledger(region, f"priors_snapshot_{region}", {
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
) -> Dict[str, Any]:
    """波次前置条件预检（S0/S1 产物门禁，S2/S3 前强制）.

    校验字段 catalog（文件 + DB 单一事实源）、新鲜度与判死清单。
    通用修复入口：FAIL 时按 remediation 跑 tools/preflight_wave.py --repair。
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
    gate_cmd = [
        py, os.path.join(resolve_tools_dir(), "wave_gate.py"),
        "--campaign-dir", campaign_dir,
        "--from-db",
        "--quality-block",  # 硬阻断模式
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

        # wave_gate.py --quality-block 在发现 EXPECTED_BLOCK 时返回非零
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

    判定只用已落库的回测结果（零平台调用、零配额）。`enabled: false` 或
    缺 `signal_floor` 配置时放行。
    """
    result: Dict[str, Any] = {"step": "signal_floor_gate", "success": True}

    thresholds_path = os.path.join(campaign_dir, "config", "thresholds.json")
    try:
        with open(thresholds_path, "r", encoding="utf-8") as f:
            thresholds = json.load(f)
    except (OSError, json.JSONDecodeError):
        result["skipped"] = "no thresholds.json"
        return result

    cfg = (thresholds.get("diversity") or {}).get("signal_floor") or {}
    if not cfg or cfg.get("enabled") is False:
        result["skipped"] = "signal_floor not configured or disabled"
        return result

    floor = float(cfg.get("max_sharpe_floor", 0.5))
    min_batches = int(cfg.get("min_batches", 2))

    # 取该 region（有 dataset 则再限定 dataset）最近若干波的回测结果。
    # 每个 wave 记为一"批"，与 signal_evidence_gate 的 batch_idx 语义对齐。
    # 口径：thresholds.json 说的是"**连续** min_batches 批"，不是全历史。
    # 取全历史会让闸永不触发 —— GBR 跑了 20 批、全局 max|sharpe|=1.04 > floor 0.5，
    # 哪怕最近 10 批全是 0.3 也照样判 ok。所以只看最近 min_batches 个波次。
    db_path = os.path.join(REPO_ROOT, "data", "wqb.db")
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

        # 读 s0_whitelist 获取 delay/universe（如有）
        delay, universe = 1, "TOP3000"
        c.execute("SELECT value FROM ledger_kv WHERE region=? AND key='s0_whitelist'", (region,))
        row = c.fetchone()
        if row:
            try:
                import json as _json
                wl = _json.loads(row[0])
                # 从 filter_criteria 或白名单推断
                fc = wl.get("filter_criteria", {})
                if isinstance(fc, dict):
                    delay = fc.get("delay", delay)
                    universe = fc.get("universe", universe)
            except Exception:
                pass

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
