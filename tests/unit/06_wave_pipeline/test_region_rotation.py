# -*- coding: utf-8 -*-
"""test_region_rotation.py — 区域饱和检测 + 跨区轮转决策（纯逻辑 + 采集 SQL）。

覆盖：
  - gather_region_metrics：内存 sqlite 建最小 schema + 已知行 → 校验 prod_measured /
    prod_wall / feasible / exhausted 计算（守护 SQL 占位符绑定数，回归 2026-09-14 的 12-vs-11 bug）
  - detect_saturation：非 prod 信号支撑饱和 / 可行库存豁免 / frozen 硬饱和 / prod 薄样本 caveat
  - rotation_score：薄样本 prod 中性（不虚高）/ proven-zero-yield 罚 / 可行存量加分
  - rank_next_regions：排除当前区 + frozen / 降序 / include_saturated 开关
  - recommend_rotation：未饱和不轮转 / 饱和选最优可行区 / 全饱和兜底
"""
import os
import sqlite3
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))), "src"))

from wqb.region_rotation import (  # noqa: E402
    SATURATION_THRESHOLDS,
    VERDICT_SATURATED,
    VERDICT_VIABLE,
    VERDICT_WATCH,
    detect_saturation,
    gather_all_regions,
    gather_region_metrics,
    rank_next_regions,
    recommend_rotation,
    rotation_score,
)


# ---------------- 采集层：内存 DB ----------------

def _mem_conn():
    """建最小 schema 的内存 sqlite（仅含 gather_region_metrics 用到的列）。"""
    c = sqlite3.connect(":memory:")
    c.executescript(
        """
        CREATE TABLE regions (id INTEGER PRIMARY KEY, name TEXT);
        CREATE TABLE alphas (alpha_id TEXT, region_id INTEGER, sharpe REAL,
            prod_correlation REAL, self_correlation REAL, platform_status TEXT);
        CREATE TABLE backtest_results (region TEXT, sharpe REAL);
        CREATE TABLE registry_empirical (region TEXT, layer TEXT, payload TEXT);
        CREATE TABLE waves (region_id INTEGER, wave_number TEXT);
        """
    )
    return c


def _seed(conn):
    """TST 区：10 回测(4 达标) + 5 alphas(覆盖 prod NULL/墙/可行/ACTIVE/self墙)。"""
    conn.execute("INSERT INTO regions VALUES (1,'TST')")
    # backtest_results：4 条 |sharpe|>=1.58
    for s in [2.0, 1.7, -1.6, 1.9, 0.5, 1.0, 0.2, 1.2, 0.9, 1.55]:
        conn.execute("INSERT INTO backtest_results VALUES ('TST',?)", (s,))
    # alphas
    conn.executemany("INSERT INTO alphas VALUES (?,?,?,?,?,?)", [
        ("a1", 1, 2.0, 0.5, 0.3, "COMPLETE"),    # feasible + unsubmitted
        ("a2", 1, 1.8, 0.9, 0.2, "COMPLETE"),    # prod 墙
        ("a3", 1, 1.7, None, None, "UNSUBMITTED"),  # prod NULL（未测量）
        ("a4", 1, 1.6, 0.4, 0.8, "ACTIVE"),      # self 墙 + ACTIVE
        ("a5", 1, 1.0, 0.2, 0.1, "COMPLETE"),    # sharpe 未达标
    ])
    conn.execute("INSERT INTO registry_empirical VALUES ('TST','dead_end','{}')")
    conn.execute("INSERT INTO registry_empirical VALUES ('TST','dead_end','{}')")
    conn.execute("INSERT INTO registry_empirical VALUES ('TST','win','{}')")
    conn.execute("INSERT INTO registry_empirical VALUES ('TST','campaign','{\"status\":\"exhausted\"}')")
    conn.execute("INSERT INTO registry_empirical VALUES ('TST','campaign','{\"status\":\"untried\"}')")
    for w in ["1", "2", "3"]:
        conn.execute("INSERT INTO waves VALUES (1,?)", (w,))
    conn.commit()


