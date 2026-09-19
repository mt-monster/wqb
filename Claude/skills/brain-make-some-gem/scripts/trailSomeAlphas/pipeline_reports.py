# -*- coding: utf-8 -*-
"""GEM 报告读写层：ideas markdown 的渲染 / 落盘 / 解析。

2026-09-12 从 run_pipeline.py 拆出。

含两类职责：
  1. 生成端兜底与落盘：exposure 标签推断、mandatory sections 补齐、
     save_ideas_report、skeleton 模式的 ideas 渲染；
  2. Concept 块解析：extract_template_blocks（主）+ table / named 两级 fallback。

与 src/wqb/workflow/nodes/gem.py 的 _parse_ideas_blocks 保持同规则
（那边是 Popen 前的零成本预检副本；本文件是权威实现）。
"""
import json
import re
from pathlib import Path

from pipeline_paths import FEATURE_ENGINEERING_DIR


# ---------------- expected_exposure 兜底（2026-09-01） ----------------
# LLM 生成 idea 时有时漏写 **Expected Exposure** 行（实测 520 条仅 14% 覆盖），
# gate.py 的收益来源多样性闸读不到标签就降级 WARN、形同虚设。
# 此函数对缺失项按 Concept/Mechanism 关键词推断标签并显式追加该行。

_EXPOSURE_KEYWORDS = [
    ("momentum", ["momentum", "trend", "drift", "continuation", "post-earnings", "pead"]),
    ("reversal", ["reversal", "overreaction", "mean-revert", "mean revert", "short-term reversal"]),
    ("value", ["value", "underval", "book-to-market", "earnings yield", "cheap"]),
    ("quality", ["quality", "profitab", "roa", "roe", "accrual", "earnings quality"]),
    ("growth", ["growth", "expansion", "revision up", "upgrade"]),
    ("lowvol", ["low vol", "lowvol", "defensive", "stability", "stable"]),
    ("liquidity", ["liquidity", "amihud", "turnover cost", "tradability"]),
    ("sentiment", ["sentiment", "news tone", "crowd", "attention", "buzz", "panic", "fear"]),
    ("flow", ["ownership", "institutional", "holdings", "insider", "buyback", "flow"]),
    ("risk", ["risk", "volatility", "tail", "drawdown", "distress", "default"]),
]


def _ensure_expected_exposure(idea_text: str) -> str:
    """idea 文本缺 **Expected Exposure** 行时按关键词推断并追加。已有则原样返回。"""
    if not idea_text:
        return idea_text
    if re.search(r"\*\*Expected Exposure\*\*\s*:", idea_text, re.IGNORECASE):
        return idea_text
    tl = idea_text.lower()
    for label, kws in _EXPOSURE_KEYWORDS:
        if any(k in tl for k in kws):
            return idea_text.rstrip() + f"\n- **Expected Exposure** (inferred): {label}\n"
    return idea_text.rstrip() + "\n- **Expected Exposure** (inferred): other\n"


def render_skeleton_ideas_md(dataset_id: str, region: str, delay: int,
                             layers: dict, metas: list, dropped: dict) -> str:
    """把填槽结果渲染为 ideas.md（Concept 块自 slots 渲染，保持元数据头/ledger 契约）。"""
    lines = [
        f"**Dataset**: {dataset_id}",
        f"**Region**: {region}",
        f"**Delay**: {delay}",
        "",
        "# Skeleton-mode ideas (operator-topology constrained)",
        "",
        f"Field layering: signal={len(layers['signal'])}, scale={len(layers['scale'])}, "
        f"metadata={len(layers['metadata'])} (excluded), date={len(layers['date'])} (excluded).",
        "",
        "## Signal fields used",
        "",
    ]
    used = sorted({m["field"] for m in metas} | {m["field2"] for m in metas if m.get("field2")})
    for fid in used:
        lines.append(f"- `{fid}`")
    lines += ["", "## Concepts", ""]
    by_family: dict[str, list] = {}
    for m in metas:
        by_family.setdefault(m["family"], []).append(m)
    for fam, items in sorted(by_family.items()):
        lines.append(f"### family: {fam}")
        lines.append("")
        for i, m in enumerate(items, 1):
            lines.append(f"**Concept {fam}.{i}**")
            lines.append("")
            lines.append(f"- skeleton: `{m['skeleton_id']}` window={m['window']} sign={m['sign']}")
            lines.append(f"- rationale: {m['rationale'] or '(none)'}")
            lines.append("")
            lines.append("**Implementation Example**")
            lines.append("")
            lines.append(f"`{m['expr']}`")
            lines.append("")
    lines += [
        "## Slot-drop statistics",
        "",
        f"```json\n{json.dumps(dropped, ensure_ascii=False, indent=2)}\n```",
        "",
    ]
    return "\n".join(lines)


