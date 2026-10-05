import json

# model27：StarMine CCR 信用违约概率族
# ★ 价值：star_ccr_combined_pd 覆盖 0.9687（MATRIX 免归约）、a=8（低拥挤）
#   且有多层级排名字段（country/industry/sector/region/global）
#   —— 正好对应今天验证过的「换分组轴」杠杆
# ⚠ 与 CASSIE 同为信用机制但**数据源不同**（StarMine vs CASSIE）⇒ prod 可能独立

S = {"decay": 160, "neut": "INDUSTRY", "truncation": 0.08, "maxTrade": "ON"}


def mk(code, note, **kw):
    d = dict(S)
    d["code"] = code
    d["note"] = note
    d.update(kw)
    return d


PD = "star_ccr_combined_pd"          # 覆盖 0.9687 主信号
IMPL = "star_ccr_implied_rating"      # 覆盖 1.0 评级
ANNP = "annual_default_probability_percent"  # 覆盖 0.7845
IND_R = "star_ccr_industry_rank"      # 行业内排位
CTY_R = "star_ccr_country_rank"       # 国别排位
GLB_R = "star_ccr_global_rank"        # 全球排位
MDL = "mdl27_index_rating"            # 覆盖 1.0

items = [
    # ---- 水平值 vs 变化量（今日结论：慢变量该用变化量）----
    mk("hump(rank(ts_delta(%s, 22)), hump=0.001)" % PD,
       "P1 ★PD 变化量 22日 (CASSIE 同形态, 最优先)"),
    mk("hump(rank(%s), hump=0.001)" % PD,
       "P2 PD 水平值直用 (对照: 验证是否也需变化量)"),
    mk("hump(rank(ts_delta(%s, 66)), hump=0.001)" % PD,
       "P3 PD 变化量 66日"),
    mk("hump(rank(ts_delta(%s, 132)), hump=0.001)" % PD,
       "P4 PD 变化量 132日 (2Y 车道)"),
    # ---- 隐含评级（覆盖 1.0）----
    mk("hump(rank(ts_delta(%s, 22)), hump=0.001)" % IMPL,
       "P5 隐含评级 变化量 (覆盖1.0)"),
    mk("hump(rank(%s), hump=0.001)" % IMPL,
       "P6 隐含评级 水平"),
    mk("hump(rank(ts_delta(%s, 22)), hump=0.001)" % MDL,
       "P7 mdl27 评级 变化量 (覆盖1.0)"),
    mk("hump(rank(%s), hump=0.001)" % MDL,
       "P8 mdl27 评级 水平"),
    # ---- 年化 PD ----
    mk("hump(rank(ts_delta(%s, 22)), hump=0.001)" % ANNP,
       "P9 年化PD% 变化量"),
    # ---- ★排名字段：换分组轴（今日已证 group_zscore 是唯一能同时保S与sub的轴）----
    mk("group_zscore(hump(rank(ts_delta(%s, 22)), hump=0.001), industry)" % PD,
       "P10 ★PD变化量 × group_zscore(industry)"),
    mk("group_zscore(hump(rank(ts_delta(%s, 22)), hump=0.001), subindustry)" % PD,
       "P11 PD变化量 × group_zscore(subindustry)"),
    # ---- ★★ 排名字段当"相对违约"信号（不同机制：不是绝对 PD，是相对位置）----
    mk("hump(rank(ts_delta(%s, 22)), hump=0.001)" % IND_R,
       "P12 ★行业内排位 变化量 (相对违约信号)"),
    mk("hump(rank(%s), hump=0.001)" % IND_R,
       "P13 行业内排位 水平"),
    mk("hump(rank(ts_delta(%s, 22)), hump=0.001)" % CTY_R,
       "P14 国别排位 变化量 (EUR多国市场, 呼应 COUNTRY 中性化)"),
    mk("hump(rank(ts_delta(%s, 22)), hump=0.001)" % GLB_R,
       "P15 全球排位 变化量"),
    # ---- 排位差（跨层级比较：国家 vs 行业，识别"行业内好但国家差"）----
    mk("hump(subtract(rank(ts_delta(%s, 22)), rank(ts_delta(%s, 22))), hump=0.001)" % (IND_R, CTY_R),
       "P16 ★★排位差 行业-国别 (跨层级相对位置)"),
    mk("hump(subtract(rank(%s), rank(%s)), hump=0.001)" % (IND_R, GLB_R),
       "P17 排位差 行业-全球"),
    # ---- 二阶（PD 恶化加速 = 风险急升）----
    mk("hump(rank(ts_delta(ts_delta(%s, 22), 22)), hump=0.001)" % PD,
       "P18 ★PD 二阶变化 (违约恶化加速度)"),
    # ---- 控制行（应复现 1YZJAMqK）----
    mk("hump(rank(ts_delta(vec_avg(qfl_cassie_convention_ocf_currliab), 22)), hump=0.001)",
       "P19 控制行 ocf_currliab (应=1.65/2Y1.81)"),
]

json.dump(items, open("tracking/EUR/candidates/eur_wave335_model27_items.json",
                      "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wave335 设计", len(items), "条：model27 StarMine CCR 信用PD 族")
print("P1 =", items[0]["code"][:74])
