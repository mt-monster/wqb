# -*- coding: utf-8 -*-
"""tools/submit_batch.py 的收尾口径：**不许再把失败报成 ALL SUBMITTED**。

2026-10-24 实证：insd_trx_w1 首派 ILLIQUID_MINVOL1M，平台 10/10 条 400
（`Universe ILLIQUID_MINVOL1M is not available.`），脚本尾行仍是 `ALL SUBMITTED`。
这个假回执在本仓已被踩过 7+ 次（.clinerules/memory.md、.workbuddy/memory 多篇），
所以这里按「退出码 + 末行」两条同时钉住：
  - 201 ⇒ 不抛、末行 `ALL SUBMITTED`；
  - 非 201 ⇒ `SystemExit(1)`、末行是 FAILED 而不是 ALL SUBMITTED。
"""
from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
MOD_PATH = REPO_ROOT / "tools" / "submit_batch.py"


def _load_mod():
    spec = importlib.util.spec_from_file_location("_t_submit_batch", MOD_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


class _Resp:
    def __init__(self, status_code: int, text: str = "", location: str = ""):
        self.status_code = status_code
        self.text = text
        self.headers = {"Location": location} if location else {}


def _install_fake_brain_api(monkeypatch, resp: _Resp):
    holder = types.SimpleNamespace(resp=resp)

    class _FakeClient:
        base_url = "https://api.worldquantbrain.com"

        def __init__(self):
            pass

        async def ensure_authenticated(self):
            return True

        def _retry_wait_seconds(self, _resp, _attempt):
            return 0

        async def _request(self, *_a, **_k):
            return holder.resp

    fake = types.ModuleType("brain_api")
    fake.BrainApiClient = _FakeClient
    monkeypatch.setitem(sys.modules, "brain_api", fake)
    return holder


def _prepare(tmp_path, monkeypatch):
    mod = _load_mod()
    # run() 会 os.chdir(MCP_DIR)；指到临时目录，避免测试期切进真实 MCP 包。
    monkeypatch.setattr(mod, "MCP_DIR", str(tmp_path), raising=True)
    expr_file = tmp_path / "e.txt"
    expr_file.write_text("ts_zscore(ts_sum(total_buy_transaction_count, 42), 252)\n",
                         encoding="utf-8")
    batch = [("e.txt", str(expr_file), 5, "SUBINDUSTRY",
              {"region": "USA", "universe": "TOP3000"})]
    return mod, batch


def test_non_201_raises_and_never_prints_all_submitted(tmp_path, monkeypatch, capsys):
    mod, batch = _prepare(tmp_path, monkeypatch)
    _install_fake_brain_api(
        monkeypatch,
        _Resp(400, '{"settings":{"universe":["Universe X is not available."]}}'),
    )
    with pytest.raises(SystemExit) as ei:
        mod.asyncio.run(mod.run(batch, sleep=0, dry_run=False))
    assert ei.value.code == 1
    out = capsys.readouterr().out
    assert "ALL SUBMITTED" not in out
    assert "PARTIAL/FAILED" in out
    assert "status=400" in out


def test_201_prints_all_submitted_with_location(tmp_path, monkeypatch, capsys):
    mod, batch = _prepare(tmp_path, monkeypatch)
    _install_fake_brain_api(
        monkeypatch,
        _Resp(201, "", "https://api.worldquantbrain.com/simulations/abc123"),
    )
    mod.asyncio.run(mod.run(batch, sleep=0, dry_run=False))
    out = capsys.readouterr().out
    assert "ALL SUBMITTED" in out
    assert "abc123" in out
