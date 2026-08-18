# -*- coding: utf-8 -*-
"""wave27 model264 探针 items 生成：字段存在性校验 + 24 条表达式"""
import json

d = json.load(open(
    r"D:\coding\traeCN_project\wqb\tracking\GBR\reference\gbr_model264_fields.json",
    encoding="utf-8"))
valid = {f.get("id") for f in d.get("fields", [])}

cands = [
    # es 组 l3（move-up 概率）
    "mdl264_es_ebit_fy1_r1m_l3",
    "mdl264_es_ebitda_fy1_r1m_l3",
    "mdl264_es_roe_fy1_r1m_l3",
    "mdl264_es_sale_fy1_r1m_l3",
    "mdl264_es_ebit_ntm_r1m_l3",
    "mdl264_es_roe_ntm_r1m_l3",
    # 技术/量价组
    "mdl264_1l_bb",
    "mdl264_1l_ips",
    "mdl264_1l_lda",
    "mdl264_1l_im",
    "mdl264_1l_m1m21_ntr",
    "mdl264_1l_fmc",
    "mdl264_macd_l3",
    "mdl264_lottery_l3",
    "mdl264_amihud_l3",
    # news/eps/基本面
    "mdl264_news_abno_sent_1d_l3",
    "mdl264_news_sentvol_1d_l3",
    "mdl264_eps_sur_decay_l3",
    "mdl264_bookp_l3",
]

missing = [c for c in cands if c not in valid]
print("missing:", missing)
assert not missing, "field not found"

items = []
# 1-8 单信号（es l3 看涨 + 技术正/反）
items.append({"code": f"rank({cands[0]})"})                       # bps fy1 r1m l3
items.append({"code": f"rank({cands[1]})"})                       # cfps fy1 r1m l3
items.append({"code": f"rank({cands[2]})"})                       # dps fy1 r1m l3
items.append({"code": f"rank({cands[3]})"})                       # ebit fy1 r1m l3
items.append({"code": f"rank({cands[4]})"})                       # ebit ntm r1m l3
items.append({"code": f"rank({cands[6]})"})                       # 1l_bb
items.append({"code": f"rank({cands[7]})"})                       # 1l_ips
items.append({"code": f"rank({cands[8]})"})                       # 1l_lda
items.append({"code": f"subtract(0, rank({cands[9]}))"})          # 1l_im 反转
items.append({"code": f"rank({cands[10]})"})                      # 1l_m1m21_ntr
items.append({"code": f"rank({cands[11]})"})                      # 1l_fmc
items.append({"code": f"rank({cands[12]})"})                      # macd_l3
items.append({"code": f"subtract(0, rank({cands[13]}))"})         # lottery_l3 反转
items.append({"code": f"subtract(0, rank({cands[14]}))"})         # amihud_l3 反转
items.append({"code": f"rank({cands[15]})"})                      # news abno sent l3
items.append({"code": f"rank({cands[16]})"})                      # news sentvol l3
items.append({"code": f"rank({cands[17]})"})                      # eps sur decay l3
items.append({"code": f"rank({cands[18]})"})                      # bookp l3
# 19-22 混合
items.append({"code": f"add(0.34 * rank({cands[0]}), 0.33 * rank({cands[3]}), 0.33 * rank({cands[1]}))"})
items.append({"code": f"add(0.34 * rank({cands[6]}), 0.33 * rank({cands[8]}), 0.33 * rank({cands[7]}))"})
items.append({"code": f"add(0.5 * rank({cands[0]}), 0.5 * rank({cands[6]}))"})
items.append({"code": f"add(0.34 * rank({cands[15]}), 0.33 * rank({cands[16]}), 0.33 * rank({cands[17]}))"})
# 23-24 ts_av_diff
items.append({"code": f"rank(ts_av_diff({cands[6]}, 20))"})
items.append({"code": f"rank(ts_av_diff({cands[0]}, 20))"})

out = r"D:\coding\traeCN_project\wqb\tracking\GBR\candidates\gbr_wave27_model264_items.json"
json.dump(items, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
uniq = [it["code"] for it in items]
json.dump(uniq, open(
    r"D:\coding\traeCN_project\wqb\tracking\GBR\candidates\_wave27_uniq_exprs.json",
    "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("items:", len(items))
for it in items:
    print(it["code"][:110])
