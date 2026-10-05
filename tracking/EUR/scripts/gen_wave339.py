import json

# ★ wave339：analyst45 —— 覆盖 1.0（EUR analyst 类最高）、a=635
#   但注意：它**不是分析师预期数据**，是「投资 idea 跟踪」数据
#   （目标价 / 信念度 / 净敞口 / 想法选股的相对收益）
#   ⇒ 这是**全新的信息维度**：反映「意见领袖/聪明钱的选择」，与公司基本面零重叠（§3）
# ★ 覆盖 1.0 解决了 wave338 的致命伤（信号字段覆盖仅 0.3158）
#
# 核心信号设计：
#   ① 目标价套利空间 = (target_prc - latest_prc) / latest_prc  ← 经典分析师目标价信号
#   ② 现价 vs 平均初始买入价 = 浮盈亏
#   ③ 信念度 probability（a=0，无人用 ⇒ 低拥挤）
#   ④ 想法净敞口 net_market_exposure（a=114，多空分歧度）
#   ⑤ 想法选股的相对收益（anl45_stock_ret_per_relative, a=11）= 意见领袖选股能力

S = {"decay": 160, "neut": "INDUSTRY", "truncation": 0.08, "maxTrade": "ON"}


def mk(code, note, **kw):
    d = dict(S)
    d["code"] = code
    d["note"] = note
    d.update(kw)
    return d


def dz(f, win=22, h="0.001", grp=None):
    core = "hump(rank(ts_delta(vec_avg(%s),%d)), hump=%s)" % (f, win, h)
    return "group_zscore(%s, %s)" % (core, grp) if grp else core


TGT = "anl45_target_prc"          # 作者预期退出价
LST = "anl45_latest_prc"          # 想法当前价
AVGI = "anl45_avg_initial_prc"    # 平均初始买入价（volume 加权）
PROB = "anl45_probability"        # 信念度（a=0 无人用）
NME = "anl45_net_market_exposure"  # 多空净敞口（a=114）
REL = "anl45_stock_ret_per_relative"  # 想法选股相对收益（a=11）
IDEA = "anl45_idea_count"         # 想法数（关注度）
TIME = "anl45_time"               # 预期持有期
TOTP = "anl45_tot_ret_per"        # 总收益率
TREE = "anl45_treynor_ratio"      # 特雷诺（风险调整）
JEN = "anl45_jensensalpha"        # 詹森alpha
ANG = "anl45_ang_inv"             # 时间加权投资额

items = [
    # ---- ★★★ 目标价套利空间（最经典）----
    mk("hump(rank(divide(subtract(vec_avg(%s), vec_avg(%s)), vec_avg(%s))), hump=0.001)" % (TGT, LST, LST),
       "D1 ★★★目标价上行空间 (TGT-LST)/LST"),
    mk("hump(rank(divide(subtract(vec_avg(%s), vec_avg(%s)), vec_avg(%s))), hump=0.001)" % (TGT, AVGI, AVGI),
       "D2 ★★目标价 vs 平均初始价 (跨期套利空间)"),
    # 目标价相对历史的变化（修正动量，论坛核心原则）
    mk(dz(TGT), "D3 ★★目标价 变化量 (修正动量, 论坛第一原则)"),
    mk(dz(TGT, 66), "D4 目标价 变化量 66日"),
    # ---- 信念度 / 关注度（a=0/13，低拥挤）----
    mk(dz(PROB), "D5 ★信念度 变化量 (a=0 无人用)"),
    mk("hump(rank(vec_avg(%s)), hump=0.001)" % PROB, "D6 信念度 水平值"),
    mk(dz(IDEA, 22), "D7 想法数 变化量 (关注度提升)"),
    mk("hump(rank(vec_avg(%s)), hump=0.001)" % IDEA, "D8 想法数 水平值"),
    # ---- 多空分歧度（a=114）----
    mk(dz(NME, 22), "D9 ★净敞口 变化量 (多空分歧)"),
    mk("hump(rank(vec_avg(%s)), hump=0.001)" % NME, "D10 净敞口 水平值"),
    # ---- 意见领袖选股能力（累积型，慢变量）----
    mk(dz(REL, 22), "D11 ★想法相对收益 变化量"),
    mk(dz(REL, 132), "D12 想法相对收益 变化量132 (累积能力)"),
    mk("hump(rank(vec_avg(%s)), hump=0.001)" % REL, "D13 想法相对收益 水平"),
    # ---- 风险调整与时间维度 ----
    mk("hump(rank(vec_avg(%s)), hump=0.001)" % TREE, "D14 特雷诺比率 水平"),
    mk("hump(rank(vec_avg(%s)), hump=0.001)" % JEN, "D15 詹森alpha 水平"),
    mk(dz(ANG, 22), "D16 投资额 变化量 (资金流入)"),
    mk(dz(TIME, 22), "D17 预期持有期 变化量 (耐心度)"),
    # ---- ★ 与CASSIE 最优形态交叉（subindustry，EUR 最强分组轴）----
    mk("group_zscore(hump(rank(divide(subtract(vec_avg(%s), vec_avg(%s)), vec_avg(%s))), hump=0.001), subindustry)"
       % (TGT, LST, LST), "D18 ★★目标价空间 × subindustry (最强分组轴)"),
]

json.dump(items, open("tracking/EUR/candidates/eur_wave339_idea_items.json",
                      "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wave339 设计", len(items), "条：analyst45 投资 idea 跟踪族（覆盖 1.0）")
print("  核心信号：目标价套利空间(D1-4) / 信念度·关注度(D5-8) / 多空分歧(D9-10)")
print("            / 意见领袖选股能力(D11-13) / 风险调整(D14-17)")
print("D1 =", items[0]["code"][:78])
