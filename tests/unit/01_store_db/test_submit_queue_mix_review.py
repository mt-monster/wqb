# -*- coding: utf-8 -*-
"""混腿审查（`submit_queue.mix_review` / `is_add_mix` / `is_pass`）的口径守护。

历史：2026-09-13「路线 A」把"禁止加腿凑指标"写成**语法判定**（只拦 ≥2 条系数腿），
2026-11-08 审计发现四层闸只有一层查、且被绕过，禁令后泄漏率 15%（26/173）。
同日查官方文档后改口径 —— **官方禁的是「无经济含义的拼接」，不是 add 本身**：

  Consultant Dos and Don'ts（2026-09-18）:
    "DO NOT add an existing Alpha from one data source to enhance the signal from another
     data source **without any strong economic sense**"

因此本文件锁三条：
1. **结构硬拦**只针对「答不出经济含义」的形态：≥2 系数腿（权重网格）/ ≥4 腿（同源堆叠）；
2. **2–3 腿**属官方允许的跨源组合，靠「三问」（holders / polarity / prior）把关；
3. **三问的强制点是提交节点**，不是入队 —— 入队默认不拦，否则几百颗存量候选会被
   一次性判 DEAD（DEAD 粘性、不可申诉）。
"""
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
for _p in (REPO_ROOT / "src",):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.store import submit_queue as sq  # noqa: E402


NARR = {
    "holders": "主腿看异常成交额（注意力/散户），次腿看借券规模（空头需求）",
    "polarity": "两腿同号看多：成交额异常为正、借券下降已 reverse 成正",
    "prior": "2:1 配比在回测前由「主腿主导、借券只做确认」的逻辑钉死",
}

#: 今天实际提交过的 4 颗 + 11-07 的 bl6AvMkN（真·跨数据集 2 腿）
REAL_TWO_LEG = {
    "zq3eb7No": "group_rank(add(ts_zscore(est_12m_ebt_mean, 240), "
                "ts_zscore(subtract(est_12m_pre_mean, est_12m_pre_mean_4wks_ago), 66)), sector)",
    "3qoGxkqZ": "add(group_rank(ts_zscore(pv103_ivam_sum, 66), sector), "
                "reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main), 504), industry)))",
    "RRE5Mwkn": "add(multiply(2, group_rank(ts_target_tvr_decay(ts_zscore(pv103_ivam_sum, 252), "
                "target_tvr=0.15), sector)), reverse(group_rank(ts_zscore("
                "vec_sum(loaned_share_count_main), 504), sector)))",
    "bl6KwjwK": "add(multiply(2, group_rank(ts_zscore(subtract("
                "analyst_upward_revision_count_fy1_revenue_7d_4, "
                "analyst_downward_revision_count_fq1_revenue_7d_5), 66), sector)), "
                "reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main), 504), sector)))",
    "bl6AvMkN": "group_neutralize(add(rank(ts_mean(eps_y1_estimate_change_3mo, 66)), "
                "rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), "
                "bucket(rank(ts_mean(predicted_surprise_f12m_ebitda_4, 66)), range=\"0,1,0.1\"))",
}

WEIGHT_GRID = [
    "add(multiply(0.4, rank(a)), multiply(0.6, rank(b)))",          # multiply 前缀
    "add(multiply(rank(a), 0.4), multiply(rank(b), 0.6))",          # multiply 后缀
    "quantile(add(0.7*rank(a), 0.3*zscore(b)))",                     # 星号中缀
    "add(0.5*rank(a), subtract(0, rank(b)), -0.2*rank(c))",          # 含镜像腿
]

STACKS = [
    "add(rank(a), rank(b), rank(c), rank(d))",                       # 平铺 4 腿
    "add(rank(a), add(rank(b), add(rank(c), rank(d))))",             # 嵌套 4 腿
]


# ---------------- 分级 ----------------

@pytest.mark.parametrize("expr", WEIGHT_GRID)
def test_weight_grid_is_hard_blocked(expr):
    """≥2 条系数腿 = 权重网格：数字本身是搜索自由度，官方红线。"""
    mr = sq.mix_review(expr)
    assert mr["kind"] == "weight_grid"
    assert mr["blocked"] is True
    assert mr["coef_legs"] >= 2
    assert "权重网格" in mr["block_reason"] or "毒模式" in mr["block_reason"]


@pytest.mark.parametrize("expr", STACKS)
def test_four_legs_is_hard_blocked(expr):
    """展平 ≥4 条信号腿 = 同源堆叠：无法逐个说清信息持有者。"""
    mr = sq.mix_review(expr)
    assert mr["kind"] == "stack"
    assert mr["blocked"] is True
    assert mr["legs"] == 4


@pytest.mark.parametrize("aid,expr", list(REAL_TWO_LEG.items()))
def test_real_cross_dataset_two_legs_need_narrative_not_blocked(aid, expr):
    """今天实际提交的 5 颗：2 腿 ⇒ **不硬拦**，但必须答三问（旧口径会把等权两颗放过、单系数两颗分类不明）。"""
    mr = sq.mix_review(expr)
    assert mr["kind"] == "two_leg", f"{aid} 腿数判错：{mr}"
    assert mr["legs"] == 2
    assert mr["blocked"] is False, f"{aid} 不该被结构硬拦（官方允许有经济含义的跨源组合）"
    assert mr["narrative_required"] is True
    assert mr["narrative_ok"] is False, "没给三问时应判未答"
    assert mr["narrative_missing"] == ["holders", "polarity", "prior"]

    mr2 = sq.mix_review(expr, NARR)
    assert mr2["narrative_ok"] is True
    assert mr2["narrative_missing"] == []


