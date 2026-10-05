# -*- coding: utf-8 -*-
"""相关性**单源化**契约（2026-10-05 审计 P1 的回归网）。

审计发现的三个事实，本文件逐条钉住：

1. **三套存储并存、无同步契约**：``alphas.prod_correlation`` / ``alpha_corr_cache``
   各自演进 ⇒ 实测 6 颗 GBR 的值只写在 ``alphas`` 里，``check_correlation`` 的 db
   缓存读不到 → 盘点判 ``CORR_UNKNOWN`` → 重复打平台单并发队列（每颗 1-5 分钟）。
   修法 = 单源写（``set_corr_cache`` 联动镜像）+ 单源读（``get_corr_authoritative``
   回落 ``alphas``）。
2. **来源自由文本无法判可信度**：``prod_corr_source`` 曾有 6 个值
   （``prod_first_screen`` / ``platform_sync`` / ``check_correlation`` / ``prod_first`` /
   ``p0_1_verify_20260923`` / ``raw_poll``），而读侧过滤只认三值词表。
3. **保鲜期必须单一事实源**：生产池会漂移（实证 EUR ``le8Y68K2`` 0.6929 → 0.9932），
   48h 口径散写多处即会漂移。
"""

import pytest

from wqb.store import CampaignStore
from wqb.store._corr_cache import CORR_SOURCES, normalize_corr_source


@pytest.fixture
def store(tmp_path):
    db = CampaignStore(str(tmp_path / "corr_single_source.db"))
    yield db
    db.close()


# --- 1. 来源词表收敛 -------------------------------------------------------


def test_normalize_collapses_legacy_free_text():
    """审计点名的 6 个自由文本必须全部收敛到登记词表。

    它们都是平台侧实测/同步产物，故归 ``platform_sync``；原值经
    ``source_detail`` 保留供复盘（不落库——表里没有该列）。
    """
    legacy = [
        "prod_first_screen", "platform_sync", "check_correlation",
        "prod_first", "p0_1_verify_20260923", "raw_poll",
    ]
    for raw in legacy:
        out = normalize_corr_source(raw)
        assert out["source"] in CORR_SOURCES, f"{raw!r} 未收敛: {out}"
        assert out["source"] == "platform_sync"
        assert out["source_detail"] == raw  # 原词不丢


def test_normalize_unknown_source_downgrades_conservatively():
    """未知来源 → ``triage_local``，**不许冒充平台权威**。

    方向性：把本地估算标成 platform_sync 会让低可信值绕过重测（放行方向的错），
    反向低估只会多测一次。空/None 同样落最保守档。
    """
    assert normalize_corr_source("some_new_tool_20270101")["source"] == "triage_local"
    assert normalize_corr_source("")["source"] == "triage_local"
    assert normalize_corr_source(None)["source"] == "triage_local"
    assert normalize_corr_source("   ")["source"] == "triage_local"


def test_source_vocabulary_matches_reader_filter():
    """词表必须与读侧过滤（``get_alpha_corr_metrics`` 的 ``source``）同口径。

    两边漂移的症状是「过滤值永远查不到行」——docstring 列了三值，写侧却写进第四个。
    """
    import wqb_db_mcp
    doc = wqb_db_mcp.get_alpha_corr_metrics.__doc__ or ""
    for src in CORR_SOURCES:
        assert src in doc, f"读侧文档未登记词 {src}"


# --- 2. 单源写：权威表联动镜像 alphas --------------------------------------


def _seed_alphas(store, alpha_id):
    """往 alphas 种一行；fixture 库无 region 定义时返回 False（调用方 skip）。"""
    try:
        store.upsert_alpha_from_platform({
            "alpha_id": alpha_id, "region": "KOR", "expression": "rank(close)",
            "sharpe": 1.8, "fitness": 1.1, "platform_status": "UNSUBMITTED",
            "alpha_type": "REGULAR", "stage": "IS",
        })
        return True
    except Exception:  # noqa: BLE001 - fixture 库可能无 regions 行
        return False


def test_single_write_mirrors_into_alphas(store):
    """写权威表即写 ``alphas``——这正是 6 颗 GBR 被重复测量的根因。"""
    if not _seed_alphas(store, "mir_s1"):
        pytest.skip("fixture 无 region 定义")

    out = store.set_corr_cache("mir_s1", prod=0.42, source="platform")
    assert "skipped" not in out, out
    assert out["mirror"].get("skipped") != "not_found", out

    row = store.connection.execute(
        "SELECT prod_correlation, prod_corr_source FROM alphas WHERE alpha_id='mir_s1'"
    ).fetchone()
    assert row is not None
    assert abs(float(row[0]) - 0.42) < 1e-9
    assert row[1] in CORR_SOURCES


