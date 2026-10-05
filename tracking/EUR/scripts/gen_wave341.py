import json

# ★★ wave341：**方向性反转验证波**
# 动机：wave339 D1/D3（目标价空间 -0.53/-0.43）+ wave340 全族18 条（-0.21~-1.13）
#       跨 3 个独立数据源、9 条独立信号，**全部负 S**
#       ⇒ 假设：EUR 存在【主观预期类信号反向定价】机制
#          （过度乐观 / 买入拥挤 / 预期过度定价）
#       而已证有效的 CASSIE `ocf_currliab` 是【客观基本面事实】⇒ 正向
#
# 本波要回答的唯一问题：**加上reverse 后能否转正？**
#   若转正 ⇒ 反向机制成立，且这就是一条独立的新机制（值得深挖）
#   若仍负 ⇒ 说明问题不在方向，而在别处（如 decay/maxTrade 对这类信号不适配）
#
# ★ 合规：reverse(...) 与 multiply(-1, ...) 都是单信号算子，不违反「禁混信号」

S = {"decay": 160, "neut": "INDUSTRY", "truncation": 0.08, "maxTrade": "ON"}


def mk(code, note, **kw):
    d = dict(S)
    d["code"] = code
    d["note"] = note
    d.update(kw)
    return d


def rev(inner):
    return "hump(reverse(rank(%s)), hump=0.001)" % inner


def dz_raw(f, win):
    # 裸变化量（未归一，用于 reverse 包裹）
    return "ts_delta(vec_avg(%s),%d)" % (f, win)


def dz_lv_raw(f):
    return "vec_avg(%s)" % f


# ==================== A组：acquisition_model 反向（wave340 全族为负）====================
GLB = "global_percentile_acquisition_likelihood"
CTRY = "country_percentile_acquisition_likelihood"
SECT = "sector_percentile_acquisition_likelihood"
IND = "industry_percentile_acquisition_likelihood"
VAL = "global_valuation_percentile_rank"
CRED = "global_credit_quality_percentile_rank"
SIZE = "global_company_size_percentile_rank"
TEXT = "global_text_factor_percentile_rank"

items = [
    # ---- 反向 × 窗口梯度（对应 wave340 E1/E2/E3 全负）----
    mk(rev(dz_raw(GLB, 22)), "F1 ★★reverse 并购可能性 22日 (E1原S-0.80)"),
    mk(rev(dz_raw(GLB, 66)), "F2 ★★reverse 66日 (E2原S-1.11)"),
    mk(rev(dz_raw(GLB, 132)), "F3 ★★reverse 132日 (E3原S-1.10)"),
    mk(rev(dz_raw(GLB, 44)), "F4 reverse 44日 (E18原S-1.13)"),
    mk(rev(dz_raw(GLB, 15)), "F5 reverse 15日 (E17原S-0.65)"),
    # ---- 反向 × 水平值（对应 E4 水平 S-0.66）----
    mk(rev(dz_lv_raw(GLB)), "F6 ★★reverse 水平值 (E4原S-0.66)"),
    # ---- 反向 × 换口径 ----
    mk(rev(dz_raw(CTRY, 22)), "F7 reverse 国别口径 (E5原S-0.70)"),
    mk(rev(dz_raw(SECT, 22)), "F8 reverse 行业口径 (E6原S-0.71)"),
    mk(rev(dz_raw(IND, 22)), "F9 reverse 细行业口径 (E7原S-0.72)"),
    # ---- 反向 × 模型分项（E12-E16 原本就负）----
    mk(rev(dz_raw(VAL, 22)), "F10 ★★reverse 估值分项 (E13原S-0.48)"),
    mk(rev(dz_raw(CRED, 22)), "F11 ★reverse 信用分项 (E16原S-0.53)"),
    mk(rev(dz_raw(TEXT, 22)), "F12 reverse 文本/新闻分项 (E15原S-0.64)"),
    mk(rev(dz_raw(SIZE, 22)), "F13 reverse 规模分项 (E12原S-0.79)"),
    # ---- ★★ 反向 + 最强分组轴（今日已证 group_zscore(·,subindustry) 有效但字段特异）----
    mk("group_zscore(%s, subindustry)" % rev(dz_raw(GLB, 22)),
       "F14 ★★★reverse × subindustry (最强杠杆×反向信号)"),
    mk("group_zscore(%s, industry)" % rev(dz_raw(GLB, 22)),
       "F15 ★★reverse × industry"),
    # ---- ★★★ 跨源验证：analyst45 的两个负信号也反向 ----
    mk(rev("divide(subtract(vec_avg(anl45_target_prc), vec_avg(anl45_latest_prc)), vec_avg(anl45_latest_prc))"),
       "F16 ★★★跨源: reverse 目标价上行空间 (D1原S-0.53)"),
    mk(rev(dz_raw("anl45_target_prc", 22)),
       "F17 ★★跨源: reverse 目标价变化量 (D3原S-0.43)"),
    # ---- 控制行（应复现 WjegEmQO=1.94，确认批次口径未漂移）----
    mk("group_zscore(hump(rank(ts_delta(vec_avg(qfl_cassie_convention_ocf_currliab),22)), hump=0.001), subindustry)",
       "F18 控制行 CASSIE (应=1.94/2Y1.59/sub1.96)"),
]

json.dump(items, open("tracking/EUR/candidates/eur_wave341_reverse_items.json",
                      "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wave341 设计", len(items), "条：★方向性反转验证波")
print("  A组(13): acquisition_model 各信号 × reverse（对应 wave340 全负）")
print("  B组(2):× subindustry/industry 杠杆")
print("  C组(2): ★跨源验证 analyst45 的两个负信号")
print("  控制(1): CASSIE 复现")
print("F1 =", items[0]["code"][:76])
