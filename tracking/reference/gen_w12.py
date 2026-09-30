# -*- coding: utf-8 -*-
"""w12: IND/PV 降 TO 探针。

核心信号: corr_last_trade_price_with_volume (ds=1358, IND/D1/PV)
目标: 保留 "反转" 语义 (取负) 与 低 prod, 同时把 TO 从 0.81 压到 <0.4。

合规约束: 只用单信号 + 时序/截面结构化 (hump/ts_decay_linear/长窗), 禁止混腿。
"""
import json, os
REPO = r"D:\coding\traeCN_project\wqb"

CORE = "corr_last_trade_price_with_volume"

# --- A 组: 长窗 ts_rank + hump (hump 专治换手) ---
A = [
    ("A1_rk22_hump", f"rank(multiply(-1, hump(ts_rank({CORE}, 22), 0.02)))"),
    ("A2_rk66", f"rank(multiply(-1, ts_rank({CORE}, 66)))"),
    ("A3_rk126", f"rank(multiply(-1, ts_rank({CORE}, 126)))"),
    ("A4_rk252", f"rank(multiply(-1, ts_rank({CORE}, 252)))"),
    ("A5_rk252_hump", f"rank(multiply(-1, hump(ts_rank({CORE}, 252), 0.02)))"),
    ("A6_rk504", f"rank(multiply(-1, ts_rank({CORE}, 504)))"),
]

# --- B 组: ts_rank + 外层 ts_decay_linear ---
B = [
    ("B1_rk22_dec5", f"rank(multiply(-1, ts_decay_linear(ts_rank({CORE}, 22), 5)))"),
    ("B2_rk22_dec10", f"rank(multiply(-1, ts_decay_linear(ts_rank({CORE}, 22), 10)))"),
    ("B3_rk22_dec22", f"rank(multiply(-1, ts_decay_linear(ts_rank({CORE}, 22), 22)))"),
    ("B4_rk66_dec10", f"rank(multiply(-1, ts_decay_linear(ts_rank({CORE}, 66), 10)))"),
    ("B5_rk126_dec10", f"rank(multiply(-1, ts_decay_linear(ts_rank({CORE}, 126), 10)))"),
    ("B6_rk252_dec10", f"rank(multiply(-1, ts_decay_linear(ts_rank({CORE}, 252), 10)))"),
]

# --- C 组: hump / ts_mean 直接压换手 (族内 ts_mean5 已验证 TO~0.35) ---
C = [
    ("C1_mean5_hump", f"rank(multiply(-1, hump(ts_mean({CORE}, 5), 0.01)))"),
    ("C2_mean5", f"rank(multiply(-1, ts_mean({CORE}, 5)))"),
    ("C3_mean10_hump", f"rank(multiply(-1, hump(ts_mean({CORE}, 10), 0.01)))"),
    ("C4_zscore66_hump", f"rank(multiply(-1, hump(ts_zscore({CORE}, 66), 0.01)))"),
    ("C5_zscore252_hump", f"rank(multiply(-1, hump(ts_zscore({CORE}, 252), 0.01)))"),
    ("C6_tsrank22_signedpower", f"rank(multiply(-1, signed_power(subtract(0.5, ts_rank({CORE}, 22)), 0.5)))"),
]

EXPRS = [{"label": l, "expression": e} for l, e in (A + B + C)]

out = os.path.join(REPO, "tracking", "reference", "exprs_ind_pv_w12.json")
json.dump(EXPRS, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"wrote {len(EXPRS)} exprs -> {out}")
for x in EXPRS:
    print(f"  {x['label']:28} {x['expression']}")
