# -*- coding: utf-8 -*-
"""提交链 P0 守护（2026-10-27）——两条会「放过不该放的候选」/「谎报已提交」的缺陷。

P0-1（已修，见 test_submit_alpha_gate.py 的 run() 集成）：
    已提交 alpha 无 Step 0 短路，重复调用会跑 prod 闸并可能报假 blocked。

P0-2（本文件重点）：``is_ppa`` 被平台**自动打的** ``PowerPoolSelected`` 标签误导。
    平台给 REGULAR 提交成功的 alpha 也打这个标签（2026-10-27 JjeMlmXA 实证），而
    ``PPA_CHECK_NAMES ⊂ RA_CHECK_NAMES`` + PPA 只看 ``LOW_SHARPE < 1``，于是
    ``LOW_FITNESS`` / ``LOW_2Y_SHARPE`` / ``IS_LADDER_SHARPE`` 等**只在 RA 名单里**的
    失败被整片漏掉 ⇒ 提交闸放行、判定层甚至可能报 SUBMITTABLE。
    修法：判定用 ``merge_failed_items``（RA 为下界 ∪ 真 PPA 的额外项），
    ``is_ppa`` 仅保留「通道」语义（另给 ``ppa_channel`` / ``ppa_tag_only`` 供盘点）。

P0-3（本文件重点）：``{"__error__": "fetch failed"}`` 被当成「异步受理、已提交」。
    应归入 ``transport_error``，并按项目铁律「提交类报错 ≠ 动作未发生」**先回查平台**
    （``status`` / ``dateSubmitted``）再决定是否补发，且不得谎报 ``submitted=True``。
"""
from __future__ import annotations

import pytest


# ---------------------------------------------------------------- merge_failed_items
def test_merge_failed_items_ra_is_lower_bound():
    """RA 项是下界：即便不是 PPA，RA 名单内的失败也必须进合并集。"""
    from wqb.config import compute_webdata_failed_counts, merge_failed_items

    counts = compute_webdata_failed_counts([
        {"name": "LOW_FITNESS", "result": "FAIL", "value": 0.9, "limit": 1.0},
        {"name": "LOW_TURNOVER", "result": "WARNING", "value": 0.5},
    ])
    assert counts["failed_ra"] == 2
    # LOW_FITNESS 不在 PPA 名单 ⇒ 只看 PPA 只有 1 项（这正是 P0-2 的漏点）
    assert counts["failed_ppa"] == 1

    merged = merge_failed_items(counts, ppa_bonus=False)
    assert merged["count"] == 2
    assert set(merged["names"]) == {"LOW_FITNESS", "LOW_TURNOVER"}


def test_merge_failed_items_ppa_bonus_only_when_true():
    """PPA 专有规则（LOW_SHARPE 结果 PASS 但 value<1）只在真 PPA 通道并入。"""
    from wqb.config import compute_webdata_failed_counts, merge_failed_items

    counts = compute_webdata_failed_counts([
        {"name": "LOW_SHARPE", "result": "PASS", "value": 0.9, "limit": 1.0},
    ])
    assert counts["failed_ra"] == 0 and counts["failed_ppa"] == 1
    assert merge_failed_items(counts, ppa_bonus=False)["count"] == 0     # REGULAR：不计
    assert merge_failed_items(counts, ppa_bonus=True)["names"] == ["LOW_SHARPE"]  # PPA：计


# ---------------------------------------------------------------- _submit_gate
@pytest.fixture
def gate():
    from wqb.workflow.nodes import submit_alpha as sa
    return sa._submit_gate


def test_gate_blocks_regular_alpha_with_auto_ppa_tag(gate):
    """P0-2 回归：REGULAR 带平台自动打的 PowerPoolSelected 标签，
    LOW_FITNESS FAIL 仍必须被拦（旧实现看 failed_ppa=0 ⇒ 放行）。"""
    r = gate({
        "type": "REGULAR",
        "tags": ["CH_REG", "PowerPoolSelected"],
        "is": {"checks": [
            {"name": "LOW_FITNESS", "result": "FAIL", "value": 0.93, "limit": 1.0},
        ]},
    })
    assert r["blocked"] is True, "REGULAR 的 RA 失败被 PPA 标签掩盖了"
    assert r["failed_ra"] == 1 and r["failed_ppa"] == 0
    assert r["failed_any"] == 1
    assert any("Phase B.0" in s for s in r["blocked_reasons"])
    assert any("LOW_FITNESS" in s for s in r["blocked_reasons"])
    # 通道 vs 标签：报告层要能区分，避免事后盘点把 REGULAR 记成 PPA
    assert r["is_ppa"] is True
    assert r["ppa_channel"] is False
    assert r["ppa_tag_only"] is True


