#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试用例扫描与分组（供 run_grouped_tests.py 消费）
=================================================
扫描项目测试用例，按**模块归属**分组，产出 `cache/test_groups.json` 供
`tools/run_grouped_tests.py` 并行跑批与出报告。

2026-10-04 由仓库根 `wq_test_scan.py` 转正为本 CLI。原主顾是 wq 工作台「测试中心」
浏览器 UI，该 UI 及其模板 `wq_workbench.html`（从未入库、已不可恢复）随工作台整端
下架到 `attic/forum_workbench_20261004/`；扫描与分组本身不依赖 UI，故保留为工具。
命名刻意不用 `test_` 前缀 —— 它不是 pytest 用例（AGENTS.md §8.4 同一处置结论）。

分组依据（项目自带的编号目录，语义最清晰）：
  - tests/unit/NN_xxx/   → 10 个领域分组（01_store_db / 02_workflow / ... / 10_toolkit_scripts）
  - tests/ 根级 test_*.py → 「tests 根级」分组
  - world-quant-brain-mcp/tests/ → 「MCP 包」分组

用例解析用 AST 静态分析（毫秒级、不依赖 pytest 能否启动、离线可用），
拼出标准 pytest node id：`相对路径::类名::用例名` 或 `相对路径::用例名`。

产物 cache/test_groups.json 结构：
{
  "generated_at": "...", "total_files": N, "total_cases": N,
  "groups": [{"id","name","dir","file_count","case_count",
              "files":[{"path","case_count","cases":[{"name","nodeid"}]}]}]
}

