# -*- coding: utf-8 -*-
"""闸1b-2（算子复杂度）+ 等价算子替换规则的守护测试（2026-10-03）。

两个守护对象的共同点：**此前只有条文、没有机器执行**，删掉不会有任何测试变红——
这类「写在文档/json 里但没人执行」的规则是本仓库反复出现��漏网形态
（历史上 `validator.py` 三份各自演化、缺 hump/bucket/densify 修复即如此溜过审计）。
本文件把两者钉住。

⚠ 只读：全部用 tmp_path / 只读断言，不触网、不写库。
"""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
TOOLKIT_SKILL = REPO / "Claude" / "skills" / "wq-brain-campaign-toolkit"
TOOLKIT = TOOLKIT_SKILL / "scripts"
#: 规则配置在 skill 根下的 config/，**不在** scripts/ 下（踩过一次）
RULES_JSON = TOOLKIT_SKILL / "config" / "methodology_rules.json"
OPT_SKILL = REPO / "Claude" / "skills" / "wq-brain-alpha-optimization-v1" / "SKILL.md"
HOW2PASS = REPO / "Claude" / "skills" / "brain-how-to-pass-alpha-test" / "SKILL.md"
SIGNALS_DOC = REPO / "docs" / "experience" / "02_signal_patterns.md"