def test_three_legs_is_allowed_but_requires_narrative():
    mr = sq.mix_review("add(rank(a), rank(b), reverse(rank(c)))")
    assert (mr["kind"], mr["legs"], mr["blocked"]) == ("three_leg", 3, False)
    assert mr["narrative_required"] is True


def test_single_leg_forms_have_no_narrative_burden():
    """单腿形态（含 subtract 反转、单腿+常数）既不硬拦、也不要三问。"""
    for expr in (
        "subtract(0.5, group_rank(ts_mean(vec_stddev(insd5_vol_chg), 55), sector))",
        "rank(ts_mean(x, 5))",
        "add(multiply(-1, x), 1)",
    ):
        mr = sq.mix_review(expr)
        assert mr["blocked"] is False, expr
        assert mr["narrative_required"] is False, expr


def test_empty_expression_is_not_blocked():
    assert sq.mix_review(None)["blocked"] is False
    assert sq.mix_review("")["kind"] == "none"
    assert sq.is_add_mix(None) is False


# ---------------- 三问质量 ----------------

def test_placeholder_answers_count_as_missing():
    """三问的价值在内容：'ok'/'yes'/'n/a' 这类敷衍答案必须判未答。"""
    assert sq.missing_mix_narrative({"holders": "ok", "polarity": "yes", "prior": "n/a"}) == [
        "holders", "polarity", "prior"]
    assert sq.missing_mix_narrative(None) == ["holders", "polarity", "prior"]
    assert sq.missing_mix_narrative({}) == ["holders", "polarity", "prior"]


def test_partial_answers_report_only_missing_keys():
    partial = {"holders": NARR["holders"]}
    assert sq.missing_mix_narrative(partial) == ["polarity", "prior"]
    mr = sq.mix_review(REAL_TWO_LEG["3qoGxkqZ"], partial)
    assert mr["narrative_ok"] is False
    assert mr["narrative_missing"] == ["polarity", "prior"]


def test_narrative_accepts_json_string():
    """MCP 的 workflow_execute(params=...) 会原样透传字符串，必须能吃。"""
    assert sq.missing_mix_narrative(json.dumps(NARR)) == []
    assert sq.mix_review(REAL_TWO_LEG["3qoGxkqZ"], json.dumps(NARR))["narrative_ok"] is True


# ---------------- is_add_mix 的分层 ----------------

def test_hard_block_ignores_narrative():
    """结构硬拦：给齐三问也不放行（官方禁的是这一类，三问答不出来）。"""
    for expr in WEIGHT_GRID + STACKS:
        assert sq.is_add_mix(expr) is True
        assert sq.is_add_mix(expr, NARR, require_narrative=True) is True


def test_narrative_enforced_only_when_required():
    """默认（入队）不因「还没写三问」判死；提交节点显式打开开关才拦。"""
    expr = REAL_TWO_LEG["3qoGxkqZ"]
    assert sq.is_add_mix(expr) is False                      # 入队：放行
    assert sq.is_add_mix(expr, None, require_narrative=True) is True   # 提交：拦
    assert sq.is_add_mix(expr, NARR, require_narrative=True) is False  # 提交 + 三问：放行


def test_is_pass_keeps_add_mix_prefix_for_weight_grid():
    """`FAIL:ADD_MIX` 前缀被 tools/submit_queue.py 的 startswith 消费，不能改。"""
    ok, why = sq.is_pass(3.0, 2.0, 2.5, 0.2, 0.5, 0.3, [], WEIGHT_GRID[0])
    assert (ok, why) == (False, "ADD_MIX")
    gate, st = sq.gate_of(3.0, 2.0, 2.5, 0.2, 0.5, 0.3, [], WEIGHT_GRID[0])
    assert (gate, st) == ("FAIL:ADD_MIX", sq.STATUS_DEAD)


def test_is_pass_reports_stack_separately():
    ok, why = sq.is_pass(3.0, 2.0, 2.5, 0.2, 0.5, 0.3, [], STACKS[0])
    assert (ok, why) == (False, "ADD_MIX:STACK")


def test_is_pass_narrative_gate_is_opt_in():
    """同一条 2 腿表达式：入队放行，提交层（require_mix_narrative）拦。"""
    expr = REAL_TWO_LEG["zq3eb7No"]
    ok, why = sq.is_pass(2.01, 1.28, 1.64, 0.15, 0.61, 0.36, [], expr)
    assert (ok, why) == (True, "")
    ok, why = sq.is_pass(2.01, 1.28, 1.64, 0.15, 0.61, 0.36, [], expr,
                         require_mix_narrative=True)
    assert (ok, why) == (False, "MIX_NARRATIVE:holders,polarity,prior")
    ok, why = sq.is_pass(2.01, 1.28, 1.64, 0.15, 0.61, 0.36, [], expr,
                         mix_narrative=NARR, require_mix_narrative=True)
    assert (ok, why) == (True, "")
