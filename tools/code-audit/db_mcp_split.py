# -*- coding: utf-8 -*-
"""db_mcp_split.py - 根入口 `wqb_db_mcp.py` 的拆分生成器（一次性工具，非通用）

【只为一件事存在】把 2026-10-04 P2-2 踩过的坑固化成可重跑的流程：分组表 + 常量归位 +
逐字节搬运 + **写盘前的组间 DAG 环硬门**。下一次执行拆分时不该重新设计这些。

用法：
    python tools/code-audit/db_mcp_split.py --plan      # 只出分组/跳组依赖/DAG 报告
    python tools/code-audit/db_mcp_split.py --apply     # 写 src/wqb/db_mcp/* 与根门面

执行前先跑凭据与备份（顺位见 `reports/db_mcp_split_20261004.md` 第五节）：
    python tools/code-audit/mcp_surface_diff.py --tag before
拆完必须：`--tag after` 要 47=47 逐项一致；还要同步改 26 条源码文本断言 +
`db_conn.DIRECT_CONNECT_WHITELIST`（否则全量测试会响亮地红）。
本工具只在入口未拆时适用（它把当前根文件当唯一输入源）。

v2 相比 v1 修掉的三件事（都是实测踩出来的）：
  1. **读写同源**：门面不再按值导出 DB_PATH，而是用 PEP 562 `__getattr__` 实时委托
     context —— 否则测试 `set_db_path()` 之后再读 `mod.DB_PATH` 会拿到陈值。
  2. 保留 `set_db_path/get_db_path` + 结果层硬闸（v1 时代没有，导致测试静默写生产库）。
  3. 根路径改走 `wqb.paths`（层数无关），不再依赖 `Path(__file__).parent` 假设文件躺在仓库根。
函数体仍**逐字节搬运**（含装饰器），仅 `str(DB_PATH)` → `get_db_path()` 这一类等价替换。
"""
import argparse
import ast
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from wqb.paths import repo_root        # noqa: E402  本文件在 tools/code-audit/，层数无关解析

REPO = repo_root()
ROOT_FILE = REPO / "wqb_db_mcp.py"
PKG = REPO / "src" / "wqb" / "db_mcp"

text = ROOT_FILE.read_text(encoding="utf-8")
lines = text.splitlines(keepends=True)
tree = ast.parse(text)

GROUPS = {
    "context": ["_store", "_conn", "_rows_to_dicts", "_parse_json_fields",
                "_now", "_deep_merge", "_num", "_json_value"],
    "queries_waves": ["get_wave_result", "list_wave_results", "get_latest_wave",
                      "get_region_config", "get_dead_ends", "get_campaigns",
                      "get_cross_region_lessons", "get_campaign_summary",
                      "get_region_overview", "get_mining_yield"],
    "queries_ledger": ["get_ledger_key", "list_ledger_keys", "get_submit_ready",
                       "get_dead_datasets"],
    "queries_fields": ["upsert_field_catalog", "get_field_catalog",
                       "build_field_prefix_clusters", "get_field_prefix_clusters",
                       "upsert_expressions", "list_expressions", "set_expression_status"],
    # 写路径/收割/轮转/判死/相关性互引成环（v1 --plan 实测），必须同模块，
    # 否则包内循环 import → 服务启动即失败。
    "mutations": [
        "upsert_ledger_key", "upsert_wave_result", "upsert_registry_empirical",
        "upsert_backtest_rows", "upsert_gate_result", "get_gate_result",
        "_canonicalize_ledger_value", "_get_ledger_raw", "_upsert_ledger_raw",
        "_whitelist_dead_guard", "_profile_drift_hook", "_cascade_wave_result",
        "harvest_multisim_results", "_harvest_candidate", "_salvage_to_pool",
        "_infer_dataset_from_expr", "get_salvage_pool", "backfill_salvage_pool",
        "backfill_salvage_pool_batch", "seal_dead_end", "_forum_recon_gate",
        "region_rotation", "_region_near_line", "_read_entry_verdict",
        "get_alpha_by_id", "list_alphas_by_wave", "search_alphas_by_sharpe",
        "get_alpha_corr_metrics", "persist_correlation", "_parse_corr_checked_at",
        "_flatten_platform_alpha",
    ],
    "step_events": ["record_step_event", "get_step_events", "get_step_eval_report"],
    "workflow_bridge": ["workflow_inventory_scan", "workflow_gem_wave",
                        "workflow_unified_gate", "workflow_auto_harvest",
                        "workflow_auto_review", "workflow_auto_pyramid"],
}

