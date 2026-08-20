"""mine_v13.py
用真实平台字段名(账户已验证 ra_failed:false 的字段)跨 3+ 不同信号族各挖一个 vader-combo alpha。
目标: 3 个互不相关且过 RA/PPA 闸的 alpha。共享 vader 腿仅贡献 ~0.25 相关, 主信号分属不同族 -> 互相低相关。
主字段用事件型包裹 ts_backfill(vec_avg(F),252) (与 earnings 同处理); 若某字段本就是常规序列导致失败, 下一轮改常规包裹。
"""
import json, sys, time
import os
SKILL_DIR = os.environ.get("WQ_ACE_LIB", r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts")
sys.path.insert(0, SKILL_DIR)
import ace_lib

def TA_L(F, G="subindustry"):
    base = "ts_backfill(vec_avg(%s), 252)" % F
    return "ts_decay_linear(signed_power(subtract(group_rank(%s, %s), 0.5), 5), 90)" % (base, G)

def TA_E(F="headline_sentiment_vader_score", G="subindustry"):
    return "ts_decay_linear(signed_power(subtract(group_rank(vec_avg(%s), %s), 0.5), 5), 90)" % (F, G)

VADER = TA_E()

SET_ILLIQ = {
    "instrumentType": "EQUITY", "region": "USA", "universe": "ILLIQUID_MINVOL1M",
    "delay": 1, "decay": 6, "neutralization": "SLOW_AND_FAST", "truncation": 0.08,
    "pasteurization": "ON", "unitHandling": "VERIFY", "nanHandling": "ON",
    "maxTrade": "OFF", "language": "FASTEXPR", "visualization": False,
    "startDate": "2014-01-01", "endDate": "2023-12-31",
}

# (tag, family, main_field)
FIELDS = [
    ("S1_shortpos",   "shortinterest", "aggregate_open_positions_count"),
    ("F1_value",      "fundamental",   "fnd110_value"),
    ("F2_unearned",   "fundamental",   "annual_unearned_revenue"),
    ("O1_own1",       "ownership",     "inst18_fundownershipv2_1"),
    ("O2_own2",       "ownership",     "inst18_fundownershipv2_2"),
    ("O3_own3",       "ownership",     "inst18_fundownershipv2_3"),
    ("M1_sent",       "sentiment",     "overall_sentiment_score"),
]

def main():
    s = ace_lib.start_session()
    sim_list, meta = [], []
    for tag, fam, fld in FIELDS:
        code = "add(multiply(%s, 0.5), multiply(%s, 0.5))" % (TA_L(fld), VADER)
        sim_list.append({"type": "REGULAR", "settings": SET_ILLIQ, "regular": code})
        meta.append((tag, fam, fld, code))
    print("=== submitting %d ===" % len(sim_list), flush=True)
    for t,f,fl,c in meta:
        print(f"  {t:14s} {f:12s} {fl}", flush=True)
    results = ace_lib.simulate_multi_alpha(s, sim_list)
    out = []
    for (tag, fam, fld, code), r in zip(meta, results):
        aid = r.get("alpha_id")
        rec = {"tag": tag, "family": fam, "field": fld, "alpha_id": aid, "code": code}
        if aid:
            try:
                j = ace_lib.get_simulation_result_json(s, aid)
                isb = j.get("is", {})
                rec["sharpe"]=isb.get("sharpe"); rec["fitness"]=isb.get("fitness")
                rec["sub_universe_sharpe"]=isb.get("subUniverseSharpe"); rec["yearly_sharpe"]=isb.get("yearlySharpe")
                chk = ace_lib.get_check_submission(s, aid)
                checks=[]
                if not chk.empty:
                    for _,row in chk.iterrows():
                        checks.append({"name":row.get("name"),"result":str(row.get("result")),"msg":str(row.get("msg"))[:140]})
                rec["checks"]=checks
                rec["ra_failed"]=any(c["result"].upper()=="FAIL" for c in checks)
                print(f"  {tag:14s} {aid} COMPLETE sharpe={rec['sharpe']} fit={rec['fitness']} subU={rec['sub_universe_sharpe']} ra_failed={rec['ra_failed']}", flush=True)
                for c in checks: print(f"      [{c['result']}] {c['name']}: {c['msg']}", flush=True)
            except Exception as e:
                rec["error"]=str(e); print(f"  {tag:14s} {aid} DETAIL ERR {e}", flush=True)
        else:
            rec["error"]="sim_failed"; print(f"  {tag:14s} FAILED (field invalid or compute error)", flush=True)
        out.append(rec); time.sleep(1)
    with open("mine_v13_results.json","w") as f: json.dump(out,f,indent=2)
    print("\n=== PASSING (ra_failed==False) ===", flush=True)
    for r in out:
        if r.get("ra_failed") is False:
            print(f"  {r['tag']:14s} {r['family']:12s} {r['alpha_id']} sharpe={r.get('sharpe')} fit={r.get('fitness')} subU={r.get('sub_universe_sharpe')}", flush=True)

if __name__ == "__main__":
    main()
