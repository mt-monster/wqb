# -*- coding: utf-8 -*-
"""gem 节点：GEM 表达式生成.

替代 brain-makeSomeGem 的 headless_runner PowerShell 命令模板。
"""

import json
import logging
import os
import re
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
    priors_from_db: bool = True,
    ideas_file: Optional[str] = None,
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
        priors_file: priors.json 路径（显式指定时优先于 DB 快照）
        priors_from_db: 是否从 DB ledger priors_snapshot_<region> 读取 priors
            （默认 True，与 SOP「DB 为单一事实源」对齐；run.py fail-closed：
            无快照即报错，不会静默无 priors 运行。仅当显式传 priors_file 或
            本参数=False 时不走 DB 直读）
        ideas_file: ideas.md 路径（显式指定，覆盖 S1 ledger 自动注入）
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
                if not effective_ideas_file:
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
    elif priors_from_db:
        # 2026-09-04 修复：默认走 DB 快照直读（SOP「DB 为单一事实源」），
        # 修复 wave112 之前 GEM 命令无任何 priors 参数导致知识库模板未注入的断点
        cmd.extend(["--priors-from-db", region])

    if effective_ideas_file:
        cmd.extend(["--ideas-file", effective_ideas_file])

    if detached:
        cmd.append("--detached")

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
            ideas_check["sample"] = chk["sample"]
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

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.path.dirname(runner_script),
        )

        if detached:
            # detached 模式：轮询磁盘上新 task 的 meta.json，不依赖 stdout 文本握手。
            # 2026-09-03 修复：原实现 communicate/readline 抓 stdout 的 task_id= 行，
            # 受 MCP 客户端超时窗口与管道缓冲影响易挂死；run.py spawn 后台 child 后会把
            # task_id/pid/日志路径先写入 <tasks_dir>/<task_id>/meta.json 再退出，磁盘轮询最稳。
            import time
            tasks_dir = os.path.abspath(
                os.path.join(os.path.dirname(runner_script), "..", "outputs", "tasks")
            )
            pre_existing = set(os.listdir(tasks_dir)) if os.path.isdir(tasks_dir) else set()

            task_meta = None
            task_dir = None
            start = time.time()
            deadline = start + 30  # 最多等 30 秒（与 MCP 客户端超时窗口对齐）
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
                time.sleep(0.3)

            process_stdout = ""
            process_stderr = ""
            if not task_meta:
                try:
                    process_stdout, process_stderr = process.communicate(timeout=5)
                except Exception:
                    try:
                        process.kill()
                    except Exception:
                        pass

            if task_meta:
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
            if rc not in (None, 0):
                error = f"detached launcher exited rc={rc} before writing meta.json"
            elif rc is None:
                error = "detached launcher still running but no meta.json within 30s"
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
