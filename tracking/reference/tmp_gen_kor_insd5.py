# -*- coding: utf-8 -*-
"""KOR insiders5 表达式生成：复刻 shrt38 成功三共性
 ① VECTOR 事件流 → vec_sum 聚合
 ② 比率结构 divide(...)（非价差）
 ③ group_rank(..., sector) / hump 削峰
核心字段:
 insd5_ghc_tr   = Change in ownership % (from transaction)  ← 最直接的交易方向
 insd5_vol_bf   = 交易前持股数
 insd5_vol_af   = 交易后持股数
 insd5_trd_amt  = 交易金额 (KRW)
 insd5_fb_tr    = 交易前持股比例
 insd5_fa_tr    = 交易后持股比例
 insd5_trsy_ratio = 库存股占比
 insd5_tnc      = 特殊方数量
"""
import json, os
REPO = r"D:\coding\traeCN_project\wqb"

E = []
def add(lab, expr): E.append([lab, expr])

# --- A 组：ghc_tr（持股变化率）净信号，比率化（复刻 shrt38 divide 结构） ---
add("A1_ghc_rank", "group_rank(ts_backfill(vec_sum(insd5_ghc_tr), 22), sector)")
add("A2_ghc_hump", "hump(group_rank(ts_backfill(vec_sum(insd5_ghc_tr), 22), sector), hump=0.003)")
add("A3_ghc_decay", "hump(group_rank(ts_decay_linear(ts_backfill(vec_sum(insd5_ghc_tr), 22), 10), sector), hump=0.003)")
add("A4_ghc_zscore1260", "group_rank(ts_mean(ts_zscore(ts_backfill(vec_sum(insd5_ghc_tr), 22), 1260), 5), sector)")
add("A5_ghc_meandiff", "group_rank(ts_mean(vec_sum(insd5_ghc_tr), 22), sector)")
add("A6_ghc_neg", "group_rank(ts_backfill(vec_avg(insd5_ghc_tr), 22), sector)")

# --- B 组：vol_af/vol_bf 比率（复刻 divide(sell,buy)） ---
add("B1_af_over_bf", "group_rank(divide(vec_sum(insd5_vol_af), vec_sum(insd5_vol_bf)), sector)")
add("B2_af_over_bf_hump", "hump(group_rank(divide(vec_sum(insd5_vol_af), vec_sum(insd5_vol_bf)), sector), hump=0.003)")
add("B3_bf_over_af", "group_rank(divide(vec_sum(insd5_vol_bf), vec_sum(insd5_vol_af)), sector)")
add("B4_afbf_ratio_decay", "hump(group_rank(ts_decay_linear(divide(vec_sum(insd5_vol_af), vec_sum(insd5_vol_bf)), 10), sector), hump=0.003)")

# --- C 组：fb_tr/fa_tr 持股比例比率 ---
add("C1_fa_over_fb", "group_rank(divide(vec_sum(insd5_fa_tr), vec_sum(insd5_fb_tr)), sector)")
add("C2_fa_bf_diff", "group_rank(subtract(vec_sum(insd5_fa_tr), vec_sum(insd5_fb_tr)), sector)")

# --- D 组：trd_amt 净额比率 ---
add("D1_amt_ratio", "group_rank(divide(vec_sum(insd5_trd_amt), vec_sum(insd5_source_data)), sector)")
add("D2_amt_avg", "group_rank(ts_backfill(vec_avg(insd5_trd_amt), 22), sector)")

# --- E 组：trsy_ratio / tnc ---
add("E1_trsy_ratio", "group_rank(ts_backfill(vec_avg(insd5_trsy_ratio), 22), sector)")
add("E2_tnc", "group_rank(ts_backfill(vec_avg(insd5_tnc), 22), sector)")

out = os.path.join(REPO, "tracking/reference/exprs_kor_insd5_w1.json")
json.dump(E, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"wrote {len(E)} exprs -> {out}")
for l, e in E: print(f"  {l:22s} {e[:110]}")
