# -*- coding: utf-8 -*-
"""w14: KOR/Risk 塔 (risk70, Multi-Factor Model 96字段) 单信号探针。

经济逻辑: 风险模型因子载荷 => 因子动量/均值回归。
高价值字段(用户多=有信号): earnyild(566)/anlystsn(606)/btop(242)/dsrt(241)/
                          resvol(225)/srtindcnt(217)/momentum(120)/ltrevrsl(121)
合规: 单信号 + ts_rank/ts_zscore/ts_delta 结构化, 禁止混腿。
"""
import json, os
REPO = r"D:\coding\traeCN_project\wqb"

E = []
# 核心字段（按 userCount 高→低挑 9 个）
F = [
    ("earnyild", "rsk70_mfm2_asetrd_earnyild"),
    ("anlystsn", "rsk70_mfm2_asetrd_anlystsn"),
    ("btop", "rsk70_mfm2_asetrd_btop"),
    ("dsrt", "rsk70_mfm2_asetrd_dsrt"),
    ("resvol", "rsk70_mfm2_asetrd_resvol"),
    ("srtindcnt", "rsk70_mfm2_asetrd_srtindcnt"),
    ("momentum", "rsk70_mfm2_asetrd_momentum"),
    ("ltrevrsl", "rsk70_mfm2_asetrd_ltrevrsl"),
    ("strevrsl", "rsk70_mfm2_asetrd_strevrsl"),
]

# 对 3 个最优字段做几何扫描
for name, fld in F[:3]:
    E += [
        (f"A_{name}_rank252", f"rank(multiply(-1, ts_rank({fld}, 252)))"),
        (f"B_{name}_z252", f"rank(multiply(-1, ts_zscore({fld}, 252)))"),
        (f"C_{name}_z66", f"rank(multiply(-1, ts_zscore({fld}, 66)))"),
        (f"D_{name}_delta22", f"rank(multiply(-1, ts_delta({fld}, 22)))"),
        (f"E_{name}_grpsubind", f"group_rank(multiply(-1, {fld}), subindustry)"),
    ]
# 其余 6 个字段各 1 个最优几何
for name, fld in F[3:]:
    E += [
        (f"F_{name}_rank252", f"rank(multiply(-1, ts_rank({fld}, 252)))"),
        (f"G_{name}_grpsubind", f"group_rank(multiply(-1, {fld}), subindustry)"),
    ]

out = os.path.join(REPO, "tracking", "reference", "exprs_kor_risk_w14.json")
json.dump([[l, e] for l, e in E], open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"wrote {len(E)} -> {out}")