# 顶层常量的强制归属（其余按"被哪个组用"自动归位；多组用 → context）
CONST_FORCE = {
    "_REGION_PROFILE_DIR": "mutations", "_CANONICAL_LEDGER_KEYS": "mutations",
    "_WAVE_VERDICT_OK": "mutations", "_normalize_wave_verdict": "mutations",
    "HARVEST_SOURCE": "mutations", "_HARD_GATE": "mutations",
    "_NEAR_LINE_FALLBACK": "mutations", "_PROFILE_DRIFT_LAYERS": "mutations",
    "_GATE_DECISIONS": "mutations", "_EVIDENCE_KEEP": "mutations",
}
# 由门面/context 自己手写、不从原文搬运的顶层语句
# （_self = sys.modules.get(__name__) 是**门面专属**的类交换变量，不能跟到 context 去）
SKIP_CONSTS = {"ROOT", "SRC", "DB_PATH", "mcp", "_self"}
# v1 已验证：这些是 set_db_path/get_db_path/_reject… 与 _GuardedModule，手写进 context/门面
SKIP_FUNC = {"set_db_path", "get_db_path", "_reject_production_db_under_tests"}

funcs, consts = {}, {}
for node in tree.body:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        start = min([node.lineno] + [d.lineno for d in node.decorator_list])
        funcs[node.name] = (start, node.end_lineno)
    elif isinstance(node, ast.Assign):
        for t in node.targets:
            consts[ast.unparse(t)] = (node.lineno, node.end_lineno)

owner = {}
for g, members in GROUPS.items():
    for m in members:
        if m not in funcs:
            print(f"[FATAL] 组 {g} 里的 {m} 不是顶层函数")
            sys.exit(2)
        owner[m] = g
leftover = sorted(set(funcs) - set(owner) - SKIP_FUNC)
if leftover:
    print(f"[FATAL] 未分组函数 {len(leftover)}：{leftover}")
    sys.exit(2)


