import os
"""mine_corr.py
计算一组 alpha 的日频 PnL 两两相关系数, 用于验证"互不相关"。
用法: python mine_corr.py id1 id2 id3 ...
"""
import sys, json
import pandas as pd
import numpy as np
SKILL_DIR = os.environ.get("WQ_ACE_LIB", r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts")
sys.path.insert(0, SKILL_DIR)
import ace_lib

def main():
    ids = sys.argv[1:]
    if not ids:
        # 默认候选集: 我的新 earnings+vader + 账户既有其他族
        ids = ["YPv8gzdv", "vRvg7NzA", "vR0QYmxr", "MPQVZRnk", "P0GxGQxM", "rK2922Ra", "YPv87K0M"]
    s = ace_lib.start_session()
    series = {}
    for aid in ids:
        try:
            df = ace_lib.get_alpha_daily_pnl(s, aid)
            col = [c for c in df.columns if "pnl" in c.lower()][0]
            s2 = df[col].copy()
            s2.index = pd.to_datetime(s2.index)
            series[aid] = s2
            print(f"  got {aid}: {len(df)} rows", flush=True)
        except Exception as e:
            print(f"  {aid} ERR {e}", flush=True)
    if len(series) < 2:
        print("not enough series"); return
    merged = pd.DataFrame(series).dropna()
    print("\nPairwise correlation (daily PnL):")
    corr = merged.corr()
    print(corr.round(3).to_string())
    # 也打印 sharpe/fitness
    print("\nMetrics:")
    for aid in merged.columns:
        try:
            j = ace_lib.get_simulation_result_json(s, aid)
            isb = j.get("is", {})
            print(f"  {aid}: sharpe={isb.get('sharpe')} fitness={isb.get('fitness')}")
        except Exception as e:
            print(f"  {aid}: metric ERR {e}")

if __name__ == "__main__":
    main()
