# -*- coding: utf-8 -*-
"""KOR insd5 第六批：复刻 shrt38 真结构 —— vec_sum(if_else(方向)) 买卖分量分离。
关键: if_else 必须在 vec_sum 内层（先判每条事件方向，再求和）。
"""
import json, os
REPO = r"D:\coding\traeCN_project\wqb"
E = []
def add(l, e): E.append([l, e])

BUY  = "vec_sum(if_else(greater(insd5_vol_af, insd5_vol_bf), subtract(insd5_vol_af, insd5_vol_bf), 0))"
SELL = "vec_sum(if_else(less(insd5_vol_af, insd5_vol_bf), subtract(insd5_vol_bf, insd5_vol_af), 0))"
BUY_A  = "vec_sum(if_else(greater(insd5_trd_amt, 0), insd5_trd_amt, 0))"
NET    = "subtract(vec_sum(insd5_vol_af), vec_sum(insd5_vol_bf))"

# --- Y 组：买卖分量比（复刻 shrt38 divide(sell,buy)）---
add("Y1_buy_over_sell", f"reverse(group_rank(divide({BUY}, add(1, {SELL})), sector))")
add("Y2_sell_over_buy", f"reverse(group_rank(divide({SELL}, add(1, {BUY})), sector))")
add("Y3_net_over_gross", f"reverse(group_rank(divide({NET}, add(1, add({BUY}, {SELL}))), sector))")
add("Y4_net_over_sell", f"reverse(group_rank(divide({NET}, add(1, {SELL})), sector))")
add("Y5_buy_minus_sell_rank", f"reverse(group_rank(subtract({BUY}, {SELL}), sector))")

# --- Z 组：金额加权方向 ---
add("Z1_amt_net", f"reverse(group_rank(divide(vec_sum(multiply(insd5_trd_amt, sign(subtract(insd5_vol_af, insd5_vol_bf)))), add(1, vec_sum(insd5_trd_amt))), sector))")
add("Z2_amt_abs", f"reverse(group_rank(divide({BUY_A}, add(1, vec_sum(insd5_trd_amt))), sector))")

# --- AA 组：方向分离 + 归一（比例化）---
add("AA1_buy_ratio_bf", f"reverse(group_rank(divide({BUY}, add(1, vec_sum(insd5_vol_bf))), sector))")
add("AA2_net_ratio_bf", f"reverse(group_rank(divide({NET}, add(1, vec_sum(insd5_vol_bf))), sector))")
add("AA3_buy_sell_ratio_tsmean", f"reverse(group_rank(ts_mean(divide({BUY}, add(1, {SELL})), 22), sector))")

# --- AB 组：raw 版本（不 rank，让中性化处理）---
add("AB1_raw_buy_over_sell", f"reverse(divide({BUY}, add(1, {SELL})))")
add("AB2_raw_net_over_gross", f"reverse(divide({NET}, add(1, add({BUY}, {SELL}))))")

# --- AC 组：用 fa_tr/fb_tr 做方向（比例字段）---
add("AC1_fa_fb_split", "reverse(group_rank(divide(vec_sum(if_else(greater(insd5_fa_tr, insd5_fb_tr), subtract(insd5_fa_tr, insd5_fb_tr), 0)), add(0.001, vec_sum(if_else(less(insd5_fa_tr, insd5_fb_tr), subtract(insd5_fb_tr, insd5_fa_tr), 0)))), sector))")
add("AC2_ghc_split", "reverse(group_rank(divide(vec_sum(if_else(greater(insd5_ghc_tr, 0), insd5_ghc_tr, 0)), add(0.001, vec_sum(if_else(less(insd5_ghc_tr, 0), multiply(-1, insd5_ghc_tr), 0)))), sector))")

out = os.path.join(REPO, "tracking/reference/exprs_kor_insd5_w6.json")
json.dump(E, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"wrote {len(E)} -> {out}")
for l, e in E: print(f"  {l:24s} {e[:120]}")