def test_gather_backtest_yield():
    conn = _mem_conn()
    _seed(conn)
    m = gather_region_metrics(conn, "TST")
    assert m["backtested"] == 10
    assert m["bt_sharpe_pass"] == 4  # 2.0/1.7/-1.6/1.9（ABS>=1.58）
    assert m["yield_rate"] == pytest.approx(0.4)


def test_gather_alpha_prod_feasible():
    """守护 prod/feasible SQL：占位符绑定数错误会全 0（回归 12-vs-11 bug）。"""
    conn = _mem_conn()
    _seed(conn)
    m = gather_region_metrics(conn, "TST")
    assert m["alphas_total"] == 5
    assert m["sharpe_pass"] == 4          # a1-a4（a5 sharpe 1.0 未达标）
    assert m["prod_measured"] == 3        # a1/a2/a4 有 prod；a3 NULL 不计
    assert m["prod_wall"] == 1            # 仅 a2 prod 0.9>=0.7
    assert m["feasible_measured"] == 1    # 仅 a1（a4 self 0.8 撞 self 墙）
    assert m["feasible_unsubmitted"] == 1  # a1 platform_status!=ACTIVE
    assert m["active"] == 1               # a4
    assert m["prod_wall_ratio"] == pytest.approx(1 / 3, abs=1e-3)


def test_gather_registry_and_waves():
    conn = _mem_conn()
    _seed(conn)
    m = gather_region_metrics(conn, "TST")
    assert m["dead_ends"] == 2 and m["wins"] == 1
    assert m["campaigns"] == {"untried": 1, "in_progress": 0, "exhausted": 1}
    assert m["campaigns_total"] == 2 and m["exhausted_pct"] == pytest.approx(0.5)
    assert m["waves"] == 3


def test_gather_entry_verdict_injected():
    conn = _mem_conn()
    _seed(conn)
    assert gather_region_metrics(conn, "TST")["entry_verdict"] == "unknown"
    assert gather_region_metrics(conn, "TST", entry_verdict="frozen")["entry_verdict"] == "frozen"


def test_gather_missing_region_safe_zeros():
    """无记录区域安全降级为 0，不抛异常。"""
    conn = _mem_conn()
    _seed(conn)
    m = gather_region_metrics(conn, "NOWHERE")
    assert m["backtested"] == 0 and m["alphas_total"] == 0 and m["yield_rate"] is None


def test_gather_all_regions_filters_empty():
    conn = _mem_conn()
    _seed(conn)
    conn.execute("INSERT INTO regions VALUES (2,'BLANK')")  # 无任何活动
    conn.commit()
    allm = gather_all_regions(conn)
    assert "TST" in allm and "BLANK" not in allm  # 无活动痕迹的区域被过滤


# ---------------- 决策层：detect_saturation（纯 dict） ----------------

def _metrics(**kw):
    """构造指标 dict 的便捷工厂（合理默认 + 覆写）。"""
    base = dict(region="XXX", entry_verdict="active", backtested=100, bt_sharpe_pass=10,
                yield_rate=0.10, alphas_total=50, sharpe_pass=10, prod_measured=10,
                prod_wall=1, prod_wall_ratio=0.1, feasible_measured=9,
                feasible_unsubmitted=5, active=3, dead_ends=5, wins=2,
                campaigns={"untried": 1, "in_progress": 0, "exhausted": 1},
                campaigns_total=2, exhausted_pct=0.5, waves=20)
    base.update(kw)
    return base


def test_saturation_viable_fresh_region():
    res = detect_saturation(_metrics())
    assert res["verdict"] == VERDICT_VIABLE
    assert res["data_caveat"] is None


def test_saturation_frozen_is_hard_saturated():
    res = detect_saturation(_metrics(entry_verdict="frozen"))
    assert res["verdict"] == VERDICT_SATURATED
    assert "frozen_profile" in res["strong"]


