# -*- coding: utf-8 -*-
"""gem 节点：GEM 表达式生成.

替代 brain-make-some-gem 的 headless_runner PowerShell 命令模板。
"""

import json
import logging
import os
import re
import subprocess
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..mcp_check import require_mcp_tools
from .._common import (
    REPO_ROOT,
    detached_launch_failed,
    infer_data_category,
    resolve_db_path,
    resolve_skill_dir,
    unbuffered_env,
    validate_argv,
    wq_py,
)

logger = logging.getLogger(__name__)


#: S1 ledger `source` 属于确定性模板渲染（brain-data-feature-engineering/scripts/
#: feature_engineering.py，无 LLM）的取值；这类文档不作为 GEM 的 ideas 输入。
TEMPLATE_IDEAS_SOURCES = ("feature_engineering_node", "standalone", "standalone_v2")


def is_template_ideas_source(source: Optional[str]) -> bool:
    src = str(source or "").strip()
    return any(src == t or src.startswith(t + " ") or src.startswith(t + "(")
               for t in TEMPLATE_IDEAS_SOURCES)


@require_mcp_tools("gem")
def run(
    region: str,
    dataset_id: str,
    delay: int,
    universe: str,
    data_category: Optional[str] = None,
    instrument_type: str = "EQUITY",
    data_type: str = "MATRIX",
    priors_file: Optional[str] = None,
    priors_from_db: bool = True,
    ideas_file: Optional[str] = None,
    detached: bool = True,
    launch_only: bool = False,
    pipeline_mode: Optional[str] = "phased",
    batch_size: int = 100,
    require_operators: Optional[str] = None,
    require_count: int = 2,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """执行 GEM 表达式生成.

    Args:
        region: 区域代码
        dataset_id: 数据集 ID
        delay: 延迟（0 或 1）
        universe: 宇宙（如 TOP3000）
        data_category: 数据类别（如 analyst）
        instrument_type: 工具类型（默认 EQUITY）
        data_type: 数据类型（MATRIX 或 VECTOR）
        priors_file: priors.json 路径（显式指定时优先于 DB 快照）
        priors_from_db: 是否从 DB ledger priors_snapshot_<region> 读取 priors
            （默认 True，与 SOP「DB 为单一事实源」对齐；run.py fail-closed：
            无快照即报错，不会静默无 priors 运行。仅当显式传 priors_file 或
            本参数=False 时不走 DB 直读）
        ideas_file: ideas.md 路径（显式指定，覆盖 S1 ledger 自动注入）
        detached: 是否后台执行
        launch_only: 只启动不等待（2026-09-12 P1）：Popen 后立即返回，
            不等 meta.json 握手，彻底规避 MCP 客户端超时。Agent 后续用
            workflow_task_status(prefix="gem_") 轮询任务状态。
        pipeline_mode: GEM 生成模式 single / phased / skeleton（2026-09-18 ③）。
            默认 "phased"（三阶段分批：structure→mapping→render），解决全量大字段集
            （如订单流 198 字段）single-shot 模式 LLM 生成超时（9+ 分钟）的问题。
            "single" = 一次性 LLM 调用（旧默认，仅小字段集 <50 适用）；
            "skeleton" = 骨架枚举 + LLM 填槽（语法构造保证）。
        batch_size: phased 模式下每批字段数（默认 100）。
            198 字段订单流实测：batch_size=50 拆散同族字段（bid_* / ask_* 跨批），
            跨族机制（如 ask-bid 价差）无法在同一批内设计；100 让同族字段同批。
        _context: 执行上下文

    Returns:
        执行结果字典
    """
    ctx = _context or {}
    store = ctx.get("store")

    # 自动推断 data_category（如未提供）
    if not data_category:
        data_category = infer_data_category(dataset_id)

    result = {
        "region": region,
        "dataset_id": dataset_id,
        "delay": delay,
        "universe": universe,
        "data_category": data_category,
        "instrument_type": instrument_type,
        "data_type": data_type,
        "steps": [],
        "success": False,
    }

    # dry-run 统一口径（2026-09-05）：走完所有零成本前置——S1 ledger 读取、
    # skill 目录/脚本/config 解析、命令构建、ideas 格式预检——到 Popen 前即停。
    # 不 subprocess、不写库（build_candidate_field_pool 的 persist 亦跳过）。
    # 此前只返回一句写死的 "Would run GEM: ..."，等于什么都没验证。
    dry_run = bool(ctx.get("dry_run"))
    result["dry_run"] = dry_run

    # Step 1: 检查 S1 ledger（自动注入 ideas-file）
    s1_ledger = None
    field_prefix_summary = None
    candidate_field_pool = []
    # 显式 ideas_file 优先于 S1 ledger 自动注入
    effective_ideas_file = ideas_file
    if store:
        try:
            s1_key = f"s1_{dataset_id}_d{delay}"
            s1_ledger = store.get_ledger(region, s1_key)
            if s1_ledger and s1_ledger.get("ideas_md_path"):
                # 2026-09-15 审计缺陷 A：ledger 里可能残留历史 Agent 安装位/旧命名的
                # ideas_md_path（如 .qoder-cn\...\brain-makeSomeGem\...）——2026-09-10
                # skill 多目标同步改名后这些物理拷贝/旧目录已不存在或已分叉，注入后
                # GEM 在 check_ideas_format（文件不存在/格式不符）或实跑时断裂。
                # 注入前先验存在性：失效路径视为"无 ideas"，改走概念优先自含生成
                # （显式 ideas_file 不受影响——那是用户当轮给的真实路径）。
                _ledger_ideas_path = s1_ledger["ideas_md_path"]
                _ledger_ideas_exists = os.path.exists(_ledger_ideas_path)
                if not _ledger_ideas_exists and not ideas_file:
                    result["steps"].append({
                        "step": "s1_ledger_check",
                        "success": True,
                        "s1_key": s1_key,
                        "ideas_md_path": _ledger_ideas_path,
                        "auto_inject": False,
                        "skipped_reason": (
                            "ledger 记录的 ideas_md_path 文件已不存在（历史安装位残留），"
                            "视为无 ideas：GEM 走概念优先自含生成；如需重生成请跑 "
                            "workflow_feature_engineering(force_regen=true) 或显式传 ideas_file"
                        ),
                    })
                elif is_template_ideas_source(s1_ledger.get("source")) and not effective_ideas_file:
                    # 2026-09-15 ②：确定性模板文档（feature_engineering.py 8 问框架渲染）
                    # 不再自动注入——注入后 GEM 一行 LLM 都不调，整波退化为
                    # `rank(ts_mean({f},66))` 式模板展开（GBR intraday_pv_feats 实证）。
                    # （若该路径同时已失效，上面第一个分支已按"无 ideas"处理。）
                    result["steps"].append({
                        "step": "s1_ledger_check",
                        "success": True,
                        "s1_key": s1_key,
                        "ideas_md_path": s1_ledger["ideas_md_path"],
                        "auto_inject": False,
                        "skipped_reason": f"source={s1_ledger.get('source')!r} 是模板渲染文档，"
                                          "GEM 改走概念优先自含生成（显式 ideas_file 可覆盖）",
                    })
                else:
                    if not effective_ideas_file:
                        # 路径已失效但用户没给显式 ideas_file：同样视为无 ideas，
                        # 不注入死路径（否则 check_ideas_format 必挂）。
                        if _ledger_ideas_exists or ideas_file:
                            effective_ideas_file = s1_ledger["ideas_md_path"]
                    result["steps"].append({
                        "step": "s1_ledger_check",
                        "success": True,
                        "s1_key": s1_key,
                        "ideas_md_path": s1_ledger["ideas_md_path"],
                        "auto_inject": not ideas_file,
                        "override": bool(ideas_file),
                    })
        except Exception as e:
            logger.warning(f"Failed to check S1 ledger: {e}")

        try:
            field_prefix_summary = store.get_field_prefix_clusters(region, dataset_id)
            if not field_prefix_summary and s1_ledger:
                field_prefix_summary = s1_ledger.get("field_prefix_summary")
            if field_prefix_summary:
                result["steps"].append({
                    "step": "field_prefix_summary_check",
                    "success": True,
                    "s1_prefix_key": f"s1_prefix_{dataset_id}",
                    "total_fields": field_prefix_summary.get("total_fields"),
                    "total_clusters": field_prefix_summary.get("total_clusters"),
                    "auto_inject": True,
                })
        except Exception as e:
            logger.warning(f"Failed to check field prefix summary: {e}")

        try:
            pool_payload = store.get_candidate_field_pool(region, dataset_id)
            if not pool_payload:
                # dry-run 下不落库：只算不写
                pool_payload = store.build_candidate_field_pool(
                    region, dataset_id, persist=not dry_run
                )
            candidate_field_pool = (pool_payload or {}).get("candidate_field_pool", [])
            if candidate_field_pool:
                result["steps"].append({
                    "step": "candidate_field_pool_check",
                    "success": True,
                    "s2_field_pool_key": f"s2_field_pool_{dataset_id}",
                    "pool_size": len(candidate_field_pool),
                    "auto_inject": True,
                })
        except Exception as e:
            logger.warning(f"Failed to check candidate field pool: {e}")

    # Step 2: 定位 GEM runner
    gem_root = resolve_skill_dir("brain-make-some-gem")
    if not gem_root:
        result["steps"].append({
            "step": "find_gem_root",
            "success": False,
            "error": "brain-make-some-gem skill not found",
        })
        return result

    runner_script = os.path.join(gem_root, "scripts", "headless_runner", "run.py")
    config_file = os.path.join(gem_root, "scripts", "headless_runner", "config.json")

    if not os.path.exists(runner_script):
        result["steps"].append({
            "step": "find_gem_root",
            "success": False,
            "error": f"run.py not found at {runner_script}",
        })
        return result

    # Step 3: 检查 config.json
    if not os.path.exists(config_file):
        result["steps"].append({
            "step": "check_config",
            "success": False,
            "error": f"config.json not found at {config_file}. Copy from config.example.json and fill credentials.",
            "fallback": f"cp {config_file.replace('config.json', 'config.example.json')} {config_file}",
        })
        return result

    result["steps"].append({
        "step": "check_config",
        "success": True,
        "config_file": config_file,
    })

    # Step 4: 构建命令
    # 2026-09-08：解释器加 `-u`（与 batch_track 同源修复）。run.py 在 --detached
    # 下会再 spawn 一个后台 child 并把它的 stdout 重定向到日志文件；Python 默认
    # 块缓冲，进程退出时未满的缓冲直接丢 —— 表现为任务日志 0 字节，外部完全看不出
    # 发生过什么。`-u` 管住启动器，Popen 的 PYTHONUNBUFFERED 管住它的孙子进程。
    cmd = [
        wq_py(),
        "-u",
        runner_script,
        "--config", config_file,
        "--data-category", data_category,
        "--region", region,
        "--delay", str(delay),
        "--dataset-id", dataset_id,
        "--universe", universe,
        "--instrument-type", instrument_type,
        "--data-type", data_type,
    ]

    if priors_file:
        cmd.extend(["--priors-file", priors_file])
    elif priors_from_db:
        # 2026-09-04 修复：默认走 DB 快照直读（SOP「DB 为单一事实源」），
        # 修复 wave112 之前 GEM 命令无任何 priors 参数导致知识库模板未注入的断点
        cmd.extend(["--priors-from-db", region])
        # 2026-09-09 修复：显式传 --db-path 绝对路径。headless_runner/run.py 的
        # _materialize_priors_from_db 在 build_command() 内被调，而 build_command
        # 在 os.chdir(trailSomeAlphas) 之后还会再调一次 —— 那时 cwd 向上 8 级
        # 找不到 data/wqb.db，且 unbuffered_env 不设 WQB_WORKSPACE/WQB_DB_PATH，
        # _find_wqb_db 探测链全灭 → SystemExit fail-closed。传绝对路径后第一级命中。
        cmd.extend(["--db-path", resolve_db_path()])

    if effective_ideas_file:
        cmd.extend(["--ideas-file", effective_ideas_file])

    # 2026-09-18 ③：pipeline_mode 默认 phased（三阶段分批），解决全量大字段集
    # single-shot 模式 LLM 生成超时问题。显式传 None 才走 headless_runner 的
    # config.json 解析链（config.json `pipeline_mode` → 缺省 phased）。
    if pipeline_mode:
        _mode = str(pipeline_mode).strip().lower()
        if _mode not in ("single", "phased", "skeleton"):
            result["steps"].append({
                "step": "validate_pipeline_mode", "success": False,
                "error": f"pipeline_mode 必须是 single/phased/skeleton，收到 {pipeline_mode!r}",
            })
            result["success"] = False
            result["error"] = f"invalid pipeline_mode: {pipeline_mode!r}"
            return result
        cmd.extend(["--pipeline-mode", _mode])
        if _mode == "skeleton" and effective_ideas_file:
            # skeleton 模式自产 ideas，不消费 ideas 文件（run_pipeline.py 同口径）
            cmd = [c for i, c in enumerate(cmd)
                   if not (c == "--ideas-file" or (i > 0 and cmd[i - 1] == "--ideas-file"))]
        elif _mode == "phased" and batch_size:
            # phased 模式：透传 batch_size（默认 100，防拆散同族字段）
            cmd.extend(["--batch-size", str(int(batch_size))])

    if detached:
        cmd.append("--detached")

    # 2026-09-17 #6：多样性强制（此前 headless_runner 有这两个参数、但本节点**从未透传**，
    # 等于"要求了多样性却没人下指令"。run.py 的 --require-operators 是
    # "comma operators for diversity mandate"，--require-count 是"最少几条用到它们"。
    if require_operators:
        cmd.extend(["--require-operators", str(require_operators)])
        cmd.extend(["--require-count", str(require_count)])

    # P0 修复（2026-09-12）：统一 gem 任务根目录到 logs/_async_tasks，
    # 与 batch_track / campaign / feature_engineering 一致，使
    # workflow_task_status 能发现 gem 任务。原实现解析到
    # headless_runner/outputs/tasks（该目录从不存在），导致 90s 超时误杀。
    tasks_dir = os.path.abspath(
        os.environ.get("WQB_TASK_ROOT") or os.path.join(REPO_ROOT, "logs", "_async_tasks")
    )
    os.makedirs(tasks_dir, exist_ok=True)
    cmd.extend(["--tasks-dir", tasks_dir])

    # argv 契约校验（2026-09-06）：headless_runner/run.py 的 argparse 必须接受本命令。
    # 干跑与实跑都走，避免"命令构建成功 → Popen → 秒退"被吞成 success。
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

    # Step 4.5: ideas 文件格式预检（Popen 前零成本拦截）
    # run_pipeline 在 BRAIN 登录与数据准备之后才解析 **Concept** 块，格式错误会白烧一轮
    # 认证/拉数；这里用同一套块解析规则提前校验，不通过则不启动任何进程。
    ideas_check = {"step": "check_ideas_format", "success": True}
    if effective_ideas_file:
        chk = _check_ideas_file(effective_ideas_file)
        ideas_check.update({
            "success": chk["ok"],
            "ideas_file": effective_ideas_file,
            "blocks": chk["blocks"],
        })
        if not chk["ok"]:
            ideas_check["errors"] = chk["errors"]
            ideas_check["sample"] = chk.get("sample", "")
            result["steps"].append(ideas_check)
            return result
    else:
        ideas_check["message"] = "no ideas file (pipeline will auto-generate); pre-check skipped"
    result["steps"].append(ideas_check)

    # dry-run：命令已构建、前置已验，未执行
    if dry_run:
        result["success"] = True
        result["note"] = "dry-run：命令已构建，未执行"
        result["command"] = " ".join(cmd)
        result["plan"] = {
            "region": region,
            "dataset_id": dataset_id,
            "delay": delay,
            "universe": universe,
            "data_category": data_category,
            "instrument_type": instrument_type,
            "data_type": data_type,
            "priors_from_db": priors_from_db and not priors_file,
            "priors_file": priors_file,
            "ideas_file": effective_ideas_file,
            "gem_root": gem_root,
            "runner_script": runner_script,
            "detached": detached,
        }
        return result

    # Step 5: 执行
    try:
        logger.info(f"Executing GEM: {' '.join(cmd)}")

        if detached:
            # P1 修复（2026-09-12）：launch_only 模式 —— Popen 后立即返回，
            # 不等 meta.json 握手。MCP 客户端超时通常 30-60s，而 gem 启动链
            # （venv 两段式 + import + 写 meta）可能 20-30s+，90s 握手窗口
            # 仍可能撞客户端超时。launch_only=True 时 1s 内返回，Agent 用
            # workflow_task_status 轮询后续状态。
            if launch_only:
                # 2026-09-12 修复(2)：launch_only 不能用 stdout/stderr=PIPE —— 本函数
                # 立即 return，Popen 对象随之被回收、管道读端关闭，launcher 第一次
                # print 就撞 BrokenPipe，死在写 meta.json 之前（GBR wave57 实测：
                # 4 个 launcher 3 个无声退出、0 个 task 目录）。改为落到 tasks_dir 下
                # 的启动日志，子进程继承文件句柄，父进程关掉自己那份即可。
                import time
                os.makedirs(tasks_dir, exist_ok=True)
                stamp = time.strftime("%Y%m%d_%H%M%S")
                launch_log = os.path.join(
                    tasks_dir, f"gem_launch_{region}_{dataset_id}_{stamp}.log"
                )
                with open(launch_log, "a", encoding="utf-8") as log_fh:
                    process = subprocess.Popen(
                        cmd,
                        stdout=log_fh,
                        stderr=subprocess.STDOUT,
                        stdin=subprocess.DEVNULL,
                        cwd=os.path.dirname(runner_script),
                        env=unbuffered_env(),
                    )
                result["steps"].append({
                    "step": "execute",
                    "success": True,
                    "detached": True,
                    "launch_only": True,
                    "pid": process.pid,
                    "tasks_dir": tasks_dir,
                    "launch_log": launch_log,
                    "command": " ".join(cmd),
                })
                result["success"] = True
                result["detached"] = True
                result["launch_only"] = True
                result["pid"] = process.pid
                result["tasks_dir"] = tasks_dir
                result["launch_log"] = launch_log
                result["message"] = (
                    f"GEM launch_only task started: pid={process.pid}. "
                    f"Launcher output -> {launch_log}; "
                    f"poll workflow_task_status(prefix='gem_') for status."
                )
                return result

            # detached 模式：轮询磁盘上新 task 的 meta.json，不依赖 stdout 文本握手。
            # 2026-09-03 修复：原实现 communicate/readline 抓 stdout 的 task_id= 行，
            # 受 MCP 客户端超时窗口与管道缓冲影响易挂死；run.py spawn 后台 child 后会把
            # task_id/pid/日志路径先写入 <tasks_dir>/<task_id>/meta.json 再退出，磁盘轮询最稳。
            # 2026-09-12 修复：pre_existing 快照必须在 Popen 之前拍 —— 原实现先启动再取
            # 快照，若 launcher 抢先建出 task 目录，该目录被并入快照而永远识别不到 →
            # 即使任务已启动也必然等满超时并误杀。
            import time
            pre_existing = set(os.listdir(tasks_dir)) if os.path.isdir(tasks_dir) else set()

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.path.dirname(runner_script),
                # PYTHONUNBUFFERED 传给 run.py 及其 spawn 的后台 child —— 后者的
                # stdout_log 才是长跑任务唯一的可观测手段
                env=unbuffered_env(),
            )
        else:
            # 2026-09-12 修复(2)：P1 编辑把 Popen 挪进了 detached 分支，非 detached
            # 路径下 `process` 从未赋值 → communicate 处 UnboundLocalError
            # （test_gem_consumes_field_prefix_summary 复现）。恢复同步模式的启动。
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.path.dirname(runner_script),
                env=unbuffered_env(),
            )

        if detached:
            task_meta = None
            task_dir = None
            start = time.time()
            # 2026-09-12：30s 太紧 —— 本机 venv python 为两段式启动（wrapper→real），
            # 冷加载/AV 扫描可将 "import → 写 meta" 拉长到 20-30s+；默认放宽到 90s，
            # 可用环境变量 GEM_META_TIMEOUT_SEC 覆盖。
            deadline_sec = float(os.environ.get("GEM_META_TIMEOUT_SEC", "90"))
            deadline = start + deadline_sec
            heartbeat_interval = 5  # 每 5 秒输出一次心跳
            last_heartbeat = start
            logger.info(f"[GEM-START] waiting for meta.json, timeout={deadline_sec:.0f}s, tasks_dir={tasks_dir}")
            while time.time() < deadline:
                if os.path.isdir(tasks_dir):
                    for d in sorted(set(os.listdir(tasks_dir)) - pre_existing):
                        meta_path = os.path.join(tasks_dir, d, "meta.json")
                        if not os.path.isfile(meta_path):
                            continue
                        try:
                            with open(meta_path, "r", encoding="utf-8") as mf:
                                task_meta = json.load(mf)
                            task_dir = os.path.join(tasks_dir, d)
                            break
                        except Exception:
                            continue
                    if task_meta:
                        break
                if process.poll() is not None:
                    break  # 启动器已退出（meta.json 必在其退出前落盘）→ 成败已定
                # 心跳日志：每 5 秒输出一次等待状态
                elapsed = time.time() - start
                if time.time() - last_heartbeat >= heartbeat_interval:
                    new_dirs = set(os.listdir(tasks_dir)) - pre_existing if os.path.isdir(tasks_dir) else set()
                    logger.info(f"[GEM-WAIT] {elapsed:.0f}s elapsed, still initializing... (new_task_dirs={len(new_dirs)})")
                    last_heartbeat = time.time()
                time.sleep(0.3)

            process_stdout = ""
            process_stderr = ""
            if not task_meta:
                try:
                    process_stdout, process_stderr = process.communicate(timeout=5)
                except Exception:
                    # 2026-09-12：整树收尸。本机 venv python 为两段式启动
                    # （wrapper→real，meta.pid 只是 wrapper），只 kill() 直接子进程会
                    # 留下仍在慢启动的孤儿；Windows 用 taskkill /F /T 收整棵树。
                    killed = False
                    if os.name == "nt":
                        try:
                            subprocess.run(
                                ["taskkill", "/F", "/T", "/PID", str(process.pid)],
                                capture_output=True,
                                timeout=15,
                            )
                            killed = True
                        except Exception:
                            killed = False
                    if not killed:
                        try:
                            process.kill()
                        except Exception:
                            pass
                # 终扫：meta 若在等待窗口之后才落盘，标记 killed_by_watchdog，
                # 杜绝"被收尸的进程 meta 永久停留 running"的假状态
                if os.path.isdir(tasks_dir):
                    for d in sorted(set(os.listdir(tasks_dir)) - pre_existing):
                        late_meta_path = os.path.join(tasks_dir, d, "meta.json")
                        if not os.path.isfile(late_meta_path):
                            continue
                        try:
                            with open(late_meta_path, "r", encoding="utf-8") as mf:
                                late_meta = json.load(mf)
                            late_meta["status"] = "killed_by_watchdog"
                            late_meta["error"] = "meta arrived after timeout window; launcher tree killed"
                            with open(late_meta_path, "w", encoding="utf-8") as mf:
                                json.dump(late_meta, mf, ensure_ascii=False, indent=2)
                            logger.warning(f"[GEM-KILL] late meta marked killed_by_watchdog: {late_meta_path}")
                        except Exception:
                            pass
                        break

            if task_meta:
                # 收尸：launcher 写完 meta 后即将退出；短超时 drain 管道，
                # 避免其后续 print 撞上已关闭的管道（BrokenPipe → 误翻状态）
                try:
                    if process.poll() is None:
                        process.communicate(timeout=10)
                except Exception:
                    pass
                result["steps"].append({
                    "step": "execute",
                    "success": True,
                    "detached": True,
                    "task_id": task_meta.get("task_id"),
                    "task_dir": task_dir,
                    "pid": task_meta.get("pid"),
                    "stdout_log": task_meta.get("stdout_log"),
                    "stderr_log": task_meta.get("stderr_log"),
                })
                result["success"] = True
                result["detached"] = True
                result["task_id"] = task_meta.get("task_id")
                result["task_dir"] = task_dir
                result["pid"] = task_meta.get("pid")
                result["stdout_log"] = task_meta.get("stdout_log")
                result["stderr_log"] = task_meta.get("stderr_log")
                result["message"] = (
                    f"GEM detached task launched: {task_meta.get('task_id')}. "
                    f"Poll stdout_log / task_dir for final_expressions.json"
                )
                return result

            # 未命中 meta.json：启动失败或超时，返回诊断信息
            stdout_tail = (process_stdout or "")[-1000:]
            stderr_tail = (process_stderr or "")[-1000:]
            rc = process.returncode
            new_dirs_now = (
                set(os.listdir(tasks_dir)) - pre_existing if os.path.isdir(tasks_dir) else set()
            )
            if rc not in (None, 0):
                error = f"detached launcher exited rc={rc} before writing meta.json"
            elif rc is None:
                if new_dirs_now:
                    error = (
                        f"detached launcher running; task dir appeared "
                        f"but meta.json not ready within {deadline_sec:.0f}s (slow startup?)"
                    )
                else:
                    error = (
                        f"detached launcher still running but no meta.json within "
                        f"{deadline_sec:.0f}s"
                    )
            else:
                error = "detached launcher exited without writing meta.json (unexpected)"
            result["steps"].append({
                "step": "execute",
                "success": False,
                "detached": True,
                "error": error,
                "stdout_tail": stdout_tail,
                "stderr_tail": stderr_tail,
                "tasks_dir": tasks_dir,
            })
            result["message"] = error
            return result
        else:
            # 非 detached：等待完成（带超时）
            stdout, stderr = process.communicate(timeout=1800)  # 30 分钟

            success = process.returncode == 0
            result["steps"].append({
                "step": "execute",
                "success": success,
                "returncode": process.returncode,
                "stdout_tail": stdout[-1000:] if stdout else "",
                "stderr_tail": stderr[-1000:] if stderr else "",
            })

        # Step 6: 检查产物
        final_expr_path = _find_final_expressions(gem_root, dataset_id, region, delay)
        if final_expr_path and os.path.exists(final_expr_path):
            with open(final_expr_path, "r", encoding="utf-8") as f:
                expressions = json.load(f)

            result["steps"].append({
                "step": "check_output",
                "success": True,
                "final_expressions_path": final_expr_path,
                "expression_count": len(expressions),
            })

            result["success"] = True
            result["final_expressions_path"] = final_expr_path
            result["expression_count"] = len(expressions)
            result["field_prefix_summary"] = field_prefix_summary or {}
            result["candidate_field_pool"] = candidate_field_pool
            # 2026-09-17 #1：把本次生成的表达式标注来源（source）。
            # 此前**全链路无人写 source** → 全库 89.8% 为 NULL、GEM 产出不可辨识
            # （按 source 过滤只能看到一个月前的语料），也无法做 phased/skeleton 的 A/B。
            # 这里用 final_expressions.json 里**确切的表达式串**回写（不是按 id 区间猜）。
            result["source_labeled"] = _label_source(
                expressions, region, pipeline_mode,
            )

            # Step 7: 质量预估（特征工程 SOP 阶段5，强制）
            quality_result = _run_quality_estimation(
                region=region,
                dataset_id=dataset_id,
                final_expr_path=final_expr_path,
                expressions=expressions,
                store=store,
                field_prefix_summary=field_prefix_summary,
            )
            result["steps"].append(quality_result)
            result["quality_estimation"] = quality_result

            # 如果质量预估发现 EXPECTED_BLOCK，标记需要 Mode B
            if quality_result.get("expected_block_count", 0) > 0:
                result["mode_b_required"] = True
                result["mode_b_reason"] = f"{quality_result['expected_block_count']} candidates EXPECTED_BLOCK"

            # 保存到 DB
            if store:
                try:
                    store.upsert_ledger("WORKFLOW", f"gem_{region}_{dataset_id}_{datetime.now().strftime('%Y%m%d')}", {
                        "generated_at": datetime.now().isoformat(),
                        "region": region,
                        "dataset_id": dataset_id,
                        "expression_count": len(expressions),
                        "final_expressions_path": final_expr_path,
                        "field_prefix_summary": field_prefix_summary or {},
                        "candidate_field_pool": candidate_field_pool,
                        "quality_estimation": quality_result,
                        "mode_b_required": result.get("mode_b_required", False),
                    })
                except Exception as e:
                    logger.warning(f"Failed to save GEM record: {e}")
        else:
            result["steps"].append({
                "step": "check_output",
                "success": False,
                "error": "final_expressions.json not found",
            })

    except subprocess.TimeoutExpired:
        process.kill()
        result["steps"].append({
            "step": "execute",
            "success": False,
            "error": "Timeout after 1800s",
        })
    except Exception as e:
        logger.exception("GEM execution failed")
        result["steps"].append({
            "step": "execute",
            "success": False,
            "error": str(e),
        })

    return result


