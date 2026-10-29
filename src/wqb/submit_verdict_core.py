# -*- coding: utf-8 -*-
"""wqb.submit_verdict_core — 提交层判定的唯一实现（纯函数，无 I/O，可离线单测）。

三个入口共用本模块，禁止各自复写判定口径：
  * CLI  ``tools/submit_verdict.py``
  * MCP  ``world-quant-brain-mcp/tools_ops.py::submit_verdict``
  * 批量 ``tools/batch_submit_verdict.py``

2026-09-29 整改（skills 审查 X-2 / T0-1）：此前 CLI 与 MCP 各抄一份、批量工具是第三份且缺
Failed-count 资格门；退出码 0 同时代表 SUBMITTABLE / UNVERIFIABLE / ALREADY_SUBMITTED，
以 ``$?==0`` 放行的脚本会把「提交层无信息」的 UNVERIFIABLE 当成可提交。

判定语义（**否决权威**：只能拦，不能放；放行还需「平台 prod<0.7 实测 + 用户明确确认」，均不在本模块内）：

  verdict            含义                                                          退出码
  SUBMITTABLE        模拟层干净 且 GET /submit=200。平台现状恒 404，仅作防御分支保留      0
  BLOCKED            模拟层 FAIL / 硬闸类 WARNING / Failed-count 非零 / 提交层 403 / 未知响应   1
  UNVERIFIABLE       模拟层干净，但 GET /submit 处女提交 404 ⇒ 提交层无信息；须另跑
                     check_correlation 确认 prod<0.7（缓存优先：48h 内有效缓存直接命中，
                     无缓存才回源平台）                                                  10
  ALREADY_SUBMITTED  已 ACTIVE/SUBMITTED（或有 dateSubmitted）；不做可提交判定；勿再 POST   11

退出码 2 = argparse 参数错误（Python 缺省）；未捕获异常 = 1（与 BLOCKED 同向：fail closed）。
现实中 SUBMITTABLE 不会出现（GET /submit 恒 404，见 worldquant-submit-alpha）；文档与上游
条件只能依赖 UNVERIFIABLE / BLOCKED / ALREADY_SUBMITTED 三态，不得写「等 SUBMITTABLE」。
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from .config import compute_webdata_failed_counts, merge_failed_items
from .robustness_record import normalize_record as _normalize_robustness

VERDICTS = ("SUBMITTABLE", "UNVERIFIABLE", "BLOCKED", "ALREADY_SUBMITTED")

#: 退出码契约（CLI 用；MCP 在返回体里带 ``exit_code`` 供调用方对照）
EXIT_CODES: Dict[str, int] = {
    "SUBMITTABLE": 0,
    "BLOCKED": 1,
    "UNVERIFIABLE": 10,
    "ALREADY_SUBMITTED": 11,
}

#: 模拟层显示 WARNING、提交层（POST）重新评估为 FAIL 的检查名（KOR PPA 2026-08-22 实锤）
#: 2Y 有两个载体（`RA_2Y_NAMES`）：平台按 alpha 代际只发 `LOW_2Y_SHARPE` 或 `IS_LADDER_SHARPE`
#: 之一，两者在提交层同义 ⇒ 两个名字都要认（2026-10-23 IND 实测）。
SUBMIT_HARD_GATE_WARNINGS = frozenset(
    {"LOW_FITNESS", "LOW_SHARPE", "LOW_2Y_SHARPE", "IS_LADDER_SHARPE"})

_ALREADY_STATUSES = ("ACTIVE", "SUBMITTED")

_NEXT_STEP_RELEASE = (
    "另跑 check_correlation(alpha_id) 确认 all_passed 且 prod<0.7（2026-10-27 起缓存优先："
    "48h 内有效缓存直接命中，无缓存才回源平台；只有预读值时不构成放行依据）；"
    "用户明确确认后才可 workflow_submit_alpha(confirm_submit=True)（不可逆）。"
)

_UNVERIFIABLE_NOTE = (
    "提交层返回 404（GET /alphas/{id}/submit 平台恒 404，该视图已定性为死端点），"
    "无法验证。模拟层无 FAIL/硬闸 WARNING/Failed-count，但 PROD_CORRELATION / "
    "SELF_CORRELATION 未经平台确认——放行条件 = 平台 prod<0.7 + 用户确认；"
    "提交前必须另跑 check_correlation(alpha_id) 并确认 all_passed"
    "（缓存优先，命中 48h 内权威缓存即算实测；无缓存才回源打平台单并发队列）。"
)


def is_already_submitted(detail: Dict[str, Any]) -> bool:
    """已提交 / 已落地：不再做可提交判定（此前对 ACTIVE 也报 BLOCKED，假阴性）。"""
    return detail.get("status") in _ALREADY_STATUSES or bool(detail.get("dateSubmitted"))


def is_ppa_alpha(detail: Dict[str, Any]) -> bool:
    """PPA 判定：type=PPA 或带 PowerPoolSelected 标签（CLI 旧实现漏了标签，与 MCP 不一致）。"""
    if str(detail.get("type") or "").upper() == "PPA":
        return True
    return any("PowerPoolSelected" in str(t) for t in (detail.get("tags") or []))


def normalize_submit_layer(status_code: Optional[int], body: Any) -> List[Dict[str, Any]]:
    """把 GET /alphas/{id}/submit 的响应体规整成 checks 列表（200: is.checks；403: checks/detail）。"""
    body = body if isinstance(body, dict) else {}
    if status_code == 200:
        return list((body.get("is") or {}).get("checks") or [])
    if status_code == 403:
        checks = body.get("checks") or body.get("detail") or []
        if isinstance(checks, str):
            checks = [checks]
        if isinstance(checks, list):
            return [{"name": c, "result": "FAIL"} if isinstance(c, str) else c for c in checks]
    return []


def _names(items: List[Dict[str, Any]]) -> List[str]:
    return [str(c.get("name")) for c in items]


def decide(
    alpha_id: str,
    detail: Dict[str, Any],
    submit_status: Optional[int] = None,
    submit_checks: Optional[List[Dict[str, Any]]] = None,
    robustness: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """按模拟层 + 提交层视图给出否决权威判定。

    ``detail`` = ``get_alpha_details`` 的返回；``submit_status`` = GET /submit 的 HTTP 状态
    （已提交者无需请求，传 None）；``submit_checks`` = :func:`normalize_submit_layer` 的结果；
    ``robustness`` = 台账 ``robustness_<alpha_id>`` 的记录（:func:`wqb.robustness_record.read_record`，
    2026-09-29 起）：``REJECT`` → BLOCKED；``CONDITIONAL`` / 无记录 → 只在 ``next_step`` 里提示、不拦。
    返回字典的键是 MCP ``submit_verdict`` 历史返回体的超集，另加 ``exit_code`` /
    ``reason_code`` / ``next_step``。
    """
    status = detail.get("status")
    is_ = detail.get("is") or {}
    sim_checks = is_.get("checks") or []
    fails = [c for c in sim_checks if c.get("result") == "FAIL"]
    warns = [c for c in sim_checks if c.get("result") == "WARNING"]
    submit_checks = submit_checks or []

    base: Dict[str, Any] = {
        "alpha_id": alpha_id,
        "alpha_status": status,
        "sim_fails": fails,
        "sim_warnings": warns,
    }

    if is_already_submitted(detail):
        _ppa_ch = str(detail.get("type") or "").strip().upper() == "PPA"
        _ppa = is_ppa_alpha(detail)
        base.update({
            "verdict": "ALREADY_SUBMITTED",
            "exit_code": EXIT_CODES["ALREADY_SUBMITTED"],
            "reason_code": "ALREADY_SUBMITTED",
            "verdict_note": (f"alpha 已提交/已落地（status={status}），不构成可提交判定对象；"
                             "请勿重复 POST submit（幂等但浪费配额/产生混乱）。"),
            "next_step": "不要再 POST submit；如需回写台账走 S6（wave_results upsert）。",
            "is_ppa": _ppa,
            "ppa_channel": _ppa_ch,
            "ppa_tag_only": _ppa and not _ppa_ch,
            "hard_gate_warnings": [], "submit_status": None, "submit_checks": [],
            "submit_layer_view": "not_queried", "prepost_unverifiable": False,
            "failed_ra": 0, "failed_ppa": 0, "failed_any": 0,
            "failed_ra_items": [], "failed_ppa_items": [], "failed_any_items": [],
        })
        return base

    # WebDataScope Failed-count 资格门（唯一实现 = wqb.config）
    # ⚠ 2026-10-27 P0：此前按 is_ppa 二选一取数（PPA 看 PPA、REGULAR 看 RA）。平台会给
    # **REGULAR 提交成功**的 alpha 自动打 PowerPoolSelected 标签 ⇒ is_ppa 被误判为 True
    # ⇒ 去看更小的 PPA 子集，LOW_FITNESS / LOW_2Y_SHARPE / IS_LADDER_SHARPE 等纯 RA 项的
    # 失败被整片漏掉，判定层可能对 Failed RA>0 的候选报 SUBMITTABLE。改为 RA 为下界
    # ∪ 真 PPA 的额外项（merge_failed_items），is_ppa 仅保留「通道」语义。
    is_ppa = is_ppa_alpha(detail)
    counts = compute_webdata_failed_counts(sim_checks)
    failed_ra, failed_ppa = counts["failed_ra"], counts["failed_ppa"]
    failed_ra_items, failed_ppa_items = counts["ra_items"], counts["ppa_items"]
    merged = merge_failed_items(counts, ppa_bonus=is_ppa)
    # 报告标签按**失败项的真实来源**给，而非按标签：失败项全部落在 RA 名单时，
    # 即使带 PowerPoolSelected（平台自动标签）也报 RA（2026-10-27 P0）。
    # 只有 PPA 专有规则命中的项（LOW_SHARPE 结果 PASS 但 value<1）才报 PPA。
    _ra_names = {str(it.get("name")) for it in failed_ra_items}
    _ppa_only = [it for it in merged["items"] if str(it.get("name")) not in _ra_names]
    kind = "PPA" if (is_ppa and _ppa_only) else "RA"
    failed_gate_items = merged["items"]
    failed_gate_ok = merged["count"] == 0
    # 名单内检查仍 PENDING：Failed==0 只表示「暂无失败」，不是「已通过」（skills 审查 RF-03）
    pending_names = list(dict.fromkeys(
        list(counts["ra_pending_names"]) + list(counts["ppa_pending_names"])))

    hard_gate_warns = [c for c in warns if c.get("name") in SUBMIT_HARD_GATE_WARNINGS]
    prepost_unverifiable = submit_status == 404 and status == "UNSUBMITTED"
    rob = _normalize_robustness(robustness) if robustness is not None else None
    rob_reject = bool(rob and rob["verdict"] == "REJECT")
    ok = (not fails and not hard_gate_warns and failed_gate_ok and not rob_reject
          and (submit_status == 200 or prepost_unverifiable))

    reasons: List[Tuple[str, List[str]]] = []
    if fails:
        reasons.append(("SIM_FAIL", _names(fails)))
    if not failed_gate_ok:
        reasons.append((f"FAILED_COUNT_{kind}", _names(failed_gate_items)))
    if hard_gate_warns:
        reasons.append(("SUBMIT_HARD_WARN", _names(hard_gate_warns)))
    if rob_reject:
        reasons.append(("ROBUSTNESS_REJECT", list(rob["failed_checks"])))
    if submit_status == 403:
        reasons.append(("SUBMIT_403", _names(submit_checks)))
    if submit_status == 404 and status != "UNSUBMITTED":
        # 平台状态不是 UNSUBMITTED 又没到 ACTIVE/SUBMITTED（如本地队列里的过时副本）：不是可提交对象
        reasons.append(("NOT_UNSUBMITTED", [str(status)]))
    if not ok and not reasons:
        reasons.append((f"UNKNOWN_HTTP_{submit_status}", []))

    pending_note = (f"；资格门名单内仍有 PENDING 项 {pending_names}：Failed=0 只表示暂无失败，"
                    "待其算完（重取 get_alpha_details）再判，不得据此放行" if pending_names else "")
    if ok and prepost_unverifiable:
        # 2026-09-08：处女提交（404）时提交层没有任何信息，此前一律报 SUBMITTABLE，
        # 造成假阳性（IND qMja95Q2 判 SUBMITTABLE 实测 prod 0.7354；MEA Jj7ee6nO/omqEE1pn 同）。
        verdict, note, next_step = "UNVERIFIABLE", _UNVERIFIABLE_NOTE + pending_note, _NEXT_STEP_RELEASE
        reason_code = "UNVERIFIABLE_404"
    elif ok:
        verdict, note, next_step = "SUBMITTABLE", (pending_note.lstrip("；") or None), _NEXT_STEP_RELEASE
        reason_code = "SUBMITTABLE"
    else:
        verdict = "BLOCKED"
        reason_code = ":".join([reasons[0][0]] + ([",".join(reasons[0][1])] if reasons[0][1] else []))
        note = "；".join(f"{code}[{','.join(nm)}]" if nm else code for code, nm in reasons)
        next_step = "先修复上述阻断项并重新回测后再判定；不要绕过（force / 直接 POST 探测均不可取）。"

    if verdict != "BLOCKED":
        if rob is None:
            next_step += (" 稳健性结论未落台账（ledger `robustness_<alpha_id>`）：未跑 brain-alpha-robustness 则先跑；"
                          "本提示不拦截。")
        elif rob["verdict"] == "CONDITIONAL":
            next_step += (" 稳健性 CONDITIONAL：先 brain-alpha-repair 修复并重审（≤ 2 轮），再请用户确认；本提示不拦截。")
    base.update({
        "robustness": {"recorded": rob is not None, "verdict": rob["verdict"] if rob else None,
                       "failed_checks": rob["failed_checks"] if rob else [],
                       "checked_at": rob["checked_at"] if rob else None},
        "verdict": verdict,
        "exit_code": EXIT_CODES[verdict],
        "reason_code": reason_code,
        "reasons": [{"code": c, "names": n} for c, n in reasons],
        "verdict_note": note,
        "next_step": next_step,
        "is_ppa": is_ppa,
        # 通道 vs 仅标签（2026-10-27）：平台给 REGULAR 提交成功的 alpha 也打
        # PowerPoolSelected，据此区分「真 PPA 通道」与「自动标签」。
        "ppa_channel": str(detail.get("type") or "").strip().upper() == "PPA",
        "ppa_tag_only": bool(is_ppa) and str(detail.get("type") or "").strip().upper() != "PPA",
        "hard_gate_warnings": hard_gate_warns,
        "failed_ra": failed_ra, "failed_ppa": failed_ppa,
        "failed_any": merged["count"],
        "failed_ra_items": failed_ra_items, "failed_ppa_items": failed_ppa_items,
        "failed_any_items": failed_gate_items,
        "pending_gate_names": pending_names,
        "submit_status": submit_status,
        "submit_checks": submit_checks,
        "submit_layer_view": "dead_endpoint_404" if submit_status == 404 else "live",
        "prepost_unverifiable": prepost_unverifiable,
    })
    return base
