# -*- coding: utf-8 -*-
"""概念分类学映射表的一致性（skills 审查 RT-01 / RT-05）。

旧表标题写「hypothesis 12 类」，表里只出现 10 个类名（`under_reaction` / `event_conditional` 漏了），
且三个本体 skill 里没有任何东西会在「新增类」时触发同步表。这里守：hypothesis-first 声明的每个类名都在映射表里。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SK = ROOT / "Claude" / "skills"
MAP = SK / "wq-brain-ra-pipeline" / "references" / "concept-taxonomy-map.md"
HYP = SK / "brain-alpha-research-hypothesis-first" / "SKILL.md"


def _declared_classes():
    text = HYP.read_text(encoding="utf-8")
    m = re.search(r"假设类别（12 类.*?）：`([a-z_ /]+)`", text)
    assert m, "hypothesis-first 里找不到「假设类别（12 类…）：`a / b / …`」这一行——格式变了，请同步本测试"
    return [c.strip() for c in m.group(1).split("/") if c.strip()]


def test_hypothesis_first_declares_twelve_classes():
    classes = _declared_classes()
    assert len(classes) == 12 and len(set(classes)) == 12, classes


def test_every_hypothesis_class_is_mapped():
    table = MAP.read_text(encoding="utf-8")
    missing = [c for c in _declared_classes() if f"`{c}`" not in table]
    assert not missing, f"concept-taxonomy-map.md 缺少 hypothesis 类：{missing}"


def test_map_does_not_teach_the_dead_batch_check():
    """批级判重的执行口径是闸 6，`validator.check_batch` 只作方法论参考（零调用方）。"""
    table = MAP.read_text(encoding="utf-8")
    assert "check_batch_diversity" in table
    for line in table.splitlines():
        if "validator.check_batch" in line:
            assert "零调用方" in line or "不构成" in line, line


def test_ontology_skills_link_the_map():
    for name in ("brain-data-feature-engineering", "brain-make-some-gem", "brain-alpha-research-hypothesis-first"):
        text = (SK / name / "SKILL.md").read_text(encoding="utf-8")
        assert "references/concept-taxonomy-map.md)" in text, f"{name}/SKILL.md 应以链接引用概念分类学映射表"
