# -*- coding: utf-8 -*-
"""``PowerPoolSelected`` ≠ PPA 通道（2026-11-10 实证修正）。

背景：平台会给 **REGULAR / RA** 提交成功的 alpha 自动追加 ``PowerPoolSelected``
（``P0obGoQJ`` 实证），用户也可在提交后 PATCH 增删该标签做 PP 池治理
（11-10 对 ``O07AMoKR`` / ``JjeMlmXA`` 的实测）。增删标签**不改变** ``type``，
也**不改变**平台 ``themes`` —— 全账户 301 颗 ACTIVE 中仅 1 颗命中当期
``GLB/D1 Power Pool Nov`26`` 主题，其余带标签货命中 Sept/Oct/Aug **往期**主题。

⇒ 该标签是「PP 池成分开关」，不是通道证据。旧 ``is_ppa_alpha`` 与
``tools/alpha_properties.py normalize`` 据此推 CH_PPA 会把 RA alpha 误标成 PPA，
违反用户「RA 是唯一可接受通道」的政策，也会给补标签的 CH_REG 货错打通道。

本文件锁死四条不变量：
1. 通道判定只认 ``type=PPA`` 或 ``CH_PPA``；
2. 单独 ``PowerPoolSelected`` / ``CH_REG``+标签 一律 **不算 PPA**；
3. ``decide()`` 的 ``is_ppa`` / ``ppa_tag_only`` 报告字段同步正确；
4. ``tag_notes`` 必须点明 themes 与标签是两个独立条件。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from wqb import alpha_properties as ap  # noqa: E402
from wqb.submit_verdict_core import decide, is_ppa_alpha  # noqa: E402


# ---------------------------------------------------------------- 1/2 通道判定

def test_type_ppa_is_ppa_channel():
    assert is_ppa_alpha({"type": "PPA"}) is True


def test_ch_ppa_is_ppa_channel():
    assert is_ppa_alpha({"type": "REGULAR", "tags": ["CH_PPA", "PowerPoolSelected"]}) is True


@pytest.mark.parametrize("tags", [
    ["PowerPoolSelected"],
    ["CH_REG", "SRC_risk68", "PowerPoolSelected"],
    ["CH_REG", "SRC_analyst7", "CORR_MID"],
    [],
])
def test_pool_tag_alone_is_not_ppa_channel(tags):
    """平台自动追加标签 / 手动补标签的 RA alpha 不得被判成 PPA。"""
    assert is_ppa_alpha({"type": "REGULAR", "tags": tags}) is False


def test_substring_variants_are_not_channels():
    assert is_ppa_alpha({"type": "REGULAR", "tags": ["PowerPoolSelected_old"]}) is False
    assert is_ppa_alpha({"type": "REGULAR", "tags": ["my_CH_PPA"]}) is False


# ---------------------------------------------------------------- 3 decide 报告字段

def test_decide_already_submitted_reports_ra_not_ppa():
    d = {
        "status": "ACTIVE", "type": "REGULAR",
        "tags": ["CH_REG", "SRC_dl_riskfree_returns", "PowerPoolSelected"],
        "is": {"checks": []},
    }
    r = decide("P0obGoQJ", d, None, [])
    assert r["verdict"] == "ALREADY_SUBMITTED"
    assert r["is_ppa"] is False
    assert r["ppa_tag_only"] is False
    assert r["ppa_channel"] is False


# ---------------------------------------------------------------- 4 tag_notes 口径

def test_tag_notes_mentions_themes_independence():
    notes = ap.tag_notes(["CH_REG", "PowerPoolSelected"])
    assert len(notes) == 1
    assert notes[0].startswith("PowerPoolSelected")
    assert "themes" in notes[0]
    assert "非违规" in notes[0]


def test_normalize_no_longer_infers_channel_from_pool_tag():
    """源码守卫：normalize 不得再用 PowerPoolSelected 推 CH_PPA。"""
    src = (ROOT / "tools" / "alpha_properties.py").read_text(encoding="utf-8")
    body = "\n".join(l for l in src.splitlines() if not l.strip().startswith("#"))
    assert not re.search(r'"PowerPoolSelected"\s+in\s+old_tags', body), (
        "normalize 仍把 PP 池标签当通道证据，会给 CH_REG 货错打 CH_PPA")
    assert re.search(r'"CH_PPA"\s+in\s+old_tags', body)
