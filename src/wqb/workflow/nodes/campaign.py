# -*- coding: utf-8 -*-
"""campaign 节点：S1-S6 战役阶段执行.

包装 wq-brain-campaign-toolkit 的各阶段脚本，消除 --campaign-dir 手工传递。

2026-09-03 根治：subprocess.run → Popen 异步化，避免 MCP 客户端超时。
子进程在后台运行，结果写入临时 JSON，调用方通过 task_file 轮询。
"""

import json
import logging
import os
import re
import sqlite3
import subprocess
import threading
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from ..mcp_check import require_mcp_tools
from .._common import (
    REPO_ROOT,
    connect_db_readonly,
    resolve_async_tasks_root,
    resolve_campaign_dir,
    resolve_db_path,
    resolve_toolkit_dir,
    resolve_toolkit_file,
    resolve_tools_dir,
    unbuffered_env,
    validate_argv,
    wq_py,
)

from wqb.db_conn import connect as db_connect  # 规范工厂（2026-09-20 L1 收口）
from wqb.semantic_ledger import ledger_has_l35, parse_ledger  # L3.5 判定唯一口径（与 tools/field_semantic_classify.py 同源）
# ── 开波闸簇已抽至 ./_campaign_open_gates（2026-10-02 拆分，接口不变）──
# 此处 re-export：run_open_wave_gates / _normalize_verdict / _run_*_gate / STOP|BACKLOG_*_DEFAULTS
# 等仍可从 `wqb.workflow.nodes.campaign` 导入，batch_track / registry / 测试的既有 import 不受影响。
from ._campaign_open_gates import (  # noqa: F401
    BACKLOG_GATE_DEFAULTS,
    STOP_RULES_DEFAULTS,
    _axis_wave_metadata,
    _dead_end_productive,
    _evaluate_stop_rules_axis,
    _normalize_verdict,
    _parse_dt_loose,
    _recent_closed_waves,
    _run_backlog_gate,
    _run_signal_floor_gate,
    _run_stop_rules_gate,
    _stop_rules_schema_supports_axis,
    _wall_routing_hint,
    _waiver_from_result,
    run_open_wave_gates,
)

