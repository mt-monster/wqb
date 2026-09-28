# -*- coding: utf-8 -*-
"""守护 docs/experience/ 挖掘经验库不被架空（2026-09-29 建立）。

背景：经验库建成时，01-05 五篇在 skills / 回测流程里**零引用**——纯软文档无人读，
等于没写。本测试把"被引用"变成可断言的事实，防止后续重构静默删锚点让资料库退化成死文档。

守护三件事：
  1. 六篇文件都在（README 索引 + 01-05 分类篇）；
  2. 每篇至少被一个**权威引用源**（AGENTS.md / README.md / Claude/skills/**/*.md）提到；
  3. 机器消费层 methodology_rules.json 里经验条目声明的 doc 路径真实存在（双轨同源校验）。

引用源不含 docs/experience/ 自身（自引不算引用），也不含 attic/ output_report/ tracking/
等归档与产物目录（那里的旧引用不代表流程会读）。
"""
import json
import os
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = REPO_ROOT / "docs" / "experience"
RULES_JSON = (
    REPO_ROOT
    / "Claude"
    / "skills"
    / "wq-brain-campaign-toolkit"
    / "config"
    / "methodology_rules.json"
)

# 经验库六篇（README 是索引，01-05 是分类实证篇）
KB_FILES = [
    "README.md",
    "01_platform_gates.md",
    "02_signal_patterns.md",
    "03_region_dataset.md",
    "04_engineering.md",
    "05_antipatterns.md",
]

# 权威引用源：这些地方被 Agent / 人实际读取，出现文件名才算"接进流程"
REF_FILES = [
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "README.md",
]
SKILLS_DIR = REPO_ROOT / "Claude" / "skills"


def _ref_source_texts():
    """收集权威引用源的文本（只读 .md，跳过 __pycache__ 与非文档）。"""
    texts = {}
    for p in REF_FILES:
        if p.exists():
            texts[str(p)] = p.read_text(encoding="utf-8", errors="ignore")
    if SKILLS_DIR.exists():
        for p in SKILLS_DIR.rglob("*.md"):
            if "__pycache__" in p.parts:
                continue
            texts[str(p)] = p.read_text(encoding="utf-8", errors="ignore")
    return texts


def test_experience_kb_files_exist():
    """六篇文件必须存在——缺一篇就是资料库被误删。"""
    missing = [f for f in KB_FILES if not (DOCS_DIR / f).exists()]
    assert not missing, f"经验库缺文件: {missing}（目录 {DOCS_DIR}）"


def test_experience_kb_files_not_gitignored():
    """经验库必须可入库；被 .gitignore 吞掉等于下次 clone 后流程引用全部落空。"""
    import subprocess

    try:
        out = subprocess.run(
            ["git", "check-ignore", "--stdin"],
            input="\n".join(f"docs/experience/{f}" for f in KB_FILES),
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
    except (OSError, subprocess.SubprocessError):
        pytest.skip("git 不可用，跳过 ignore 校验")

    if out.returncode == 1:  # 1 = 无匹配 = 全部未被忽略
        return
    ignored = [ln for ln in out.stdout.splitlines() if ln.strip()]
    assert not ignored, f"经验库文件被 .gitignore 忽略，无法入库: {ignored}"


@pytest.mark.parametrize("fname", KB_FILES)
def test_each_kb_file_is_referenced_by_pipeline(fname):
    """每篇至少被一个权威引用源提到。

    这是本文件的核心断言：**没有引用的经验 = 死文档**。
    若你重构 skill 时删掉了锚点，这里会红——补回锚点，不要删测试。
    """
    texts = _ref_source_texts()
    hit = [src for src, txt in texts.items() if fname in txt]
    assert hit, (
        f"`docs/experience/{fname}` 在 AGENTS.md / README.md / Claude/skills/**/*.md 中"
        f"均未被引用——经验库已被架空。请在对应 skill 或 AGENTS.md 补回锚点。"
        f"（已扫描 {len(texts)} 个引用源）"
    )


def test_methodology_rules_json_valid():
    """机器消费层必须可被 RuleStore 解析，否则 L3 注入会静默退化成空规则集。"""
    assert RULES_JSON.exists(), f"缺少机器消费层规则库: {RULES_JSON}"
    data = json.loads(RULES_JSON.read_text(encoding="utf-8"))
    rules = data.get("rules")
    assert isinstance(rules, list) and rules, "methodology_rules.json 无 rules"

    ids = [r.get("rule_id") for r in rules if r.get("rule_id")]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    assert not dup, f"rule_id 重复会导致区域覆盖全局时行为不确定: {dup}"

    valid_types = {
        "strategy", "dead_end", "gate_override", "universe_lever",
        "field_whitelist", "diagnosis", "explore_contract",
    }
    bad = [(r.get("rule_id"), r.get("type")) for r in rules
           if r.get("type") not in valid_types]
    assert not bad, f"未知 rule_type 不会被任何消费点命中: {bad}"


def test_rule_declared_docs_exist():
    """双轨同源：规则里 params.doc 指向的经验文档必须真实存在。

    防止出现"机器层说见 01_platform_gates.md，但那篇已经被改名/删除"的断链。
    """
    if not RULES_JSON.exists():
        pytest.skip("无规则库")
    data = json.loads(RULES_JSON.read_text(encoding="utf-8"))
    broken = []
    checked = 0
    for r in data.get("rules", []):
        doc = ((r.get("action") or {}).get("params") or {}).get("doc")
        if not doc:
            continue
        checked += 1
        if not (REPO_ROOT / doc).exists():
            broken.append((r.get("rule_id"), doc))
    assert not broken, f"规则声明的经验文档不存在（双轨断链）: {broken}"
    assert checked >= 5, (
        f"仅 {checked} 条规则声明了 doc 来源——经验入库后应回填 doc 字段，"
        f"否则无法追溯机器层与文档层的对应关系"
    )


def test_agents_declares_dual_track():
    """AGENTS.md 必须写明"md 给人看 / rules.json 给机器消费"的双轨关系。

    否则后来者只会改其中一边，两边漂移（这正是 2026-09-05 ra-pipeline 与 AGENTS.md
    逐字复制后漂移的同一类事故）。
    """
    agents = REPO_ROOT / "AGENTS.md"
    if not agents.exists():
        pytest.skip("无 AGENTS.md")
    txt = agents.read_text(encoding="utf-8", errors="ignore")
    assert "methodology_rules.json" in txt, (
        "AGENTS.md 未提及 methodology_rules.json——双轨中的机器层未被声明，改文档的人不会知道要同步"
    )
    assert "docs/experience" in txt, "AGENTS.md 未引用经验库目录"


def test_no_docs_experience_broken_relative_links():
    """经验文档之间的相对链接不得断链（索引 README 指向的篇目必须存在）。"""
    readme = DOCS_DIR / "README.md"
    if not readme.exists():
        pytest.skip("无 README 索引")
    txt = readme.read_text(encoding="utf-8", errors="ignore")
    # 匹配形如 `01_platform_gates.md` 或 (01_platform_gates.md) 的文件名引用
    refs = set(re.findall(r"([0-9]{2}_[a-z_]+\.md)", txt))
    broken = sorted(r for r in refs if not (DOCS_DIR / r).exists())
    assert not broken, f"README 索引指向了不存在的篇目: {broken}"
