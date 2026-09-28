# -*- coding: utf-8 -*-
"""skill 职责边界契约的机械守护（2026-09-26 新增）。

## 缘起

实测：**边界声明覆盖率只有 39%（13/33）**，20 个 skill 没写清"上游/下游/不做什么"。
这不是洁癖——它直接导致两类事故：

1. **选错 skill**：`brain-how-to-pass-alpha-test`（"提交失败原因"）与
   `wq-brain-alpha-optimization-v1`（"修复失败的提交测试"）触发词撞车，共享 7 个资源，
   互不提及 → Agent 无法判断该 invoke 谁。
2. **职责真空**：`worldquant-submit-alpha`(REGULAR) 与 `wq-brain-superalpha`(SUPER) 共享
   6 个资源却**都没有**书面边界；反倒是**不执行提交**的 `brain-alpha-judge` 写得最清楚。
   → 判定权清楚、执行权是空的。

本模块把「每个 SKILL.md 必须有职责边界段」变成可断言的事实，并锁住两条已裁定的硬规则：
- skill **不得改写** `src/wqb/config.py` 的权威常量（只能引用）；
- L5 的 REGULAR / SUPER 执行权必须**互相声明互斥**。

详见 `output_report/skills_boundary_review_20260926.md`。
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / "Claude" / "skills"
INDEX_MD = SKILLS_DIR / "INDEX.md"

HEADING = "## 职责边界"
REQUIRED_BULLETS = ("**本 skill 负责**", "**本 skill 不做**", "**上游 / 下游**")

#: skill 不得用这些口吻改写 `src/wqb/config.py` 的权威常量（只能引用）
_OVERRIDE_PATTERNS = (
    re.compile(r"区域优先级\s*(?:修正|改为|调整为)"),
    re.compile(r"(?:实测|实证)\s*推翻"),
    re.compile(r"config\.(?:REGION_PRIORITY|REGIONS|GATES|CONCURRENCY)\s*(?:已过时|应改为|修正为)"),
)


def _skill_md_files():
    return sorted(p for p in SKILLS_DIR.glob("*/SKILL.md") if "_unpacked" not in p.as_posix())


def _boundary_section(text: str) -> str | None:
    m = re.search(rf"^{re.escape(HEADING)}\s*$(.*?)(?=^##\s|\Z)", text, re.S | re.M)
    return m.group(1) if m else None


def test_every_skill_declares_responsibility_boundary():
    """33 个 skill 每一个都必须有 `## 职责边界` 段，且含三条契约。

    只断言"文档干净"是不够的——本条断言的是**契约的存在**，防止补齐后再被删。
    """
    missing, incomplete = [], []
    for p in _skill_md_files():
        sec = _boundary_section(p.read_text(encoding="utf-8", errors="replace"))
        if sec is None:
            missing.append(p.parent.name)
            continue
        lack = [b for b in REQUIRED_BULLETS if b not in sec]
        if lack:
            incomplete.append(f"{p.parent.name}: 缺 {lack}")
    assert not missing, f"以下 skill 缺 `## 职责边界` 段：{missing}"
    assert not incomplete, "职责边界段缺条目（需 负责/不做/上游·下游）：\n" + "\n".join(incomplete)


def test_boundary_section_immediately_follows_h1():
    """边界段必须紧跟正文第一个 H1（间距 ≤3 行）——放在文末等于没写。

    判据用**相对 H1 的间距**而非绝对行号：`planning-with-files` 的 frontmatter 就有 36 行，
    绝对阈值会误伤；而"紧跟标题"才是真正要保证的可读性。
    """
    bad = []
    for p in _skill_md_files():
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        h1 = next((i for i, l in enumerate(lines, 1) if l.startswith("# ")), None)
        b = next((i for i, l in enumerate(lines, 1) if l.strip() == HEADING), None)
        if h1 is None or b is None:
            bad.append(f"{p.parent.name}: H1={h1} 边界段={b}")
        elif not (0 < b - h1 <= 3):
            bad.append(f"{p.parent.name}: H1 在第 {h1} 行，边界段在第 {b} 行（间距 {b - h1}）")
    assert not bad, ("职责边界段未紧跟正文第一个 H1（会被读者略过，或误插进代码块）：\n"
                     + "\n".join(bad))


def test_no_skill_overrides_config_authority():
    """skill 不得用"修正 / 推翻"口吻改写 `config.py` 权威常量。

    2026-09-26 实证：`brain-alpha-research` 曾写「区域优先级**修正为** HKG ≈ KOR > EUR」，
    而 `config.REGION_PRIORITY` 是 EUR=2 / HKG=1 —— **结论相反**，会直接误导选区投入。
    裁定：skill 只能引用常量；实证与常量冲突时保留观测但显式标注冲突、以 config 为准。
    """
    bad = []
    for p in _skill_md_files():
        for i, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            s = line.strip()
            if s.startswith("#") or s.startswith(">"):
                continue  # 标题与引用块（引用旧文不算主张）
            for pat in _OVERRIDE_PATTERNS:
                if pat.search(s):
                    bad.append(f"{p.parent.name}:{i}: {s[:110]}")
    assert not bad, (
        "skill 正文试图改写 `src/wqb/config.py` 权威常量（区域优先级/universe/GATES 等）。"
        "skill 只能**引用**常量；若实证与常量冲突，保留观测但显式标注冲突并裁定以 config 为准。\n"
        + "\n".join(bad[:10]))


def test_l5_execution_rights_are_mutually_declared():
    """L5 执行权：REGULAR 与 SUPER 必须**互相**声明互斥。

    二者共享 6 个资源（`registry_empirical` / `wave_results` / `run_selection` /
    `set_alpha_properties` / `submit_verdict` / `workflow_submit_alpha`）却曾都没有书面边界。
    """
    pairs = {
        "worldquant-submit-alpha": "wq-brain-superalpha",
        "wq-brain-superalpha": "worldquant-submit-alpha",
    }
    bad = []
    for name, other in pairs.items():
        sec = _boundary_section((SKILLS_DIR / name / "SKILL.md").read_text(encoding="utf-8"))
        if sec is None or other not in sec:
            bad.append(f"{name} 的边界段未指明与 {other} 的分工")
    assert not bad, (
        "L5 执行权边界未互相声明（REGULAR↔SUPER 必须互不代劳）：\n" + "\n".join(bad))


def test_l4_diagnosis_vs_improvement_is_declared():
    """L4：只读查阈值（how-to-pass）与动手改（optimization-v1）必须互相点名。

    判据：**是否产生新表达式** —— 不产生 → how-to-pass；产生 → optimization-v1。
    """
    pairs = {
        "brain-how-to-pass-alpha-test": "wq-brain-alpha-optimization-v1",
        "wq-brain-alpha-optimization-v1": "brain-how-to-pass-alpha-test",
    }
    bad = []
    for name, other in pairs.items():
        sec = _boundary_section((SKILLS_DIR / name / "SKILL.md").read_text(encoding="utf-8"))
        if sec is None or other not in sec:
            bad.append(f"{name} 的边界段未引用 {other}")
    assert not bad, "L4 诊断/改进边界未互相声明（触发词已撞车，必须点名分工）：\n" + "\n".join(bad)


def test_l2_fi_declares_embedded_status():
    """L2：`brain-feature-implementation` 必须声明"我不是独立主链入口"（它被内嵌在 GEM 内）。

    实测：该 skill 正文对 GEM / trailSomeAlphas / 主链 **零次提及**，而 ra-pipeline 已把
    "把 FI 当主链入口"列为反模式 → 读它的 Agent 会误当独立入口。
    """
    sec = _boundary_section((SKILLS_DIR / "brain-feature-implementation" / "SKILL.md")
                            .read_text(encoding="utf-8"))
    assert sec is not None, "brain-feature-implementation 缺职责边界段"
    assert "brain-make-some-gem" in sec and "主链" in sec, (
        "brain-feature-implementation 的边界段必须写明：主链入口是 brain-make-some-gem，"
        "本 skill 被内嵌在 GEM 引擎内、不得当独立主链入口")


def test_index_declares_boundary_contract_as_required():
    """INDEX 必须把「职责边界」列为新 skill 的必备契约，否则本套守护失去规范依据。"""
    idx = INDEX_MD.read_text(encoding="utf-8")
    assert HEADING in idx, "INDEX.md 未声明 `## 职责边界` 为正文必备段"
    assert "本 skill 负责" in idx and "本 skill 不做" in idx, "INDEX.md 未给出三段模板"
