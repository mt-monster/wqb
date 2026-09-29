# -*- coding: utf-8 -*-
"""skills 审查 X-14（2026-09-29，S-D）：运行时代码里不得有作者本机的 Windows 盘符路径。

此前约 14 个代码文件带着 `r"D:\\coding\\traeCN_project\\wqb"` 之类的兜底（`WQB_ROOT or … or <作者盘符>`）：
仓库不在该盘符时静默退化（读到空库 / 造出杂散目录），在别的机器上更是「看似有兜底、实际没有」。
现在：环境变量 > 从本文件上溯到含 `src/wqb` 的仓库根，没有盘符兜底。

扫描口径：`src/`、`tools/`（不含 `tools/legacy/` 归档）、`Claude/skills/**`、`world-quant-brain-mcp/` 顶层脚本里的
**字符串常量**（用 AST，所以注释与 docstring 里对历史路径的叙述不算）。`tracking/` 是区域历史实现（归档 / 私有脚本）、
`tests/` 是测试，均不在范围内。
"""
import ast
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PATTERNS = (re.compile(r"[A-Za-z]:[\\/]+coding[\\/]+traeCN_project", re.I),
            re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+[A-Za-z0-9_.-]+[\\/]", re.I))
SKIP_PARTS = {"__pycache__", ".venv", "attic", "legacy", "node_modules"}


def _py_files():
    roots = [REPO / "src", REPO / "tools", REPO / "Claude" / "skills"]
    for root in roots:
        for p in root.rglob("*.py"):
            if not (SKIP_PARTS & set(p.relative_to(REPO).parts)):
                yield p
    for p in (REPO / "world-quant-brain-mcp").glob("*.py"):
        yield p
    yield from (REPO / "wqb_db_mcp.py",)


def _docstring_ids(tree):
    ids = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = getattr(node, "body", [])
            if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) \
                    and isinstance(body[0].value.value, str):
                ids.add(id(body[0].value))
    return ids


def test_no_author_drive_paths_in_runtime_string_constants():
    offenders = []
    for p in _py_files():
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="ignore"))
        except SyntaxError:
            continue
        docs = _docstring_ids(tree)
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docs:
                if any(rx.search(node.value) for rx in PATTERNS):
                    offenders.append(f"{p.relative_to(REPO).as_posix()}:{node.lineno}: {node.value[:70]!r}")
    assert not offenders, ("运行时代码里出现作者本机盘符路径（用环境变量 / 从 __file__ 上溯仓库根）：\n  "
                           + "\n  ".join(offenders[:20]))


def test_workspace_root_helpers_prefer_env_then_repo_walkup(tmp_path, monkeypatch):
    """inspect-raw 的 _workspace 与 toolkit 的 wqb_store 都只认环境变量与真实上溯，不再有固定路径候选。"""
    import sys
    skill = REPO / "Claude" / "skills" / "brain-inspect-raw-template-create-setting"
    if str(skill) not in sys.path:
        sys.path.insert(0, str(skill))
    from scripts import _workspace
    ws = tmp_path / "ws"
    (ws / "src" / "wqb").mkdir(parents=True)
    monkeypatch.setenv("WQB_WORKSPACE", str(ws))
    monkeypatch.delenv("WQB_ROOT", raising=False)
    monkeypatch.delenv("WQ_PROJECT_ROOT", raising=False)
    roots = _workspace.workspace_roots()
    assert roots[0] == str(ws)
    assert all("traeCN_project" not in r for r in roots)
    assert str(REPO) in roots                      # 仓库内运行时，上溯也能找到仓库根

    toolkit = REPO / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"
    if str(toolkit) not in sys.path:
        sys.path.insert(0, str(toolkit))
    from _lib import wqb_store
    assert not hasattr(wqb_store, "_LEGACY_ROOT")
    assert all("traeCN_project" not in r for r in wqb_store._workspace_roots())