def test_saturation_eur_like_via_nonprod_signals():
    """EUR 型：战役穷尽 100% + 深挖 166 波 + 110 死路 → 饱和（不依赖 prod 测量量）。"""
    res = detect_saturation(_metrics(
        exhausted_pct=1.0, campaigns={"untried": 0, "in_progress": 0, "exhausted": 6},
        campaigns_total=6, waves=166, dead_ends=110, prod_measured=4,
        prod_wall_ratio=0.0, feasible_unsubmitted=0, yield_rate=0.083))
    assert res["verdict"] == VERDICT_SATURATED
    assert {"campaigns_exhausted", "mined_out", "dead_end_saturated"} <= set(res["strong"])
    # prod 薄样本 → caveat 存在，但饱和判定不靠它
    assert res["data_caveat"] is not None and "prod" in res["data_caveat"]


def test_saturation_thin_prod_suppresses_prod_signals():
    """prod_measured < min_measured → prod_wall / no_feasible_headroom 不触发，回 caveat。"""
    res = detect_saturation(_metrics(
        prod_measured=3, prod_wall=3, prod_wall_ratio=1.0, feasible_unsubmitted=0))
    assert "prod_wall" not in res["strong"]
    assert "no_feasible_headroom" not in res["strong"]
    assert res["data_caveat"] is not None


def test_saturation_prod_wall_fires_when_measured():
    """prod_measured 充足 + 墙占比高 → prod_wall 触发（IND/MEA 型）。"""
    res = detect_saturation(_metrics(
        prod_measured=100, prod_wall=73, prod_wall_ratio=0.73, feasible_unsubmitted=0,
        exhausted_pct=0.95, campaigns={"untried": 0, "in_progress": 0, "exhausted": 20},
        campaigns_total=20))
    assert "prod_wall" in res["strong"]
    assert "no_feasible_headroom" in res["strong"]
    assert res["verdict"] == VERDICT_SATURATED


def test_saturation_feasible_reprieve_downgrades_to_watch():
    """IND 型：prod 墙 + 战役穷尽本应饱和，但 feasible_unsubmitted>=5 → 豁免降 WATCH。"""
    res = detect_saturation(_metrics(
        prod_measured=104, prod_wall=76, prod_wall_ratio=0.73, feasible_unsubmitted=8,
        exhausted_pct=0.95, campaigns={"untried": 0, "in_progress": 0, "exhausted": 37},
        campaigns_total=39, dead_ends=53))
    assert res["verdict"] == VERDICT_WATCH
    assert any("豁免" in r for r in res["reasons"])


def test_saturation_reprieve_not_applied_to_frozen():
    """frozen 区即便有可行库存也不豁免（平台/季度硬限制）。"""
    res = detect_saturation(_metrics(entry_verdict="frozen", feasible_unsubmitted=8))
    assert res["verdict"] == VERDICT_SATURATED


def test_saturation_yield_collapse_is_medium():
    res = detect_saturation(_metrics(
        yield_rate=0.01, backtested=300, exhausted_pct=0.0,
        campaigns={"untried": 0, "in_progress": 0, "exhausted": 0}, campaigns_total=0,
        dead_ends=0, waves=10, prod_measured=0, prod_wall_ratio=None))
    assert "yield_collapse" in res["medium"]


def test_saturation_thresholds_overridable():
    m = _metrics(exhausted_pct=0.7, campaigns_total=6,
                 campaigns={"untried": 0, "in_progress": 0, "exhausted": 4}, waves=10,
                 dead_ends=0, prod_measured=0, prod_wall_ratio=None, feasible_unsubmitted=0)
    assert detect_saturation(m)["verdict"] != VERDICT_SATURATED  # 默认 0.8 阈值下未穷尽
    # 放宽 exhausted 阈值到 0.6 → 触发（但仍需第二个 strong；此处验证阈值被读取）
    res = detect_saturation(m, thresholds={"exhausted_pct_min": 0.6})
    assert "campaigns_exhausted" in res["strong"]


