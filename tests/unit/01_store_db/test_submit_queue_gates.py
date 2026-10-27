# -*- coding: utf-8 -*-
"""submit_queue 三坑回归（2026-09-20）：

坑 1  RA 硬闸 FAIL（robust / sub-universe / CW ...）不得进 READY
坑 2  add(A,B) 混腿不得进 READY；同骨架兄弟已实测 prod>=0.7 且本条 prod 未测 → DEAD（PROD_SIBLING）
坑 3  SUBMITTED/DEAD 终态粘性（harvest 再 enqueue 不复活）；enqueue_from_alphas 排除平台 ACTIVE/已提交；
      retire_active / retire_platform_done 把已 ACTIVE 的 READY 行退役
"""
import os
import sqlite3
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "src"))

from wqb.store import submit_queue as sq  # noqa: E402

_ALPHAS_DDL = """
CREATE TABLE regions (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE alphas (
    alpha_id TEXT, region_id INTEGER, universe TEXT, delay INTEGER, neutralization TEXT,
    expression TEXT, sharpe REAL, fitness REAL, turnover REAL, two_year_sharpe REAL,
    sub_universe_sharpe REAL, cluster_test REAL, prod_correlation REAL, self_correlation REAL,
    soft_deleted INTEGER DEFAULT 0, disposition TEXT, status TEXT,
    platform_status TEXT, date_submitted TEXT);
CREATE TABLE backtest_results (id INTEGER PRIMARY KEY AUTOINCREMENT, alpha_id TEXT, ra_failed_checks TEXT);
INSERT INTO regions VALUES (1, 'IND');
"""

_GOOD = dict(sharpe=3.0, fitness=2.0, turnover=0.2, two_year_sharpe=2.5,
             sub_universe_sharpe=1.5, cluster_test=None, prod_correlation=None, self_correlation=None,
             universe="TOP500", delay=1, neutralization="SUBINDUSTRY", status="UNSUBMITTED")


@pytest.fixture()
def db(tmp_path, monkeypatch):
    path = str(tmp_path / "t.db")
    con = sqlite3.connect(path)
    con.executescript(_ALPHAS_DDL)
    con.commit()
    con.close()
    monkeypatch.setenv("WQB_DB_PATH", path)
    return path


def _ins_alpha(path, aid, expr, **kw):
    row = dict(_GOOD, **kw)
    con = sqlite3.connect(path)
    con.execute(
        """INSERT INTO alphas (alpha_id, region_id, universe, delay, neutralization, expression,
           sharpe, fitness, turnover, two_year_sharpe, sub_universe_sharpe, cluster_test,
           prod_correlation, self_correlation, soft_deleted, disposition, status, platform_status, date_submitted)
           VALUES (?,1,?,?,?,?,?,?,?,?,?,?,?,?,0,NULL,?,?,?)""",
        (aid, row["universe"], row["delay"], row["neutralization"], expr, row["sharpe"], row["fitness"],
         row["turnover"], row["two_year_sharpe"], row["sub_universe_sharpe"], row["cluster_test"],
         row["prod_correlation"], row["self_correlation"], row["status"],
         row.get("platform_status"), row.get("date_submitted")))
    con.commit()
    con.close()


def _ins_bt(path, aid, fails):
    con = sqlite3.connect(path)
    con.execute("INSERT INTO backtest_results (alpha_id, ra_failed_checks) VALUES (?,?)", (aid, fails))
    con.commit()
    con.close()


def _status(path, aid):
    con = sqlite3.connect(path)
    r = con.execute("SELECT status, gate, note FROM submit_ready WHERE alpha_id=?", (aid,)).fetchone()
    con.close()
    return r


# ---------------- 坑 1：RA 硬闸 ----------------