def render_phased_ideas_md(mapping_results: list, dataset_id: str, region: str, delay: int) -> str:
    """phased 模式 Phase 3 确定性渲染（2026-09-13：替代 LLM 重写，消除最后一段自由文本）。

    把 Phase 2 的 mapping JSON（mechanism / field_ids / templates / why）直接渲染为
    ideas markdown——**Concept** 块格式与 extract_template_blocks 解析契约兼容，
    占位符合法性交给下游归一化（normalize_template_placeholders）兜底，
    但不再经过 LLM 自由文本生成（字段名拼接幻觉面归零）。

    Returns:
        ideas markdown 文本；Phase 2 无可用模板时返回仅含头部的文本
        （下游 extract_template_blocks 返回空 → fail fast，不静默产假候选）。
    """
    lines = [
        f"**Dataset**: {dataset_id}",
        f"**Region**: {region}",
        f"**Delay**: {delay}",
        "",
        "# Phased-mode ideas (deterministic render from Phase-2 mapping)",
        "",
        "## Concepts",
        "",
    ]
    rendered = 0
    for item in (mapping_results or []):
        if not isinstance(item, dict):
            continue
        mech = str(item.get("mechanism") or "").strip() or "(unnamed mechanism)"
        why = str(item.get("why") or item.get("rationale") or "").strip()
        fields = item.get("field_ids") or []
        if isinstance(fields, (list, tuple)):
            fstr = ", ".join(f"`{f}`" for f in fields if f)
        else:
            fstr = f"`{fields}`"
        fields_line = f"- **Fields**: {fstr}" if fstr else "- **Fields**: (from mapping)"
        templates = item.get("templates") or []
        if isinstance(templates, str):
            templates = [templates]
        k = 0
        for t in templates:
            t = str(t).strip()
            if not t or "{" not in t or "}" not in t:
                continue
            k += 1
            rendered += 1
            name = mech if k == 1 else f"{mech} #{k}"
            lines += [
                f"**Concept**: {name}",
                "",
                f"- **Mechanism**: {why or mech}",
                fields_line,
                f"- **Implementation Example**: `{t}`",
                "",
            ]
    if rendered == 0:
        lines += [
            "(Phase 2 produced no renderable templates — downstream will fail fast;",
            " re-run phased mode or fall back to single/skeleton mode.)",
            "",
        ]
    return "\n".join(lines)


def _ensure_mandatory_sections(content: str, dataset_id: str, region: str, delay: int) -> str:
    """Ensure the ideas markdown contains all mandatory sections for downstream parsing.

    Required sections (checked by regex, auto-appended if missing):
      - ## 字段（Fields）
      - ## 特征（Features）
      - ## 建议（Implementation Examples）
      - ## 字段白名单（Field Whitelist）
      - ## Concepts
    """
    if not content:
        return content

    # Check for mandatory sections (allow both Chinese and English headers)
    has_fields = re.search(r"^##\s+字段|^##\s+Fields", content, flags=re.MULTILINE | re.IGNORECASE)
    has_features = re.search(r"^##\s+特征|^##\s+Features", content, flags=re.MULTILINE | re.IGNORECASE)
    has_examples = re.search(r"^##\s+建议|^##\s+Implementation", content, flags=re.MULTILINE | re.IGNORECASE)
    has_whitelist = re.search(r"^##\s+字段白名单|^##\s+Field Whitelist", content, flags=re.MULTILINE | re.IGNORECASE)
    has_concepts = re.search(r"^##\s+Concepts|^##\s+概念", content, flags=re.MULTILINE | re.IGNORECASE)

    missing = []
    if not has_fields:
        missing.append("字段（Fields）")
    if not has_features:
        missing.append("特征（Features）")
    if not has_examples:
        missing.append("建议（Implementation Examples）")
    if not has_whitelist:
        missing.append("字段白名单（Field Whitelist）")
    if not has_concepts:
        missing.append("Concepts")

    if not missing:
        return content

    # Auto-append missing sections with sensible defaults
    lines = [content.rstrip(), ""]
    lines.append("---")
    lines.append("")
    lines.append("## Auto-appended mandatory sections (GEM 生成端兜底)")
    lines.append("")

    if not has_fields:
        lines.extend([
            "## 字段（Fields）",
            "",
            "| Field ID | Type | Coverage | Role |",
            "|---|---|---|---|",
            f"| (auto-generated from {dataset_id}) | MATRIX | N/A | 主信号 |",
            "",
        ])

    if not has_features:
        lines.extend([
            "## 特征（Features）",
            "",
            "- ts_backfill：对低覆盖率稀疏字段做时间序列回填",
            "- group_zscore / group_rank：截面中性化（cross-sectional）",
            "- rank / winsorize：防厚尾与极值",
            "",
        ])

    if not has_examples:
        # Extract existing Implementation Examples from Concepts
        examples = re.findall(r"\*\*Implementation Example\*\*[:\s]*`([^`]+)`", content)
        if not examples:
            examples = re.findall(r"Implementation Example[:\s]*`([^`]+)`", content, flags=re.IGNORECASE)
        lines.extend([
            "## 建议（Implementation Examples）",
            "",
        ])
        if examples:
            for i, ex in enumerate(examples[:10], 1):
                lines.append(f"- concept_{i}: `{ex}`")
        else:
            lines.append("- (no Implementation Examples found in Concepts)")
        lines.append("")

    if not has_whitelist:
        # Extract field ids from backticks in the whole document
        field_ids = re.findall(r"`([a-z][a-z0-9_]{3,})`", content)
        field_ids = sorted(set(f for f in field_ids if not f.startswith(("rank", "ts_", "vec_", "group_", "add", "sub", "mul", "div"))))
        lines.extend([
            "## 字段白名单（Field Whitelist）",
            "",
            "```",
        ])
        lines.extend(field_ids[:50])  # cap at 50
        lines.extend([
            "```",
            "",
        ])

    if not has_concepts:
        lines.extend([
            "## Concepts",
            "",
            "(Concept blocks were not found in the original output; see above sections for extracted fields and templates.)",
            "",
        ])

    print(f"[sections] auto-appended missing mandatory sections: {', '.join(missing)}", flush=True)
    return "\n".join(lines)


