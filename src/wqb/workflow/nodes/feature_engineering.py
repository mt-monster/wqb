# -*- coding: utf-8 -*-
"""feature_engineering 节点：S1-S3 特征工程流程封装.

封装特征工程 SOP 阶段1-3：字段理解 → 字段筛选 → 预处理决策。
产出写入 ledger_kv s1_<dataset>_d<delay>，供 S2 自动注入。
"""

import logging
import os
import subprocess
from datetime import datetime
from typing import Any, Dict, Optional

from ..mcp_check import require_mcp_tools
from .._common import infer_data_category, resolve_skill_dir, wq_py

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

    # dry-run：构建到特征工程流水线命令即停，不 subprocess、不写库
    # （2026-09-01 缺陷 A 修复：此前 dry_run 仍真实跑 pipeline + build_* persist）。
    if ctx.get("dry_run"):
        result["success"] = True
        result["dry_run"] = True
        result["steps"].append({
            "step": "dry_run",
            "success": True,
            "message": (
                "Would run feature engineering S1-S3: check S1 ledger → resolve "
                "brain-data-feature-engineering → run pipeline → write s1_ledger"
            ),
        })
        result["plan"] = {
            "region": region,
            "dataset_id": dataset_id,
            "delay": delay,
            "universe": universe,
            "data_category": data_category,
            "force_regen": force_regen,
        }
        return result

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

    # Step 3: 运行特征工程流程（阶段1-3）
    try:
        fe_result = _run_feature_engineering_pipeline(
            skill_root=skill_root,
            region=region,
            dataset_id=dataset_id,
            delay=delay,
            universe=universe,
            data_category=data_category,
        )
        result["steps"].append(fe_result)

        if not fe_result.get("success"):
            result["steps"].append({
                "step": "feature_engineering_failed",
                "success": False,
                "error": fe_result.get("error", "Unknown error"),
            })
            return result

        # Step 4: 写入 ledger（强制）
        prefix_summary = None
        candidate_field_pool = []
        if store:
            try:
                prefix_summary = store.build_field_prefix_clusters(
                    region=region,
                    dataset=dataset_id,
                    prefix_depth=1,
                    top_n=10,
                    samples_per_cluster=5,
                    persist=True,
                )
                result["steps"].append({
                    "step": "build_prefix_clusters",
                    "success": True,
                    "s1_prefix_key": f"s1_prefix_{dataset_id}",
                    "total_fields": prefix_summary.get("total_fields"),
                    "total_clusters": prefix_summary.get("total_clusters"),
                })
            except Exception as e:
                logger.warning(f"Failed to build field prefix clusters: {e}")
                result["steps"].append({
                    "step": "build_prefix_clusters",
                    "success": False,
                    "error": str(e),
                })

            try:
                pool_payload = store.build_candidate_field_pool(
                    region=region,
                    dataset=dataset_id,
                    persist=True,
                )
                candidate_field_pool = pool_payload.get("candidate_field_pool", [])
                result["steps"].append({
                    "step": "build_candidate_field_pool",
                    "success": True,
                    "s2_field_pool_key": f"s2_field_pool_{dataset_id}",
                    "pool_size": pool_payload.get("pool_size", 0),
                })
            except Exception as e:
                logger.warning(f"Failed to build candidate field pool: {e}")
                result["steps"].append({
                    "step": "build_candidate_field_pool",
                    "success": False,
                    "error": str(e),
                })

        if store:
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

            try:
                store.upsert_ledger(region, s1_key, ledger_data)
                result["steps"].append({
                    "step": "write_ledger",
                    "success": True,
                    "s1_key": s1_key,
                    "field_whitelist_size": len(ledger_data["field_whitelist"]),
                    "candidate_field_pool_size": len(candidate_field_pool),
                })
            except Exception as e:
                logger.error(f"Failed to write S1 ledger: {e}")
                result["steps"].append({
                    "step": "write_ledger",
                    "success": False,
                    "error": str(e),
                })
                # 不阻止返回，但标记警告
                result["warning"] = f"Ledger write failed: {e}"

        result["success"] = True
        result["ideas_md_path"] = fe_result.get("ideas_md_path")
        result["field_whitelist"] = candidate_field_pool or fe_result.get("field_whitelist", [])
        result["candidate_field_pool"] = candidate_field_pool
        result["preprocessing"] = fe_result.get("preprocessing", {})
        result["field_prefix_summary"] = prefix_summary or {}

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


def _run_feature_engineering_pipeline(
    skill_root: str,
    region: str,
    dataset_id: str,
    delay: int,
    universe: str,
    data_category: str,
) -> Dict[str, Any]:
    """运行特征工程流水线（阶段1-3）.

    调用 brain-data-feature-engineering 的脚本生成 ideas 和字段白名单。
    """
    result = {
        "step": "feature_engineering_pipeline",
        "success": False,
        "ideas_md_path": None,
        "field_whitelist": [],
        "preprocessing": {},
    }

    # 查找主脚本
    main_script = os.path.join(skill_root, "scripts", "feature_engineering.py")
    if not os.path.exists(main_script):
        # 备用路径
        main_script = os.path.join(skill_root, "feature_engineering.py")

    if not os.path.exists(main_script):
        result["error"] = f"Main script not found in {skill_root}"
        return result

    # 构建输出目录
    output_dir = os.path.join(skill_root, "output_report")
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

    try:
        logger.info(f"Running feature engineering: {' '.join(cmd)}")

        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=1800,  # 30 分钟
            cwd=skill_root,
        )

        result["stdout_tail"] = proc.stdout[-2000:] if proc.stdout else ""
        result["stderr_tail"] = proc.stderr[-2000:] if proc.stderr else ""

        if proc.returncode != 0:
            result["error"] = f"Script failed with returncode {proc.returncode}"
            return result

        # 检查产物
        if not os.path.exists(ideas_path):
            result["error"] = f"Ideas file not generated: {ideas_path}"
            return result

        result["success"] = True
        result["ideas_md_path"] = ideas_path

        # 尝试解析 ideas 文件提取字段白名单和预处理决策
        try:
            with open(ideas_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 简单解析：提取代码块中的字段名
            import re
            fields = re.findall(r'\b([a-z][a-z0-9_]*(?:_[a-z0-9]+)+)\b', content)
            # 过滤常见非字段词
            stopwords = {"self", "true", "false", "none", "null", "return", "import", "from", "def", "class"}
            result["field_whitelist"] = list(set(f for f in fields if f not in stopwords and len(f) > 3))[:50]

            # 预处理决策从内容中提取（简化版）
            preprocessing = {}
            if "ts_backfill" in content:
                preprocessing["ts_backfill"] = "sparse fields"
            if "group_zscore" in content or "group_rank" in content:
                preprocessing["group_neutralize"] = "cross-sectional"
            if "vec_" in content:
                preprocessing["vector_wrap"] = "VECTOR fields"

            result["preprocessing"] = preprocessing

        except Exception as e:
            logger.warning(f"Failed to parse ideas file: {e}")

    except subprocess.TimeoutExpired:
        result["error"] = "Timeout after 1800s"
    except Exception as e:
        result["error"] = str(e)

    return result