def test_saturation_defaults_unchanged():
    assert SATURATION_THRESHOLDS["prod_wall_ratio_max"] == 0.60
    assert SATURATION_THRESHOLDS["min_measured"] == 8
    assert SATURATION_THRESHOLDS["feasible_reprieve_min"] == 5


# ---------------- 决策层：rotation_score ----------------

def test_score_thin_prod_not_inflated():
    """薄样本 prod（measured<8）不得给满分 prod_ok：与中性 0.5 同分。"""
    thin = _metrics(region="GBR", prod_measured=4, prod_wall=0, prod_wall_ratio=0.0,
                    feasible_unsubmitted=0, yield_rate=0.0, backtested=267,
                    exhausted_pct=0.0, waves=47)
    # 一个 prod 未测（None）但其余相同的区域应与薄样本低墙区域同分（都拿中性 0.5）
    unmeasured = dict(thin, prod_measured=0, prod_wall_ratio=None)
    assert rotation_score(thin) == pytest.approx(rotation_score(unmeasured), abs=1e-6)


def test_score_zero_yield_penalty():
    """大量回测 + 0 产出 → 罚 0.5（结构性难产，非新大陆）。"""
    hard = _metrics(region="GBR", yield_rate=0.0, backtested=267, feasible_unsubmitted=0)
    fresh = _metrics(region="NEW", yield_rate=0.0, backtested=20, feasible_unsubmitted=0)
    # 同为 0 yield，但回测量大的被罚；小样本未知不罚 → fresh 分更高（其它特征相同时）
    hard2 = dict(hard, backtested=267)
    assert rotation_score(hard2) < rotation_score(fresh)


def test_score_feasible_headroom_boosts():
    lo = _metrics(feasible_unsubmitted=0)
    hi = _metrics(feasible_unsubmitted=15)
    assert rotation_score(hi) > rotation_score(lo)


def test_score_yield_dominates_target_choice():
    """高产出区分数高于零产出区（同 verdict/entry_verdict）。"""
    hi = _metrics(region="IND", yield_rate=0.378, feasible_unsubmitted=8,
                  prod_measured=104, prod_wall_ratio=0.73)
    lo = _metrics(region="GBR", yield_rate=0.0, feasible_unsubmitted=0,
                  prod_measured=4, prod_wall_ratio=0.0, backtested=267)
    assert rotation_score(hi) > rotation_score(lo)


def test_score_frozen_zeroed():
    assert rotation_score(_metrics(entry_verdict="frozen")) == 0.0


def test_score_saturated_penalized():
    m = _metrics()
    s_sat = {"verdict": VERDICT_SATURATED}
    s_ok = {"verdict": VERDICT_VIABLE}
    assert rotation_score(m, s_sat) < rotation_score(m, s_ok)


# ---------------- 决策层：rank_next_regions ----------------

def _all_metrics():
    return {
        "EUR": _metrics(region="EUR", exhausted_pct=1.0, waves=166, dead_ends=110,
                        campaigns_total=6, campaigns={"untried": 0, "in_progress": 0, "exhausted": 6},
                        prod_measured=4, prod_wall_ratio=0.0, feasible_unsubmitted=0, yield_rate=0.083),
        "IND": _metrics(region="IND", yield_rate=0.378, feasible_unsubmitted=8,
                        prod_measured=104, prod_wall=76, prod_wall_ratio=0.73,
                        exhausted_pct=0.95, campaigns_total=39,
                        campaigns={"untried": 0, "in_progress": 0, "exhausted": 37}, dead_ends=53),
        "MEA": _metrics(region="MEA", entry_verdict="frozen", yield_rate=0.199),
        "GBR": _metrics(region="GBR", yield_rate=0.0, backtested=267, feasible_unsubmitted=0,
                        prod_measured=4, prod_wall_ratio=0.0),
        "DEU": _metrics(region="DEU", entry_verdict="probe-only", yield_rate=0.251,
                        backtested=1288, prod_measured=5, prod_wall_ratio=1.0,
                        feasible_unsubmitted=0, exhausted_pct=0.0, waves=131, dead_ends=23),
    }