def save_ideas_report(content: str, region: str, delay: int, dataset_id: str) -> Path:
    # Ensure mandatory sections before saving
    content = _ensure_mandatory_sections(content, dataset_id, region, delay)
    output_dir = FEATURE_ENGINEERING_DIR / "output_report"
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{region}_delay{delay}_{dataset_id}_ideas.md"
    output_path = output_dir / filename
    output_path.write_text(content, encoding="utf-8")
    return output_path


def extract_templates(markdown_text: str) -> list[str]:
    """Extract implementation templates from idea markdown.

    For pipeline robustness, this function returns ONLY the template strings.
    The recommended, higher-fidelity parser is `extract_template_blocks()`,
    which returns both template + idea text per **Concept** block.
    """

    blocks = extract_template_blocks(markdown_text)
    templates = [b["template"] for b in blocks if b.get("template")]
    return sorted(set(t.strip() for t in templates if t and t.strip()))


def extract_table_template_blocks(markdown_text: str) -> list[dict[str, str]]:
    """Fallback parser for markdown tables that contain a `{placeholder}` template.

    Accepts both column orders:
      | ID | `template` | rationale |
      | # | Idea | `template` |
    """
    row_re = re.compile(r"^\|\s*(?:\d+\s*)?\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|?\s*$")
    out: list[dict[str, str]] = []
    seen: set[str] = set()

    def _add(template: str, rationale: str) -> None:
        template = template.strip()
        if "{" not in template or "}" not in template or template in seen:
            return
        seen.add(template)
        idea = f"**Concept**: {rationale}\n- **Implementation Example**: `{template}`"
        out.append({"template": template, "idea": idea})

    for line in markdown_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or stripped.startswith("|---"):
            continue
        matched = row_re.match(stripped)
        if matched:
            _add(matched.group(1).strip(), matched.group(2).strip().strip("|").strip())
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 2:
            continue
        template = None
        other: list[str] = []
        for cell in cells:
            bt = re.search(r"`([^`]+)`", cell)
            if bt and "{" in bt.group(1) and "}" in bt.group(1) and template is None:
                template = bt.group(1).strip()
            else:
                other.append(re.sub(r"`+", "", cell).strip())
        if template:
            rationale = " ".join(x for x in other if x and x != "---" and not x.isdigit())
            _add(template, rationale)
    return out


