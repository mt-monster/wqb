# -*- coding: utf-8 -*-
"""区域 skill 四目录布局守护（2026-08-18 用户决策：rules/config/references/scripts）。

背景：14 个区域 skill 此前只有 `SKILL.md` + `references/`，rules / config / scripts 三层职责
散落在 SKILL.md 手写区与 `tracking/<R>/` 里，导致：实证叙事寄生在规则层（同 CONTRACT:6 冲突）、
控制值视图无处安放、区域脚本归属不明。2026-10-18 起四目录成为硬布局，本测试把它变成可断言的事实。

守护四件事：
  1. 每个区域 skill 具备 rules / config / scripts 三目录 + 各自 README（references 见下方例外）；
  2. `config/region_view.json` 存在、带 `as_of`、且 `source_of_truth` 指向 `tracking/<R>/config/`；
     region 字段与目录名一致（视图不得张冠李戴）。
  3. SKILL.md 里有四目录导航块（`region-scaffold:nav`）——目录建了却不被检索等于没建。
  4. 例外：`references/` 只在「该区 cells.json 有类别」时要求存在（未开战役的区不建空目录，
     空目录既不会被 git 跟踪，又会在导航块里造死链）。

命名与生命周期：与 `render.check_structure`（孤儿分支文件判据）互补——那条管 references/ 内容，
本条管四目录骨架；两者都不依赖网络与生产库。
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILLS_DIR = REPO_ROOT / "Claude" / "skills"
TRACKING_DIR = REPO_ROOT / "tracking"
NAV_MARK = "<!-- region-scaffold:nav:start -->"


def _region_dirs() -> list[tuple[str, Path]]:
    out = []
    for d in sorted(SKILLS_DIR.glob("wq-brain-ra-*")):
        if d.name == "wq-brain-ra-pipeline" or not (d / "SKILL.md").is_file():
            continue
        out.append((d.name.removeprefix("wq-brain-ra-").upper(), d))
    return out


def _cells(r: str) -> dict:
    p = TRACKING_DIR / r / "config" / "cells.json"
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {}


REGIONS = _region_dirs()


def test_region_skill_set_is_not_empty():
    """目录扫描本身要有效：否则下面的断言会假绿。"""
    assert len(REGIONS) >= 10, f"只扫到 {len(REGIONS)} 个区域 skill，扫描逻辑或目录布局变了"


@pytest.mark.parametrize("region,skill_dir", REGIONS, ids=[r for r, _ in REGIONS])
def test_three_dirs_exist_with_readme(region: str, skill_dir: Path):
    """rules / config / scripts 三目录 + README 必须齐（references 由 cells 决定，见下）。"""
    missing = [f"{sub}/README.md" for sub in ("rules", "config", "scripts") if not (skill_dir / sub / "README.md").is_file()]
    assert not missing, f"{region}: 缺 {missing}（四目录布局未完成或 README 被删）"


@pytest.mark.parametrize("region,skill_dir", REGIONS, ids=[r for r, _ in REGIONS])
def test_config_view_shape(region: str, skill_dir: Path):
    """config/region_view.json：带 as_of、指向真身、region 自洽——它是视图不是事实源。"""
    p = skill_dir / "config" / "region_view.json"
    assert p.is_file(), f"{region}: 缺 config/region_view.json"
    v = json.loads(p.read_text(encoding="utf-8"))
    assert str(v.get("as_of") or "").strip(), f"{region}: region_view.json 缺 as_of（快照类事实必须带失效条件）"
    assert v.get("region") == region, f"{region}: region_view.json 的 region={v.get('region')!r} 与目录不符"
    sot = v.get("source_of_truth") or {}
    for key in ("settings", "thresholds", "cells"):
        target = str(sot.get(key) or "")
        assert target.startswith(f"tracking/{region}/config/"), (
            f"{region}: region_view.json 的 source_of_truth.{key}={target!r} 未指向本区真身目录"
        )


@pytest.mark.parametrize("region,skill_dir", REGIONS, ids=[r for r, _ in REGIONS])
def test_skill_md_has_scaffold_nav(region: str, skill_dir: Path):
    """目录建了却不被检索等于没建：SKILL.md 必须有四目录导航块。"""
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    assert NAV_MARK in text, f"{region}: SKILL.md 缺四目录导航块（{NAV_MARK}）"
    for sub in ("rules", "config", "scripts"):
        assert f"]({sub}/README.md)" in text, f"{region}: 导航块未链到 {sub}/README.md"


@pytest.mark.parametrize("region,skill_dir", REGIONS, ids=[r for r, _ in REGIONS])
def test_references_dir_matches_cells(region: str, skill_dir: Path):
    """references/ 的存在条件由 cells.json 决定：有类别 ⇒ 必须有卡；无类别（未开战役）⇒ 不建空目录。"""
    cats = _cells(region).get("cells") or {}
    refs = skill_dir / "references"
    if cats:
        assert refs.is_dir(), f"{region}: cells.json 有 {len(cats)} 个类别但没有 references/"
        missing = [f"{cat}.md" for cat in cats if not (refs / f"{cat}.md").is_file()]
        assert not missing, f"{region}: 缺组合分支卡 {missing}（跑 $WQ_PY -m wqb.profiles render --region {region} --apply）"
    else:
        assert not refs.is_dir(), (
            f"{region}: 无 cells 类别却建了 references/——空目录不会被 git 跟踪，且会在导航块里造死链"
        )