def _parse_ideas_blocks(markdown_text: str) -> List[Dict[str, str]]:
    """解析 ideas markdown 中的 **Concept** 块（与 run_pipeline.extract_template_blocks 同规则）.

    有效块 = 以 **Concept** 开头、含 **Implementation Example** 行且模板含
    {variable} 占位符（支持反引号包裹/同行/后续 3 行内三种模板位置）。
    """
    concept_re = re.compile(r"^\*\*Concept\*\*\s*:\s*(.*)\s*$")
    impl_re = re.compile(r"\*\*Implementation Example\*\*\s*:\s*(.*)$", re.IGNORECASE)
    backtick_re = re.compile(r"`([^`]*)`")
    boundary_re = re.compile(r"^(?:-{3,}|#{1,6}\s+.*)\s*$")

    lines = markdown_text.splitlines()
    blocks: List[List[str]] = []
    current: List[str] = []
    for line in lines:
        if concept_re.match(line.strip()):
            if current:
                blocks.append(current)
            current = [line]
            continue
        if current and boundary_re.match(line.strip()):
            blocks.append(current)
            current = []
            continue
        if current:
            current.append(line)
    if current:
        blocks.append(current)

    out: List[Dict[str, str]] = []
    for block_lines in blocks:
        template: Optional[str] = None
        impl_line_idx: Optional[int] = None
        for i, raw in enumerate(block_lines):
            m = impl_re.search(raw)
            if not m:
                continue
            impl_line_idx = i
            tail = (m.group(1) or "").strip()
            bt = backtick_re.search(tail)
            if bt:
                template = bt.group(1).strip()
                break
            if tail and ("{" in tail and "}" in tail):
                template = tail.strip().strip("`")
                break
            for j in range(i + 1, min(i + 4, len(block_lines))):
                nxt = block_lines[j].strip()
                if not nxt:
                    continue
                bt2 = backtick_re.search(nxt)
                if bt2:
                    template = bt2.group(1).strip()
                    break
                if "{" in nxt and "}" in nxt:
                    template = nxt.strip().strip("`")
                    break
            break
        if not template or "{" not in template or "}" not in template:
            continue
        idea_lines = [ln for k, ln in enumerate(block_lines) if k != impl_line_idx]
        out.append({"template": template.strip(), "idea": "\n".join(idea_lines).strip()})
    return out


