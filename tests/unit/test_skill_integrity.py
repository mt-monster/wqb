# -*- coding: utf-8 -*-
"""Skill / Workflow 完整性守护测试（2026-09-05 新增）.

背景：此前没有任何测试扫描 SKILL.md —— tests/unit/test_skills.py 名字像，
实测的却是 operator_audit / validator。于是这一类问题只能靠人眼审计：

  - brain-make-some-gem 目录存在但缺 SKILL.md（Agent 根本加载不到）
  - SKILL.md 里引用 src/wqb/expression/paradigms.py，而该模块已被删除
  - SKILL.md 里写 mcp__wq-brain-http__<tool>，而 MCP 侧根本没注册该工具
  - registry NodeMeta 的 optional_params 与节点 run() 签名漂移
    （workflow_list_nodes 把它当 API 文档直接给 Agent 看）
  - mcp_config.json 的服务器名与 .mcp.json 不一致（全线工具前缀失配）

本文件把这些做成回归。
"""
from __future__ import annotations

import inspect
import json
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
MCP_DIR = REPO_ROOT / "world-quant-brain-mcp"

sys.path.insert(0, str(REPO_ROOT / "src"))


def _resolve_skills_dir() -> Path:
    """定位 Agent 真正加载的那份 skill 目录。

    2026-09-06 修复：此前硬编码 `REPO_ROOT / "Claude" / "skills"`，而 Claude Code
    实际从 `~/.claude/skills` 加载（`~/.qoder-cn/skills` 是指向它的 junction）。
    仓库副本在场时这里校验的是另一份拷贝，两边一漂移就守了个寂寞；仓库副本不在
    场时（本次审计发现的 247 文件误删）更是整体 skip。

    现复用 `wqb.workflow._common._skill_roots()` —— 与 campaign / gem 节点定位
    skill 用的是同一套解析顺序，测的就是运行时会加载的那一份。
    """
    try:
        from wqb.workflow._common import _skill_roots
        for root in _skill_roots():
            candidate = Path(root)
            if candidate.is_dir() and any(candidate.glob("*/SKILL.md")):
                return candidate
    except Exception:  # pragma: no cover - 解析失败回落仓库副本
        pass
    return REPO_ROOT / "Claude" / "skills"


SKILLS_DIR = _resolve_skills_dir()


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _skill_dirs():
    """列出 skill 目录；目录缺失时返回空列表。

    2026-09-06 修复：原实现在此调 `pytest.skip()`，而本函数被用在模块级
    `@pytest.mark.parametrize(...)` 里 —— collection 期的模块级 skip 不是跳过，
    是 `ERROR + Interrupted`，整场 323 个用例一个都跑不了（实测）。
    返回空列表则参数化自然产出零用例，其余测试照常执行。
    """
    if not SKILLS_DIR.is_dir():
        return []
    return sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir() and not d.name.startswith("."))


def test_skills_dir_is_discoverable():
    """守护解析本身：一份都找不到就是安装/误删事故，不该静默跳过。"""
    assert _skill_dirs(), (
        f"未在 {SKILLS_DIR} 找到任何 skill 目录。检查 skill 是否被误删"
        "（git restore Claude/skills）或安装位是否变更（WQ_SKILLS_DIR）。"
    )


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _frontmatter(text: str) -> dict:
    """极简 frontmatter 解析（只取顶层 `key: value`，不引入 PyYAML 依赖）。"""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out = {}
    for line in text[3:end].splitlines():
        if not line or line.startswith((" ", "\t", "#", "-")):
            continue
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def _registered_mcp_tools() -> set:
    """扫描 @mcp.tool() 装饰的函数名，返回 mcp__<server>__<tool> 全名集合。"""
    tools = set()
    pattern = re.compile(r"@mcp\.tool\([^)]*\)\s*\n\s*(?:async\s+)?def\s+([A-Za-z0-9_]+)")
    for f in sorted(MCP_DIR.glob("tools_*.py")) + [MCP_DIR / "main.py", MCP_DIR / "mcp_core.py"]:
        if f.exists():
            for m in pattern.finditer(_read(f)):
                tools.add(f"mcp__wq-brain-http__{m.group(1)}")
    db_mcp = REPO_ROOT / "wqb_db_mcp.py"
    if db_mcp.exists():
        for m in pattern.finditer(_read(db_mcp)):
            tools.add(f"mcp__wqb-db__{m.group(1)}")
    return tools


