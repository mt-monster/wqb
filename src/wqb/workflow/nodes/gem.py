# -*- coding: utf-8 -*-
"""gem 节点：GEM 表达式生成.

替代 brain-makeSomeGem 的 headless_runner PowerShell 命令模板。
"""

import json
import logging
import os
import subprocess
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..mcp_check import require_mcp_tools
from .._common import infer_data_category, resolve_skill_dir, wq_py

logger = logging.getLogger(__name__)


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
    detached: bool = True,
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
        priors_file: priors.json 路径
        detached: 是否后台执行
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

    # Step 1: 检查 S1 ledger（自动注入 ideas-file）
    s1_ledger = None
    if store:
        try:
            s1_key = f"s1_{dataset_id}_d{delay}"
            s1_ledger = store.get_ledger(region, s1_key)
            if s1_ledger and s1_ledger.get("ideas_md_path"):
                result["steps"].append({
                    "step": "s1_ledger_check",
                    "success": True,
                    "s1_key": s1_key,
                    "ideas_md_path": s1_ledger["ideas_md_path"],
                    "auto_inject": True,
                })
        except Exception as e:
            logger.warning(f"Failed to check S1 ledger: {e}")

    # Step 2: 定位 GEM runner
    gem_root = resolve_skill_dir("brain-makeSomeGem")
    if not gem_root:
        result["steps"].append({
            "step": "find_gem_root",
            "success": False,
            "error": "brain-makeSomeGem skill not found",
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
    cmd = [
        wq_py(),
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

    if detached:
        cmd.append("--detached")

    result["steps"].append({
        "step": "build_command",
        "success": True,
        "command": " ".join(cmd),
    })

    # Step 5: 执行
    try:
        logger.info(f"Executing GEM: {' '.join(cmd)}")

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.path.dirname(runner_script),
        )

        # 等待完成（带超时）
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

            # Step 7: 质量预估（特征工程 SOP 阶段5，强制）
            quality_result = _run_quality_estimation(
                region=region,
                dataset_id=dataset_id,
                final_expr_path=final_expr_path,
                expressions=expressions,
                store=store,
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


def _infer_category(dataset_id: str) -> str:
    """从 dataset_id 推断数据类别（向后兼容别名，实际逻辑在 _common）。"""
    return infer_data_category(dataset_id)


def _find_gem_root() -> Optional[str]:
    """查找 brain-makeSomeGem skill 根目录（向后兼容别名）。"""
    return resolve_skill_dir("brain-makeSomeGem")


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
        "details": {},
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
