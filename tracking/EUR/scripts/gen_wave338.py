import json

# ★ 数据集切换的正当性（用户：「不频繁换数据集，除非无计可施」）
#   CASSIE 族已穷尽：30 字段 × 6 分组轴 × 5 decay × 3 hump × 5 窗口 = 2700+ 组合
#   model27（StarMine 信用 PD）已证死机制
#   ⇒ 符合「无计可施」条款
# ★ analyst_base_ref：ANALYST 类 / a=7（低拥挤）/ cov 0.832
#   且论坛 5 帖（合计 174 赞）一致指出：分析师数据在 EUR 有效的是
#   「修正动量 > 绝对水平」、「广度 > 幅度」、PEAD
#   —— 而 EUR 历史实测「分析师预期修正」族（analyst_factor_signals）产出过 S1.66（全闸过，prod 0.757 挡）
#   ⇒ 机制在 EUR 被验证过有效，只是上一轮撞 prod；本轮换用【低拥挤】的analyst_base_ref，prod 可能不同

S = {"decay": 40, "neut": "INDUSTRY", "truncation": 0.08, "maxTrade": "ON"}


def mk(code, note, **kw):
    d = dict(S)
    d["code"] = code
    d["note"] = note
    d.update(kw)
    return d


# VECTOR 字段需 vec_avg 归约
F_SURPRISE = "consensus_surprise_percentage_annual"  # ★ PEAD 核心
F_STD = "consensus_stddev_estimate_annual"           # ★ 分歧度
F_NUM = "num_estimates_consensus_annual"             # ★ 广度
F_MEAN = "consensus_mean_estimate_annual"             # 一致预期均值（对照组）
F_HIGH = "consensus_high_estimate_annual"
F_LOW = "consensus_low_estimate_annual"
F_DIFF = "consensus_vs_actual_diff_annual"            # ★ 实际 vs 预期差
F_ACT = "reported_actual_value_annual"


def dz(f, win=22, h="0.001", grp=None):
    """变化量 + hump（今天验证的最优形态）"""
    core = "hump(rank(ts_delta(vec_avg(%s),%d)), hump=%s)" % (f, win, h)
    return "group_zscore(%s, %s)" % (core, grp) if grp else core


def lv(f, h="0.001", grp=None):
    core = "hump(rank(vec_avg(%s)), hump=%s)" % (f, h)
    return "group_zscore(%s, %s)" % (core, grp) if grp else core


items = [
    # ---- ★ 论坛第1 信号：PEAD（盈利意外）— 预期惊喜的变化量 ----
    mk(dz(F_SURPRISE), "A1 ★★PEAD 预期惊喜 变化量 (论坛第一信号)"),
    mk(dz(F_SURPRISE, 66), "A2 PEAD 变化量 66日"),
    mk(lv(F_SURPRISE), "A3 PEAD 水平值 (对照: 验证是否也需变化量)"),
    # ---- ★ 论坛第2 信号：预期差 = 实际 - 预期 ----
    mk(dz(F_DIFF, 22), "A4 ★★预期差(实际-预期) 变化量"),
    mk(dz(F_DIFF, 66), "A5 预期差 变化量 66日"),
    mk(lv(F_DIFF), "A6 预期差 水平值"),
    # ---- ★ 论坛第3 信号：广度 / 分歧度 ----
    mk(dz(F_STD, 22), "A7 ★分歧度(stddev) 变化量"),
    mk(lv(F_STD), "A8 分歧度 水平值"),
    mk(dz(F_NUM, 22), "A9 ★广度(分析师数量) 变化量"),
    mk(lv(F_NUM), "A10 广度 水平值"),
    # ---- 分歧度与广度之比（覆盖分歧：分析师多但分歧大 = 不确定）----
    mk("hump(rank(divide(vec_avg(%s), vec_avg(%s))), hump=0.001)" % (F_STD, F_NUM),
       "A11 ★★分歧/广度 比 (不确定性定价)"),
    mk("hump(rank(divide(vec_avg(%s), ts_mean(vec_avg(%s), 66))), hump=0.001)" % (F_STD, F_STD),
       "A12 分歧度相对自身历史(惊讶的意外性)"),
    # ---- 一致预期水平的绝对值（论坛说这条弱，作对照）----
    mk(lv(F_MEAN), "A13 一致预期均值 水平 (论坛: 绝对水平弱, 对照组)"),
    mk(dz(F_MEAN, 22), "A14 一致预期均值 变化量 (修正动量)"),
    # ---- 分析师分歧的价格含量（high-low 区间 = 不确定性）----
    mk("hump(rank(divide(subtract(vec_avg(%s), vec_avg(%s)), vec_avg(%s))), hump=0.001)"
       % (F_HIGH, F_LOW, F_MEAN), "A15 ★★预期区间宽度 (high-low)/mean"),
    # ---- 换分组轴（今天证subindustry 最强，16 天内跨3族验证）----
    mk(dz(F_SURPRISE, 22, grp="subindustry"), "A16 ★PEAD × subindustry (最强分组轴)"),
    mk(dz(F_DIFF, 22, grp="subindustry"), "A17 ★预期差 × subindustry"),
    mk(dz(F_SURPRISE, 22, grp="industry"), "A18 PEAD × industry (对照)"),
]

json.dump(items, open("tracking/EUR/candidates/eur_wave338_analyst_items.json",
                      "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wave338 设计", len(items), "条：analyst_base_ref 分析师预期族")
print("  论坛三大信号全覆盖：PEAD(A1-3) / 预期差(A4-6) / 广度·分歧(A7-12)")
print("A1 =", items[0]["code"][:76])
