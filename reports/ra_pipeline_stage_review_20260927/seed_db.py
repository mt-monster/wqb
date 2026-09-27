# -*- coding: utf-8 -*-
"""Seed a SYNTHETIC campaign DB inside the sandbox (region KOR, fake dataset syn_analyst).

All values are fixtures for exercising code paths; they are not real platform data.
"""
import json
import os
import sqlite3
import sys

SBX = os.environ["SBX"]
sys.path.insert(0, os.path.join(SBX, "src"))
from wqb.store import CampaignStore  # noqa: E402

DB = os.path.join(SBX, "data", "wqb.db")
if os.path.exists(DB):
    os.remove(DB)
st = CampaignStore(DB)
R, DS = "KOR", "syn_analyst"

# ---- typed catalog (闸2/3/8 数据源) ----
fields = [
    {"id": "syn_eps_rev_up", "type": "MATRIX", "coverage": 0.92, "userCount": 3, "alphaCount": 12},
    {"id": "syn_eps_rev_dn", "type": "MATRIX", "coverage": 0.91, "userCount": 5, "alphaCount": 20},
    {"id": "syn_num_est", "type": "MATRIX", "coverage": 0.95, "userCount": 60, "alphaCount": 900},
    {"id": "syn_tgt_px_gap", "type": "MATRIX", "coverage": 0.35, "userCount": 2, "alphaCount": 4},
    {"id": "syn_rec_mean", "type": "MATRIX", "coverage": 0.88, "userCount": 15, "alphaCount": 80},
    {"id": "syn_surprise_evt", "type": "EVENT", "coverage": 0.30, "userCount": 1, "alphaCount": 2},
    {"id": "syn_est_vec", "type": "VECTOR", "coverage": 0.85, "userCount": 0, "alphaCount": 0},
]
st.upsert_field_catalog(R, {"dataset": DS, "data_type": "MATRIX", "region": R, "delay": 1,
                            "universe": "TOP600", "fields": fields})

# ---- 3 closed waves with backtests (w1..w3) ----
def rows(wave, n, lo, step, fail_top=0, rn_neg_idx=None):
    out = []
    for i in range(n):
        s = round(lo + i * step, 3)
        r = {"alpha_id": f"SYN{wave}{i:03d}", "code": f"rank(ts_delta(syn_eps_rev_up, {5 + i}))",
             "sharpe": s, "fitness": round(0.6 * s, 3), "turnover": 0.12, "margin": 0.0008,
             "two_year_sharpe": round(0.8 * s, 3), "sub_universe_sharpe": round(0.7 * s, 3),
             "risk_neutralized_sharpe": round(0.5 * s, 3), "universe": "TOP600", "delay": 1,
             "neutralization": "STATISTICAL", "status": "COMPLETE"}
        if fail_top and i >= n - fail_top:
            r["ra_failed_checks"] = ["LOW_2Y_SHARPE"]
        if rn_neg_idx is not None and i == rn_neg_idx:
            r["risk_neutralized_sharpe"] = -0.2
        out.append(r)
    return out

st.upsert_backtest_rows(R, "w1", rows("w1", 40, -0.6, 0.065, fail_top=2, rn_neg_idx=37), dataset=DS)
st.upsert_backtest_rows(R, "w2", rows("w2", 40, -0.8, 0.05), dataset=DS)   # max 1.15
st.upsert_backtest_rows(R, "w3", rows("w3", 40, -0.9, 0.045), dataset=DS)  # max 0.855

# ---- current wave w4: 150 gem + 30 gated (未消费积压) ----
gem = [f"group_rank(ts_mean(syn_eps_rev_up, {d}), subindustry)" for d in range(1, 151)]
st.upsert_expressions(R, "w4", gem, dataset=DS, status="gem", source="gem")
gated = [f"rank(ts_zscore(syn_rec_mean, {d}))" for d in range(1, 31)]
st.upsert_expressions(R, "w4", gated, dataset=DS, status="gated", source="gem")

