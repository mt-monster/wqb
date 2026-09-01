# -*- coding: utf-8 -*-
"""campaign 节点：S1-S6 战役阶段执行.

包装 wq-brain-campaign-toolkit 的各阶段脚本，消除 --campaign-dir 手工传递。
"""

import logging
import os
import subprocess
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
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """执行战役阶段.

    Args:
        region: 区域代码
        stage: 阶段（S0/S1/S2/S3/S4/S5/S6）
        dataset: 数据集 ID（如需要）
        wave: 波次号（如需要）
        subcommand: 子命令（如 ledger/registry/wave）
        extra_args: 额外参数列表
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
        cmd.extend(["--region", region])
    elif stage == "S1":
        if dataset:
            cmd.extend(["--dataset", dataset])
    elif stage == "S2":
        # S2 前强制前置条件预检（S0/S1 产物门禁）
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
        # S3 前强制质量闸（特征工程 SOP 阶段6）
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

    # 添加额外参数
    if extra_args:
        cmd.extend(extra_args)

    result["steps"].append({
        "step": "build_command",
        "success": True,
        "command": " ".join(cmd),
    })

    # 执行
    try:
        logger.info(f"Executing campaign {stage}: {' '.join(cmd)}")

        process_result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3600,
            cwd=toolkit_dir,
        )

        success = process_result.returncode == 0
        result["steps"].append({
            "step": "execute",
            "success": success,
            "returncode": process_result.returncode,
            "stdout_tail": process_result.stdout[-2000:] if process_result.stdout else "",
            "stderr_tail": process_result.stderr[-2000:] if process_result.stderr else "",
        })

        result["success"] = success

        # 保存到 DB
        if store and success:
            try:
                store.upsert_ledger("WORKFLOW", f"campaign_{region}_{stage}_{datetime.now().strftime('%Y%m%d')}", {
                    "executed_at": datetime.now().isoformat(),
                    "region": region,
                    "stage": stage,
                    "dataset": dataset,
                    "wave": wave,
                })
            except Exception as e:
                logger.warning(f"Failed to save campaign record: {e}")

    except subprocess.TimeoutExpired:
        result["steps"].append({
            "step": "execute",
            "success": False,
            "error": "Timeout after 3600s",
        })
    except Exception as e:
        logger.exception(f"Campaign {stage} execution failed")
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