#: 文档里作为「已移除，不要依赖」的反面教材出现的工具名，不参与存在性校验。
DEPRECATED_TOOL_MENTIONS = {
    "mcp__wq-brain-http__get_submission_quota",
    # brain-alpha-judge SKILL.md 里作为「提交语义反面教材」提及（201≠成功），
    # 提交走 submit_verdict → workflow_submit_alpha 链，不经此工具。
    "mcp__wq-brain-http__submit_alpha",
}
#: 前缀通配写法（allowed-tools 里的 mcp__wq-brain-http__* 之类），不是具体工具。
_WILDCARD = re.compile(r"^mcp__[a-z-]+__$")


# ---------------------------------------------------------------------------
# 1. SKILL.md 存在性与 frontmatter
# ---------------------------------------------------------------------------

def test_every_skill_dir_has_skill_md():
    missing = [d.name for d in _skill_dirs() if not (d / "SKILL.md").is_file()]
    assert not missing, (
        f"以下 skill 目录缺 SKILL.md，Agent 无法加载：{missing}。"
        "要么补 SKILL.md，要么把目录移出 Claude/skills/。"
    )


@pytest.mark.parametrize("skill_dir", _skill_dirs(), ids=lambda d: d.name)
def test_frontmatter_name_matches_dir(skill_dir):
    md = skill_dir / "SKILL.md"
    if not md.is_file():
        pytest.skip("covered by test_every_skill_dir_has_skill_md")
    fm = _frontmatter(_read(md))
    assert fm.get("name"), f"{skill_dir.name}/SKILL.md 缺 frontmatter name"
    assert fm.get("description"), f"{skill_dir.name}/SKILL.md 缺 frontmatter description"
    assert fm["name"] == skill_dir.name, (
        f"frontmatter name={fm['name']!r} 与目录名 {skill_dir.name!r} 不一致"
    )


# ---------------------------------------------------------------------------
# 2. 引用可达性
# ---------------------------------------------------------------------------

_MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


@pytest.mark.parametrize("skill_dir", _skill_dirs(), ids=lambda d: d.name)
def test_markdown_links_resolve(skill_dir):
    md = skill_dir / "SKILL.md"
    if not md.is_file():
        pytest.skip("covered by test_every_skill_dir_has_skill_md")
    broken = []
    for target in _MD_LINK.findall(_read(md)):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        if "<" in target:  # 含占位符的模板路径
            continue
        # 允许相对 skill 目录，或相对仓库根（skill 里常直接写 src/... docs/...）
        if (skill_dir / target).exists() or (REPO_ROOT / target).exists():
            continue
        broken.append(target)
    assert not broken, f"{skill_dir.name}/SKILL.md 链接指向不存在的路径：{broken}"


# ---------------------------------------------------------------------------
# 3. MCP 工具名有效性
# ---------------------------------------------------------------------------

def test_skill_mcp_tool_references_are_registered():
    registered = _registered_mcp_tools()
    assert registered, "未能从 world-quant-brain-mcp/ 解析出任何 @mcp.tool()，检查扫描路径"

    # 末尾带 * 的是通配写法（allowed-tools、"workflow_* 快捷方式" 之类），不是具体工具
    pattern = re.compile(r"mcp__(?:wq-brain-http|wqb-db)__[A-Za-z0-9_]*\*?")
    unknown = {}
    for skill_dir in _skill_dirs():
        md = skill_dir / "SKILL.md"
        if not md.is_file():
            continue
        for name in set(pattern.findall(_read(md))):
            if name.endswith("*") or _WILDCARD.match(name):
                continue
            if name in DEPRECATED_TOOL_MENTIONS:
                continue
            if name not in registered:
                unknown.setdefault(skill_dir.name, []).append(name)
    assert not unknown, (
        f"SKILL.md 引用了未注册的 MCP 工具：{unknown}。"
        "要么在 MCP 侧注册，要么改文档；已移除的工具加进 DEPRECATED_TOOL_MENTIONS。"
    )