def test_rank_excludes_current_and_frozen():
    ranked = rank_next_regions(_all_metrics(), exclude=("EUR",))
    regions = [r["region"] for r in ranked]
    assert "EUR" not in regions       # 当前区排除
    assert "MEA" not in regions       # frozen 排除
    assert "IND" in regions and "GBR" in regions


def test_rank_sorted_desc():
    ranked = rank_next_regions(_all_metrics(), exclude=("EUR",))
    scores = [r["score"] for r in ranked]
    assert scores == sorted(scores, reverse=True)


# ---------------- fail-safe：campaign 状态采集失败不可被当成"未饱和"（2026-10-03） ----------------
#
# 缺陷背景：`_campaign_status` 原先 `except Exception: pass` 后返回全零。返回值进
# `detect_saturation.exhausted_pct` 与 `rotation_score.f_headroom/f_untried`，
# 于是「DB 读不到战役状态」被当成「该区战役很少、空间最大」→ f_headroom=1.0 满分，
# 给出**方向相反**的转区建议。而 region_rotation 的卖点正是"零平台请求、零配额"，
# 最该确定的地方反而最不可靠。历史前科见 .workbuddy/memory/2026-10-01.md
# （310 行无 status 的脏 campaign 记录被长期静默忽略，无任何告警）。
#
# 这些用例**不 mock**：用缺 `registry_empirical` 表的真实 sqlite 连接触发
# sqlite3.OperationalError，验证真实失败路径。


def _broken_campaign_conn():
    """只缺 registry_empirical 表的内存 DB → campaign 查询必然抛 OperationalError。

    其余表保留，使 gather_region_metrics 的其他指标仍能采集（模拟"DB 部分可用"
    而非整体不可用——最容易被静默吞掉的情形）。
    """
    c = sqlite3.connect(":memory:")
    c.executescript(
        """
        CREATE TABLE regions (id INTEGER PRIMARY KEY, name TEXT);
        CREATE TABLE alphas (alpha_id TEXT, region_id INTEGER, sharpe REAL,
            prod_correlation REAL, self_correlation REAL, platform_status TEXT);
        CREATE TABLE backtest_results (region TEXT, sharpe REAL);
        CREATE TABLE waves (region_id INTEGER, wave_number TEXT);
        """
    )
    c.execute("INSERT INTO regions VALUES (1,'TST')")
    for s in [2.0, 1.7, -1.6, 1.9, 0.5, 1.0, 0.2, 1.2, 0.9, 1.55]:
        c.execute("INSERT INTO backtest_results VALUES ('TST',?)", (s,))
    c.execute("INSERT INTO waves VALUES (1,'1')")
    c.commit()
    return c


def test_campaign_query_failure_is_distinguishable_from_zero_campaigns():
    """采集失败必须给 campaigns_available=False + exhausted_pct=None，而非全零。"""
    m = gather_region_metrics(_broken_campaign_conn(), "TST")
    assert m["campaigns_available"] is False
    assert m["exhausted_pct"] is None, "未知 ≠ 0.0（0.0 会被读成『确认未穷尽』）"
    # 其他指标仍应采集成功（部分可用 ≠ 全部不可用）
    assert m["backtested"] == 10


def test_available_flag_true_on_healthy_db():
    """回归守护：正常 DB 下 campaigns_available 必须为 True（别把 fail-safe 写成常态）。"""
    conn = _mem_conn()
    _seed(conn)
    m = gather_region_metrics(conn, "TST")
    assert m["campaigns_available"] is True
    assert m["exhausted_pct"] == pytest.approx(0.5)


