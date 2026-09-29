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
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from ...config import WAIT_THRESHOLDS
from .._common import (
    get_brain_client as _get_brain_client,
    persist_workflow_record,
    run_async as _run_async,
)

logger = logging.getLogger(__name__)

#: 异步受理后等状态翻转的窗口（秒）——唯一来源 wqb.config.WAIT_THRESHOLDS（2026-09-29：180 → 240）
_FLIP_WAIT_S = int(WAIT_THRESHOLDS["submit_flip_wait_s"])

_POLL_INTERVAL_SEC = int(WAIT_THRESHOLDS["submit_flip_poll_s"])


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


def run(
    alpha_id: str,
    name: Optional[str] = None,
    color: Optional[str] = None,
    tags: Optional[List[str]] = None,
    descriptions: Optional[str] = None,
    force: bool = False,
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
        force: 是否跳过本地预检（仅当 confirm_submit=True 时有意义）
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
                "verify_timeout": verify_timeout,
                "calls": (
                    ["get_alpha_details(alpha_id)", "pre_submit_check(alpha_id)"]
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

    result: Dict[str, Any] = {
        "alpha_id": alpha_id,
        "steps": [],
        "success": False,
        "submitted": False,
    }

    client = _get_brain_client()

    # Step 1: 预检（get_alpha_details + pre_submit_check）
    precheck = _run_async(client.get_alpha_details(alpha_id))
    check = _run_precheck(client, precheck)
    result["steps"].append(check)

    if check.get("blocked") and not force:
        result["reason"] = "pre_submit_check blocked"
        result["blocked"] = True
        return _finalize(result, store, alpha_id)

    # Step 2: 设置属性（仅在实际提交前做，避免空改）
    if confirm_submit:
        # tags 未显式给出 → 按规范自动生成（此处才可触碰网络：dry-run 已在上面短路）
        if tags is None:
            tags = _derive_tags(alpha_id, dataset, wave, expr_family, channel)
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
            alpha_id, name=name, color=_color, tags=tags, descriptions=descriptions))
        result["steps"].append({
            "step": "set_properties",
            "success": not isinstance(props, dict) or not props.get("__error__"),
            "preserved": preserved,
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


def _run_precheck(client, details: Dict[str, Any]) -> Dict[str, Any]:
    """包装 pre_submit_check（本地启发式），失败不抛异常。"""
    try:
        cr = client.pre_submit_check(details)
        return {
            "step": "pre_submit_check",
            "success": True,
            "passed": bool(cr.get("passed")),
            "blocked": not bool(cr.get("passed")),
            "check_result": cr,
        }
    except Exception as e:
        logger.warning(f"pre_submit_check failed: {e}")
        return {"step": "pre_submit_check", "success": False, "error": str(e),
                "blocked": False, "check_result": None}


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