def refs(name):
    s, e = funcs[name]
    src = text.splitlines()[s - 1:e]
    try:
        sub = ast.parse("\n".join(src))
    except SyntaxError:
        return set()
    out = {n.func.id for n in ast.walk(sub)
           if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    out |= {n.id for n in ast.walk(sub) if isinstance(n, ast.Name)}
    return out


dep = {n: refs(n) for n in funcs}

const_owner = {}
for c in consts:
    if c in SKIP_CONSTS:
        continue
    if c in CONST_FORCE:
        const_owner[c] = CONST_FORCE[c]
        continue
    users = {owner[f] for f in funcs if c in dep.get(f, ())}
    const_owner[c] = next(iter(users)) if len(users) == 1 else "context"

need = defaultdict(lambda: defaultdict(set))
for f, (s, e) in funcs.items():
    for r in dep[f]:
        if r in owner and owner[r] != owner[f]:
            need[owner[f]][owner[r]].add(r)
        elif r in const_owner and const_owner[r] != owner[f]:
            need[owner[f]][const_owner[r]].add(r)

edges = defaultdict(set)
for g, deps in need.items():
    edges[g] |= set(deps)


def cycle(g):
    seen, stack = set(), set()

    def dfs(n):
        if n in stack:
            return [n]
        if n in seen:
            return None
        seen.add(n)
        stack.add(n)
        for m in sorted(edges.get(n, ())):
            c = dfs(m)
            if c:
                return c + [n]
        stack.discard(n)
        return None
    return dfs(g)


print(f"顶层函数 {len(funcs)}（已分组 {len(owner)}）｜常量 {len(consts)}")
for g in sorted(edges):
    print(f"  {g:16} -> {sorted(edges[g])}")
c = next((x for x in (cycle(g) for g in sorted(edges)) if x), None)
if c:
    print(f"[FATAL] 组间环：{' -> '.join(reversed(c))}")
    sys.exit(3)
print("DAG 校验：无环 ✅\n")

if "--plan" in sys.argv:
    for g in sorted(GROUPS):
        cs = sorted(k for k, v in const_owner.items() if v == g)
        print(f"{g}: {len(GROUPS[g])} 函数｜常量 {cs}")
    sys.exit(0)

HEADER = '''# -*- coding: utf-8 -*-
"""wqb-db MCP 实现层 · {mod}（2026-10-04 P2-2 由根 wqb_db_mcp.py verbatim 拆出）。

函数体逐字节搬运，逻辑未改写；共享状态（库指向 / mcp 实例 / 结果层硬闸）在 `.context`。
旧导入路径 `from wqb_db_mcp import …` 由仓库根门面保持兼容（同 brain_api 门面约定）。
"""
from __future__ import annotations

import datetime
import json
import logging
import os
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from mcp.server.fastmcp import FastMCP

from wqb import recon_evidence as _recon_evidence
from wqb import registry_contract as _registry_contract
from wqb import wave_results_contract as _wave_contract
from wqb.config import compute_webdata_failed_counts
from wqb.store import CampaignStore

from .context import (  # noqa: F401
    ROOT, get_db_path, mcp, set_db_path, _conn, _deep_merge, _json_value,
    _now, _num, _parse_json_fields, _rows_to_dicts, _store,
)
'''

#: 注意：**不把 DB_PATH 放进子模块 import 表**。按值导入会在导入时抄一次陈值，
#: 之后 set_db_path() 就看不到了 —— 那正是 P2-2 v1 的静默错位形态。子模块一律走
#: get_db_path()；真的有人误读 DB_PATH 则 NameError 响亮报出，而不是拿陈值跑。
HEADER_BASE = HEADER.split("from .context import (")[0]
CTX_UTIL_IMPORTS = ""   # context 不 import 自己

# context 里手写的状态与闸（从现根文件原文抽出 set_db_path/get_db_path/_reject…）
def extract(name):
    s, e = funcs[name]
    return "\n".join(text.splitlines()[s - 1:e])


PKG.mkdir(parents=True, exist_ok=True)


def block(s, e):
    src = "\n".join(text.splitlines()[s - 1:e])
    return src.replace("str(DB_PATH)", "get_db_path()")


ctx = [HEADER_BASE.format(mod="context（共享状态：库指向、mcp 实例、结果层硬闸）"), '''
from wqb.paths import repo_relative

#: 仓库根：`wqb.paths` 向上探测，**与文件所在层数无关**（AGENTS.md §8.13）。
#: 旧写法 `ROOT = Path(__file__).resolve().parent` 只对"躺在仓库根"成立，拆包即失效。
ROOT = repo_relative()
SRC = ROOT / "src"

#: 库指向是**可变状态**：测试经 `set_db_path()` 改它，所有读点走 `get_db_path()`。
DB_PATH: Path = Path(os.environ.get("WQB_DB_PATH") or str(ROOT / "data" / "wqb.db"))

mcp = FastMCP(
    "wqb-db-mcp",
    "Local wqb.db query service (single-track DB mode)",
)


''']
for n in ["set_db_path", "get_db_path", "_reject_production_db_under_tests"]:
    ctx.append("\n\n" + extract(n).replace("str(DB_PATH).replace", "str(DB_PATH).replace") + "\n")
for n in GROUPS["context"]:
    ctx.append("\n\n" + block(*funcs[n]) + "\n")
for c in sorted(const_owner):
    if const_owner[c] == "context":
        ctx.append("\n\n" + block(*consts[c]) + "\n")
(PKG / "context.py").write_text("".join(ctx), encoding="utf-8")

for g in sorted(GROUPS):
    if g == "context":
        continue
    parts = [HEADER.format(mod=g)]
    for dg, names in sorted(need.get(g, {}).items()):
        skip = {"get_db_path", "set_db_path", "mcp", "_conn", "_store",
                "_now", "_num", "_json_value", "_rows_to_dicts",
                "_parse_json_fields", "_deep_merge", "ROOT"}
        real = sorted(n for n in names if not (dg == "context" and n in skip))
        if real:
            parts.append(f"\nfrom .{dg} import {', '.join(real)}  # noqa: F401\n")
    for c in sorted(k for k, v in const_owner.items() if v == g):
        parts.append("\n" + block(*consts[c]) + "\n")
    for n in GROUPS[g]:
        parts.append("\n\n" + block(*funcs[n]) + "\n")
    (PKG / f"{g}.py").write_text("".join(parts), encoding="utf-8")

order = ["context"] + [g for g in sorted(GROUPS) if g != "context"]
init = ['''# -*- coding: utf-8 -*-
"""wqb.db MCP 的实现层（2026-10-04 P2-2 由根 `wqb_db_mcp.py` 拆出）。

import 本包即完成全部 `@mcp.tool()` 注册；仓库根 `wqb_db_mcp.py` 是**门面 + .mcp.json
入口**，保持 `from wqb_db_mcp import …` 旧路径与 47 个工具面不变（同 brain_api 门面约定）。
"""
''']
for g in order:
    init.append(f"from . import {g}  # noqa: F401\n")
init.append("\nfrom .context import get_db_path, mcp, set_db_path  # noqa: F401,E402\n")
(PKG / "__init__.py").write_text("".join(init), encoding="utf-8")

# ---------------- 根门面 ----------------
doc = "\n".join(text.splitlines()[:22])
fac = [doc, '''

import sys as _sys
import types as _types
from pathlib import Path as _Path

_ROOT = _Path(__file__).resolve().parent
_SRC = _ROOT / "src"
if str(_SRC) not in _sys.path:
    _sys.path.insert(0, str(_SRC))

from wqb.db_mcp import get_db_path, mcp, set_db_path  # noqa: E402  import 即注册全部工具
from wqb.db_mcp import context as _context  # noqa: E402
''']
for g in [x for x in order if x != "context"]:
    fac.append(f"\nfrom wqb.db_mcp.{g} import (  # noqa: E402,F401\n"
               f"    {', '.join(GROUPS[g])},\n)\n")
fac.append('''

def __getattr__(name):
    """`DB_PATH` 实时委托 context —— 保证 `set_db_path()` 后读 `wqb_db_mcp.DB_PATH` 也是新值。

    按值 `from .context import DB_PATH` 会在导入时抄一次，之后两者分叉：那是又一次
    「读写不同源」的静默错位（P2-2 v1 就栽在相邻的一处）。
    """
    if name == "DB_PATH":
        return _context.DB_PATH
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


class _GuardedModule(_types.ModuleType):
    """拦 `wqb_db_mcp.DB_PATH = …`：属性式 patch 在结构变动后会静默失效（写生产库）。"""

    def __setattr__(self, name, value):
        if name == "DB_PATH":
            raise AttributeError(
                "DB_PATH 不可直接赋值：请用 set_db_path(...)。属性式 patch 在 DB 访问被"
                "抽到别的模块后会静默失效，测试会把数据写进生产 data/wqb.db。")
        super().__setattr__(name, value)


_self = _sys.modules.get(__name__)
if _self is not None:
    _self.__class__ = _GuardedModule


if __name__ == "__main__":
    import os as _os_sc
    _os_sc.environ.setdefault("WQB_STARTUP_CHECKS", "once")  # 启动校验每进程只打一次（2026-09-19）
    mcp.run()
''')
ROOT_FILE.write_text("".join(fac), encoding="utf-8")

print(f"[apply] {PKG.relative_to(REPO).as_posix()}：{len(order)} 模块")
print(f"[apply] 根门面 {len(''.join(fac).splitlines())} 行")