#: 走 campaign.py 子命令路由的 subcommand——**subcommand 优先于 stage**（见 run() 内
#: `if subcommand and subcommand in subcommand_script_map`）。因此传什么 stage 都能路由到
#: campaign.py，stage 只决定超时预算。约定：assemble-priors 属 S2（priors 是 S2 上游产物）、
#: diversity-extract 属 S2、ledger/registry/wave 属 S6；不要因 stage 分支再 append 一次。
_SUBCOMMAND_ROUTED = ("assemble-priors", "diversity-extract", "dataset-experience")

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

    # 阶段必填参数校验（2026-09-15 审计缺陷 B）：registry 层 required_params 只有
    # region/stage，dataset 是 optional —— S1 缺 dataset 会构建出无对象的
    # scan_fields 命令，dry-run 放行、实跑静默空转。此处按 stage 细化：
    # S1 必须有 dataset（扫描对象）；S2 的 dataset 合法可选（build_wave 可从库
    # 跨集重取，无 dataset 时 preflight 走 warning-skip，既有契约）；
    # S4 的 wave 必填在下方 S4 分支已有显式检查。subcommand 路由
    # （assemble-priors 等）不依赖 dataset/wave，不受此校验约束。
    if subcommand not in _SUBCOMMAND_ROUTED:
        _stage_required = {"S1": ("dataset",)}
        _missing = [p for p in _stage_required.get(stage, ()) if not locals().get(p)]
        if _missing:
            return _fail_step(
                result,
                "validate_stage_params",
                f"stage={stage} 缺少必填参数: {', '.join(_missing)}。"
                f"（S1=字段扫描需 dataset；S2 的 dataset 可选——build_wave 可从库重取）",
            )

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
        "dataset-experience": "campaign.py",
    }

    # ── 缓存检查：calibrate / assemble-priors 结果缓存到 ledger（Dry-Run 2.0 优化） ──
    if store and not ctx.get("dry_run"):
        cache_key = None
        if stage == "S0" and calibrate:
            cache_key = f"s0_calibrate_{region}"
        elif subcommand == "assemble-priors":
            # 2026-09-17 P2-12：本键原为 `priors_snapshot_{region}`，与
            # `assemble_priors.py` 落的**真实 payload** 键 `priors_snapshot_<region.lower()>`
            # 仅大小写之差 → 同名不同物（本处是 cache marker，payload 在另一键），
            # 查询 `priors_snapshot_<REGION>` 会拿到不含 wins/dead_ends 的缓存标记。
            # 改为独立命名，与 `s0_calibrate_*` 同族，彻底消除大小写撞键。
            cache_key = f"assemble_priors_cache_{region}"

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
                    # T2 事件（2026-09-30 方案 B）：缓存复用是客观事实，旁路记账供
                    # step_eval 的 cache_reuse_rate 消费；safe 包装不阻塞主流程。
                    from wqb.step_events import safe_record_event
                    safe_record_event(
                        region, "S0" if stage == "S0" else "S2", "cache_hit",
                        wave=str(wave) if wave else None, value=1.0,
                        source="campaign.py::run(cache)",
                        metadata={"cache_key": cache_key},
                    )
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
        # 2026-09-28（P1-3 开区硬前置入节点）：体检包缺失清单——白名单数据集缺
        # field_inspect 包时，步 5 体检硬门"未生效"（预处理约束裸奔到仿真，历史三连复发）。
        # 零成本只读，dry-run 也输出；不阻断 S0 打分，但把清单摆在开波前。
        result["steps"].append(_field_inspect_pack_check(region, campaign_dir))
    elif stage == "S1":
        if dataset:
            cmd.extend(["--dataset", dataset])
        # 2026-10-01（步3 断流修复 · 通气 B）：S1 = typed catalog + 语义归类。
        # 语义台账 `s1_semantic_<ds>` 是步 5 闸 SEM 的 fail-closed 输入，也是生成侧
        # 字段池的非信号过滤源；此前它靠人工记忆单跑，全库覆盖率仅 4.7%（EUR/IND/GLB/JPN=0）。
        # 此处把它接成 S1 的默认附属动作（本地零配额秒级，缺台账才跑）。只报告不阻断。
        if not ctx.get("dry_run"):
            result["steps"].append(_semantic_coverage_check(region, dataset))
        else:
            result["steps"].append({
                "step": "semantic_coverage_check", "success": True, "dry_run": True,
                "plan": f"缺 s1_semantic_{dataset} 时自动补做（python tools/field_semantic_classify.py "
                        f"--region {region} --dataset {dataset} --write-ledger）",
            })
        # 添加缓存参数支持
        if extra_args:
            # 检查是否包含缓存相关参数
            if "--force-refresh" in extra_args:
                cmd.append("--force-refresh")
            if "--cache-ttl" in extra_args:
                # 找到 --cache-ttl 参数的值
                try:
                    ttl_idx = extra_args.index("--cache-ttl")
                    if ttl_idx + 1 < len(extra_args):
                        ttl_value = extra_args[ttl_idx + 1]
                        cmd.extend(["--cache-ttl", ttl_value])
                except (ValueError, IndexError):
                    pass  # 如果参数格式不正确，忽略
            # 移除已处理的缓存参数，避免重复传递
            extra_args = [arg for arg in extra_args if arg not in ["--force-refresh", "--cache-ttl"]]
            # 移除 --cache-ttl 的值
            if "--cache-ttl" in extra_args:
                try:
                    ttl_idx = extra_args.index("--cache-ttl")
                    if ttl_idx + 1 < len(extra_args):
                        extra_args.pop(ttl_idx + 1)  # 移除值
                    extra_args.pop(ttl_idx)  # 移除参数名
                except (ValueError, IndexError):
                    pass
    elif stage == "S2" and subcommand == "assemble-priors":
        # 2026-09-27（P0-2 真实环境演练补充）：assemble-priors 只把 DB 里的 KB 组装成
        # priors 文件 + 快照，零配额、不开波，不走下面的三道开波闸与 S0/S1 产物预检。
        # 此前它们同样拦截 assemble-priors：KOR 真实历史（最近 3 个 closed 波全 FAIL）
        # 命中停止规则 B 后，S6 回写的新 dead_ends 再也进不了快照，GEM 的快照过期告警
        # 指向的恰是这条被拦的命令；而 gem SKILL 的 stage="S6" 写法不经闸，两条路径不一致。
        # diversity-extract 会生成候选（同 build_wave），仍走闸。
        result["steps"].append({
            "step": "region_gates",
            "success": True,
            "skipped": True,
            "reason": "assemble-priors 为本地 KB→priors 组装（零配额、不开波），不受开波闸约束",
        })
    elif stage == "S2":
        # 三道开波闸（信号天花板 / 停止规则 2026-09-15 ⑦ / 积压 2026-09-15 行动 3）：
        # 纯 DB 判定、零配额，干跑也走 —— 干跑就该回答"这个区还值不值得继续开波"。
        gate_steps, gate_error = run_open_wave_gates(region, dataset, campaign_dir)
        result["steps"].extend(gate_steps)
        if gate_error:
            result["success"] = False
            result["error"] = gate_error
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
                store=store,
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

        # 2026-09-12 修复(2)：S2 的 script_map 指向 build_wave.py **本体**，它没有
        # `build-wave` 子命令（那是 campaign.py 分发器的入口名）。此前无条件追加
        # `["build-wave", "--from-db"]` 拼出 `build_wave.py ... --wave W build-wave --from-db`，
        # 多出的位置参数被 argparse 拒绝（rc=2）；而 validate_argv 只校验子命令/选项、
        # 不校验多余位置参数，干跑也放行。subcommand 路由（assemble-priors 等）时脚本
        # 已切到 campaign.py，本分支不得再拼任何 build_wave 参数，交给下方路由块。
        if subcommand not in _SUBCOMMAND_ROUTED:
            if dataset:
                cmd.extend(["--dataset", dataset])
            if wave:
                cmd.extend(["--wave", wave])
            cmd.append("--from-db")
            # size is capacity, never an implicit exact-count contract.
            # Reviewed experiments opt in via --selection-contract-key (identities)
            # or explicit --expected-count (legacy count-only guard).
    elif stage == "S3":
        # 三道开波闸（同 S2：纯 DB 判定，dry-run 也走）
        gate_steps, gate_error = run_open_wave_gates(region, dataset, campaign_dir)
        result["steps"].extend(gate_steps)
        if gate_error:
            result["success"] = False
            result["error"] = gate_error
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
        # 2026-09-15 ④：review_wave.py 要求 --multisim 或 --alphas，此前节点只传 --tag，
        # 实跑必 `error: need --multisim or --alphas`（rc=2，campaign_USA_S4_20260903 实证）
        # 而干跑因 argv 静态契约通过而报 success。现从库解析本波 alpha_id 再拼命令。
        if not wave:
            result["steps"].append({
                "step": "resolve_s4_alphas", "success": False,
                "error": "S4 需要 wave（用于从 backtest_results 解析本波 alpha_id）",
            })
            result["success"] = False
            result["error"] = "S4 requires wave"
            return result
        alpha_ids, resolved_wave, available = _resolve_wave_alpha_ids(region, wave, dataset)
        if not alpha_ids:
            hint = f"该 region 最近的波次: {available[:10]}" if available else "该 region 尚无 backtest_results"
            result["steps"].append({
                "step": "resolve_s4_alphas", "success": False,
                "error": f"backtest_results 中找不到 region={region} wave={wave} 的 alpha（{hint}）；"
                         "先跑步 6 回测，或用 review_wave.py --multisim <id> 手动评审",
            })
            result["success"] = False
            result["error"] = f"no backtest alphas for {region}/{wave}"
            return result
        result["steps"].append({
            "step": "resolve_s4_alphas", "success": True,
            "wave": resolved_wave, "alpha_count": len(alpha_ids),
        })
        # ---- 2026-10-02 P1：S4 前置预筛（离线版，零平台 API）----
        # 背景：SKILL.md 步 7 把 `s4-prescreen`（全灭直接判死）写成固定动作，但它**从未被编排调用**
        # （grep 全仓仅注释+文档），所谓"8× 预筛压缩"实际靠人手工。此处补上编排前置。
        # 用**离线**口径（读 backtest_results 已落库指标，调 _lib/prescreen 唯一口径），
        # 而非在线 `campaign_intel s4-prescreen`（后者要平台鉴权，campaign 节点未必持有）。
        # 语义：全灭（REJECT==全部）→ 跳过昂贵的 review_wave，直接判死；有存活则照常评审并带上分层。
        try:
            pre = _s4_prescreen_local(region, resolved_wave, alpha_ids)
        except Exception as e:  # noqa: BLE001 — 预筛失败不阻断（fail-open）
            pre = None
            result["steps"].append({"step": "s4_prescreen", "success": False,
                                    "error": f"预筛失败（不阻断）: {e}"})
        if pre is not None:
            result["steps"].append({
                "step": "s4_prescreen", "success": True,
                "tiers": {k: len(v) for k, v in pre.items() if isinstance(v, list)},
                "ready": pre.get("READY", []), "reject": pre.get("REJECT", []),
                "source": "offline _lib/prescreen（backtest_results 已落库指标）",
            })
            n_total = len(alpha_ids)
            if n_total and not pre.get("READY") and not pre.get("REVIEW"):
                # 全灭：整波无一条够格进评审 → 判死，不跑 review_wave
                result["success"] = True
                result["steps"].append({
                    "step": "s4_prescreen_all_reject", "success": True,
                    "message": f"{n_total} 条全判 REJECT（0 READY / 0 REVIEW）→ 本波判死，"
                               "跳过 review_wave（对齐 SKILL.md 步 7「全灭直接判死」）",
                })
                return result
        cmd.extend(["--alphas", *alpha_ids])
        cmd.extend(["--tag", str(resolved_wave)])
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
        if subcommand == "assemble-priors":
            # 2026-09-27 P0-2：GEM 默认 `--priors-from-db`，只读 DB 快照 priors_snapshot_<region>；
            # 快照只有 `--snapshot-ledger` 才会写。此前本节点不带它 —— 按 SOP 步 4 调用只重写
            # priors 文件，S6 回写的 region_kb 进不了下一波 GEM（新区快照缺失则 GEM fail-closed）。
            # priors 是区域级产物：assemble_priors.py 不认 --dataset/--wave。拼上后干跑照样放行
            # （validate_argv 只校验到 campaign.py 分发层），实跑才 exit 2 "unrecognized arguments"。
            if "--snapshot-ledger" not in (extra_args or []):
                cmd.append("--snapshot-ledger")
        else:
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
    task_dir = os.path.abspath(resolve_async_tasks_root())
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
            from ..process_identity import process_identity
            with open(task_file, "w", encoding="utf-8") as f:
                json.dump({
                    "task_id": task_id,
                    "status": "running",
                    "pid": process.pid,
                    "cmd": cmd,
                    "process_identity": process_identity(process.pid),
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

                # S4 walls 诊断（2026-10-02 P0：优先读结构化台账，stdout 扫描降为 fallback）
                if stage == "S4":
                    walls = _extract_walls_summary(stdout or "", region=region, wave=wave,
                                                   store=store)
                    if walls:
                        exec_result["walls"] = walls
                        exec_result["walls_source"] = walls.pop("_source", "unknown")

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
                        # 与上方 cache_key 同名（2026-09-17 P2-12：不再用 priors_snapshot_{region}）
                        thread_store.upsert_ledger(region, f"assemble_priors_cache_{region}", {
                            "assembled_at": datetime.now().isoformat(),
                            "region": region,
                            "stdout_tail": exec_result.get("stdout_tail", ""),
                        })
                        # T2 事件（2026-09-30 方案 B）：assemble-priors 成功后 region_kb→priors
                        # 已按最新 DB 快照刷新，是客观事实，供 step_eval 的 kb_refresh 消费。
                        # dedupe_key 按天：同一天多次重跑只计一次（region_kb 刷新是区域级幂等动作）。
                        from wqb.step_events import safe_record_event
                        safe_record_event(
                            region, "S2", "region_kb_refreshed",
                            value=1.0, source="campaign.py::run(assemble-priors)",
                            dedupe_key=f"assemble-priors:{datetime.now().strftime('%Y%m%d')}",
                            metadata={"wave": wave},
                        )
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
    store: Any = None,
) -> Dict[str, Any]:
    """波次前置条件预检（S0/S1 产物门禁，S2/S3 前强制）.

    校验字段 catalog（文件 + DB 单一事实源）、新鲜度与判死清单。
    通用修复入口：FAIL 时按 remediation 跑 tools/preflight_wave.py --repair。
    
    2026-09-12 增强：预检成功后自动补录 S2 合规记录（如缺失）。
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
            return result
        
        # 2026-09-12 增强：预检成功后自动补录 S2 合规记录（如缺失）
        if wave and store:
            s2_key = f"s2_compliance_w{wave}"
            try:
                existing = store.get_ledger(region, s2_key)
                if not existing:
                    # 从 S1 ledger 读取 ideas_md_path
                    s1_key = f"s1_{dataset}_d1"  # 默认 delay=1
                    s1_record = store.get_ledger(region, s1_key)
                    if s1_record and s1_record.get("ideas_md_path"):
                        s2_data = {
                            "wave": wave,
                            "feature_engineering_doc": s1_record["ideas_md_path"],
                            "candidate_pool_source": "skill",
                            "marked_at": datetime.now().isoformat(),
                            "notes": "auto-marked by preflight (S2 compliance auto-fix)",
                        }
                        store.upsert_ledger(region, s2_key, s2_data)
                        result["s2_compliance_auto_marked"] = True
                        logger.info(f"Auto-marked S2 compliance: {s2_key}")
            except Exception as e:
                logger.warning(f"Failed to auto-mark S2 compliance: {e}")
                # 不阻断流程，仅记录警告
                result["s2_compliance_warning"] = str(e)
                
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
    # 2026-09-17 优化：去掉 --quality-block（质量预估降级为仅标注）。
    # 根因：质量预估模型不准（model32 预估 WEAK=27/HARD=29 实测 S=1.33；
    # model252 预估 WEAK=10/HARD=24 实测 S=2.37），硬拦截会错过有信号的数据集。
    gate_cmd = [
        py, os.path.join(resolve_tools_dir(), "wave_gate.py"),
        "--campaign-dir", campaign_dir,
        "--from-db",
        # 不再传 --quality-block：质量预估仅标注不拦截
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

        # wave_gate.py 在默认模式（无 --quality-block）下不会因质量预估返回非零。
        # 只有语法/字段/毒模式等硬闸失败才返回非零。
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


def _resolve_wave_alpha_ids(region: str, wave: str, dataset: Optional[str]):
    """从 backtest_results 解析本波 alpha_id（S4 评审输入）。

    wave 两套命名并存（战役编号 "61" / GEM 标签 "s2_<ds>_d<delay>"），按序尝试：
    精确匹配 → 有 dataset 时 `s2_<dataset>_d%` 标签。返回 (ids, 命中的 wave, 该区最近波次列表)。
    """
    db_path = resolve_db_path()
    ids: List[str] = []
    hit = str(wave)
    recent: List[str] = []
    try:
        conn = connect_db_readonly(db_path)   # 纯读：库不存在时不建空库（dry-run 同走此路）
        try:
            rows = conn.execute(
                "SELECT DISTINCT alpha_id FROM backtest_results WHERE region=? AND wave=? "
                "AND alpha_id IS NOT NULL AND alpha_id != '' ORDER BY id", (region, str(wave)),
            ).fetchall()
            ids = [r[0] for r in rows]
            if not ids and dataset:
                rows = conn.execute(
                    "SELECT DISTINCT alpha_id, wave FROM backtest_results WHERE region=? "
                    "AND wave LIKE ? AND alpha_id IS NOT NULL AND alpha_id != '' ORDER BY id",
                    (region, f"s2_{dataset}_d%"),
                ).fetchall()
                ids = [r[0] for r in rows]
                if rows:
                    hit = str(rows[-1][1])
            recent = [
                str(w) for (w,) in conn.execute(
                    "SELECT wave FROM backtest_results WHERE region=? AND wave IS NOT NULL "
                    "GROUP BY wave ORDER BY MAX(id) DESC LIMIT 10", (region,))
            ]
        finally:
            conn.close()
    except Exception as e:  # 库不可读 → 当作无结果，由调用方给提示
        logger.warning(f"_resolve_wave_alpha_ids failed: {e}")
    return ids, hit, recent


def _s4_prescreen_local(region: str, wave: str, alpha_ids: List[str]):
    """S4 前置预筛（离线，2026-10-02 P1）。

    读 `backtest_results` 已落库指标，调 `_lib/prescreen.prescreen`（三处唯一口径）分层。
    返回 {"READY": [...], "REVIEW": [...], "REJECT": [...]}；不可用返回 None（调用方 fail-open）。

    **为何用离线版而不是 `campaign_intel s4-prescreen`**：后者逐条打平台 `get_alpha_details`
    （要鉴权 + 平台往返），campaign 节点未必持有凭据；而 S4 前置的唯一目的就是"全灭则别跑
    review_wave"，用已落库指标足矣。在线版仍保留给人工/需要 prod-self 精确值时的场景。
    """
    import sys as _sys
    # 仓库副本优先（安装位可能滞后、缺 prescreen.py —— 2026-10-02 实测踩坑）。
    _ps_file = resolve_toolkit_file("_lib/prescreen.py")
    if not _ps_file:
        return None
    _scripts_dir = os.path.dirname(os.path.dirname(_ps_file))  # .../scripts
    if _scripts_dir not in _sys.path:
        _sys.path.insert(0, _scripts_dir)
    from _lib.prescreen import prescreen as _ps  # type: ignore

    conn = connect_db_readonly(resolve_db_path())
    try:
        conn.row_factory = sqlite3.Row
        qmarks = ",".join("?" * len(alpha_ids))
        rows = [dict(r) for r in conn.execute(
            f"SELECT * FROM backtest_results WHERE region=? AND wave=? AND alpha_id IN ({qmarks})",
            (region, str(wave), *alpha_ids))]
    finally:
        conn.close()
    if not rows:
        return None
    # 区域阈值（USA sharpe_min=1.25 等）若可得则注入；缺省用 prescreen 的 DEFAULT
    thresh = None
    try:
        _t = _resolve_thresholds_for_region(region)
        if _t:
            thresh = {
                "sharpe_min": _t.get("sharpe_min"),
                "fitness_min": _t.get("fitness_min"),
                "two_year_min": _t.get("two_year_sharpe_min"),
                "turnover_min": _t.get("turnover_min"),
                "turnover_max": _t.get("turnover_max"),
            }
    except Exception:  # noqa: BLE001 — 阈值读不到 → 用 DEFAULT
        thresh = None
    res = _ps(rows, thresh)
    return {k: res.get(k, []) for k in ("READY", "REVIEW", "REJECT")}


def _resolve_thresholds_for_region(region: str):
    """读 `tracking/<REGION>/config/thresholds.json` 的 review 节（缺失返回 None）。"""
    try:
        p = os.path.join(resolve_campaign_dir(region), "config", "thresholds.json")
        if not os.path.isfile(p):
            return None
        with open(p, encoding="utf-8") as f:
            return (json.load(f) or {}).get("review")
    except Exception:  # noqa: BLE001
        return None


def _field_inspect_pack_check(region: str, campaign_dir: str) -> Dict[str, Any]:
    """S0 开区硬前置（零成本只读，2026-09-28 P1-3）：白名单数据集的体检包缺失清单.

    包路径 = tracking/mining/field_inspect_<region 小写>_<dataset>.json；缺包时步 5 的
    体检硬门不生效（低覆盖/厚尾/稀疏事件的预处理约束一路裸奔到仿真）。
    白名单来源：ledger `s0_whitelist`（缺则 settings.json 的 `_s0_whitelist`）。
    只报告不拦截（拦截由 wave_gate 的 --inspect-mode / 新数据集首波自动 enforce 负责）。
    """
    step: Dict[str, Any] = {"step": "field_inspect_pack_check", "success": True}
    try:
        datasets: List[str] = []
        conn = connect_db_readonly(resolve_db_path())
        try:
            row = conn.execute(
                "SELECT value FROM ledger_kv WHERE region=? AND key='s0_whitelist'",
                (region,)).fetchone()
        finally:
            conn.close()
        if row and row[0]:
            val = json.loads(row[0]) if isinstance(row[0], (str, bytes)) else row[0]
            if isinstance(val, dict):
                datasets = [str(d) for d in (val.get("datasets") or [])]
            elif isinstance(val, list):
                datasets = [str(d) for d in val]
        if not datasets:
            try:
                with open(os.path.join(campaign_dir, "config", "settings.json"),
                          encoding="utf-8") as f:
                    datasets = [str(d) for d in (json.load(f).get("_s0_whitelist") or [])]
            except (OSError, json.JSONDecodeError):
                datasets = []
        mining = os.path.join(os.path.dirname(os.path.abspath(campaign_dir)), "mining")
        if not os.path.isdir(mining):
            mining = os.path.join(REPO_ROOT, "tracking", "mining")
        packs: Dict[str, Optional[str]] = {}
        missing: List[str] = []
        for ds in datasets:
            fn = f"field_inspect_{region.lower()}_{ds}.json"
            ok = os.path.exists(os.path.join(mining, fn))
            packs[ds] = fn if ok else None
            if not ok:
                missing.append(ds)
        step.update({"datasets": datasets, "packs": packs, "missing_packs": missing,
                     "mining_dir": mining})
        if missing:
            step["warning"] = (
                f"体检包缺失 {len(missing)}/{len(datasets)}：{missing} —— 步 5 体检硬门对这些集"
                f"不生效（预处理约束无把关）；生成（离线零配额）："
                f"python tools/gen_field_inspect_packs.py --region {region} --delay <D>")
        elif datasets:
            step["message"] = f"{len(datasets)} 个白名单数据集体检包齐备"
        else:
            step["message"] = "未读到白名单（ledger s0_whitelist / settings._s0_whitelist 均空），跳过"
    except Exception as e:
        step["warning"] = f"field_inspect pack check failed: {e}"
    return step


def _semantic_coverage_check(region: str, dataset: str) -> Dict[str, Any]:
    """S1 语义台账覆盖检查 + **自动补做**（2026-10-01 步3 断流修复 · 通气 B）.

    背景（实测）：`s1_semantic_<ds>` 台账覆盖率极低——全库 catalog 697 个，语义台账
    仅 33 个（4.7%）；EUR/IND/GLB/JPN 全为 0。于是步 5 闸 SEM 的 fail-closed 在多数
    区域只能靠「阻断」生效，而非「过滤」——一旦 waiver 放行，49.4% 非信号字段就裸奔。

    本步让「跑 S1」= 「typed catalog + 语义归类」一次做完（本地、零配额、秒级），
    把语义归类从「人工记忆的可选动作」变成 **S1 的默认产物**。

    **补做触发条件（两条，2026-10-01 修订）**：
    1. `missing_ledger` —— 缺 `s1_semantic_<ds>` 台账；
    2. `missing_families` —— 台账在但由**旧版**生成（不含 L3.5：`family_stats`/`families`
       键都不存在）。

    ⚠ 判定必须用 `wqb.semantic_ledger.ledger_has_l35()`（键存在），**不能用「族非空」**：
    原生集字段名不带角色后缀、空族是正确结果，按"族为空"判补做会导致永不幂等。

    第 2 条是 L3.5 落地后的断流修复：全库 414 个语义台账里仅 76 个（18.4%）带
    `families`，338 个是 families 功能之前生成的旧版（含 KOR 主力集 model109 /
    other466 / fundamental17）。旧实现见台账存在即 return、只把「缺 families」记成
    info 提示 ⇒ **L4 形态构建五步法的第一步「族」在 81.6% 的数据集上拿不到输入**。
    重跑是本地零配额秒级，故缺 families 与缺台账同等对待。

    **fail-open**：任何异常只记 warning，不阻断 S1（S1 的主产物是 typed catalog，
    语义归类是附加产物；阻断由步 5 闸 SEM 负责）。
    """
    step: Dict[str, Any] = {"step": "semantic_coverage_check", "success": True}
    if not dataset:
        step["message"] = "无 dataset，跳过语义归类检查"
        return step
    try:
        conn = connect_db_readonly(resolve_db_path())
        try:
            row = conn.execute(
                "SELECT value FROM ledger_kv WHERE region=? AND key=?",
                (region, f"s1_semantic_{dataset}")).fetchone()
        finally:
            conn.close()
        if row and row[0]:
            sem = parse_ledger(row[0])
            if isinstance(sem, dict):
                # ★ 补做条件 = 台账**不含 L3.5**（缺 family_stats/families 键），而非"族为空"。
                # 原生集（fundamental*/pv*/news*）字段名不带角色后缀 → 空族是**正确结果**，
                # 若按"族为空"补做会导致每次 S1 都重跑、永不幂等。口径见 wqb.semantic_ledger。
                has_l35 = ledger_has_l35(row[0])
                n_fam = len(sem["families"]) if isinstance(sem.get("families"), dict) else 0
                step.update({
                    "ledger": True,
                    "total_fields": sem.get("total_fields"),
                    "blocked_field_count": sem.get("blocked_field_count"),
                    "has_families": has_l35,
                    "family_count": n_fam,
                })
                if has_l35:
                    step["message"] = (f"s1_semantic_{dataset} 台账在（非信号 "
                                       f"{sem.get('blocked_field_count')} 字段，"
                                       f"L3.5 族 {n_fam} 个）")
                    if n_fam == 0:
                        step["info"] = ("该集无结构族（字段名不含角色/期限/方向后缀，属正常结果）"
                                        "——L4 退化用 L3 经济大类 by_category 作聚合轴")
                    return step
                # 台账在但由旧版生成（不含 L3.5）→ 与缺台账同等对待
                reason = "missing_families"
                step["info"] = "旧版台账缺 L3.5 段（L4 机制推理的输入），自动重跑补齐"
            else:
                reason = "missing_ledger"
        else:
            reason = "missing_ledger"

        # 缺台账 / 缺 L3.5 族 → 自动补做（本地、零配额、秒级）
        script = os.path.join(REPO_ROOT, "tools", "field_semantic_classify.py")
        if not os.path.exists(script):
            step["warning"] = f"语义归类脚本缺失：{script}（无需阻断，步 5 闸 SEM 仍会兜底）"
            return step
        cmd = [wq_py(), "-u", script, "--region", region, "--dataset", dataset, "--write-ledger"]
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=300, cwd=REPO_ROOT)
        if proc.returncode != 0:
            step["warning"] = (f"语义归类自动补做未成功（rc={proc.returncode}），"
                               f"不阻断 S1；可手动跑：python tools/field_semantic_classify.py "
                               f"--region {region} --dataset {dataset} --write-ledger；"
                               f"stderr: {(proc.stderr or '')[-300:]}")
            return step
        _why = ("缺 s1_semantic_%s 台账" % dataset) if reason == "missing_ledger" \
            else ("s1_semantic_%s 缺 L3.5 families 段" % dataset)
        step.update({"ledger": True, "auto_ran": True, "reason": reason,
                     "message": f"{_why}，已自动补做（本地零配额）"})
    except Exception as e:
        step["warning"] = f"semantic coverage check failed: {e}"
    return step


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
        conn = db_connect(db_path)
        c = conn.cursor()

        # 读 s0_whitelist 获取 delay/universe（2026-09-17 P0-4 修复）
        # 旧实现只认 `filter_criteria.{delay,universe}` —— 实测全 13 个区域的白名单
        # 均无 `filter_criteria` 键（`value LIKE '%filter_criteria%'` 返回空），
        # 属**死代码**：白名单锁定的 universe 从未被本节点消费，恒回落
        # delay=1 / universe="TOP3000" 再被 regions 表 legal[0] 覆盖。
        # 现改用 wqb.ledger_whitelist 的容错归一（覆盖 candidates/whitelist/datasets/
        # 推断/损坏抢救 共 5 种历史形态），解析失败**显式告警**而非静默回落。
        delay, universe = 1, "TOP3000"
        c.execute("SELECT value FROM ledger_kv WHERE region=? AND key='s0_whitelist'", (region,))
        row = c.fetchone()
        if row:
            try:
                from ...ledger_whitelist import normalize as _norm_wl
                _wl = _norm_wl(row[0])
                if _wl.get("delay") is not None:
                    delay = _wl["delay"]
                if _wl.get("universe"):
                    universe = _wl["universe"]
                if _wl.get("schema") in ("inferred", "recovered"):
                    logger.warning(
                        f"_ensure_campaign_config({region}): s0_whitelist 形态="
                        f"{_wl['schema']}（{_wl.get('reason')}）")
                elif not _wl.get("ok"):
                    logger.warning(
                        f"_ensure_campaign_config({region}): s0_whitelist 无法解析"
                        f"（{_wl.get('reason')}）——回落 delay={delay}/universe={universe}")
            except Exception as e:
                logger.warning(
                    f"_ensure_campaign_config({region}): s0_whitelist 归一失败 "
                    f"{type(e).__name__}: {e}")

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

        # 区域默认中性化：只在新建战役目录时兜底，取 config.REGIONS 的 default_neutralization（缺省 SUBINDUSTRY）。
        # 建好之后以 settings.json 为准；组合级覆盖在 cells.json（2026-10-04 收口：此前是本函数里的区域字面量表）。
        from wqb.config import REGIONS as _REGIONS
        neutralization = (_REGIONS.get(region) or {}).get("default_neutralization", "SUBINDUSTRY")

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


def _extract_walls_summary(stdout: str, region: Optional[str] = None,
                           wave: Optional[str] = None,
                           store: Any = None) -> Optional[Dict[str, Any]]:
    """提取 S4 walls 诊断摘要（2026-10-02 P0 改造：结构化优先，stdout 扫描降为 fallback）。

    **主路径**：`review_wave.py` 评审后已把结构化墙摘要写入 ledger 键
    `s4_walls_<region>_<wave>`（值含 `walls: {墙名: 计数}` + `per_alpha`）。本函数优先读它——
    **不经任何文本解析**，无漏报/误报。

    **降级路径（fallback）**：拿不到结构化键时，退回对子进程 stdout 做关键词扫描。
    这条路径有已知缺陷（2026-10-02 实测）：全 PASS 输出 → 返回 None（漏报）；
    含 "structural" 字样的普通告警行 → 产出假墙（误报）。保留仅为兼容旧调用方/离线日志，
    **不应作为主依据**；返回值会带 `_source: "stdout_scan"` 以资区分。

    返回 dict 带 `_source` ∈ {"ledger", "stdout_scan"}；调用方 pop 掉再入库。
    """
    # ---- 主路径：读结构化台账键（store 可来自 ctx；缺则惰性建一个）----
    if region and wave:
        st = store
        if st is None:
            try:
                from ...store.campaign import CampaignStore
                st = CampaignStore(resolve_db_path())
            except Exception:  # noqa: BLE001 — 建 store 失败 → 走 fallback
                st = None
        if st is not None:
            try:
                payload = st.get_ledger(region, f"s4_walls_{region}_{wave}")
                if isinstance(payload, dict) and isinstance(payload.get("walls"), dict):
                    out = dict(payload)
                    out["_source"] = "ledger"
                    return out
            except Exception:  # noqa: BLE001 — 台账不可读 → 走 fallback
                pass

    # ---- 降级路径：stdout 关键词扫描（缺陷见 docstring）----
    if not stdout:
        return None

    walls: Dict[str, Any] = {}
    lower = stdout.lower()

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
    sharpe_match = re.search(r"sharpe[=:]\s*([\d.]+)", lower)
    if sharpe_match:
        walls["sharpe"] = float(sharpe_match.group(1))
    fitness_match = re.search(r"fitness[=:]\s*([\d.]+)", lower)
    if fitness_match:
        walls["fitness"] = float(fitness_match.group(1))

    if not walls:
        return None
    walls["_source"] = "stdout_scan"
    return walls
