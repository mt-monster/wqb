# -*- coding: utf-8 -*-
"""`tools/harvest_multisim.py` 收批重试回归测试（2026-09-28）。

背景（实证，勿回退）：
  `GET /simulations/{multisim_id}` 在**并发读同一 multisim 时返回 404**（不是 409/423）。
  实证：pipeline（batch_track）正在轮询这批的同一时刻另起 CLI 收批，21 个 ID 里 20 个
  报 HTTP 404；pipeline 结束后用**同样的 ID、同样的 URL 拼法**重跑，全部 200
  （含当时被误判为「孤儿批」的那只）。直连复现也是 200 → URL 构造无误，404 是平台侧
  瞬态并发假象。

  此前该函数零重试，把瞬态 404 当「该批不存在」，配合 `--auto-upsert` 会**静默丢整批**。

本测试守护：404/5xx/异常按可重试处理（有限次退避），401/403 等确定性失败不重试，
且失败返回里带 `transient_404` 标记与排障提示。
"""
from __future__ import annotations

import asyncio
import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TOOL = REPO / "tools" / "harvest_multisim.py"


def _load_tool():
    """按文件路径加载（tools 非包）。模块导入无副作用：_bootstrap() 只在 main() 内调用。"""
    spec = importlib.util.spec_from_file_location("_harvest_multisim", TOOL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_harvest_multisim"] = mod
    spec.loader.exec_module(mod)
    return mod


class _Resp:
    def __init__(self, status_code, payload=None):
        self.status_code = status_code
        self.text = "{}" if payload is None else "x"
        self._payload = payload if payload is not None else {}

    def json(self):
        return self._payload


class _FakeBrain:
    """按脚本回放状态码；记录调用次数。"""

    base_url = "https://api.worldquantbrain.com"

    def __init__(self, script, children_payload=None):
        self._script = list(script)
        self.calls = 0
        self._children = children_payload or {}

    async def _request(self, method, url, **kw):
        self.calls += 1
        if self._script:
            code = self._script.pop(0)
        else:
            code = 200
        if code == 200:
            # children 形态：一个 child location
            return _Resp(200, {"children": [self._children]})
        return _Resp(code)


def test_transient_404_is_retried_until_success():
    """404 后重试成功：不应把整批判为失败。"""
    hm = _load_tool()
    brain = _FakeBrain([404, 404, 200], children_payload="/simulations/child1")
    # 把 child 状态请求也变成 200（DONE）
    import unittest.mock as mock

    async def fake_child_status(_brain, _loc):
        return {"status": "DONE", "alpha_id": "A1", "location": _loc}

    with mock.patch.object(hm, "fetch_child_status", fake_child_status), \
         mock.patch("asyncio.sleep", new=_no_sleep):
        res = asyncio.run(hm.harvest_one_multisim(brain, "MS1", ids_only=True))

    assert brain.calls >= 3, f"应重试父请求至少 3 次，实际 {brain.calls}"
    assert not res.get("error"), f"重试后应成功，实际 {res.get('error')}"
    assert res.get("child_count") == 1


def test_persistent_404_reports_transient_hint():
    """4 次仍 404 → 返回错误且带 transient_404 标记与排障提示。"""
    hm = _load_tool()
    brain = _FakeBrain([404, 404, 404, 404])
    import unittest.mock as mock

    with mock.patch("asyncio.sleep", new=_no_sleep):
        res = asyncio.run(hm.harvest_one_multisim(brain, "MS2", ids_only=True))

    assert res.get("error"), "持续 404 应报错"
    assert res.get("transient_404") is True
    assert "并发" in str(res.get("error")), "应提示 404 可能是并发抢占"


def test_auth_failure_is_not_retried():
    """401/403 是确定性失败，不重试（避免无谓等待）。"""
    hm = _load_tool()
    brain = _FakeBrain([403, 200])
    import unittest.mock as mock

    with mock.patch("asyncio.sleep", new=_no_sleep):
        res = asyncio.run(hm.harvest_one_multisim(brain, "MS3", ids_only=True))

    assert brain.calls == 1, f"403 不应重试，实际调用 {brain.calls} 次"
    assert res.get("error")
    assert res.get("transient_404") is False


async def _no_sleep(_secs):
    """测试用：跳过退避等待。"""
    return None


def test_salvage_accepts_string_wave():
    """波号是**字符串**（`s2_<ds>_d1` 形态），salvage 不得强转 int。

    缺口：原先写 `int(a.wave)` → 传 `s2_fundamental17_d1` 抛
    `invalid literal for int()`，被 except 吞成 `[salvage] skipped`，
    整波残值静默不入池（本次实证 141 条差点全部丢档）。
    """
    src = TOOL.read_text(encoding="utf-8")
    # 只看**代码行**：修复的注释里会提到被替换掉的 `int(a.wave)` 字样，不能误判
    code_lines = [l.split("#", 1)[0] for l in src.splitlines()]
    code = "\n".join(code_lines)
    assert "int(a.wave)" not in code, "salvage 不得对波号强转 int（SOP 波号是字符串）"
    assert "_salvage_to_pool(a.region, a.wave, all_alphas)" in code, (
        "应以字符串波号直传 _salvage_to_pool")
