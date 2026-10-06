# -*- coding: utf-8 -*-
"""mcp_surface_diff.py - MCP 工具面快照与比对（拆分/重构的回归凭据）

为什么需要它
------------
拆分一个承载 MCP 工具注册的模块时，"函数体逐字节搬运、行为不变"是**主张**而不是事实。
唯一能机器证明的是工具面：tool 名集合、docstring、inputSchema（由签名生成）三项全等。
2026-10-04 拆 `wqb_db_mcp.py` 就靠它判定"拆分本身成功、失败全在耦合面"。

用法
----
    python tools/code-audit/mcp_surface_diff.py --tag before      # 改动前
    # …做改动…
    python tools/code-audit/mcp_surface_diff.py --tag after       # 自动与 before 比对

模块通过 `.mcp.json` 里的入口名导入（默认 `wqb_db_mcp`），也可 `--module` 指定。
快照落在 `cache/mcp_surface_<tag>.json`（运行产物，不入库）。

退出码：0 = 一致（或首次建基线）；1 = 有回归（丢失/新增/docstring/schema 变化）；2 = 工具故障。
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2] / "src"))
from wqb.paths import repo_root            # noqa: E402  层数无关，本文件可安全搬家

REPO = repo_root()
OUT_DIR = REPO / "cache"


def _load(module_name: str):
    """按仓库根入口名导入（这些模块刻意躺在根，需要 sys.path 有仓库根）。"""
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    return __import__(module_name)


async def _snapshot(module_name: str) -> list:
    mod = _load(module_name)
    tools = await mod.mcp.list_tools()
    return sorted(
        [{"name": t.name,
          "desc": (t.description or "").strip()[:200],
          "schema": json.dumps(t.inputSchema, sort_keys=True, ensure_ascii=False)}
         for t in tools],
        key=lambda x: x["name"])


def main() -> int:
    ap = argparse.ArgumentParser(description="MCP 工具面快照与比对（只读）")
    ap.add_argument("--tag", required=True, choices=["before", "after"])
    ap.add_argument("--module", default="wqb_db_mcp", help="含 `mcp` 实例的入口模块名")
    a = ap.parse_args()

    try:
        rows = asyncio.run(_snapshot(a.module))
    except Exception as e:  # 工具故障 ≠ 回归，用退出码 2 区分
        print(f"[error] 导入/列举失败：{type(e).__name__}: {e}", file=sys.stderr)
        return 2

    dest = OUT_DIR / f"mcp_surface_{a.tag}.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[{a.tag}] tools = {len(rows)} → {dest.relative_to(REPO).as_posix()}")

    if a.tag != "after":
        return 0
    base = OUT_DIR / "mcp_surface_before.json"
    if not base.is_file():
        print("[warn] 无 before 基线，无法比对")
        return 0

    before = json.loads(base.read_text(encoding="utf-8"))
    by_b = {x["name"]: x for x in before}
    names_b = set(by_b)
    names_a = {x["name"] for x in rows}
    lost, added = sorted(names_b - names_a), sorted(names_a - names_b)
    d_desc = [x["name"] for x in rows
              if x["name"] in by_b and x["desc"] != by_b[x["name"]]["desc"]]
    d_schema = [x["name"] for x in rows
                if x["name"] in by_b and x["schema"] != by_b[x["name"]]["schema"]]
    print(f"比对 before={len(names_b)} after={len(names_a)}")
    print(f"  丢失={lost or '无'}")
    print(f"  新增={added or '无'}")
    print(f"  docstring 变化={d_desc or '无'}")
    print(f"  inputSchema 变化={d_schema or '无'}")
    if lost or added or d_desc or d_schema:
        print("→ 工具面有回归 ❌")
        return 1
    print("→ 工具面逐项一致 ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
