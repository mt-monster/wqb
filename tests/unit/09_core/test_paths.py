# -*- coding: utf-8 -*-
"""src/wqb/paths.py 的行为契约（2026-10-04 P2-1）。

本模块存在的理由是「仓库根推导不得依赖文件所在层数」，所以核心断言只有一条：
**同仓库内任意层数的起点，必须解析到同一个根**。
"""
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]     # tests/unit/09_core/本文件 → 仓库根
if str(REPO / "src") not in sys.path:
    sys.path.insert(0, str(REPO / "src"))

from wqb.paths import find_repo_root, repo_relative, repo_root  # noqa: E402


def test_repo_root_is_the_workspace_root():
    assert repo_root() == REPO


def test_depth_independent_across_nested_paths():
    """任意深度/类别的起点都得同一个根 —— 这是本模块的全部意义。"""
    for start in (
        REPO / "tools" / "x.py",
        REPO / "tools" / "data-repair" / "x.py",            # 下沉一层后
        REPO / "Claude" / "skills" / "a" / "scripts" / "y.py",
        REPO / "src" / "wqb" / "store" / "_common.py",
        REPO / "tracking" / "KOR" / "scripts" / "z.py",
    ):
        assert find_repo_root(str(start)) == REPO, start
        assert find_repo_root(str(start.parent)) == REPO, start.parent


def test_directory_and_file_start_are_equivalent():
    as_file = find_repo_root(str(REPO / "tools" / "refs_scan.py"))
    as_dir = find_repo_root(str(REPO / "tools"))
    assert as_file == as_dir == REPO


def test_repo_relative_builds_known_paths():
    assert repo_relative("data", "wqb.db") == REPO / "data" / "wqb.db"
    assert repo_relative("pyproject.toml").is_file()


def test_outside_repo_raises_rather_than_guessing(tmp_path):
    """仓库外必须显式失败：静默返回错误根会让脚本把数据写到别处。"""
    outside = tmp_path / "orphan_script.py"
    outside.write_text("# no repo markers above me\n", encoding="utf-8")
    with pytest.raises(RuntimeError):
        find_repo_root(str(outside))


def test_wqb_root_override_is_honored(monkeypatch):
    monkeypatch.setenv("WQB_ROOT", str(REPO))
    assert find_repo_root() == REPO


def test_wrong_wqb_root_is_not_trusted_silently(monkeypatch, tmp_path):
    """WQB_ROOT 指到无根标记的位置时不得采信（否则脚本会把数据写到那里）。

    这里把起点也放在仓库外，验证两个错叠在一起时是**显式报错**而不是猜一个根。
    """
    monkeypatch.setenv("WQB_ROOT", str(tmp_path / "not_a_repo"))
    outside = tmp_path / "orphan.py"
    outside.write_text("# outside repo\n", encoding="utf-8")
    with pytest.raises(RuntimeError):
        find_repo_root(str(outside))
