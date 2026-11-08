# -*- coding: utf-8 -*-
"""Step 1.2（混腿审查）在 `run()` 里的接线守护。

`test_submit_queue_mix_review.py` 锁的是判定本身；本文件锁**接进提交主流程后的行为**。
它补的是一个真实漏洞：2026-11-08 审计发现四层闸里只有波次装配层查混信号，而提交节点
**完全不查** ⇒ 直走 batch/multisim 派发时等于没有这道闸，禁令后泄漏率 15%（26/173）。

三条必须成立的语义：
1. `weight_grid`（≥2 系数腿）/ `stack`（≥4 腿）⇒ `confirm_submit=True` 一律阻断，
   **`force=True` 不豁免**，且阻断点在任何平台副作用之前；
2. 2–3 腿的多源组合 ⇒ 缺三问则阻断（`force=True` 可豁免留痕），三问齐则放行；
3. 顺带产出 `path`（ATOM:LAST_2Y / LADDER）—— 信息项，**不参与阻断**，只提示
   「近 2 年弱有没有退路」（官方：单数据集只查 Last-2Y ≥2.38；多数据集走 Ladder 可退到 7Y/10Y）。
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
for _p in (REPO_ROOT / "src",):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.workflow.nodes import submit_alpha as SA  # noqa: E402


GRID = "add(multiply(0.4, rank(a)), multiply(0.6, rank(b)))"
TWO_LEG = ("add(group_rank(ts_zscore(pv103_ivam_sum, 66), sector), "
           "reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main), 504), industry)))")
STACK = "add(rank(a), rank(b), rank(c), rank(d))"
SINGLE = "subtract(0.5, group_rank(ts_mean(vec_stddev(insd5_vol_chg), 55), sector))"

NARR = {
    "holders": "主腿看异常成交额（注意力/散户），次腿看借券规模（空头需求）",
    "polarity": "两腿同号看多：成交额异常为正、借券下降已 reverse 成正",
    "prior": "2:1 配比在回测前由「主腿主导、借券只做确认」的逻辑钉死",
}


def _detail(code, checks=None):
    return {
        "id": "TESTALPHA1",
        "status": "UNSUBMITTED",
        "type": "REGULAR",
        "settings": {"region": "GBR", "universe": "TOP700", "delay": 1},
        "regular": {"operatorCount": 5, "code": code},
        "is": {
            "sharpe": 2.0, "fitness": 1.5, "turnover": 0.15,
            "checks": checks if checks is not None else [
                {"name": "LOW_SHARPE", "result": "PASS"},
                {"name": "IS_LADDER_SHARPE", "result": "PASS"},
            ],
        },
    }


class _FakeClient:
    def __init__(self, detail):
        self._detail = detail

    async def get_alpha_details(self, alpha_id):
        return self._detail

    async def submit_alpha(self, alpha_id):
        return {"success": True, "status_code": 200,
                "message": "Alpha submitted; IS checks passed"}

    async def performance_comparison(self, alpha_id):
        return {"partitionName": "EQUITY:GBR:1:POWER_POOL",
                "stats": {"before": {"sharpe": 2.0, "fitness": 1.2, "turnover": 0.15,
                                     "returns": 0.08, "drawdown": 0.05},
                          "after": {"sharpe": 2.3, "fitness": 1.3, "turnover": 0.15,
                                    "returns": 0.09, "drawdown": 0.04}}}

    def __getattr__(self, name):
        async def _noop(*a, **k):
            return {}
        return _noop


def _run(monkeypatch, code, *, checks=None, confirm_submit=False, force=False, narrative=None):
    client = _FakeClient(_detail(code, checks))
    monkeypatch.setattr(SA, "_get_brain_client", lambda: client)
    monkeypatch.setattr(SA, "ALLOW_ALPHA_SUBMIT", True)
    monkeypatch.setattr(SA, "_submit_gate", lambda *a, **k: {
        "step": "submit_gate", "passed": True, "blocked": False,
        "robustness": {"recorded": True, "verdict": "PASS"}})
    monkeypatch.setattr(SA, "_quota_gate", lambda *a, **k: {
        "allowed": True, "used": 1, "limit": 4, "remaining": 3})
    monkeypatch.setattr(SA, "_prod_gate", lambda *a, **k: {
        "allowed": True, "prod_max": 0.5, "threshold": 0.7})
    monkeypatch.setattr(SA, "_poll_status", lambda *a, **k: "ACTIVE")
    monkeypatch.setattr(SA, "_finalize", lambda r, s, a, **k: r)
    return SA.run(alpha_id="TESTALPHA1", confirm_submit=confirm_submit, force=force,
                  mix_narrative=narrative, _context={})


def _mix_step(result):
    for s in result.get("steps") or []:
        if s.get("step") == "mix_audit":
            return s
    return None


# ---------------- 结构硬拦 ----------------

def test_preflight_reports_weight_grid_but_does_not_block(monkeypatch):
    """预检必须把结构判定与路径判出来，且**不**置 blocked（预检不提交）。"""
    r = _run(monkeypatch, GRID)
    s = _mix_step(r)
    assert s is not None, "预检未产出 mix_audit"
    assert s["available"] is True
    assert s["kind"] == "weight_grid"
    assert s["blocked"] is True
    assert not r.get("blocked")
    assert r.get("success") is True
    assert r.get("mix_warning"), "预检必须预告真提交会被拦"


def test_weight_grid_blocks_real_submit_before_side_effects(monkeypatch):
    r = _run(monkeypatch, GRID, confirm_submit=True)
    assert r.get("blocked") is True
    assert r.get("reason", "").startswith("mix_audit blocked"), r.get("reason")
    assert "force 不豁免" in (r.get("blocked_reason") or "")
    names = [x.get("step") for x in (r.get("steps") or [])]
    assert "set_properties" not in names, "阻断必须早于 set_properties"
    assert "submit" not in names, "阻断必须早于 POST"
    assert r.get("submitted") is not True


def test_weight_grid_ignores_force_and_narrative(monkeypatch):
    """结构硬拦：force 与三问都救不了（官方禁的就是这一类）。"""
    r = _run(monkeypatch, GRID, confirm_submit=True, force=True, narrative=NARR)
    assert r.get("blocked") is True
    assert r.get("reason", "").startswith("mix_audit blocked")


def test_stack_blocks_real_submit(monkeypatch):
    r = _run(monkeypatch, STACK, confirm_submit=True, narrative=NARR)
    s = _mix_step(r)
    assert s["kind"] == "stack" and s["legs"] == 4
    assert r.get("blocked") is True
    assert r.get("reason", "").startswith("mix_audit blocked")


# ---------------- 三问 ----------------

def test_two_leg_without_narrative_blocks(monkeypatch):
    r = _run(monkeypatch, TWO_LEG, confirm_submit=True)
    s = _mix_step(r)
    assert (s["kind"], s["blocked"], s["narrative_ok"]) == ("two_leg", False, False)
    assert r.get("blocked") is True
    assert r.get("reason", "").startswith("mix_narrative missing")
    assert "holders" in (r.get("reason") or "")
    names = [x.get("step") for x in (r.get("steps") or [])]
    assert "set_properties" not in names and "submit" not in names


def test_two_leg_with_narrative_passes(monkeypatch):
    r = _run(monkeypatch, TWO_LEG, confirm_submit=True, narrative=NARR)
    s = _mix_step(r)
    assert s["narrative_ok"] is True and s["narrative_missing"] == []
    assert not r.get("blocked"), r.get("reason")
    assert "mix_warning" not in r
    assert "submit" in [x.get("step") for x in (r.get("steps") or [])]


def test_two_leg_force_bypasses_narrative_only(monkeypatch):
    """三问是自设纪律，force 可豁免（留痕）；但结构硬拦 force 无效（上一条已锁）。"""
    r = _run(monkeypatch, TWO_LEG, confirm_submit=True, force=True)
    assert not r.get("blocked"), r.get("reason")
    assert "submit" in [x.get("step") for x in (r.get("steps") or [])]


def test_single_leg_needs_no_narrative(monkeypatch):
    r = _run(monkeypatch, SINGLE, confirm_submit=True)
    s = _mix_step(r)
    assert s["blocked"] is False and s["narrative_required"] is False
    assert not r.get("blocked")
    assert "mix_warning" not in r


# ---------------- ATOM / Ladder 路径提示 ----------------

def test_path_ladder_from_checks_names(monkeypatch):
    r = _run(monkeypatch, TWO_LEG, checks=[
        {"name": "LOW_SHARPE", "result": "PASS"},
        {"name": "IS_LADDER_SHARPE", "result": "PASS"}])
    s = _mix_step(r)
    assert (s["data_usage"], s["path"]) == ("MULTI_DATA_SET", "LADDER")
    assert "7Y 2.06" in s["hint"] and "1.59" in s["hint"]


def test_path_atom_from_checks_names(monkeypatch):
    r = _run(monkeypatch, SINGLE, checks=[
        {"name": "LOW_SHARPE", "result": "PASS"},
        {"name": "LOW_2Y_SHARPE", "result": "PASS"}])
    s = _mix_step(r)
    assert (s["data_usage"], s["path"]) == ("SINGLE_DATA_SET", "ATOM:LAST_2Y")
    assert "2.023" in s["hint"] or "2.38" in s["hint"]


def test_path_unknown_when_neither_marker(monkeypatch):
    r = _run(monkeypatch, SINGLE, checks=[{"name": "LOW_SHARPE", "result": "PASS"}])
    s = _mix_step(r)
    assert s["path"] == "UNKNOWN"
    assert s["blocked"] is False, "路径不可判不得阻断提交"


def test_path_hint_never_blocks(monkeypatch):
    """路径是提示项：ATOM 判定下 2Y 很弱也不阻断（阻断只认结构/三问）。"""
    r = _run(monkeypatch, SINGLE, confirm_submit=True, checks=[
        {"name": "LOW_2Y_SHARPE", "result": "PASS"}])
    assert _mix_step(r)["path"] == "ATOM:LAST_2Y"
    assert not r.get("blocked")


# ---------------- fail-open 边界 ----------------

def test_missing_expression_fails_open(monkeypatch):
    """读不到 regular.code（非 REGULAR 或平台未回填）⇒ 不审查、不阻断。"""
    r = _run(monkeypatch, "", confirm_submit=True)
    s = _mix_step(r)
    assert s["available"] is False
    assert "读不到 regular.code" in (s.get("note") or "")
    assert not r.get("blocked")