def test_saturation_disables_campaign_signals_when_unavailable():
    """campaign 不可采信 → 禁用 campaigns_exhausted / mined_out 强信号。"""
    metrics = _metrics(region="EUR", exhausted_pct=1.0, campaigns_total=6,
                       campaigns={"untried": 0, "in_progress": 0, "exhausted": 6},
                       waves=200, dead_ends=120)
    healthy = detect_saturation(dict(metrics, campaigns_available=True))
    broken = detect_saturation(dict(metrics, campaigns_available=False,
                                    exhausted_pct=None))

    # 健康时这两个 campaign 依赖的信号确实会触发
    assert "campaigns_exhausted" in healthy["strong"]
    assert "mined_out" in healthy["strong"]

    # 采集失败时：不得据此断言饱和
    assert "campaigns_exhausted" not in broken["strong"]
    assert "mined_out" not in broken["strong"]
    # 且必须显式声明证据不足，而不是静默
    assert broken["data_caveat"] and "campaign" in broken["data_caveat"]


def test_rotation_score_headroom_is_neutral_not_max_when_unknown():
    """★ 核心回归：exhausted_pct 未知时 f_headroom 不得取满分 1.0。

    旧实现 `1.0 - _clamp01(m.get("exhausted_pct") or 0.0)` 在 None 时得 1.0（满分），
    等于把「读不到战役状态」宣传成「该区空间最大」。这里锁定中性 0.5。
    """
    known_empty = {"region": "AAA", "exhausted_pct": 0.0, "campaigns_available": True,
                   "campaigns": {"untried": 0, "in_progress": 0, "exhausted": 0},
                   "entry_verdict": "active"}
    known_full = dict(known_empty, exhausted_pct=1.0,
                      campaigns={"untried": 0, "in_progress": 0, "exhausted": 5})
    unknown = dict(known_empty, exhausted_pct=None, campaigns_available=False)

    s_empty = rotation_score(dict(known_empty))
    s_full = rotation_score(dict(known_full))
    s_unknown = rotation_score(dict(unknown))

    assert s_empty > s_full, "确认未穷尽应优于已穷尽（校准前提）"
    assert s_unknown < s_empty, (
        "★ campaign 状态未知时不得优于『确认未穷尽』——旧实现会得满分从而虚高")
    # 中性 0.5：应落在两者之间
    assert s_full < s_unknown < s_empty


def test_rotation_score_untried_neutral_when_campaigns_unavailable():
    """campaign 不可采信时 f_untried 取中性，不得因查不到 untried 而把该区排末。"""
    base = {"region": "BBB", "exhausted_pct": 0.0, "entry_verdict": "active",
            "yield_rate": 0.2, "backtested": 50, "prod_measured": 20,
            "prod_wall_ratio": 0.3, "feasible_unsubmitted": 2}
    with_untried = dict(base, campaigns_available=True,
                        campaigns={"untried": 8, "in_progress": 0, "exhausted": 0})
    unknown = dict(base, campaigns_available=False,
                   campaigns={"untried": 0, "in_progress": 0, "exhausted": 0})
    # 未知时既不应得满分（像有大量 untried）也不应得 0 分（像完全没有）
    assert rotation_score(unknown) > rotation_score(dict(unknown, campaigns_available=True,
                                                        campaigns={"untried": 0, "in_progress": 0, "exhausted": 0}))
    assert rotation_score(unknown) < rotation_score(with_untried)


def test_recommend_rotation_does_not_rotate_on_unavailable_campaign_data():
    """端到端：唯一区 campaign 状态不可采信时，不得给出"该区未饱和、继续挖"的误导结论。"""
    metrics = {"EUR": _metrics(region="EUR", exhausted_pct=None, campaigns_total=0,
                               campaigns_available=False, waves=200, dead_ends=120)}
    rec = recommend_rotation("EUR", metrics, target=20)
    assert rec["should_rotate"] is False
    assert "campaigns_exhausted" not in rec["current_saturation"]["strong"]



