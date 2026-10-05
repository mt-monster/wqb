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
import re
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from ...config import ALLOW_ALPHA_SUBMIT, WAIT_THRESHOLDS
from .._common import (
    get_brain_client as _get_brain_client,
    persist_workflow_record,
    run_async as _run_async,
)
from ...config import compute_webdata_failed_counts
from ...quota import REGULAR_DAILY_LIMIT, probe_today

logger = logging.getLogger(__name__)

#: 异步受理后等状态翻转的窗口（秒）——唯一来源 wqb.config.WAIT_THRESHOLDS（2026-09-29：180 → 240）
_FLIP_WAIT_S = int(WAIT_THRESHOLDS["submit_flip_wait_s"])

_POLL_INTERVAL_SEC = int(WAIT_THRESHOLDS["submit_flip_poll_s"])

# 提交层硬闸项：模拟层 WARNING 但提交层 FAIL 的检查名（与 tools/submit_verdict.py 同口径）。
# 2026-09-29 P0：这些 WARNING 在 POST submit 时平台会重新评估为 FAIL，必须在本地 fail-closed 拦截。
_SUBMIT_HARD_GATE_WARNINGS = {"LOW_FITNESS", "LOW_SHARPE", "LOW_2Y_SHARPE"}

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
    allow_prod_above_07: bool = False,
    confirm_submit: bool = False,
    verify_timeout: int = _FLIP_WAIT_S,
    dataset: Optional[str] = None,
    wave: Optional[str] = None,
    expr_family: Optional[str] = None,
    channel: Optional[str] = None,
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
            **不豁免 prod 闸**（见 allow_prod_above_07）——prod 是用户铁律，与预检分离。
        robustness_audited: 是否已通过 brain-alpha-robustness 审计（Phase B/C 逐年归因）。
            **fail-closed（2026-09-29 P0）**：confirm_submit=True 时必须为 True，
            否则拒绝提交（除非 force）。robustness 的 Phase B.0 硬门（Failed RA/PPA==0）
            已由 submit_gate 自动判定，此参数补齐无法自动的逐年归因部分。
            **2026-10-02**：若 ledger 已有 ``robustness_<alpha_id>`` 记录（agent 已跑过审计
            并落库），本声明闸降为辅助——不再强制重复声明；台账 ``REJECT`` 由 Step 1 直接拦下。
        allow_prod_above_07: 是否显式豁免 prod 闸（默认 False）。**不能由 force 隐式触发**：
            用户铁律「prod ≥ 0.7 不得提交」是必须显式留痕的红线。为 True 时才跳过
            Step 1.6 的 prod probe（与 super_build `--allow-prod-above-07` 同名同义）。
            仅 REGULAR/PPA 走本闸；SUPER 在本节点被拒（走 super_build）。
        confirm_submit: 是否真正 POST submit（默认 False，只做预检+状态查询）
        verify_timeout: 提交后状态确认超时（秒）
        dataset: 来源数据集 → 自动生成 `SRC_<dataset>` 标签
        wave: 波次 → 自动生成 `W<wave>` 标签
        expr_family: 表达式族 → 自动生成 `EXPRFAM_<family>` 标签（防同族自相残杀）
        channel: 通道标签覆盖（默认按 type 推断 `CH_REG`/`CH_SUPER`）
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
                "allow_prod_above_07": allow_prod_above_07,
                "verify_timeout": verify_timeout,
                "calls": (
                    ["get_alpha_details(alpha_id)",
                     "submit_gate(FAIL/硬闸WARNING/Failed RA·PPA/robustness台账REJECT，fail-closed)"]
                    + ([
                        "robustness_audited 声明（confirm_submit 时 fail-closed 必过；台账已有记录则降为辅助）",
                        "quota 闸：list stage=OS 数 ET 今日提交数，满 4/日 → blocked（fail-open）",
                        ("prod 闸：check_correlation(production, refresh=True)，max≥0.7 或未出数 → blocked"
                         if not allow_prod_above_07 else
                         "prod 闸：allow_prod_above_07=True 显式豁免（留痕）"),
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
    gate = _submit_gate(precheck, alpha_id=alpha_id)
    result["steps"].append(gate)

    if gate.get("blocked") and not force:
        result["reason"] = "submit_gate blocked: " + "; ".join(gate.get("blocked_reasons") or [])
        result["blocked"] = True
        return _finalize(result, store, alpha_id)

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
    # **force 不豁免本闸**：probe 未出数（pending/busy/超时）一律 fail-closed；
    # 仅 `allow_prod_above_07=True` 显式豁免并留痕（Step 0 已在 dry-run plan 里列出）。
    if confirm_submit and not allow_prod_above_07:
        prod = _prod_gate(client, alpha_id)
        result["steps"].append({"step": "prod_gate", **prod})
        if not prod.get("allowed"):
            result["reason"] = "prod_gate blocked: " + str(prod.get("reason") or "")
            result["blocked"] = True
            result["blocked_reason"] = (
                "用户铁律 prod ≥ 0.7 不得提交；或 prod 未出数（fail-closed）。"
                "确要提交须显式传 allow_prod_above_07=True（留痕）。")
            return _finalize(result, store, alpha_id)
    elif confirm_submit and allow_prod_above_07:
        result["steps"].append({
            "step": "prod_gate", "skipped": True, "allowed": True,
            "note": "allow_prod_above_07=True 显式豁免 prod 闸（用户红线留痕）",
        })

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
        result["steps"].append({
            "step": "submit",
            "success": bool(isinstance(submit, dict) and submit.get("success"))
                       or submit_state in ("async_accepted", "unknown_accept"),
            "response_state": submit_state,   # ①confirmed / ②async_accepted / ③unknown_accept / ④rejected
            "result": submit,
        })
        result["submitted"] = (bool(isinstance(submit, dict) and submit.get("success"))
                               or submit_state in ("async_accepted", "unknown_accept"))
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
        return _finalize(result, store, alpha_id)

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
            "async_accepted", "unknown_accept"):
        resub = _run_async(client.submit_alpha(alpha_id))
        resubmitted = True
        result["steps"].append({
            "step": "async_resubmit",
            "success": True,
            "response_state": _classify_submit_response(resub),
            "result": resub,
            "note": "响应形态②/③=异步受理且轮询未翻 ACTIVE，按 SOP re-POST 补发一次（幂等）",
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

    return _finalize(result, store, alpha_id)


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
    """把 POST /alphas/{id}/submit 的响应归入四态（worldquant-submit-alpha「关键坑①」）.

    ① confirmed：success + 「IS checks passed」（明确通过）；
    ② async_accepted：201/202「Accepted (async); IS checks still computing」（异步受理）；
    ③ unknown_accept：「Non-JSON submit response」/空体（异步受理、结果未知）；
    ④ rejected：403 + failing IS checks（明确失败，零成本带回真因）。
    对客户端返回形态做宽松识别（status_code / http_status / reason / detail 文本）。
    """
    if not isinstance(submit, dict):
        return "unknown_accept"
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
    # type==PPA **或** 带 PowerPoolSelected 标签都算 PPA（此前只认 type，
    # 会把 {type:REGULAR, tags:[PowerPoolSelected]} 误判成 REGULAR 而看错计数组）。
    is_ppa = _is_ppa_alpha(details)

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

    failed = counts["failed_ppa"] if is_ppa else counts["failed_ra"]
    if failed:
        names = counts["ppa_failed_names"] if is_ppa else counts["ra_failed_names"]
        reasons.append(f"WebDataScope Failed {'PPA' if is_ppa else 'RA'} = {failed}"
                       f"（Phase B.0 硬门非零）：{names}")

    blocked = bool(reasons)
    return {
        "step": "submit_gate",
        "passed": not blocked,
        "blocked": blocked,
        "blocked_reasons": reasons,
        "failed_ra": counts["failed_ra"],
        "failed_ppa": counts["failed_ppa"],
        "fails": fails,
        "hard_gate_warns": hard_warns,
        "is_ppa": is_ppa,
        "robustness": ({"recorded": True, "verdict": str(rob.get("verdict")).upper(),
                        "failed_checks": list(rob.get("failed_checks") or [])}
                       if isinstance(rob, dict) else {"recorded": False, "verdict": None}),
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
    refresh=True)`（refresh=True 强制走平台、不吃 7 天缓存），读
    ``checks.production.max_correlation``：
      - max < threshold（默认 0.7）→ allowed；
      - max ≥ threshold → blocked；
      - 未出数（pending / busy / data_unavailable / 异常）→ blocked（fail-closed），
        等价 super_build `_probe_prod_max` 超时语义。

    返回 {allowed, prod_max, threshold, status, reason}。**纯判定，不做 POST**。
    """
    thr = _PROD_THRESHOLD if threshold is None else float(threshold)
    try:
        r = _run_async(client.check_correlation(
            alpha_id, correlation_type="production", threshold=thr, refresh=True))
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
    raw_max = prod.get("max_correlation")
    status = str(prod.get("status") or r.get("status") or "ok")

    if raw_max is None:
        return {"allowed": False, "prod_max": None, "threshold": thr, "status": status,
                "reason": (f"prod 未出数（status={status}，平台仍在算或单并发忙碌）→ fail-closed 拒绝提交；"
                           "稍后重跑 check_correlation(refresh=True)")}
    try:
        prod_max = float(raw_max)
    except (TypeError, ValueError):
        return {"allowed": False, "prod_max": None, "threshold": thr, "status": status,
                "reason": f"prod max 非数值：{raw_max!r} → fail-closed"}

    if prod_max >= thr:
        return {"allowed": False, "prod_max": prod_max, "threshold": thr, "status": status,
                "reason": (f"prod max={prod_max} ≥ {thr} → 用户铁律 prod≥0.7 不得提交"
                           "（即使平台提交层可能判 PASS）")}
    return {"allowed": True, "prod_max": prod_max, "threshold": thr, "status": status,
            "reason": f"prod max={prod_max} < {thr} → 过闸"}


def _current_status(client, alpha_id: str) -> Optional[str]:
    """查询当前 alpha 状态（不轮询）。"""
    details = _run_async(client.get_alpha_details(alpha_id))
    if isinstance(details, dict) and not details.get("__error__"):
        return details.get("status")
    return None


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


def _finalize(result: Dict[str, Any], store, alpha_id: str) -> Dict[str, Any]:
    """保存提交记录到台账并返回（容错与告警由 persist_workflow_record 承担）。"""
    persist_workflow_record(store, "submit", alpha_id, {
        "submitted_at": datetime.now().isoformat(),
        "submitted": result.get("submitted", False),
        "final_status": result.get("final_status"),
        "steps": result.get("steps"),
    })
    # 提交成功 → 退役出队（否则已提交项会永久滞留在待提交队列）
    if result.get("submitted") and result.get("success"):
        _retire_queue(alpha_id, "SUBMITTED")
    return result
