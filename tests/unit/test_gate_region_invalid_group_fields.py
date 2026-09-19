# -*- coding: utf-8 -*-
"""2026-09-19 闸2b：区域非法 group 字段（JPN sector/subindustry/industry）必须在本地闸 FAIL。

实证：JPN 2026-09-15 模拟层报 'Invalid data field subindustry/sector'（POST 可接受、执行必 ERROR），
JPN wave7 池里 15 条这类表达式若入批会连坐整批 CANCELLED。名单在 platform_constraints.json
`region_invalid_group_fields`（单一事实源，GEM 侧 pipeline_pregate 同源）。
"""
import json
import os
import re
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TK_SCRIPTS = os.path.join(REPO, "Claude", "skills", "wq-brain-campaign-toolkit", "scripts")
CFG = os.path.join(REPO, "Claude", "skills", "wq-brain-campaign-toolkit",
                   "config", "platform_constraints.json")


@pytest.fixture(scope="module")
def gate():
    sys.path.insert(0, TK_SCRIPTS)
    import gate  # noqa: PLC0415
    return gate


@pytest.fixture(scope="module")
def pc():
    return json.loads(open(CFG, encoding="utf-8").read())


def _issues(gate, pc, expr, region):
    p = dict(pc)
    p["_region"] = region
    idents = set(re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", expr))
    o = gate.check_one(expr, (idents, "MATRIX", {}, []), None, [], p)
    return o["issues"]


def test_config_declares_jpn_invalid_groups(pc):
    assert set(pc["region_invalid_group_fields"]["JPN"]) == {"sector", "subindustry", "industry"}


def test_jpn_sector_is_a_field_fail(gate, pc):
    issues = _issues(gate, pc, "group_zscore(rank(mdl_x), sector)", "JPN")
    assert any("不支持的 group 字段" in i and "sector" in i for i in issues), issues


def test_same_expression_passes_in_ind(gate, pc):
    issues = _issues(gate, pc, "group_zscore(rank(mdl_x), sector)", "IND")
    assert not any("不支持的 group 字段" in i for i in issues), issues


def test_jpn_market_is_fine(gate, pc):
    issues = _issues(gate, pc, "group_neutralize(rank(mdl_x), market)", "JPN")
    assert not any("不支持的 group 字段" in i for i in issues), issues
