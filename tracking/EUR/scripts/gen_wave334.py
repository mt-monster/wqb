import json

# W9 = qes_alter_debt_weighted_interest_rate：S1.48 / F0.98 / 2Y2.05 / sub1.13
# 距 S 差 0.10、距 F 差 0.02 —— 在杠杆可达范围内
F = "qfl_cassie_qes_alter_debt_weighted_interest_rate"


def mk(code, note, decay=160, neut="INDUSTRY", trunc=0.08, maxTrade="ON", hump=None):
    d = {"code": code, "note": note, "decay": decay, "neut": neut,
         "truncation": trunc, "maxTrade": maxTrade}
    return d


def core(win=22, h="0.001", fld=F):
    return "hump(rank(ts_delta(vec_avg(%s),%d)), hump=%s)" % (fld, win, h)


items = [
    # 控制行（复现 W9）
    mk(core(), "Z1 控制行 W9复现 (S1.48/2Y2.05)"),
    # ---- decay 细网格（W9 用的是 160，S 型可能需要不同档）----
    mk(core(), "Z2 decay=40 (W9 未测此档)", decay=40),
    mk(core(), "Z3 decay=100", decay=100),
    mk(core(), "Z4 decay=250", decay=250),
    mk(core(), "Z5 decay=400 (极长档压2Y提S?)", decay=400),
    # ---- hump 档位（decay=160 上从未细扫）----
    mk(core(h="0.0005"), "Z6 hump 0.0005"),
    mk(core(h="0.002"), "Z7 hump 0.002"),
    mk(core(h="0.004"), "Z8 hump 0.004"),
    # ---- 窗口细扫（22 是唯一测过的）----
    mk(core(win=15), "Z9 窗口15"),
    mk(core(win=30), "Z10 窗口30"),
    mk(core(win=44), "Z11 窗口44"),
    mk(core(win=66), "Z12 窗口66 (W9的2Y高, 试长窗口)"),
    # ---- 中性化档（W9 用 INDUSTRY；今日已证 COUNTRY/CROWDING 降 S，但值得验证）----
    mk(core(), "Z13 neut=SUBINDUSTRY (W9未测)", neut="SUBINDUSTRY"),
    mk(core(), "Z14 neut=FAST", neut="FAST"),
    # ---- truncation（W9 用 0.08；今日已证 M1 族 no-op，但本族未测）----
    mk(core(), "Z15 truncation=0.0", trunc=0.0),
    mk(core(), "Z16 truncation=0.20", trunc=0.2),
    # ---- 换 hump 应用位置（先 hump 再 rank vs 先 rank 再 hump）----
    mk("hump(ts_delta(vec_avg(%s),22), hump=0.001)" % F, "Z17 无rank包裹(测rank的贡献)"),
    # ---- 对照：CASSIE 已知最优字段在同设置下（确认设置档口径）----
    mk("hump(rank(ts_delta(vec_avg(qfl_cassie_convention_ocf_currliab),22)), hump=0.001)",
       "Z18 对照 ocf_currliab (应=1.65/1.81)"),
]

json.dump(items, open("tracking/EUR/candidates/eur_wave334_w9_items.json",
                      "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wave334 设计", len(items), "条：W9 债务加权利率设置档全扫")
print("Z1 =", items[0]["code"][:74])
