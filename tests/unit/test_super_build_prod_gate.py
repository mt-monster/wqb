# -*- coding: utf-8 -*-
"""super_build prod 闸单测（2026-09-25 落地）。

用户铁律：**prod ≥ 0.7 不得提交**——即使平台提交层对 SUPER 回带 value>limit 且
result=PASS（GLB 0.8094 / KOR 0.8571 PASS 实证）也不提交；probe 超时 fail-closed。
覆盖：`_prod_gate_verdict` 纯函数判定 + `_probe_prod_max` 轮询行为（假客户端）。
"""
import asyncio
import os
import sys

TOOLS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "tools")
sys.path.insert(0, TOOLS)

from super_build import _prod_gate_verdict, _probe_prod_max  # noqa: E402


# ------------------------------------------------- 判定（纯函数）
def test_block_when_above_threshold():
    allowed, reason = _prod_gate_verdict(0.8571, 0.7)
    assert allowed is False
    assert "0.8571" in reason


def test_block_at_exact_threshold():
    # 用户口径 prod>=0.7 不能提交 → 恰好 0.7 也拒
    allowed, _ = _prod_gate_verdict(0.7, 0.7)
    assert allowed is False


def test_allow_below_threshold():
    allowed, reason = _prod_gate_verdict(0.6999, 0.7)
    assert allowed is True
    assert "过闸" in reason


def test_timeout_fail_closed():
    allowed, reason = _prod_gate_verdict(None, 0.7)
    assert allowed is False
    assert "fail-closed" in reason


def test_custom_threshold():
    allowed, _ = _prod_gate_verdict(0.75, 0.8)
    assert allowed is True


# ------------------------------------------------- 轮询（假客户端）
class _Resp:
    def __init__(self, payload):
        self._p = payload

    def json(self):
        if self._p is None:
            raise ValueError("empty body")
        return self._p


class _FakeBrain:
    def __init__(self, payloads):
        self._payloads = list(payloads)
        self.calls = 0
        self.base_url = "https://api.example.com"
        self.urls = []

    async def _request(self, method, url):
        self.calls += 1
        self.urls.append((method, url))
        p = self._payloads[min(self.calls - 1, len(self._payloads) - 1)]
        return _Resp(p)


def test_probe_returns_max_on_first_response():
    brain = _FakeBrain([{"records": [[0.8, 0.9, 1]], "max": 0.8571, "min": -0.4}])
    mx, n = asyncio.run(_probe_prod_max(brain, "ABC123", timeout_s=5, interval_s=0.01,
                                        log=lambda *_: None))
    assert mx == 0.8571 and n == 1
    assert brain.urls[0][1].endswith("/alphas/ABC123/correlations/prod")


def test_probe_empty_then_filled():
    brain = _FakeBrain([None, {"max": 0.5}])
    mx, n = asyncio.run(_probe_prod_max(brain, "ABC123", timeout_s=5, interval_s=0.01,
                                        log=lambda *_: None))
    assert mx == 0.5 and n == 2


def test_probe_timeout_returns_none():
    brain = _FakeBrain([None])
    mx, n = asyncio.run(_probe_prod_max(brain, "ABC123", timeout_s=0.05,
                                        interval_s=0.01, log=lambda *_: None))
    assert mx is None and n >= 2
