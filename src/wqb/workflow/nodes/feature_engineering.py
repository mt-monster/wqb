# -*- coding: utf-8 -*-
"""feature_engineering 节点：S1-S3 特征工程流程封装.

封装特征工程 SOP 阶段1-3：字段理解 → 字段筛选 → 预处理决策。
产出写入 ledger_kv s1_<dataset>_d<delay>，供 S2 自动注入。

2026-09-03 根治：subprocess.run → Popen 异步化，避免 MCP 客户端超时。
"""

import json
import logging
import os
import subprocess
import threading
from datetime import datetime
from typing import Any, Dict, Optional

from ..mcp_check import require_mcp_tools
from .._common import REPO_ROOT, infer_data_category, resolve_skill_dir, wq_py

logger = logging.getLogger(__name__)


@require_mcp_tools("feature_engineering")
def run(
    region: str,
    dataset_id: str,
    delay: int,
    universe: str,
    data_category: Optional[str] = None,
    force_regen: bool = False,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """执行特征工程 S1-S3 流程.

    Args:
        region: 区域代码
        dataset_id: 数据集 ID
        delay: 延迟（0 或 1）
        universe: 宇宙（如 TOP3000）
        data_category: 数据类别（如 analyst）
        force_regen: 是否强制重新生成（忽略已有 ledger）
        _context: 执行上下文

    Returns:
        执行结果字典，含 s1_ledger_key 和 ideas_md_path
    """
    ctx = _context or {}
    store = ctx.get("store")

    if not data_category:
        data_category = infer_data_category(dataset_id)

    s1_key = f"s1_{dataset_id}_d{delay}"

    result = {
        "region": region,
        "dataset_id": dataset_id,
        "delay": delay,
        "universe": universe,
        "data_category": data_category,
        "s1_key": s1_key,
        "steps": [],
        "success": False,
    }

    # dry-run 统一口径（2026-09-05）：走完所有零成本前置——S1 ledger 检查、
    # skill 目录与主脚本解析、命令构建——到 Popen 前即停，不建目录、不写库。
    # 此前只返回一句写死的 "Would run feature engineering ..."，等于什么都没验证。
    dry_run = bool(ctx.get("dry_run"))
    result["dry_run"] = dry_run

    # Step 1: 检查是否已有 S1 ledger（且不强制重新生成）
    if store and not force_regen:
        try:
            existing = store.get_ledger(region, s1_key)
            if existing and existing.get("ideas_md_path"):
                result["steps"].append({
                    "step": "check_existing",
                    "success": True,
                    "message": "S1 ledger exists, skipping regeneration",
                    "s1_key": s1_key,
                    "ideas_md_path": existing["ideas_md_path"],
                })
                result["success"] = True
                result["ideas_md_path"] = existing["ideas_md_path"]
                result["field_whitelist"] = existing.get("field_whitelist", [])
                result["preprocessing"] = existing.get("preprocessing", {})
                result["skipped"] = True
                return result
        except Exception as e:
            logger.warning(f"Failed to check existing S1 ledger: {e}")

    # Step 2: 定位 brain-data-feature-engineering skill
    skill_root = resolve_skill_dir("brain-data-feature-engineering")
    if not skill_root:
        result["steps"].append({
            "step": "find_skill",
            "success": False,
            "error": "brain-data-feature-engineering skill not found",
        })
        return result

    result["steps"].append({
        "step": "find_skill",
        "success": True,
        "skill_root": skill_root,
    })

    # Step 3: 运行特征工程流程（阶段1-3）— 异步模式
    task_id = f"fe_{region}_{dataset_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    # 2026-09-04 修复：任务目录支持 WQB_TASK_ROOT 注入（单测隔离，默认仓库 logs/_async_tasks）
    task_dir = os.environ.get("WQB_TASK_ROOT") or os.path.join(REPO_ROOT, "logs", "_async_tasks")
    if not dry_run:
        os.makedirs(task_dir, exist_ok=True)
    task_file = os.path.join(task_dir, f"{task_id}.json")

    try:
        fe_async_result = _run_feature_engineering_pipeline_async(
            skill_root=skill_root,
            region=region,
            dataset_id=dataset_id,
            delay=delay,
            universe=universe,
            data_category=data_category,
            task_id=task_id,
            task_file=task_file,
            store=store,
            s1_key=s1_key,
            result=result,
            dry_run=dry_run,
        )
        result["steps"].append(fe_async_result)

        if not fe_async_result.get("success"):
            result["steps"].append({
                "step": "feature_engineering_failed",
                "success": False,
                "error": fe_async_result.get("error", "Unknown error"),
            })
            return result

        if dry_run:
            result["success"] = True
            result["note"] = "dry-run：命令已构建，未执行"
            result["command"] = fe_async_result.get("command")
            result["plan"] = {
                "region": region,
                "dataset_id": dataset_id,
                "delay": delay,
                "universe": universe,
                "data_category": data_category,
                "force_regen": force_regen,
                "skill_root": skill_root,
                "s1_key": s1_key,
            }
            return result

        # 异步模式：立即返回，结果通过 task_file 轮询
        result["success"] = True
        result["async"] = True
        result["task_id"] = task_id
        result["task_file"] = task_file
        result["pid"] = fe_async_result.get("pid")
        result["message"] = f"Feature engineering launched in background. Poll {task_file} for result."

    except Exception as e:
        logger.exception("Feature engineering pipeline failed")
        result["steps"].append({
            "step": "feature_engineering_pipeline",
            "success": False,
            "error": str(e),
        })

    return result


def _infer_category(dataset_id: str) -> str:
    """从 dataset_id 推断数据类别（向后兼容别名）。"""
    return infer_data_category(dataset_id)


def _find_feature_engineering_skill() -> Optional[str]:
    """查找 brain-data-feature-engineering skill 根目录（向后兼容别名）。"""
    return resolve_skill_dir("brain-data-feature-engineering")


def _run_feature_engineering_pipeline_async(
    skill_root: str,
    region: str,
    dataset_id: str,
    delay: int,
    universe: str,
    data_category: str,
    task_id: str,
    task_file: str,
    store: Any,
    s1_key: str,
    result: Dict[str, Any],
    dry_run: bool = False,
) -> Dict[str, Any]:
    """运行特征工程流水线（阶段1-3）— 异步模式.

    Popen 启动子进程后立即返回，后台线程等待完成并写入结果文件。
    """
    step_result = {
        "step": "feature_engineering_pipeline",
        "success": False,
        "async": True,
        "task_id": task_id,
        "task_file": task_file,
    }

    # 查找主脚本
    main_script = os.path.join(skill_root, "scripts", "feature_engineering.py")
    if not os.path.exists(main_script):
        main_script = os.path.join(skill_root, "feature_engineering.py")

    if not os.path.exists(main_script):
        step_result["error"] = f"Main script not found in {skill_root}"
        return step_result

    # 构建输出目录（dry-run 不建目录）
    output_dir = os.path.join(skill_root, "output_report")
    if not dry_run:
        os.makedirs(output_dir, exist_ok=True)

    ideas_filename = f"{region}_delay{delay}_{dataset_id}_ideas.md"
    ideas_path = os.path.join(output_dir, ideas_filename)

    # 构建命令
    cmd = [
        wq_py(), main_script,
        "--region", region,
        "--dataset", dataset_id,
        "--delay", str(delay),
        "--universe", universe,
        "--category", data_category,
        "--output", ideas_path,
    ]

    step_result["command"] = " ".join(cmd)
    step_result["main_script"] = main_script
    if dry_run:
        step_result["success"] = True
        step_result["dry_run"] = True
        step_result["note"] = "dry-run：命令已构建，未执行"
        return step_result

    try:
        logger.info(f"Running feature engineering (async): {' '.join(cmd)}")

        popen_kwargs: Dict[str, Any] = {
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "text": True,
            "cwd": skill_root,
        }
        if os.name == "nt":
            # 2026-09-04 修复：脱离父进程组——MCP 服务进程退出不带走后台子进程
            popen_kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
        proc = subprocess.Popen(cmd, **popen_kwargs)

        step_result["pid"] = proc.pid
        step_result["success"] = True
        step_result["message"] = f"Feature engineering launched (pid={proc.pid})"

        # 2026-09-04 修复：主线程先写 running 占位——即使收尾线程随 MCP 进程退出被杀，
        # 轮询方也能读到 status=running 而非"任务文件不存在"（收尾线程完成时覆盖终态）。
        try:
            with open(task_file, "w", encoding="utf-8") as f:
                json.dump({
                    "task_id": task_id,
                    "status": "running",
                    "pid": proc.pid,
                    "started_at": datetime.now().isoformat(),
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.warning(f"Failed to write running placeholder {task_file}: {e}")

        # 后台线程：等待完成并收集结果
        def _wait_and_collect():
            fe_result = {
                "task_id": task_id,
                "success": False,
                "ideas_md_path": None,
                "field_whitelist": [],
                "preprocessing": {},
            }
            try:
                stdout, stderr = proc.communicate(timeout=1800)
                fe_result["stdout_tail"] = stdout[-2000:] if stdout else ""
                fe_result["stderr_tail"] = stderr[-2000:] if stderr else ""
                fe_result["returncode"] = proc.returncode

                if proc.returncode != 0:
                    fe_result["error"] = f"Script failed with returncode {proc.returncode}"
                elif not os.path.exists(ideas_path):
                    fe_result["error"] = f"Ideas file not generated: {ideas_path}"
                else:
                    fe_result["success"] = True
                    fe_result["ideas_md_path"] = ideas_path

                    # 解析 ideas 文件提取字段白名单和预处理决策
                    try:
                        with open(ideas_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        import re
                        fields = re.findall(r'\b([a-z][a-z0-9_]*(?:_[a-z0-9]+)+)\b', content)
                        stopwords = {"self", "true", "false", "none", "null", "return", "import", "from", "def", "class"}
                        fe_result["field_whitelist"] = list(set(f for f in fields if f not in stopwords and len(f) > 3))[:50]

                        preprocessing = {}
                        if "ts_backfill" in content:
                            preprocessing["ts_backfill"] = "sparse fields"
                        if "group_zscore" in content or "group_rank" in content:
                            preprocessing["group_neutralize"] = "cross-sectional"
                        if "vec_" in content:
                            preprocessing["vector_wrap"] = "VECTOR fields"
                        fe_result["preprocessing"] = preprocessing
                    except Exception as e:
                        logger.warning(f"Failed to parse ideas file: {e}")

            except subprocess.TimeoutExpired:
                # 2026-09-04 修复：超时后 kill 子进程并回收——否则孤儿进程继续占平台槽位
                try:
                    proc.kill()
                    proc.communicate(timeout=30)
                except Exception:
                    pass
                fe_result["error"] = "Timeout after 1800s (process killed)"
            except Exception as e:
                fe_result["error"] = str(e)

            fe_result["finished_at"] = datetime.now().isoformat()

            # 2026-09-04 修复：收尾线程重建独立 sqlite 连接（复用主线程连接跨线程使用
            # 会抛 sqlite3.ProgrammingError，fe ledger_error 实证）。闭包内用原参数名
            # 重赋值会把 store 解析为局部变量并 UnboundLocalError，故用 thread_store。
            thread_store = None
            if store is not None and hasattr(store, "path"):
                try:
                    thread_store = store.__class__(store.path)
                except Exception as e:
                    logger.warning(f"Failed to reopen store in collector thread: {e}")

            # 写入 ledger（在后台线程中完成）
            if thread_store and fe_result.get("success"):
                try:
                    prefix_summary = None
                    candidate_field_pool = []
                    try:
                        prefix_summary = thread_store.build_field_prefix_clusters(
                            region=region, dataset=dataset_id,
                            prefix_depth=1, top_n=10, samples_per_cluster=5, persist=True,
                        )
                    except Exception as e:
                        logger.warning(f"Failed to build field prefix clusters: {e}")

                    try:
                        pool_payload = thread_store.build_candidate_field_pool(
                            region=region, dataset=dataset_id, persist=True,
                        )
                        candidate_field_pool = pool_payload.get("candidate_field_pool", [])
                    except Exception as e:
                        logger.warning(f"Failed to build candidate field pool: {e}")

                    ledger_data = {
                        "generated_at": datetime.now().isoformat(),
                        "region": region,
                        "dataset_id": dataset_id,
                        "delay": delay,
                        "universe": universe,
                        "data_category": data_category,
                        "ideas_md_path": fe_result.get("ideas_md_path"),
                        "field_whitelist": candidate_field_pool or fe_result.get("field_whitelist", []),
                        "candidate_field_pool": candidate_field_pool,
                        "preprocessing": fe_result.get("preprocessing", {}),
                        "field_prefix_summary": prefix_summary or {},
                        "source": "feature_engineering_node",
                    }
                    thread_store.upsert_ledger(region, s1_key, ledger_data)
                    fe_result["ledger_written"] = True
                    fe_result["field_whitelist_size"] = len(ledger_data["field_whitelist"])
                    fe_result["candidate_field_pool_size"] = len(candidate_field_pool)
                except Exception as e:
                    logger.error(f"Failed to write S1 ledger: {e}")
                    fe_result["ledger_error"] = str(e)

            # 写入结果文件
            try:
                with open(task_file, "w", encoding="utf-8") as f:
                    json.dump(fe_result, f, indent=2, ensure_ascii=False)
            except Exception as e:
                logger.error(f"Failed to write task result {task_file}: {e}")

        bg_thread = threading.Thread(target=_wait_and_collect, daemon=True)
        bg_thread.start()

    except Exception as e:
        step_result["error"] = str(e)

    return step_result
