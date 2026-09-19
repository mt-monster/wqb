# -*- coding: utf-8 -*-
"""2026-09-19 GEM 生成侧预闸扩展回归（pipeline_pregate.py）。

实证：IND w171/w172 与 JPN w7 三个数据集共 13 条 `hump(x, 0.01)`（平台只认 hump=）需手工改；
JPN w7 四条 `bucket(rank(x))` 缺 range → 平台 ERROR 整批连坐；JPN 池 17 条用了平台不存在的
sector/subindustry；GEM 大量产 20/60/63/250 等非标窗（CLAUDE.md 只允许 1/5/22/66/252/504/1008/1260）。
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GEM_DIR = REPO_ROOT / "Claude" / "skills" / "brain-make-some-gem" / "scripts" / "trailSomeAlphas"
if str(GEM_DIR) not in sys.path:
    sys.path.insert(0, str(GEM_DIR))

import pipeline_pregate as pg  # noqa: E402


def test_hump_positional_becomes_named():
    e, n = pg.normalize_named_only("hump(ts_delta(ts_backfill(x, 5), 22), 0.01)")
    assert n == 1 and e == "hump(ts_delta(ts_backfill(x, 5), 22), hump=0.01)"
    # 已是命名参数 / 单参数：不动
    for ok in ("hump(x, hump=0.05)", "hump(x)", "rank(hump(x))"):
        assert pg.normalize_named_only(ok) == (ok, 0)


def test_bucket_rank_gets_default_range_and_non_rank_is_unfixable():
    e, n, bad = pg.normalize_bucket("group_neutralize(y, bucket(rank(x)))")
    assert n == 1 and bad == 0 and e == 'group_neutralize(y, bucket(rank(x), range="0,1,0.1"))'
    e, n, bad = pg.normalize_bucket("group_rank(y, bucket(analyst_conf))")
    assert n == 0 and bad == 1                       # 值域未知，不补默认值
    ok = 'group_rank(y, bucket(rank(x), range="0,1,0.2"))'
    assert pg.normalize_bucket(ok) == (ok, 0, 0)


def test_windows_normalize_only_near_standard_values():
    e, n, rem = pg.normalize_windows("ts_mean(ts_backfill(f, 60), 20)")
    assert e == "ts_mean(ts_backfill(f, 66), 22)" and n == 2 and rem == []
    e, n, rem = pg.normalize_windows("ts_corr(a, b, 250)")
    assert e == "ts_corr(a, b, 252)" and n == 1
    # 10 / 33 / 44 / 126 不在别名表：保留原值并报告为非标窗
    e, n, rem = pg.normalize_windows("ts_corr(ts_delta(a, 10), b, 33)")
    assert n == 0 and sorted(rem) == [10, 33] and e == "ts_corr(ts_delta(a, 10), b, 33)"
    # 阈值/常数不是窗口位：不碰（trade_when 第 2 参数 0.3；divide 常数）
    ok = "trade_when(greater(abs(x), 0.3), divide(y, 60), -1)"
    assert pg.normalize_windows(ok)[0] == ok


def test_region_invalid_group_fields_env_override(monkeypatch):
    assert pg.region_invalid_group_fields("JPN") == ("sector", "subindustry", "industry")
    assert pg.region_invalid_group_fields("IND") == ()
    monkeypatch.setenv("WQB_INVALID_GROUP_FIELDS", "country, exchange")
    assert pg.region_invalid_group_fields("IND") == ("country", "exchange")


def test_pregate_end_to_end_jpn(monkeypatch):
    monkeypatch.delenv("WQB_INVALID_GROUP_FIELDS", raising=False)
    exprs = [
        "hump(ts_delta(x, 22), 0.05)",                       # → 命名参数
        "group_zscore(x, sector)",                            # JPN 非法 group 字段 → 丢
        "group_neutralize(x, bucket(y))",                     # bucket 缺 range 且非 rank → 丢
        "group_neutralize(x, bucket(rank(y)))",               # → 补 range
        "ts_mean(x, 60)",                                     # → 66
        "ts_mean(x, 60)",                                     # 归一后与上条重复 → 去重
    ]
    kept, rep = pg.pregate(exprs, log=lambda *_: None, region="JPN")
    assert kept == [
        "hump(ts_delta(x, 22), hump=0.05)",
        'group_neutralize(x, bucket(rank(y), range="0,1,0.1"))',
        "ts_mean(x, 66)",
    ]
    assert rep["named_arg_normalized"] == 1
    assert rep["bucket_range_added"] == 1 and rep["bucket_dropped"] == 1
    assert rep["invalid_group_dropped"] == 1
    assert rep["windows_normalized"] == 2
    assert rep["kept"] == 3


def test_pregate_window_normalization_can_be_disabled():
    kept, rep = pg.pregate(["ts_mean(x, 60)"], log=lambda *_: None, region="IND", normalize_window=False)
    assert kept == ["ts_mean(x, 60)"] and rep["windows_normalized"] == 0


def test_skeleton_signature_and_cap():
    assert pg.skeleton_signature("rank(ts_mean(snt21_pos_mean, 22))") == pg.skeleton_signature("rank(ts_mean(snt21_neg_max, 66))")
    assert pg.skeleton_signature("rank(ts_mean(a, 22))") != pg.skeleton_signature("rank(ts_delta(a, 22))")
    # 命名参数名与 group 关键字保留，不当字段
    assert "hump=" in pg.skeleton_signature("hump(x, hump=0.01)")
    assert "subindustry" in pg.skeleton_signature("group_rank(x, subindustry)")
    exprs = [f"rank(ts_mean(f{i}, 22))" for i in range(20)] + ["rank(ts_delta(g, 5))"]
    kept, dropped, n_skel = pg.cap_per_skeleton(exprs, 3)
    assert len(kept) == 4 and dropped == 17 and n_skel == 2
    assert pg.cap_per_skeleton(exprs, 0) == (exprs, 0, 0)          # 0 关闭


def test_pregate_applies_skeleton_cap(monkeypatch):
    monkeypatch.delenv("WQB_GEM_MAX_PER_SKELETON", raising=False)
    exprs = [f"rank(ts_mean(f{i}, 22))" for i in range(30)]
    kept, rep = pg.pregate(exprs, log=lambda *_: None, region="IND", max_per_skeleton=5)
    assert len(kept) == 5 and rep["skeleton_capped"] == 25 and rep["skeletons"] == 1
    monkeypatch.setenv("WQB_GEM_MAX_PER_SKELETON", "7")
    kept, rep = pg.pregate(exprs, log=lambda *_: None, region="IND")
    assert len(kept) == 7 and rep["max_per_skeleton"] == 7
