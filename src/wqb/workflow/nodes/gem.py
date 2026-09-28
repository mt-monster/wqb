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
import tempfile
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..mcp_check import require_mcp_tools
from .._common import (
    REPO_ROOT,
    detached_launch_failed,
    infer_data_category,
    local_ts,
    resolve_async_tasks_root,
    resolve_db_path,
    resolve_gem_data_dir,
    resolve_skill_dir,
    unbuffered_env,
    validate_argv,
    wq_py,
)

from wqb.db_conn import connect as db_connect  # 规范工厂（2026-09-20 L1 收口）
logger = logging.getLogger(__name__)


#: S1 ledger `source` 属于确定性模板渲染（brain-data-feature-engineering/scripts/
#: feature_engineering.py，无 LLM）的取值；这类文档不作为 GEM 的 ideas 输入。
TEMPLATE_IDEAS_SOURCES = ("feature_engineering_node", "standalone", "standalone_v2")


def is_template_ideas_source(source: Optional[str]) -> bool:
    src = str(source or "").strip()
    return any(src == t or src.startswith(t + " ") or src.startswith(t + "(")
               for t in TEMPLATE_IDEAS_SOURCES)


#: priors 快照的 ledger 源（assemble_priors.py 读这三个键；另读 registry_empirical 的
#: win / dead_end 层，见下）。任一比快照新 = 快照已过期。
_PRIORS_SOURCES = (("{region}", "region_kb"), ("KB", "template_kb"), ("KB", "operator_principle_kb"))


#: 时间戳统一成本地时间便于比较（两种写入口径见 `_common.local_ts`；2026-09-27 提升为公共函数）
_ledger_ts = local_ts


def _priors_snapshot_freshness(region: str) -> Dict[str, Any]:
    """GEM 读的 priors 快照是否落后于它的 KB 源（2026-09-27 P0-2）。

    GEM 默认 `--priors-from-db`，只读 ledger `priors_snapshot_<region>`；快照只由
    `campaign.py assemble-priors --snapshot-ledger` 写。S6 回写 / pipeline 波后刷新
    region_kb / 判死封存（registry dead_end）/ 登记 win 之后若没重组，GEM 会静默沿用旧先验
    ——这里把它变成可见告警。时间戳口径见 `_ledger_ts`。只读、零配额，不阻断
    （缺快照时 GEM 自身会 fail-closed）。
    """
    step: Dict[str, Any] = {"step": "priors_snapshot_check", "success": True}
    r = str(region or "").strip().upper()
    key = f"priors_snapshot_{r.lower()}"
    step["snapshot_key"] = key
    db = resolve_db_path()
    if not os.path.isfile(db):
        step["warning"] = f"战役库不存在（{db}），无法检查 priors 快照 {key}"
        return step
    try:
        conn = db_connect(db)
        try:
            snap = conn.execute(
                "SELECT updated_at FROM ledger_kv WHERE region=? AND key=?", (r, key)
            ).fetchone()
            sources = []
            for src_region, src_key in _PRIORS_SOURCES:
                src_region = src_region.format(region=r)
                row = conn.execute(
                    "SELECT updated_at FROM ledger_kv WHERE region=? AND key=?",
                    (src_region, src_key),
                ).fetchone()
                if row:
                    sources.append((f"{src_region}/{src_key}", _ledger_ts(row[0])))
            # registry_empirical：两类写入方时钟不同，SQL 的 MAX 按字符串比会错，逐行归一后取最大
            try:
                reg = [_ledger_ts(v) for (v,) in conn.execute(
                    "SELECT updated_at FROM registry_empirical "
                    "WHERE region=? AND layer IN ('win', 'dead_end') AND updated_at IS NOT NULL", (r,))]
            except sqlite3.OperationalError:  # 老库无该表
                reg = []
            if reg:
                sources.append((f"{r}/registry_empirical(win,dead_end)", max(reg)))
        finally:
            conn.close()
    except sqlite3.Error as e:
        step["warning"] = f"priors 快照检查读库失败：{e}"
        return step
    fix = (f"先跑 workflow_campaign(region='{r}', stage='S2', subcommand='assemble-priors')"
           f"（默认带 --snapshot-ledger）")
    if not snap:
        step["warning"] = f"DB 无 {r}/{key}：GEM（--priors-from-db）启动后会 fail-closed。{fix}"
        return step
    snap_ts = _ledger_ts(snap[0])
    step["snapshot_updated_at"] = snap_ts
    stale = [f"{name}@{ts}" for name, ts in sources if ts > snap_ts]
    if stale:
        step["stale_sources"] = stale
        step["warning"] = (f"priors 快照 {key}（{snap_ts}）早于其 KB 源 {', '.join(stale)}："
                           f"S6 回写后没重组 priors，本次 GEM 会用旧先验。{fix}")
    return step
