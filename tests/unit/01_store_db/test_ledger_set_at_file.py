# -*- coding: utf-8 -*-
"""2026-09-21：`campaign.py ledger set KEY @file.json` 必须支持文件通道（AGENTS.md §5），
与 set-verdict 一致；此前只吃内联 JSON，10KB 中文 region_kb 无法经 CLI 写入。"""
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
TK = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"
if str(TK) not in sys.path:
    sys.path.insert(0, str(TK))

from _lib import ledger as ledger_mod  # noqa: E402


class _Ctx:
    def __init__(self, tmp_path):
        self.region = "TST"
        self.dir = str(tmp_path)
        self.ledger_path = str(tmp_path / "ledger.json")

    def path(self, rel):
        return os.path.join(self.dir, rel)


def _run(ctx, argv, monkeypatch):
    monkeypatch.setenv("WQB_LEDGER_BACKEND", "json")
    return ledger_mod.cli_main(ctx, argv)


def test_set_reads_json_from_at_file_absolute(tmp_path, monkeypatch):
    ctx = _Ctx(tmp_path)
    payload = {"中文": "值", "n": 3, "list": [1, 2]}
    f = tmp_path / "payload.json"
    f.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    rc = _run(ctx, ["set", "region_kb", "@" + str(f)], monkeypatch)
    assert rc in (0, None)
    store = ledger_mod.LedgerStore(ctx.ledger_path)
    assert store.load()["region_kb"] == payload


def test_set_reads_json_from_at_file_relative_to_campaign_dir(tmp_path, monkeypatch):
    ctx = _Ctx(tmp_path)
    (tmp_path / "rel.json").write_text('{"a": 1}', encoding="utf-8")
    rc = _run(ctx, ["set", "k", "@rel.json"], monkeypatch)
    assert rc in (0, None)
    assert ledger_mod.LedgerStore(ctx.ledger_path).load()["k"] == {"a": 1}


def test_set_inline_json_still_works(tmp_path, monkeypatch):
    ctx = _Ctx(tmp_path)
    rc = _run(ctx, ["set", "k2", '{"b": 2}'], monkeypatch)
    assert rc in (0, None)
    assert ledger_mod.LedgerStore(ctx.ledger_path).load()["k2"] == {"b": 2}


def test_set_bad_json_returns_1(tmp_path, monkeypatch):
    ctx = _Ctx(tmp_path)
    assert _run(ctx, ["set", "k3", "not json"], monkeypatch) == 1
    assert _run(ctx, ["set", "k4", "@" + str(tmp_path / "missing.json")], monkeypatch) == 1