conn = st.connection
# upsert_backtest_rows 自动建的表达式行：确保 status=backtested（口径与积压闸一致）
conn.execute("UPDATE expressions SET status='backtested' WHERE region=? AND wave IN ('w1','w2','w3')", (R,))
conn.commit()

# ---- wave_results: w1 PARTIAL / w2 FAIL / w3 FAIL (closed, 时间戳显式递增) ----
for w, v, ts in (("w1", "PARTIAL", "2026-09-20 10:00:00"), ("w2", "FAIL", "2026-09-21 10:00:00"),
                 ("w3", "FAIL", "2026-09-22 10:00:00")):
    conn.execute("INSERT INTO wave_results (region, wave_number, verdict, status, key_findings, "
                 "created_at, updated_at) VALUES (?,?,?,?,?,?,?)",
                 (R, w, v, "closed", json.dumps([f"fixture {w}"]), ts, ts))
conn.commit()

# ---- ledger ----
st.upsert_ledger(R, "s0_whitelist", {"universe": "TOP600", "delay": 1,
                                      "datasets": [DS, "syn_news"], "generated_at": "2026-09-20"})
st.upsert_ledger(R, "s0_ranking", {"universe": "TOP600", "ranking": [
    {"dataset": DS, "score": 0.81, "tier": 1}, {"dataset": "syn_news", "score": 0.55, "tier": 2}]})
st.upsert_ledger(R, "region_kb", {
    "win_recipes": [{"name": "rev_breadth_fixture",
                     "skeleton": "group_rank(ts_delta(syn_eps_rev_up,22),subindustry)",
                     "evidence": "synthetic fixture", "settings": "STATISTICAL/decay4"}],
    "dead_patterns": ["news_emotion 3 连死 (fixture)"],
    "gate_priors": {"by_decay": {"4": {"n": 300, "pass_rate": 0.03}, "10": {"n": 40, "pass_rate": 0.09}}},
})
st.upsert_ledger(R, "s1_syn_analyst_d1", {"ideas_md_path": os.path.join(SBX, "output_report", "_missing_ideas.md"),
                                           "source": "feature_engineering_node"})

# ---- 体检包（field_inspect，步 5 体检硬门数据源）----
pack = {"fields": {DS: {
    "syn_tgt_px_gap": {"metadata": {"coverage_ratio": 0.35, "skewness": 3.1, "kurtosis": 12.0,
                                    "distribution_shape": "heavy_tail"}, "advices": []},
    "syn_eps_rev_up": {"metadata": {"coverage_ratio": 0.92, "skewness": 0.4, "kurtosis": 3.0,
                                    "distribution_shape": "normal"}, "advices": []},
    "syn_surprise_evt": {"metadata": {"coverage_ratio": 0.30, "skewness": None, "kurtosis": None,
                                      "distribution_shape": "zero_inflated"}, "advices": []},
}}}
with open(os.path.join(SBX, "tracking", "mining", "field_inspect_kor_syn_analyst.json"), "w",
          encoding="utf-8") as f:
    json.dump(pack, f, ensure_ascii=False, indent=1)

# ---- GEM runner 占位 config（仓库不含 config.json / config.example.json；dry-run 只查存在性）----
cfg = os.path.join(SBX, "Claude", "skills", "brain-make-some-gem", "scripts", "headless_runner", "config.json")
with open(cfg, "w", encoding="utf-8") as f:
    json.dump({"_sandbox_placeholder": True}, f)

# ---- 汇总 ----
q = lambda sql, *p: conn.execute(sql, p).fetchall()
print("expressions by status:", q("SELECT status, COUNT(*) FROM expressions WHERE region=? GROUP BY status", R))
print("backtest_results:", q("SELECT wave, COUNT(*), MAX(sharpe) FROM backtest_results WHERE region=? GROUP BY wave", R))
print("wave_results:", q("SELECT wave_number, verdict, status FROM wave_results WHERE region=?", R))
print("ledger keys:", [r[0] for r in q("SELECT key FROM ledger_kv WHERE region=?", R)])
print("field_catalog datasets:", q("SELECT name, data_type, field_count FROM datasets"))
st.close()