# ---------------------------------------------------------------------------
# run() 步骤实现（2026-09-25 结构拆分）。run() 只做编排，实现下放私有函数，
# 行为与拆分前逐字等价。观测面冻结（tests 依赖）：run / _parse_ideas_blocks /
# _label_source / _find_final_expressions / _run_quality_estimation /
# is_template_ideas_source 的名称与调用约定不变；subprocess/os 仍从本模块引用
# （test_workflow_nodes monkeypatch gm.subprocess.Popen / gm.os.path.exists）。
# ---------------------------------------------------------------------------


def _spawn_process(
    cmd: List[str],
    runner_script: str,
    capture: bool = True,
    stdout: Any = None,
    stderr: Any = None,
):
    """统一 Popen 启动点（detached/launch_only/同步三路共用不变量）。

    - stdin 必须 DEVNULL：2026-09-21 根治 "no meta.json within 90s" —— MCP 服务
      进程的 stdin 是宿主的异步管道，子解释器继承它后在启动阶段永久阻塞（仅加载
      python313.dll、0 字节输出）；launch_only 分支早已 DEVNULL 且从不复现。
      任何从 MCP 服务 spawn 的子进程都必须显式断开 stdin
      （test_workflow_popen_stdin_devnull 守护）。
    - env=unbuffered_env()：PYTHONUNBUFFERED 传给 run.py 及其 spawn 的后台
      child —— 后者的 stdout_log 才是长跑任务唯一的可观测手段。
    """
    kw: Dict[str, Any] = {
        "stdin": subprocess.DEVNULL,
        "cwd": os.path.dirname(runner_script),
        "env": unbuffered_env(),
    }
    if capture:
        kw.update(stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    else:
        kw.update(stdout=stdout, stderr=stderr)
    return subprocess.Popen(cmd, **kw)


def _resolve_ideas_from_ledger(
    store: Any,
    region: str,
    dataset_id: str,
    delay: int,
    ideas_file: Optional[str],
    result: Dict[str, Any],
) -> Any:
    """Step 1A：S1 ledger 检查（自动注入 ideas-file）。

    显式 ideas_file 优先于 S1 ledger 自动注入。返回 (effective_ideas_file, s1_ledger)。
    """
    effective_ideas_file = ideas_file
    s1_ledger = None
    if not store:
        return effective_ideas_file, s1_ledger
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
    return effective_ideas_file, s1_ledger


def _load_field_context(
    store: Any,
    region: str,
    dataset_id: str,
    s1_ledger: Any,
    dry_run: bool,
    result: Dict[str, Any],
) -> Any:
    """Step 1B/1C：字段前缀摘要 + 候选字段池（经济学归类优先，cross_cluster 回退）。

    返回 (field_prefix_summary, candidate_field_pool)。
    """
    field_prefix_summary = None
    candidate_field_pool: List[str] = []
    if not store:
        return field_prefix_summary, candidate_field_pool
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
        # 2026-09-25 增强：优先使用经济学归类字段池（有经济学约束），
        # 无归类结果时回退旧 cross_cluster 池。
        pool_payload = store.get_candidate_field_pool(region, dataset_id)
        econ_pool_used = False
        if not pool_payload:
            # 尝试经济学归类池（v3）
            try:
                econ_payload = store.build_economic_field_pool(
                    region, dataset_id, persist=not dry_run
                )
                if econ_payload and not econ_payload.get("error") and econ_payload.get("candidate_field_pool"):
                    pool_payload = econ_payload
                    econ_pool_used = True
                    result["steps"].append({
                        "step": "economic_field_pool_check",
                        "success": True,
                        "s2_field_pool_key": f"s2_field_pool_{dataset_id}",
                        "pool_size": len(econ_payload["candidate_field_pool"]),
                        "categories_covered": econ_payload.get("economic_stats", {}).get("categories_covered", 0),
                        "source": "economic_category",
                        "auto_inject": True,
                    })
            except Exception as _econ_err:
                logger.debug(f"Economic field pool not available: {_econ_err}")

        if not pool_payload:
            # dry-run 下不落库：只算不写
            pool_payload = store.build_candidate_field_pool(
                region, dataset_id, persist=not dry_run
            )
        candidate_field_pool = (pool_payload or {}).get("candidate_field_pool", [])
        if candidate_field_pool and not econ_pool_used:
            # 只在非经济学池时记录 candidate_field_pool_check（避免重复）
            result["steps"].append({
                "step": "candidate_field_pool_check",
                "success": True,
                "s2_field_pool_key": f"s2_field_pool_{dataset_id}",
                "pool_size": len(candidate_field_pool),
                "auto_inject": True,
            })
    except Exception as e:
        logger.warning(f"Failed to check candidate field pool: {e}")
    return field_prefix_summary, candidate_field_pool


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
    console: bool = False,
    pipeline_mode: Optional[str] = "phased",
    batch_size: int = 100,
    require_operators: Optional[str] = None,
    require_count: int = 2,
    prod_first: bool = False,
    prod_first_top_k: int = 2,
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
        console: 在 detached 后台之外**再弹一个真实控制台窗口**滚动生成过程
            （2026-09-25，仅 Windows）。背景：run.py 的 detached 分支写死
            `DETACHED_PROCESS|CREATE_NO_WINDOW` + stdout 重定向到文件，MCP 服务
            又无控制台，所以整条链路"看得见"的只有日志文件。置 True 后子进程把
            stdout 交还给新窗口（人看）并经 _ConsoleFileTee 双写同一份
            stdout.log（机器看），--status / workflow_task_status 不受影响。
            代价：任务寿命绑在那个窗口上 —— 关窗口 = 杀任务，而 phased 无断点，
            中途被杀 = 整波丢弃；只在人盯盘时开。
        pipeline_mode: GEM 生成模式 single / phased / skeleton（2026-09-18 ③）。
            默认 "phased"（三阶段分批：structure→mapping→render），解决全量大字段集
            （如订单流 198 字段）single-shot 模式 LLM 生成超时（9+ 分钟）的问题。
            "single" = 一次性 LLM 调用（旧默认，仅小字段集 <50 适用）；
            "skeleton" = 骨架枚举 + LLM 填槽（语法构造保证）。
        batch_size: phased 模式下每批字段数（默认 100）。
            198 字段订单流实测：batch_size=50 拆散同族字段（bid_* / ask_* 跨批），
            跨族机制（如 ask-bid 价差）无法在同一批内设计；100 让同族字段同批。
        prod_first: 生成后、选波前做字段族级 prod 预筛（2026-09-24 P0 强度优先）。
            对候选按字段族分组，每组最强 top_k 条先跑 check_correlation(production)；
            prod ≥0.7 的族整族不再生成变体（当前是回测后才发现，已烧 8-24 条/族）。
            默认 False（灰度，不阻断主流程）。
        prod_first_top_k: 每族预筛条数（默认 2）。

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

    # Step 1: 检查 S1 ledger（自动注入 ideas-file）+ 字段上下文（实现见 _resolve_ideas_from_ledger / _load_field_context）
    effective_ideas_file, s1_ledger = _resolve_ideas_from_ledger(
        store, region, dataset_id, delay, ideas_file, result,
    )
    field_prefix_summary, candidate_field_pool = _load_field_context(
        store, region, dataset_id, s1_ledger, dry_run, result,
    )

    # Step 1.5：priors 快照新鲜度（零成本只读，干跑也走；只告警不阻断）
    if priors_from_db and not priors_file:
        snap_step = _priors_snapshot_freshness(region)
        result["steps"].append(snap_step)
        if snap_step.get("warning"):
            result.setdefault("warnings", []).append(snap_step["warning"])

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
        # 找不到 data/wqb.db，且（当时）unbuffered_env 不设 WQB_WORKSPACE/WQB_DB_PATH，
        # _find_wqb_db 探测链全灭 → SystemExit fail-closed。传绝对路径后第一级命中。
        # 2026-09-27 R19 起 unbuffered_env 缺省注入 WQB_WORKSPACE；显式 --db-path 仍保留
        # （第一级命中，且与本节点 resolve_db_path() 同一个库，不依赖子进程 env）。
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
        # 2026-09-25：--console 只在 detached 路径有意义（inline 本来就挂在调用方终端）
        if console:
            cmd.append("--console")

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
    tasks_dir = os.path.abspath(resolve_async_tasks_root())
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

    # Step 5-7.5：执行 + 产物收集（2026-09-25 结构拆分，实现下放 _execute_gem / _collect_results）
    try:
        if not _execute_gem(cmd, runner_script, tasks_dir, region, dataset_id,
                            launch_only, detached, result):
            return result
        return _collect_results(
            gem_root, dataset_id, region, delay, pipeline_mode, universe,
            field_prefix_summary, candidate_field_pool, store,
            prod_first, prod_first_top_k, result,
        )
    except subprocess.TimeoutExpired:
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


def _execute_gem(
    cmd: List[str],
    runner_script: str,
    tasks_dir: str,
    region: str,
    dataset_id: str,
    launch_only: bool,
    detached: bool,
    result: Dict[str, Any],
) -> bool:
    """Step 5：执行 GEM（launch_only / detached 握手 / 同步三路）。

    返回 True = 继续 Step 6 产物检查；False = 已终结（result 已填好），调用方 return result。
    2026-09-25 从 run() 内联体拆出，行为逐字保留（含历史修复注释）。
    """
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
            os.makedirs(tasks_dir, exist_ok=True)
            stamp = time.strftime("%Y%m%d_%H%M%S")
            launch_log = os.path.join(
                tasks_dir, f"gem_launch_{region}_{dataset_id}_{stamp}.log"
            )
            with open(launch_log, "a", encoding="utf-8") as log_fh:
                process = _spawn_process(
                    cmd, runner_script, capture=False,
                    stdout=log_fh, stderr=subprocess.STDOUT,
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
            return False

        # detached 模式：轮询磁盘上新 task 的 meta.json，不依赖 stdout 文本握手。
        # 2026-09-03 修复：原实现 communicate/readline 抓 stdout 的 task_id= 行，
        # 受 MCP 客户端超时窗口与管道缓冲影响易挂死；run.py spawn 后台 child 后会把
        # task_id/pid/日志路径先写入 <tasks_dir>/<task_id>/meta.json 再退出，磁盘轮询最稳。
        # 2026-09-12 修复：pre_existing 快照必须在 Popen 之前拍 —— 原实现先启动再取
        # 快照，若 launcher 抢先建出 task 目录，该目录被并入快照而永远识别不到 →
        # 即使任务已启动也必然等满超时并误杀。
        pre_existing = set(os.listdir(tasks_dir)) if os.path.isdir(tasks_dir) else set()

        process = _spawn_process(cmd, runner_script)

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
            return False

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
        return False

    # 非 detached：等待完成（带超时）
    try:
        process = _spawn_process(cmd, runner_script)
        stdout, stderr = process.communicate(timeout=1800)  # 30 分钟
    except subprocess.TimeoutExpired:
        try:
            process.kill()
        except Exception:
            pass
        result["steps"].append({
            "step": "execute",
            "success": False,
            "error": "Timeout after 1800s",
        })
        return False

    success = process.returncode == 0
    result["steps"].append({
        "step": "execute",
        "success": success,
        "returncode": process.returncode,
        "stdout_tail": stdout[-1000:] if stdout else "",
        "stderr_tail": stderr[-1000:] if stderr else "",
    })
    return True


def _collect_results(
    gem_root: str,
    dataset_id: str,
    region: str,
    delay: int,
    pipeline_mode: Optional[str],
    universe: str,
    field_prefix_summary: Any,
    candidate_field_pool: List[str],
    store: Any,
    prod_first: bool,
    prod_first_top_k: int,
    result: Dict[str, Any],
) -> Dict[str, Any]:
    """Step 6-7.5：产物检查 + source 标注 + 质量预估 + prod-first 预筛 + 落库。

    2026-09-25 从 run() 内联体拆出，行为逐字保留。始终返回 result。
    """
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

        # Step 7.5: prod-first 预筛（2026-09-24 P0 强度优先）
        # 对候选按字段族分组，每组最强 top_k 条先跑 prod；prod≥0.7 的族整族标 dropped。
        # 当前是回测后才发现 prod 撞墙（EUR/ASI 库存 47/47、19/19 全 ≥0.70），
        # 把 prod 检查从 S4 评审前置到 S2 生成后，可省 80% 回测配额。
        if prod_first and store and result.get("success") and result.get("expression_count", 0) > 0:
            try:
                prod_first_result = _run_prod_first_prescreen(
                    region=region,
                    dataset_id=dataset_id,
                    expressions=expressions,
                    store=store,
                    top_k=prod_first_top_k,
                    universe=universe,
                    delay=delay,
                )
                result["steps"].append(prod_first_result)
                result["prod_first"] = prod_first_result
                if prod_first_result.get("blocked_families", 0) > 0:
                    result["mode_b_required"] = True
                    result["mode_b_reason"] = (
                        f"{prod_first_result['blocked_families']} field families prod≥0.7 blocked"
                    )
            except Exception as _pf_err:
                logger.warning(f"prod-first prescreen failed: {_pf_err}")
                result["steps"].append({
                    "step": "prod_first_prescreen",
                    "success": False,
                    "error": str(_pf_err),
                })

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
    return result


def _run_prod_first_prescreen(
    region: str,
    dataset_id: str,
    expressions: List[Dict],
    store: Any,
    top_k: int = 2,
    universe: str = "TOP3000",
    delay: int = 1,
) -> Dict[str, Any]:
    """字段族级 prod 预筛（2026-09-24 P0 强度优先）.

    对候选按字段族分组（用 _lib.common.expr_fields 提取字段集合），
    每组最强 top_k 条先跑 check_correlation(production)；prod≥0.7 的族整族标 dropped。
    当前是回测后才发现 prod 撞墙（EUR/ASI 库存 47/47、19/19 全 ≥0.70），
    把 prod 检查从 S4 评审前置到 S2 生成后，可省 80% 回测配额。
    """
    result = {
        "step": "prod_first_prescreen",
        "success": True,
        "top_k": top_k,
        "families_checked": 0,
        "families_blocked": 0,
        "families_clean": 0,
        "blocked_families": 0,
        "clean_families": 0,
        "details": [],
    }
    try:
        from _lib.common import expr_fields as _expr_fields
        from _lib.common import load_platform_constraints as _lpc
    except Exception as _imp_err:
        result["success"] = False
        result["error"] = f"import _lib.common failed: {_imp_err}"
        return result

    known_ops = set(_lpc().get("known_ops", []))
    # 表达式文本 -> 本波 DB id：dropped 必须按 id 过滤（set_expression_status 契约：
    # ids/from_status 至少给一个，无过滤全波改状态直接拒绝），且只精确命中本族。
    wave_label = f"s2_{dataset_id}_d{delay}"
    expr_id_map: Dict[str, int] = {}
    try:
        _rows = store.connection.execute(
            "SELECT id, expression FROM expressions WHERE region=? AND wave=?",
            (region, wave_label),
        ).fetchall()
        for _r in _rows:
            expr_id_map[str(_r[1])] = int(_r[0])
    except Exception as _id_err:
        logger.warning(f"prod-first id lookup unavailable: {_id_err}")
    # 按字段族分组
    fam_map = {}
    for item in expressions:
        expr = item if isinstance(item, str) else (item.get("expression") or item.get("expr") or "")
        if not expr:
            continue
        fields = frozenset(_expr_fields(expr, known_ops))
        fam_map.setdefault(fields, []).append(expr)

    if not fam_map:
        result["success"] = False
        result["error"] = "no expressions with extractable fields"
        return result

    # 对每族最强 top_k 条跑 prod（用 brain_client 的 check_correlation）
    try:
        import asyncio
        from brain_api import brain_client
    except Exception as _brain_err:
        result["success"] = False
        result["error"] = f"import brain_api failed: {_brain_err}"
        return result

    async def _check_family(fields, exprs):
        # 取最强 top_k 条（按表达式长度降序，近似复杂度/强度）
        reps = sorted(exprs, key=lambda e: -len(e))[:top_k]
        max_prod = 0.0
        for expr in reps:
            try:
                # 先 simulate 得到 alpha_id，再 check_correlation
                sim = await brain_client.create_simulation({
                    "type": "REGULAR",
                    "settings": {
                        "instrumentType": "EQUITY",
                        "region": region,
                        # 2026-09-25 修复：预筛必须用本波真实 universe/delay——
                        # 硬编码 TOP3000/d1 时 GBR（TOP700）预筛跑在错误宇宙，
                        # prod 相关性对生产池的代表性失效。
                        "universe": universe,
                        "delay": delay,
                        "decay": 4,
                        "neutralization": "SUBINDUSTRY",
                        "truncation": 0.08,
                        "pasteurization": "ON",
                        "unitHandling": "VERIFY",
                        "nanHandling": "ON",
                        "language": "FASTEXPR",
                        "visualization": False,
                    },
                    "regular": expr,
                })
                alpha_id = sim.get("alpha")
                if not alpha_id:
                    continue
                pc = await brain_client.check_correlation(alpha_id, correlation_type="production", threshold=0.7)
                prod = ((pc.get("checks") or {}).get("production") or {}).get("max_correlation")
                if isinstance(prod, (int, float)):
                    max_prod = max(max_prod, prod)
            except Exception:
                continue
        return max_prod

    # 串行预筛（prod 队列单并发，避免 429）
    blocked_families = []
    clean_families = []
    for fields, exprs in fam_map.items():
        try:
            max_prod = asyncio.run(_check_family(fields, exprs))
            result["families_checked"] += 1
            if max_prod >= 0.7:
                result["families_blocked"] += 1
                result["blocked_families"] += 1
                blocked_families.append({
                    "fields": sorted(fields),
                    "n_exprs": len(exprs),
                    "max_prod": max_prod,
                })
                # 整族标 dropped（按 id 精确过滤本族，仅未回测行可改）
                fam_ids = [expr_id_map[e] for e in exprs if e in expr_id_map]
                if fam_ids:
                    try:
                        store.set_expression_status(
                            region=region,
                            wave=wave_label,
                            to_status="dropped",
                            ids=fam_ids,
                            from_status="gem",
                            reason=f"prod-first prescreen: family prod={max_prod:.3f}≥0.7 blocked",
                        )
                    except Exception as _drop_err:
                        logger.warning(f"prod-first drop family failed: {_drop_err}")
                else:
                    logger.warning(
                        f"prod-first: family blocked but no DB ids matched (wave={wave_label})，跳过 drop"
                    )
            else:
                result["families_clean"] += 1
                result["clean_families"] += 1
                clean_families.append({
                    "fields": sorted(fields),
                    "n_exprs": len(exprs),
                    "max_prod": max_prod,
                })
        except Exception as _fam_err:
            logger.warning(f"prod-first family check failed: {_fam_err}")
            continue

    result["details"] = {
        "blocked": blocked_families[:10],  # 只留前 10 个示例
        "clean": clean_families[:10],
    }
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
        conn = db_connect(resolve_db_path())
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
    """查找 final_expressions.json 路径（三段优先级）。

    2026-09-25 结构优化目标 A：GEM 数据产物迁出 skill 安装位到仓库稳定路径
    data/gem_runs/（resolve_gem_data_dir，与 _skill_roots 解耦）。新跑的任务走 1；
    历史产物（已在旧深嵌套位置）走 2/3 仍可读——旧路径兜底必须保留：改动部署时
    在飞的 detached GEM 任务带着旧 env 会写旧位置。
    """
    # 1) 新稳定路径（仓库 data/gem_runs，与 skill 安装位解耦）
    try:
        new_path = resolve_gem_data_dir(dataset_id, region, delay) / "final_expressions.json"
        if new_path.exists():
            return str(new_path)
    except Exception:
        pass

    # 2) 旧标准路径（历史产物兜底）
    path = os.path.join(
        gem_root,
        "scripts", "trailSomeAlphas", "skills", "brain-feature-implementation",
        "data", f"{dataset_id}_{region}_delay{delay}",
        "final_expressions.json"
    )
    if os.path.exists(path):
        return path

    # 3) 旧备用路径（历史产物兜底）
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
