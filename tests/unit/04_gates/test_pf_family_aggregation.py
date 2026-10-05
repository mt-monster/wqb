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


# ---- 2026-10-01 P1：unknown_mode（新骨架 enforce 档）----

def test_unknown_mode_default_warn_keeps_history(fake_store):
    """缺省 unknown_mode=warn：新骨架只 WARN、不拦波（与历史逐字一致）。"""
    fake_store.rows = [_FakeRow(expression="rank(ts_mean(x, 5))", prod_correlation=0.3)]
    rep = wave_gate.check_prod_family_gate(
        ["ts_delta(divide(a, b), 22)"], "TESTREG", "ds")   # ts_delta→divide 新骨架
    assert rep["unknown_mode"] == "warn"
    assert rep["status"] == "warn"
    assert rep["passed"] is True
    assert rep["violations"] == []


def test_unknown_mode_enforce_blocks_new_family(fake_store):
    """unknown_mode=enforce：新骨架（无 prod 记录）→ 计入 violations、status=enforced、passed=False。"""
    fake_store.rows = [_FakeRow(expression="rank(ts_mean(x, 5))", prod_correlation=0.3)]
    rep = wave_gate.check_prod_family_gate(
        ["ts_delta(divide(a, b), 22)"], "TESTREG", "ds", unknown_mode="enforce")
    assert rep["unknown_mode"] == "enforce"
    assert rep["status"] == "enforced"
    assert rep["passed"] is False
    assert rep["violations"] and rep["violations"][0]["family"] == "ts_delta→divide"
    assert "未探明" in rep["violations"][0]["reason"]


def test_unknown_mode_enforce_does_not_touch_clean_family(fake_store):
    """unknown_mode=enforce 不误伤已探明干净族（有 prod<0.7 记录）→ 仍 pass。"""
    fake_store.rows = [
        _FakeRow(expression="rank(ts_mean(x, 5))", prod_correlation=0.4),
        _FakeRow(expression="rank(ts_mean(y, 5))", prod_correlation=0.5),
        _FakeRow(expression="rank(ts_mean(z, 5))", prod_correlation=0.3),
    ]
    rep = wave_gate.check_prod_family_gate(
        ["rank(ts_mean(new_field, 10))"], "TESTREG", "ds", unknown_mode="enforce")
    assert rep["status"] == "pass"
    assert rep["passed"] is True
    assert rep["violations"] == []


def test_unknown_mode_enforce_dead_family_message_stays_dead(fake_store):
    """unknown_mode=enforce 下若同时有死路族，violations 仍以死路为准（reason 含 prod_corr 死路）。"""
    fake_store.rows = [
        _FakeRow(expression=f"signed_power(subtract(a{i}, b{i}), 2)", prod_correlation=0.8 + i * 0.01)
        for i in range(3)
    ]
    rep = wave_gate.check_prod_family_gate(
        ["signed_power(subtract(new_a, new_b), 2)"], "TESTREG", "ds", unknown_mode="enforce")
    assert rep["status"] == "enforced"
    assert any("死路" in v["reason"] for v in rep["violations"])
