# -*- coding: utf-8 -*-
"""2026-11-10 审查第二批：wqb.prod_verdict 唯一判据解析的守护测试。"""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from wqb.prod_verdict import gate_allowed, prod_verdict  # noqa: E402


def _blk(**kw):
    return {"checks": {"production": kw}}


def test_platform_live_is_usable():
    v = prod_verdict(_blk(max_correlation=0.42, passes_check=True))
    assert v["value"] == 0.42 and v["usable"] is True
    assert v["passes"] is True and v["provenance"] == "platform_live"
    assert gate_allowed(_blk(max_correlation=0.42)) is True


def test_trusted_cache_is_usable():
    v = prod_verdict(_blk(max_correlation=0.5, from_cache=True, source="check_correlation"))
    assert v["usable"] is True and v["provenance"] == "cache"


def test_prod_peek_cache_is_usable():
    v = prod_verdict(_blk(max_correlation=0.5, from_cache=True, source="prod_peek"))
    assert v["usable"] is True


@pytest.mark.parametrize("src", ["manual", "legacy", "alphas_backfill",
                                 "checkpoint_backfill", "triage_local", None, ""])
def test_non_realtime_cache_not_usable_but_can_falsify(src):
    v = prod_verdict(_blk(max_correlation=0.4, from_cache=True, source=src))
    assert v["usable"] is False and v["provenance"] == "nonrealtime"
    assert v["passes"] is True          # 数值上 < 阈值
    assert gate_allowed(_blk(max_correlation=0.4, from_cache=True, source=src)) is False
    # 证伪仍然有效：≥ 阈值一律拦
    hi = prod_verdict(_blk(max_correlation=0.8, from_cache=True, source=src))
    assert hi["passes"] is False
    assert gate_allowed(_blk(max_correlation=0.8, from_cache=True, source=src)) is False


def test_preread_not_usable():
    v = prod_verdict(_blk(max_correlation=0.4, source="alpha_detail_cached", provisional=True))
    assert v["provenance"] == "preread" and v["usable"] is False
    assert gate_allowed(_blk(max_correlation=0.4, source="alpha_detail_cached")) is False


@pytest.mark.parametrize("st", ["pending", "correlation_busy", "data_unavailable"])
def test_unavailable_statuses_never_pass(st):
    r = {"status": st, "checks": {"production": {"max_correlation": None, "status": st}}}
    v = prod_verdict(r)
    assert v["value"] is None and v["passes"] is None and v["usable"] is False
    assert v["status"] == st
    assert gate_allowed(r) is False


def test_error_and_non_dict_fail_closed():
    assert prod_verdict({"__error__": "boom"})["status"] == "error"
    assert prod_verdict(None)["usable"] is False
    assert gate_allowed({"__error__": "boom"}) is False
    assert gate_allowed("nonsense") is False


def test_out_of_range_value_is_none():
    for bad in (1.4, -0.1, "abc"):
        v = prod_verdict(_blk(max_correlation=bad))
        assert v["value"] is None and v["passes"] is None
        assert gate_allowed(_blk(max_correlation=bad)) is False


def test_missing_value_never_fabricates_zero():
    v = prod_verdict(_blk())
    assert v["value"] is None and v["passes"] is None
    assert gate_allowed(_blk()) is False


def test_field_name_variants_supported():
    # 顶层 max_correlation
    assert prod_verdict({"max_correlation": 0.3})["value"] == 0.3
    # correlation.max
    assert prod_verdict({"correlation": {"max": 0.3}})["value"] == 0.3
    # get_production_correlation 直返 max
    assert prod_verdict({"max": 0.3, "status": "ok"})["value"] == 0.3
    # judge 的 result 包装
    assert prod_verdict({"result": _blk(max_correlation=0.3)})["value"] == 0.3


def test_threshold_boundary_is_strict():
    assert prod_verdict(_blk(max_correlation=0.7))["passes"] is False
    assert prod_verdict(_blk(max_correlation=0.6999))["passes"] is True
    assert gate_allowed(_blk(max_correlation=0.7)) is False


def test_custom_threshold():
    v = prod_verdict(_blk(max_correlation=0.65), threshold=0.6)
    assert v["threshold"] == 0.6 and v["passes"] is False


def test_default_threshold_from_config():
    from wqb.config import PRODCORR_CEILING
    assert prod_verdict(_blk(max_correlation=0.5))["threshold"] == float(PRODCORR_CEILING)


# ── 2026-11-23 用户「三、优化空间」第 5 条：档案字段 + 交付层强制 ──────────
# 实证：imb5 N1PlYMGX 缓存 0.60(gate_allowed 放行) → refresh 真值 0.9726（漂移 +0.37）
# ⇒ 交付前必须 platform_live；缓存够判闸但不够交付。
def test_archive_fields_record_provenance_and_time():
    from wqb.prod_verdict import archive_fields

    af = archive_fields(_blk(max_correlation=0.42))
    assert af["prod_correlation"] == 0.42
    assert af["prod_provenance"] == "platform_live"
    assert af["prod_usable"] is True and af["prod_passes"] is True
    assert af["corr_checked_at"]  # 实测时刻必须落下来
    assert af["prod_corr_source"].startswith("platform_live")


def test_archive_fields_never_fake_freshness_for_preread():
    """预读值测量时间不可知 ⇒ corr_checked_at 必须是 None，不得写 now 造假新鲜度。"""
    from wqb.prod_verdict import archive_fields

    af = archive_fields(_blk(max_correlation=0.6, provisional=True))
    assert af["prod_provenance"] == "preread"
    assert af["corr_checked_at"] is None
    assert af["prod_usable"] is False


def test_archive_fields_keep_cached_at_from_source():
    from wqb.prod_verdict import archive_fields

    af = archive_fields(_blk(max_correlation=0.6, from_cache=True,
                             source="check_correlation",
                             cached_at="2026-11-23T10:57:22"))
    assert af["corr_checked_at"] == "2026-11-23T10:57:22"
    assert af["prod_provenance"] == "cache"


def test_delivery_block_rejects_cache_even_if_passing():
    """缓存值 passes=True 也拦：交付终验必须 refresh 实测（本轮 0.60→0.9726 教训）。"""
    from wqb.prod_verdict import delivery_block, gate_allowed

    blk = _blk(max_correlation=0.6, from_cache=True, source="check_correlation")
    assert gate_allowed(blk) is True          # 判闸够用
    assert "refresh=True" in delivery_block(blk)  # 交付不够用


def test_delivery_block_rejects_live_fail():
    from wqb.prod_verdict import delivery_block

    msg = delivery_block(_blk(max_correlation=0.9707))
    assert msg and "撞红线" in msg


def test_delivery_block_allows_live_pass():
    from wqb.prod_verdict import delivery_block

    assert delivery_block(_blk(max_correlation=0.42)) is None


def test_delivery_block_rejects_unavailable():
    from wqb.prod_verdict import delivery_block

    assert "refresh=True" in delivery_block({"status": "platform_unavailable",
                                             "checks": {"production": {"status": "platform_unavailable"}}})
