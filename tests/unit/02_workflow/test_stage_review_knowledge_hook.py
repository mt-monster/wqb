# -*- coding: utf-8 -*-
"""toolkit `_lib/knowledge.py` 薄壳的委托行为（2026-11-15 P1）。

薄壳只做委托：store 的取用与关闭在 shim，判定逻辑全在 `wqb.knowledge.capture`。
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLKIT = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"
if str(TOOLKIT) not in sys.path:
    sys.path.insert(0, str(TOOLKIT))


class _FakeStore:
    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True


class _Ctx:
    region = "KOR"
    dir = "tracking/KOR"


def test_refresh_from_review_delegates_and_closes(monkeypatch):
    import _lib.knowledge as shim
    import _lib.wqb_store as ws
    import wqb.knowledge.capture as cap

    fake = _FakeStore()
    seen = {}

    def fake_get_store(ctx):
        seen["ctx"] = ctx
        return fake

    def fake_refresh(store, region, wave, **kwargs):
        seen.update({"store": store, "region": region, "wave": wave, "kwargs": kwargs})
        return {"written": 1, "records": 1}

    monkeypatch.setattr(ws, "get_store", fake_get_store)
    monkeypatch.setattr(cap, "refresh_attempt_knowledge", fake_refresh)

    out = shim.refresh_from_review(_Ctx(), "101", [{"alpha_id": "A1"}],
                                   settings={"universe": "TOP600"},
                                   thresholds={"near_sharpe_min": 1.0})
    assert out == {"written": 1, "records": 1}
    assert seen["region"] == "KOR" and seen["wave"] == "101"
    assert seen["kwargs"]["settings"] == {"universe": "TOP600"}
    assert fake.closed is True


def test_shim_degrades_when_wqb_missing(monkeypatch):
    import _lib.knowledge as shim

    # 模拟“技能装在仓库外”：capture 导入失败
    monkeypatch.setattr(shim, "_warn_once", lambda: None)
    import builtins
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "wqb.knowledge.capture":
            raise ImportError("wqb not available")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    assert shim.refresh_from_review(_Ctx(), "101", []) is None


def test_write_digest_delegates_region_path(monkeypatch, tmp_path):
    import _lib.knowledge as shim
    import _lib.wqb_store as ws
    import wqb.knowledge.digest as dg

    fake = _FakeStore()
    seen = {}
    monkeypatch.setattr(ws, "get_store", lambda ctx: fake)

    def fake_write(store, region, path):
        seen.update({"store": store, "region": region, "path": path})
        return {"path": path, "region": region}

    monkeypatch.setattr(dg, "write_region_digest", fake_write)
    ctx = _Ctx()
    ctx.dir = str(tmp_path / "tracking" / "KOR")
    out = shim.write_digest(ctx)
    assert out["path"].replace("\\", "/").endswith("priors/experience_digest.md")
    assert seen["region"] == "KOR" and fake.closed is True
