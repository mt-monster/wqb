# -*- coding: utf-8 -*-
"""forum_cache_builder 的缓存路径不再写死某个宿主的安装位（skills 审查 RB-04）。"""
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))


def _fresh(monkeypatch, env=None):
    for k in ("WQ_ROBUSTNESS_SKILL_DIR",):
        monkeypatch.delenv(k, raising=False)
    if env:
        monkeypatch.setenv("WQ_ROBUSTNESS_SKILL_DIR", env)
    sys.modules.pop("forum_cache_builder", None)
    return importlib.import_module("forum_cache_builder")


def test_cache_lives_in_the_repo_skill_dir_not_a_host_install_path(monkeypatch):
    mod = _fresh(monkeypatch)
    assert mod.SKILL_DIR == ROOT / "Claude" / "skills" / "brain-alpha-robustness"
    assert ".qoder" not in str(mod.CACHE_FILE) and mod.CACHE_FILE.name == "forum_cache.json"


def test_env_override(monkeypatch, tmp_path):
    mod = _fresh(monkeypatch, str(tmp_path))
    assert mod.SKILL_DIR == tmp_path and mod.CACHE_FILE == tmp_path / "data" / "forum_cache.json"
