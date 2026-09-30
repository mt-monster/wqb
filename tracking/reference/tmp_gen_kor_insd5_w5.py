# -*- coding: utf-8 -*-
"""KOR insd5 第五批：验证 reverse 算子 + 用 reverse 重写取反 + 推 S。
求证:
 ① reverse(group_rank(x)) == multiply(-1, group_rank(x)) ?（预期等价，都= -x）
 ② reverse 在 rank 内 vs 外的差异
③ 推 S 旋钮: decay / 分组轴 / signed_power / 双窗 / winsorize / zscore 组合
"""
import json, os
REPO = r"D:\coding\traeCN_project\wqb"
E = []
def add(l, e): E.append([l, e])

BASE = "divide(vec_sum(insd5_trd_amt), add(1, vec_sum(insd5_source_data)))"
BASE2 = "ts_decay_linear(divide(vec_sum(insd5_trd_amt), add(1, vec_sum(insd5_source_data))), 10)"

# --- U 组：reverse 算子验证（对照 P2/P1）---
add("U1_reverse_out", f"reverse(group_rank({BASE}, sector))")
add("U2_reverse_out2", f"reverse(group_rank({BASE2}, sector))")
add("U3_reverse_in", f"group_rank(reverse({BASE}), sector)")            # 预期无效
add("U4_reverse_raw", f"reverse({BASE})")                              # 裸取负
add("U5_reverse_sub", f"reverse(subtract(0.5, group_rank({BASE}, sector)))")

# --- V 组：推 S —— decay 扫描（P4 结构 + 不同 decay_linear 窗口）---
for w in [5, 20, 40, 66]:
    add(f"V_decay{w}", f"subtract(0.5, group_rank(ts_decay_linear({BASE}, {w}), sector))")
add("V_tsmean22", f"subtract(0.5, group_rank(ts_mean({BASE}, 22), sector))")
add("V_tsmean5", f"subtract(0.5, group_rank(ts_mean({BASE}, 5), sector))")

# --- W 组：换分组轴 ---
add("W_subind", f"subtract(0.5, group_rank({BASE2}, subindustry))")
add("W_industry", f"subtract(0.5, group_rank({BASE2}, industry))")
add("W_market", f"subtract(0.5, group_rank({BASE2}, market))")
add("W_zscore_grp", f"group_zscore(reverse({BASE2}), sector)")

# --- X 组：signed_power / winsorize 压尾 ---
add("X_sp05", f"signed_power(subtract(0.5, group_rank({BASE2}, sector)), 0.5)")
add("X_winsor", f"winsorize(subtract(0.5, group_rank({BASE2}, sector)), std=4)")

out = os.path.join(REPO, "tracking/reference/exprs_kor_insd5_w5.json")
json.dump(E, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"wrote {len(E)} -> {out}")
for l, e in E: print(f"  {l:16s} {e[:120]}")
