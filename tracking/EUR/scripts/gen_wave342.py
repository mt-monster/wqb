import json

# ★★ wave342：反向定价机制的「2Y 车道」尝试
#依据 §105.2：反转后 S 最高 1.13（差 0.45），但 2Y 全部 0.00–0.86（无一过 1.58）
#   ⇒ S 与 2Y 在此机制里是【跷跷板】⇒ 必须走 2Y 车道，不能继续调 S
#
# 已证的三条 2Y 车道（本日实证）：
#   ① decay 上调（CASSIE：40→160 时 2Y 1.76→1.81）
#   ② 长窗口（wave332 X3 `ts_rank(·,132)` 拿到该波 2Y 最高 1.88）
#   ③ 水平值代替变化量（wave336 G5 market 2Y 1.75；wave341 F6/F11 水平值 2Y 0.84/0.86 相对最好）
#
# 目标：把 2Y 从 0.86 推到 ≥1.58，同时 S 保持 ≥1.58
#★ 已知最优候选：F4（reverse 窗口44，S1.13/2Y0.55）S 最高、F6（水平值，2Y 0.84）、F11（信用分项，2Y 0.86）
#
# 依据「杠杆×信号方向耦合」（§105.3）⇒ 不再叠 subindustry，只走设置档维度

S = {"decay": 160, "neut": "INDUSTRY", "truncation": 0.08, "maxTrade": "ON"}
GLB = "global_percentile_acquisition_likelihood"
CRED = "global_credit_quality_percentile_rank"
VAL = "global_valuation_percentile_rank"


def mk(code, note, **kw):
    d = dict(S)
    d["code"] = code
    d["note"] = note
    d.update(kw)
    return d


def rev(inner):
    return "hump(reverse(rank(%s)), hump=0.001)" % inner


def dz_raw(f, win):
    return "ts_delta(vec_avg(%s),%d)" % (f, win)


items = [
    # ---- 车道①：decay 上调（对 F4 窗口44 施加，S 最高的那个）----
    mk(rev(dz_raw(GLB, 44)), "G1 ★★reverse44 × decay=400 (S1.13/2Y0.55 基线)"),
    mk(rev(dz_raw(GLB, 44)), "G2 ★★reverse44 × decay=250", decay=250),
    mk(rev(dz_raw(GLB, 44)), "G3 ★reverse44 × decay=700", decay=700),
    mk(rev(dz_raw(GLB, 44)), "G4 reverse44 × decay=40 (反向对照: 低decay)", decay=40),
    # ---- 车道②：长窗口（F4 的 44 已是最优，向上找）----
    mk(rev(dz_raw(GLB, 88)), "G5 ★★reverse88 (44→88 窗口)"),
    mk(rev(dz_raw(GLB, 132)), "G6 reverse132"),
    mk(rev(dz_raw(GLB, 176)), "G7 ★reverse176 (半年窗)"),
    mk(rev(dz_raw(GLB, 252)), "G8 ★reverse252 (年窗, 2Y车道最强候选)"),
    # ---- 车道③：长窗口 + 长 decay 组合（双2Y 加厚）----
    mk(rev(dz_raw(GLB, 88)), "G9 ★★★reverse88 × decay=400", decay=400),
    mk(rev(dz_raw(GLB, 132)), "G10 ★★★reverse132 × decay=400", decay=400),
    mk(rev(dz_raw(GLB, 252)), "G11 ★★reverse252 × decay=400", decay=400),
    # ---- 车道④：水平值（2Y 相对最好：F6 0.84 / F11 0.86）× 长 decay ----
    mk(rev("vec_avg(%s)" % GLB), "G12 ★★reverse水平值 × decay=400", decay=400),
    mk(rev("vec_avg(%s)" % CRED), "G13 ★★reverse信用分项水平 × decay=400", decay=400),
    mk(rev("vec_avg(%s)" % CRED), "G14 reverse信用分项水平 × decay=700", decay=700),
    mk(rev("ts_delta(vec_avg(%s),132)" % CRED), "G15 ★★reverse信用分项132 × decay=400", decay=400),
    # ---- 车道⑤：估值分项（波内2Y 唯一为负的，需换窗口救）----
    mk(rev("ts_delta(vec_avg(%s),132)" % VAL), "G16 ★reverse估值分项132 × decay=400", decay=400),
    # ---- 控制行：确认批次口径未漂移（应=1.94/2Y1.59/sub1.96）----
    mk("group_zscore(hump(rank(ts_delta(vec_avg(qfl_cassie_convention_ocf_currliab),22)), hump=0.001), subindustry)",
       "G17 控制行 CASSIE (应=1.94/2Y1.59/sub1.96)"),
]

json.dump(items, open("tracking/EUR/candidates/eur_wave342_rev2y_items.json",
                      "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wave342 设计", len(items), "条：★反向机制的 2Y 车道")
print("  ① decay 上调(160/250/400/700)  ② 长窗口(44→88/132/176/252)")
print("  ③ 长窗口×长decay 组合  ④ 水平值×长decay  ⑤ 估值分项换窗口")
print("  控制行 G17 校验批次口径")
print("G1 =", items[0]["code"][:74])
