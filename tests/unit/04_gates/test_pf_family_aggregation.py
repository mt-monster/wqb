# -*- coding: utf-8 -*-
"""闸 PF 同族聚合 max/min 双记（2026-09-28 修复守护）.

背景（评估报告 P1-1）：`_load_prod_wall_families` 此前同族只留 min(prod_corr)=最干净，
`check_prod_family_gate` 又以 min 判 ok/dead —— 族里只要有一条干净记录，撞墙证据就被吞：
GLB 实测 `group_zscore→ts_decay_linear` 37 条、max 0.9929 仍被判"干净"，
而代码注释写的是"取最严格的"。修复后：
  - `prod_corr`=min、`prod_max`=max、`n_wall`=≥0.7 记录数（双记）；
  - 全族皆墙（min≥0.7）且 n≥3 → enforced 拦截（原语义不变）；
  - 证据混合（max≥0.7>min）→ 单列 MIXED，不再算干净：走 3 算子粒度加深，
    加深后仍混合/无证据 → WARN 并建议 prod-first 探针；加深后确认全墙 → 拦截。
"""
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "tools"))

import wave_gate  # noqa: E402


class _FakeRow(dict):
    pass


class _FakeStore:
    rows = []

    def __init__(self, *args, **kwargs):
        pass

    def list_alphas_by_region(self, region):
        return list(self.rows)

    def close(self):
        pass


@pytest.fixture
def fake_store(monkeypatch):
    _FakeStore.rows = []
    monkeypatch.setattr(wave_gate, "_campaign_store_cls", lambda *a, **k: _FakeStore)
    monkeypatch.setattr(wave_gate, "_wqb_db_path", lambda *a, **k: "unused.db")
    return _FakeStore


def test_aggregation_records_min_max_and_wall_count(fake_store):
    """同族 3 条（0.45 / 0.99 / 0.60）：min=0.45、max=0.99、n_wall=1。"""
    fake_store.rows = [
        _FakeRow(expression="group_zscore(ts_decay_linear(x, 5), industry)", prod_correlation=0.45),
        _FakeRow(expression="group_zscore(ts_decay_linear(y, 66), country)", prod_correlation=0.99),
        _FakeRow(expression="group_zscore(ts_decay_linear(ts_zscore(z, 5), 5), industry)",
                 prod_correlation=0.60),
    ]
    fams = wave_gate._load_prod_wall_families("TESTREG")
    fam = "group_zscore→ts_decay_linear"
    assert fam in fams
    assert fams[fam]["prod_corr"] == pytest.approx(0.45)   # min
    assert fams[fam]["prod_max"] == pytest.approx(0.99)    # max（此前被吞掉）
    assert fams[fam]["n_wall"] == 1
    assert fams[fam]["n"] == 3


def test_mixed_family_is_not_clean_and_warns(fake_store):
    """证据混合族不得再判 OK：候选落在该族 → WARN_MIXED（passed=True 但 status=warn）。"""
    fake_store.rows = [
        _FakeRow(expression="group_zscore(ts_decay_linear(x, 5), industry)", prod_correlation=0.45),
        _FakeRow(expression="group_zscore(ts_decay_linear(y, 5), industry)", prod_correlation=0.95),
    ]
    rep = wave_gate.check_prod_family_gate(
        ["group_zscore(ts_decay_linear(new_field, 5), industry)"], "TESTREG", "ds")
    assert rep["n_mixed_families"] == 1
    assert rep["n_ok_families"] == 0
    assert rep["passed"] is True                 # 混合不误伤（不 enforced）
    assert rep["status"] == "warn"               # 但也不算干净
    st = rep["expr_status"][0]
    assert st["verdict"] in ("WARN_MIXED", "OK_DEEP", "DEAD")
    assert st["verdict"] != "OK"


def test_all_wall_family_still_enforced(fake_store):
    """全族皆墙（min≥0.7）且 n≥3 → 仍拦截（原语义不变）。"""
    fake_store.rows = [
        _FakeRow(expression=f"signed_power(subtract(a{i}, b{i}), 2)", prod_correlation=0.8 + i * 0.01)
        for i in range(3)
    ]
    rep = wave_gate.check_prod_family_gate(
        ["signed_power(subtract(new_a, new_b), 2)"], "TESTREG", "ds")
    assert rep["status"] == "enforced"
    assert rep["passed"] is False
    assert rep["violations"] and rep["violations"][0]["family"] == "signed_power→subtract"


def test_mixed_deepens_to_three_ops(fake_store):
    """混合族加深到 3 算子：加深后全墙 → 拦截；加深后干净 → OK_DEEP。"""
    # 2 算子族 group_zscore→ts_decay_linear 混合；3 算子粒度上
    # group_zscore→ts_decay_linear→ts_backfill 全墙（3 条 ≥0.7）
    fake_store.rows = [
        _FakeRow(expression="group_zscore(ts_decay_linear(ts_backfill(x, 66), 5), industry)",
                 prod_correlation=0.9),
        _FakeRow(expression="group_zscore(ts_decay_linear(ts_backfill(y, 66), 5), industry)",
                 prod_correlation=0.8),
        _FakeRow(expression="group_zscore(ts_decay_linear(ts_backfill(z, 66), 5), industry)",
                 prod_correlation=0.75),
        # 同 2 算子族的干净变体（不同 3 算子指纹）→ 造成 2 算子粒度混合
        _FakeRow(expression="group_zscore(ts_decay_linear(ts_zscore(w, 5), 5), industry)",
                 prod_correlation=0.30),
    ]
    rep = wave_gate.check_prod_family_gate(
        ["group_zscore(ts_decay_linear(ts_backfill(new1, 66), 5), industry)",
         "group_zscore(ts_decay_linear(ts_zscore(new2, 5), 5), industry)"],
        "TESTREG", "ds")
    by_idx = {s["index"]: s for s in rep["expr_status"]}
    assert by_idx[0]["verdict"] == "DEAD"        # 加深后全墙 → 拦截
    assert by_idx[1]["verdict"] == "OK_DEEP"     # 加深后干净 → 放行
    assert rep["passed"] is False
