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


# ------------------------------------------------- CLI 缺省（skills 审查 SP-17）
def test_select_requires_explicit_neutralization(monkeypatch, capsys):
    """`--neutralization` 无缺省：SUBINDUSTRY 只是 USA / GLB 的已知最优，KOR / IND 是 STATISTICAL，缺省会把人引向错误起点。"""
    import super_build
    monkeypatch.setattr(sys, "argv", ["super_build.py", "select", "--region", "KOR"])
    monkeypatch.setattr(super_build, "_bootstrap", lambda: None)
    try:
        super_build.main()
    except SystemExit as e:
        assert e.code == 2
    else:  # pragma: no cover
        raise AssertionError("缺 --neutralization 应被 argparse 拒绝")
    assert "--neutralization" in capsys.readouterr().err


def test_universe_and_delay_come_from_config_not_a_hardcoded_top400():
    """旧缺省 `--universe TOP400` 只对 MEA 合法；非法档位平台回 HTTP 500 且无提示。"""
    import super_build
    assert super_build.resolve_universe_delay("KOR") == ("TOP600", 1)
    uni, dly = super_build.resolve_universe_delay("usa")
    assert uni == "TOP3000" and dly in (0, 1)
    assert super_build.resolve_universe_delay("HKG", "TOP500", 1) == ("TOP500", 1)


def test_illegal_universe_or_region_is_refused_with_the_legal_list():
    import pytest
    import super_build
    with pytest.raises(ValueError, match="合法 universe"):
        super_build.resolve_universe_delay("KOR", "TOP3000")
    with pytest.raises(ValueError, match="合法 delay"):
        super_build.resolve_universe_delay("ASI", None, 0)
    with pytest.raises(ValueError, match="未知区域"):
        super_build.resolve_universe_delay("XXX")


def test_select_accepts_full_expression_overrides(monkeypatch):
    """--selection / --combo 覆盖模板（workflow_superalpha 的同名参数经此生效）。"""
    import super_build
    seen = {}

    async def fake_select(a):
        seen["a"] = a
        return 0

    monkeypatch.setattr(super_build, "cmd_select", fake_select)
    monkeypatch.setattr(super_build, "_bootstrap", lambda: None)
    monkeypatch.setattr(sys, "argv", ["super_build.py", "select", "--region", "KOR",
                                      "--neutralization", "STATISTICAL",
                                      "--selection", "SEL", "--combo", "CMB"])
    assert super_build.main() == 0
    assert seen["a"].selection == "SEL" and seen["a"].combo == "CMB"
    assert seen["a"].universe is None and seen["a"].delay is None   # 缺省交给 config 解析