def test_rank_ind_beats_zeroyield():
    """IND（真实产出+库存）排在 GBR（0 产出）之前。"""
    ranked = rank_next_regions(_all_metrics(), exclude=("EUR",))
    order = [r["region"] for r in ranked]
    assert order.index("IND") < order.index("GBR")


def test_rank_include_saturated_flag():
    allm = _all_metrics()
    # 把 IND 也变饱和（库存清零 + 穷尽）→ include_saturated=False 应排除它
    allm["IND"] = _metrics(region="IND", yield_rate=0.378, feasible_unsubmitted=0,
                           prod_measured=104, prod_wall=76, prod_wall_ratio=0.73,
                           exhausted_pct=0.95, campaigns_total=39,
                           campaigns={"untried": 0, "in_progress": 0, "exhausted": 37},
                           dead_ends=53)
    with_sat = rank_next_regions(allm, exclude=("EUR",), include_saturated=True)
    without = rank_next_regions(allm, exclude=("EUR",), include_saturated=False)
    assert "IND" in [r["region"] for r in with_sat]
    assert "IND" not in [r["region"] for r in without]


# ---------------- 决策层：recommend_rotation ----------------

def test_recommend_no_rotate_when_viable():
    allm = {"CUR": _metrics(region="CUR"), "OTHER": _metrics(region="OTHER")}
    rec = recommend_rotation("CUR", allm, target=20)
    assert rec["should_rotate"] is False
    assert rec["to_region"] is None
    assert rec["carry_target"] == 20
    assert "继续" in rec["next_action"]


def test_recommend_rotates_when_saturated():
    allm = _all_metrics()
    rec = recommend_rotation("EUR", allm, target=20)
    assert rec["should_rotate"] is True
    assert rec["from_region"] == "EUR"
    assert rec["to_region"] == "IND"       # 最高分可行区
    assert rec["all_saturated"] is False
    assert rec["carry_target"] == 20
    assert "IND" in rec["next_action"]


def test_recommend_carries_target_into_next_region():
    allm = _all_metrics()
    rec = recommend_rotation("EUR", allm, target=20)
    assert rec["carry_target"] == 20
    # 2026-09-25 P4：转入区有 8 颗未提交可行存量时，承接目标 = max(0, target - feasible) = 12
    assert "12" in rec["next_action"]


def test_recommend_all_saturated_fallback():
    """全部候选饱和 → all_saturated=True，仍给最不乏味者 + 升级提示。"""
    allm = {
        "EUR": _metrics(region="EUR", exhausted_pct=1.0, waves=166, dead_ends=110,
                        campaigns_total=6, campaigns={"untried": 0, "in_progress": 0, "exhausted": 6},
                        prod_measured=4, feasible_unsubmitted=0),
        "A": _metrics(region="A", exhausted_pct=1.0, waves=150, dead_ends=120,
                      campaigns_total=6, campaigns={"untried": 0, "in_progress": 0, "exhausted": 6},
                      prod_measured=4, feasible_unsubmitted=0),
    }
    rec = recommend_rotation("EUR", allm, target=20)
    assert rec["should_rotate"] is True
    assert rec["all_saturated"] is True
    assert "next-move" in rec["next_action"] or "next_move" in rec["next_action"]


def test_recommend_unknown_region_errors_gracefully():
    rec = recommend_rotation("NOPE", {"EUR": _metrics(region="EUR")}, target=20)
    assert rec["should_rotate"] is False
    assert rec.get("error")


def test_recommend_ranked_present_and_ordered():
    rec = recommend_rotation("EUR", _all_metrics(), target=20)
    scores = [r["score"] for r in rec["ranked"]]
    assert scores == sorted(scores, reverse=True)
    assert rec["ranked"][0]["region"] == rec["to_region"]