def _check_ideas_file(file_path: str) -> Dict[str, Any]:
    """预检 ideas 文件是否含至少一个可实现的 **Concept** 块（run_pipeline 硬性要求）.

    Returns:
        预检结果（ok/blocks/errors/sample），失败时附合规示例供快速修正。
    """
    result: Dict[str, Any] = {"ok": True, "blocks": 0, "errors": []}
    if not os.path.exists(file_path):
        result["ok"] = False
        result["errors"].append(f"ideas file not found: {file_path}")
        return result
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        result["ok"] = False
        result["errors"].append(f"failed to read ideas file: {e}")
        return result
    blocks = _parse_ideas_blocks(text)
    result["blocks"] = len(blocks)
    if not blocks:
        result["ok"] = False
        result["errors"].append(
            "no valid **Concept** block with **Implementation Example** found "
            "(each must include a {variable} template)"
        )
        result["sample"] = (
            "**Concept**: <signal idea>\n"
            "- **Implementation Example**: `<operator({variable})>`\n"
            "- **Rationale**: <why this might work>"
        )
    return result


def _infer_category(dataset_id: str) -> str:
    """从 dataset_id 推断数据类别（向后兼容别名，实际逻辑在 _common）。"""
    return infer_data_category(dataset_id)


def _find_gem_root() -> Optional[str]:
    """查找 brain-make-some-gem skill 根目录（向后兼容别名）。"""
    return resolve_skill_dir("brain-make-some-gem")


