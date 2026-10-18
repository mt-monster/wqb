# -*- coding: utf-8 -*-
"""test_skill_no_hyphenated_report_paths.py — 指令源级防守：skill 不得教人写出命名违规。

背景（2026-10-10 第四轮输出目录治理 P1-3）：`brain-alpha-robustness/SKILL.md` 曾把
`tracking/YYYY-MM-DD_robustness.md` / `tracking/<日期>_robustness.md` 写成规范，
每个照 skill 执行的会话都产出 S16 违规文件 —— 同形态**复发 3 次**
（10-06~08 的 4 个被改名、10-09 复发再改、10-10 又复发）。

S16 守的是**磁盘产物**（事后提醒），本测试守**指令源**（事前拦截）：
写进 skill 的路径模板本身必须合规。两边都过，才断得了复发循环。
"""
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
SKILLS = REPO / "Claude" / "skills"

#: 违规形态：带杠日期的报告路径、`YYYY-MM-DD_<主题>.md` 模板、
#: 修复前的真实占位符 `<日期>_robustness`。正则已对全量 skill 语料实测零误报。
#: ⚠ 目录段 2026-10-14 放宽为「报告可能落到的四个目录」而非只 `tracking/`：
#: 稳健性报告的输出位已从 tracking/ 迁到 reports/，若正则仍钉死 tracking/，
#: 这次迁移本身就把这条防守打了个洞（`reports/2026-10-06_x.md` 会静默通过）。
BAD = re.compile(
    r"(?:tracking|reports|output_report|docs)/\d{4}-\d{2}-\d{2}_"
    r"|YYYY-MM-DD_\w*\.md|<日期>_robustness")


@pytest.mark.skipif(not SKILLS.is_dir(), reason="仓库无 Claude/skills（浅克隆裁剪）")
def test_skills_never_teach_hyphenated_date_report_paths():
    hits = []
    for md in SKILLS.rglob("*.md"):
        for i, line in enumerate(md.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if BAD.search(line):
                hits.append(f"{md.relative_to(REPO).as_posix()}:{i}")
    assert not hits, (
        f"skill 文档在教「带杠日期」的报告路径（S16 违规的指令源，照做即复发）：{hits}；"
        "改为 `<主题>_YYYYMMDD.md`（AGENTS.md §8.13）")


def test_robustness_skill_teaches_compliant_report_path():
    """点名守 brain-alpha-robustness 的台账/报告路径模板（复发 3 次的源头）。

    ⚠ 目录位 2026-10-14 由 `tracking/` 改 `reports/`（布局审计 §2.B-3：人工审计/复盘属
    AGENTS.md §8.13 的 `reports/` 桶，`tracking/` 顶层是业务目录；复发由 `audit_structure` S18 拦）。
    本测试的不变量是**命名形态**（日期后缀、无杠、单一每日一份模板），不是目录；
    目录跟着 §8.13 走，命名违规照红。
    """
    skill = SKILLS / "brain-alpha-robustness" / "SKILL.md"
    if not skill.is_file():
        pytest.skip("brain-alpha-robustness skill 不存在")
    text = skill.read_text(encoding="utf-8", errors="replace")
    assert "reports/robustness_YYYYMMDD.md" in text, (
        "报告路径模板应为 reports/robustness_YYYYMMDD.md（日期后缀、无杠；2026-10-14 起输出位在 reports/）")
    assert "tracking/<日期>_robustness.md" not in text, "旧占位符未清干净"
    assert "YYYY-MM-DD_robustness" not in text, "旧带杠模板未清干净"
