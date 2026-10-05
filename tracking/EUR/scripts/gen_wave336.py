import json

# ★ 突破：X13 = group_zscore(hump(rank(ts_delta(ocf_currliab,22)),hump=0.001), subindustry)
#   S1.94 / F1.38 / 2Y1.59 / sub1.96 / robust1.37 / TO0.031，零 FAIL
#   相对 1YZJAMqK（S1.65/1.10/1.81/1.65）：**S +0.29、sub +0.31、robust +0.27**
#   ⇒ 「外层 group_zscore(·, subindustry)」是 EUR 目前最有效的组合杠杆

F = "qfl_cassie_convention_ocf_currliab"
S = {"decay": 160, "neut": "INDUSTRY", "truncation": 0.08, "maxTrade": "ON"}


def mk(code, note, **kw):
    d = dict(S)
    d["code"] = code
    d["note"] = note
    d.update(kw)
    return d


def gz(inner_group, field=F, win=22, h="0.001"):
    return "group_zscore(hump(rank(ts_delta(vec_avg(%s),%d)), hump=%s), %s)" % (
        field, win, h, inner_group)


items = [
    # ---- 控制行复现 ----
    mk(gz("subindustry"), "G1 控制行 X13复现 (S1.94/2Y1.59/sub1.96)"),
    # ---- ★★ 分组轴全扫（本波最重要维度：industry→subindustry 带来 +0.29S）----
    mk(gz("industry"), "G2 industry (X12已知1.64, 作受控对照)"),
    mk(gz("sector"), "G3 ★sector (比 industry 更粗一档)"),
    mk(gz("country"), "G4 ★country (EUR多国市场, 今天已证neut=COUNTRY降S但表达式级分组未测)"),
    mk(gz("market"), "G5 ★market (全市场同值, 应退化- 对照)"),
    # ---- 窗口细扫（22 是原值，subindustry 换轴后最优窗口可能变）----
    mk(gz("subindustry", win=15), "G6 subindustry × 窗口15"),
    mk(gz("subindustry", win=30), "G7 subindustry × 窗口30"),
    mk(gz("subindustry", win=44), "G8 subindustry × 窗口44"),
    mk(gz("subindustry", win=66), "G9 subindustry × 窗口66"),
    # ---- hump 档位（subindustry 换轴后）----
    mk(gz("subindustry", h="0.0005"), "G10 subindustry × hump0.0005"),
    mk(gz("subindustry", h="0.002"), "G11 subindustry × hump0.002"),
    # ---- decay 档（今日证 decay 是 2Y 杠杆，这里 2Y 只有 1.59 刚过线，须加固）----
    mk(gz("subindustry"), "G12 ★subindustry × decay=100 (2Y刚过线, 试更高档)", decay=100),
    mk(gz("subindustry"), "G13 ★subindustry × decay=250 (加档提2Y)", decay=250),
    mk(gz("subindustry"), "G14 subindustry × decay=400", decay=400),
    # ---- 换字段（把 subindustry 杠杆施加到 wave331 的 W9 最优字段）----
    mk(gz("subindustry", field="qfl_cassie_qes_alter_debt_weighted_interest_rate"),
       "G15 ★★W9债务加权利率 × subindustry (两个发现交叉)"),
    mk(gz("subindustry", field="qfl_cassie_qes_alter_insolvency_stress_2y"),
       "G16 破产压力2y × subindustry"),
    # ---- 变化轴替换（在最优组合上）----
    mk("group_zscore(hump(rank(ts_rank(%s, 66)), hump=0.001), subindustry)" % F,
       "G17 ★ts_rank66 × subindustry (换轴+最优分组)"),
    mk("group_zscore(hump(rank(ts_delta(vec_avg(%s),18)), hump=0.001), subindustry)" % F,
       "G18 窗口18 × subindustry (X16的1.51+sub1.55 组合)"),
]

json.dump(items, open("tracking/EUR/candidates/eur_wave336_gzsub_items.json",
                      "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wave336 设计", len(items), "条：group_zscore(·,subindustry) 深挖 + 分组轴全扫 + 字段交叉")
print("G1 =", items[0]["code"][:80])
