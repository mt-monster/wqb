# -*- coding: utf-8 -*-
"""DEU-DUAL v2 —— 第二轮（Mode B：换结构，非调参）。

首轮结论：
  - other532 族 14 条全弱（最强 S=1.07，用 idiosyncratic_return_eue_monthly 反转）→ **月度特质收益反转方向对，但需换结构**
  - shortinterest3 首轮 VECTOR 比率族待回测

v2 结构变更（合规：换概念/换算子几何/换轴，不做双腿加权）：
  T2' Other 塔：
    a) 多窗 ts_rank 差分（短-长特质收益动量）
    b) group 轴换 sector / market
    c) ts_decay_linear 窗 60/120/250
    d) 特质收益波动率（ts_std_dev）→ 低波异象
  T1' SI 塔（若首轮败）：
    a) shrt3_bar 借券需求等级的 ts_delta / ts_zscore
    b) loaned_market_value 比值 + 换轴
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
CKPT = os.path.join(REPO, "tracking/DEU/candidates/wave_DEUDUAL2_checkpoint.json")
NU, TRUNC = "SLOW_AND_FAST", 0.02

GD = "oth532_global_daily_specificreturn"
GM = "oth532_global_monthly_specificreturn"
ED = "oth532_emerging_daily_specificreturn"
IDM = "idiosyncratic_return_eue_monthly"


def t2_exprs():
    e = []
    # a) 短-长 ts_rank 差分（动量结构，单一价差信号）
    for f, tag in [(GD, "gd"), (IDM, "idm"), (ED, "ed")]:
        e.append((f"T2b_sl_{tag}",
                  f"hump(group_rank(ts_decay_linear(subtract(ts_rank({f}, 60), ts_rank({f}, 250)), 20), subindustry), hump=0.0025)"))
        e.append((f"T2b_ml_{tag}",
                  f"hump(group_rank(ts_decay_linear(subtract(ts_rank({f}, 250), ts_rank({f}, 60)), 20), industry), hump=0.0025)"))
    # b) 换轴 sector / market
    e.append(("T2b_sec",
              f"hump(group_rank(ts_decay_linear(multiply(-1, {IDM}), 20), sector), hump=0.0025)"))
    e.append(("T2b_mkt",
              f"hump(group_rank(ts_decay_linear(multiply(-1, {IDM}), 20), market), hump=0.0025)"))
    # c) 更长 decay 窗
    e.append(("T2b_d120",
              f"hump(group_rank(ts_decay_linear(multiply(-1, {IDM}), 120), subindustry), hump=0.0025)"))
    e.append(("T2b_d250",
              f"hump(group_rank(ts_decay_linear(multiply(-1, {IDM}), 250), subindustry), hump=0.0025)"))
    # d) 特质收益波动率（低波异象）
    e.append(("T2b_vol",
              f"hump(group_rank(ts_decay_linear(multiply(-1, ts_std_dev({GD}, 60)), 20), subindustry), hump=0.0025)"))
    # e) 全局日/月特质收益 ts_zscore 差
    e.append(("T2b_zgap",
              f"hump(group_rank(ts_decay_linear(subtract(ts_zscore({GD}, 60), ts_zscore({GM}, 250)), 20), subindustry), hump=0.0025)"))
    return e


def t1_exprs():
    e = []
    # a) shrt3_bar 借券需求等级：变化率 / 标准化
    e.append(("T1b_bar_delta",
              "hump(group_rank(ts_decay_linear(vec_avg(ts_delta(shrt3_bar, 20)), 30), subindustry), hump=0.0025)"))
    e.append(("T1b_bar_z",
              "hump(group_rank(ts_decay_linear(vec_avg(ts_zscore(shrt3_bar, 250)), 30), industry), hump=0.0025)"))
    # b) 借券市值/股数 隐含均价 比值 + 换轴
    rs = "divide(vec_sum(loaned_market_value_usd), add(vec_sum(loaned_share_count), 0.0001))"
    e.append(("T1b_px_sub",
              f"hump(group_rank(ts_decay_linear({rs}, 500), subindustry), hump=0.0025)"))
    e.append(("T1b_px_ind",
              f"hump(group_rank(ts_decay_linear({rs}, 500), industry), hump=0.0025)"))
    # c) 借券费率波动率（风险溢价）
    e.append(("T1b_volrate",
              "hump(group_rank(ts_decay_linear(vec_avg(loan_rate_volatility), 250), subindustry), hump=0.0025)"))
    # d) 借券量变化（拥挤度）
    e.append(("T1b_cnt_delta",
              "hump(group_rank(ts_decay_linear(vec_sum(ts_delta(loaned_share_count, 20)), 30), industry), hump=0.0025)"))
    return e


SPECS = [("T1b_SI3", "shortinterest3", t1_exprs()), ("T2b_O532", "other532", t2_exprs())]


async def main():
    ck = {"done_batches": []}
    if os.path.exists(CKPT) and os.environ.get("DEU2_FRESH") != "1":
        ck = json.load(open(CKPT, encoding="utf-8"))
    from brain_api import brain_client
    from tools_sim import create_multi_simulation
    await brain_client.ensure_authenticated()
    for gname, ds, exprs in SPECS:
        print(f"\n=== {gname} ({ds}) {len(exprs)} exprs ===")
        for i in range(0, len(exprs), 8):
            chunk = exprs[i:i + 8]
            if len(chunk) < 2:
                break
            label = f"{gname}_{i:02d}"
            if any(b.get("label") == label for b in ck["done_batches"]):
                print(f"  {label} skip(ckpt)"); continue
            r = await create_multi_simulation([c[1] for c in chunk], region="DEU", universe="TOP500",
                                              delay=1, decay=30, neutralization=NU, truncation=TRUNC,
                                              nan_handling="ON", test_period="P0Y0M")
            if isinstance(r, dict) and r.get("error"):
                print(f"  {label} ERR {json.dumps(r,ensure_ascii=False)[:200]}"); continue
            pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
            print(f"  {label} pid={pid}")
            ck["done_batches"].append({"label": label, "progress_id": pid, "dataset": ds,
                                       "ids": [c[0] for c in chunk], "exprs": [c[1] for c in chunk]})
            json.dump(ck, open(CKPT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            await asyncio.sleep(1)
    print("\nSAVED", CKPT, "n=", len(ck["done_batches"]))


asyncio.run(main())
