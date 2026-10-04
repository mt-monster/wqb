# -*- coding: utf-8 -*-
"""s0-select 的「未测」口径 = backtest_results ∪ expressions（2026-10-04）。

此前 `hist_backtested` 只来自 `backtest_results`：GEM 生成 / 选波已落库、但还没关联回测的数据集会被当成「处女地」，
白名单三重交集（S0 tier ∩ 非 dead_end ∩ 未测）里的「未测」就漏判。`_expr_counts_by_dataset` 是只读、
region 作用域的辅助查询，s0-select 用它给这类集打「已有表达式 N 条未回测:非处女地」。

守两件事：按数据集计数；区域隔离（别区的表达式不算本区）。
"""
import importlib.util
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
for _p in (REPO, os.path.join(REPO, "src")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from wqb.store import CampaignStore  # noqa: E402


def _load():
    spec = importlib.util.spec_from_file_location(
        "campaign_intel_untested", os.path.join(REPO, "tools", "campaign_intel.py"))
    m = importlib.util.module_from_spec(spec)
    sys.modules["campaign_intel_untested"] = m
    spec.loader.exec_module(m)
    return m


@pytest.fixture
def cur(tmp_path):
    db = str(tmp_path / "wqb.db")
    st = CampaignStore(db)
    try:
        st.upsert_expressions("TST", "w1", ["rank(a1)", "rank(a2)"], dataset="ds_a", status="gem")
        st.upsert_expressions("TST", "w2", ["rank(b1)"], dataset="ds_b", status="gem")
        st.upsert_expressions("OTH", "w1", ["rank(other_region)"], dataset="ds_a", status="gem")
        st.upsert_expressions("OTH", "w2", ["rank(c1)"], dataset="ds_c", status="gem")
        cur = st.connection.cursor()
        yield cur
    finally:
        st.close()


def test_counts_expressions_per_dataset_in_the_region(cur):
    ci = _load()
    assert ci._expr_counts_by_dataset(cur, "TST") == {"ds_a": 2, "ds_b": 1}


def test_other_regions_expressions_do_not_count(cur):
    ci = _load()
    assert ci._expr_counts_by_dataset(cur, "OTH") == {"ds_a": 1, "ds_c": 1}
    assert "ds_c" not in ci._expr_counts_by_dataset(cur, "TST")     # ds_c 只在 OTH，不会漏进 TST


def test_empty_region_gives_empty_map(cur):
    ci = _load()
    assert ci._expr_counts_by_dataset(cur, "NONE") == {}
