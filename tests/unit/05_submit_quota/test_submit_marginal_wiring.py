# -*- coding: utf-8 -*-
"""Step 1.7 在 `run()` 里的接线守护：**负边际贡献 = 硬闸，阻断提交**。

`test_submit_marginal_contribution.py` 锁的是 `_marginal_contribution` 本身的语义；
本文件锁的是接进提交主流程后的行为。

口径沿革：2026-11-04 引入时为「信息项 / 永不阻断」（理由见节点 docstring 的四条）；
**2026-11-08 用户明令「如果边际贡献为负你就阻断不准提交」⇒ 语义反转为否决闸**。
新语义三条：

1. `confirm_submit=False` 的**预检仍必须产出**该数值（用户要据此判断分散/稀释），
   预检本身不阻断，但必须留下「真提交会被拦」的痕迹（顶层 `marginal_warning`）；
2. `ΔSharpe<0` 且 `confirm_submit=True` ⇒ `blocked=True`，在 set_properties / POST
   **之前** return（零平台副作用）；
3. `ΔSharpe>=0` ⇒ 无 `marginal_warning`，流程照常。
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
for _p in (REPO_ROOT / "src",):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.workflow.nodes import submit_alpha as SA  # noqa: E402


def _alpha_detail():
    return {
        "id": "TESTALPHA1",
        "status": "UNSUBMITTED",
        "type": "REGULAR",
        "settings": {"region": "DEU", "universe": "TOP500", "delay": 1},
        "regular": {"operatorCount": 10, "code": "x"},
        "is": {"sharpe": 2.0, "fitness": 1.5, "turnover": 0.15, "checks": []},
    }


class _FakeClient:
    def __init__(self, before, after):
        self._payload = {
            "partitionName": "EQUITY:DEU:1:POWER_POOL",
            "stats": {"before": before, "after": after},
        }

    async def get_alpha_details(self, alpha_id):
        return _alpha_detail()

    async def performance_comparison(self, alpha_id):
        return self._payload

    def __getattr__(self, name):
        async def _noop(*a, **k):
            return {}
        return _noop


def _run(monkeypatch, before, after, confirm_submit=False):
    client = _FakeClient(before, after)
    monkeypatch.setattr(SA, "_get_brain_client", lambda: client)
    # 全局禁提交开关：本文件专测链路行为，绕过它（真实调用由用户点名 + 环境变量放行）
    monkeypatch.setattr(SA, "ALLOW_ALPHA_SUBMIT", True)
    # 把其余闸门与持久化换成直通，专测 Step 1.7 的接线
    monkeypatch.setattr(SA, "_submit_gate", lambda *a, **k: {
        "step": "submit_gate", "passed": True, "blocked": False,
        "robustness": {"recorded": True, "verdict": "PASS"},
    })
    monkeypatch.setattr(SA, "_quota_gate", lambda *a, **k: {
        "allowed": True, "used": 1, "limit": 4, "remaining": 3,
    })
    monkeypatch.setattr(SA, "_prod_gate", lambda *a, **k: {
        "allowed": True, "prod_max": 0.60, "threshold": 0.7,
    })
    # 提交后状态轮询：直接返回 ACTIVE，避免测试真等 verify_timeout
    monkeypatch.setattr(SA, "_poll_status", lambda *a, **k: "ACTIVE")
    monkeypatch.setattr(SA, "_finalize", lambda r, s, a, **k: r)
    return SA.run(alpha_id="TESTALPHA1", confirm_submit=confirm_submit, _context={})


_BEFORE = {"sharpe": 1.73, "fitness": 1.37, "turnover": 0.127,
           "returns": 0.0799, "drawdown": 0.0608}
_DILUTIVE_AFTER = {"sharpe": 1.55, "fitness": 1.30, "turnover": 0.130,
                   "returns": 0.0750, "drawdown": 0.0700}
_HELPFUL_AFTER = {"sharpe": 1.98, "fitness": 1.50, "turnover": 0.137,
                  "returns": 0.0784, "drawdown": 0.0402}


def _marginal_step(result):
    for s in result.get("steps") or []:
        if s.get("step") == "marginal_contribution":
            return s
    return None


def test_preflight_produces_marginal_contribution(monkeypatch):
    """预检（confirm_submit=False）就必须有这项数值。"""
    r = _run(monkeypatch, _BEFORE, _HELPFUL_AFTER)
    s = _marginal_step(r)
    assert s is not None, "预检未产出 marginal_contribution"
    assert s["available"] is True
    assert s["partition"] == "EQUITY:DEU:1:POWER_POOL"


def test_negative_delta_blocks_real_submit(monkeypatch):
    """ΔS<0 且 confirm_submit=True ⇒ 阻断，且在 set_properties / POST 之前。"""
    r = _run(monkeypatch, _BEFORE, _DILUTIVE_AFTER, confirm_submit=True)

    s = _marginal_step(r)
    assert s["dilutive"] is True
    assert "blocked" not in s, "闸门标志属于顶层 result，step 自带会与其它闸混淆"

    assert r.get("blocked") is True, "ΔS<0 必须阻断提交（用户 2026-11-08 铁律）"
    assert r.get("reason", "").startswith("marginal_contribution blocked"), r.get("reason")
    assert "force 不豁免" in (r.get("blocked_reason") or "")

    w = r.get("marginal_warning")
    assert w and w["delta_sharpe"] < 0, "ΔS<0 必须在顶层留下 marginal_warning"
    assert "硬闸阻断" in w["note"]

    # 阻断点必须在任何平台副作用之前
    step_names = [x.get("step") for x in (r.get("steps") or [])]
    assert "set_properties" not in step_names, "阻断必须早于 set_properties"
    assert "submit" not in step_names, "阻断必须早于 POST"
    assert r.get("submitted") is not True


def test_negative_delta_preflight_warns_but_not_blocked(monkeypatch):
    """预检不阻断，但必须预告真提交会被拦（不可静默）。"""
    r = _run(monkeypatch, _BEFORE, _DILUTIVE_AFTER, confirm_submit=False)
    assert r.get("marginal_warning"), "预检也必须呈现 ΔS<0"
    assert not r.get("blocked"), "预检不提交，不应置 blocked"
    assert r.get("success") is True


def test_positive_delta_has_no_warning(monkeypatch):
    r = _run(monkeypatch, _BEFORE, _HELPFUL_AFTER, confirm_submit=True)
    assert "marginal_warning" not in r
    assert _marginal_step(r)["dilutive"] is False
    assert not r.get("blocked")
