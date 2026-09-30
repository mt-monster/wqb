# -*- coding: utf-8 -*-
"""w15: KOR/Sentiment —— 依据平台论坛（nip族点亮news塔 / 双字段Sentiment）重写。

论坛方法论（91-vote 两帖）：
  A. 相关性算子 + FAST neutralization 最适合 news/sentiment 数据
     -> ts_corr(fld, returns, ndays) / ts_covariance(fld, returns, ndays)
     -> ts_regression(returns, fld, ndays, lag=0, rettype=2)
  B. 双字段互相参照三步骤：合并(差/和/cov) -> 时序算子 -> 横截面算子
     模板1 group_rank(ts_delta(a-b, d), group)
     模板2 group_neutralize(quantile(ts_covariance(a, b, d)), group)
     模板3 -ts_zscore(ts_std_dev(a-b, d1), d2)
     模板4 group_scale(ts_arg_max(-(a+b), d), group)

字段（KOR news_sentiment_transfer, 23 个, cov 0.9654）：
  primary_sentiment_average / secondary_sentiment_average  (最热, 17/15 users)
  sentiment_score_average / _median / _minimum / _maximum
  news_article_count / normalized_news_article_count
"""
import json, os

R = r"D:\coding\traeCN_project\wqb\tracking\reference"

PA = "primary_sentiment_average"
SA = "secondary_sentiment_average"
SAVG = "sentiment_score_average"
SMED = "sentiment_score_median"
SMIN = "sentiment_score_minimum"
SMAX = "sentiment_score_maximum"
NAC = "news_article_count"

items = []

# ============ A 组：相关性算子路线（论坛首推）============
# ts_corr(field, returns, ndays)  —— 情绪与收益的滚动相关
for d in (66, 126, 252, 504):
    items.append((f"A1_corr_PA_r{d}", f"rank(multiply(-1, ts_corr({PA}, returns, {d})))"))
    items.append((f"A2_corr_SA_r{d}", f"rank(multiply(-1, ts_corr({SA}, returns, {d})))"))
items.append(("A3_corr_SM_r252", f"rank(multiply(-1, ts_corr({SAVG}, returns, 252)))"))
items.append(("A4_corr_SMED_r252", f"rank(multiply(-1, ts_corr({SMED}, returns, 252)))"))

# ts_covariance(field, returns, ndays) —— 情绪冲击的协动幅度
for d in (126, 252, 504):
    items.append((f"A5_cov_PA_r{d}", f"rank(multiply(-1, ts_covariance({PA}, returns, {d})))"))
items.append(("A6_cov_SA_r252", f"rank(multiply(-1, ts_covariance({SA}, returns, 252)))"))

# ts_regression(returns, field, ndays, lag=0, rettype=2) —— 情绪对收益的敏感度
for d in (126, 252):
    items.append((f"A7_reg_PA_r{d}", f"rank(multiply(-1, ts_regression(returns, {PA}, {d}, lag=0, rettype=2)))"))
items.append(("A8_reg_SA_r252", f"rank(multiply(-1, ts_regression(returns, {SA}, 252, lag=0, rettype=2)))"))

# ============ B 组：双字段参照（论坛三步骤）============
# 模板1：两字段差值的时序变化
for d in (5, 22, 66):
    items.append((f"B1_delta_PA_SA_{d}",
                  f"group_rank(ts_delta({PA} - {SA}, {d}), subindustry)"))
    items.append((f"B2_delta_avg_med_{d}",
                  f"group_rank(ts_delta({SAVG} - {SMED}, {d}), subindustry)"))

# 模板2：两字段是否一起变化（协动）
for d in (66, 252):
    items.append((f"B3_cov_PA_SA_{d}",
                  f"group_neutralize(quantile(ts_covariance({PA}, {SA}, {d})), subindustry)"))

# 模板3：差值的稳定性（越低越稳 -> 取负）
for d1, d2 in ((22, 66), (66, 252)):
    items.append((f"B4_std_PA_SA_{d1}_{d2}",
                  f"multiply(-1, ts_zscore(ts_std_dev({PA} - {SA}, {d1}), {d2}))"))

# 模板4：组合后的极值时间
items.append(("B5_argmax_PA_SA_126",
              f"group_scale(ts_arg_max(multiply(-1, add({PA}, {SA})), 126), subindustry)"))

# ============ C 组：单字段 + FAST 中性化基线（对照）============
items.append(("C1_PA_neg", f"rank(multiply(-1, {PA}))"))
items.append(("C2_SA_neg", f"rank(multiply(-1, {SA}))"))
items.append(("C3_PA_z252", f"rank(multiply(-1, ts_zscore({PA}, 252)))"))
items.append(("C4_PA_mean5", f"rank(ts_mean({PA}, 5))"))

# ============ D 组：新闻量（注意力）路线 ============
items.append(("D1_nac_neg", f"rank(multiply(-1, {NAC}))"))
items.append(("D2_nac_z252", f"rank(multiply(-1, ts_zscore({NAC}, 252)))"))
items.append(("D3_corr_nac_r252", f"rank(multiply(-1, ts_corr({NAC}, returns, 252)))"))
items.append(("D4_nac_delta22", f"rank(multiply(-1, ts_delta({NAC}, 22)))"))
items.append(("D5_nac_grpsubind", f"group_rank({NAC}, subindustry)"))

assert len(items) == len({l for l, _ in items}), "label 碰撞"

out = os.path.join(R, "exprs_kor_sent_w15.json")
json.dump(items, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"wrote {len(items)} exprs -> {out}")
for l, _ in items:
    print("  ", l)
