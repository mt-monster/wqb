# -*- coding: utf-8 -*-
"""submit_alpha 节点：提交路由与状态确认.

真实调用 brain_client（submit_alpha / set_alpha_properties / get_alpha_details），
替代 worldquant-submit-alpha 的 PowerShell 命令模板。

职责边界（2026-08-31 修复）：
  - 旧实现三个 `_call_mcp_*` 全部返回硬编码模拟值，会虚报"提交成功"。
  - 现改为真实调用 brain_client 单例；凭据解析与 MCP 服务一致。
  - 提交是敏感决策：默认仅做预检 + 状态查询，只有 confirm_submit=True
    才真正 POST submit（与"judge READY 后停等确认"纪律一致）。
"""
from __future__ import annotations

import logging
import os
import re
import sqlite3
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from ...config import ALLOW_ALPHA_SUBMIT, WAIT_THRESHOLDS
from .._common import (
    get_brain_client as _get_brain_client,
    persist_workflow_record,
    run_async as _run_async,
)
from ...config import compute_webdata_failed_counts, merge_failed_items
from ...quota import REGULAR_DAILY_LIMIT, probe_today

logger = logging.getLogger(__name__)

#: 异步受理后等状态翻转的窗口（秒）——唯一来源 wqb.config.WAIT_THRESHOLDS（2026-09-29：180 → 240）
_FLIP_WAIT_S = int(WAIT_THRESHOLDS["submit_flip_wait_s"])

_POLL_INTERVAL_SEC = int(WAIT_THRESHOLDS["submit_flip_poll_s"])

# 提交层硬闸项：模拟层 WARNING 但提交层 FAIL 的检查名（与 tools/submit_verdict.py 同口径）。
# 2026-09-29 P0：这些 WARNING 在 POST submit 时平台会重新评估为 FAIL，必须在本地 fail-closed 拦截。
_SUBMIT_HARD_GATE_WARNINGS = {"LOW_FITNESS", "LOW_SHARPE", "LOW_2Y_SHARPE", "IS_LADDER_SHARPE"}

#: REGULAR 提交前 prod 闸阈值（用户铁律：prod ≥ 0.7 不得提交）。与 super_build.py 的
#: `--prod-gate` 默认值同口径；本节点不允许把阈值放宽到 ≥0.7 之外。
_PROD_THRESHOLD = 0.7

#: REGULAR 每日提交配额上限（ET 日历日）。唯一实现口径 = `wqb.quota`
#: （REGULAR 4 / SUPER 1 / PPA 独立 1）。本节点只前置 REGULAR 的账务核对。
_REGULAR_QUOTA_LIMIT = REGULAR_DAILY_LIMIT


def _derive_tags(alpha_id: str, dataset: Optional[str], wave: Optional[str],
                 expr_family: Optional[str], channel: Optional[str]) -> List[str]:
    """按规范自动生成 tags；并**保留平台已有标签**（避免误清 RETIRE_* 等留痕）。

    规范见 `docs/alpha_properties_spec.md`：
        CH_<通道> · SRC_<数据集> · W<波次> · EXPRFAM_<族> · CORR_<档> · TOOL_<工具>
    平台已有的 `RETIRE_*` 等人工留痕一律保留、追加在末尾。
    """
    try:
        from ...alpha_properties import build_tags  # wqb.alpha_properties
    except Exception:  # pragma: no cover - 路径兜底
        try:
            from wqb.alpha_properties import build_tags  # type: ignore
        except Exception:
            return []

    # 读取平台已有标签（用同步 client，容错）
    existing: List[str] = []
    try:
        client = _get_brain_client()
        details = _run_async(client.get_alpha_details(alpha_id))
        if isinstance(details, dict):
            existing = [str(t) for t in (details.get("tags") or [])]
    except Exception as e:  # noqa: BLE001
        logger.warning(f"读取已有 tags 失败（将不保留）：{e}")

    # 已有手工留痕（RETIRE_* 等）保留；规范前缀的旧标签由新生成覆盖
    keep = [t for t in existing if not t.startswith(("CH_", "SRC_", "W", "EXPRFAM_", "CORR_", "TOOL_"))]

    built = build_tags(
        channel=channel,
        dataset=dataset,
        wave=wave,
        expr_family=expr_family,
        extra=keep,
    )
    return built


def _preserved_properties(details: Any, *, name: Optional[str],
                          descriptions: Optional[str]) -> Dict[str, Any]:
    """调用方未给的 name / descriptions 一律视为"保留平台现值"，返回被保留的值供留痕。

    输入 `details` 是 get_alpha_details 的返回（dict），缺字段时容错为 None。
    """
    out: Dict[str, Any] = {}
    if not isinstance(details, dict):
        return out
    if name is None:
        out["name"] = details.get("name")
    if descriptions is None:
        reg = details.get("regular")
        out["description"] = reg.get("description") if isinstance(reg, dict) else None
    return out


def _derive_name(name: Optional[str], details: Any, *, dataset: Optional[str],
                 wave: Optional[str], expr_family: Optional[str], channel: Optional[str],
                 alpha_type_hint: Optional[str] = None) -> Dict[str, Any]:
    """`name=None` 时按规范生成 `<REGION>_<R|S>_<family>_<NN>`。

    2026-10-05 补：此前 `build_name` 在 REGULAR 提交链路上**零调用**
    （`git grep build_name` 只命中 `super_build.py`），即name 完全由调用方自由填写
    —— 规范里的3 位大写区域码校验、`seq ∈ 1..99`、族名净化**全部不生效**，
    且 `name=None` 时按`_preserved_properties` 保留提交前的临时名。

    seq 取法：优先用调用方给的 `wave` 的数字部分（波次号在区域内唯一且单调，
    是最自然的序号来源）；解析不出则退回 1。**无法确定 region 时不生成**——
    宁可保留平台现值，也不要瞎编一个区域码（`build_name` 会抛 ValueError）。

    返回 `{"name": <最终名或None>, "derived": bool, "note": str}`。
    """
    out: Dict[str, Any] = {"name": name, "derived": False, "note": ""}
    if name:
        return out

    try:
        from ...alpha_properties import build_name  # wqb.alpha_properties
    except Exception:  # pragma: no cover - 路径兜底
        try:
            from wqb.alpha_properties import build_name  # type: ignore
        except Exception:
            out["note"] = "build_name 不可用，保留平台现名"
            return out

    region = _extract_region(details)
    if not region:
        out["note"] = f"无法从 alpha_details 判定 region（读到 {region!r}），保留平台现名"
        return out

    # alpha 类型：REGULAR / SUPER（SUPER 走 super_build，不经本节点，仍兼容）
    at = (alpha_type_hint or "").strip().upper() or "REGULAR"

    # family：显式给的 expr_family 优先；否则退化用数据集名；再否则 alpha
    fam = expr_family or dataset or "alpha"
    fam = re.sub(r"[^a-z0-9_]", "_", str(fam).lower())[:18].strip("_") or "alpha"

    # seq 取 wave 的数字部分（波次号在区域内唯一且单调，是最自然的序号来源）
    seq = 1
    m = re.search(r"(\d+)", str(wave or ""))
    if m:
        n = int(m.group(1))
        seq = n if 1 <= n <= 99 else (n % 100 or 1)

    try:
        out["name"] = build_name(region, at, fam, seq)
        out["derived"] = True
        out["note"] = f"按build_name 生成（region={region} family={fam} seq={seq}）"
    except Exception as e:  # noqa: BLE001
        out["note"] = f"build_name 失败（{e}），保留平台现名"
        out["name"] = None
    return out


