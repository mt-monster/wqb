# -*- coding: utf-8 -*-
"""等待 / 退避 / 卡住阈值的唯一来源：wqb.config.WAIT_THRESHOLDS（skills 审查 X-15 / P0-4，2026-09-29）。

此前同一件事有 5 个数：提交后等翻转 40 s / 60 s / 180 s / 2–3 min / 4 min；prod 轮询 15 s×900 s 与 30 s×3600 s；
「卡住」3 分钟 / 60 分钟。且 MCP `submit_alpha` 对**恒 404 的** GET /submit 简短轮询 60 s——每次 POST 白等一分钟；
`super_build.py` 的 `sleep(30)` 分支不可达。
"""
import asyncio
import importlib.util
import inspect
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
for _p in (str(ROOT / "src"), str(ROOT / "world-quant-brain-mcp"),
           str(ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from wqb.config import WAIT_THRESHOLDS as W  # noqa: E402


def test_submit_flip_window_is_240s_and_shared_by_node_and_mcp_tool():
    assert W["submit_flip_wait_s"] == 240 and W["submit_repost_max"] == 1
    from wqb.workflow.nodes import submit_alpha as node
    assert inspect.signature(node.run).parameters["verify_timeout"].default == W["submit_flip_wait_s"]
    assert node._POLL_INTERVAL_SEC == W["submit_flip_poll_s"]
    import tools_workflow
    fn = tools_workflow.workflow_submit_alpha
    fn = getattr(fn, "fn", fn)
    assert inspect.signature(fn).parameters["verify_timeout"].default == W["submit_flip_wait_s"]


def test_prod_corr_poll_constants_match_the_mcp_implementation():
    src = (ROOT / "world-quant-brain-mcp" / "brain_mixin_spcread.py").read_text(encoding="utf-8")
    # 2026-10-28：窗口收成**单一模块常量**。旧版有两处独立字面量（``= 120`` 与
    # ``else 120.0``），本用例只逮到前者 ⇒ 改窗口时另一处静默漏改（inflight TTL 跟着错）。
    assert int(re.search(r"_PROD_CORR_WAIT_S\s*=\s*(\d+)", src).group(1)) == \
        W["prod_corr_timeout_s"]
    assert not re.search(r"max_wait_seconds\s*=\s*\d", src), \
        "窗口不得再写字面量：一律引用 _PROD_CORR_WAIT_S"
    assert src.count("_PROD_CORR_WAIT_S") >= 3, "常量应有 1 个定义 + 2 个使用点"
    assert int(re.search(r"poll_interval\s*=\s*(\d+)", src).group(1)) == W["prod_corr_poll_s"]


def test_prod_corr_window_covers_normal_platform_compute_time():
    """窗口必须覆盖平台**正常**耗时，否则每条真实计算都必然 ``pending``。

    用户口径（2026-10-28）：一次 prod 正常查询 **180–200 s**。
    120 s 的教训：2026-10-28 那次 14h 取证里「成功耗时最大 117 s」不是平台极限，
    而是**被 120 s 窗口截断**——超过窗口的计算一律记 pending，永远进不了成功样本。
    上界防回退：窗口多长就占账号级单槽多久，别回到 900（一次调用堵死整账号 15 分钟）。
    """
    assert 200 <= W["prod_corr_timeout_s"] <= 300


def test_sim_stall_and_timeout_match_the_toolkit_poller():
    from _lib.poller import DEFAULT_POLL
    assert DEFAULT_POLL["stall_minutes"] == W["sim_stall_min"]
    assert DEFAULT_POLL["timeout_minutes"] == W["sim_timeout_min"]


def test_mcp_submit_alpha_does_not_poll_the_dead_submit_endpoint():
    from brain_mixin_simulation import SimulationMixin
    assert not hasattr(SimulationMixin, "_poll_submit_until_resolved")

    calls = []

    class Resp:
        status_code, headers, text = 201, {}, ""

    class Client(SimulationMixin):
        base_url = "https://api.example.invalid"

        def log(self, *a, **k):
            pass

        async def ensure_authenticated(self):
            return True

        async def _request(self, method, url, **kw):
            calls.append((method, url))
            return Resp()

    out = asyncio.run(Client().submit_alpha("ABC123"))
    assert calls == [("POST", "https://api.example.invalid/alphas/ABC123/submit")]     # 只 POST 一次，不再 GET 轮询
    assert out["success"] is True and out["reason"].startswith("Accepted (async)") and out["status_code"] == 201


def test_super_build_has_no_unreachable_sleep_branch():
    text = (ROOT / "tools" / "super_build.py").read_text(encoding="utf-8")
    code = "\n".join(ln for ln in text.splitlines() if not ln.strip().startswith("#"))
    assert "asyncio.sleep(30)" not in code
