import json

S = {"decay": 40, "neut": "SUBINDUSTRY"}


def mk(code, note, **kw):
    d = dict(S)
    d["code"] = code
    d["note"] = note
    d.update(kw)
    return d


A = "total_financing_cash_flow"


def vne(subj, axis):
    return "vector_neut(%s,rank(divide(%s,assets_total_2)))" % (subj, axis)


def rat(x):
    return "reverse(rank(divide(%s,assets_total_2)))" % x


core3 = vne(vne(vne(rat(A), "free_cash_flow"), "fnd23_intfvm_xeci"), "operating_cashflow")
core2 = vne(vne(rat(A), "free_cash_flow"), "fnd23_intfvm_xeci")

items = [
    mk(core3, "Y1 控制行 JjQmx9nm复现 (prod0.6695已通过)"),
    mk(core3, "Y2 控制行 × maxTrade=ON (今日通用杠杆首试该族)", maxTrade="ON"),
    mk(vne(rat(A), "cashflow_op"), "Y3 二层残差 第2轴=cashflow_op"),
    mk(vne(rat(A), "fnd23_annfv1a_1dls"), "Y4 二层残差 第2轴=annfv1a_1dls"),
    mk(vne(rat(A), "fnd23_annfv1a_1los"), "Y5 二层残差 第2轴=annfv1a_1los"),
]
for i, ax in enumerate(["cashflow_op", "fnd23_annfv1a_1dls", "fnd23_annfv1a_1los",
                        "financing_cash_flow_2", "fnd23_annfv1a_1dls"], 6):
    items.append(mk(vne(vne(vne(rat(A), "free_cash_flow"), "fnd23_intfvm_xeci"), ax),
                    "Y%d 四层残差 第3轴=%s" % (i, ax)))

items += [
    mk(vne(rat(A), "free_cash_flow"), "Y11 轴序对调(intfvm->fcf) 顺序敏感性"),
    mk("vector_neut(%s,rank(divide(free_cash_flow,actual_total_assets_value_annual12)))" % rat(A),
       "Y12 分母=actual_total_assets_value_annual12"),
    mk("vector_neut(%s,rank(divide(free_cash_flow,change_net_net_assets_to_price)))" % rat(A),
       "Y13 分母=change_net_net_assets_to_price"),
    mk(core2, "Y14 二层残差 × maxTrade=ON", maxTrade="ON"),
    mk(core3, "Y15 四层残差 × maxTrade=ON", maxTrade="ON"),
    mk(core3, "Y16 四层残差 × decay=100 (今日证 decay 是 2Y 杠杆)", decay=100),
    mk(core3, "Y17 四层残差 × decay=160", decay=160),
]

json.dump(items, open("tracking/EUR/candidates/eur_wave333_deepres_items.json",
                      "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wave333 设计", len(items), "条")
print("Y1 =", items[0]["code"][:76], "...")
