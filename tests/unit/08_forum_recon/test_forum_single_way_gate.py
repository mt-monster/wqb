# -*- coding: utf-8 -*-
"""论坛「唯一方式」机械闸（2026-11-18 用户裁定）。

裁定：全项目查论坛一律按 `docs/reference/forum_and_doc_tools_guide.md`，只经 `wq-brain-http`
的 5 个 MCP 工具；论坛访问单一实现 = `tools/lib/forum_mcp.py`。本闸防止回归到 requests 抓取 /
直连 Zendesk API / WebSearch 当论坛通道等旁路（那些会把「检索故障」误读成「论坛无解」）。

守四件事：
  1. 活跃代码（tools/ + src/wqb）不再 import 已删除的 `forum_research` 抓取模块（该文件已删除，留 import 即报错）；
  2. `forum_recon.py` 传输层走 `forum_mcp`（MCP），不 import requests、不抓 HTML；
  3. `forum_mcp.py` 只允许调 guide 白名单的 5 个工具（非白名单直接拒绝）；
  4. **写方向例外受管**：活跃代码里任何「requests + 论坛」的模块必须出现在
     `REQUESTS_FORUM_EXCEPTIONS` 里，且 guide 必须写明该例外（否则旁路可以无声新增）。
"""
import ast
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "tools"))

GUIDE_TOOLS = {
    "search_forum_posts",
    "read_forum_post",
    "get_glossary_terms",
    "get_documentations",
    "get_documentation_page",
}

#: 唯一允许的「requests + 论坛」模块（写方向）。
#: 2026-11-18 用户裁定的是**查**论坛的唯一方式（读方向，5 个 MCP 工具）。
#: 发帖方向 MCP 侧**没有**对应工具（`create_forum_post` 在 MCP 包内已不存在），
#: 故 `tools/forum/forum_post.py` 是当前唯一的发帖实现——它是**登记在册的例外**，
#: 不是隐形旁路：MCP 一旦补上发帖工具，本例外即应删除（棘轮：新增即红）。
REQUESTS_FORUM_EXCEPTIONS = {
    "tools/forum/forum_post.py",
}


def _imports_module(tree: ast.AST, name: str) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(a.name == name or a.name.startswith(name + ".") for a in node.names):
                return True
        elif isinstance(node, ast.ImportFrom):
            if node.module and (node.module == name or node.module.startswith(name + ".")):
                return True
    return False


def _active_py_files():
    for base in (REPO_ROOT / "tools", REPO_ROOT / "src" / "wqb"):
        for p in base.rglob("*.py"):
            if "__pycache__" in p.parts or "legacy" in p.parts or "attic" in p.parts:
                continue
            yield p


def test_no_active_code_imports_the_retired_scraper():
    offenders = []
    for p in _active_py_files():
        try:
            tree = ast.parse(p.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            continue
        if _imports_module(tree, "forum_research"):
            offenders.append(str(p.relative_to(REPO_ROOT)))
    assert not offenders, (
        "查论坛唯一方式是 MCP（forum_and_doc_tools_guide.md）；这些文件仍 import 退役的 "
        f"forum_research 抓取模块：{offenders}。请改走 tools/lib/forum_mcp.py。")


def test_forum_recon_transport_is_mcp_not_requests():
    src = (REPO_ROOT / "tools" / "forum_recon.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    assert not _imports_module(tree, "requests"), "forum_recon 不得 import requests（论坛唯一入口是 MCP）"
    assert not _imports_module(tree, "forum_research"), "forum_recon 不得再依赖退役抓取模块"
    assert "from lib import forum_mcp" in src, "forum_recon 传输层必须走 tools/lib/forum_mcp.py"
    assert "search_html" not in src, "不得抓 HTML 搜索页"


def test_forum_mcp_whitelist_matches_the_guide():
    from lib import forum_mcp as FM
    assert FM.ALLOWED_TOOLS == GUIDE_TOOLS, "forum_mcp 白名单必须与 guide 的 5 个工具一致"


def test_forum_mcp_rejects_non_whitelisted_tool():
    from lib import forum_mcp as FM

    class _Cli:
        def call_tool(self, name, args):
            raise AssertionError("白名单外的工具不得被调用")
    with pytest.raises(ValueError):
        FM._call(_Cli(), "create_forum_post", {})      # 写工具不在论坛检索白名单
    with pytest.raises(ValueError):
        FM._call(_Cli(), "get_datafields", {})


def _requests_forum_modules():
    """活跃代码里同时「import requests」且涉及论坛/社区的模块。"""
    hits = set()
    for p in _active_py_files():
        try:
            src = p.read_text(encoding="utf-8")
            tree = ast.parse(src)
        except (SyntaxError, UnicodeDecodeError):
            continue
        if not _imports_module(tree, "requests"):
            continue
        low = src.lower()
        if "forum" in low or "zendesk" in low or "community/posts" in low:
            hits.add(str(p.relative_to(REPO_ROOT)).replace("\\", "/"))
    return hits


def test_requests_forum_paths_are_declared_exceptions():
    """requests 论坛路径必须逐个登记为例外，且例外集合不得无记录地扩大。"""
    found = _requests_forum_modules()
    undeclared = sorted(found - REQUESTS_FORUM_EXCEPTIONS)
    assert not undeclared, (
        "发现未登记的 requests 论坛路径："
        f"{undeclared}。查论坛唯一方式是 MCP（forum_and_doc_tools_guide.md）；"
        "若确属例外（如发帖方向 MCP 暂无工具），须先在 "
        "REQUESTS_FORUM_EXCEPTIONS 与 guide 中登记理由，否则按旁路处理。")
    stale = sorted(REQUESTS_FORUM_EXCEPTIONS - found)
    assert not stale, (
        f"REQUESTS_FORUM_EXCEPTIONS 里的 {stale} 已不存在（文件被删/改名）——"
        "请同步清理登记，或说明它为何仍需保留。")


def test_forum_write_exception_is_documented_in_guide():
    """登记为例外还不够：guide 必须写明，否则读者无从知道发帖走另一条路。"""
    guide = (REPO_ROOT / "docs" / "reference" / "forum_and_doc_tools_guide.md")
    text = guide.read_text(encoding="utf-8")
    for rel in REQUESTS_FORUM_EXCEPTIONS:
        assert rel in text, (
            f"{rel} 是登记在册的 requests 论坛例外，但 guide "
            "（docs/reference/forum_and_doc_tools_guide.md）没有写明它——"
            "请在 guide 里补一句：发帖方向为何仍走它、何时退役。")
