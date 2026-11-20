# -*- coding: utf-8 -*-
"""super_build prod 闸单测（2026-09-25 落地）。

用户铁律：**prod ≥ 0.7 不得提交**——即使平台提交层对 SUPER 回带 value>limit 且
result=PASS（GLB 0.8094 / KOR 0.8571 PASS 实证）也不提交；probe 超时 fail-closed。
覆盖：`_prod_gate_verdict` 纯函数判定 + `_probe_prod_max` 轮询行为（假客户端）。
"""
import asyncio
import os
import sys

import pytest

TOOLS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
    "tools")
sys.path.insert(0, TOOLS)

from super_build import _prod_gate_verdict, _probe_prod_max  # noqa: E402


@pytest.fixture(autouse=True)
def _isolate_correlation_slot(tmp_path, monkeypatch):
    """隔离跨进程锁目录（2026-10-22）。

    `_probe_prod_max` 现在会申请平台「账号级单并发槽」（`wqb.correlation_slot`,
    token 落在 `logs/_dblock/correlation.lock.json`）。不隔离就会读到**本机真实在跑**
    的相关性查询 token ⇒ 假客户端用例全部 fail-fast 拿到 `(None, 0)`。
    这里把锁目录指到 `tmp_path`，保证用例只验证轮询逻辑本身。
    """
    monkeypatch.setenv("WQB_DBLOCK_DIR", str(tmp_path / "_dblock"))
    monkeypatch.delenv("WQB_DBLOCK_DISABLE", raising=False)


# ------------------------------------------------- 判定（纯函数）
@pytest.mark.parametrize("value,threshold,allowed,reason_sub", [
    (0.8571, 0.7, False, "0.8571"),   # 超阈值拒
    (0.7, 0.7, False, None),          # 恰好等于也拒（用户口径 >= 不提交）
    (0.6999, 0.7, True, "过闸"),       # 低于阈值放行
    (None, 0.7, False, "fail-closed"), # 探针超时 fail-closed
    (0.75, 0.8, True, None),          # 自定义阈值
])
def test_prod_gate_verdict(value, threshold, allowed, reason_sub):
    got_allowed, reason = _prod_gate_verdict(value, threshold)
    assert got_allowed is allowed
    if reason_sub:
        assert reason_sub in reason


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


# ------------------------------------------- 残留锁分因（2026-11-17 事故回归）
def test_probe_waits_out_known_cooldown_instead_of_giving_up():
    """**事故回归**：上一轮计算留下的 195s 冷却（写入进程已退出）曾被当成「别的进程
    占着槽」直接 attempts=0 放弃，人工等 TTL 重跑才成功。

    冷却时长是**已知的**，应在窗口内等它到期再抢，而不是 fail-closed。
    """
    from wqb import correlation_slot as cs
    cs.write_cooldown(0.2)
    brain = _FakeBrain([{"max": 0.55}])
    logs = []
    mx, n = asyncio.run(_probe_prod_max(brain, "ABC123", timeout_s=10, interval_s=0.01,
                                        log=logs.append))
    assert mx == 0.55 and n == 1
    assert any("冷却" in s for s in logs)


def test_probe_fail_closed_when_holder_is_alive():
    """存活进程持槽 ⇒ 仍 fail-fast、不排队（原设计不变量，不得被冷却修复放宽）。"""
    import json
    from wqb import correlation_slot as cs
    info = cs.acquire("holder")
    tok = cs.slot_path()
    data = json.loads(open(tok, encoding="utf-8").read())
    data["pid"] = os.getppid()
    open(tok, "w", encoding="utf-8").write(json.dumps(data))

    brain = _FakeBrain([{"max": 0.55}])
    logs = []
    mx, n = asyncio.run(_probe_prod_max(brain, "ABC123", timeout_s=2, interval_s=0.01,
                                        log=logs.append))
    assert (mx, n) == (None, 0)
    assert brain.calls == 0                       # 没抢到槽 ⇒ 一个请求都不许发
    assert any("存活" in s for s in logs)
    cs.release(info["token"], cooldown=False)


def test_probe_fail_closed_when_platform_unavailable(monkeypatch):
    from wqb import correlation_slot as cs
    monkeypatch.setenv("WQB_CORR_UNAVAILABLE_STREAK", "1")
    cs.note_pending_streak("ABC123")
    brain = _FakeBrain([{"max": 0.55}])
    mx, n = asyncio.run(_probe_prod_max(brain, "ABC123", timeout_s=2, interval_s=0.01,
                                        log=lambda *_: None))
    assert (mx, n) == (None, 0)
    cs.clear_unavailable()


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
