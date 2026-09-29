# -*- coding: utf-8 -*-
"""区域三处清单对齐：config.REGIONS ↔ 区域 profile ↔ tracking/<R>/config（skills 审查 RA-12 / RR-09）。

旧文档把「13 个 profile」「14 个 REGIONS」「仅 AMR 未覆盖」写成三种说法且随时过期；实际还有 TWN 有 profile 无 tracking 目录、
AMR 无 profile 却有 tracking/AMR/config——违反 SOP 自己的「开新区前必须补 profile + tracking/<R>/config/」。
这里把**已知缺口显式登记**（同时写在 `references/region-profile-contract.md` §4）：出现新缺口必红；缺口被补上后必须从登记里删。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from wqb.config import REGIONS  # noqa: E402

PROFILES = ROOT / "Claude" / "skills" / "wq-brain-ra-pipeline" / "references" / "regions"
CONTRACT = ROOT / "Claude" / "skills" / "wq-brain-ra-pipeline" / "references" / "region-profile-contract.md"

#: 已知缺口（区域 → 缺什么）。补上后必须删；新增缺口必须先登记并在 contract §4 写明步 1 的行为。
KNOWN_NO_PROFILE = {"AMR"}
KNOWN_NO_TRACKING = {"TWN"}


def _profiles():
    return {p.stem for p in PROFILES.glob("*.md")}


def _tracking():
    return {p.parent.parent.name for p in (ROOT / "tracking").glob("*/config/thresholds.json")}


def test_no_profile_gap_is_exactly_the_registered_one():
    missing = set(REGIONS) - _profiles()
    assert missing == KNOWN_NO_PROFILE, (
        f"缺 profile 的区域 {sorted(missing)} ≠ 登记 {sorted(KNOWN_NO_PROFILE)}：补 profile，或更新登记与 contract §4")


def test_no_tracking_gap_is_exactly_the_registered_one():
    missing = set(REGIONS) - _tracking()
    assert missing == KNOWN_NO_TRACKING, (
        f"缺 tracking/<R>/config 的区域 {sorted(missing)} ≠ 登记 {sorted(KNOWN_NO_TRACKING)}")


def test_no_orphan_profiles_or_tracking_dirs():
    assert _profiles() <= set(REGIONS)
    assert _tracking() <= set(REGIONS)


def test_contract_section_lists_the_gaps():
    text = CONTRACT.read_text(encoding="utf-8")
    sec = text[text.index("## 4. 区域缺口"):]
    for r in KNOWN_NO_PROFILE | KNOWN_NO_TRACKING:
        assert re.search(rf"\|\s*{r}\s*\|", sec), f"contract §4 没有登记 {r} 的缺口"
