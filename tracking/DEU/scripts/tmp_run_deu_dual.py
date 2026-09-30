# -*- coding: utf-8 -*-
"""DEU-DUAL v1 —— DEU 双塔点亮挖掘（2026-09-29）。

目标：点亮 DEU/D1 的两座"只差 1 颗"的未亮塔：
  塔1 Short Interest（现 2 颗，缺 1）→ 数据源 `shortinterest3`（Securities Lending Files，25 VECTOR 字段）
  塔2 Other（现 2 颗，缺 1）→ 数据源 `other532`（Specific Returns，8 MATRIX 字段）

方法：直接迁移 KOR `shortinterest38` 已实证配方（SI15/17 三重印证）：
  - **分组轴决定 prod**：subindustry(0.57) << industry(0.69) << sector(0.77)
  - **推荐结构**：hump(group_rank(ts_decay_linear(<ratio>,500), <轴>), hump=0.0025)
  - 设置：neutralization=SLOW_AND_FAST + truncation=0.02（绕 PURE_POWER_POOL_THEME + CW PASS）

断点续跑：checkpoint 记 progress_id，跳过已完成批。
用法: python tmp_run_deu_dual.py            # 续跑
      DEU_FRESH=1 python tmp_run_deu_dual.py  # 全新
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

CKPT = os.path.join(REPO, "tracking/DEU/candidates/wave_DEUDUAL_checkpoint.json")
FRESH = os.environ.get("DEU_FRESH") == "1"

NU = "SLOW_AND_FAST"
TRUNC = 0.02

# ---------- 塔1：Short Interest（shortinterest3 VECTOR 比率族）----------
SI3_VEC = [
    "mean_loan_rate", "max_loan_rate", "min_loan_rate",
    "loan_rate_volatility", "loaned_market_value_usd",
    "loaned_share_count", "average_loan_duration_days",
    "transaction_count", "shrt3_bar",
]
# 比率对（经济含义：供需/成本压力）
SI3_PAIRS = [
    ("mean_loan_rate", "max_loan_rate"),          # 平均/最高借券费率 = 费率结构
    ("loaned_market_value_usd", "loaned_share_count"),  # 市值/股数 = 隐含均价
    ("max_loan_rate", "min_loan_rate"),           # 费率离散度
    ("loaned_share_count", "average_loan_duration_days"),
    ("loan_rate_volatility", "mean_loan_rate"),
]


def si3_exprs():
    exprs = []
    for a, b in SI3_PAIRS:
        rs = f"divide(vec_sum({a}), add(vec_sum({b}), 0.0001))"
        for axis in ("subindustry", "industry"):
            exprs.append((f"T1_{a[:12]}_{b[:12]}_{axis[:4]}",
                          f"hump(group_rank(ts_decay_linear({rs}, 500), {axis}), hump=0.0025)"))
    # 单字段等级
    for f in ("shrt3_bar", "mean_loan_rate", "loaned_share_count"):
        exprs.append((f"T1_lvl_{f[:12]}",
                      f"hump(group_rank(ts_decay_linear(vec_avg({f}), 500), subindustry), hump=0.0025)"))
    return exprs


# ---------- 塔2：Other（other532 特质收益族）----------
O532 = [
    "oth532_global_daily_specificreturn",
    "oth532_emerging_daily_specificreturn",
    "oth532_global_monthly_specificreturn",
    "oth532_emerging_monthly_specificreturn",
    "idiosyncratic_return_eue_daily",
    "idiosyncratic_return_eue_monthly",
]


def o532_exprs():
    exprs = []
    # 反转：负特质收益 → 均值回复
    for f in O532:
        exprs.append((f"T2_rev_{f[:20]}",
                      f"hump(group_rank(ts_decay_linear(multiply(-1, {f}), 20), subindustry), hump=0.0025)"))
        exprs.append((f"T2_rank_{f[:20]}",
                      f"hump(group_rank(ts_decay_linear(ts_rank({f}, 250), 20), industry), hump=0.0025)"))
    # 日 vs 月 特质收益差（动量/反转结构）
    exprs.append(("T2_dm_gap",
                  "hump(group_rank(ts_decay_linear(subtract(oth532_global_daily_specificreturn,"
                  " oth532_global_monthly_specificreturn), 20), subindustry), hump=0.0025)"))
    # 全球 vs 新兴 特质收益差
    exprs.append(("T2_ge_gap",
                  "hump(group_rank(ts_decay_linear(subtract(oth532_global_daily_specificreturn,"
                  " oth532_emerging_daily_specificreturn), 20), industry), hump=0.0025)"))
    return exprs


SPECS = [
    ("T1_SI3", "shortinterest3", si3_exprs()),
    ("T2_O532", "other532", o532_exprs()),
]


async def main():
    ck = {"done_batches": [], "batches": []}
    if os.path.exists(CKPT) and not FRESH:
        ck = json.load(open(CKPT, encoding="utf-8"))
    done = {b["progress_id"] for b in ck.get("done_batches", []) if b.get("progress_id")}

    from brain_api import brain_client
    from tools_sim import create_multi_simulation
    await brain_client.ensure_authenticated()

    for gname, ds, exprs in SPECS:
        print(f"\n=== {gname} ({ds}) {len(exprs)} exprs, stride=8 ===")
        for i in range(0, len(exprs), 8):
            chunk = exprs[i:i + 8]
            if len(chunk) < 2:
                break
            label = f"{gname}_{i:02d}"
            if any(b.get("label") == label for b in ck.get("done_batches", [])):
                print(f"  {label} skip(ckpt)"); continue
            r = await create_multi_simulation(
                [c[1] for c in chunk], region="DEU", universe="TOP500", delay=1,
                decay=30, neutralization=NU, truncation=TRUNC,
                nan_handling="ON", test_period="P0Y0M")
            if isinstance(r, dict) and r.get("error"):
                print(f"  {label} ERR {json.dumps(r, ensure_ascii=False)[:200]}"); continue
            pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
            print(f"  {label} pid={pid} n={len(chunk)}")
            ck["done_batches"].append({"label": label, "progress_id": pid, "dataset": ds,
                                       "ids": [c[0] for c in chunk], "exprs": [c[1] for c in chunk]})
            json.dump(ck, open(CKPT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            await asyncio.sleep(1)

    print("\nSAVED", CKPT)
    print("total batches:", len(ck["done_batches"]))


asyncio.run(main())