运行：python tools/scan_test_groups.py [--refresh]
"""
from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path


def _bootstrap_src() -> None:
    """把 `src/` 放上 sys.path：向上探测双标记，**与文件层数无关**
    （AGENTS.md §8 禁止新增 `parents[N]` / `dirname(dirname())` 这类层数硬编码）。
    """
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists() and (parent / "src" / "wqb").is_dir():
            src = str(parent / "src")
            if src not in sys.path:
                sys.path.insert(0, src)
            return
    raise RuntimeError("仓库根未找到（向上未见 pyproject.toml + src/wqb 双标记）")


_bootstrap_src()
from wqb.paths import find_repo_root  # noqa: E402
REPO_ROOT = find_repo_root(__file__)  # 本文件在 tools/ 下，仓库根 = 上两级
DATA = REPO_ROOT / "cache" / "test_groups.json"

VENV_PY = REPO_ROOT / "world-quant-brain-mcp" / ".venv" / "Scripts" / "python.exe"

UNIT_DIR = REPO_ROOT / "tests" / "unit"
TESTS_DIR = REPO_ROOT / "tests"
MCP_TESTS_DIR = REPO_ROOT / "world-quant-brain-mcp" / "tests"

GROUP_DIR_RE = re.compile(r"^\d{2}_")


def rel(p: Path) -> str:
    """仓库相对路径（统一用 / 分隔，产物里不出现绝对路径）。"""
    try:
        return p.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except Exception:  # noqa: BLE001
        return p.as_posix()


def cases_in_file(path: Path) -> list:
    """AST 解析出测试函数/方法，返回 node id 后缀列表（Class::func 或 func）。"""
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src)
    except Exception:  # noqa: BLE001 - 语法坏的文件跳过，不拖垮整体
        return []

    found: list = []

    def walk(node, prefix: str):
        for n in getattr(node, "body", []):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if n.name.startswith("test"):
                    found.append(prefix + n.name)
            elif isinstance(n, ast.ClassDef):
                # 只往下钻类名以 Test 开头或全量？pytest 默认收集 Test* 类，
                # 但本项目也用普通类组织，故一律下钻（无害）
                walk(n, prefix + n.name + "::")

    walk(tree, "")
    return found


def collect_nodeids(timeout: int = 240) -> dict:
    """用 pytest --collect-only 拿真实用例清单（含参数化展开），失败返回 None。

    AST 会把 parametrize 的一组算成 1 个，与 pytest 实际执行的条数不符，
    故优先用 collect-only（准确），AST 仅作兜底。
    返回 {相对文件路径: [node id 后缀, ...]}。
    """
    py = str(VENV_PY) if VENV_PY.exists() else sys.executable
    try:
        r = subprocess.run(
            [py, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider"],
            cwd=str(REPO_ROOT), capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=timeout,
        )
    except Exception:  # noqa: BLE001 - 超时/解释器缺失都走兜底
        return None

    # 注意：参数化 id 可能含空格（如 test_x[a b]），故后缀用 (.+) 而非 (\S+)
    pat = re.compile(r"^(\S+\.py)::(.+)$")
    out: dict = {}
    for raw in (r.stdout or "").splitlines():
        line = raw.strip()
        for tok in ("ERROR ", "FAILED ", "SKIPPED ", "XFAIL ", "XPASS "):
            if line.startswith(tok):
                line = line[len(tok):].strip()
                break
        m = pat.match(line)
        if m:
            out.setdefault(m.group(1), []).append(m.group(2))
    return out or None


def build_group(gid: str, name: str, gdir: str, files: list, casemap: dict = None) -> dict:
    items = []
    total = 0
    for f in sorted(files, key=lambda x: x.as_posix()):
        rp = rel(f)
        if casemap is not None and rp in casemap:
            names = casemap[rp]          # pytest 真实收集的（含参数化）
        else:
            names = cases_in_file(f)     # 兜底：AST
        # cases 只存名字后缀；node id 由前端按 "文件路径::名字" 拼出，省一半体积
        items.append({
            "path": rp,
            "case_count": len(names),
            "cases": names,
        })
        total += len(names)
    return {
        "id": gid,
        "name": name,
        "dir": gdir,
        "file_count": len(items),
        "case_count": total,
        "files": items,
    }


def scan(casemap: dict = None) -> dict:
    groups: list = []

    # 1) tests/unit/ 下的编号目录（10 个领域分组）
    if UNIT_DIR.exists():
        for d in sorted(UNIT_DIR.iterdir(), key=lambda x: x.name):
            if d.is_dir() and GROUP_DIR_RE.match(d.name):
                files = [p for p in d.rglob("test_*.py") if "__pycache__" not in p.parts]
                if files:
                    groups.append(build_group(d.name, d.name, rel(d), files, casemap))

    # 2) tests/ 根级
    if TESTS_DIR.exists():
        root_files = [p for p in TESTS_DIR.glob("test_*.py")]
        if root_files:
            groups.append(build_group("tests_root", "tests 根级", rel(TESTS_DIR), root_files, casemap))

    # 3) MCP 包
    if MCP_TESTS_DIR.exists():
        mcp_files = [p for p in MCP_TESTS_DIR.rglob("test_*.py") if "__pycache__" not in p.parts]
        if mcp_files:
            groups.append(build_group("mcp_pkg", "MCP 包", rel(MCP_TESTS_DIR), mcp_files, casemap))

    return {
        "generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
        "total_files": sum(g["file_count"] for g in groups),
        "total_cases": sum(g["case_count"] for g in groups),
        "groups": groups,
    }


def main() -> int:
    print("[INFO] 用 pytest --collect-only 收集真实用例（约 7s）…", file=sys.stderr)
    casemap = collect_nodeids()
    src = "pytest --collect-only" if casemap else "AST 静态解析（collect 不可用，已兜底）"
    data = scan(casemap)
    data["source"] = src
    DATA.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] 扫描完成 → {DATA.name}（数据源：{src}）")
    print(f"     分组 {len(data['groups'])} 个｜文件 {data['total_files']} 个｜用例 {data['total_cases']} 个")
    for g in data["groups"]:
        print(f"       {g['name']:<22} {g['file_count']:>3} 文件 / {g['case_count']:>4} 用例")
    kb = DATA.stat().st_size // 1024
    print(f"     产物体积 {kb} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
