"""mine_v14.py
用账户已验证的真实字段名(从 get_user_alphas dump 提取), 跨 3 个互不相关信号族各挖 alpha:
  族1 shortinterest/positions : aggregate_open_positions_count
  族2 fundamental value       : fnd110_value
  族3 ownership               : inst18_fundownershipv2_cur_holding
每族测 single(无共享腿, 最大化去相关) 与 combo(0.5*main+0.5*vader, 复刻 v10 提升子宇宙 sharpe 打法) 两个版本。
独立单跑(simulate_single_alpha)避免批量取消。
验证: get_simulation_result_json(sharpe/fitness/subU) + get_check_submission(ra_failed)。
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

CANDIDATES = [
    ("S_single", "shortinterest", "aggregate_open_positions_count", TA_L("aggregate_open_positions_count")),
    ("S_combo",  "shortinterest", "aggregate_open_positions_count", "add(multiply(%s,0.5),multiply(%s,0.5))"%(TA_L("aggregate_open_positions_count"),VADER)),
    ("F_single", "fundamental",   "fnd110_value", TA_L("fnd110_value")),
    ("F_combo",  "fundamental",   "fnd110_value", "add(multiply(%s,0.5),multiply(%s,0.5))"%(TA_L("fnd110_value"),VADER)),
    ("O_single", "ownership",     "inst18_fundownershipv2_cur_holding", TA_L("inst18_fundownershipv2_cur_holding")),
    ("O_combo",  "ownership",     "inst18_fundownershipv2_cur_holding", "add(multiply(%s,0.5),multiply(%s,0.5))"%(TA_L("inst18_fundownershipv2_cur_holding"),VADER)),
]

def main():
    s = ace_lib.start_session()
    out = []
    for tag, fam, fld, code in CANDIDATES:
        sim = {"type":"REGULAR","settings":SET_ILLIQ,"regular":code}
        rec = {"tag":tag,"family":fam,"field":fld,"code":code}
        print(f"\n=== {tag} ({fam}/{fld}) ===", flush=True)
        try:
            r = ace_lib.simulate_single_alpha(s, sim)
            aid = r.get("alpha_id")
            rec["alpha_id"]=aid
            if aid:
                j = ace_lib.get_simulation_result_json(s, aid)
                isb=j.get("is",{})
                rec["sharpe"]=isb.get("sharpe"); rec["fitness"]=isb.get("fitness")
                rec["sub_universe_sharpe"]=isb.get("subUniverseSharpe"); rec["yearly_sharpe"]=isb.get("yearlySharpe")
                chk=ace_lib.get_check_submission(s,aid)
                checks=[]
                if not chk.empty:
                    for _,row in chk.iterrows():
                        checks.append({"name":row.get("name"),"result":str(row.get("result")),"msg":str(row.get("msg"))[:140]})
                rec["checks"]=checks
                rec["ra_failed"]=any(c["result"].upper()=="FAIL" for c in checks)
                print(f"  {aid} sharpe={rec['sharpe']} fit={rec['fitness']} subU={rec['sub_universe_sharpe']} ra_failed={rec['ra_failed']}", flush=True)
                for c in checks: print(f"    [{c['result']}] {c['name']}: {c['msg']}", flush=True)
            else:
                rec["error"]="sim_failed"; print("  FAILED (invalid field/compute)", flush=True)
        except Exception as e:
            rec["error"]=str(e); print(f"  EXC {e}", flush=True)
        out.append(rec); time.sleep(2)
    with open("mine_v14_results.json","w") as f: json.dump(out,f,indent=2)
    print("\n=== PASSING (ra_failed==False) ===", flush=True)
    for r in out:
        if r.get("ra_failed") is False:
            print(f"  {r['tag']:10s} {r['family']:12s} {r['alpha_id']} sharpe={r.get('sharpe')} fit={r.get('fitness')} subU={r.get('sub_universe_sharpe')}", flush=True)

if __name__ == "__main__":
    main()
