import json

# ★ wave340：acquisition_model（M&A 被收购概率模型）
#   15/15 字段覆盖 0.994、alphaCount=10（极低拥挤）
#   机制 = M&A Target Model（并购目标选择），**与本会话所有已测机制零重叠**
#   （本会话已证死：信用/新闻/季节/违约距离/分析师预期/投资idea）
#
# 字段设计要点：
#   核心 = *percentile_acquisition_likelihood（全球/国家/行业/区域四个口径）
#   含义 = 该股成为并购标的的相对可能性
#   ★ 学术依据：被收购公司通常有显著正向超额收益（公告效应 announcement effect）

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


def lv(f, h="0.001", grp=None):
    core = "hump(rank(vec_avg(%s)), hump=%s)" % (f, h)
    return "group_zscore(%s, %s)" % (core, grp) if grp else core


GLB = "global_percentile_acquisition_likelihood"      # ★主信号 全球口径
CTRY = "country_percentile_acquisition_likelihood"   # 国别口径
SECT = "sector_percentile_acquisition_likelihood"    # 行业口径
IND = "industry_percentile_acquisition_likelihood"   # 细行业口径
REGN = "region_percentile_acquisition_likelihood"    # 区域口径
FUND = "global_fundamental_factor_percentile_rank"   # 基本面分项
SIZE = "global_company_size_percentile_rank"         # 规模分项
TEXT = "global_text_factor_percentile_rank"          # 文本/新闻分项
CRED = "global_credit_quality_percentile_rank"       # 信用分项
VAL = "global_valuation_percentile_rank"             # 估值分项

items = [
    # ---- 主信号：并购可能性（水平 = 水平分已是百分位，变化量 = 修正）----
    mk(dz(GLB), "E1 ★★★并购可能性 变化量 (全球口径)"),
    mk(dz(GLB, 66), "E2 并购可能性 变化量 66日"),
    mk(dz(GLB, 132), "E3 并购可能性 变化量 132日 (慢变量)"),
    mk(lv(GLB), "E4 并购可能性 水平值 (对照)"),
    # ---- 分层口径：谁的口径更有信息？----
    mk(dz(CTRY, 22), "E5 国别口径 变化量"),
    mk(dz(SECT, 22), "E6 行业口径 变化量"),
    mk(dz(IND, 22), "E7 ★细行业口径 变化量 (最细粒度)"),
    mk(dz(REGN, 22), "E8 区域口径 变化量"),
    # ---- ★★ 口径差 = 「在全球被看好但在本行业被看好得少」= 跨层错位信号 ----
    mk("hump(rank(subtract(rank(vec_avg(%s)), rank(vec_avg(%s)))), hump=0.001)" % (GLB, SECT),
       "E9 ★★口径差 全球-行业 (相对错位)"),
    mk("hump(rank(subtract(rank(vec_avg(%s)), rank(vec_avg(%s)))), hump=0.001)" % (GLB, CTRY),
       "E10 ★★口径差 全球-国别 (国别溢价)"),
    mk(dz(SECT, 22, grp="subindustry"), "E11 ★行业口径 × subindustry (最强分组轴)"),
    # ---- 模型分项：哪个分项驱动并购可能性？（学术：规模与估值是主要驱动）----
    mk(dz(SIZE, 22), "E12 规模分项 变化量 (并购规模效应)"),
    mk(dz(VAL, 22), "E13 ★估值分项 变化量 (便宜的被买)"),
    mk(dz(FUND, 22), "E14 基本面分项 变化量"),
    mk(dz(TEXT, 22), "E15 ★文本/新闻分项 变化量 (收购传闻)"),
    mk(dz(CRED, 22), "E16 信用分项 变化量 (信用恶化易被收购)"),
    # ---- 主信号 × 换窗口微调 ----
    mk(dz(GLB, 15), "E17 并购可能性 窗口15"),
    mk(dz(GLB, 44), "E18 并购可能性 窗口44"),
]

json.dump(items, open("tracking/EUR/candidates/eur_wave340_ma_items.json",
                      "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wave340 设计", len(items), "条：acquisition_model并购概率族")
print("  核心(E1-4) / 分层口径(E5-8) / ★口径差(E9-10) / 模型分项(E12-16) / 窗口(E17-18)")
print("E1 =", items[0]["code"][:76])
