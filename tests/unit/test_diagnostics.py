# -*- coding: utf-8 -*-
"""test_diagnostics.py — 论坛实证预检（ProdCorr 下限 / 过拟合四信号 / 相关性剪枝）。"""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "src"))

from wqb.diagnostics import (  # noqa: E402
    OVERFIT_THRESHOLDS,
    PROD_CORR_LIMIT,
    iter_prune,
    overfit_signals,
    prod_corr_lower_bound,
    should_skip_prod_check,
)


# ---------------- ProdCorr 下限（传递不等式） ----------------

def test_lower_bound_identity():
    """y=1 且 know_corr=k → 下限 = k（完全同源则相关相同）。"""
    assert prod_corr_lower_bound(1.0, 0.65) == pytest.approx(0.65)


def test_lower_bound_orthogonal():
    """y=0（与已知 alpha 正交）→ 下限 = -√(1-k²)，无信息。"""
    lb = prod_corr_lower_bound(0.0, 0.8)
    assert lb == pytest.approx(-0.6)  # -sqrt(1-0.64)


def test_lower_bound_monotonic_in_y():
    """y 越大（越像那个高相关 alpha），下限越高。"""
    lbs = [prod_corr_lower_bound(y, 0.85) for y in (0.3, 0.6, 0.9)]
    assert lbs == sorted(lbs)
    assert lbs[0] < lbs[-1]


def test_should_skip_true_and_false():
    """下限是**保守**估计：需极高的 y 才会超限。

    y=0.95/k=0.85 → 下限 0.643（未超限，仍值得实测）；
    y=0.99/k=0.90 → 下限 ≈0.83（超限，直接放弃查相关）。
    """
    assert should_skip_prod_check(0.95, 0.85) is False
    assert prod_corr_lower_bound(0.95, 0.85) == pytest.approx(0.643, abs=1e-3)
    assert should_skip_prod_check(0.99, 0.90) is True
    assert should_skip_prod_check(0.1, 0.85) is False


def test_should_skip_none_on_missing():
    assert should_skip_prod_check(None, 0.8) is None
    assert should_skip_prod_check(0.5, None) is None


def test_lower_bound_clamps_out_of_range():
    """入参超 [-1,1] 被裁剪，不抛异常。"""
    assert prod_corr_lower_bound(5.0, 0.7) is not None


# ---------------- 过拟合四信号 ----------------

def test_overfit_clean_passes():
    res = overfit_signals(yearly_sharpe=[1.5, 1.4, 1.6, 1.45],
                          decay_sharpe={0: 1.8, 5: 1.7},
                          yearly_corr=[0.3, 0.32, 0.31],
                          sharpe_full=1.8, sharpe_trimmed=1.6)
    assert res["verdict"] == "PASS" and res["n_signals"] == 0


def test_overfit_decay_cliff():
    """decay=5 时 1.8→0.8（比值 0.44）→ 命中。"""
    res = overfit_signals(decay_sharpe={0: 1.8, 5: 0.8})
    assert "decay_cliff" in res["hits"] and res["verdict"] == "REJECT"


def test_overfit_yearly_variance():
    res = overfit_signals(yearly_sharpe=[3.0, -0.5, 2.8, -0.3])
    assert "yearly_sharpe_var" in res["hits"]


def test_overfit_tail_trim():
    res = overfit_signals(sharpe_full=2.0, sharpe_trimmed=0.8)
    assert "tail_trim_halved" in res["hits"]


def test_overfit_yearly_corr_jump():
    """相邻两年 corr 从 0.2 跳到 0.8（跳变 0.6>0.4）→ 命中。"""
    res = overfit_signals(yearly_corr=[0.2, 0.8, 0.25])
    assert "yearly_corr_jump" in res["hits"]


def test_overfit_needs_three_years_for_variance():
    """样本 <3 年不判方差（避免误判）。"""
    assert overfit_signals(yearly_sharpe=[3.0, -2.0])["n_signals"] == 0


def test_overfit_thresholds_overridable():
    res = overfit_signals(decay_sharpe={0: 1.8, 5: 0.8},
                          thresh={"decay_cliff_ratio": 0.3})
    assert res["n_signals"] == 0  # 阈值放宽后不再命中
    assert res["thresholds"]["decay_cliff_ratio"] == 0.3


def test_overfit_defaults_unchanged():
    assert OVERFIT_THRESHOLDS["yearly_corr_jump_max"] == 0.4
    assert PROD_CORR_LIMIT == 0.7


# ---------------- 相关性剪枝 ----------------

def test_iter_prune_removes_high_corr():
    alphas = [{"id": "a", "sharpe": 1.8}, {"id": "b", "sharpe": 1.7},
              {"id": "c", "sharpe": 1.2}]
    corr = {("a", "b"): 0.95, ("a", "c"): 0.1, ("b", "c"): 0.05}

    def fn(x, y):
        return corr.get((x["id"], y["id"]), corr.get((y["id"], x["id"]), 0.0))

    kept = [a["id"] for a in iter_prune(alphas, fn)]
    assert kept == ["a", "c"]  # b 与 a 高相关被剪


def test_iter_prune_empty():
    assert list(iter_prune([], lambda a, b: 0.0)) == []