def extract_named_template_blocks(markdown_text: str) -> list[dict[str, str]]:
    """Fallback for LLM headings: - **Template**: `expr` plus nearby Rationale."""
    named_re = re.compile(r"\*\*Template\*\*\s*:\s*`([^`]+)`", flags=re.IGNORECASE)
    rationale_re = re.compile(r"\*\*Rationale\*\*\s*:\s*(.*)$", flags=re.IGNORECASE)
    heading_re = re.compile(r"^#{2,6}\s+(.*)$")
    out: list[dict[str, str]] = []
    current_heading = ""
    pending_template: str | None = None
    pending_rationale = ""
    pending_heading = ""

    def _flush() -> None:
        nonlocal pending_template, pending_rationale, pending_heading
        if pending_template and "{" in pending_template and "}" in pending_template:
            idea = f"**Concept**: {pending_heading or pending_rationale}\n{pending_rationale}".strip()
            out.append({"template": pending_template.strip(), "idea": idea})
        pending_template = None
        pending_rationale = ""
        pending_heading = ""

    for line in markdown_text.splitlines():
        stripped = line.strip()
        hm = heading_re.match(stripped)
        if hm:
            _flush()
            current_heading = hm.group(1).strip()
            continue
        tm = named_re.search(stripped)
        if tm:
            _flush()
            pending_template = tm.group(1).strip()
            pending_heading = current_heading
            continue
        rm = rationale_re.search(stripped)
        if rm and pending_template:
            pending_rationale = (rm.group(1) or "").strip()
    _flush()
    return out


def extract_template_blocks(markdown_text: str) -> list[dict[str, str]]:
    """Parse **Concept** blocks and extract {template, idea}.

    A "block" is a section that starts with a line like:
      **Concept**: ...
    and contains a line like:
      - **Implementation Example**: `...`

    Output:
      [{"template": <string>, "idea": <string>}, ...]

    Notes:
    - `template` is taken from inside backticks when present; otherwise uses the
      remainder of the line after ':'.
    - `idea` is the rest of the block text (including the concept line and
      bullets) excluding the implementation example line.
    """

    concept_re = re.compile(r"^\*\*Concept\*\*\s*:\s*(.*)\s*$")
    impl_re = re.compile(r"\*\*Implementation Example\*\*\s*:\s*(.*)$", flags=re.IGNORECASE)
    backtick_re = re.compile(r"`([^`]*)`")
    boundary_re = re.compile(r"^(?:-{3,}|#{1,6}\s+.*)\s*$")

    lines = markdown_text.splitlines()
    blocks: list[list[str]] = []
    current: list[str] = []

    def _flush():
        nonlocal current
        if current:
            # Trim leading/trailing blank lines in block.
            while current and not current[0].strip():
                current.pop(0)
            while current and not current[-1].strip():
                current.pop()
            if current:
                blocks.append(current)
        current = []

    for line in lines:
        if concept_re.match(line.strip()):
            _flush()
            current = [line]
            continue

        # If we are inside a concept block and hit a section boundary (e.g. '---', '### Q2'),
        # close the block so unrelated headings don't get included in the idea text.
        if current and boundary_re.match(line.strip()):
            _flush()
            continue

        if current:
            current.append(line)

    _flush()

    out: list[dict[str, str]] = []
    for block_lines in blocks:
        template: str | None = None
        impl_line_idx: int | None = None

        # Find the implementation example line (or its continuation).
        for i, raw in enumerate(block_lines):
            m = impl_re.search(raw)
            if not m:
                continue

            impl_line_idx = i
            tail = (m.group(1) or "").strip()

            # Case 1: template is in backticks on the same line.
            bt = backtick_re.search(tail)
            if bt:
                template = bt.group(1).strip()
                break

            # Case 2: tail itself is the template.
            if tail and ("{" in tail and "}" in tail):
                template = tail.strip().strip("`")
                break

            # Case 3: template is on the next non-empty line, often in backticks.
            for j in range(i + 1, min(i + 4, len(block_lines))):
                nxt = block_lines[j].strip()
                if not nxt:
                    continue
                bt2 = backtick_re.search(nxt)
                if bt2:
                    template = bt2.group(1).strip()
                    break
                if "{" in nxt and "}" in nxt:
                    template = nxt.strip().strip("`")
                    break
            break

        if not template or "{" not in template or "}" not in template:
            continue

        # idea = all block text except the implementation example line itself.
        idea_lines: list[str] = []
        for i, raw in enumerate(block_lines):
            if impl_line_idx is not None and i == impl_line_idx:
                continue
            idea_lines.append(raw)

        idea = "\n".join(idea_lines).strip()
        out.append({"template": template.strip(), "idea": idea})

    if not out:
        out = extract_table_template_blocks(markdown_text)
    if not out:
        out = extract_named_template_blocks(markdown_text)

    return out
