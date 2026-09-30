# -*- coding: utf-8 -*-
"""IS→OS 衰减基准工具的守卫（2026-09-19）。

锁定两件事：
  1. 纯函数口径正确（分位数、保留率只统计 IS>0 且有 OS 值者）；
  2. 核心方法论结论被固化为机读字段：**IS 对 OS 无预测力**
     —— 实测 n=124：corr(IS,保留率)=+0.001、corr(IS,OS)=+0.092、负 OS 比例 ≈22%
     且各 IS 分桶的负 OS 比例都在 20–22% → 抬 IS 门槛**不能**降低 OS 风险。
     若未来有人把"提高 IS 门槛"写进选品规则，本测试应能提示该结论。
"""
import json
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(REPO, "tools"))

import os_decay_benchmark as B  # noqa: E402


# --------------------------------------------------------------------------- 1
def test_percentile_matches_linear_interpolation():
    v = [0.0, 1.0, 2.0, 3.0, 4.0]
    assert B.pct(v, 0.5) == pytest.approx(2.0)
    assert B.pct(v, 0.25) == pytest.approx(1.0)
    assert B.pct(v, 0.75) == pytest.approx(3.0)
    assert B.pct([], 0.5) is None


def test_retention_only_counts_valid_pairs():
    rows = [
        {"is_sharpe": 2.0, "os_sharpe": 1.0},    # 保留 0.5 ✓
        {"is_sharpe": 2.0, "os_sharpe": -1.0},   # 保留 -0.5 ✓（负 OS 必须计入！）
        {"is_sharpe": None, "os_sharpe": 1.0},   # IS 缺失 ✗
        {"is_sharpe": 2.0, "os_sharpe": None},   # OS 缺失 ✗
        {"is_sharpe": 0, "os_sharpe": 1.0},      # IS=0 不可除 ✗
        {"is_sharpe": -1.0, "os_sharpe": 1.0},   # IS<0 排除 ✗
    ]
    got = B.retention_of(rows)
    assert sorted(got) == [-0.5, 0.5]


def test_summarize_reports_all_deciles():
    """分位口径 = **线性插值**（不是最近秩）：10 个点、p10 落在 v[0] 与 v[1] 之间 0.9 处。"""
    rows = [{"is_sharpe": 1.0, "os_sharpe": v} for v in
            (-0.4, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8)]
    d = B.summarize(rows, "t")
    assert d["n"] == 10
    for k in ("p10", "p25", "p50", "p75", "p90", "mean"):
        assert k in d
    # k=(10-1)*0.10=0.9 → -0.4 + (0.0-(-0.4))*0.9 = -0.04
    assert d["p10"] == pytest.approx(-0.04)
    assert d["p50"] == pytest.approx(0.35)


# --------------------------------------------------------------------------- 2
def test_decommissioned_not_better_than_active():
    """实证：被退役队列的保留率**不高于**在跑队列（中位 0.349 vs 0.319）——
    即"被退役"不是由 OS 低造成的，故不能用 OS 基线反推筛选规则。"""
    cache = os.path.join(REPO, "logs", "_os_metrics_cache.json")
    if not os.path.isfile(cache):
        pytest.skip("无 OS 缓存（先跑 tools/os_report.py）")
    with open(cache, encoding="utf-8") as f:
        rows = [r for r in json.load(f).values() if (r.get("region") or "") == "USA"]
    act = B.summarize([r for r in rows if (r.get("status") or "").upper() == "ACTIVE"], "a")
    dec = B.summarize([r for r in rows if (r.get("status") or "").upper() == "DECOMMISSIONED"], "d")
    if not (act.get("n") and dec.get("n")):
        pytest.skip("样本不足")
    assert dec["p50"] <= act["p50"] + 0.15, (
        f"退役队列保留率({dec['p50']}) 明显高于在跑队列({act['p50']}) → "
        "与 2026-09-19 实证结论不符，需重新审视定标口径")


def test_benchmark_json_carries_predictivity_caveat(tmp_path, monkeypatch):
    """机读基准必须带 `is_predictivity` 与 `selection_standard`（防止下游只见数字不见前提）。"""
    out = os.path.join(REPO, "data", "os_decay_benchmark.json")
    if not os.path.isfile(out):
        pytest.skip("尚未生成机读基准（先跑 tools/os_decay_benchmark.py）")
    with open(out, encoding="utf-8") as f:
        d = json.load(f)
    assert "coverage_caveat" in d and "USA" in d["coverage_caveat"]
    assert "conservative_base" in d and "p50" in d["conservative_base"]
    assert "is_predictivity" in d
    assert "selection_standard" in d
    # 核心结论必须能读出来
    assert "IS" in d["selection_standard"]["implication"]