def run(
    alpha_id: str,
    name: Optional[str] = None,
    color: Optional[str] = None,
    tags: Optional[List[str]] = None,
    descriptions: Optional[str] = None,
    force: bool = False,
    robustness_audited: bool = False,
    confirm_submit: bool = False,
    verify_timeout: int = _FLIP_WAIT_S,
    dataset: Optional[str] = None,
    wave: Optional[str] = None,
    expr_family: Optional[str] = None,
    channel: Optional[str] = None,
    mix_narrative: Optional[Dict[str, str]] = None,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """执行 alpha 提交流程.

    Args:
        alpha_id: Alpha ID
        name: 名称。**默认 None**；规范格式见 `wqb.alpha_properties.build_name`
            （`<REGION>_<R|S>_<family>_<seq>`）。禁止用 PROD 数值命名（会过期）。
        color: 颜色。**默认 None → 提交态用 BLUE**。平台仅接受
            `GREEN/BLUE/RED/YELLOW/PURPLE`（其余 400），见 `alpha_properties.COLORS`。
        tags: 标签。**默认 None → 按规范自动生成**（见下）；显式传入则以传入为准。
        descriptions: 描述文本（三段式，≥100 英文词）
        force: 是否跳过本地预检（仅当 confirm_submit=True 时有意义）。
            **不豁免 prod 闸**——prod 是用户合规红线，与预检分离，且无任何豁免入口。
            **也不豁免** Step 1.2 的 `weight_grid`/`stack` 结构硬拦、Step 1.7 的 ΔSharpe<0 硬闸。
            **可豁免**（留痕）Step 1.2 的三问、Step 1.5 的 robustness 声明、Step 1.8 的分散度软闸
            ——这三项是自设纪律，不是平台规则。
        robustness_audited: 是否已通过 brain-alpha-robustness 审计（Phase B/C 逐年归因）。
            **fail-closed（2026-09-29 P0）**：confirm_submit=True 时必须为 True，
            否则拒绝提交（除非 force）。robustness 的 Phase B.0 硬门（Failed RA/PPA==0）
            已由 submit_gate 自动判定，此参数补齐无法自动的逐年归因部分。
            **2026-10-02**：若 ledger 已有 ``robustness_<alpha_id>`` 记录（agent 已跑过审计
            并落库），本声明闸降为辅助——不再强制重复声明；台账 ``REJECT`` 由 Step 1 直接拦下。
        confirm_submit: 是否真正 POST submit（默认 False，只做预检+状态查询）
        verify_timeout: 提交后状态确认超时（秒）
        dataset: 来源数据集 → 自动生成 `SRC_<dataset>` 标签
        wave: 波次 → 自动生成 `W<wave>` 标签
        expr_family: 表达式族 → 自动生成 `EXPRFAM_<family>` 标签（防同族自相残杀）
        channel: 通道标签覆盖（默认按 type 推断 `CH_REG`/`CH_SUPER`）
        mix_narrative: 混腿「三问」答案（2026-11-08）。键固定三个：
            ``holders``（两腿的信息持有者分别是谁）/ ``polarity``（极性是否对齐）/
            ``prior``（组合方向与权重是否在**回测前**钉死）。仅当表达式是 2–3 条信号腿的
            多源组合时才需要；`weight_grid`（≥2 系数腿）与 `stack`（≥4 腿）**给不给都拦**。
            缺答时 `confirm_submit=True` 会被 Step 1.2 拦下（`force=True` 可豁免留痕）。
        _context: 执行上下文

    Returns:
        执行结果字典（含预检/提交/状态确认各步明细）

    2026-09-20 属性规范修复（详见 docs/alpha_properties_spec.md）：
      - 旧实现 `color="GREEN"` + `tags=["PowerPoolSelected"]` 会**无条件**把 PPA 通道标签
        与"健康"色打给**所有**提交（含普通 REGULAR），造成语义污染（审计实证）。
      - 现改为：color 默认 `BLUE`（待观察，GREEN 须由 OS 结果挣得）；
        tags 默认按规范自动生成，且**保留已有标签**（避免误清 `RETIRE_*` 等留痕）。
    """
    ctx = _context or {}
    store = ctx.get("store")
    # 注意：不再默认 ["PowerPoolSelected"] —— 那是 PPA 专有通道标识。
    # tags 的实际推导推迟到 Step 2（dry-run 短路之后）：_derive_tags 会读平台已有标签，
    # 必须遵守「dry-run 零副作用」契约（2026-09-20，曾被 test_submit_alpha_dry_run 抓到）。

    # dry-run：构建到提交流程计划即停，不触碰 network / 不写库
    # （2026-09-01 缺陷 A 修复：此前 dry_run 仍真实调用 get_alpha_details 等；
    #   2026-09-05 再修：连 brain_client 的解析都不做——解析本身会 import 依赖、
    #   可能建立连接，与「干跑零副作用」契约冲突，且会让调用方误以为已连通）。
    if ctx.get("dry_run"):
        return {
            "alpha_id": alpha_id,
            "success": True,
            "dry_run": True,
            "submitted": False,
            "note": "dry-run：请求计划已构建，未调用平台",
            "steps": [{
                "step": "plan_only",
                "success": True,
                "skipped": True,
                "note": "dry-run 不解析 brain_client，避免触碰网络与子进程",
            }],
            "plan": {
                "alpha_id": alpha_id,
                "name": name,
                "color": color,
                "tags": tags,
                "confirm_submit": confirm_submit,
                "force": force,
                "robustness_audited": robustness_audited,
                "verify_timeout": verify_timeout,
                "calls": (
                    ["get_alpha_details(alpha_id)",
                     "submit_gate(FAIL/硬闸WARNING/Failed RA·PPA/robustness台账REJECT，fail-closed)",
                     "mix_audit：混腿审查（≥2 系数腿 / ≥4 腿堆叠 ⇒ 结构硬拦；2–3 腿 ⇒ 必答三问）"
                     "＋按 checks 名判 ATOM(Last-2Y) 还是 LADDER，仅提示不阻断"]
                    + ([
                        "robustness_audited 声明（confirm_submit 时 fail-closed 必过；台账已有记录则降为辅助）",
                        "quota 闸：list stage=OS 数 ET 今日提交数，满 4/日 → blocked（fail-open）",
                        "prod 闸：check_correlation(production, refresh=False 缓存优先)，max≥0.7 或未出数 → blocked"
                        "（合规红线，2026-10-18 起无豁免入口）",
                    ] if confirm_submit else [])
                    + [
                        "边际贡献：performance_comparison(before-and-after 分区组合) → "
                        "ΔSharpe<0 硬闸阻断（2026-11-08 用户明令，force 不豁免；取数失败才 fail-open）",
                        "分散度：self≥0.55 且 ΔSharpe<+0.02 → 软闸阻断（force 可豁免）"
                        "—— 读 is.selfCorrelation，为空回落本地库缓存（不现算，避免拖长节点）",
                    ]
                    + ([
                        "set_alpha_properties(alpha_id, name/color/tags/descriptions)",
                        "POST /alphas/{id}/submit",
                        f"poll get_alpha_details until OS/ACTIVE (<= {verify_timeout}s)",
                        "若响应形态②/③（异步受理）且轮询未翻 ACTIVE：re-POST 补发一次再轮询（四态处置）",
                    ] if confirm_submit else [])
                ),
                "note": (
                    "confirm_submit=False：仅预检与查状态，不会 POST submit"
                    if not confirm_submit else
                    "confirm_submit=True：会真实提交——必须已有用户明确确认"
                ),
            },
        }

    # Step 0.2 全局禁提交闸（2026-10-05，用户指令）：「只挖不提交」——产出的 alpha 一律积攒，
    # 是否提交由用户决定。本工作区的**全局限制**，fail-closed 置于任何副作用之前：
    #   - 覆盖 `workflow_submit_alpha`（MCP 快捷入口）与 `workflow_execute(node="submit_alpha")`；
    #   - `force=True` 不豁免；`confirm_submit=False` 的预检/查状态不受影响。
    #   - 唯一放行：用户显式改 `wqb.config.ALLOW_ALPHA_SUBMIT=True`，或设 `WQB_ALLOW_ALPHA_SUBMIT=1`。
    if confirm_submit and not ALLOW_ALPHA_SUBMIT:
        result = {
            "alpha_id": alpha_id,
            "steps": [{
                "step": "global_submit_lock",
                "success": False,
                "skipped": False,
                "note": "全局禁提交开关 ALLOW_ALPHA_SUBMIT=False（只挖不提交，提交由用户决定）",
            }],
            "success": False,
            "submitted": False,
            "blocked": True,
            "reason": "global_submit_lock: ALLOW_ALPHA_SUBMIT=False",
            "blocked_reason": (
                "全局禁提交生效（2026-10-05 用户指令）：本工作区只挖不提交，产出的 alpha 一律积攒，"
                "是否提交由用户决定；force=True 不豁免本闸。需放行时由用户显式把 "
                "wqb.config.ALLOW_ALPHA_SUBMIT 置 True，或设环境变量 WQB_ALLOW_ALPHA_SUBMIT=1（仅当次进程）。"),
        }
        return _finalize(result, store, alpha_id)

    result: Dict[str, Any] = {
        "alpha_id": alpha_id,
        "steps": [],
        "success": False,
        "submitted": False,
    }

    client = _get_brain_client()

    # Step 1: fail-closed 提交前置闸（自动判定：模拟层 FAIL / 提交层硬闸 WARNING / Failed RA/PPA
    #   / robustness 台账 REJECT）
    # 2026-09-29 P0：把 brain-alpha-robustness 的 Phase B.0 硬门（WebDataScope Failed RA/PPA==0）
    # 与提交层四闸（LOW_SHARPE/LOW_FITNESS/LOW_2Y_SHARPE）焊进提交路由，替代旧的弱启发式
    # pre_submit_check（Sharpe 1.3 / Fitness 0.75 且预检失败 fail-open；2026-10-02 已物理删除）。
    # 2026-10-02 P0（F7）：闸内新增读 ``robustness_<alpha_id>`` 台账——REJECT → blocked，
    # 消除「判定层否决、动作层却放行」的两个入口口径分裂。
    precheck = _run_async(client.get_alpha_details(alpha_id))

    # Step 0: 已提交短路（P0，2026-10-27）——平台 status 非 UNSUBMITTED 时立即返回，
    # 不再走 submit_gate / quota_gate / prod_gate，更不 POST。
    # 实证：JjeMlmXA / 6Xdm3pXL 的 POST 实际已打穿平台（dateSubmitted 已写入），
    # 但 HTTP 响应在回程丢失，调用方看到 submitted=false 便重试；重试时 prod_gate
    # 撞上 correlation_busy 返回 blocked，把「已成功」误报成「被拒」，并白耗配额。
    # 平台口径：GET /alphas/{id}/submit 恒返 404，只能靠 status + dateSubmitted 复核。
    # 本次短路把该复核前移到第一个网络调用之后，彻底消除该类假阴性。
    _status = str((precheck or {}).get("status") or "").upper()
    if confirm_submit and _status and _status != "UNSUBMITTED":
        _dsub = (precheck or {}).get("dateSubmitted")
        result["steps"].append({
            "step": "already_submitted",
            "status": _status,
            "stage": (precheck or {}).get("stage"),
            "dateSubmitted": _dsub,
            "note": "平台已受理，跳过 submit_gate/quota_gate/prod_gate 与 POST（幂等短路）",
        })
        result["success"] = True
        result["already_submitted"] = True
        result["submitted"] = True      # 目标态已达成
        result["posted"] = False        # 但本次调用没有发 POST（区分重复计数）
        result["blocked"] = False
        result["final_status"] = _status
        result["dateSubmitted"] = _dsub
        result["reason"] = (
            f"already_submitted: status={_status}, stage={(precheck or {}).get('stage')}, "
            f"dateSubmitted={_dsub} → 未重复 POST（幂等）。若需补 name/color/tags，"
            "请单独调 set_alpha_properties。")
        return _finalize(result, store, alpha_id)

    gate = _submit_gate(precheck, alpha_id=alpha_id)
    result["steps"].append(gate)

    if gate.get("blocked") and not force:
        result["reason"] = "submit_gate blocked: " + "; ".join(gate.get("blocked_reasons") or [])
        result["blocked"] = True
        return _finalize(result, store, alpha_id)

    # Step 1.2: 混腿审查（2026-11-08，官方口径）——结构硬拦 + 三问 + ATOM/Ladder 路径提示。
    # 位置刻意放在所有**额外网络调用之前**：结构不合格的候选不该消耗 prod 探针槽与配额查询
    # （prod 端点并发有限，busy 时会白等）。纯函数，只读 precheck。
    # 阻断分两级：
    #   · weight_grid / stack ⇒ **force 不豁免**（结构上答不出经济含义，官方明确禁止）；
    #   · 2–3 腿缺三问 ⇒ 拦，但 `force=True` 可豁免并留痕（这是自设纪律，非平台规则）。
    # 预检（confirm_submit=False）只产出判定与预告，不阻断。
    mix = _mix_audit(precheck, narrative=mix_narrative)
    result["steps"].append(mix)
    if mix.get("available"):
        logger.info("[submit_alpha] 混腿审查 %s kind=%s legs=%d coef=%d path=%s%s",
                    alpha_id, mix.get("kind"), mix.get("legs") or 0,
                    mix.get("coef_legs") or 0, mix.get("path"),
                    "（结构硬拦）" if mix.get("blocked") else "")
        if mix.get("blocked"):
            if confirm_submit:
                result["reason"] = "mix_audit blocked: " + str(mix.get("block_reason") or "")
                result["blocked"] = True
                result["blocked_reason"] = (
                    "混腿结构硬拦（weight_grid/stack）：官方 Do Not「靠增删/拟合 parameters、"
                    "factors 提信号」，force 不豁免。出路：拆成单腿重挖，或改成 ≤3 腿且权重"
                    "由先验固定后重跑。")
                return _finalize(result, store, alpha_id)
            result["mix_warning"] = {
                "kind": mix.get("kind"), "reason": mix.get("block_reason"),
                "note": "预检已判定：confirm_submit=True 时将被 Step 1.2 拦下（force 不豁免）",
            }
        elif mix.get("narrative_required") and not mix.get("narrative_ok"):
            _miss = ",".join(mix.get("narrative_missing") or [])
            if confirm_submit and not force:
                result["reason"] = "mix_narrative missing: " + _miss
                result["blocked"] = True
                result["blocked_reason"] = (
                    "本颗是 %d 条信号腿的多源组合，须先答「三问」再提交（官方口径："
                    "跨源相加必须有 strong economic sense）。缺答：%s。请在 mix_narrative "
                    "里补齐（键：holders / polarity / prior，每条 ≥%d 字符）；"
                    "确已人工判定且要跳过时传 force=True（留痕）。"
                    % (mix.get("legs") or 0, _miss, mix.get("answer_min_len") or 8))
                return _finalize(result, store, alpha_id)
            if confirm_submit:
                logger.warning("[submit_alpha] %s 缺三问但 force=True 放行（缺：%s）",
                               alpha_id, _miss)
            result["mix_warning"] = {
                "kind": mix.get("kind"), "missing": mix.get("narrative_missing"),
                "note": ("预检已判定：缺三问，confirm_submit=True 时将被拦下（force 可豁免）"),
            }

    # Step 1.5: robustness 审计声明闸（confirm_submit=True 时 fail-closed）。
    # 2026-10-02：台账已有记录时本闸降为辅助——REJECT 已由 Step 1 拦下；PASS/CONDITIONAL
    # 的台账记录本身就是「审计已跑过」的更强证据，不再强制调用方重复声明。
    rob_record = gate.get("robustness") or {}
    rob_recorded = bool(rob_record.get("recorded"))
    if confirm_submit and not robustness_audited and not force and not rob_recorded:
        result["reason"] = "robustness audit not confirmed"
        result["blocked"] = True
        result["blocked_reason"] = (
            "提交前必须通过 brain-alpha-robustness 审计（Phase B/C 逐年 PnL 归因）并显式声明 "
            "robustness_audited=True（或让审计结论落 ledger `robustness_<alpha_id>`）；"
            "确已人工审计且要跳过时传 force=True（留痕）"
        )
        return _finalize(result, store, alpha_id)

    # Step 1.4: 配额闸（P0，2026-10-02，F9 修复）——REGULAR 提交前核对 ET 日历日配额。
    # 满额时前置拦截，不再靠 POST 后的 403 才发现（白跑一趟真请求、污染 attempt）。
    # fail-open：读不到 OS 池一律放行（平台 403 仍零成本兜底）。**force 不豁免**本闸。
    if confirm_submit and _alpha_type(precheck) != "SUPER":
        quota = _quota_gate(client, alpha_id)
        result["steps"].append({"step": "quota_gate", **quota})
        if not quota.get("allowed"):
            result["reason"] = "quota_gate blocked: " + str(quota.get("reason") or "")
            result["blocked"] = True
            result["blocked_reason"] = (
                "ET 今日 REGULAR 配额已满；等 ET 次日 00:00 重置后再提交（无需 force，force 也不豁免）。")
            return _finalize(result, store, alpha_id)

    # 2026-09-29（skills 审查 SP-13 / T0-4）：SUPER 的提交只走 `super_build.py submit`（或
    # `workflow_superalpha(confirm_submit=True)`，它内部调用同一入口）——那里有 prod ≥ 0.7 不提交的闸。
    # 2026-10-02：本节点现在也有 REGULAR/PPA 的 prod 闸（Step 1.6），但 SUPER 仍须走 super_build
    # （本闸不覆盖 SUPER 的 selection/combo 双闸与 naming 规范）。`force=True` 不豁免 prod 闸，
    # 对 SUPER 直接 confirm_submit=True 等于绕过用户铁律，且第一次通过的 POST 就是真提交。
    # 所以在任何副作用（改属性 / POST）之前拒绝，force 也不能放行。
    if confirm_submit and _alpha_type(precheck) == "SUPER":
        result["reason"] = "super_requires_super_build"
        result["blocked"] = True
        result["error"] = (
            "SUPER alpha 不得经本节点提交：请用 `python tools/super_build.py submit --alpha-id <ID>`"
            "（内置 prod 闸，max ≥ 0.7 或探针超时一律拒绝）或 `workflow_superalpha(confirm_submit=True)`；"
            "`force=True` 对 SUPER 无效。见 wq-brain-superalpha。")
        return _finalize(result, store, alpha_id)

    # Step 1.6: prod 闸（P0，2026-10-02，F8 修复）——REGULAR/PPA 提交前自动核对生产池相关性真值。
    # 用户铁律「prod ≥ 0.7 不得提交」此前只在 SUPER（super_build）有代码承载，REGULAR 侧纯靠
    # Agent 手动跑 check_correlation；本步把它焊进提交路由（与 super_build `_prod_gate_verdict` 同语义）。
    # **force 不豁免本闸**：probe 未出数（pending/busy/超时）一律 fail-closed。
    # ★★ 2026-10-18 收紧：原 `allow_prod_above_07` 显式豁免参数已**彻底移除**
    #    （用户明令该闸门不合规）。prod ≥ 0.7 是合规红线，不存在任何豁免入口，
    #    也不接受"平台 result 可能 PASS"作为放行理由。
    if confirm_submit:
        prod = _prod_gate(client, alpha_id)
        result["steps"].append({"step": "prod_gate", **prod})
        if not prod.get("allowed"):
            result["reason"] = "prod_gate blocked: " + str(prod.get("reason") or "")
            result["blocked"] = True
            result["blocked_reason"] = (
                "合规红线 prod ≥ 0.7 不得提交；或 prod 未出数（fail-closed）。"
                "无豁免入口，须更换候选或稍后重跑等平台算完。")
            return _finalize(result, store, alpha_id)

    # Step 1.7: 边际贡献闸（**2026-11-08 用户明令：ΔSharpe < 0 一律阻断，不准提交**）。
    # 沿革：2026-11-04 引入时为「信息项 / fail-open / 永不阻断」（理由见 _marginal_contribution
    # docstring 的四条）；2026-11-08 用户看过 bl6AvMkN 的 ΔS=−0.04 后明确指令
    # 「如果边际贡献为负你就阻断不准提交」⇒ 本步升为**否决闸**，与 prod 闸同级，
    # `force=True` 不豁免。
    # 唯一保留的 fail-open 面：`available=False`（取数失败 / 无分区归属）**不阻断** ——
    # 「ΔS 为负」与「ΔS 不可得」是两件事，端点故障不该把所有候选闷死。
    # 位置仍在 prod 闸之后、set_properties 之前：阻断发生在任何平台副作用之前。
    marginal = _marginal_contribution(client, alpha_id)
    result["steps"].append(marginal)
    if marginal.get("available"):
        _d_s = (marginal.get("delta") or {}).get("sharpe")
        logger.info(
            "[submit_alpha] 边际贡献 %s partition=%s ΔSharpe=%s%s",
            alpha_id, marginal.get("partition"), _d_s,
            "（稀释，阻断）" if marginal.get("dilutive") else "",
        )
        if marginal.get("dilutive"):
            result["marginal_warning"] = {
                "partition": marginal.get("partition"),
                "delta_sharpe": _d_s,
                "delta_drawdown": (marginal.get("delta") or {}).get("drawdown"),
                "note": (
                    "组合边际贡献为负（ΔSharpe < 0）⇒ **硬闸阻断**（用户 2026-11-08 明令）。"
                    "无豁免入口，force 不豁免。出路：换候选，或改结构使 ΔSharpe ≥ 0 后重跑。"
                ),
            }
            if confirm_submit:
                result["reason"] = (
                    "marginal_contribution blocked: ΔSharpe=%+.4f < 0 (partition=%s)"
                    % (_d_s if _d_s is not None else 0.0, marginal.get("partition")))
                result["blocked"] = True
                result["blocked_reason"] = (
                    "组合边际贡献为负（稀释）不得提交（用户 2026-11-08 铁律：ΔSharpe < 0 一律阻断）；"
                    "force 不豁免。换候选或改结构使 ΔSharpe ≥ 0 后重跑。")
                return _finalize(result, store, alpha_id)
            # 预检（confirm_submit=False）不阻断，但必须预告真提交会被拦
            logger.warning(
                "[submit_alpha] %s 边际贡献为负（ΔSharpe=%+.4f，partition=%s）——"
                "预检已判定：confirm_submit=True 时将被阻断",
                alpha_id, _d_s, marginal.get("partition"),
            )
    else:
        logger.info("[submit_alpha] 边际贡献不可用：%s（可用性缺失不阻断）",
                    marginal.get("note") or "unknown")

    # Step 1.8: 分散度审查（2026-11-08，自设纪律）——self 软线 0.55 + ΔS 补偿。
    # 依据：124 颗已提交 USA alpha 的真实 OS 实测显示**所有 IS 指标都不预测 OS**
    # （Sharpe ρ=+0.007 / Fitness +0.003 / margin +0.068 / two_year **−0.146**），
    # 唯一可动的是组合有效宽度 N/(1+(N-1)ρ̄)，它饱和于 1/ρ̄ ⇒ 降 ρ 远比增 N 有效。
    # 复用 Step 1.7 的 ΔS；self 复用 precheck 的 is.selfCorrelation，
    # **为空时回落本地库缓存**（未提交 alpha 该字段常为空；不现算，见函数 docstring）。
    # blocked 时 `force=True` 可豁免（自设纪律，非平台红线，与 Step 1.2 的三问同级）。
    diversity = _diversity_audit(client, alpha_id, precheck, marginal)
    result["steps"].append(diversity)
    if diversity.get("blocked"):
        logger.warning("[submit_alpha] 分散度 %s self=%s ΔS=%s（%s）——软闸",
                       alpha_id, diversity.get("self_corr"),
                       diversity.get("delta_sharpe"), diversity.get("block_reason"))
        result["diversity_warning"] = {
            "level": diversity.get("level"),
            "self_corr": diversity.get("self_corr"),
            "delta_sharpe": diversity.get("delta_sharpe"),
            "note": ("与池内已有 alpha 高度重复且边际贡献落在噪声带 ⇒ 预检已判定："
                     "confirm_submit=True 时将被 Step 1.8 拦下（force=True 可豁免留痕）。"
                     "换一颗更独立的候选，或证明 ΔS 更高。"),
        }
        if confirm_submit and not force:
            result["reason"] = "diversity_gate blocked: " + str(diversity.get("block_reason") or "")
            result["blocked"] = True
            result["blocked_reason"] = (
                "分散度软闸：与池内已有 alpha 的 self 相关 ≥ %.2f，而 ΔSharpe < %.2f"
                "（边际贡献落在估计噪声内）。CAP 的有效宽度饱和于 1/ρ̄，重复候选不抬组合。"
                "出路：换更独立的候选／降低相关结构／或确已人工判定时传 force=True（留痕）。"
                % (_DENSITY_SELF_SOFT, _DENSITY_DELTA_MIN))
            return _finalize(result, store, alpha_id)
    elif diversity.get("available"):
        logger.info("[submit_alpha] 分散度 %s level=%s self=%s ΔS=%s",
                    alpha_id, diversity.get("level"),
                    diversity.get("self_corr"), diversity.get("delta_sharpe"))

    # Step 2: 设置属性（仅在实际提交前做，避免空改）
    if confirm_submit:
        # tags 未显式给出 → 按规范自动生成（此处才可触碰网络：dry-run 已在上面短路）
        if tags is None:
            tags = _derive_tags(alpha_id, dataset, wave, expr_family, channel)

        # name 未显式给出 → 按 `build_name` 规范生成（2026-10-05 补：此前 REGULAR
        # 链路上 build_name 零调用，name 完全由调用方自由填写/ 保留临时名）。
        # region 取不到时**不生成**，保留平台现值（宁缺勿编）。
        _name_info = _derive_name(name, precheck, dataset=dataset, wave=wave,
                                  expr_family=expr_family, channel=channel)
        _name = _name_info.get("name")

        # check_tags 只告警不阻断（P1-3 补：此前该函数除审计 CLI 外零调用，
        # 规范里的告警等于死代码）。写进步骤结果便于事后核对。
        _tag_warnings = []
        try:
            from ...alpha_properties import check_tags as _check_tags
        except Exception:  # pragma: no cover
            try:
                from wqb.alpha_properties import check_tags as _check_tags  # type: ignore
            except Exception:
                _check_tags = None
        if _check_tags is not None:
            try:
                _tag_warnings = list(_check_tags(tags or []))
            except Exception as e:  # noqa: BLE001
                _tag_warnings = [f"check_tags 调用失败（{e}）"]
        if _tag_warnings:
            logger.warning("[submit_alpha] tags 规范告警: %s", _tag_warnings)
        # color 默认 BLUE（待观察）；GREEN 须由 OS 结果挣得，禁当默认值（2026-09-20 规范）
        _color = color
        if _color is None:
            try:
                from ...alpha_properties import COLOR_PENDING  # noqa: WPS433
            except Exception:  # pragma: no cover
                try:
                    from wqb.alpha_properties import COLOR_PENDING  # type: ignore
                except Exception:
                    COLOR_PENDING = "BLUE"
            _color = COLOR_PENDING
        # name / descriptions 未显式给出 → **保留平台已有值**（2026-09-21 事故：此前把 None
        # 原样传给客户端，客户端无条件 PATCH name=null / regular.description=null，
        # gJboYLRl 提交前刚设好的名称与描述被清空）。客户端现已只发非 None 字段，这里再
        # 显式回读一次，把"保留了什么"写进步骤结果，便于事后核对。
        preserved = _preserved_properties(precheck, name=name, descriptions=descriptions)
        props = _run_async(client.set_alpha_properties(
            alpha_id, name=_name, color=_color, tags=tags, descriptions=descriptions))
        result["steps"].append({
            "step": "set_properties",
            "success": not isinstance(props, dict) or not props.get("__error__"),
            "preserved": preserved,
            "name_derived": _name_info,
            "tag_warnings": _tag_warnings,
            "result": props,
        })
    else:
        result["steps"].append({
            "step": "set_properties",
            "success": True,
            "skipped": True,
            "note": "confirm_submit=False，跳过属性设置",
        })

    # Step 3: 提交（敏感决策，需 confirm_submit=True）
    submit_state = None
    if confirm_submit:
        submit = _run_async(client.submit_alpha(alpha_id))
        submit_state = _classify_submit_response(submit)
        # transport_error（fetch failed）= 结果未知，**不得**记成已提交（2026-10-27 P0）
        _accepted = submit_state in ("async_accepted", "unknown_accept")
        result["steps"].append({
            "step": "submit",
            "success": bool(isinstance(submit, dict) and submit.get("success")) or _accepted,
            "response_state": submit_state,   # ①confirmed / ②async_accepted / ③unknown_accept / ④rejected / ⑤transport_error
            "result": submit,
        })
        result["submitted"] = (bool(isinstance(submit, dict) and submit.get("success"))
                               or _accepted)

        # Step 3.5: 传输层错误 → 先回查平台再决定补发（铁律「报错≠动作未发生」）
        if submit_state == "transport_error":
            recheck = _post_outcome_recheck(client, alpha_id)
            result["steps"].append({
                "step": "post_transport_recheck",
                "success": bool(recheck.get("landed")),
                "landed": bool(recheck.get("landed")),
                "status": recheck.get("status"),
                "date_submitted": recheck.get("date_submitted"),
                "detail": recheck.get("detail"),
                "note": ("POST 响应为传输层错误（无响应体）：按「报错≠动作未发生」回查"
                         "status/dateSubmitted。已落地即视为提交成功、不再补发。"),
            })
            if recheck.get("landed"):
                result["submitted"] = True
                result["submitted_via"] = "transport_error_recheck"
    else:
        result["steps"].append({
            "step": "submit",
            "success": True,
            "skipped": True,
            "note": "confirm_submit=False，未真正提交（仅预检）",
        })
        # 未提交时：返回当前状态即结束
        status = _current_status(client, alpha_id)
        result["final_status"] = status
        result["success"] = True
        return _finalize(result, store, alpha_id, client=client)

    # Step 4: 提交后状态确认（四态处置，worldquant-submit-alpha「关键坑①」）：
    # ② 201/202「Accepted (async)」与 ③ 空体「Non-JSON submit response」都是**异步受理、
    # 结果未知**——客户端只等 60s 就放弃，轮询到点仍非 ACTIVE 时必须 re-POST 补发一次
    # （幂等），否则候选悬空（2026-09-26 实证：O0GjWqeY / 2rpX85Ax / np8VGNz3 悬空 >24h）。
    final_status = _poll_status(client, alpha_id, verify_timeout)
    result["steps"].append({
        "step": "verify",
        "success": final_status in ("ACTIVE", "SUBMITTED"),
        "status": final_status,
    })
    resubmitted = False
    if final_status not in ("ACTIVE", "SUBMITTED") and submit_state in (
            "async_accepted", "unknown_accept", "transport_error"):
        resub = _run_async(client.submit_alpha(alpha_id))
        resubmitted = True
        result["steps"].append({
            "step": "async_resubmit",
            "success": True,
            "response_state": _classify_submit_response(resub),
            "result": resub,
            "note": ("响应形态②/③/⑤（异步受理或传输错误）且轮询未翻 ACTIVE，"
                     "按 SOP re-POST 补发一次（幂等）"),
        })
        final_status = _poll_status(client, alpha_id, verify_timeout)
        result["steps"].append({
            "step": "verify_after_resubmit",
            "success": final_status in ("ACTIVE", "SUBMITTED"),
            "status": final_status,
            "note": "补发后仍非 ACTIVE 才记 ASYNC_STUCK 并知会用户",
        })
    result["resubmitted"] = resubmitted
    result["final_status"] = final_status
    result["success"] = final_status in ("ACTIVE", "SUBMITTED")
    if not result["success"] and resubmitted:
        result["async_stuck"] = True

    # Step 5: prod 快照恒等式（信息项，不阻断）——闸门读的数 == 平台冻结的数？
    # 只在真提交成功时做：预检路径没有 POST，冻结值尚未产生，比对无意义。
    if result["success"]:
        snap = _prod_snapshot_check(client, alpha_id, result["steps"])
        result["steps"].append(snap)
        if snap.get("available") and not snap.get("matches"):
            result["prod_snapshot_warning"] = {
                "gate_value": snap.get("gate_value"),
                "recorded_value": snap.get("recorded_value"),
                "delta": snap.get("delta"),
                "note": ("闸门读数与平台冻结值不一致。提交已 ACTIVE 无法回退，"
                         "须排查是否缓存过期或并发槽混淆；该颗的 prod 判定应以 "
                         "recorded_value 为准并补记账。"),
            }
            logger.warning(
                "[submit_alpha] prod 快照不一致 %s：闸门 %.4f vs 平台 %.4f（Δ%+.4f）",
                alpha_id, snap.get("gate_value") or 0.0,
                snap.get("recorded_value") or 0.0, snap.get("delta") or 0.0,
            )

    return _finalize(result, store, alpha_id, client=client)


def _alpha_type(details: Any) -> str:
    """alpha 详情里的 type（REGULAR / SUPER / …），缺失或异常返回空串。"""
    if not isinstance(details, dict):
        return ""
    return str(details.get("type") or "").strip().upper()


def _is_ppa_alpha(details: Any) -> bool:
    """PPA 判定：type==PPA **或** 带 PowerPoolSelected 标签。

    2026-10-02 P1（F10b）：与 :func:`wqb.submit_verdict_core.is_ppa_alpha` 统一口径。
    此前本节点只认 `type == "PPA"`，会把 ``{type: REGULAR, tags: [PowerPoolSelected]}``
    误判成 REGULAR，去比对 RA 计数组 —— 提交闸与判定层对同一 alpha 给出不同结论。
    延迟 import 判定层实现（单一实现来源），import 失败时退化为本地 type 判定。
    """
    try:
        from ...submit_verdict_core import is_ppa_alpha as _core_is_ppa
        return _core_is_ppa(details if isinstance(details, dict) else {})
    except Exception:  # pragma: no cover - 兜底
        if not isinstance(details, dict):
            return False
        if str(details.get("type") or "").upper() == "PPA":
            return True
        return any("PowerPoolSelected" in str(t) for t in (details.get("tags") or []))


def _classify_submit_response(submit: Any) -> str:
    """把 POST /alphas/{id}/submit 的响应归入五态（worldquant-submit-alpha「关键坑①」）.

    ① confirmed：success + 「IS checks passed」（明确通过）；
    ② async_accepted：201/202「Accepted (async); IS checks still computing」（异步受理）；
    ③ unknown_accept：「Non-JSON submit response」/空体（异步受理、结果未知）；
    ④ rejected：403 + failing IS checks（明确失败，零成本带回真因）。
    ⑤ transport_error：``{"__error__": ...}``——**请求根本没拿到响应**（fetch failed /
    超时 / 连接重置）。2026-10-27 P0 补：此前该形态落到 unknown_accept，被当成
    「异步受理、已提交」→ 先谎报 submitted=True，再空轮询 240s，最后才补发。
    语义上它是「结果未知，须回查平台」，与异步受理的处置完全不同。

    对客户端返回形态做宽松识别（status_code / http_status / reason / detail 文本）。
    """
    if not isinstance(submit, dict):
        return "unknown_accept"
    # ⚠ 必须放在最前：run_async 把异常包成 {"__error__": "fetch failed"}，没有
    # status_code / success / detail，会一路落到最后的 unknown_accept。
    if submit.get("__error__"):
        return "transport_error"
    code = submit.get("status_code") or submit.get("http_status") or submit.get("code")
    text = " ".join(str(submit.get(k) or "") for k in ("reason", "detail", "message", "error"))
    checks = submit.get("checks") or (submit.get("is") or {}).get("checks") or []
    if submit.get("success") and "checks passed" in text.lower():
        return "confirmed"
    if code in (201, 202) or "accepted" in text.lower():
        return "async_accepted"
    if checks and not submit.get("success") and code == 403:
        return "rejected"
    if submit.get("success"):
        return "confirmed"
    if not submit.get("success") and (not text.strip() or "non-json" in text.lower()):
        return "unknown_accept"
    return "unknown_accept" if not checks else "rejected"


def _extract_region(details: Any) -> Optional[str]:
    """从 get_alpha_details 返回提取 region（与 judge._extract_region 同口径）。

    brain_client 返回可能是 {"result": {...}} 或直接 {...}；region 在 settings.region。
    """
    if not isinstance(details, dict) or details.get("__error__"):
        return None
    d = details.get("result", details)
    if not isinstance(d, dict):
        return None
    settings = d.get("settings", {})
    if isinstance(settings, dict):
        region = settings.get("region")
        if region:
            return str(region).upper()
    region = d.get("region")
    return str(region).upper() if region else None


def _submit_gate(details: Any, *, alpha_id: Optional[str] = None,
                 robustness: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """fail-closed 提交前置闸（P0，2026-09-29；2026-10-02 增补 robustness 台账读取）。

    把 brain-alpha-robustness 的 Phase B.0 硬门（WebDataScope Failed RA/PPA==0）
    与提交层四闸（LOW_SHARPE/LOW_FITNESS/LOW_2Y_SHARPE 的模拟层 WARNING）焊进提交路由。
    默认纯函数（不触网）；仅当 `alpha_id` 非空 **且** `robustness` 未显式传入时，
    才尝试从 ledger 读 ``robustness_<alpha_id>``（只读、异常返回 None）。

    fail-closed 语义：**无法判定 = 阻断**（预检失败/无 is.checks 一律 blocked，
    不重蹈旧 pre_submit_check「预检异常即放行」的 fail-open 缺陷；旧方法已于 2026-10-02 删除）。

    阻断条件（任一即 blocked）：
      1. details 非 dict / 无 is.checks（回测未完成或预检失败）；
      2. 模拟层 checks 存在 result==FAIL；
      3. 模拟层 WARNING 含提交层硬闸项（提交时平台升级 FAIL）；
      4. Failed RA（REGULAR）或 Failed PPA（PPA）计数非零（Phase B.0 硬门）；
      5. **robustness 台账 ``REJECT``**（2026-10-02 P0）。

    第 5 条消除 F7 绕行：提交判定层（submit_verdict_core.decide）对 REJECT 明文否决，
    但此前动作层 `workflow_submit_alpha(confirm_submit=True, robustness_audited=True)`
    对同一证据放行 —— 两个入口给出相反结论。现在把台账读进本闸，两侧口径一致。
    `CONDITIONAL` / 无记录 → 只提示、不拦（与 decide 的 fail-open 边界一致）。
    """
    if not isinstance(details, dict):
        return {"step": "submit_gate", "passed": False, "blocked": True,
                "blocked_reasons": ["get_alpha_details 返回异常（非 dict），无法判定"]}

    is_ = details.get("is") or {}
    checks = is_.get("checks") or []
    if not checks:
        return {"step": "submit_gate", "passed": False, "blocked": True,
                "blocked_reasons": ["无 is.checks（回测未完成或预检失败），fail-closed 阻断"]}

    fails = [c for c in checks if str(c.get("result")) == "FAIL"]
    hard_warns = [c for c in checks
                  if str(c.get("result")) == "WARNING"
                  and c.get("name") in _SUBMIT_HARD_GATE_WARNINGS]
    counts = compute_webdata_failed_counts(checks)
    # 2026-10-02 P1（F10b）：与 submit_verdict_core.is_ppa_alpha 统一口径——
    # type==PPA **或** 带 PowerPoolSelected 标签都算 PPA。
    # ⚠ 2026-10-27 P0 修正：该口径会被平台**给 REGULAR 提交成功的 alpha 自动打的**
    # PowerPoolSelected 标签误导（JjeMlmXA 实证），而 PPA 名单是 RA 名单的子集 ⇒
    # 只看 failed_ppa 会漏掉 LOW_FITNESS / LOW_2Y_SHARPE / IS_LADDER_SHARPE 等纯 RA 项。
    # 判定改用 merge_failed_items（RA 为下界 ∪ 真 PPA 的额外项），is_ppa 仅保留
    # 「通道」语义供报告，不再决定是否拦截。
    is_ppa = _is_ppa_alpha(details)
    merged = merge_failed_items(counts, ppa_bonus=is_ppa)

    # 2026-10-02 P0（F7）：读 robustness 台账（显式传入优先，否则按 alpha_id 读库）。
    rob: Optional[Dict[str, Any]] = robustness
    if rob is None and alpha_id:
        try:
            from ...robustness_record import read_record as _read_rob
            rob = _read_rob(str(alpha_id), _extract_region(details))
        except Exception as e:  # noqa: BLE001 —— 读台账失败不能让提交闸崩溃
            logger.warning(f"读 robustness 台账失败（忽略）：{e}")
            rob = None
    rob_reject = bool(isinstance(rob, dict) and str(rob.get("verdict") or "").upper() == "REJECT")

    reasons: List[str] = []
    if fails:
        reasons.append(f"模拟层 {len(fails)} 项 FAIL："
                       f"{', '.join(str(c.get('name')) for c in fails)}")
    if hard_warns:
        reasons.append(
            "模拟层 WARNING 含提交层硬闸项（提交时平台升级 FAIL）："
            f"{', '.join(str(c.get('name')) for c in hard_warns)}")
    if rob_reject:
        failed_checks = rob.get("failed_checks") or []
        reasons.append("robustness 台账判定 REJECT（brain-alpha-robustness 否决）："
                       f"{', '.join(str(x) for x in failed_checks) or '(未列明细)'}")

    if merged["count"]:
        reasons.append(f"WebDataScope Failed RA={counts['failed_ra']} / PPA={counts['failed_ppa']}"
                       f"（Phase B.0 硬门非零，任一通道失败即拦）：{merged['names']}")

    blocked = bool(reasons)
    return {
        "step": "submit_gate",
        "passed": not blocked,
        "blocked": blocked,
        "blocked_reasons": reasons,
        "failed_ra": counts["failed_ra"],
        "failed_ppa": counts["failed_ppa"],
        "failed_any": merged["count"],
        "fails": fails,
        "hard_gate_warns": hard_warns,
        "is_ppa": is_ppa,
        # 通道 vs 仅标签（2026-10-27）：平台给 REGULAR 提交成功的 alpha 也打
        # PowerPoolSelected，事后盘点据此区分「真 PPA」与「自动标签」。
        "ppa_channel": _alpha_type(details) == "PPA",
        "ppa_tag_only": bool(is_ppa) and _alpha_type(details) != "PPA",
        "robustness": ({"recorded": True, "verdict": str(rob.get("verdict")).upper(),
                        "failed_checks": list(rob.get("failed_checks") or [])}
                       if isinstance(rob, dict) else {"recorded": False, "verdict": None}),
    }


#: 平台 9 项提交测试里唯一区分「单数据集 / 多数据集」的两项，**互斥出现**：
#:   ``LOW_2Y_SHARPE``    ⇒ 单数据集（ATOM）：不走 IS Ladder，只查 Last-2Y IS Sharpe ≥ 2.38
#:   ``IS_LADDER_SHARPE`` ⇒ 多数据集：走 Ladder，2Y 同样要 2.38，但可逐级退到 7Y 2.06 / 10Y 1.59
#: 依据：官方 Single Dataset Alphas 页 + 论坛 WH23488（266 条实测，37/37 对应，无同时出现者）
#: ＋本地抽样 5 颗逐颗吻合（RRE9NkVj/GrW9OxmG=LOW_2Y，zq3eb7No 等 5 颗=IS_LADDER）。
_ATOM_MARK = "LOW_2Y_SHARPE"
_LADDER_MARK = "IS_LADDER_SHARPE"

_MIX_LADDER_HINT = (
    "多数据集 ⇒ 走 **IS Ladder**：2Y 不足时可逐级降线到 7Y / 10Y 窗（官方示例线 2.38 → 7Y 2.06 → "
    "10Y 1.59，D1 换手<30% 再 ×0.85）⇒ 近 2 年偏弱不必然死。"
    "⚠ 实际线随 region/universe/delay 变（实测 DEU 侧 7Y 1.751 / FAIL 线 1.59），以该颗 "
    "IS_LADDER_SHARPE 的实判为准。")
_MIX_ATOM_HINT = (
    "单数据集（ATOM）⇒ **不走 Ladder**：只查 Last-2Y IS Sharpe，2Y 不足直接 FAIL、无退路。"
    "⚠ 线随 region/universe/delay 变（实测 GBR/TOP700/D1 的 2Y=1.98 可过；官方示例 2.38），"
    "以该颗 LOW_2Y_SHARPE 的实判为准。")

#: Step 1.8 分散度软线。平台硬线是 self<0.7（官方提交测试之一），但 0.7 只防「几乎同一颗」，
#: 不防「同类」。CAP ≈ (μ̄/σ̄)·sqrt(N/(1+(N-1)ρ̄))，有效宽度饱和于 1/ρ̄ ⇒ 降 ρ 比增 N 有效。
#: 取 0.55：READY 队列 183 颗的 self 分位 p50=0.394 / p75=0.505 / p90=0.656，
#: 0.55 命中 top 15–25%（真正重复的那批），不碰主体。
_DENSITY_SELF_SOFT = 0.55
#: 高相关候选须达到的最小 ΔSharpe。N≈266 时 ΔS 的估计噪声约 0.005–0.01，取 0.02 = 2–4 倍噪声。
_DENSITY_DELTA_MIN = 0.02


def _local_self_corr(alpha_id: str) -> Optional[float]:
    """读本地库里的既有 self 相关读数（零网络、毫秒级）。

    ★ 为什么读缓存而不是现算：`check_correlation(correlation_type="self")` 是**本地 OS 池
      计算**（要列全池 + 下载 PnL），实测拖长 12s 以上 —— 2026-11-08 端到端验证时直接把
      MCP 进程拖到被守护误判重启（日志：`marginal_contribution` 之后进程即被替换）。

    ★ 为什么缓存值可以用于判定：self 相关是「与池内单颗的**最大**相关」，
      而池只增不减 ⇒ **缓存值是保守下界**（真实值只会更高）。用它判定不会误伤，
      最坏情况是漏拦。
    """
    try:
        from ... import db_conn
        from ...store._common import default_db_path
        db = default_db_path()
    except Exception:  # pragma: no cover - 包路径退化
        return None
    try:
        conn = db_conn.connect(db, timeout=3, readonly=True)
    except Exception:  # pragma: no cover
        return None
    try:
        for sql in ("SELECT self_correlation FROM alphas WHERE alpha_id=?",
                    "SELECT self FROM submit_ready WHERE alpha_id=?"):
            try:
                row = conn.execute(sql, (alpha_id,)).fetchone()
            except sqlite3.Error:
                continue
            if row and row[0] is not None:
                return float(row[0])
    except Exception:  # pragma: no cover
        return None
    finally:
        conn.close()
    return None


def _diversity_audit(client, alpha_id: str, details: Any,
                     marginal: Dict[str, Any]) -> Dict[str, Any]:
    """Step 1.8 分散度审查（2026-11-08，**自设纪律，非平台规则**）。

    为什么加这一步。CAP = 等权组合的费后 Sharpe，数学上

        CAP ≈ (μ̄/σ̄) · sqrt( N / (1 + (N-1)·ρ̄) )

    起点是 2026-11-08 用 **124 颗已提交 USA alpha 的真实 OS 数据**做的实测，结论全部反直觉：

      · **所有 IS 读数对 OS 的秩相关都接近 0**：
        Sharpe +0.007｜Fitness +0.003｜margin +0.068｜sub_universe −0.057｜
        **two_year −0.146（反向）**
      · **只有 OS 能预测 OS**：ρ(os60, os125)=+0.564、ρ(os125, os全期)=+0.639
      · margin 对 −Turnover 的 ρ = **+0.922** ⇒ 它只是「低换手」的代理，不是独立信息
      · margin ≈ Returns/(504×Turnover)（逐颗验证误差 <1%）⇒ 定义上就是 Returns/TO 的函数
      · 数据集层面组间 R² = 0.010 ⇒ 「选对数据集」也没有可继承性

    ⇒ **换任何 IS 指标去筛选候选，都不会改善 CAP**。唯一能动的是有效宽度
      `N/(1+(N-1)ρ̄)`，而它在 N 大时饱和于 1/ρ̄：ρ̄=0.05、N=374 时有效宽度只有 19，
      再交 100 颗也只到 19.3。所以**降 ρ 比增 N 有效得多**。
      官方侧同一结论：Consultant FAQ「build diversity in your personal Alpha pool」；
      Brain Genius「formulating more pyramids can potentially improve both the Value
      Factor and Combined Alpha Performance through diversification」。

    为什么**不**用 margin 闸（同批实证的副产品）：READY 队列 183 颗里 margin<8bp 占 62%、
    <5bp 占 35%，设闸等于大面积误伤；而 margin 对 os125 的 ρ 仅 +0.068、不预测 OS。
    两边都不支持，故不设 —— 记在这里防止以后又「凭直觉补一道闸」。

    判定三级（`force=True` **可豁免**，因为这是自设纪律、不是平台红线）：
      · `self < 0.55`                     ⇒ `light`，放行
      · `self >= 0.55` 且 `ΔS >= +0.02`   ⇒ `dense_justified`，放行（用边际贡献补偿相关预算）
      · `self >= 0.55` 且 `ΔS <  +0.02`   ⇒ `blocked`
      · self 或 ΔS 读不到                  ⇒ `unknown`，**fail-open**
        （「无法判定」≠「判定不合格」，与 Step 1.7 的可用性口径一致）

    ★ 读数来源（2026-11-08 端到端验证后定案）：未提交 alpha 的 `is.selfCorrelation`
      **通常为空**（平台只在提交或主动检查后回填；实测 IND `786wl6b8` 预检时就是 null）。
      若直接 fail-open，本步对绝大多数候选等于不存在 ⇒ 为空时回落**本地库缓存**
      （`alphas.self_correlation` → `submit_ready.self`，见 `_local_self_corr`）。
      **不现算**：`check_correlation(self)` 是本地全池计算（列池 + 下载 PnL），
      实测拖长 12s+，直接把 MCP 进程拖到被守护误判重启。
      缓存值可用的理由：self 是「与池内单颗的**最大**相关」，池只增不减 ⇒
      **缓存值是保守下界**，用它判定不会误伤，最坏只是漏拦。
      `self_source` 标明来源（`platform` / `local_cache`）。

    ★ 已知局限：`is.selfCorrelation` 是「与池内单颗的最大相关」，不是组合平均两两相关 ρ̄。
      它偏保守（max ≥ 平均），所以用它当阈值只会**少拦**、不会多拦。
    """
    out: Dict[str, Any] = {"step": "diversity_audit", "available": False}
    self_corr = None
    self_source = None
    if isinstance(details, dict):
        raw = ((details.get("is") or {}).get("selfCorrelation"))
        try:
            self_corr = None if raw is None else float(raw)
            self_source = None if self_corr is None else "platform"
        except (TypeError, ValueError):
            self_corr = None
    # 未提交 alpha 的 `is.selfCorrelation` 常为空（平台只在提交/主动检查后回填）。
    # 若就此 fail-open，本步对绝大多数候选等于不存在 ⇒ 回落本地库缓存（零网络）。
    # **不主动现算**：self 检查要列全池 + 下载 PnL，实测拖长 12s+，会拖垮 MCP 进程。
    if self_corr is None:
        v = _local_self_corr(alpha_id)
        if v is not None:
            self_corr = v
            self_source = "local_cache"
    d_s = None
    if isinstance(marginal, dict) and marginal.get("available"):
        try:
            v = (marginal.get("delta") or {}).get("sharpe")
            d_s = None if v is None else float(v)
        except (TypeError, ValueError):
            d_s = None

    out.update({
        "self_corr": self_corr,
        "self_source": self_source,
        "delta_sharpe": d_s,
        "soft_line": _DENSITY_SELF_SOFT,
        "delta_min": _DENSITY_DELTA_MIN,
        "platform_line": 0.7,
    })

    if self_corr is None:
        out["level"] = "unknown"
        out["note"] = ("平台未回填 is.selfCorrelation，本地库也无缓存读数 ⇒ 分散度不可判，"
                       "fail-open。提交前跑一次 check_self_correlation 可让下次命中缓存。")
        return out
    if self_corr < _DENSITY_SELF_SOFT:
        out.update({
            "available": True, "level": "light",
            # 与池内单颗最大相关为 ρ 时，该颗的有效宽度贡献约为 ρ=0 候选的 (1-ρ)。
            "width_share": round(1 - self_corr, 3),
            "note": (f"self={self_corr:.4f} < 软线 {_DENSITY_SELF_SOFT} ⇒ 分散度充足，"
                     f"有效宽度贡献约为全新候选的 {1 - self_corr:.0%}。"),
        })
        return out

    if d_s is None:
        out.update({
            "available": True, "level": "unknown",
            "width_share": round(1 - self_corr, 3),
            "note": (f"self={self_corr:.4f} ≥ 软线 {_DENSITY_SELF_SOFT}，但 ΔSharpe 不可得 ⇒ "
                     "无法判定是否有足够边际贡献补偿相关预算，fail-open。建议先查 prod/self 终验。"),
        })
        return out

    if d_s >= _DENSITY_DELTA_MIN:
        out.update({
            "available": True, "level": "dense_justified",
            "width_share": round(1 - self_corr, 3),
            "note": (f"self={self_corr:.4f} ≥ 软线，但 ΔSharpe={d_s:+.4f} ≥ {_DENSITY_DELTA_MIN} "
                     "⇒ 边际贡献足以补偿相关预算，放行。"),
        })
        return out

    out.update({
        "available": True, "level": "blocked", "blocked": True,
        "width_share": round(1 - self_corr, 3),
        "block_reason": (f"self={self_corr:.4f} ≥ {_DENSITY_SELF_SOFT} 且 ΔSharpe={d_s:+.4f} < "
                         f"{_DENSITY_DELTA_MIN}"),
        "note": (f"与池内已有 alpha 高度重复（self={self_corr:.4f}），而边际贡献 ΔSharpe="
                 f"{d_s:+.4f} 落在噪声带（<{_DENSITY_DELTA_MIN}）⇒ 它占用相关预算却证明不了"
                 "正贡献。CAP 的有效宽度饱和于 1/ρ̄，这类候选再多交也不抬组合。"),
    })
    return out


def _mix_audit(details: Any, *, narrative: Any = None) -> Dict[str, Any]:
    """Step 1.2：混腿审查 + ATOM/Ladder 路径判决（2026-11-08，依官方口径重写）。

    为什么必须有这一步：2026-11-08 审计发现**四层闸里只有一层查混信号，而那一层被绕过**——
      ① 发批预检 `preflight_expressions` 只查「字段是否存在 + VECTOR 包裹」；
      ② 波次装配 `gate.py` 闸5 严格，但直走 batch/multisim 派发就绕过；
      ③ 队列 `submit_queue.is_add_mix` 旧口径明文放行等权 add；
      ④ `submit_alpha` **从不检查**。
    结果：禁令（2026-09-13 路线 A）后提交 173 颗、违规 26 颗 = **15%**。
    本步把结构审查接到**提交路径**上，成为最后一道、也是唯一有强制力的关口。

    两级语义（依据官方 Consultant Dos and Don'ts 的 "without any strong economic sense"）：
      · **硬拦**（`weight_grid` / `stack`）：`force` **不豁免**。权重网格里的数字本身就是
        搜索自由度（0.4/0.6 与 0.5/0.5 回测可分辨），≥4 腿堆叠无法逐个说清信息持有者——
        两者都答不出「经济含义」，正是官方禁止的那类。
      · **需三问**（`two_leg` / `three_leg`）：官方**允许**有经济含义的跨源组合，
        但必须答出 holders / polarity / prior；缺答则拦（`force=True` 可豁免，留下显式痕迹）。

    ★ 附带产出 `path`（`ATOM:LAST_2Y` / `LADDER`）：平台 checks 名单里两项互斥，直接暴露
      平台把本颗归为哪一类 —— 这是**免费**的路径判决，用于提示「这颗近 2 年弱也没关系」
      还是「这颗 2Y 不足就真死」。信息项，不参与阻断判定。
    ★ fail-open 边界：读不到表达式 / submit_queue 不可导入 ⇒ `available=False` 且不拦。
      「无法审查」与「审查不通过」是两件事，导入故障不该把所有候选闷死（与 Step 1.7 同哲学）。
    """
    checks: List[Any] = []
    code = ""
    if isinstance(details, dict):
        code = str(((details.get("regular") or {}).get("code")) or "")
        checks = ((details.get("is") or {}).get("checks") or []) or []
    names = {str(c.get("name")) for c in checks if isinstance(c, dict)}
    if _LADDER_MARK in names:
        usage, path, hint = "MULTI_DATA_SET", "LADDER", _MIX_LADDER_HINT
    elif _ATOM_MARK in names:
        usage, path, hint = "SINGLE_DATA_SET", "ATOM:LAST_2Y", _MIX_ATOM_HINT
    else:
        usage, path = "UNKNOWN", "UNKNOWN"
        hint = "平台 checks 里既无 LOW_2Y_SHARPE 也无 IS_LADDER_SHARPE ⇒ 路径不可判（回测未完成？）"

    base = {"step": "mix_audit", "data_usage": usage, "path": path, "hint": hint}
    if not code:
        return {**base, "available": False,
                "note": "读不到 regular.code（非 REGULAR 通道或平台未回填），结构审查跳过"}

    try:
        from ...store import submit_queue as _sq
    except Exception:  # pragma: no cover - 包路径退化
        try:
            from wqb.store import submit_queue as _sq  # type: ignore
        except Exception:
            return {**base, "available": False,
                    "note": "submit_queue 不可导入，混腿审查跳过（fail-open）"}

    mr = _sq.mix_review(code, narrative)
    return {
        **base,
        "available": True,
        "expr": code[:160],
        "kind": mr["kind"],
        "legs": mr["legs"],
        "coef_legs": mr["coef_legs"],
        "blocked": mr["blocked"],
        "block_reason": mr["block_reason"],
        "narrative_required": mr["narrative_required"],
        "narrative_ok": mr["narrative_ok"],
        "narrative_missing": mr["narrative_missing"],
        "answer_min_len": _sq.MIX_ANSWER_MIN_LEN,
        "questions": dict(_sq.MIX_NARRATIVE_QUESTIONS),
    }


def _quota_gate(client, alpha_id: str, *, limit: int = None) -> Dict[str, Any]:
    """REGULAR 提交前配额闸（P0，2026-10-02，F9 修复）。

    此前提交路径**没有任何配额前置**：满额时唯一反馈是 POST 后的 403
    ``REGULAR_SUBMISSION(4/4)``——白跑一趟真 POST（虽不扣配额，但污染 attempt 记录、
    且要等到提交才发现）。本闸把 `wqb.quota` 的口径（唯一实现：
    list ``stage=OS`` 按 ``dateSubmitted`` 倒序，数 **当前 ET 日历日** 的 **REGULAR** 条目）
    前置到提交路由。

    **类型化计数（2026-10-05 修正）**：平台对 REGULAR(4/ET 日) 与 SUPER(1/ET 日) 是两条
    **独立**配额线。此前本闸把当日提交**总数**当 REGULAR 用量 ⇒ 混入 SUPER 会高估用量、
    在 REGULAR 仍有余额时**误拦**合法提交。现改用 ``probe_today()`` 只取
    ``regular_used``（判型优先读记录自带 ``type`` 字段）。

    fail-**open**（与 prod 闸的 fail-closed 不同）：无法判定（拉不到 OS 池）时**放行** ——
    配额是账务性前置，读不到绝不能变成新故障点；平台 403 仍是最终兜底（零成本）。

    返回 {allowed, used, limit, remaining, super_used, reason}。
    """
    lim = _REGULAR_QUOTA_LIMIT if limit is None else int(limit)
    try:
        r = _run_async(client.get_user_alphas(stage="OS", limit=100, offset=0,
                                              order="-dateSubmitted"))
        results = (r or {}).get("results") if isinstance(r, dict) else None
        if results is None:
            return {"allowed": True, "used": None, "limit": lim, "remaining": None,
                    "reason": "无法读取 OS 池（返回异常）→ fail-open 放行，由平台 403 兜底"}
        # 只数 REGULAR：平台对 REGULAR(4/ET 日) 与 SUPER(1/ET 日) 是**两条独立**配额线。
        # 2026-10-05 修正 —— 此前把当日提交总数当 REGULAR 用量，混入 SUPER 会**高估**用量，
        # 在 REGULAR 仍有余额时误拦合法提交（实测当日 4 颗中 1 颗为 SUPER，报 4/4 实为 3/4）。
        q = probe_today(results)
        used = q["regular_used"]
        super_used = q["super_used"]
    except Exception as e:  # noqa: BLE001 —— 读配额失败不能让提交路由崩溃
        return {"allowed": True, "used": None, "limit": lim, "remaining": None,
                "reason": f"配额检查异常（{e}）→ fail-open 放行，由平台 403 兜底"}

    remaining = max(0, lim - used)
    if used >= lim:
        return {"allowed": False, "used": used, "limit": lim, "remaining": 0,
                "super_used": super_used,
                "reason": (f"ET 今日 REGULAR 已用 {used}/{lim}，配额已满 → 提交必 403 "
                           "`REGULAR_SUBMISSION(value=4, limit=4)`；等 ET 次日 00:00 重置"
                           "（不扣配额但白跑 POST，故前置拦截）"
                           f"（SUPER 另计 {super_used}/1，两条线互不影响）")}
    return {"allowed": True, "used": used, "limit": lim, "remaining": remaining,
            "super_used": super_used,
            "reason": f"ET 今日 REGULAR {used}/{lim} → 剩余 {remaining}"}


def _prod_gate(client, alpha_id: str, *, threshold: float = None) -> Dict[str, Any]:
    """REGULAR 提交前 prod 闸（P0，2026-10-02）。

    F8 修复：此前 REGULAR 提交路径**完全没有** prod 闸（本节点旧注释明文写
    "本节点没有 prod 闸"），而 SUPER 经 `super_build.py` 有 —— 两条路径不对称，
    用户铁律「prod ≥ 0.7 不得提交」在 REGULAR 侧无代码承载。

    实现：调用 MCP 侧 `check_correlation(alpha_id, correlation_type="production",
    refresh=False)`（★ 2026-10-27 起缓存优先：48h 内有效缓存直接命中，
    过期/缺失才回源平台；`WQB_PROD_GATE_REFRESH=1` 可强制回源），读
    ``checks.production.max_correlation``：
      - max < threshold（默认 0.7）→ allowed；
      - max ≥ threshold → blocked；
      - 未出数（pending / busy / data_unavailable / 异常）→ blocked（fail-closed），
        等价 super_build `_probe_prod_max` 超时语义。
    ★ 2026-10-28 补：缓存未命中时 MCP 会先预读 alpha 详情里的 ``is.prodCorrelation``
    （``source=alpha_detail_cached``，``provisional=True``，测量时间不可知）。
    **预读值只许证伪、不许放行**：它 ≥ 阈值时直接 blocked；< 阈值时本函数补一次
    ``refresh=True`` 真重测再决定（一次提交只多花一个平台单并发槽），
    重测拿不到数仍 fail-closed。

    返回 {allowed, prod_max, threshold, status, from_cache, cached_at, provisional, reason}。
    **纯判定，不做 POST**。
    """
    thr = _PROD_THRESHOLD if threshold is None else float(threshold)

    # ★ 2026-10-27（用户要求「有值的话就不实时重算了」）：改为**缓存优先**。
    # 旧实现硬编码 refresh=True ⇒ 每次提交都绕过 ``wqb.db::alpha_corr_cache``
    # 的 48h 保鲜缓存，直接打平台单并发相关性队列；队列一忙就
    # correlation_busy / data_unavailable → fail-closed，即使库里已有完全
    # 有效的 prod 值也提不出去（10-27 JjeMlmXA 实测：非刷新查询立刻返回
    # 缓存 0.6658 通过，提交却因强制刷新被卡死）。
    # 现改为 refresh=False：MCP check_correlation 先读权威缓存
    # （``_prod_corr_cached``，>48h 或 stale 自动视为无缓存回源平台），
    # 有值直接用，无值才打平台。需要强制回源时设 WQB_PROD_GATE_REFRESH=1。
    # **合规语义完全不变**：prod ≥ 0.7 一律 blocked；拿不到值一律 fail-closed。
    force_refresh = (os.environ.get("WQB_PROD_GATE_REFRESH") or "").strip().lower() in (
        "1", "true", "yes", "on")

    def _call(refresh_flag: bool) -> Any:
        return _run_async(client.check_correlation(
            alpha_id, correlation_type="production", threshold=thr,
            refresh=refresh_flag))

    try:
        r = _call(force_refresh)
    except Exception as e:  # noqa: BLE001
        return {"allowed": False, "prod_max": None, "threshold": thr,
                "status": "error", "reason": f"check_correlation 异常：{e}"}

    if not isinstance(r, dict):
        return {"allowed": False, "prod_max": None, "threshold": thr,
                "status": "bad_response", "reason": "check_correlation 返回非 dict"}

    if r.get("__error__"):
        return {"allowed": False, "prod_max": None, "threshold": thr,
                "status": "error", "reason": f"check_correlation 调用失败：{r.get('__error__')}"}

    prod = ((r.get("checks") or {}).get("production") or {})

    # ★ 2026-10-28：**预读值只许证伪，不许放行**。
    # `source=alpha_detail_cached`（alpha 详情里的 is.prodCorrelation）是平台存储值，
    # 测量时间不可知 → check_correlation 会打 ``provisional=True``。它足以拒绝
    # （≥0.7 就是 ≥0.7，旧值也说明这颗与生产池高度重合），但不足以批准：拿「不知道
    # 多久以前算的」值过用户铁律的 0.7 闸，等于把闸变成摆设。
    # 因此仅在**即将放行**时补一次 refresh=True 真重测（只花一次账号级单并发槽，
    # 且一次提交只发生一次）；重测拿不到数仍 fail-closed。
    provisional = bool(prod.get("provisional")
                       or prod.get("source") == "alpha_detail_cached"
                       or r.get("provisional"))
    if (not force_refresh and provisional
            and prod.get("max_correlation") is not None):
        try:
            r2 = _call(True)
        except Exception as e:  # noqa: BLE001
            return {"allowed": False, "prod_max": None, "threshold": thr,
                    "status": "error", "provisional": True,
                    "reason": (f"prod 只有预读值（alpha_detail_cached），强制重测异常：{e}"
                               " → fail-closed")}
        if not isinstance(r2, dict) or r2.get("__error__"):
            return {"allowed": False, "prod_max": None, "threshold": thr,
                    "status": "error", "provisional": True,
                    "reason": ("prod 只有预读值（alpha_detail_cached），强制重测调用失败"
                               f"：{(r2 or {}).get('__error__') if isinstance(r2, dict) else r2!r}"
                               " → fail-closed")}
        r = r2
        prod = ((r.get("checks") or {}).get("production") or {})
        provisional = bool(prod.get("provisional"))

    raw_max = prod.get("max_correlation")
    status = str(prod.get("status") or r.get("status") or "ok")
    from_cache = bool(prod.get("from_cache") or r.get("from_cache"))
    cached_at = prod.get("cached_at") or r.get("cached_at")

    if raw_max is None:
        return {"allowed": False, "prod_max": None, "threshold": thr, "status": status,
                "from_cache": from_cache, "cached_at": cached_at,
                "provisional": provisional,
                "reason": (f"prod 未出数（status={status}，48h 内无缓存且平台单并发忙碌）"
                           "→ fail-closed 拒绝提交；稍后重跑或设 WQB_PROD_GATE_REFRESH=1 强制回源")}
    try:
        prod_max = float(raw_max)
    except (TypeError, ValueError):
        return {"allowed": False, "prod_max": None, "threshold": thr, "status": status,
                "from_cache": from_cache, "cached_at": cached_at,
                "provisional": provisional,
                "reason": f"prod max 非数值：{raw_max!r} → fail-closed"}

    src = f"缓存@{cached_at}" if from_cache else "平台实时"
    if prod_max >= thr:
        return {"allowed": False, "prod_max": prod_max, "threshold": thr, "status": status,
                "from_cache": from_cache, "cached_at": cached_at,
                "provisional": provisional,
                "reason": (f"prod max={prod_max} ≥ {thr} → 用户铁律 prod≥0.7 不得提交"
                           f"（{src}；即使平台提交层可能判 PASS）")}
    return {"allowed": True, "prod_max": prod_max, "threshold": thr, "status": status,
            "from_cache": from_cache, "cached_at": cached_at,
            "provisional": provisional,
            "reason": f"prod max={prod_max} < {thr} → 过闸（{src}）"}


def _prod_snapshot_check(client, alpha_id: str, steps: List[Dict[str, Any]],
                         *, tol: float = 0.005) -> Dict[str, Any]:
    """Step 5：prod 快照恒等式 —— **闸门读到的数，是否等于平台记下的数**。

    2026-11-08 新增。依据一条实测事实：``is.prodCorrelation`` 是**提交瞬间的冻结值**，
    永不随池变动（三颗逐位核对：kqN92KpK 0.6196 / bl6AvMkN 0.6470 / zq3eb7No 0.6171
    与各自提交时闸门读数完全相同）。因此提交后读它与 Step 1.6 的 ``prod_max`` 比对，
    是一次近乎免费的恒等式检查：

    - 相等 ⇒ 闸门没有被「缓存过期 / 并发槽返回他人结果 / 池在读与写之间变动」骗过；
    - 不等 ⇒ **闸门判定的数与平台实际记录的数不同源**。这是唯一能在当时发现该类事故的
      时机；否则要等到日后跑账户级审计才暴露，而那时已 ACTIVE 无从回退。

    ★ 信息项，**不阻断、不改 success**：提交已完成，此处只能告警留痕。
    与 ``tools/gates/prod_gate_audit.py`` 的分工必须分清——
    那个是**账户级事后审计**（400+ 请求、算历史泄漏率与口径校准）；
    本函数是**单颗在线恒等式**（1 请求、查这一次闸门是否诚实）。两者不可互替，
    也都不构成新的准入条件。
    """
    gate = next((s for s in steps if s.get("step") == "prod_gate"), None)
    if not gate or gate.get("prod_max") is None:
        return {"step": "prod_snapshot", "available": False,
                "note": "无 prod_gate 读数（SUPER/PPA 走 super_build，或闸门未取到数）"}
    gate_v = gate.get("prod_max")
    try:
        details = _run_async(client.get_alpha_details(alpha_id))
    except Exception as e:  # noqa: BLE001
        return {"step": "prod_snapshot", "available": False, "gate_value": gate_v,
                "note": f"读取失败：{type(e).__name__}: {e}"}
    # `run_async` 吞异常后返回 {"__error__": ...}，必须显式识别，否则会被误当成
    # 「平台尚未回填」——两者含义不同，混起来会掩盖接口故障。
    if isinstance(details, dict) and details.get("__error__"):
        return {"step": "prod_snapshot", "available": False, "gate_value": gate_v,
                "note": f"读取失败：{details['__error__']}"}
    recorded = ((details or {}).get("is") or {}).get("prodCorrelation") if isinstance(details, dict) else None
    if not isinstance(recorded, (int, float)):
        return {"step": "prod_snapshot", "available": False, "gate_value": gate_v,
                "note": "平台尚未回填 is.prodCorrelation（异步检查未落库）"}
    delta = float(recorded) - float(gate_v)
    return {"step": "prod_snapshot", "available": True,
            "gate_value": float(gate_v), "recorded_value": float(recorded),
            "delta": round(delta, 4), "tolerance": tol,
            "matches": abs(delta) <= tol,
            "note": ("闸门读数与平台冻结值一致，prod 闸诚实"
                     if abs(delta) <= tol else
                     "★ 闸门读数与平台冻结值不一致 ⇒ 闸门可能被缓存/池变动骗过，须查同源")}


def _marginal_contribution(client, alpha_id: str) -> Dict[str, Any]:
    """Step 1.7 边际贡献（``performance_comparison``）：候选叠加到所属**分区组合**前后的对比。

    平台端点 ``GET /users/self/alphas/{id}/before-and-after-performance``：
    ``before`` = 该分区已提交池的组合指标，``after`` = 把本候选**等权叠加**之后的组合指标。
    提交前即可调用（平台按 IS 期模拟），返回空体时带 ``Retry-After``（异步计算中，
    MCP 侧 ``_request_json_with_retries`` 自动重试；实测正常 0.8–1.0s，重试路径约 5s）。

    ★★ **2026-11-08 起为否决闸**：用户明令「如果边际贡献为负你就阻断不准提交」。
      `dilutive=True` 且 `confirm_submit=True` ⇒ `blocked=True` 并在 set_properties/POST
      之前 return（`force=True` 不豁免）。`confirm_submit=False` 的预检仍只产出数值 + 预告。

    以下是 2026-11-04 定案「纯信息项、永不阻断」时的四条理由，**现降级为遗留风险说明**
    （不再作为放行依据，但复议会用到，故原样保留）：
      ① **不在官方提交测试内**：`Consultant Submission Tests` 只有 9 项
         （fitness / sharpe / turnover / weight / sub-universe / self / prod / IS-ladder / bias），
         做成硬闸会拦掉本来能过的候选；
      ② **ΔS 的分母是「池子」不是「候选」**：before = 该分区已提交池的组合 Sharpe。
         同一颗合格候选，进强池（before S 3.04）易得低 ΔS、进弱池（1.73）易得高 ΔS
         ⇒ 用它做闸等于「池子越烂越容易过闸」，判定权错位；
         极端情形：S=1.6 的合格候选（过 1.58 闸线）进 S=3.0 的池子必为负 ΔS，
         但它是分散化来源 —— 硬闸会**系统性拒绝所有「合格但不突出」的新机制**；
      ③ **基准池随分区漂移**：实测同批两颗 DEU/D1 候选分属不同分区 ——
         `A1Vvqded`→`EQUITY:DEU:1`（before Sharpe 3.04）、
         `bl6OWZ2M`→`EQUITY:DEU:1:POWER_POOL`（before 1.73）
         ⇒ **跨 alpha 的 ΔS 不可直接比较**，不能拿来横向排序或设统一阈值；
      ④ **平台自己不当它是考核**：已提交（OS）alpha 调本端点**恒 400 Bad Request**
         （2026-11-04 实测 20/20 已提交跨 9 区全 400；未提交 3/3 全 200）
         ⇒ 端点的定位是「提交前预览」，提交后即不可查。若它是准入测试，平台不会把它删掉。
      ⚠ 触发升闸的实例：`bl6AvMkN`（DEU/TOP500）ΔSharpe=−0.04 于 2026-11-08 13:00 提交成功，
      用户随即裁定该口径不合用 ⇒ 改判硬闸。

    本账本口径：`dilutive = Δsharpe < 0` ⇒ **提交阻断**（`run()` Step 1.7）；
    空体 / 超时 / 异常一律 `available=False`（**可用性缺失不阻断** —— 与「为负」区分）。
    """
    out: Dict[str, Any] = {"step": "marginal_contribution", "success": True, "available": False}
    try:
        d = _run_async(client.performance_comparison(alpha_id))
    except Exception as e:  # noqa: BLE001 —— 信息项，任何异常都不影响提交
        out["note"] = f"调用异常（fail-open，不影响提交）：{e}"
        return out
    if not isinstance(d, dict):
        out["note"] = f"返回非 dict（{type(d).__name__}），fail-open"
        return out
    if d.get("__error__"):
        out["note"] = f"调用失败（fail-open）：{d.get('__error__')}"
        return out
    stats = d.get("stats") or {}
    b = stats.get("before") or {}
    a = stats.get("after") or {}
    if not b or not a:
        # 平台仍在算（空体已由 MCP 重试耗尽）或该 alpha 尚无分区归属
        out["note"] = "平台未返回 before/after（异步计算中或无分区归属），fail-open"
        return out

    def _num(x):
        try:
            return float(x)
        except (TypeError, ValueError):
            return None

    keys = ("sharpe", "fitness", "turnover", "returns", "drawdown")
    before = {k: _num(b.get(k)) for k in keys}
    after = {k: _num(a.get(k)) for k in keys}
    delta = {
        k: (None if before[k] is None or after[k] is None else round(after[k] - before[k], 6))
        for k in keys
    }
    d_s = delta.get("sharpe")
    out.update({
        "available": True,
        "partition": d.get("partitionName"),
        "before": before,
        "after": after,
        "delta": delta,
        "dilutive": bool(d_s is not None and d_s < 0),
        "risk_note": (
            None if d_s is None else
            (f"ΔSharpe={d_s:+.4f} ⇒ 组合稀释（**硬闸：提交阻断**，用户 2026-11-08 铁律）"
             if d_s < 0 else
             f"ΔSharpe={d_s:+.4f} ⇒ 组合分散（正向边际贡献）")
        ),
        "note": "ΔSharpe < 0 ⇒ 阻断提交（force 不豁免）；ΔS 仅在**同一分区**内可比",
    })
    return out


def _current_status(client, alpha_id: str) -> Optional[str]:
    """查询当前 alpha 状态（不轮询）。"""
    details = _run_async(client.get_alpha_details(alpha_id))
    if isinstance(details, dict) and not details.get("__error__"):
        return details.get("status")
    return None


def _post_outcome_recheck(client, alpha_id: str) -> Dict[str, Any]:
    """POST 之后**回查平台**判定动作是否真的落地（2026-10-27 P0）。

    项目铁律「提交类报错 ≠ 动作未发生」：``fetch failed`` / 连接重置时，POST 可能已经
    打穿平台，只是响应在回程丢了（2026-10-27 三颗 α 全中：当次都报 submitted=false，
    事后 ``status=ACTIVE`` + ``dateSubmitted`` 齐全）。所以传输层错误之后**必须先回查
    再决定是否补发**，否则重复 POST 只污染 attempt 记录、徒增混乱。

    返回 ``{"landed": bool, "status": str|None, "date_submitted": str|None, "detail": ...}``。
    """
    try:
        d = _run_async(client.get_alpha_details(alpha_id))
    except Exception as e:  # noqa: BLE001 —— 回查失败不能中断提交流程
        return {"landed": False, "status": None, "date_submitted": None,
                "detail": f"回查异常：{e}"}
    if not isinstance(d, dict) or d.get("__error__"):
        return {"landed": False, "status": None, "date_submitted": None,
                "detail": f"回查失败：{(d or {}).get('__error__') if isinstance(d, dict) else d!r}"}
    status = str(d.get("status") or "").upper() or None
    date_submitted = d.get("dateSubmitted") or d.get("date_submitted")
    landed = bool(date_submitted) or status in ("ACTIVE", "SUBMITTED")
    return {"landed": landed, "status": status, "date_submitted": date_submitted, "detail": None}


def _poll_status(client, alpha_id: str, timeout: int) -> Optional[str]:
    """轮询 alpha 状态直到脱离 UNSUBMITTED 或超时。"""
    deadline = time.time() + timeout
    while time.time() < deadline:
        status = _current_status(client, alpha_id)
        if status and status != "UNSUBMITTED":
            return status
        time.sleep(_POLL_INTERVAL_SEC)
    return None


def _retire_queue(alpha_id: str, status: str = "SUBMITTED") -> int:
    """提交成功后把该 alpha 从待提交队列退役（2026-09-20）。

    容错设计：队列记账失败**绝不能**影响提交流程本身，故全包在 try/except 内，
    失败只记 warning。
    """
    try:
        from ...store import submit_queue as _sq  # wqb.store.submit_queue
        n = _sq.retire(alpha_id, status=status)
        if n:
            logger.info(f"submit_queue: {alpha_id} → {status}（退役 {n} 条）")
        return n
    except Exception as e:  # noqa: BLE001
        logger.warning(f"submit_queue retire skipped for {alpha_id}: {e}")
        return 0


def _persist_submission_to_local(client, store, alpha_id: str, result: Dict[str, Any]) -> None:
    """提交成功后把平台真值落到本地：submission_ledger + alphas 表。

    ★ 修复（2026-11-03）：此前 _finalize 只写 WORKFLOW 台账 + 退役队列，从没调
      store.record_submission / store.upsert_alpha_from_platform —— 这俩正是「提交后落库」
      的唯一写法（upsert_alpha_from_platform 文档原话：提交脚本在 ACTIVE 后调用本方法）。
      结果：MCP 提交成功后，submission_ledger 没记录、alphas.date_submitted/stage/
      platform_status 全不更新 ⇒ 面板「今日提交 Alpha 明细」恒空（本地无感知）。

    做法：回查平台 get_alpha_details 拿权威真值（真 dateSubmitted/status/stage/region/
    type/expression），只填**非空键**交给 store（_write_alpha_row 是合并语义：d 里 None 的
    键不动本地已有好值，故缺字段安全）。全程容错——落库失败只告警，绝不影响提交已成功的事实。
    """
    if not store:
        return
    try:
        d = _run_async(client.get_alpha_details(alpha_id))
    except Exception as e:  # noqa: BLE001
        logger.warning("[submit_alpha] 提交后落库：回查平台失败（不影响提交成功）: %s", e)
        return
    if not isinstance(d, dict) or d.get("__error__"):
        logger.warning("[submit_alpha] 提交后落库：平台未返回有效详情（不影响提交成功）")
        return

    status = str(d.get("status") or "").upper() or None
    date_submitted = d.get("dateSubmitted") or d.get("date_submitted")
    settings = d.get("settings") or {}
    region = settings.get("region") or d.get("region")

    # ① submission_ledger（审计/配额口径来源之一）。submitted_at 用平台真值 dateSubmitted，
    #    与「今日提交」按平台 ET 日历日切齐；平台没给才退 now()（upsert_submission 兜底）。
    #    ★ 走 upsert_submission 而非 record_submission——后者不透传 submitted_at，会丢平台真值。
    try:
        store.upsert_submission(
            alpha_id=alpha_id,
            region=region,
            submission_type="REGULAR",
            status=status or "ACTIVE",
            submitted_at=date_submitted,
        )
    except Exception as e:  # noqa: BLE001
        logger.warning("[submit_alpha] 写 submission_ledger 失败（不影响提交成功）: %s", e)

    # ② alphas 表（面板①「今日提交」靠 alphas.date_submitted 判窗口）。只填非空键。
    payload = {"alpha_id": alpha_id}
    if region:
        payload["region"] = region
    if d.get("stage"):
        payload["stage"] = d.get("stage")
    if status:
        payload["platform_status"] = status
    if date_submitted:
        payload["date_submitted"] = date_submitted
    atype = d.get("type") or d.get("alpha_type")
    if atype:
        payload["alpha_type"] = atype
    reg = d.get("regular")
    expr = reg.get("code") if isinstance(reg, dict) else d.get("expression")
    if expr:
        payload["expression"] = expr
    try:
        store.upsert_alpha_from_platform(payload)
    except Exception as e:  # noqa: BLE001
        logger.warning("[submit_alpha] 回写 alphas 表失败（不影响提交成功）: %s", e)


def _finalize(result: Dict[str, Any], store, alpha_id: str,
              client: Any = None) -> Dict[str, Any]:
    """保存提交记录到台账并返回（容错与告警由 persist_workflow_record 承担）。"""
    persist_workflow_record(store, "submit", alpha_id, {
        "submitted_at": datetime.now().isoformat(),
        "submitted": result.get("submitted", False),
        "final_status": result.get("final_status"),
        "steps": result.get("steps"),
    })
    # 提交成功 → 落库到 submission_ledger + alphas 表（修复「本地无感知」，见 _persist_submission_to_local）
    if result.get("submitted") and result.get("success"):
        if client is not None:
            _persist_submission_to_local(client, store, alpha_id, result)
        # 退役出队（否则已提交项会永久滞留在待提交队列）
        _retire_queue(alpha_id, "SUBMITTED")
    return result