def test_ra_fail_of_accepts_list_json_double_encoded_and_dict():
    assert sq.ra_fail_of(["LOW_ROBUST_UNIVERSE_SHARPE"]) == "LOW_ROBUST_UNIVERSE_SHARPE"
    assert sq.ra_fail_of('["CONCENTRATED_WEIGHT"]') == "CONCENTRATED_WEIGHT"
    assert sq.ra_fail_of('"[\\"HIGH_TURNOVER\\"]"') == "HIGH_TURNOVER"
    assert sq.ra_fail_of({"fail": [{"name": "IS_LADDER_SHARPE"}]}) == "IS_LADDER_SHARPE"
    assert sq.ra_fail_of([{"name": "LOW_SUB_UNIVERSE_SHARPE", "result": "FAIL"}]) == "LOW_SUB_UNIVERSE_SHARPE"
    # 非硬闸名（WARNING/PENDING 类）与空值不触发
    assert sq.ra_fail_of(None) is None
    assert sq.ra_fail_of("[]") is None
    assert sq.ra_fail_of(["MATCHES_COMPETITION"]) is None


def test_gate_of_ra_fail_is_dead_even_when_metrics_pass():
    gate, st = sq.gate_of(3.0, 2.0, 2.5, 0.2, 0.5, 0.3, ["LOW_ROBUST_UNIVERSE_SHARPE"], "rank(x)")
    assert (gate, st) == ("FAIL:RA:LOW_ROBUST_UNIVERSE_SHARPE", sq.STATUS_DEAD)


def test_enqueue_from_alphas_carries_latest_ra_failed_checks(db):
    _ins_alpha(db, "A1", "rank(ts_mean(x, 5))")
    _ins_bt(db, "A1", '["LOW_ROBUST_UNIVERSE_SHARPE"]')       # 旧记录
    _ins_bt(db, "A1", '[]')                                    # 最新记录已通过
    _ins_alpha(db, "A2", "rank(ts_mean(y, 22))")
    _ins_bt(db, "A2", '["CONCENTRATED_WEIGHT"]')
    sq.enqueue_from_alphas(region="IND", dedup=False)
    assert _status(db, "A1")[0] == sq.STATUS_READY
    assert _status(db, "A2")[:2] == (sq.STATUS_DEAD, "FAIL:RA:CONCENTRATED_WEIGHT")


# ---------------- 坑 2：add 混腿 + prod 兄弟 ----------------

@pytest.mark.parametrize("expr,mix", [
    # 口径 = gate.py 闸5（用户 2026-09-13 路线 A）：只拦「加权」混腿
    ("rank(add(multiply(0.4, a), multiply(0.6, b)))", True),                # multiply 权重在前
    ("add(multiply(rank(a), 0.4), multiply(rank(b), 0.6))", True),          # multiply 权重在后
    ("quantile(add(0.7*rank(a), 0.3*zscore(b)))", True),                    # 星号中缀
    ("add(0.5*rank(a), subtract(0, rank(b)), -0.2*rank(c))", True),         # 含镜像腿、≥2 系数腿
    ("add(multiply(0.4, a), add(multiply(0.3, b), multiply(0.3, c)))", True),  # 嵌套 add
    ("add(rank(a), rank(b))", False),                                       # 等权不拦
    ("add(0.5*rank(a), rank(b))", False),                                   # 单腿缩放不拦
    ("subtract(rank(a), rank(b))", False),                                  # 闸5 列为合规替代
    ("multiply(-1, ts_mean(corr_last_trade_price_with_volume, 5))", False),
    ("ts_mean(subtract(divide(close, p), 1), 5)", False),
    ("group_rank(ts_delta(x, 5), subindustry)", False),
    ("add(multiply(-1, x), 1)", False),                                     # 单系数腿 + 常数
    # 上游截断到 110 字符的表达式（括号不平衡）：结构判定放行，靠闸5 正则兜底
    ("rank(add(multiply(0.4, rank(ts_backfill(long_term_quantile5_r120_pred, 66))), multiply(0.3, rank(ts_backfill(s", True),
    ("add(0.3 * rank(ts_av_diff(ep_yield_pct_smest_fy2_3, 20)), 0.233 * multiply(rank(forward_pe_smest_fy1_3), -1), ", True),
    ("add(add(rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 6)), rank(ts_mean(mean_estimate_change_pct_", False),
    (None, False),
])
def test_is_add_mix(expr, mix):
    assert sq.is_add_mix(expr) is mix