# ---------------------------------------------------------------------------
# 4. registry 元数据 ↔ 节点签名
# ---------------------------------------------------------------------------

def test_registry_meta_matches_node_signature():
    from wqb.workflow import get_registry

    registry = get_registry()
    drift = {}
    for name in registry.list_nodes():
        func = registry.get(name)
        meta = registry.get_meta(name)
        sig = inspect.signature(func)
        required = [
            k for k, v in sig.parameters.items()
            if v.default is inspect.Parameter.empty and k != "_context"
        ]
        optional = [
            k for k, v in sig.parameters.items()
            if v.default is not inspect.Parameter.empty and k not in ("_context", "dry_run")
        ]
        problems = []
        if required != list(meta.required_params):
            problems.append(f"required: sig={required} meta={list(meta.required_params)}")
        if sorted(optional) != sorted(meta.optional_params):
            problems.append(f"optional: sig={sorted(optional)} meta={sorted(meta.optional_params)}")
        if problems:
            drift[name] = problems
    assert not drift, (
        f"registry NodeMeta 与节点签名漂移：{drift}。"
        "workflow_list_nodes 把这份元数据当 API 文档暴露给 Agent，漂移即误导。"
    )


# ---------------------------------------------------------------------------
# 5. MCP 服务器命名一致性
# ---------------------------------------------------------------------------

def test_mcp_server_names_are_consistent():
    root_cfg = REPO_ROOT / ".mcp.json"
    sample_cfg = REPO_ROOT / "mcp_config.json"
    if not root_cfg.exists() or not sample_cfg.exists():
        pytest.skip("mcp config not present")
    expected = set(json.loads(_read(root_cfg))["mcpServers"])
    actual = set(json.loads(_read(sample_cfg))["mcpServers"])
    assert actual == expected, (
        f"mcp_config.json 服务器名 {sorted(actual)} 与 .mcp.json {sorted(expected)} 不一致。"
        "所有 skill 调用的工具前缀是 mcp__<serverName>__*，改名即全线失配。"
    )


# ---------------------------------------------------------------------------
# 6. dry-run 契约：全节点干跑零副作用且成功
# ---------------------------------------------------------------------------

_DRY_RUN_CASES = {
    "batch_track": {"region": "KOR", "wave": "_test", "dataset": "_test"},
    "submit_alpha": {"alpha_id": "_TEST_"},
    "superalpha": {"region": "KOR", "components": ["_a_"] * 10},
    "judge": {"alpha_id": "_TEST_"},
    "gem": {"region": "KOR", "dataset_id": "_test", "delay": 1, "universe": "TOP3000"},
    "campaign": {"region": "KOR", "stage": "S0"},
    "wave_gate": {"region": "KOR", "dataset": "analyst4", "wave": "97"},
    "feature_engineering": {
        "region": "KOR", "dataset_id": "_test", "delay": 1, "universe": "TOP3000",
    },
}


def test_all_nodes_have_dry_run_cases():
    from wqb.workflow import get_registry

    nodes = set(get_registry().list_nodes())
    assert nodes == set(_DRY_RUN_CASES), (
        f"节点集合与 dry-run 用例不匹配：缺用例 {sorted(nodes - set(_DRY_RUN_CASES))}，"
        f"多余用例 {sorted(set(_DRY_RUN_CASES) - nodes)}"
    )


@pytest.mark.parametrize("node,params", sorted(_DRY_RUN_CASES.items()))
def test_dry_run_reports_error_when_it_fails(node, params):
    """干跑允许失败（如本机没装 toolkit），但失败必须带得出原因。

    2026-09-05：此前 campaign 把 error 塞进 steps[-1]、顶层只有 success=False，
    executor 读不到 → `execute_chain` 静默中断且 error=None。
    """
    from wqb.workflow import execute

    result = execute(node, params, dry_run=True)
    assert result.dry_run is True
    if not result.success:
        assert result.error, f"{node} 干跑失败却没有 error 信息（静默失败）"
