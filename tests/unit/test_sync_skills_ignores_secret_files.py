# -*- coding: utf-8 -*-
"""sync_skills 不得把 skill 目录内的密钥类本地文件（.env / .arxiv_llm.env …）复制到安装位（skills 审查 X-15 / OP-04）。"""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import sync_skills  # noqa: E402


@pytest.mark.parametrize("name", [".env", ".arxiv_llm.env", "prod.env", ".env.local", ".env.production"])
def test_secret_like_files_are_ignored(name):
    assert sync_skills._is_ignored(Path("some-skill/scripts") / name)


@pytest.mark.parametrize("name", [".env.example", "config.example.json", "SKILL.md", "environment.md", "arxiv_api.py"])
def test_templates_and_normal_files_still_sync(name):
    assert not sync_skills._is_ignored(Path("some-skill/scripts") / name)
