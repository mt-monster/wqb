# -*- coding: utf-8 -*-
"""`sync_skills.RETIRED_SKILLS`：已裁定退役的 skill 必须能被 prune 到归档。

为什么需要这张表（2026-10-15 实证）：`prune_orphans` 的第二层判据
`_never_in_repo_history()` 用「`git log --all -- Claude/skills/<name>` 零提交」
识别**宿主原生 skill**，以免把宿主在用的 skill 归档掉。但「在同一个未提交的工作区
状态里建了又删」的 skill **同样零提交** ⇒ 被误判成宿主原生而**永久跳过清理**。

`wq-brain-gatebreak-kor` 就是这个形态：用户 2026-10-15 22:20 裁定「KOR 字段体检 →
归因 → 破闸工作流改由 `wq-brain-ra-kor`（profiles 生成物）承载」，仓库侧当天删除，
7 个宿主入口（6 个物理安装位，`~/.qoder-cn/skills` 是指向 `~/.claude/skills` 的
junction）的副本却因零提交被判 `[user-native]` 留在原地 —— 于是同一套 KOR 六步方法论
以两个 skill 名并存，Agent 按名字调到的是已作废的那份。

这两种形态在 git 里**不可区分**，所以由 `RETIRED_SKILLS` 提供人工反证。
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
SYNC_SKILLS = REPO_ROOT / "tools" / "sync_skills.py"


def _load_sync_skills():
    spec = importlib.util.spec_from_file_location("_sync_skills_under_test", SYNC_SKILLS)
    mod = importlib.util.module_from_spec(spec)
    # 刻意不注册进 sys.modules：`_GuardedModule` 之类的条件安装依赖 sys.modules[__name__]，
    # 注册会与并行导入打架（见 AGENTS.md §8.4 第 9 项的战例）。
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def ss():
    if not SYNC_SKILLS.is_file():
        pytest.skip(f"缺 {SYNC_SKILLS}")
    return _load_sync_skills()


def test_retired_and_protected_are_disjoint(ss):
    """白名单先筛、退役表后筛 ⇒ 交集里的条目会被 protected 吃掉，登记等于没登记。"""
    overlap = set(ss.RETIRED_SKILLS) & set(ss.PROTECTED_ORPHANS)
    assert not overlap, (
        f"这些名字同时在 PROTECTED_ORPHANS 与 RETIRED_SKILLS 里，退役登记会被静默吞掉：{sorted(overlap)}"
    )


def test_retired_entries_carry_a_ruling(ss):
    """每条登记必须写清裁定依据，否则半年后 attic 里的目录无从判断处置方式。"""
    for name, ruling in ss.RETIRED_SKILLS.items():
        assert isinstance(ruling, str) and len(ruling.strip()) >= 20, f"{name} 的裁定依据过短"
        # 依据里要能看出「谁承接了」——只写"已废弃"不解决问题。
        assert any(ch.isdigit() for ch in ruling), f"{name} 的裁定依据缺日期"


def test_retired_names_absent_from_repo_source(ss):
    """登记项若又出现在仓库源里，说明它没退役（或被复活）⇒ 登记表在说谎。"""
    stale = [n for n in ss.RETIRED_SKILLS if (ss.SOURCE / n).exists()]
    assert not stale, f"这些「已退役」名字又出现在 {ss.SOURCE}：{sorted(stale)}（请撤登记或说明）"


def test_retired_beats_native_classification(ss, tmp_path, monkeypatch):
    """核心行为：零提交（native 判据为真）也照样进归档名单，只要它在退役表里。"""
    source = tmp_path / "repo_skills"
    source.mkdir()
    (source / "alive-skill").mkdir()
    (source / "alive-skill" / "SKILL.md").write_text("# alive\n", encoding="utf-8")

    target = tmp_path / "host_skills"
    target.mkdir()
    retired_name = next(iter(ss.RETIRED_SKILLS))
    (target / retired_name).mkdir()
    (target / retired_name / "SKILL.md").write_text("# retired\n", encoding="utf-8")
    (target / "alive-skill").mkdir()
    (target / "alive-skill" / "SKILL.md").write_text("# alive\n", encoding="utf-8")

    monkeypatch.setattr(ss, "SOURCE", source)
    monkeypatch.setattr(ss, "REPO_ROOT", tmp_path / "repo")
    # 让它「像宿主原生」：零提交。没有退役表时这一条会把它永久跳过。
    monkeypatch.setattr(ss, "_never_in_repo_history", lambda name: True)

    dry = ss.prune_orphans(target, apply=False)
    assert retired_name in dry, "退役登记未能压过 native 判定 —— 副本会永久留在安装位"

    moved = ss.prune_orphans(target, apply=True)
    assert retired_name in moved
    assert not (target / retired_name).exists(), "归档应把副本移出安装位"
    # 归档子目录名取的是 `target.resolve().parent.name`（宿主名，如 `.claude`），
    # 不是 target 自己的名字 —— 与被测实现同一口径，别在这里另立一套。
    host = target.resolve().parent.name
    archives = list((tmp_path / "repo" / "attic").glob(f"sync_orphans_*/{host}/{retired_name}"))
    assert len(archives) == 1, f"归档落点异常：{archives}"


def test_archive_records_the_ruling(ss, tmp_path, monkeypatch):
    """归档目录必须自带裁定依据（retired_skills.txt），与 dangling_symlinks.txt 同理。"""
    source = tmp_path / "repo_skills"
    source.mkdir()
    target = tmp_path / "host_skills"
    target.mkdir()
    retired_name = next(iter(ss.RETIRED_SKILLS))
    (target / retired_name).mkdir()
    (target / retired_name / "SKILL.md").write_text("# retired\n", encoding="utf-8")

    monkeypatch.setattr(ss, "SOURCE", source)
    monkeypatch.setattr(ss, "REPO_ROOT", tmp_path / "repo")
    monkeypatch.setattr(ss, "_never_in_repo_history", lambda name: True)

    ss.prune_orphans(target, apply=True)
    host = target.resolve().parent.name
    manifests = list((tmp_path / "repo" / "attic").glob(f"sync_orphans_*/{host}/retired_skills.txt"))
    assert len(manifests) == 1, f"未写出裁定依据：{manifests}"
    text = manifests[0].read_text(encoding="utf-8")
    assert retired_name in text
    assert ss.RETIRED_SKILLS[retired_name][:20] in text


def test_gatebreak_kor_is_registered(ss):
    """本次裁定的具体条目：漏登记就会复发（安装位留着已作废的 KOR 六步方法论）。"""
    assert "wq-brain-gatebreak-kor" in ss.RETIRED_SKILLS
    assert not (ss.SOURCE / "wq-brain-gatebreak-kor").exists(), "仓库侧应已删除"