def test_gate_of_add_mix_is_dead():
    gate, st = sq.gate_of(3.0, 2.0, 2.5, 0.2, 0.5, 0.3, [], "add(multiply(0.4, rank(a)), multiply(0.6, rank(b)))")
    assert (gate, st) == ("FAIL:ADD_MIX", sq.STATUS_DEAD)


def test_prod_sibling_marks_untested_twin_dead(db):
    # 同骨架（仅窗口数字不同）兄弟已实测 prod 0.82 → 本条 prod 未测者不得进 READY
    _ins_alpha(db, "W1", "multiply(-1, ts_mean(f1, 5))", prod_correlation=0.82)
    _ins_alpha(db, "W2", "multiply(-1, ts_mean(f1, 22))")
    sq.enqueue_from_alphas(region="IND", dedup=False)
    assert _status(db, "W1")[:2] == (sq.STATUS_DEAD, "FAIL:PROD")
    st, gate, _ = _status(db, "W2")
    assert st == sq.STATUS_DEAD and gate.startswith("FAIL:PROD_SIBLING(W1=0.82")


def test_prod_sibling_not_applied_when_own_prod_measured(db):
    _ins_alpha(db, "W1", "multiply(-1, ts_mean(f1, 5))", prod_correlation=0.82)
    _ins_alpha(db, "W3", "multiply(-1, ts_mean(f1, 66))", prod_correlation=0.55, self_correlation=0.3)
    sq.enqueue_from_alphas(region="IND", dedup=False)
    assert _status(db, "W3")[:2] == (sq.STATUS_READY, "SUBMIT_LAYER_VERIFIED")


# ---------------- 坑 3：终态粘性 + ACTIVE 排除 + 退役 ----------------

def test_submitted_and_dead_are_sticky_on_reenqueue(db):
    _ins_alpha(db, "S1", "rank(ts_mean(x, 5))")
    _ins_alpha(db, "D1", "rank(ts_mean(y, 5))")
    sq.enqueue_from_alphas(region="IND", dedup=False)
    assert sq.retire("S1", sq.STATUS_SUBMITTED) == 1
    assert sq.retire("D1", sq.STATUS_DEAD) == 1
    # harvest 收批再次自动入队：不得复活
    sq.enqueue_from_alphas(region="IND", dedup=False, note="auto-enqueue wave=99")
    assert _status(db, "S1")[0] == sq.STATUS_SUBMITTED
    assert _status(db, "D1")[0] == sq.STATUS_DEAD
    assert "retired:SUBMITTED" in _status(db, "S1")[2]   # note 也不被覆盖


def test_ready_row_still_refreshes_metrics_on_reenqueue(db):
    _ins_alpha(db, "R1", "rank(ts_mean(x, 5))")
    sq.enqueue_from_alphas(region="IND", dedup=False)
    con = sqlite3.connect(db)
    con.execute("UPDATE alphas SET prod_correlation=0.5, self_correlation=0.2 WHERE alpha_id='R1'")
    con.commit(); con.close()
    sq.enqueue_from_alphas(region="IND", dedup=False)
    assert _status(db, "R1")[:2] == (sq.STATUS_READY, "SUBMIT_LAYER_VERIFIED")


def test_enqueue_from_alphas_skips_platform_active_and_submitted(db):
    _ins_alpha(db, "ACT", "rank(ts_mean(x, 5))", status="COMPLETE", platform_status="ACTIVE")
    _ins_alpha(db, "DEC", "rank(ts_mean(y, 5))", status="COMPLETE", platform_status="DECOMMISSIONED")
    _ins_alpha(db, "SUB", "rank(ts_mean(z, 5))", status="COMPLETE", date_submitted="2026-09-20")
    _ins_alpha(db, "NEW", "rank(ts_mean(w, 5))", status="COMPLETE")
    n = sq.enqueue_from_alphas(region="IND", dedup=False)
    assert n == 1
    assert _status(db, "NEW")[0] == sq.STATUS_READY
    assert _status(db, "ACT") is None and _status(db, "DEC") is None and _status(db, "SUB") is None


