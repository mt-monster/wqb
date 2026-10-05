import json

# ★ wave337：把已验证的最强组合【group_zscore(·,subindustry) + maxTrade=ON + decay=160】
#   系统性施加到 CASSIE 族全部「有信号苗头」的字段上。
# 依据：§96.2 证明 subindustry 粒度给 +0.29S / +0.31sub；
#      §94 证明 CASSIE 信号集中在 ocf_currliab，但 W9(S1.48) / W3(S1.40) / W5(S1.42)
#      三个字段在裸形态下已接近过线，叠加该杠杆后可能全部突破。
# ★ 本波设计要点：这些字段在【裸形态】下已知 S 值，可在结果里直接读出「杠杆增益」。

S = {"decay": 160, "neut": "INDUSTRY", "truncation": 0.08, "maxTrade": "ON"}

# (字段, 说明, 裸形态已知 S)
FIELDS = [
    ("qfl_cassie_qes_alter_debt_weighted_interest_rate", "债务加权利率 (W9 裸S1.48/2Y2.05 ★最有希望)", 1.48),
    ("qfl_cassie_qes_alter_insolvency_stress_2y", "破产压力2y (W3 裸S1.40)", 1.40),
    ("qfl_cassie_qes_alter_moderate_insolvency_stress_1y", "中度破产压力1y (W5 裸S1.42)", 1.42),
    ("qfl_cassie_qes_alter_extreme_insolvency_stress_1y", "极度破产压力1y (W7 裸S1.27)", 1.27),
    ("qfl_cassie_qes_alter_insolvency_stress_1y", "破产压力1y (W2 裸S1.07)", 1.07),
    ("qfl_cassie_qes_alter_insolvency_stress_9m", "破产压力9m (W4 裸S0.81)", 0.81),
    ("qfl_cassie_qes_alter_debt_weighted_duration", "债务加权久期 (W8 裸S0.47)", 0.47),
    ("qfl_cassie_qes_alter_growth_shortterm_debt", "短债增长率 (W10 裸S0.33)", 0.33),
    ("qfl_cassie_qes_alter_shortterm_debt_ratio", "短债占比 (W11 裸S0.67)", 0.67),
    ("qfl_cassie_qes_alter_revolver_debt", "循环信贷 (W13 裸S0.32)", 0.32),
    ("qfl_cassie_qes_cassie_prelimcomposite", "CASSIE初步综合分 (W19 裸S0.78)", 0.78),
    ("qfl_cassie_convention_longdebt_equity", "长期债务/权益 (W15 裸S0.57)", 0.57),
    ("qfl_cassie_convention_cng_longdebt_equity", "长期债务/权益变动 (W17 裸S0.61)", 0.61),
    ("qfl_cassie_convention_debt_mktcapital", "债务/市值 (W14 裸S0.01)", 0.01),
]


def gz(field, group, win=22, h="0.001"):
    return "group_zscore(hump(rank(ts_delta(vec_avg(%s),%d)), hump=%s), %s)" % (
        field, win, h, group)


items = []
for i, (fld, desc, base) in enumerate(FIELDS, 1):
    items.append({"code": gz(fld, "subindustry"),
                  "note": "H%-2d subindustry | %s" % (i, desc),
                  **S})
# G15 交叉验证（G15 裸形态只有 0.67，加 subindustry 后看能否翻转）
items.append({"code": gz("qfl_cassie_qes_alter_short_longterm_debt_ratio", "subindustry"),
              "note": "H15 subindustry | 短长债比 (裸S-0.56 反向轴, 测能否翻转)",
              **S})
# 杠杆强度对照：subindustry 已在 G1/2/3/5/12/13/18 测过，这里只加两条不同窗口确认
items.append({"code": gz("qfl_cassie_convention_ocf_currliab", "subindustry", win=18),
              "note": "H16 控制 窗口18 (应≈G18 1.83/2Y1.56)", **S})
items.append({"code": gz("qfl_cassie_convention_ocf_currliab", "subindustry", win=30),
              "note": "H17 控制 窗口30 (裸形态仅1.20, 看subindustry能否救活)", **S})

json.dump(items, open("tracking/EUR/candidates/eur_wave337_subindustry_items.json",
                      "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wave337 设计", len(items), "条：group_zscore(·,subindustry) × CASSIE 14 个字段")
print("  （裸形态 S 值已知，结果里可直接读出杠杆增益）")
print("H1 =", items[0]["code"][:78])
