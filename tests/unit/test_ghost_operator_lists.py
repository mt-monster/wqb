# -*- coding: utf-8 -*-
"""幽灵算子（平台不存在）的口径与拦截（skills 审查 T0-12 / X-16 / DF-08，2026-09-29）。

证据（MCP `operator_audit`，本地 stdio 连接实测）：`ts_median` 是幽灵算子（violations=ghost_ops[ts_median]），
而 `validate_expressions` / `preflight_expressions` 对它返回 valid=true——**这两个工具不查幽灵算子**，
所以 SOP 里的"预检"不能只写 validate/preflight；闸门（gate.py）与 operator_audit 才是拦截点。

同源问题：ghost 名单曾有多份（platform_constraints.ghost_ops=10、wqb.config.GHOST_OPERATORS=18、
verifier 的 GHOST_OPERATORS、KB ghost_operator_advisory）。单源 = wqb.config.GHOST_OPERATORS ∪ inaccessible_ops，
其余名单必须是其子集（本测试守护漂移）。
另：ts_event_* 在平台不存在（tracking/KOR/TOOLKIT_CHECKLIST.md Wave16：102 个算子中无该系列，8/8 ERROR）。
"""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
TK = REPO / "Claude" / "skills" / "wq-brain-campaign-toolkit"
PC = TK / "config" / "platform_constraints.json"
GATE = TK / "scripts" / "gate.py"

for _p in (str(REPO / "src"), str(TK / "scripts"), str(REPO / "Claude" / "skills" / "alpha-expression-verifier" / "scripts")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from wqb.config import GHOST_OPERATORS  # noqa: E402


@pytest.fixture(scope="module")
def g():
    spec = importlib.util.spec_from_file_location("_gate_ghost_test", GATE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_gate_ghost_test"] = mod
    spec.loader.exec_module(mod)
    return mod


def _pc():
    pc = json.loads(PC.read_text(encoding="utf-8"))
    pc["_region"] = "USA"
    return pc


def test_platform_constraints_ghost_list_is_a_subset_of_the_single_source():
    pc = _pc()
    allowed = set(GHOST_OPERATORS) | set(pc["inaccessible_ops"])
    stray = sorted(set(pc["ghost_ops"]) - allowed)
    assert not stray, f"platform_constraints.ghost_ops 含不在单源里的算子: {stray}"


def test_verifier_ghost_list_is_a_subset_of_the_single_source():
    import validator  # alpha-expression-verifier（gate 1 直调）
    stray = sorted(set(validator.GHOST_OPERATORS) - set(GHOST_OPERATORS))
    assert not stray, f"verifier.GHOST_OPERATORS 含不在单源里的算子: {stray}"


def test_ts_median_is_a_ghost_everywhere():
    assert "ts_median" in GHOST_OPERATORS
    assert "ts_median" in _pc()["ghost_ops"]


@pytest.mark.parametrize("op", sorted(GHOST_OPERATORS))
def test_gate_reports_every_ghost_operator_as_ghost_not_as_a_field(g, op):
    pc = _pc()
    wl = ({"aaa1"}, "MATRIX", {"aaa1": "MATRIX"}, [])
    item = g.check_one(f"{op}(aaa1, 22)", wl, "D1", list(pc["poison_patterns"]), pc)
    assert any(i.startswith("[GHOST]") and op in i for i in item["issues"]), item["issues"]
    assert not any(i.startswith("[FIELD]") and op in i for i in item["issues"]), \
        f"{op} 被当成「未验证字段」报（应报幽灵算子）: {item['issues']}"


def test_ts_event_family_is_not_a_known_operator():
    """ts_event_*：平台不存在。known_ops 不得收录；SOP 不得再当作可用算子推荐（文档守护另见机检）。"""
    pc = _pc()
    assert not [o for o in pc["known_ops"] if o.startswith("ts_event_")]
    text = (REPO / "tracking" / "KOR" / "TOOLKIT_CHECKLIST.md").read_text(encoding="utf-8")
    assert "ts_event_" in text and "不存在" in text        # 证据仍在仓库里


def test_gate8_no_longer_demands_a_nonexistent_operator(g):
    ft = {"evt1": "EVENT", "mat1": "MATRIX"}
    issues = g.check_sanity_event_type(None, "D1", ["rank(ts_mean(evt1, 22))", "rank(mat1)"], ft)
    assert len(issues) == 1 and "evt1" in issues[0]
    assert "勿去找 ts_event_*" in issues[0] and "先 1 条探针" in issues[0]
    # 旧口径下“用了 ts_event_*”会放行；现在 ts_event_* 不是合法出路——引用 EVENT 字段一律拦
    assert g.check_sanity_event_type(None, "D1", ["ts_event_mean(evt1, 22)"], ft)
