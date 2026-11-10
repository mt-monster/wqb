# -*- coding: utf-8 -*-
"""`PowerPoolSelected` 口径守护（2026-11-08）。

背景：该标签是**平台**在提交成功后自动追加的（11-06 KOR / 11-07 GBR risk68 两次
实证），不是我们的规范缺陷。此前 `check_tags` 把它当违规报「应仅用于真实 PPA
通道」，在 297 颗 ACTIVE 上刷出 36 条假告警（逐颗核实均为平台所打、零退役）。

本文件锁死四条不变量：

1. **不算违规**：`check_tags(["CH_REG","PowerPoolSelected"])` 不得包含 PPA 相关告警，
   只走 `tag_notes` 信息项（不进"有告警"统计）。
2. **提交前剔除**：`_derive_tags` 必须把 `PowerPoolSelected` 从 keep 里剔掉——
   提交前 PATCH 预置它会触发 `PURE_POWER_POOL_THEME`，合法 REGULAR 可能被拒。
   同时 `RETIRE_*` 等人工留痕仍须保留（不能误伤）。
3. **提交后留痕**：`_tag_disposal` 记录平台现状与处置口径（kept / absent），
   且**永不阻断**（提交已 ACTIVE 无法回退）。
4. **精确判定**：`has_ppa_tag` 不做子串匹配（`PowerPoolSelected_old` 不算）。
"""

from __future__ import annotations

from wqb import alpha_properties as ap
from wqb.workflow.nodes import submit_alpha as SA


class _Client:
    def __init__(self, tags=None, raises=None, error=None):
        self._tags = tags or []
        self._raises = raises
        self._error = error

    async def get_alpha_details(self, alpha_id):
        if self._raises:
            raise self._raises
        if self._error:
            return {"__error__": self._error}
        return {"id": alpha_id, "type": "REGULAR", "tags": list(self._tags)}


# ---------------------------------------------------------------- 1. 不算违规

def test_check_tags_no_longer_flags_ppa_tag():
    warns = ap.check_tags(["CH_REG", "SRC_risk68", "PowerPoolSelected"])
    assert not any("PowerPoolSelected" in w for w in warns), warns
    assert warns == []


def test_check_tags_still_flags_real_gaps():
    """撤 PPA 告警不能顺手把真问题也撤掉。"""
    warns = ap.check_tags(["PowerPoolSelected"])
    assert any("缺 CH_*" in w for w in warns)
    assert any("缺 SRC_*" in w for w in warns)


def test_tag_notes_reports_ppa_as_info():
    notes = ap.tag_notes(["CH_REG", "PowerPoolSelected"])
    assert len(notes) == 1
    assert notes[0].startswith("PowerPoolSelected")
    assert "非违规" in notes[0]
    assert ap.tag_notes(["CH_REG"]) == []


def test_tag_notes_real_ppa_channel_is_normal():
    notes = ap.tag_notes(["CH_PPA", "PowerPoolSelected"])
    assert notes and "真 PPA 通道" in notes[0]


# ---------------------------------------------------------------- 2. 提交前剔除

def _patch_client(monkeypatch, client):
    monkeypatch.setattr(SA, "_get_brain_client", lambda: client, raising=False)


def test_derive_tags_strips_ppa_tag(monkeypatch):
    _patch_client(monkeypatch, _Client(tags=["PowerPoolSelected", "RETIRE_20261001"]))
    tags = SA._derive_tags("X", dataset="risk68", wave=None,
                           expr_family="lvlrev", channel="CH_REG")
    assert "PowerPoolSelected" not in tags
    assert "CH_REG" in tags and "SRC_risk68" in tags
    # 人工留痕仍保留
    assert "RETIRE_20261001" in tags


def test_derive_tags_survives_read_failure(monkeypatch):
    _patch_client(monkeypatch, _Client(raises=RuntimeError("boom")))
    tags = SA._derive_tags("X", dataset=None, wave=None,
                           expr_family=None, channel="CH_REG")
    assert "CH_REG" in tags
    assert "PowerPoolSelected" not in tags


# ---------------------------------------------------------------- 3. 提交后留痕

def test_tag_disposal_absent():
    r = SA._tag_disposal(_Client(tags=["CH_REG", "SRC_risk68"]), "X",
                         ["CH_REG", "SRC_risk68"])
    assert r["step"] == "tag_disposal"
    assert r["available"] is True
    assert r["power_pool_selected"] is False
    assert r["disposition"].startswith("absent")
    assert r["pre_submit_has_ppa_tag"] is False
    assert "blocked" not in r


def test_tag_disposal_kept():
    r = SA._tag_disposal(_Client(tags=["CH_REG", "PowerPoolSelected"]), "X", ["CH_REG"])
    assert r["power_pool_selected"] is True
    assert r["disposition"].startswith("kept")


def test_tag_disposal_flags_pre_submit_preset():
    """提交前 PATCH 就带 PPA 标签 = 会触发 PURE_POWER_POOL_THEME，必须留证。"""
    r = SA._tag_disposal(_Client(tags=[]), "X", ["CH_REG", "PowerPoolSelected"])
    assert r["pre_submit_has_ppa_tag"] is True
    assert "PURE_POWER_POOL_THEME" in r["pre_submit_warning"]


def test_tag_disposal_never_blocks_on_read_failure():
    r = SA._tag_disposal(_Client(error="fetch failed"), "X", ["CH_REG"])
    assert r["available"] is False
    assert "blocked" not in r and r["success"] is True

    r2 = SA._tag_disposal(_Client(raises=RuntimeError("net")), "X", ["CH_REG"])
    assert r2["available"] is False and r2["success"] is True


# ---------------------------------------------------------------- 4. 精确判定

def test_has_ppa_tag_exact_membership():
    assert ap.has_ppa_tag(["PowerPoolSelected"]) is True
    assert ap.has_ppa_tag(["PowerPoolSelected_old"]) is False
    assert ap.has_ppa_tag(["my_PowerPoolSelected"]) is False
    assert ap.has_ppa_tag([]) is False