def _label_source(expressions: Any, region: str, pipeline_mode: Optional[str]) -> int:
    """把本次 GEM 产出的 `expressions.source` 标注为具体生成模式（best-effort）。

    标签取值：`gem_<mode>`（`gem_phased` / `gem_skeleton` / `gem_single`），
    mode 未知时退化为 `gem`。

    **只标 NULL/空** —— 不覆盖上游已写入的更具体来源（人工标注优先）。
    任何异常都吞掉并返回 0：本函数是**可观测性增强**，不得影响生成主流程。
    """
    try:
        items = []
        for e in (expressions or []):
            if isinstance(e, str):
                if e.strip():
                    items.append(e.strip())
            elif isinstance(e, dict):
                v = (e.get("expression") or e.get("expr") or "").strip()
                if v:
                    items.append(v)
        if not items:
            return 0
        label = "gem"
        if pipeline_mode and str(pipeline_mode).strip():
            label = f"gem_{str(pipeline_mode).strip().lower()}"
        conn = sqlite3.connect(resolve_db_path())
        try:
            cur = conn.cursor()
            n = 0
            for expr in items:
                cur.execute(
                    "UPDATE expressions SET source=?, updated_at=datetime('now') "
                    "WHERE region=? AND expression=? AND (source IS NULL OR source='')",
                    (label, region, expr),
                )
                n += cur.rowcount
            conn.commit()
            return n
        finally:
            conn.close()
    except Exception:
        return 0


