# -*- coding: utf-8 -*-
"""tools/prod_first_screen.py 平台侧枚举（--from-file）的回归守护。

起因（2026-09-30 EUR 实测）：prod 清扫只按本地 alphas 表枚举，而本地镜像的
`two_year_sharpe`/`margin` 常缺同步 → 平台侧 12 条 S>=1.66/2Y>=1.69 从未测过的存量被筛成
"0 待测"，EUR 因此连跑 4 轮空清扫。本文件锁住新加的 four-layer 筛选：
区域 / 闸5 毒模式 / 族已撞墙自动排除 / 同族配给 + 表达式去重。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools"))

import prod_first_screen as pfs  # noqa: E402

# ------------------------------------------------------------------ 字段族提取


@pytest.mark.parametrize("code,expect", [
    # 表达式以算子开头时，族必须取第一个「字段」而非算子名
    ("(group_rank(ts_backfill(mdl39_d1_val_mo_industry_rank,60),sector) + 2) / 3", "mdl39_d1"),
    ("rank(add(vec_avg(financial_statement_volatility_factor), vec_avg(alpha_score)))",
     "financial_statement"),
    ("rank(group_neutralize(subtract(rank(ts_backfill(predicted_surprise_pct_f12m_earnings_5, 60)),"
     " rank(pcf_ratio)), industry))", "predicted_surprise"),
    ("group_rank(ts_zscore(ts_backfill(pe_ratio_relative_score_float,60),35),subindustry)",
     "pe_ratio"),
])
def test_field_family_skips_operator_tokens(code, expect):
    assert pfs.field_family(code) == expect


def test_known_ops_nonempty_single_source():
    """算子名单来自 toolkit platform_constraints.json（单一事实源），缺文件即空集→族提取会退化。"""
    ops = pfs.known_ops()
    assert {"rank", "group_rank", "vec_avg", "ts_backfill"} <= ops


# ------------------------------------------------------------------ 闸5 结构判定


@pytest.mark.parametrize("code", [
    "add(multiply(0.4, rank(a_field_x)), multiply(0.6, rank(b_field_y)))",
    "add(0.70 * add(0.65 * subtract(0, rank(long_term_free_cash_flow_to_price_2)),"
    " 0.35 * subtract(0, rank(short_term_trailing_free_cash_flow_to_price_2))), 0.3 * rank(c))",
    "ts_decay_linear(add(multiply(reverse(rank(ts_zscore(returns, 252))), 0.5),"
    " multiply(reverse(rank(ts_zscore(returns, 504))), 0.5)))",
])
def test_structural_weighted_mix_detected(code):
    assert pfs.structural_weighted_mix(code) is True


@pytest.mark.parametrize("code", [
    "rank(subtract(rank(a_field_x), rank(b_field_y)))",          # 等权价差几何：闸5 不拦
    "group_rank(ts_zscore(ts_backfill(pe_ratio_relative_score_float,60),35),subindustry)",
    "multiply(rank(a_field_x), 0.5)",                              # 单腿缩放
    "subtract(0, rank(long_term_free_cash_flow_to_price_2))",
])
def test_structural_weighted_mix_not_flagged_for_allowed_shapes(code):
    assert pfs.structural_weighted_mix(code) is False


# ------------------------------------------------------------------ 四层筛选


@pytest.fixture()
def fake_inventory(monkeypatch):
    """把族级 prod、「在库」判定与 RA 失败集换成可控替身（不碰真实 DB）。"""

    def _setup(walled: dict, in_table=(), ra_failed=()):
        monkeypatch.setattr(pfs, "prod_by_family", lambda region: dict(walled))
        monkeypatch.setattr(pfs, "already_in_table", lambda region: set(in_table))
        monkeypatch.setattr(pfs, "ra_failed_ids", lambda region="", db=None: set(ra_failed))

    return _setup


# ------------------------------------------------------------------ RA-clean 口径


@pytest.mark.parametrize("value,expect", [
    (None, False), ("", False), ("null", False), ("NULL", False), ("[]", False),
    ("none", False),
    ('["LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO"]', True),
    ('["LOW_ASI_JPN_SHARPE","LOW_SUB_UNIVERSE_SHARPE"]', True),
])
def test_ra_failed_value_only_counts_items(value, expect):
    """NULL/空/'null'/'[]' 按无失败计（与 get_mining_yield(strict) 同源）；有条目才算失败。"""
    assert pfs.ra_failed_value(value) is expect


def test_enumerate_skips_platform_ra_failed_rows(tmp_path, fake_inventory):
    """平台 RA 硬闸已失败的行不测 prod（不可提交，测了是烧单并发队列）。"""
    fake_inventory({}, ra_failed={"BAD1BAD1"})
    path = _write_cand(tmp_path, [
        _item("BAD1BAD1", "rank(ts_mean(pe_ratio_relative_score_float, 66))", s=3.44, f=4.01),
        _item("GOOD1111", "rank(ts_mean(dividend_yield_relative_score_float, 66))", s=2.0),
    ])
    rows, meta = pfs.enumerate_from_file(path, "EUR")
    assert [r["alpha_id"] for r in rows] == ["GOOD1111"]
    assert meta["skip_ra_failed"] == 1
    # 显式允许时坏行回到队列（--allow-ra-failed 语义）
    rows2, meta2 = pfs.enumerate_from_file(path, "EUR", allow_ra_failed=True)
    assert {r["alpha_id"] for r in rows2} == {"BAD1BAD1", "GOOD1111"}
    assert meta2["skip_ra_failed"] == 0


def _write_cand(tmp_path, items):
    p = tmp_path / "cand.json"
    p.write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")
    return str(p)


def _item(aid, code, region="EUR", s=2.0, f=1.2, ty=2.0):
    return {"id": aid, "region": region, "code": code, "sharpe": s, "fitness": f,
            "two_year_sharpe": ty, "universe": "TOP2500", "delay": 1, "neut": "SUBINDUSTRY"}


def test_enumerate_excludes_walled_family_and_other_region(tmp_path, fake_inventory):
    fake_inventory({"predicted_surprise": 0.9983})
    path = _write_cand(tmp_path, [
        _item("Aaaaaaaa", "rank(group_neutralize(subtract(rank(predicted_surprise_pct_f12m_e), "
                          "rank(pe_ratio_relative_score_float)), industry))"),
        _item("Bbbbbbbb", "group_rank(ts_zscore(ts_backfill(pe_ratio_relative_score_float,60),35),"
                          "subindustry)"),
        _item("Cccccccc", "rank(ts_mean(chart_pattern_quality_score_cn20, 66))", region="GLB"),
    ])
    rows, meta = pfs.enumerate_from_file(path, "EUR", family_cap=0)
    assert [r["alpha_id"] for r in rows] == ["Bbbbbbbb"]
    assert meta["skip_region"] == 1 and meta["skip_walled_family"] == 1


def test_enumerate_drops_poison_by_default(tmp_path, fake_inventory):
    fake_inventory({})
    path = _write_cand(tmp_path, [
        _item("Mix11111", "add(multiply(0.4, rank(a_field_x)), multiply(0.6, rank(b_field_y)))"),
        _item("Mix22222", "add(0.70 * add(0.65 * subtract(0, rank(long_term_free_cash_flow_a)),"
                          " 0.35 * subtract(0, rank(short_term_free_cash_flow_b))), 0.3 * rank(c))"),
        _item("Clean111", "subtract(0, rank(long_term_free_cash_flow_a))"),
    ])
    rows, meta = pfs.enumerate_from_file(path, "EUR")
    assert [r["alpha_id"] for r in rows] == ["Clean111"]
    assert meta["skip_poison"] == 2
    # 关掉毒模式后两条混腿会回到队列（--keep-poison 的语义）
    rows2, _ = pfs.enumerate_from_file(path, "EUR", drop_poison=False)
    assert {r["alpha_id"] for r in rows2} == {"Mix11111", "Mix22222", "Clean111"}


def test_enumerate_family_cap_and_dedup(tmp_path, fake_inventory):
    fake_inventory({})
    same = "group_rank(ts_zscore(ts_backfill(dividend_yield_relative_score_float,60),35),subindustry)"
    path = _write_cand(tmp_path, [
        _item("D1", "rank(ts_mean(pe_ratio_relative_score_float, 66))", s=2.5),
        _item("D2", "rank(ts_mean(pe_ratio_relative_score_float, 22))", s=2.4),
        _item("D3", "rank(ts_mean(pe_ratio_relative_score_float, 5))", s=2.3),
        _item("D4", same, s=1.9),
        _item("D5", same, s=1.8),          # 表达式完全相同 → 去重
    ])
    rows, meta = pfs.enumerate_from_file(path, "EUR", family_cap=2)
    assert [r["alpha_id"] for r in rows] == ["D1", "D2", "D4"]
    assert meta["skip_family_cap"] == 1 and meta["skip_dup"] == 1


def test_enumerate_skips_below_is_gate_unless_include_weak(tmp_path, fake_inventory):
    fake_inventory({})
    path = _write_cand(tmp_path, [
        _item("W1", "rank(ts_mean(pe_ratio_relative_score_float, 66))", s=1.5),
        _item("W2", "rank(ts_mean(dividend_yield_relative_score_float, 66))", s=2.0, f=0.9),
        _item("W3", "rank(ts_mean(pcf_ratio_relative_score_float, 66))", s=2.0, f=1.2),
    ])
    rows, _ = pfs.enumerate_from_file(path, "EUR")
    assert [r["alpha_id"] for r in rows] == ["W3"]
    rows_all, meta = pfs.enumerate_from_file(path, "EUR", include_weak=True)
    assert len(rows_all) == 3 and meta["skip_weak"] == 0


def test_enumerate_reports_in_alphas_flag_for_registration(tmp_path, fake_inventory):
    fake_inventory({}, in_table={"R1"})
    path = _write_cand(tmp_path, [
        _item("R1", "rank(ts_mean(pe_ratio_relative_score_float, 66))"),
        _item("R2", "rank(ts_mean(dividend_yield_relative_score_float, 66))"),
    ])
    rows, _ = pfs.enumerate_from_file(path, "EUR")
    assert {r["alpha_id"]: r["in_alphas"] for r in rows} == {"R1": True, "R2": False}