def test_gate_blocks_regular_alpha_on_only_ra_gate(gate):
    """只在 RA 名单里的闸（LOW_RETURNS）失败，带 PPA 标签时同样要拦。"""
    r = gate({
        "type": "REGULAR",
        "tags": ["PowerPoolSelected"],
        "is": {"checks": [
            {"name": "LOW_RETURNS", "result": "WARNING", "value": 0.004, "limit": 0.01},
        ]},
    })
    assert r["blocked"] is True
    assert r["failed_ra"] == 1 and r["failed_ppa"] == 0
    assert r["failed_any"] == 1


def test_gate_real_ppa_still_uses_ppa_rule(gate):
    """真 PPA（type=PPA）保留 PPA 专有规则：LOW_SHARPE PASS 但 value<1 仍计失败。"""
    r = gate({
        "type": "PPA",
        "is": {"checks": [
            {"name": "LOW_SHARPE", "result": "PASS", "value": 0.9, "limit": 1.0},
        ]},
    })
    assert r["blocked"] is True
    assert r["failed_any"] == 1 and r["failed_ppa"] == 1
    assert r["ppa_channel"] is True and r["ppa_tag_only"] is False


def test_gate_clean_alpha_passes(gate):
    r = gate({
        "type": "REGULAR",
        "tags": ["CH_REG", "PowerPoolSelected"],
        "is": {"checks": [
            {"name": "LOW_SHARPE", "result": "PASS", "value": 2.3, "limit": 1.58},
            {"name": "LOW_FITNESS", "result": "PASS", "value": 1.1, "limit": 1.0},
        ]},
    })
    assert r["blocked"] is False and r["failed_any"] == 0


# ---------------------------------------------------------------- decide()
def _detail(checks, *, type="REGULAR", tags=None):
    return {"status": "UNSUBMITTED", "type": type, "tags": tags or [],
            "is": {"checks": list(checks)}}


def test_decide_blocks_regular_alpha_with_auto_ppa_tag():
    """P0-2 回归（判定层）：旧实现会因 PPA 标签看错计数组 → 可能报 SUBMITTABLE。

    用 ``LOW_GLB_AMER_SHARPE``（在 RA 名单、**不在** PPA 名单、也不是硬闸 WARNING）
    才能把差异单独暴露在 Failed-count 这道闸上。
    """
    from wqb.submit_verdict_core import decide

    r = decide("A1", _detail(
        [{"name": "LOW_GLB_AMER_SHARPE", "result": "WARNING", "value": 0.42, "limit": 1.0}],
        tags=["CH_REG", "PowerPoolSelected"]), 404, [])
    assert r["verdict"] == "BLOCKED"
    assert r["reason_code"] == "FAILED_COUNT_RA:LOW_GLB_AMER_SHARPE"
    assert r["failed_ra"] == 1 and r["failed_ppa"] == 0
    assert r["failed_any"] == 1
    assert r["ppa_channel"] is False and r["ppa_tag_only"] is True


def test_decide_hard_gate_fail_still_blocks_with_auto_ppa_tag():
    """带 PPA 自动标签时，模拟层 FAIL 仍走 SIM_FAIL（不被标签改变语义）。"""
    from wqb.submit_verdict_core import decide

    r = decide("A2", _detail(
        [{"name": "LOW_2Y_SHARPE", "result": "FAIL", "value": 1.21, "limit": 1.58}],
        tags=["CH_REG", "PowerPoolSelected"]), 404, [])
    assert r["verdict"] == "BLOCKED"
    assert r["reason_code"].startswith("SIM_FAIL:LOW_2Y_SHARPE")


def test_decide_ppa_bonus_still_applies_for_real_ppa():
    from wqb.submit_verdict_core import decide

    r = decide("P1", _detail(
        [{"name": "LOW_SHARPE", "result": "PASS", "value": 0.9, "limit": 1.0}],
        type="PPA"), 404, [])
    assert r["verdict"] == "BLOCKED"
    assert r["reason_code"] == "FAILED_COUNT_PPA:LOW_SHARPE"
    assert r["failed_any"] == 1 and r["ppa_channel"] is True


