"""mine_v12.py
目标：挖 3 个"互不相关"且过 RA/PPA 闸的 USA/D1 alpha（用户最新要求，区别于 v10/v11 的 4 个同源 earnings+vader）。

策略：从 3 个互不相关的信号族各挖 >=1 个过闸 alpha：
  族A shortinterest : shrt7_combo_utilisation   (shortinterest7, cov0.93 daily spread)
  族B fundamental    : fnd17_ebitda2ev          (fundamental17, cov0.87 daily spread, 价值因子)
  族C risk/volatility: rsk62_risk_backfill_volatility (risk62, cov0.95 daily spread)

每族做 3 个候选：
  - single_nat  : TA_L(F, flip=False)            纯主信号(无共享腿, 最大化去相关)
  - single_flip : TA_L(F, flip=True)             反向主信号(覆盖因子朝向)
  - combo_nat   : 0.5*TA_L(F)+0.5*TA_E(vader)   并联 vader 正交腿(复刻 v10 提升子宇宙 sharpe 打法)

模板：
  TA_L(F,G,flip) = ts_decay_linear(signed_power(subtract(group_rank(F,G),0.5),5),90)   (level 字段)
                   flip 时用 subtract(0.5, group_rank(F,G))
  TA_E(F,G)      = ts_decay_linear(signed_power(subtract(group_rank(vec_avg(F),G),0.5),5),90) (事件字段, 如 vader)

设置：复刻 v10 已验证通过组合 ILLIQUID_MINVOL1M/SLOW_AND_FAST/maxTrade OFF/decay6。

输出：mine_v12_results.json (含每个 alpha 的 sharpe/fitness/sub_universe/checks)。
"""
import json, sys, time
import os
SKILL_DIR = os.environ.get("WQ_ACE_LIB", r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts")
sys.path.insert(0, SKILL_DIR)
import ace_lib

def TA_L(F, G="subindustry", flip=False):
    # 事件型字段需先 vec_avg -> 常规序列; 稀疏(季频fundamental)再 ts_backfill 前向填充
    base = "ts_backfill(vec_avg(%s), 252)" % F
    inner = "subtract(group_rank(%s, %s), 0.5)" % (base, G)
    if flip:
        inner = "subtract(0.5, group_rank(%s, %s))" % (base, G)
    return "ts_decay_linear(signed_power(%s, 5), 90)" % inner

def TA_E(F, G="subindustry"):
    return "ts_decay_linear(signed_power(subtract(group_rank(vec_avg(%s), %s), 0.5), 5), 90)" % (F, G)

VADER = TA_E("headline_sentiment_vader_score")

SET_ILLIQ = {
    "instrumentType": "EQUITY", "region": "USA", "universe": "ILLIQUID_MINVOL1M",
    "delay": 1, "decay": 6, "neutralization": "SLOW_AND_FAST", "truncation": 0.08,
    "pasteurization": "ON", "unitHandling": "VERIFY", "nanHandling": "ON",
    "maxTrade": "OFF", "language": "FASTEXPR", "visualization": False,
    "startDate": "2014-01-01", "endDate": "2023-12-31",
}

# (tag, family, code)
CANDIDATES = [
    # 族A shortinterest
    ("A1_SI_single_nat",  "shortinterest", TA_L("shrt7_combo_utilisation")),
    ("A2_SI_single_flip", "shortinterest", TA_L("shrt7_combo_utilisation", flip=True)),
    ("A3_SI_combo_nat",   "shortinterest", "add(multiply(%s, 0.5), multiply(%s, 0.5))" % (TA_L("shrt7_combo_utilisation"), VADER)),
    # 族B fundamental
    ("B1_FND_single_nat",  "fundamental", TA_L("fnd17_ebitda2ev")),
    ("B2_FND_single_flip", "fundamental", TA_L("fnd17_ebitda2ev", flip=True)),
    ("B3_FND_combo_nat",   "fundamental", "add(multiply(%s, 0.5), multiply(%s, 0.5))" % (TA_L("fnd17_ebitda2ev"), VADER)),
    # 族C risk/volatility
    ("C1_RSK_single_nat",  "risk", TA_L("rsk62_risk_backfill_volatility")),
    ("C2_RSK_single_flip", "risk", TA_L("rsk62_risk_backfill_volatility", flip=True)),
    ("C3_RSK_combo_nat",   "risk", "add(multiply(%s, 0.5), multiply(%s, 0.5))" % (TA_L("rsk62_risk_backfill_volatility"), VADER)),
]

def main():
    s = ace_lib.start_session()
    sim_list = []
    meta = []  # (tag, family, code) parallel to sim_list
    for tag, fam, code in CANDIDATES:
        sim_list.append({"type": "REGULAR", "settings": SET_ILLIQ, "regular": code})
        meta.append((tag, fam, code))
    print(f"=== submitting {len(sim_list)} simulations (parallel multi) ===", flush=True)
    for tag, fam, code in meta:
        print(f"  {tag:18s} {fam:12s} {code[:90]}", flush=True)
    results = ace_lib.simulate_multi_alpha(s, sim_list)
    print("\n=== results ===", flush=True)
    out = []
    for (tag, fam, code), r in zip(meta, results):
        aid = r.get("alpha_id")
        rec = {"tag": tag, "family": fam, "alpha_id": aid, "code": code}
        if aid:
            try:
                j = ace_lib.get_simulation_result_json(s, aid)
                isblock = j.get("is", {})
                rec["sharpe"] = isblock.get("sharpe")
                rec["fitness"] = isblock.get("fitness")
                rec["sub_universe_sharpe"] = isblock.get("subUniverseSharpe")
                rec["yearly_sharpe"] = isblock.get("yearlySharpe")
                # checks
                chk = ace_lib.get_check_submission(s, aid)
                checks = []
                if not chk.empty:
                    for _, row in chk.iterrows():
                        checks.append({"name": row.get("name"), "result": row.get("result"), "msg": str(row.get("msg"))[:120]})
                rec["checks"] = checks
                # ra_failed heuristic: any check result FAIL that is RA-related OR not pass/warn
                ra_fail = any((str(c["result"]).upper()=="FAIL") for c in checks)
                rec["ra_failed"] = ra_fail
                print(f"  {tag:18s} {aid}  sharpe={rec['sharpe']} fit={rec['fitness']} subU={rec['sub_universe_sharpe']} ra_failed={ra_fail}", flush=True)
                for c in checks:
                    print(f"      [{c['result']}] {c['name']}: {c['msg']}", flush=True)
            except Exception as e:
                rec["error"] = str(e)
                print(f"  {tag:18s} {aid}  ERROR getting details: {e}", flush=True)
        else:
            rec["error"] = "simulation_failed"
            print(f"  {tag:18s} NO alpha_id (sim failed)", flush=True)
        out.append(rec)
        time.sleep(1)
    with open("mine_v12_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\n=== DONE -> mine_v12_results.json ===")
    # summary
    print("\n# PASSING (ra_failed==False):")
    for r in out:
        if r.get("ra_failed") is False:
            print(f"  {r['tag']:18s} {r['family']:12s} {r['alpha_id']}  sharpe={r.get('sharpe')} fit={r.get('fitness')} subU={r.get('sub_universe_sharpe')}")

if __name__ == "__main__":
    main()
