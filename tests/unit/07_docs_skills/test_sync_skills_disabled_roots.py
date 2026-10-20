# -*- coding: utf-8 -*-
"""`sync_skills.DISABLED_INSTALL_ROOTS`：用户裁定的安装位不得被同步回填。

2026-10-20 实证：用户清空 `~/.cursor/skills` 后，6 分钟内被一次
`python tools/sync_skills.py` 回填 51 项。只删内容不解决问题 —— 必须在
自动枚举与显式 `--target` 两条路径上都拒绝。
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
SYNC_SKILLS = REPO_ROOT / "tools" / "sync_skills.py"


def _load_sync_skills():
    spec = importlib.util.spec_from_file_location("_sync_skills_disabled_under_test", SYNC_SKILLS)
    mod = importlib.util.module_from_spec(spec)
    # 刻意不注册进 sys.modules：理由同 test_sync_skills_retired.py。
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def ss():
    if not SYNC_SKILLS.is_file():
        pytest.skip(f"缺 {SYNC_SKILLS}")
    return _load_sync_skills()


def test_cursor_root_is_disabled_by_user_decision(ss):
    cursor = Path.home() / ".cursor" / "skills"
    assert cursor.resolve() in ss.DISABLED_INSTALL_ROOTS, (
        "用户 2026-10-20 裁定不再维护 Cursor 安装位；若确需恢复，先删这条断言与登记"
    )
    assert ss.DISABLED_INSTALL_ROOTS[cursor.resolve()]


def test_tilde_form_is_recognized(ss):
    """`--target ~/.cursor/skills` 不得因未展开波浪号而绕过关闭登记。"""
    assert ss._disabled_reason(Path("~/.cursor/skills")) is not None


def test_automatic_resolution_skips_disabled_root(ss, tmp_path, monkeypatch):
    disabled = tmp_path / "cursor" / "skills"
    allowed = tmp_path / "claude" / "skills"
    disabled.mkdir(parents=True)
    allowed.mkdir(parents=True)
    monkeypatch.setattr(ss, "DISABLED_INSTALL_ROOTS", {disabled.resolve(): "test"})
    monkeypatch.setattr(ss, "_candidate_roots", lambda: [disabled, allowed])

    assert ss.resolve_install_roots() == [allowed]


def test_tilde_explicit_target_is_refused_as_disabled(ss, monkeypatch, capsys):
    """CLI 的波浪号写法不得被误判成「与仓库相关」而掩盖关闭原因。"""
    monkeypatch.setattr(sys, "argv", ["sync_skills.py", "--target", "~/.cursor/skills"])

    assert ss.main() == 2
    assert "已关闭的安装位" in capsys.readouterr().err


def test_explicit_target_is_refused_before_write(ss, tmp_path, monkeypatch, capsys):
    disabled = tmp_path / "cursor" / "skills"
    disabled.mkdir(parents=True)
    monkeypatch.setattr(ss, "DISABLED_INSTALL_ROOTS", {disabled.resolve(): "test"})
    monkeypatch.setattr(sys, "argv", ["sync_skills.py", "--target", str(disabled)])

    assert ss.main() == 2
    assert "已关闭的安装位" in capsys.readouterr().err
    # 拒绝必须发生在写盘前：目标目录仍为空。
    assert list(disabled.iterdir()) == []
