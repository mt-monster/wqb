#!/usr/bin/env python
"""KOR S-PRE 只读查表（wqb-db MCP 未连接时的降级读取）。只读，不写库。"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from wqb.db_conn import connect as db_connect  # 规范工厂（禁裸 sqlite3.connect）

REGION = sys.argv[1] if len(sys.argv) > 1 else "KOR"
c = db_connect(readonly=True)
_cur=[None]
def q(s,*a):
    _cur[0]=c.execute(s,a)
    return _cur[0].fetchall()
rid = q("SELECT id FROM regions WHERE name=?", REGION)
RID = rid[0][0] if rid else None
print("REGION=", REGION, "region_id=", RID)


def sect(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


def show(rows, lim=300):
    for r in rows:
        d = dict(zip([x[0] for x in _cur[0].description], r))
        print({k: (str(v)[:lim] + "…" if isinstance(v, str) and len(str(v)) > lim else v) for k, v in d.items()})


sect("1. campaign_state")
show(q("SELECT * FROM campaign_state WHERE region_id=?", RID))

sect("2. registry_empirical (win/dead) — layer 计数")
show(q("SELECT layer, COUNT(*) n FROM registry_empirical WHERE region=? GROUP BY layer", REGION))
sect("2b. win 层明细")
show(q("SELECT entry_id, family, payload FROM registry_empirical WHERE region=? AND layer IN ('win','win_recipe','wins') ORDER BY updated_at DESC LIMIT 25", REGION))
sect("2c. dead_end 层明细")
show(q("SELECT entry_id, family, payload FROM registry_empirical WHERE region=? AND layer LIKE '%dead%' ORDER BY updated_at DESC LIMIT 40", REGION))

sect("3. datasets (KOR) — 按 tier/category")
show(q("""SELECT id, name, category, field_count, coverage, alpha_count, tier, status, data_type, delay
          FROM datasets WHERE region_id=? ORDER BY tier, alpha_count""", RID), 120)

sect("4. backtest_results 汇总")
show(q("""SELECT COUNT(*) n, MAX(ABS(sharpe)) ms, MAX(ABS(fitness)) mf,
                 MAX(ABS(risk_neutralized_sharpe)) mrns
          FROM backtest_results WHERE region=?""", REGION))
print("达标(S>1.58 & F>1.0):", q("SELECT COUNT(*) FROM backtest_results WHERE region=? AND ABS(sharpe)>1.58 AND ABS(fitness)>1.0", REGION)[0][0])
sect("4b. 按 dataset 产出")
show(q("""SELECT dataset, COUNT(*) n, ROUND(MAX(ABS(sharpe)),2) ms,
                 SUM(CASE WHEN ABS(sharpe)>1.58 AND ABS(fitness)>1.0 THEN 1 ELSE 0 END) pass,
                 SUM(CASE WHEN ra_failed_checks IS NULL OR ra_failed_checks='' OR ra_failed_checks='[]' THEN 1 ELSE 0 END) clean
          FROM backtest_results WHERE region=? GROUP BY dataset ORDER BY clean DESC, ms DESC""", REGION))

sect("5. 最近 18 波 wave_results")
show(q("""SELECT wave_number, verdict, status, batches, substr(key_findings,1,180) kf, updated_at
          FROM wave_results WHERE region=? ORDER BY updated_at DESC LIMIT 18""", REGION))

sect("6. expressions 积压")
show(q("SELECT status, COUNT(*) n FROM expressions WHERE region=? GROUP BY status", REGION))

sect("7. ledger_kv 键清单 (KOR)")
show(q("SELECT key, LENGTH(value) lv, updated_at FROM ledger_kv WHERE region=? ORDER BY updated_at DESC LIMIT 70", REGION), 60)

sect("8. cross_region_lessons")
show(q("SELECT lesson_id, family, substr(finding,1,200) f, substr(rule,1,200) r FROM cross_region_lessons ORDER BY updated_at DESC LIMIT 20"), 220)

sect("9. alphas (KOR)")
show(q("SELECT status, COUNT(*) n FROM alphas WHERE region_id=? GROUP BY status", RID))
print("-- ACTIVE 明细 --")
show(q("""SELECT alpha_id, status, sharpe, fitness, turnover, prod_correlation, self_correlation, date_submitted
          FROM alphas WHERE region_id=? AND status='ACTIVE' ORDER BY date_submitted DESC LIMIT 40""", RID), 80)
print("-- submit_ready --")
show(q("SELECT status, COUNT(*) n FROM submit_ready WHERE region=? GROUP BY status", REGION))
show(q("SELECT alpha_id, sharpe, fitness, turnover, prod, self, gate, towers, family, status FROM submit_ready WHERE region=? ORDER BY added_at DESC LIMIT 30", REGION), 120)
