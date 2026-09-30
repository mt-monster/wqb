# -*- coding: utf-8 -*-
"""区域三处清单对齐：config.REGIONS ↔ 区域 profile ↔ tracking/<R>/config（skills 审查 RA-12 / RR-09）。

旧文档把「13 个 profile」「14 个 REGIONS」「仅 AMR 未覆盖」写成三种说法且随时过期；实际还有 TWN 有 profile 无 tracking 目录、
AMR 无 profile 却有 tracking/AMR/config——违反 SOP 自己的「开新区前必须补 profile + tracking/<R>/config/」。
这里把**已知缺口显式登记**（同时写在 `references/region-profile-contract.md` §4）：出现新缺口必红；缺口被补上后必须从登记里删。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
from wqb.config import REGIONS  # noqa: E402

PROFILES = ROOT / "Claude" / "skills" / "wq-brain-ra-pipeline" / "references" / "regions"
CONTRACT = ROOT / "Claude" / "skills" / "wq-brain-ra-pipeline" / "references" / "region-profile-contract.md"

#: 已知缺口（区域 → 缺什么）。补上后必须删；新增缺口必须先登记并在 contract §4 写明步 1 的行为。
KNOWN_NO_PROFILE = set()  # AMR profile 已于 2026-09-28 补建（references/regions/AMR.md），缺口关闭
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


# ---------------------------------------------------------------------------
# profile `static` 层 ↔ config.REGIONS（skills 审查 T0-8 残留：EUR 仍列已被平台移除的 ILLIQUID_MINVOL1M、DEU 多列一个 config 没有的 TOP300）
# ---------------------------------------------------------------------------

def _static(region: str) -> dict:
    text = (PROFILES / f"{region}.md").read_text(encoding="utf-8")
    front = re.match(r"^---\n(.*?)\n---", text, re.S).group(1)
    block = re.search(r"^static:\n((?:[ \t]+.*\n?)+)", front + "\n", re.M).group(1)

    def _list(key):
        m = re.search(rf"^\s+{key}:\s*\[([^\]]*)\]", block, re.M)
        return [x.strip().strip("\"'") for x in m.group(1).split(",") if x.strip()] if m else None

    def _scalar(key):
        m = re.search(rf"^\s+{key}:\s*([^\s#]+)", block, re.M)
        return None if (not m or m.group(1) in ("null", "~")) else m.group(1).strip("\"'")

    return {"universe": _list("universe"), "universe_default": _scalar("universe_default"),
            "delay": [int(x) for x in (_list("delay") or [])], "delay_default": _scalar("delay_default")}


def _profile_regions():
    return sorted(r for r in REGIONS if (PROFILES / f"{r}.md").is_file())


def test_profile_static_universe_is_a_subset_of_config_and_defaults_agree():
    """profile 的 `static.universe` 是给人 / assemble-priors 看的；运行时以 `config.REGIONS` 为准。二者不许分叉：
    profile 里出现 config 没有的档位（如已被平台移除的 ILLIQUID_MINVOL1M）会诱导选池；空 `[]` = 「未建立，步 1 强制实测」，合法。"""
    bad = []
    for r in _profile_regions():
        st = _static(r)
        cfg = REGIONS[r]
        assert st["universe"] is not None, f"{r}.md 的 static 缺 universe"
        extra = [u for u in st["universe"] if u not in cfg["universes"]]
        if extra:
            bad.append(f"{r}: profile 多出 {extra}（config 只有 {cfg['universes']}）")
        if st["universe_default"] is not None and st["universe_default"] != cfg["default_universe"]:
            bad.append(f"{r}: universe_default profile={st['universe_default']} ≠ config={cfg['default_universe']}")
    assert not bad, "profile static 层与 config.REGIONS 分叉：\n" + "\n".join(bad)


def test_profile_static_delay_is_a_subset_of_config():
    bad = []
    for r in _profile_regions():
        st = _static(r)
        cfg = REGIONS[r]
        extra = [d for d in st["delay"] if d not in cfg["delays"]]
        if extra:
            bad.append(f"{r}: profile delay 多出 {extra}（config {cfg['delays']}）")
        dd = st["delay_default"]
        if dd is not None and int(dd) not in cfg["delays"]:
            bad.append(f"{r}: delay_default={dd} 不在 config {cfg['delays']}")
    assert not bad, "profile static 层 delay 与 config.REGIONS 分叉：\n" + "\n".join(bad)


def test_the_removed_illiquid_universe_is_not_in_any_profile_front_matter_or_step6_list():
    """ILLIQUID_MINVOL1M：2026-09-22 已从档位表移除、对 USA/ASI/EUR 永久停提。文档里只许以「已移除 / 不得」口吻出现。"""
    warn = re.compile(r"已移除|已被|移除|停提|不得|不可用|不再|禁")
    for p in PROFILES.glob("*.md"):
        lines = p.read_text(encoding="utf-8").splitlines()
        for i, ln in enumerate(lines):
            if "ILLIQUID_MINVOL1M" in ln:
                assert warn.search(" ".join(lines[max(0, i - 2):i + 2])), f"{p.name}:{i + 1} 仍在推荐 ILLIQUID_MINVOL1M"
                assert not ln.lstrip().startswith("universe"), f"{p.name}:{i + 1} static.universe 不得列 ILLIQUID_MINVOL1M"