def test_retire_platform_done_and_retire_active(db):
    _ins_alpha(db, "P1", "rank(ts_mean(x, 5))")
    _ins_alpha(db, "P2", "rank(ts_mean(y, 5))")
    _ins_alpha(db, "P3", "rank(ts_mean(z, 5))")
    sq.enqueue_from_alphas(region="IND", dedup=False)
    # 之后平台上 P1 变 ACTIVE（本地 alphas 表同步到了），P2 只在平台 OS 列表里
    con = sqlite3.connect(db)
    con.execute("UPDATE alphas SET platform_status='ACTIVE' WHERE alpha_id='P1'")
    con.commit(); con.close()
    assert sq.retire_platform_done(region="IND") == 1
    assert sq.retire_active(["P2", "nonexistent"], region="IND") == 1
    assert _status(db, "P1")[0] == sq.STATUS_SUBMITTED
    assert _status(db, "P2")[0] == sq.STATUS_SUBMITTED
    assert _status(db, "P3")[0] == sq.STATUS_READY
    # 幂等
    assert sq.retire_platform_done(region="IND") == 0
    assert sq.retire_active(["P2"], region="IND") == 0
    # list_ready 只剩 P3
    assert [r["alpha_id"] for r in sq.list_ready(region="IND")] == ["P3"]


def test_regrade_ready_applies_new_gates_to_legacy_rows(db):
    # 模拟闸门升级前入队的历史行：add 混腿 / RA FAIL / prod 兄弟 都还是 READY
    _ins_alpha(db, "L1", "add(multiply(0.4, rank(a)), multiply(0.6, rank(b)))")
    _ins_alpha(db, "L2", "rank(ts_mean(x, 5))")
    _ins_alpha(db, "L3", "multiply(-1, ts_mean(f1, 22))")
    _ins_alpha(db, "L4", "rank(ts_mean(y, 5))")
    sq.enqueue_from_alphas(region="IND", dedup=False)
    con = sqlite3.connect(db)
    con.execute("UPDATE submit_ready SET status='READY', gate='IS_ONLY'")   # 回滚成旧闸门状态
    con.execute("INSERT INTO backtest_results (alpha_id, ra_failed_checks) VALUES ('L2','[\"LOW_ROBUST_UNIVERSE_SHARPE\"]')")
    con.execute("INSERT INTO submit_ready (alpha_id, region, expr, skeleton, prod, status) "
                "VALUES ('L3s','IND','multiply(-1, ts_mean(f1, 5))', ?, 0.9, 'DEAD')",
                (sq._sig("multiply(-1, ts_mean(f1, 5))"),))
    con.commit(); con.close()
    d = sq.regrade_ready(region="IND", dry_run=True)
    assert _status(db, "L1")[0] == sq.STATUS_READY          # dry-run 不写
    d = sq.regrade_ready(region="IND")
    assert d["checked"] == 4 and d["dead"] == 3
    assert _status(db, "L1")[:2] == (sq.STATUS_DEAD, "FAIL:ADD_MIX")
    assert _status(db, "L2")[:2] == (sq.STATUS_DEAD, "FAIL:RA:LOW_ROBUST_UNIVERSE_SHARPE")
    assert _status(db, "L3")[0] == sq.STATUS_DEAD and _status(db, "L3")[1].startswith("FAIL:PROD_SIBLING(L3s=0.90")
    assert _status(db, "L4")[0] == sq.STATUS_READY
    assert sq.regrade_ready(region="IND")["changes"] == []   # 幂等


