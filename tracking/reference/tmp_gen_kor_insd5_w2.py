# -*- coding: utf-8 -*-
"""KOR insd5 第二批：聚焦"净买入 vs 净卖出"分离（最像 shrt38 divide(sell,buy)）。
核心：内部人交易是离散事件流，ghc_tr 有正负。按符号拆分再比率化。
"""
import json, os
REPO = r"D:\coding\traeCN_project\wqb"
E = []
def add(l, e): E.append([l, e])

# --- 组 F：显式买卖分离（if_else 正负拆）→ 比率 ---
# ghc_tr > 0 = 增持(买入)，< 0 = 减持(卖出)
add("F1_buy_over_sell",
    "group_rank(divide(ts_sum(if_else(greater(vec_sum(insd5_ghc_tr), 0), vec_sum(insd5_ghc_tr), 0), 22), "
    "add(0.001, ts_sum(if_else(less(vec_sum(insd5_ghc_tr), 0), multiply(-1, vec_sum(insd5_ghc_tr)), 0), 22))), sector)")
add("F2_sell_over_buy",
    "group_rank(divide(ts_sum(if_else(less(vec_sum(insd5_ghc_tr), 0), multiply(-1, vec_sum(insd5_ghc_tr)), 0), 22), "
    "add(0.001, ts_sum(if_else(greater(vec_sum(insd5_ghc_tr), 0), vec_sum(insd5_ghc_tr), 0), 22))), sector)")
add("F3_net_over_gross",
    "group_rank(divide(ts_sum(vec_sum(insd5_ghc_tr), 22), "
    "add(0.001, ts_sum(abs(vec_sum(insd5_ghc_tr)), 22))), sector)")
add("F4_gross_signed",
    "group_rank(ts_sum(vec_sum(insd5_ghc_tr), 22), sector)")

# --- 组 G：vol_af/vol_bf 显式买卖分离 ---
add("G1_af_minus_bf_norm",
    "group_rank(divide(subtract(vec_sum(insd5_vol_af), vec_sum(insd5_vol_bf)), "
    "add(1, vec_sum(insd5_vol_bf))), sector)")
add("G2_afbf_delta_sum",
    "group_rank(ts_sum(divide(subtract(vec_sum(insd5_vol_af), vec_sum(insd5_vol_bf)), add(1, abs(vec_sum(insd5_vol_bf)))), 22), sector)")

# --- 组 H：trd_amt 净额（金额加权） ---
add("H1_amt_pos_ratio",
    "group_rank(divide(vec_sum(insd5_trd_amt), add(1, vec_sum(insd5_source_data))), sector)")
add("H2_amt_tsmean",
    "hump(group_rank(ts_decay_linear(divide(vec_sum(insd5_trd_amt), add(1, vec_sum(insd5_source_data))), 10), sector), hump=0.003)")
add("H3_amt_zscore",
    "group_rank(ts_zscore(divide(vec_sum(insd5_trd_amt), add(1, vec_sum(insd5_source_data))), 252), sector)")

# --- 组 I：直接把 shrt38 的结构搬到 insd5（保底复刻） ---
add("I1_ratio_like_shrt38",
    "hump(group_rank(divide(vec_sum(insd5_vol_af), add(1, vec_sum(insd5_vol_bf))), sector), hump=0.003)")
add("I2_ratio_decay_like_shrt38",
    "hump(group_rank(ts_decay_linear(divide(vec_sum(insd5_vol_af), add(1, vec_sum(insd5_vol_bf))), 20), sector), hump=0.003)")
add("I3_sharecount_ratio",
    "hump(group_rank(divide(vec_sum(insd5_data), add(1, vec_sum(insd5_vol_bf))), sector), hump=0.003)")

# --- 组 J：权益比例变化 ghc + fa_tr ---
add("J1_fa_tr_ratio",
    "hump(group_rank(divide(vec_sum(insd5_fa_tr), add(0.001, vec_sum(insd5_fb_tr))), sector), hump=0.003)")
add("J2_ghc_times_amt",
    "group_rank(ts_sum(multiply(vec_sum(insd5_ghc_tr), vec_sum(insd5_unt_val)), 22), sector)")

out = os.path.join(REPO, "tracking/reference/exprs_kor_insd5_w2.json")
json.dump(E, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"wrote {len(E)} -> {out}")
for l, e in E: print(f"  {l:24s} {e[:110]}")
