# -*- coding: utf-8 -*-
"""proxy_mode 单元测试：配置读写 + 进程 env 应用（不联网）。

2026-11-07 起因：代理关掉后 HTTP(S)_PROXY 仍指向死端口 127.0.0.1:7897，
平台靠 NO_PROXY 无碍，但论坛通道会回落读它而打空 —— 本模块负责一键切换。
"""
import os

import pytest

import proxy_mode as pm

_PROXY_VARS = ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy")


@pytest.fixture()
def mode_file(tmp_path, monkeypatch):
    path = tmp_path / "proxy_mode.json"
    monkeypatch.setenv("WQB_PROXY_MODE_FILE", str(path))
    return path


def test_default_is_auto_when_no_config(mode_file):
    cfg = pm.read_config()
    assert cfg["mode"] == "auto"
    assert cfg["proxy_url"].startswith("http")


def test_write_rejects_unknown_mode(mode_file):
    with pytest.raises(ValueError):
        pm.write_config("maybe")


def test_write_then_read_roundtrip(mode_file):
    pm.write_config("on", "http://127.0.0.1:7999")
    got = pm.read_config()
    assert got["mode"] == "on"
    assert got["proxy_url"] == "http://127.0.0.1:7999"


def test_off_clears_proxy_env_and_sets_forum_bypass(mode_file, monkeypatch):
    for key in _PROXY_VARS:
        monkeypatch.setenv(key, "http://127.0.0.1:7897")
    pm.apply(pm.write_config("off"))
    for key in _PROXY_VARS:
        assert key not in os.environ
    assert os.environ["WQB_FORUM_BYPASS_PROXY"] == "1"


def test_on_sets_proxy_env_and_clears_bypass(mode_file, monkeypatch):
    monkeypatch.setenv("WQB_FORUM_BYPASS_PROXY", "1")
    pm.apply(pm.write_config("on", "http://127.0.0.1:7890"))
    assert os.environ["HTTPS_PROXY"] == "http://127.0.0.1:7890"
    assert os.environ["https_proxy"] == "http://127.0.0.1:7890"
    assert "WQB_FORUM_BYPASS_PROXY" not in os.environ


def test_auto_does_not_touch_env(mode_file, monkeypatch):
    monkeypatch.setenv("HTTPS_PROXY", "http://127.0.0.1:7897")
    pm.apply(pm.write_config("auto"))
    assert os.environ["HTTPS_PROXY"] == "http://127.0.0.1:7897"


def test_snapshot_reports_forum_bypass(mode_file):
    pm.apply(pm.write_config("off"))
    snap = pm.snapshot()
    assert snap["forum_bypass"] is True
    assert snap["config"]["mode"] == "off"


def test_resolve_proxy_url_honours_bypass(monkeypatch):
    ff = pytest.importorskip("forum_functions")
    monkeypatch.setenv("FORUM_SETTINGS_PROXY", "http://127.0.0.1:7897")
    monkeypatch.delenv("WQB_FORUM_BYPASS_PROXY", raising=False)
    assert ff._resolve_proxy_url() == "http://127.0.0.1:7897"
    monkeypatch.setenv("WQB_FORUM_BYPASS_PROXY", "1")
    assert ff._resolve_proxy_url() is None
