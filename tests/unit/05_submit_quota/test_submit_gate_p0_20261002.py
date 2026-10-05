# -*- coding: utf-8 -*-
"""提交路由三闸（P0，2026-10-02）守护 —— F7 / F8 / F9 修复。

背景（步 8 评估 §15.4）：
  - **F7**：`submit_alpha` 节点不读 robustness 台账 → `submit_verdict` 对 `REJECT` 否决，
    但 `workflow_submit_alpha(confirm_submit=True, robustness_audited=True)` 放行，两入口矛盾。
  - **F8**：REGULAR 提交路径**无 prod 闸**（只有 SUPER 经 super_build 有）。
  - **F9**：提交路径无配额前置（满额只有 POST 后 403 才知道）。

本文件钉住三闸的:
  1. `_submit_gate` 读台账 → REJECT blocked；PASS/CONDITIONAL/无记录不拦；
  2. `_prod_gate` 纯判定：max<0.7 放行、≥0.7 拦、未出数 fail-closed；
  3. `_quota_gate` 纯判定：满 4 拦、未满放行、读不到 fail-open；
  4. run() 集成：robustness 台账 REJECT → blocked；prod ≥ 0.7 → blocked；
     配额满 → blocked；`force` 不豁免 prod / 配额（但豁免 submit_gate）。
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

ROOT = Path(__file__).resolve().parents[3]
for _p in (str(ROOT / "src"), str(ROOT / "world-quant-brain-mcp")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from wqb.workflow.nodes import submit_alpha as sa  # noqa: E402


@pytest.fixture(autouse=True)
def _allow_submit(monkeypatch):
    """本文件验证『提交被允许时』的 P0 闸（robustness/prod/quota/super）；全局禁提交闸由
    test_global_submit_lock.py 单独守护。"""
    monkeypatch.setattr(sa, "ALLOW_ALPHA_SUBMIT", True, raising=True)


# ---------------------------------------------------------------- _submit_gate 读台账
def _clean_checks():
    return {"is": {"checks": [{"name": "LOW_SHARPE", "result": "PASS", "value": 1.8, "limit": 1.58}]}}


def test_submit_gate_blocks_on_robustness_reject_via_ledger():
    """F7：台账 REJECT → gate blocked（robustness 显式传入）。"""
    r = sa._submit_gate(_clean_checks(), alpha_id="A1", robustness={
        "verdict": "REJECT", "failed_checks": ["SUBCRITICAL_DRAWDOWN"]})
    assert r["blocked"] is True
    assert any("REJECT" in s for s in r["blocked_reasons"])
    assert r["robustness"]["verdict"] == "REJECT"


def test_submit_gate_allows_robustness_pass():
    r = sa._submit_gate(_clean_checks(), alpha_id="A1", robustness={"verdict": "PASS"})
    assert r["blocked"] is False
    assert r["robustness"]["recorded"] is True


def test_submit_gate_allows_no_robustness_record():
    """无台账记录 → 不拦（fail-open 边界与 submit_verdict_core 一致）。"""
    r = sa._submit_gate(_clean_checks(), alpha_id="A1", robustness=None)
    assert r["blocked"] is False
    assert r["robustness"]["recorded"] is False


def test_submit_gate_reads_ledger_from_db_when_not_passed(monkeypatch, tmp_path):
    """未显式传 robustness 时，按 alpha_id + region 读 ledger。"""
    calls = {}

    def _fake_read(alpha_id, region, db_path=None):
        calls["args"] = (alpha_id, region)
        return {"verdict": "REJECT", "failed_checks": ["X"]}

    import wqb.robustness_record as rr
    monkeypatch.setattr(rr, "read_record", _fake_read)
    details = _clean_checks()
    details["settings"] = {"region": "gbr"}
    r = sa._submit_gate(details, alpha_id="A9")
    assert r["blocked"] is True
    assert calls["args"] == ("A9", "GBR")  # region 大写化
    assert any("REJECT" in s for s in r["blocked_reasons"])


def test_submit_gate_ledger_read_failure_is_tolerated(monkeypatch):
    """读台账抛异常 → 不崩溃、不拦（读不到不能让提交闸崩）。"""
    import wqb.robustness_record as rr

    def _boom(*a, **k):
        raise RuntimeError("db locked")

    monkeypatch.setattr(rr, "read_record", _boom)
    r = sa._submit_gate(_clean_checks(), alpha_id="A1")
    assert r["blocked"] is False


# ---------------------------------------------------------------- _prod_gate 纯判定
class _ProdClient:
    def __init__(self, payload):
        self.payload = payload

    async def check_correlation(self, alpha_id, correlation_type="production",
                               threshold=0.7, refresh=False):
        return self.payload


def _prod(payload):
    return sa._prod_gate(_ProdClient(payload), "A1")


def test_prod_gate_allows_below_threshold():
    r = _prod({"all_passed": True, "checks": {"production": {
        "max_correlation": 0.42, "passes_check": True}}})
    assert r["allowed"] is True and r["prod_max"] == 0.42


def test_prod_gate_blocks_at_or_above_threshold():
    r = _prod({"all_passed": False, "checks": {"production": {
        "max_correlation": 0.7, "passes_check": False}}})
    assert r["allowed"] is False and r["prod_max"] == 0.7
    assert "不得提交" in r["reason"]


def test_prod_gate_fail_closed_when_no_data():
    r = _prod({"all_passed": None, "status": "pending",
               "checks": {"production": {"max_correlation": None, "status": "pending"}}})
    assert r["allowed"] is False
    assert "fail-closed" in r["reason"]


def test_prod_gate_fail_closed_on_exception(monkeypatch):
    """check_correlation 抛异常 → fail-closed；`_run_async` 会把它包成 {"__error__": …}。"""
    class _Boom:
        async def check_correlation(self, *a, **k):
            raise RuntimeError("network down")
    r = sa._prod_gate(_Boom(), "A1")
    assert r["allowed"] is False
    assert "error" in r["status"] and ("network down" in r["reason"] or "失败" in r["reason"])


# ---------------------------------------------------------------- _quota_gate 纯判定
class _QuotaClient:
    def __init__(self, results=None, boom=False):
        self.results = results
        self.boom = boom

    async def get_user_alphas(self, **kw):
        if self.boom:
            raise RuntimeError("cannot list")
        return {"results": self.results}


def test_quota_gate_allows_when_slots_free():
    import datetime as dt
    from wqb.timeutil import et_now
    # 构造一条"现在（ET）"的提交记录 → 必然落在当前 ET 日历日
    iso = et_now().astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    res = [{"id": "x", "dateSubmitted": iso, "settings": {"region": "USA"}}]
    r = sa._quota_gate(_QuotaClient(results=res), "A1")
    assert r["limit"] == 4 and r["used"] == 1 and r["remaining"] == 3
    assert r["allowed"] is True


def test_quota_gate_blocks_when_full():
    """构造 4 条今日提交 → blocked。"""
    import datetime as dt
    from wqb.timeutil import et_now
    iso = et_now().astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    res = [{"id": f"x{i}", "dateSubmitted": iso, "settings": {"region": "USA"}}
           for i in range(4)]
    r = sa._quota_gate(_QuotaClient(results=res), "A1")
    assert r["allowed"] is False and r["used"] >= 4
    assert "配额已满" in r["reason"]


def test_quota_gate_fail_open_on_error():
    r = sa._quota_gate(_QuotaClient(boom=True), "A1")
    assert r["allowed"] is True and "fail-open" in r["reason"]


# ---------------------------------------------------------------- run() 集成
@pytest.fixture
def patched(monkeypatch):
    """默认：client 干净、各闸放行；各测试再按需覆盖单个闸。"""
    def _d(*a, **k):
        return {"success": True, "is": {"checks": [
            {"name": "LOW_SHARPE", "result": "PASS", "value": 1.8, "limit": 1.58}]}}
    monkeypatch.setattr(sa, "_get_brain_client", lambda: MagicMock())
    monkeypatch.setattr(sa, "_run_async", _d)
    monkeypatch.setattr(sa, "_poll_status", lambda *a, **k: "ACTIVE")
    monkeypatch.setattr(sa, "_current_status", lambda *a, **k: "ACTIVE")
    monkeypatch.setattr(sa, "_classify_submit_response", lambda *a, **k: "confirmed")
    monkeypatch.setattr(sa, "_derive_tags", lambda *a, **k: [])
    monkeypatch.setattr(sa, "_retire_queue", lambda *a, **k: 0)
    monkeypatch.setattr(sa, "_prod_gate", lambda *a, **k: {
        "allowed": True, "prod_max": 0.5, "threshold": 0.7, "status": "ok", "reason": "stub"})
    monkeypatch.setattr(sa, "_quota_gate", lambda *a, **k: {
        "allowed": True, "used": 0, "limit": 4, "remaining": 4, "reason": "stub"})
    # 默认无台账记录
    monkeypatch.setattr(sa, "_submit_gate", sa._submit_gate)  # 保持真实
    return sa


def test_run_robustness_ledger_reject_blocks(patched, monkeypatch):
    """F7 集成：台账 REJECT → run 直接 blocked（robustness_audited=True 也拦）。"""
    import wqb.robustness_record as rr
    monkeypatch.setattr(rr, "read_record", lambda *a, **k: {
        "verdict": "REJECT", "failed_checks": ["Z"]})
    out = patched.run(alpha_id="A1", confirm_submit=True, robustness_audited=True)
    assert out["blocked"] is True
    assert "submit_gate" in out["reason"]
    assert out.get("submitted") is False


def test_run_prod_gate_blocks(patched, monkeypatch):
    """F8 集成：prod ≥ 0.7 → blocked。"""
    monkeypatch.setattr(patched, "_prod_gate", lambda *a, **k: {
        "allowed": False, "prod_max": 0.81, "threshold": 0.7, "status": "ok",
        "reason": "prod max=0.81 ≥ 0.7"})
    out = patched.run(alpha_id="A1", confirm_submit=True, robustness_audited=True)
    assert out["blocked"] is True and "prod_gate" in out["reason"]


def test_run_prod_gate_exempt_by_flag(patched, monkeypatch):
    """allow_prod_above_07=True 显式豁免 → 继续提交。"""
    monkeypatch.setattr(patched, "_prod_gate", lambda *a, **k: pytest.fail("不应调用 prod 闸"))
    out = patched.run(alpha_id="A1", confirm_submit=True, robustness_audited=True,
                      allow_prod_above_07=True)
    assert out.get("submitted") is True
    steps = [s.get("step") for s in out["steps"]]
    assert "prod_gate" in steps


def test_run_quota_gate_blocks(patched, monkeypatch):
    """F9 集成：配额满 → blocked。"""
    monkeypatch.setattr(patched, "_quota_gate", lambda *a, **k: {
        "allowed": False, "used": 4, "limit": 4, "remaining": 0, "reason": "配额已满"})
    out = patched.run(alpha_id="A1", confirm_submit=True, robustness_audited=True)
    assert out["blocked"] is True and "quota_gate" in out["reason"]


def test_run_force_does_not_exempt_prod_or_quota(patched, monkeypatch):
    """force=True 仍受 prod 闸 / 配额闸约束（用户红线不可用 force 绕过）。"""
    monkeypatch.setattr(patched, "_prod_gate", lambda *a, **k: {
        "allowed": False, "prod_max": 0.9, "threshold": 0.7, "status": "ok", "reason": "x"})
    out = patched.run(alpha_id="A1", confirm_submit=True, force=True)
    assert out["blocked"] is True and "prod_gate" in out["reason"]


def test_run_super_skips_quota_gate(patched, monkeypatch):
    """SUPER 在配额闸前就被拒（quota 闸只对非 SUPER 生效）。"""
    monkeypatch.setattr(patched, "_run_async",
                        lambda *a, **k: {"type": "SUPER", "is": {"checks": [
                            {"name": "SHARPE", "result": "PASS", "value": 3.0}]}})
    out = patched.run(alpha_id="A1", confirm_submit=True, robustness_audited=True)
    assert out["reason"] == "super_requires_super_build"
