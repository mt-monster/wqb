# -*- coding: utf-8 -*-
"""campaign 节点：S1-S6 战役阶段执行.

包装 wq-brain-campaign-toolkit 的各阶段脚本，消除 --campaign-dir 手工传递。

2026-09-03 根治：subprocess.run → Popen 异步化，避免 MCP 客户端超时。
子进程在后台运行，结果写入临时 JSON，调用方通过 task_file 轮询。
"""

import json
import logging
import os
import subprocess
import threading
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..mcp_check import require_mcp_tools
from .._common import REPO_ROOT, resolve_campaign_dir, resolve_toolkit_dir, resolve_tools_dir, wq_py

logger = logging.getLogger(__name__)


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
    if not campaign_dir or not os.path.exists(campaign_dir):
        result["steps"].append({
            "step": "validate_campaign_dir",
            "success": False,
            "error": f"Campaign directory not found: {campaign_dir}",
        })
        return result

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
        result["steps"].append({
            "step": "find_toolkit",
            "success": False,
            "error": "wq-brain-campaign-toolkit not found",
        })
        return result

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
        result["steps"].append({
            "step": "route_stage",
            "success": False,
            "error": f"Unknown stage: {stage}",
        })
        return result

    script_path = os.path.join(toolkit_dir, script_name)
    if not os.path.exists(script_path):
        result["steps"].append({
            "step": "route_stage",
            "success": False,
            "error": f"Script not found: {script_path}",
        })
        return result

    # 构建命令
    cmd = [wq_py(), script_path, "--campaign-dir", campaign_dir]

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
                result["steps"].append({
                    "step": "preflight_block",
                    "success": False,
                    "error": preflight_result.get("error", "Preflight failed"),
                    "preflight": preflight_result,
                })
                return result

        if dataset:
            cmd.extend(["--dataset", dataset])
        if wave:
            cmd.extend(["--wave", wave])
        cmd.append("--from-db")
    elif stage == "S3":
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
                result["steps"].append({
                    "step": "quality_gate_block",
                    "success": False,
                    "error": "Quality gate failed, blocking S3 execution",
                    "quality_gate": quality_gate_result,
                })
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
        if subcommand:
            cmd.append(subcommand)
        if wave:
            cmd.extend(["--wave", wave])

    # subcommand 路由：assemble-priors / diversity-extract（走 campaign.py 子命令）
    if subcommand in ("assemble-priors", "diversity-extract"):
        cmd.append(subcommand)
        if dataset:
            cmd.extend(["--dataset", dataset])
        if wave:
            cmd.extend(["--wave", wave])

    # 添加额外参数
    if extra_args:
        cmd.extend(extra_args)

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
    task_dir = os.path.join(REPO_ROOT, "logs", "_async_tasks")
    os.makedirs(task_dir, exist_ok=True)
    task_file = os.path.join(task_dir, f"{task_id}.json")

    try:
        logger.info(f"Executing campaign {stage} (async): {' '.join(cmd)}")

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=toolkit_dir,
        )

        # 后台线程：等待进程完成并收集结果
        def _wait_and_collect():
            try:
                stdout, stderr = process.communicate(timeout=3600)
                success = process.returncode == 0
                exec_result = {
                    "task_id": task_id,
                    "success": success,
                    "returncode": process.returncode,
                    "stdout_tail": stdout[-2000:] if stdout else "",
                    "stderr_tail": stderr[-2000:] if stderr else "",
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
                exec_result = {
                    "task_id": task_id,
                    "success": False,
                    "error": "Timeout after 3600s",
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

            # 保存到 DB
            if store and exec_result.get("success"):
                try:
                    store.upsert_ledger("WORKFLOW", f"campaign_{region}_{stage}_{datetime.now().strftime('%Y%m%d')}", {
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
            if store and exec_result.get("success"):
                try:
                    if stage == "S0" and calibrate:
                        store.upsert_ledger(region, f"s0_calibrate_{region}", {
                            "calibrated_at": datetime.now().isoformat(),
                            "region": region,
                            "stdout_tail": exec_result.get("stdout_tail", ""),
                        })
                    elif subcommand == "assemble-priors":
                        store.upsert_ledger(region, f"priors_snapshot_{region}", {
                            "assembled_at": datetime.now().isoformat(),
                            "region": region,
                            "stdout_tail": exec_result.get("stdout_tail", ""),
                        })
                except Exception as e:
                    logger.warning(f"Failed to cache result: {e}")

            # S4 walls 诊断入库
            if store and exec_result.get("success") and stage == "S4":
                try:
                    walls_summary = exec_result.get("walls")
                    if walls_summary:
                        store.upsert_ledger(region, f"s4_walls_{region}_{wave or 'unknown'}", {
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
            "message": f"Campaign {stage} launched in background (pid={process.pid}). Poll {task_file} for result.",
        })
        result["success"] = True
        result["async"] = True
        result["task_id"] = task_id
        result["task_file"] = task_file
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
