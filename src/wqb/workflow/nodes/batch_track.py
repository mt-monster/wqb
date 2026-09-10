# -*- coding: utf-8 -*-
"""batch_track 节点：S3 批量回测与跟踪.

替代 brain-sim-alphas-in-batch-and-track 的 PowerShell 命令模板。
"""

import json
import logging
import os
import subprocess
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..mcp_check import require_mcp_tools
from .._common import (
    REPO_ROOT,
    backtest_row_count,
    batch_track_no_submit_error,
    detached_launch_failed,
    resolve_campaign_dir,
    resolve_toolkit_dir,
    unbuffered_env,
    validate_argv,
    wq_py,
)

logger = logging.getLogger(__name__)


@require_mcp_tools("batch_track")
def run(
    region: str,
    wave: str,
    dataset: str,
    concurrency: int = 7,
    max_rounds: int = 3,
    dry_run: bool = False,
    output_csv: Optional[str] = None,
    campaign_dir: Optional[str] = None,
    detached: bool = True,
    submit: bool = True,
    skip_diversity_gate: bool = False,
    datasets_extra: Optional[str] = None,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """执行批量回测跟踪.

    Args:
        region: 区域代码（如 KOR）
        wave: 波次号（如 36A）
        dataset: 数据集 ID
        concurrency: 并发数（默认 7，七槽填槽）
        max_rounds: 最大轮次
        dry_run: 是否干跑
        output_csv: 输出 CSV 路径（默认自动生成）
        campaign_dir: 战役目录（可选，默认自动解析）
        detached: 是否后台执行（默认 True，避免 MCP 客户端超时；False 为旧同步模式）
        submit: 是否真正提交回测（默认 True）。False 只跑 gate + 计划，不发 simulation。
                注意：这里的"提交"是提交 **回测**（simulation），不是提交 alpha ——
                提交 alpha 走 submit_alpha 节点且需用户确认（ra-pipeline 步 8）。
        _context: 执行上下文（由 executor 注入）

    Returns:
        执行结果字典
    """
    ctx = _context or {}
    store = ctx.get("store")
    # dry-run 统一以 _context 为准（executor 注入），形参仅作直连调用的兼容入口
    dry_run = bool(ctx.get("dry_run", dry_run))
    warnings: List[str] = []

    # 生成输出路径
    if not output_csv:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_csv = f"outputs/simulation_status_{region}_{wave}_{timestamp}.csv"

    # 解析 campaign-dir（优先级：参数 > 环境变量 > 自动探测）
    if not campaign_dir:
        campaign_dir = resolve_campaign_dir(region)
    
    if not campaign_dir:
        return {
            "success": False,
            "error": f"Cannot resolve campaign_dir for region={region}. "
                     "Set WQB_CAMPAIGN_DIR env var or pass campaign_dir parameter.",
            "region": region,
            "wave": wave,
            "dataset": dataset,
        }

    # 验证战役目录
    if not os.path.exists(campaign_dir):
        return {
            "success": False,
            "error": f"Campaign directory not found: {campaign_dir}",
            "region": region,
            "wave": wave,
            "dataset": dataset,
            "campaign_dir": campaign_dir,
        }

    # 读取表达式（从 DB）
    expressions = []
    if store:
        try:
            expressions = store.list_expressions(region, wave, dataset)
        except Exception as e:
            logger.warning(f"Failed to list expressions from DB: {e}")

    if not expressions:
        msg = f"No expressions found for {region}/{wave}/{dataset}"
        if not dry_run:
            return {
                "success": False,
                "error": msg,
                "region": region,
                "wave": wave,
                "dataset": dataset,
            }
        # dry-run：库里没表达式属"状态"问题，不是流程走不通 —— 记 warning 继续验证链路
        # （2026-09-05 统一 dry-run 语义：干跑回答"这条链能不能跑通"，不回答"现在有没有货"）
        warnings.append(msg)

    # 定位 toolkit（dry-run 也要走，否则干跑发现不了 toolkit 缺失这类真断链）
    toolkit_dir = resolve_toolkit_dir()

    if not toolkit_dir or not os.path.exists(toolkit_dir):
        return {
            "success": False,
            "error": "WQ_TOOLKIT_DIR not found. Set env var or install wq-brain-campaign-toolkit skill.",
            "region": region,
            "wave": wave,
            "dataset": dataset,
        }

    pipeline_script = os.path.join(toolkit_dir, "pipeline.py")
    if not os.path.exists(pipeline_script):
        return {
            "success": False,
            "error": f"pipeline.py not found at {pipeline_script}",
            "region": region,
            "wave": wave,
            "dataset": dataset,
        }

    # 构建命令
    # 2026-09-06 修复：删除 `--concurrency` —— pipeline.py run 从未声明该参数，
    # argparse 直接 exit=2（"unrecognized arguments: --concurrency 7"），而
    # detached 分支不看退出码，于是 S3 每次都"启动成功"却从未真正跑过。
    # 槽位数由 pipeline.py 内部锁定为 n_slots=min(7, n_total)，与 wqb-concurrency
    # §8 七槽填槽一致，无需也无法从外部传入；concurrency 形参保留为计划元数据。
    #
    # 2026-09-08 修复（本节点第二次"启动成功但什么都没干"）：
    #   ① 补 `--submit`。缺它时 pipeline.py 走 `if not a.submit` 分支，打一行
    #      `[plan] gate 过 N 式；加 --submit 提交` 就 rc=0 退出 —— gate 跑了、
    #      回测一条没发。实测 CHN/chn_w1_other_ppa：backtest_results 0 行、
    #      ckpt batches 空、进程 rc=0。注意此处的"提交"是提交**回测**
    #      (simulation)，不是提交 alpha；提交 alpha 走 submit_alpha 且需用户
    #      确认（ra-pipeline 步 8），所以这不违反提交纪律。
    #   ② 解释器加 `-u`。detached 的 stdout 重定向到文件，Python 默认块缓冲，
    #      进程退出时未满的缓冲直接丢 —— 观察到的就是两个 0 字节日志，外部
    #      完全看不出发生过什么。
    cmd = [
        wq_py(),
        "-u",
        pipeline_script,
        "--campaign-dir", campaign_dir,
        "run",
        "--dataset", dataset,
        "--wave", wave,
        "--max-rounds", str(max_rounds),
        "--review",
        "--write-ledger",
    ]
    if submit:
        cmd.append("--submit")
    # 2026-09-09：探针批/单信号验证波可跳过批级结构多样性闸（闸6）。
    # 探针目的是早期判死单信号机制（2-3 条同族表达式），强制 12 算子覆盖
    # 会逼探针波塞进无关骨架，背离探针本意。仅 skip_diversity_gate=True 时透传。
    if skip_diversity_gate:
        cmd.append("--skip-diversity-gate")
    # 2026-09-09：跨金字塔慢×快表达式（如 insiders5×pv106 辅助腿）需要合并多个
    # dataset 的 typed catalog 才能过闸2 字段白名单（gate.py merge_whitelists）。
    # 逗号分隔，与 pipeline.py --datasets 契约一致。
    if datasets_extra:
        cmd += ["--datasets", datasets_extra]

    # argv 契约校验：构建出来的命令必须能被 pipeline.py 的 argparse 接受。
    # 干跑与实跑都走，干跑时它就是本节点最有价值的那次检查。
    argv_ok, argv_error = validate_argv(cmd)
    if not argv_ok:
        return {
            "success": False,
            "error": argv_error,
            "command": " ".join(cmd),
            "region": region,
            "wave": wave,
            "dataset": dataset,
        }

    if concurrency != 7:
        warnings.append(
            f"concurrency={concurrency} 仅记录于计划；pipeline.py 内部锁定 "
            "n_slots=min(7, 批数)，不接受外部覆盖（wqb-concurrency §8）"
        )

    # 干跑：命令已构建并通过 argv 校验，到此为止（不 Popen、不写库、不产生任务目录）
    if dry_run:
        return {
            "success": True,
            "dry_run": True,
            "note": "dry-run：命令已构建，未执行",
            "command": " ".join(cmd),
            "plan": {
                "region": region,
                "wave": wave,
                "dataset": dataset,
                "expression_count": len(expressions),
                "concurrency": concurrency,
                "max_rounds": max_rounds,
                "output_csv": output_csv,
                "campaign_dir": campaign_dir,
                "toolkit_dir": toolkit_dir,
                "detached": detached,
                "submit": submit,
            },
            "warnings": warnings,
            # 表达式为 0 时把结论写进 message 而不是只塞进 warnings：
            # 链式干跑读的是 success/error，warnings 会被整条链忽略掉。
            "message": (
                f"Would execute batch track for {len(expressions)} expressions"
                if expressions else
                f"链路可跑通，但 {region}/{wave}/{dataset} 库里 0 条表达式 —— "
                f"实跑会立即失败，先跑 S2 生成/选波"
            ),
        }

    logger.info(f"Executing: {' '.join(cmd)}")

    # 实跑前记下该波的回测行数基线：detached 写进 meta.json 供终态断言比对，
    # 同步模式跑完当场比对。读不到库时为 None（断言侧按"无法判定"放行）。
    rows_before = backtest_row_count(region, wave)

    # 2026-09-04 修复：detached 后台模式（默认），避免 MCP 客户端同步等待超时。
    # 原实现 subprocess.run(timeout=3600) 同步阻塞 1 小时，MCP 客户端默认超时远小于此
    # → 调用方断连。改为 Popen 后台启动 + 写 meta.json + 立即返回 task_id/log_path，
    # Agent 后续用 batch_status / 读日志轮询进度。detached=False 保留旧同步路径（CLI 调试用）。
    if detached:
        # 2026-09-04 修复：任务根目录改用仓库根 REPO_ROOT（原实现从 nodes/ 上溯 3 级
        # 只到 src/，任务实际落到 src/logs/_async_tasks/ 与 campaign/fe 布局分离，
        # 是"任务文件不存在"的直接来源之一）。支持 WQB_TASK_ROOT 注入（单测隔离）。
        tasks_root = os.environ.get("WQB_TASK_ROOT") or os.path.join(
            REPO_ROOT, "logs", "_async_tasks",
        )
        tasks_root = os.path.abspath(tasks_root)
        os.makedirs(tasks_root, exist_ok=True)
        task_id = f"batch_track_{region}_{wave}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        task_dir = os.path.join(tasks_root, task_id)
        os.makedirs(task_dir, exist_ok=True)
        stdout_log = os.path.join(task_dir, "stdout.log")
        stderr_log = os.path.join(task_dir, "stderr.log")
        meta_path = os.path.join(task_dir, "meta.json")

        try:
            out_f = open(stdout_log, "w", encoding="utf-8")
            err_f = open(stderr_log, "w", encoding="utf-8")
            popen_kwargs: Dict[str, Any] = {
                "stdout": out_f,
                "stderr": err_f,
                "cwd": toolkit_dir,
                # `-u` 管住直接启动的解释器，PYTHONUNBUFFERED 连它 spawn 的
                # 子进程一起管住 —— 日志实时落盘是 detached 唯一的可观测手段
                "env": unbuffered_env(),
            }
            if os.name == "nt":
                # Windows：脱离父进程组，避免 MCP 进程退出时子进程被终止
                popen_kwargs["creationflags"] = (
                    subprocess.CREATE_NEW_PROCESS_GROUP
                    | subprocess.DETACHED_PROCESS
                )
            else:
                popen_kwargs["start_new_session"] = True
            proc = subprocess.Popen(cmd, **popen_kwargs)

            meta = {
                "task_id": task_id,
                "pid": proc.pid,
                "cmd": cmd,
                "region": region,
                "wave": wave,
                "dataset": dataset,
                "concurrency": concurrency,
                "max_rounds": max_rounds,
                "output_csv": output_csv,
                "campaign_dir": campaign_dir,
                "stdout_log": stdout_log,
                "stderr_log": stderr_log,
                "started_at": datetime.now().isoformat(),
                # 2026-09-08：终态断言的基线。`submit` 键的存在本身就是
                # "这个任务需要跑后置断言"的标记（老任务目录没有它，行为不变），
                # 断言实现见 tasks._assert_batch_track_submitted。
                "submit": bool(submit),
                "backtest_rows_before": rows_before,
            }
            with open(meta_path, "w", encoding="utf-8") as mf:
                json.dump(meta, mf, ensure_ascii=False, indent=1)

            # 2026-09-06 新增：存活握手。detached 不看退出码是"启动即死"被吞成
            # success=True 的根因（本次审计 P0：argparse exit=2 被静默 13 天）。
            # 跑得起来的任务此刻仍在运行；跑不起来的已把原因写进 stderr。
            launch_error = detached_launch_failed(proc, stderr_log)
            if launch_error:
                out_f.close()
                err_f.close()
                meta["failed_at_launch"] = launch_error
                try:
                    with open(meta_path, "w", encoding="utf-8") as mf:
                        json.dump(meta, mf, ensure_ascii=False, indent=1)
                except OSError:
                    pass
                return {
                    "success": False,
                    "error": f"batch_track 后台任务启动失败：{launch_error}",
                    "task_id": task_id,
                    "task_dir": task_dir,
                    "stderr_log": stderr_log,
                    "command": " ".join(cmd),
                    "region": region,
                    "wave": wave,
                    "dataset": dataset,
                }

            return {
                "success": True,
                "detached": True,
                "task_id": task_id,
                "task_dir": task_dir,
                "pid": proc.pid,
                "stdout_log": stdout_log,
                "stderr_log": stderr_log,
                "region": region,
                "wave": wave,
                "dataset": dataset,
                "expression_count": len(expressions),
                "output_csv": output_csv,
                "message": (
                    f"batch_track detached task launched: {task_id} (pid={proc.pid}). "
                    f"Poll stdout_log / output_csv for progress; "
                    f"use batch_status on harvested simulation ids."
                ),
            }
        except Exception as e:
            logger.exception("batch_track detached launch failed")
            return {
                "success": False,
                "error": f"detached launch failed: {e}",
                "region": region,
                "wave": wave,
                "dataset": dataset,
            }

    # 同步模式（detached=False，旧行为）：subprocess.run 阻塞至完成或 1h 超时
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3600,  # 1 小时超时
            cwd=toolkit_dir,
            env=unbuffered_env(),
        )

        success = result.returncode == 0
        stdout_text = result.stdout or ""

        # 2026-09-08：rc=0 不等于跑过 submit。缺 --submit 时 pipeline 只打计划行
        # 就正常退出 —— 同步路径同样要过这道断言，否则又是一次"成功地什么都没干"。
        # submit=False 是"只出计划"的合法用法，此时 pipeline 必然打印计划行、
        # 也必然不落回测行 —— 断言只对 submit=True 生效。
        assert_error = None
        if success and submit:
            assert_error = batch_track_no_submit_error(
                stdout_text, rows_before, backtest_row_count(region, wave),
            )
            if assert_error:
                success = False

        output = {
            "success": success,
            "returncode": result.returncode,
            "stdout": result.stdout[-2000:] if result.stdout else "",  # 截断
            "stderr": result.stderr[-2000:] if result.stderr else "",
            "region": region,
            "wave": wave,
            "dataset": dataset,
            "expression_count": len(expressions),
            "output_csv": output_csv,
            "submit": submit,
            "backtest_rows_before": rows_before,
        }
        if assert_error:
            output["error"] = assert_error
        # 结构化摘要（Dry-Run 2.0 优化：提取 COMPLETE/ERROR/CANCELLED 计数，减少 token 消耗）
        if stdout_text:
            complete_count = stdout_text.count("COMPLETE")
            error_count = stdout_text.count("ERROR")
            cancelled_count = stdout_text.count("CANCELLED")
            if complete_count or error_count or cancelled_count:
                output["structured_summary"] = {
                    "complete": complete_count,
                    "error": error_count,
                    "cancelled": cancelled_count,
                }

        # 保存 checkpoint
        if store and success:
            try:
                store.upsert_ledger("WORKFLOW", f"batch_track_{region}_{wave}", {
                    "completed_at": datetime.now().isoformat(),
                    "expression_count": len(expressions),
                    "output_csv": output_csv,
                })
            except Exception as e:
                logger.warning(f"Failed to save checkpoint: {e}")

        return output

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Execution timeout (3600s)",
            "region": region,
            "wave": wave,
            "dataset": dataset,
        }
    except Exception as e:
        logger.exception("batch_track execution failed")
        return {
            "success": False,
            "error": str(e),
            "region": region,
            "wave": wave,
            "dataset": dataset,
        }


# _resolve_campaign_dir 已迁至 _common.resolve_campaign_dir（单一事实源）