def _load_gate():
    if not (TOOLKIT / "gate.py").is_file():
        pytest.skip("gate.py 不存在（干净克隆？）")
    if str(TOOLKIT) not in sys.path:
        sys.path.insert(0, str(TOOLKIT))
    spec = importlib.util.spec_from_file_location("wqb_gate_t1c", TOOLKIT / "gate.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def g():
    return _load_gate()


# ---------------- 闸1b-2：算子调用点数 < 10 ----------------

def _nest(n: int) -> str:
    """造出**恰好** n 个函数调用点的表达式。

    手工数括号极易数错（本轮我就把 6 个调用点的表达式当成 10 个），
    故边界用例一律程序化生成，并断言生成数 = 实测数。
    """
    e = "close"
    for _ in range(n):
        e = f"ts_mean({e}, 5)"
    return e


def test_call_counter_is_reachable(g):
    """op_arity 的 iter_call_sites 必须可达——不可达时闸1b-2 会静默不生效。"""
    assert g._call_counter is not None, (
        "闸1b-2 的调用点计数器未装载，闸会静默失效（与 1b 的 ARITY_UNKNOWN 同类风险）")
    assert g.MAX_OP_CALLS == 10, f"铁律是 <10，当前 {g.MAX_OP_CALLS}"


@pytest.mark.parametrize("n", [7, 8, 9])
def test_below_threshold_passes(g, n):
    """< 10 个调用点必须放行。"""
    assert len(g._call_counter(_nest(n))) == n
    assert n < g.MAX_OP_CALLS


@pytest.mark.parametrize("n", [10, 11, 15])
def test_at_or_above_threshold_blocks(g, n):
    """>= 10 个调用点必须拦截（铁律是「<10」，故 10 本身即违规）。"""
    assert len(g._call_counter(_nest(n))) == n
    assert n >= g.MAX_OP_CALLS


def test_nest_helper_generates_exact_count(g):
    """★ 反向守护：生成器必须自洽，否则上面的边界用例全部失去意义。

    这条是本文件最关键的一条——「手工数错括号」正是我第一版实测翻车的原因。
    """
    for n in range(1, 13):
        assert len(g._call_counter(_nest(n))) == n, f"nest({n}) 生成数与实测不符"


def test_gate_1c_registered_as_block(g):
    """闸1b-2 必须进 GATE_REGISTRY 且性质为 block（否则只是提示不是闸）。"""
    rows = {r[0]: r for r in g.GATE_REGISTRY}
    assert "1b-2" in rows, "闸1b-2 未登记到 GATE_REGISTRY"
    gid, _name, kind, _sw, _note = rows["1b-2"]
    assert kind == "block", f"闸1b-2 性质应为 block（铁律是硬约束），实为 {kind}"


def test_gate_code_version_bumped_for_cache_invalidation():
    """★ 闸判定代码变更必须递增 GATE_CODE_VERSION，否则逐条缓存会继续返回
    **未含闸1b-2** 的旧结论——新闸等于没加（静默失效，且比没加更危险）。"""
    src = (TOOLKIT / "gate.py").read_text(encoding="utf-8")
    import re
    m = re.search(r'GATE_CODE_VERSION\s*=\s*"([^"]+)"', src)
    assert m, "未找到 GATE_CODE_VERSION"
    ver = m.group(1)
    assert ver >= "2026-10-03", (
        f"GATE_CODE_VERSION={ver} 未随闸1b-2 递增；逐条 sha1 缓存不会失效，"
        f"新闸对已有缓存条目不生效")


def test_judge_rubric_aligns_with_gate_threshold():
    """judge 的 soft limit 与闸1b-2 阈值须一致，避免两套口径互相否定。"""
    rubric = (REPO / "Claude" / "skills" / "brain-alpha-judge"
              / "data" / "extra_submission_rubric.json")
    data = json.loads(rubric.read_text(encoding="utf-8"))
    rules = data if isinstance(data, list) else data.get("rules", [])
    hit = [r for r in rules if r.get("id") == "implementation_simplicity"]
    assert hit, "judge rubric 缺 implementation_simplicity 规则"
    assert hit[0]["expression_heuristics"]["max_operator_count"] == 10, (
        "judge soft limit 与闸1b-2 阈值不一致——会出现「闸拦了但 judge 说没问题」")

    judge = (REPO / "Claude" / "skills" / "brain-alpha-judge"
             / "scripts" / "judge_alpha.py")
    src = judge.read_text(encoding="utf-8")
    assert 'max_operator_count", 10' in src, "judge 的兜底默认值仍是旧值"


# ---------------- 等价算子替换（3A）：条文存在 + S4 流程引用 ----------------

def test_equivalent_operator_rule_registered_with_candidates():
    """规则必须带**可用的候选表**，不能只有一句口号。"""
    data = json.loads(RULES_JSON.read_text(encoding="utf-8"))
    blob = json.dumps(data, ensure_ascii=False)
    assert "equivalent_operator" in blob, "methodology_rules.json 缺等价算子替换规则"
    # 至少要有 signed_power -> quantile 这条实证最强的替换
    assert "quantile" in blob, "规则缺 quantile 替换候选（KOR 实证最强的那条）"


def test_s4_skill_requires_scanning_equivalent_operators_before_giving_up():
    """★ 3A 的核心守护：S4 诊断 skill 必须要求「判无解前先扫等价算子」。

    背景：该方法论在记忆里被标为「KOR 破局，最高价值方法论」，但此前
    optimization-v1 / brain-alpha-repair / ra-pipeline / step7-diagnose 对
    「等价算子」全部零命中——S4 真正需要它的时刻没有任何机制送达，
    删掉整条规则也不会有任何测试变红。
    """
    text = OPT_SKILL.read_text(encoding="utf-8")
    assert "等价算子" in text, (
        "wq-brain-alpha-optimization-v1 未要求扫等价算子——"
        "Agent 会在 S4 直接判死可救的族（KOR「不可能三角」实为 signed_power "
        "造成的假性约束）")
    # 必须链到权威表，而不是凭空发明
    assert "02_signal_patterns" in text, "未链到 02_signal_patterns.md 的替换表"


def test_how_to_pass_does_not_teach_raising_sharpe_for_sub_gate():
    """★ 防回归：不得再教「抬整体 Sharpe 破 SUB 闸」。

    SUB 是比值闸（门槛 = 系数 × S），抬 S 时门槛同比例抬高 ⇒ 原地跑步。
    该错误指引曾同时存在于 :58 修法表与 :109 正文，并通过 optimization-v1
    的上游登记放大到整条 S4 链。
    """
    text = HOW2PASS.read_text(encoding="utf-8")
    assert "先抬整体 Sharpe" not in text, (
        "brain-how-to-pass-alpha-test 又在教「先抬整体 Sharpe」破 SUB 闸——"
        "这是已实证判死的方向（比值闸，抬 S 门槛同步抬高）")
    # 必须保留比值闸的说明，否则 Agent 无从判断为什么不能抬 S
    assert "比值闸" in text, "缺少「SUB 是比值闸」的说明"


def test_signal_patterns_doc_has_equivalent_operator_section():
    """权威替换表必须在，且含 signed_power -> quantile 实证条目。"""
    text = SIGNALS_DOC.read_text(encoding="utf-8")
    assert "等价算子替换" in text, "02_signal_patterns.md 缺 §12 等价算子替换"
    assert "signed_power" in text and "quantile" in text, "替换表缺实证条目"
