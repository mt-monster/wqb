# -*- coding: utf-8 -*-
"""Step 5 `prod 快照恒等式` 守护：闸门读到的数，必须等于平台冻结的数。

2026-11-08 接入。本文件锁死四条不变量：

1. **只做恒等式，不做准入**：无论匹配与否，都**不得**回写 `blocked` / 改 `success`。
   提交一旦 ACTIVE 无法回退，此处只能告警留痕（与 Step 1.6 的 fail-closed prod 闸
   是两种语义，不能混）。

2. **比对基准 = Step 1.6 的 `prod_max`**，不是缓存文件、也不是重新计算的值。
   若 steps 里没有 prod_gate（SUPER/PPA 走 super_build），返回 `available=False`
   而不是擅自补算。

3. **平台未回填时 fail-open**：`is.prodCorrelation` 为 None ⇒ `available=False`，
   不报警。异步检查未落库是正常状态，不是异常。

4. **容差 0.005**：平台四舍五入到 4 位，同一读数允许末位抖动；超过即判不同源。
   实测三颗完全相等（kqN92KpK 0.6196 / bl6AvMkN 0.6470 / zq3eb7No 0.6171），
   故 0.005 已是极宽松阈值，一旦越界必是结构性问题。
"""

from __future__ import annotations

import pytest

from wqb.workflow.nodes import submit_alpha as SA


class _Client:
    def __init__(self, recorded=None, raises=None):
        self._recorded = recorded
        self._raises = raises

    async def get_alpha_details(self, alpha_id):
        if self._raises:
            raise self._raises
        return {"id": alpha_id, "is": {"prodCorrelation": self._recorded}}


def _steps(gate_value):
    return [{"step": "prod_gate", "allowed": True, "prod_max": gate_value,
             "threshold": 0.7}]


def test_match_is_silent():
    r = SA._prod_snapshot_check(_Client(0.6196), "X", _steps(0.6196))
    assert r["available"] is True
    assert r["matches"] is True
    assert r["delta"] == 0
    assert "blocked" not in r


def test_mismatch_flags_but_never_blocks():
    r = SA._prod_snapshot_check(_Client(0.7521), "X", _steps(0.6196))
    assert r["available"] is True
    assert r["matches"] is False
    assert r["delta"] == pytest.approx(0.1325, abs=1e-4)
    # 硬约束：不阻断
    assert "blocked" not in r
    assert "须查同源" in r["note"]


def test_tolerance_boundary():
    # 0.004 内视为一致（平台四舍五入抖动），0.006 视为不同源
    assert SA._prod_snapshot_check(_Client(0.6236), "X", _steps(0.6196))["matches"] is True
    assert SA._prod_snapshot_check(_Client(0.6256), "X", _steps(0.6196))["matches"] is False


def test_missing_gate_step_is_unavailable():
    r = SA._prod_snapshot_check(_Client(0.60), "X",
                                [{"step": "submit_gate", "passed": True}])
    assert r["available"] is False
    assert r.get("matches") is None
    assert "无 prod_gate" in r["note"]


def test_gate_without_value_is_unavailable():
    r = SA._prod_snapshot_check(_Client(0.60), "X",
                                [{"step": "prod_gate", "allowed": True, "prod_max": None}])
    assert r["available"] is False


def test_unfilled_recorded_value_is_unavailable_not_alarm():
    r = SA._prod_snapshot_check(_Client(None), "X", _steps(0.6196))
    assert r["available"] is False
    assert r.get("matches") is None
    assert "尚未回填" in r["note"]


def test_client_exception_fails_open():
    r = SA._prod_snapshot_check(_Client(raises=RuntimeError("boom")), "X", _steps(0.6196))
    assert r["available"] is False
    assert "读取失败" in r["note"]
