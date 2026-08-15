"""mine_v15.py
用账户已验证过闸的 3 个族各自的"专属模板+中性化"做 NEW 变体(换字段/分组, 不与既有账户alpha完全相同):
  族A sentiment   (ILLIQUID_MINVOL1M / STATISTICAL / decay0):
      proven vRvg7NzA: group_rank(ts_zscore(ts_backfill(overall_sentiment_score,252),252), industry)
      NEW A1: industry -> subindustry
  族B fundamental (ILLIQUID_MINVOL1M / INDUSTRY / decay5):
      proven vR0QYmxr: group_rank(ts_ir(winsorize(ts_backfill(vec_avg(fnd110_value),120),std=4),20), industry)
      NEW B1: 换 fnd93_expense_d1_max ;  NEW B2: 换 annual_additional_paid_in_capital
  族C ownership   (TOP3000 / SUBINDUSTRY / decay4):
      proven MPQVZRnk: scale(rank(ts_zscore(subtract(ts_mean(ts_backfill(inst18_fundownershipv2_pre_holding,66),22), ts_mean(ts_backfill(inst18_fundownershipv2_cur_holding,66),22), filter=true),189))) + scale(-rank(ts_zscore(returns,42)))*0.35
      NEW C1: 简化 group_rank(ts_zscore(ts_backfill(inst18_fundownershipv2_cur_holding,252),252), subindustry)
      NEW C2: proven 但窗口 66->120
目标: 3 个互不相关且过 RA/PPA 闸的 alpha (3 族各至少 1 个过闸)。
"""
import json, sys, time
import os
SKILL_DIR = os.environ.get("WQ_ACE_LIB", r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts")
sys.path.insert(0, SKILL_DIR)
import ace_lib

def base_settings(universe, neutralization, decay):
    return {
        "instrumentType":"EQUITY","region":"USA","universe":universe,"delay":1,
        "decay":decay,"neutralization":neutralization,"truncation":0.08,
        "pasteurization":"ON","unitHandling":"VERIFY","nanHandling":"ON",
        "maxTrade":"OFF","language":"FASTEXPR","visualization":False,
        "startDate":"2014-01-01","endDate":"2023-12-31",
    }

# (tag, family, settings, code)
CANDIDATES = [
    ("A1_sent_sub", "sentiment", base_settings("ILLIQUID_MINVOL1M","STATISTICAL",0),
     "group_rank(ts_zscore(ts_backfill(overall_sentiment_score, 252), 252), subindustry)"),
    ("B1_fund_fnd93", "fundamental", base_settings("ILLIQUID_MINVOL1M","INDUSTRY",5),
     "group_rank(ts_ir(winsorize(ts_backfill(vec_avg(fnd93_expense_d1_max), 120), std=4), 20), industry)"),
    ("B2_fund_apic", "fundamental", base_settings("ILLIQUID_MINVOL1M","INDUSTRY",5),
     "group_rank(ts_ir(winsorize(ts_backfill(vec_avg(annual_additional_paid_in_capital), 120), std=4), 20), industry)"),
    ("C1_own_simple", "ownership", base_settings("TOP3000","SUBINDUSTRY",4),
     "group_rank(ts_zscore(ts_backfill(inst18_fundownershipv2_cur_holding, 252), 252), subindustry)"),
    ("C2_own_variant", "ownership", base_settings("TOP3000","SUBINDUSTRY",4),
     "scale(rank(ts_zscore(subtract(ts_mean(ts_backfill(inst18_fundownershipv2_cur_holding, 120), 22), ts_mean(ts_backfill(inst18_fundownershipv2_pre_holding, 120), 22), filter=true), 189))) + scale(-rank(ts_zscore(returns, 42))) * 0.35"),
]

def main():
    s = ace_lib.start_session()
    out = []
    for tag, fam, settings, code in CANDIDATES:
        sim = {"type":"REGULAR","settings":settings,"regular":code}
        rec = {"tag":tag,"family":fam,"code":code}
        print(f"\n=== {tag} ({fam}) ===", flush=True)
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
                rec["error"]="sim_failed"; print("  FAILED", flush=True)
        except Exception as e:
            rec["error"]=str(e); print(f"  EXC {e}", flush=True)
        out.append(rec); time.sleep(2)
    with open("mine_v15_results.json","w") as f: json.dump(out,f,indent=2)
    print("\n=== PASSING (ra_failed==False) ===", flush=True)
    for r in out:
        if r.get("ra_failed") is False:
            print(f"  {r['tag']:14s} {r['family']:12s} {r['alpha_id']} sharpe={r.get('sharpe')} fit={r.get('fitness')} subU={r.get('sub_universe_sharpe')}", flush=True)

if __name__ == "__main__":
    main()
