# -*- coding: utf-8 -*-
"""2026-09-30 P1 守卫：s0-select 排序键不再把「跨区弱」计入降权。

背景（实测，见 tools/campaign_intel.py 调用处注释）：
  公平对照（≥2 区共有数据集子集 n=154，基线 yield>0 = 23%）——
    标跨区弱 → 24%（对照未标弱 23%，lift +1pp）
    标跨区强 → 22%（对照未标强 24%，lift −2pp）
  均在噪声内 ⇒ 该先验无预测力。而 soft 是排序第二键，会把 17%（8/48）的候选
  整体压到存活队尾，top-n 截断时被完全排除 ⇒ 纯系统性偏置，故移出排序键。

本测试锁死三件事：
  1. 默认：跨区弱不影响排序（只与 total_score 比较）
  2. --xr-penalize 可复现旧行为
  3. 真正有结构含义的两层（判死沉底 / 字段数不足次沉）不受影响
"""
import importlib.util
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def _load():
    spec = importlib.util.spec_from_file_location(
        "campaign_intel_p1", os.path.join(REPO, "tools", "campaign_intel.py"))
    m = importlib.util.module_from_spec(spec)
    sys.modules["campaign_intel_p1"] = m
    spec.loader.exec_module(m)
    return m


def _cand(**kw):
    base = {"ledger_dead": False, "proven_dead_by_yield": False,
            "conditioning_only": False, "xr_penalized": False,
            "total_score": 50.0}
    base.update(kw)
    return base


def test_xr_weak_does_not_demote_by_default():
    """默认：跨区弱候选与同分普通候选并列，不被压到队尾。"""
    ci = _load()
    a = _cand(xr_penalized=True, total_score=90.0)
    b = _cand(total_score=80.0)
    assert ci._s0_rank_key(a) < ci._s0_rank_key(b)
    # soft 位必须为 False（旧行为下为 True，会沉到 b 之后）
    assert ci._s0_rank_key(a)[1] is False


def test_xr_penalize_flag_restores_old_behaviour():
    """--xr-penalize：跨区弱重新进入 soft 层，即使分更高也排到普通候选之后。"""
    ci = _load()
    a = _cand(xr_penalized=True, total_score=90.0)
    b = _cand(total_score=80.0)
    assert ci._s0_rank_key(a, xr_penalize=True)[1] is True
    assert ci._s0_rank_key(a, xr_penalize=True) > ci._s0_rank_key(b, xr_penalize=True)
    # 同一开关下，低分普通候选仍在跨区弱之前 → 证明降权生效
    assert ci._s0_rank_key(b, xr_penalize=True) < ci._s0_rank_key(a, xr_penalize=True)


def test_dead_and_conditioning_only_layers_unchanged():
    """判死沉底、字段数不足次沉：两层语义不受 P1 改动影响。"""
    ci = _load()
    clean = _cand(total_score=10.0)
    dead = _cand(ledger_dead=True, total_score=99.0)
    yield_dead = _cand(proven_dead_by_yield=True, total_score=99.0)
    few_fields = _cand(conditioning_only=True, total_score=99.0)
    assert ci._s0_rank_key(clean) < ci._s0_rank_key(few_fields)
    assert ci._s0_rank_key(few_fields) < ci._s0_rank_key(dead)
    assert ci._s0_rank_key(dead)[0] is True
    assert ci._s0_rank_key(yield_dead)[0] is True


def test_score_descending_within_same_tier():
    """同层内按平台分降序（P1 不改动主轴）。"""
    ci = _load()
    keys = [ci._s0_rank_key(_cand(total_score=s)) for s in (90.0, 50.0, 10.0)]
    assert keys == sorted(keys)  # 分高者键小 = 排前面
    assert ci._s0_rank_key(_cand(total_score=90.0)) < ci._s0_rank_key(_cand(total_score=10.0))


def test_zero_and_none_score_do_not_raise():
    """平台分缺失/为 0 时不炸（键位取负，-0.0 仍可比较）。"""
    ci = _load()
    for s in (None, 0, 0.0):
        k = ci._s0_rank_key(_cand(total_score=s))
        assert isinstance(k, tuple) and len(k) == 3
