# -*- coding: utf-8 -*-
"""audit_node_registration.py — 新增 workflow 节点「四处同步」机械审计器。

背景（2026-09-18 教训）：`alpha_booster` 节点注册进 registry 后，三处配套漏同步，
导致 3 个测试红；`gem` 节点也曾漏 `batch_size` 元数据。这类漂移的代价是
`workflow_list_nodes` 把 NodeMeta 当 API 文档暴露给 Agent，漂移即误导。

新增/修改 workflow 节点时必须同步的 **四处**：
  ① `src/wqb/workflow/registry.py`            —— 节点注册 + NodeMeta（required/optional 须与 run() 签名一致）
  ② `tests/unit/test_workflow.py`             —— `test_registry_lists_all_core_nodes` 的期望节点集合
  ③ `tests/unit/test_skill_integrity.py`      —— `_DRY_RUN_CASES` 干跑用例表
  ④ `Claude/skills/INDEX.md`                  —— workflow 节点计数（`test_docs_consistency.py` 守护）

本工具把这四处做成一张对照表，**一次性列出全部缺口**，避免"改一处跑一次测试"的往返。

用法：
  python tools/audit_node_registration.py            # 全量审计（默认，发现漂移 rc=1）
  python tools/audit_node_registration.py --node X   # 只审某个节点（新增节点后自检）
  python tools/audit_node_registration.py --quiet    # 只在有漂移时输出
"""
from __future__ import annotations

import argparse
import inspect
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SRC = REPO / "src"
INDEX = REPO / "Claude" / "skills" / "INDEX.md"
TEST_WORKFLOW = REPO / "tests" / "unit" / "test_workflow.py"
TEST_INTEGRITY = REPO / "tests" / "unit" / "test_skill_integrity.py"
REGISTRY = SRC / "wqb" / "workflow" / "registry.py"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def _load_registry():
    from wqb.workflow import get_registry
    return get_registry()


def _parse_test_workflow_nodes() -> set:
    """从 test_registry_lists_all_core_nodes 的集合字面量里提取节点名。

    先剥掉注释行——历史注释里会写「已移除 step_metrics」这类说明文字，
    不剥会把已下线节点误判为"期望里多余"。
    """
    src = TEST_WORKFLOW.read_text(encoding="utf-8")
    m = re.search(
        r"def test_registry_lists_all_core_nodes\(\):(.*?)\n\n\ndef ",
        src, re.S,
    )
    if not m:
        return set()
    body = m.group(1)
    body = "\n".join(
        ln for ln in body.splitlines() if not ln.lstrip().startswith("#")
    )
    # 集合字面量内的字符串字面量（= 节点名）
    return set(re.findall(r'"([a-z_][a-z0-9_]*)"', body))


def _parse_dry_run_cases() -> set:
    """从 test_skill_integrity.py 的 _DRY_RUN_CASES 字典提取键。"""
    src = TEST_INTEGRITY.read_text(encoding="utf-8")
    m = re.search(r"_DRY_RUN_CASES = \{(.*?)\n\}", src, re.S)
    if not m:
        return set()
    body = m.group(1)
    return set(re.findall(r'^\s*"([a-z_][a-z0-9_]*)":\s*\{', body, re.M))


def _parse_index_node_count():
    """从 INDEX.md 提取 workflow 节点计数（基准段）。"""
    src = INDEX.read_text(encoding="utf-8")
    m = re.search(r"workflow 节点：\*\*(\d+) 个\*\*", src)
    return int(m.group(1)) if m else None


def _signature_drift(reg) -> dict:
    """比对 NodeMeta 与 run() 签名（复刻 test_registry_meta_matches_node_signature）。"""
    drift = {}
    for name in reg.list_nodes():
        meta = reg.get_meta(name)
        fn = reg.get(name)
        if meta is None or fn is None:
            continue
        sig = inspect.signature(fn)
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
    return drift


def main() -> int:
    ap = argparse.ArgumentParser(description="workflow 节点四处同步审计")
    ap.add_argument("--node", help="只审计指定节点")
    ap.add_argument("--quiet", action="store_true", help="只在有漂移时输出")
    a = ap.parse_args()

    reg = _load_registry()
    nodes = set(reg.list_nodes())
    if a.node:
        if a.node not in nodes:
            print(f"[ERR] registry 未注册节点：{a.node}")
            return 1
        nodes = {a.node}

    tw_nodes = _parse_test_workflow_nodes()
    dr_nodes = _parse_dry_run_cases()
    idx_count = _parse_index_node_count()
    sig_drift = _signature_drift(reg)

    problems = []

    # ① registry vs ② test_workflow 期望集合
    only_registry = nodes - tw_nodes
    only_test = tw_nodes - set(reg.list_nodes())
    if only_registry and not a.node:
        problems.append(
            f"[② test_workflow.py] 期望集合缺 {sorted(only_registry)}"
            f" —— 在 test_registry_lists_all_core_nodes 里补上")
    if only_test:
        problems.append(
            f"[② test_workflow.py] 期望集合多了 {sorted(only_test)}"
            f" —— registry 已无此节点，从期望里删掉")

    # ① registry vs ③ _DRY_RUN_CASES
    miss_dry = nodes - dr_nodes
    extra_dry = dr_nodes - set(reg.list_nodes())
    if miss_dry:
        problems.append(
            f"[③ test_skill_integrity.py] _DRY_RUN_CASES 缺 {sorted(miss_dry)}"
            f" —— 补干跑参数（纯本地/零副作用参数）")
    if extra_dry:
        problems.append(
            f"[③ test_skill_integrity.py] _DRY_RUN_CASES 多了 {sorted(extra_dry)}"
            f" —— 节点已下线，删掉用例")

    # ① registry NodeMeta vs run() 签名
    for name, probs in sorted(sig_drift.items()):
        if a.node and name != a.node:
            continue
        problems.append(f"[① registry.py] {name} NodeMeta 与签名漂移：{probs}")

    # ④ INDEX 计数
    if idx_count is not None and not a.node:
        if idx_count != len(reg.list_nodes()):
            problems.append(
                f"[④ INDEX.md] 记 {idx_count} 个，registry 实为 {len(reg.list_nodes())} 个"
                f" —— 同步 INDEX 基准段（并补一句溯源说明）")

    if not a.quiet:
        print("=" * 72)
        print(f"workflow 节点四处同步审计 | registry={len(reg.list_nodes())} 个"
              f" | test_workflow={len(tw_nodes)} | dry_run={len(dr_nodes)} | INDEX={idx_count}")
        print("=" * 72)
        print(f"  ① registry.py            : {len(reg.list_nodes())} 个节点"
              + (f"，其中 {len(sig_drift)} 个签名漂移" if sig_drift else "，签名一致"))
        print(f"  ② test_workflow.py       : {len(tw_nodes)} 个期望")
        print(f"  ③ _DRY_RUN_CASES         : {len(dr_nodes)} 个用例")
        print(f"  ④ INDEX.md workflow 节点 : {idx_count}")

    if problems:
        print(f"\n检测到 {len(problems)} 处漂移：")
        for p in problems:
            print(f"  ✗ {p}")
        print("\n修复后跑：python -m pytest tests/unit/test_workflow.py "
              "tests/unit/test_skill_integrity.py tests/unit/test_docs_consistency.py -q")
        return 1

    if not a.quiet:
        print("\n四处一致，无漂移。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