# ---------------------------------------------------------------- 响应分类
def test_classify_transport_error():
    """P0-3 回归：fetch failed 必须独立成态，不得落到 unknown_accept。"""
    from wqb.workflow.nodes import submit_alpha as sa

    assert sa._classify_submit_response({"__error__": "fetch failed"}) == "transport_error"
    # 非传输错误的空体仍是异步受理（语义不变）
    assert sa._classify_submit_response({}) == "unknown_accept"
    assert sa._classify_submit_response(
        {"success": True, "reason": "IS checks passed"}) == "confirmed"
    assert sa._classify_submit_response(
        {"status_code": 202, "detail": "Accepted (async)"}) == "async_accepted"


# ---------------------------------------------------------------- run() 传输错误处置
class _FakeClient:
    """最小假客户端：记录调用序列。

    ``get_alpha_details`` 是**有状态**的：POST 之前返回 ``pre_status``（默认
    UNSUBMITTED，避免命中 Step 0 已提交短路）；POST 之后再返回 ``landing_status`` /
    ``landing_date``，用来模拟「POST 报错但平台已落地」。
    """

    def __init__(self, *, post_result, landing_status, landing_date,
                 pre_status="UNSUBMITTED"):
        self.post_result = post_result
        self.landing_status = landing_status
        self.landing_date = landing_date
        self.pre_status = pre_status
        self.posted = False
        self.calls = []

    async def get_alpha_details(self, alpha_id):
        self.calls.append("get_alpha_details")
        status = self.landing_status if self.posted else self.pre_status
        date = self.landing_date if self.posted else None
        return {
            "id": alpha_id,
            "status": status,
            "dateSubmitted": date,
            "type": "REGULAR",
            "settings": {"region": "GLB"},
            "is": {"checks": [
                {"name": "LOW_SHARPE", "result": "PASS", "value": 2.3, "limit": 1.58},
                {"name": "LOW_FITNESS", "result": "PASS", "value": 1.1, "limit": 1.0},
            ]},
        }

    async def submit_alpha(self, alpha_id):
        self.calls.append("submit_alpha")
        self.posted = True
        return self.post_result

    async def set_alpha_properties(self, *a, **k):
        self.calls.append("set_alpha_properties")
        return {"ok": True}

    async def check_correlation(self, alpha_id, **kw):
        self.calls.append("check_correlation")
        return {"checks": {"production": {"max_correlation": 0.55, "status": "ok"}}}

    async def get_user_alphas(self, **kw):
        return {"results": []}


@pytest.fixture
def sa(monkeypatch):
    from wqb.workflow.nodes import submit_alpha as sa_mod
    monkeypatch.setattr(sa_mod, "ALLOW_ALPHA_SUBMIT", True)
    # 避免真轮询：返回当前详情里的状态
    monkeypatch.setattr(sa_mod, "_poll_status",
                        lambda client, aid, timeout: client.landing_status)
    monkeypatch.setattr(sa_mod, "_retire_queue", lambda *a, **k: 0)
    return sa_mod


def test_run_transport_error_landed_is_not_reposted(monkeypatch, sa):
    """POST 报 fetch failed，但平台已落地（dateSubmitted 有值）⇒ 不得补发、不得谎报未提交。"""
    client = _FakeClient(post_result={"__error__": "fetch failed"},
                         landing_status="ACTIVE",
                         landing_date="2026-10-27T02:12:46-04:00")
    monkeypatch.setattr(sa, "_get_brain_client", lambda: client)

    out = sa.run(alpha_id="JjeMlmXA", confirm_submit=True, robustness_audited=True)

    assert out.get("blocked") is not True
    assert out["submitted"] is True
    assert out.get("submitted_via") == "transport_error_recheck"
    assert out["final_status"] == "ACTIVE"
    assert out["success"] is True
    # 关键：只 POST 一次，靠回查确认落地，绝不补发
    assert client.calls.count("submit_alpha") == 1
    steps = [s.get("step") for s in out["steps"]]
    assert "post_transport_recheck" in steps
    assert "async_resubmit" not in steps


def test_run_transport_error_not_landed_reposts_once(monkeypatch, sa):
    """POST 报 fetch failed 且平台未落地 ⇒ 回查后按 SOP 补发一次（幂等）。"""
    client = _FakeClient(post_result={"__error__": "fetch failed"},
                         landing_status="UNSUBMITTED",
                         landing_date=None)
    monkeypatch.setattr(sa, "_get_brain_client", lambda: client)

    out = sa.run(alpha_id="X1", confirm_submit=True, robustness_audited=True)

    assert client.calls.count("submit_alpha") == 2      # 首发 + 补发
    steps = [s.get("step") for s in out["steps"]]
    assert "post_transport_recheck" in steps and "async_resubmit" in steps
    assert out.get("async_stuck") is True
    assert out["success"] is False