def test_single_write_survives_missing_alphas_row(store):
    """平台侧候选不在 ``alphas`` 表 → 权威表照样落值（镜像失败不阻断）。

    旧路径裸 ``UPDATE alphas`` 影响 0 行且不报错，等于测了没测。
    """
    out = store.set_corr_cache("ghost_s1", prod=0.55, source="platform")
    assert "skipped" not in out, out
    assert out["mirror"].get("skipped") == "not_found"
    got = store.get_corr_cache("ghost_s1")
    assert got is not None and abs(got["prod_correlation"] - 0.55) < 1e-9


def test_low_trust_source_does_not_overwrite_platform_value(store):
    """低可信（``triage_local``）不得覆盖已存的平台权威值。"""
    if not _seed_alphas(store, "mir_s2"):
        pytest.skip("fixture 无 region 定义")

    store.set_corr_cache("mir_s2", prod=0.30, source="platform")
    row = store.connection.execute(
        "SELECT prod_correlation FROM alphas WHERE alpha_id='mir_s2'"
    ).fetchone()
    assert abs(float(row[0]) - 0.30) < 1e-9

    # 本地抽测给出不同值：权威表更新（它是最新一次测量），但 alphas 保持平台值
    store.set_corr_cache("mir_s2", prod=0.61, source="triage_local")
    row = store.connection.execute(
        "SELECT prod_correlation, prod_corr_source FROM alphas WHERE alpha_id='mir_s2'"
    ).fetchone()
    assert abs(float(row[0]) - 0.30) < 1e-9, "低可信值覆盖了平台权威值"
    cache = store.get_corr_cache("mir_s2")
    assert abs(cache["prod_correlation"] - 0.61) < 1e-9, "权威表应保留最新测量"


# --- 3. 单源读：权威表缺条目回落 alphas ------------------------------------


def test_authoritative_read_falls_back_to_alphas(store):
    """值只写在 ``alphas`` 里的行必须能被读到（否则重复回源平台）。"""
    if not _seed_alphas(store, "fb_s1"):
        pytest.skip("fixture 无 region 定义")
    store.connection.execute(
        "UPDATE alphas SET prod_correlation=0.66, prod_corr_source='platform_sync',"
        " corr_checked_at=datetime('now') WHERE alpha_id='fb_s1'"
    )
    store.connection.commit()

    assert store.get_corr_cache("fb_s1") is None  # 权威表确实没条目
    got = store.get_corr_authoritative("fb_s1")
    assert got is not None
    assert abs(got["max"] - 0.66) < 1e-9
    assert got["backend"] == "alphas"
    assert got["stale"] is False


def test_authoritative_read_prefers_authoritative_table(store):
    """两侧都有值时以权威表为准（它是唯一写入口的产物）。"""
    if not _seed_alphas(store, "fb_s2"):
        pytest.skip("fixture 无 region 定义")
    store.connection.execute(
        "UPDATE alphas SET prod_correlation=0.90 WHERE alpha_id='fb_s2'"
    )
    store.connection.commit()
    store.set_corr_cache("fb_s2", prod=0.40, source="platform")

    got = store.get_corr_authoritative("fb_s2")
    assert abs(got["max"] - 0.40) < 1e-9
    assert got["backend"] == "alpha_corr_cache"


def test_authoritative_read_returns_none_when_unmeasured(store):
    """双缺失 → None（调用方据此判「未测」，不是「测出来是 0」）。"""
    assert store.get_corr_authoritative("never_seen_s1") is None


# --- 4. 保鲜期单一事实源 ---------------------------------------------------


def test_fresh_hours_is_single_source_48h():
    """48h 是全仓唯一口径：MCP TTL 与查询工具默认值都须与它同值。"""
    from wqb.store._corr_cache import CORR_FRESH_HOURS, CORR_FRESH_SECONDS
    assert CORR_FRESH_HOURS == 48
    assert CORR_FRESH_SECONDS == 48 * 3600

    import re
    from pathlib import Path
    mixin = (Path(__file__).resolve().parents[3]
             / "world-quant-brain-mcp" / "brain_mixin_correlation.py")
    if mixin.exists():
        src = mixin.read_text(encoding="utf-8")
        m = re.search(r"_PROD_CORR_TTL_SECONDS\s*=\s*(\d+)", src)
        assert m, "MCP 侧未声明 _PROD_CORR_TTL_SECONDS"
        assert int(m.group(1)) == CORR_FRESH_SECONDS, "MCP TTL 与 CORR_FRESH_HOURS 漂移"


def test_stale_flag_flips_past_fresh_hours(store):
    """超过保鲜期必须标 stale——stale 值只能排序参考，不得当终验。"""
    store.set_corr_cache("age_s1", prod=0.5, source="platform")
    fresh = store.get_corr_cache("age_s1")
    assert fresh["fresh"] is True and fresh["stale"] is False
    assert fresh["age_hours"] is not None and fresh["age_hours"] < 1

    store.connection.execute(
        "UPDATE alpha_corr_cache SET checked_at='2026-01-01T00:00:00'"
        " WHERE alpha_id='age_s1'"
    )
    store.connection.commit()
    old = store.get_corr_cache("age_s1")
    assert old["stale"] is True and old["fresh"] is False
    assert old["age_hours"] > 48

