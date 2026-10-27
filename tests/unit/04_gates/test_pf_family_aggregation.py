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


# ---------------------------------------------------------------------------
# 2026-10-24 P0-1：开波前 prod 探针封族（report §10）
#   `campaign_intel.py prod-probe` 写 `{"probe": true, "prod_corr": …}` 指纹；
#   闸 PF 读到 probe 标记且族 max ≥ PROBE_SEAL_THRESHOLD(0.75) 且 min ≥ 0.7
#   ⇒ 免 min_confidence_n 直接 enforced。无 probe 标记（prod-first 指纹）行为不变。
# ---------------------------------------------------------------------------
import json  # noqa: E402
import sqlite3  # noqa: E402

from wave_gate_pkg.gates_pf import PROBE_SEAL_THRESHOLD  # noqa: E402


@pytest.fixture
def add_fingerprint(tmp_path, monkeypatch, fake_store):
    """把 _wqb_root 指到 tmp，返回向 ledger_kv 写 prod_family_* 指纹的函数。"""
    (tmp_path / "data").mkdir()
    db = tmp_path / "data" / "wqb.db"
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE ledger_kv (id INTEGER PRIMARY KEY AUTOINCREMENT, region TEXT NOT NULL, "
              "key TEXT NOT NULL, value JSON NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
              "updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UNIQUE(region, key))")
    c.commit()
    c.close()
    monkeypatch.setattr(wave_gate, "_wqb_root", lambda *a, **k: str(tmp_path))

    def _add(family, payload):
        cc = sqlite3.connect(db)
        cc.execute("INSERT INTO ledger_kv(region, key, value) VALUES(?,?,?)",
                   ("TESTREG", f"prod_family_TESTREG_{family}", json.dumps(payload)))
        cc.commit()
        cc.close()

    return _add


def test_probe_seal_enforced_below_min_confidence_n(add_fingerprint):
    """probe=true + prod 0.76（仅 1 条）⇒ 免 n≥3 直接 enforced（判定性证据不等攒样本）。"""
    add_fingerprint("rank→ts_mean", {"prod_corr": 0.76, "probe": True,
                                     "at": "2026-10-24T01:02:03", "sealed": True})
    rep = wave_gate.check_prod_family_gate(
        ["rank(ts_mean(new_field, 22))"], "TESTREG", "ds")
    assert rep["status"] == "enforced"
    assert rep["passed"] is False
    assert rep["n_probe_sealed_families"] == 1
    assert rep["n_low_conf_dead_families"] == 0          # 封族与低置信度互斥计数
    assert "开波前 prod 探针封族" in rep["violations"][0]["reason"]
    assert "2026-10-24T01:02:03" in rep["violations"][0]["reason"]
    assert rep["probe_sealed_families_sample"] == ["rank→ts_mean"]


def test_probe_below_threshold_is_only_low_conf_warn(add_fingerprint):
    """0.72 ∈ [0.7, 0.75)：探针未达封族线 ⇒ 仍按低置信度 WARN（不误封整族）。"""
    assert 0.72 < PROBE_SEAL_THRESHOLD
    add_fingerprint("rank→ts_mean", {"prod_corr": 0.72, "probe": True, "sealed": False})
    rep = wave_gate.check_prod_family_gate(
        ["rank(ts_mean(new_field, 22))"], "TESTREG", "ds")
    assert rep["passed"] is True
    assert rep["status"] == "warn"
    assert rep["n_probe_sealed_families"] == 0
    assert rep["n_low_conf_dead_families"] == 1
    assert rep["expr_status"][0]["verdict"] == "WARN_LOW_CONF"


def test_probe_seal_respects_clean_counterexample(add_fingerprint, fake_store):
    """族内还有 <0.7 的干净反例（min<0.7）⇒ 不算封族，走既有 MIXED 加深路径。

    候选刻意用 3 算子形态：2 算子候选加深后指纹不变（rank→ts_mean），会被干净行
    直接判成 OK_DEEP；要覆盖「加深后仍无证据」的 WARN_MIXED 分支，第 3 个算子必须
    使它落到一个没有记录的更细指纹上。
    """
    add_fingerprint("rank→ts_mean", {"prod_corr": 0.78, "probe": True, "sealed": True})
    fake_store.rows = [
        _FakeRow(expression="rank(ts_mean(clean_field, 22))", prod_correlation=0.45),
    ]
    rep = wave_gate.check_prod_family_gate(
        ["rank(ts_mean(ts_backfill(new_field, 66), 22))"], "TESTREG", "ds")
    assert rep["passed"] is True                          # 「全族皆墙」纪律仍生效
    assert rep["n_probe_sealed_families"] == 0
    assert rep["n_mixed_families"] == 1
    assert rep["expr_status"][0]["verdict"] == "WARN_MIXED"


def test_fingerprint_without_probe_marker_keeps_old_behavior(add_fingerprint):
    """prod-first 指纹不带 probe ⇒ 行为不变（n=1 只 WARN，证明 marker 是承重件）。"""
    add_fingerprint("rank→ts_mean", {"prod_corr": 0.78})
    rep = wave_gate.check_prod_family_gate(
        ["rank(ts_mean(new_field, 22))"], "TESTREG", "ds")
    assert rep["passed"] is True
    assert rep["n_probe_sealed_families"] == 0
    assert rep["expr_status"][0]["verdict"] == "WARN_LOW_CONF"


def test_wave_gate_pf_is_single_authority():
    """闸 PF 只有一份实现：CLI 必须绑定包内实现（2026-10-24 去重守护）。

    历史事故：2026-09-30 包化后 `tools/wave_gate.py` 仍留着一份旧拷贝，且其
    `_load_prod_wall_families` 引用未定义全局 `wqb_root`（NameError 被
    `except Exception: pass` 静默吞掉）⇒ `campaign_intel prod-first/prod-probe`
    回写的 ledger 骨架指纹**从未被 CLI 读到**（闸 PF 只看 alphas 表，prod 覆盖率 4.4%）。
    两份实现并存时，改包内那份等于没改 —— 所以这里钉死「同一个函数对象」。
    """
    import inspect

    from wave_gate_pkg import gates_pf

    assert wave_gate.check_prod_family_gate is gates_pf.check_prod_family_gate
    assert wave_gate._load_prod_wall_families is gates_pf._load_prod_wall_families
    assert inspect.getsourcefile(wave_gate.check_prod_family_gate) == \
        inspect.getsourcefile(gates_pf.check_prod_family_gate)
    assert wave_gate.PROBE_SEAL_THRESHOLD == gates_pf.PROBE_SEAL_THRESHOLD