def _find_final_expressions(gem_root: str, dataset_id: str, region: str, delay: int) -> Optional[str]:
    """查找 final_expressions.json 路径."""
    # 标准路径
    path = os.path.join(
        gem_root,
        "scripts", "trailSomeAlphas", "skills", "brain-feature-implementation",
        "data", f"{dataset_id}_{region}_delay{delay}",
        "final_expressions.json"
    )
    if os.path.exists(path):
        return path

    # 备用路径
    alt_path = os.path.join(
        gem_root,
        "scripts", "headless_runner", "outputs",
        f"{dataset_id}_{region}_delay{delay}",
        "final_expressions.json"
    )
    if os.path.exists(alt_path):
        return alt_path

    return None


def _run_quality_estimation(
    region: str,
    dataset_id: str,
    final_expr_path: str,
    expressions: List[Dict],
    store: Optional[Any] = None,
    field_prefix_summary: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """运行质量预估（特征工程 SOP 阶段5）.

    调用 tools/quality_predict.py 和 tools/pool_diversity.py 进行零配额预检。
    """
    result = {
        "step": "quality_estimation",
        "success": True,
        "expected_pass": 0,
        "expected_review": 0,
        "expected_block": 0,
        "expected_block_count": 0,
        "diversity_risks": [],
        "details": {
            "field_prefix_summary": field_prefix_summary or {},
        },
    }

    # 1. 运行 pool_diversity.py（六维多样性评估）
    try:
        diversity_cmd = [
            wq_py(), "tools/pool_diversity.py",
            "--region", region,
            "--dataset", dataset_id,
            "--json", "-",  # 输出到 stdout
        ]

        # 如果 final_expr_path 存在，也传入
        if os.path.exists(final_expr_path):
            diversity_cmd.extend(["--input", final_expr_path])

        diversity_proc = subprocess.run(
            diversity_cmd,
            capture_output=True,
            text=True,
            timeout=300,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        )

        if diversity_proc.returncode == 0 and diversity_proc.stdout:
            try:
                diversity_data = json.loads(diversity_proc.stdout)
                result["details"]["diversity"] = diversity_data

                # 检查风险标记
                if diversity_data.get("group_dominance_risk"):
                    result["diversity_risks"].append("GROUP-DOMINANCE")
                if diversity_data.get("homogeneity_risk"):
                    result["diversity_risks"].append("HOMOG")
                if diversity_data.get("operator_entropy", 10) < 2.0:
                    result["diversity_risks"].append("LOW-ENTROPY")

            except json.JSONDecodeError:
                logger.warning("Failed to parse pool_diversity output")

    except Exception as e:
        logger.warning(f"pool_diversity.py failed: {e}")
        result["details"]["diversity_error"] = str(e)

    # 2. 运行 quality_predict.py（逐候选质量预估）
    try:
        # 先写入临时文件供 quality_predict 读取
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(expressions, f, ensure_ascii=False)
            temp_expr_path = f.name

        try:
            quality_cmd = [
                wq_py(), "tools/quality_predict.py",
                "--region", region,
                "--input", temp_expr_path,
                "--json", "-",
            ]

            quality_proc = subprocess.run(
                quality_cmd,
                capture_output=True,
                text=True,
                timeout=300,
                cwd=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            )

            if quality_proc.returncode == 0 and quality_proc.stdout:
                try:
                    quality_data = json.loads(quality_proc.stdout)
                    result["details"]["quality_predict"] = quality_data

                    # 统计判定结果
                    for item in quality_data.get("candidates", []):
                        verdict = item.get("verdict", "")
                        if verdict == "EXPECTED_PASS":
                            result["expected_pass"] += 1
                        elif verdict == "REVIEW":
                            result["expected_review"] += 1
                        elif verdict == "EXPECTED_BLOCK":
                            result["expected_block"] += 1

                    result["expected_block_count"] = result["expected_block"]

                except json.JSONDecodeError:
                    logger.warning("Failed to parse quality_predict output")

        finally:
            # 清理临时文件
            if os.path.exists(temp_expr_path):
                os.unlink(temp_expr_path)

    except Exception as e:
        logger.warning(f"quality_predict.py failed: {e}")
        result["details"]["quality_predict_error"] = str(e)

    # 3. 如果有 store，保存预估结果
    if store and result["expected_block_count"] > 0:
        try:
            store.upsert_ledger("QUALITY", f"gem_{region}_{dataset_id}_{datetime.now().strftime('%Y%m%d_%H%M')}", {
                "estimated_at": datetime.now().isoformat(),
                "region": region,
                "dataset_id": dataset_id,
                "expected_pass": result["expected_pass"],
                "expected_review": result["expected_review"],
                "expected_block": result["expected_block"],
                "diversity_risks": result["diversity_risks"],
            })
        except Exception as e:
            logger.warning(f"Failed to save quality estimation: {e}")

    return result
