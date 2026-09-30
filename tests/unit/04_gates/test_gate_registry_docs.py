# -*- coding: utf-8 -*-
"""gate.py 闸注册表（GATE_REGISTRY）是闸编号的唯一来源（skills 审查 X-7 / IX-11，2026-09-29）。

此前 INDEX / toolkit / gate.py 模块头都宣称自己是「闸编号唯一基准」，且都漏了闸 2b / 2b-2 / 9
（代码里有、文档里没有）。现在：注册表在代码里，INDEX 的闸表由 `gate.py --print-gate-table` 生成，
本测试比对两者，并保证 check_one 注释里出现的每个闸号都已登记。
"""
import importlib.util
import inspect
import re
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
GATE = REPO / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts" / "gate.py"
INDEX = REPO / "Claude" / "skills" / "INDEX.md"


@pytest.fixture(scope="module")
def g():
    for p in (str(REPO / "src"), str(GATE.parent)):
        if p not in sys.path:
            sys.path.insert(0, p)
    spec = importlib.util.spec_from_file_location("_gate_registry_test", GATE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_gate_registry_test"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_index_gate_table_is_generated_from_the_registry(g):
    text = INDEX.read_text(encoding="utf-8")
    m = re.search(r"<!-- gate-table:start -->\n(.*?)\n<!-- gate-table:end -->", text, re.S)
    assert m, "INDEX 缺 <!-- gate-table:start/end --> 标记"
    assert m.group(1).strip() == g.render_gate_table().strip(), (
        "INDEX 闸表与 GATE_REGISTRY 不一致——先改注册表，再运行 "
        "`python Claude/skills/wq-brain-campaign-toolkit/scripts/gate.py --print-gate-table` 重新生成")


def test_registry_ids_are_unique_and_well_formed(g):
    ids = [row[0] for row in g.GATE_REGISTRY]
    assert len(ids) == len(set(ids))
    for gid, name, kind, sw, note in g.GATE_REGISTRY:
        assert re.fullmatch(r"\d+(b(-\d+)?)?", gid), gid
        assert kind in ("block", "warn"), (gid, kind)
        assert name and sw and note


def test_eight_gates_plus_gate0_plus_subgates_are_all_registered(g):
    ids = {row[0] for row in g.GATE_REGISTRY}
    assert {str(i) for i in range(0, 10)} <= ids                    # 闸0–9
    assert {"1b", "2b", "2b-2"} <= ids                              # 此前文档漏登记的子闸
    numbered = {i for i in ids if i.isdigit() and 1 <= int(i) <= 8}
    assert len(numbered) == 8                                       # 「8 闸」口径 = 闸1–8（+ 闸0 可选）


def test_every_gate_mentioned_in_check_one_is_registered(g):
    src = inspect.getsource(g.check_one)
    mentioned = set(re.findall(r"#\s*闸(\d+(?:b(?:-\d+)?)?)", src))
    registered = {row[0] for row in g.GATE_REGISTRY}
    assert mentioned, "未解析到 check_one 里的闸注释（解析规则失效？）"
    assert mentioned <= registered, f"check_one 出现了未登记的闸: {sorted(mentioned - registered)}"


def test_header_keeps_the_declared_gate_count(g):
    head = GATE.read_text(encoding="utf-8")[:2000]
    assert "8 闸" in head and "闸0" in head and "GATE_REGISTRY" in head