def test_regrade_revives_sibling_dead_row_once_prod_is_measured(db):
    """#88：入队早于相关性实测 → 被兄弟闸判死，此后再也进不了复判集（旧实现只扫 READY）。

    真实事故 `88vXxaqv` / `LL53QVvn`：14:15:24 入队（prod=NULL）被兄弟 `qMEVJPo2=0.81` 判 DEAD；
    2 分钟后自身 prod 实测 0.6811 / 0.5761 落进 `alphas`（persist_correlation 不回写队列表），
    队列表停在 NULL/DEAD，结论与事实相反且永久不可申诉。
    """
    _ins_alpha(db, "SIB", "multiply(-1, ts_mean(f1, 66))", prod_correlation=0.81)
    _ins_alpha(db, "ME", "rank(ts_mean(y, 5))", prod_correlation=0.6811)
    sq.enqueue_from_alphas(region="IND", dedup=False)
    con = sqlite3.connect(db)
    # 复现事故形态：队列表里 prod 还是入队快照（NULL），兄弟闸已经把本行判死
    con.execute("UPDATE submit_ready SET prod=NULL, self=NULL, status='DEAD', "
                "gate='FAIL:PROD_SIBLING(SIB=0.81)' WHERE alpha_id='ME'")
    con.execute("UPDATE submit_ready SET status='DEAD', gate='FAIL:PROD_WALL' WHERE alpha_id='SIB'")
    con.commit(); con.close()

    assert sq.regrade_ready(region="IND", dry_run=True)["revived"] == 1
    assert _status(db, "ME")[0] == sq.STATUS_DEAD            # dry-run 不写
    d = sq.regrade_ready(region="IND")
    assert d["revived"] == 1
    st, gate, note = _status(db, "ME")
    assert st == sq.STATUS_READY and gate == "IS_ONLY"       # self 仍未测 → 待验，不是可提交
    assert "regrade:revived(FAIL:PROD_SIBLING(SIB=0.81))" in note
    con = sqlite3.connect(db)
    prod = con.execute("SELECT prod FROM submit_ready WHERE alpha_id='ME'").fetchone()[0]
    con.close()
    assert prod == pytest.approx(0.6811)                     # 以 alphas 镜像回填
    assert sq.regrade_ready(region="IND")["changes"] == []    # 幂等


def test_bulk_enqueue_never_overwrites_platform_verified_rows(db):
    # 坑 4：verify/add（平台实测）写回的 prod 不能被并行的 add-many/harvest 用 alphas 表旧值覆盖
    _ins_alpha(db, "V1", "rank(ts_mean(x, 5))", prod_correlation=0.48, self_correlation=0.2)
    sq.enqueue_from_alphas(region="IND", dedup=False)
    con = sqlite3.connect(db)
    assert con.execute("SELECT verified_by FROM submit_ready WHERE alpha_id='V1'").fetchone()[0] == "alphas"
    # 模拟 verify 写回平台新值
    con.execute("UPDATE submit_ready SET prod=0.64, verified_by='verify', verified_at='2099-01-01T00:00:00' WHERE alpha_id='V1'")
    con.commit(); con.close()
    sq.enqueue_from_alphas(region="IND", dedup=False)
    con = sqlite3.connect(db)
    prod, vb, vat = con.execute("SELECT prod, verified_by, verified_at FROM submit_ready WHERE alpha_id='V1'").fetchone()
    con.close()
    assert (prod, vb, vat) == (0.64, "verify", "2099-01-01T00:00:00")


# ---------------- N33：CampaignStore 建的库上 enqueue 不崩 ----------------

def test_enqueue_from_alphas_on_campaignstore_db(tmp_path):
    """N33：CampaignStore 建的库此前缺 soft_deleted/disposition 列，enqueue_from_alphas 的
    WHERE 直接 `no such column: a.soft_deleted`（harvest auto-enqueue 静默吞成「入队跳过」）。
    补列后应正常入队，且达标 alpha 落 READY。"""
    from wqb.store import CampaignStore

    path = str(tmp_path / "camp.db")
    store = CampaignStore(path)
    try:
        # 走规范写入路径把一条达标 alpha 落进 alphas 表（status 默认 UNSUBMITTED）
        store.upsert_expressions("IND", "1", ["rank(close)"], dataset="pv")
        store.upsert_backtest_rows(
            "IND", "1",
            [{"id": "N33A", "code": "rank(close)", "sharpe": 3.0, "fitness": 2.0,
              "turnover": 0.2, "two_year_sharpe": 2.5, "status": "UNSUBMITTED"}],
            dataset="pv",
        )
    finally:
        store.close()

    # 不得抛 sqlite3.OperationalError
    n = sq.enqueue_from_alphas(region="IND", db_path=path, dedup=False)
    assert n == 1
    row = _status(path, "N33A")
    assert row is not None and row[0] == sq.STATUS_READY


# ---------------- P1-3：族签名必须含分组轴与设置档（USA d5KzLo7v 事故回归） ----------------

#: 真实事故对（2026-10-23 USA 复盘 §9.3）：主体形状**逐字相同**，只差分组轴与中性化。
#: d5KzLo7v 是当时全 USA 唯一同时过 prod/self 双闸、且落在**未点亮塔**的候选，
#: 旧口径（仅主体形状）把它与 zqrGqVXo 判同族并标 PROD_SIBLING 判死。
_INCIDENT_PAIR = {
    # (expr, neutralization, universe, delay)
    "d5KzLo7v": ("tail(winsorize(group_rank(ts_zscore(eur_aggregated_value_1, 252), subindustry), "
                 "std=2), lower=0.2, upper=0.8, newval=0.5)", "SUBINDUSTRY", "TOP3000", 1),
    "zqrGqVXo": ("tail(winsorize(group_rank(ts_zscore(eur_aggregated_value_1, 252), industry), "
                 "std=2), lower=0.25, upper=0.75, newval=0.5)", "MARKET", "TOP3000", 1),
}


def test_family_signature_separates_incident_pair():
    """P1-3 验收（报告 §10 原文）：`d5KzLo7v`（market）vs `zqrGqVXo`（subindustry）**必须判不同族**。"""
    rows, parts = {}, {}
    for aid, (expr, neut, uni, delay) in _INCIDENT_PAIR.items():
        rows[aid] = {"alpha_id": aid, "expr": expr, "neutralization": neut,
                     "universe": uni, "delay": delay}
        parts[aid] = sq.family_parts_of_row(rows[aid])
    # 前提：主体骨架确实相同（否则这条回归没测到东西）
    assert parts["d5KzLo7v"]["body"] == parts["zqrGqVXo"]["body"]
    # 判据一：严格字符串签名不同（去重侧）
    assert sq.family_signature_of_row(rows["d5KzLo7v"]) != sq.family_signature_of_row(rows["zqrGqVXo"])
    # 判据二：通配口径（兄弟连坐侧）同样不同族
    assert not sq._same_family(parts["d5KzLo7v"], parts["zqrGqVXo"])


def test_family_signature_keeps_sibling_rule_alive_when_settings_partial():
    """P1-3 反向保护：设置档记账不全（老队列行 / alphas 镜像缺 decay）时，
    兄弟连坐**不能整条失效**（通配口径：一侧未知 ⇒ 放行）。"""
    a = sq.family_parts("rank(ts_mean(f1, 22))", {"neutralization": "SUBINDUSTRY", "universe": "TOP3000"},
                        row_key="A")
    b = sq.family_parts("rank(ts_mean(f1, 22))", {}, row_key="B")     # 一行设置档全缺
    assert sq._same_family(a, b)
    # 但「两侧都知道且不同」必须分族
    c = sq.family_parts("rank(ts_mean(f1, 22))", {"neutralization": "MARKET", "universe": "TOP3000"},
                        row_key="C")
    assert not sq._same_family(a, c)


def test_family_signature_differs_on_settings_profile():
    """P1-3：decay/truncation 不同 ⇒ 不同族（报告 §10：设置档必须进签名）。"""
    e = "rank(ts_mean(f1, 22))"
    s1 = sq.family_signature(e, {"decay": 4, "truncation": 0.08, "neutralization": "SUBINDUSTRY"})
    s2 = sq.family_signature(e, {"decay": 20, "truncation": 0.05, "neutralization": "SUBINDUSTRY"})
    assert s1 != s2 and s1.startswith(sq.FAMILY_SIG_PREFIX)
    # 平台 camelCase 与本地 snake_case 归一后同签名
    assert sq.family_signature(e, {"nanHandling": "ON", "maxTrade": "OFF"}) == \
        sq.family_signature(e, {"nan_handling": "ON", "max_trade": "OFF"})
    # 设置档全缺 ⇒ 字符串签名降级为行级唯一（保守：不与其他行同族），且带前缀可识别
    s3 = sq.family_signature(e, {}, row_key="K1")
    s4 = sq.family_signature(e, {}, row_key="K2")
    assert s3 != s4 and "NOSETTINGS#K1" in s3
