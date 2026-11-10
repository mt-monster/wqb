# EUR 字段画像归档（profiles/）

## 命名规则
- 文件名：`eur_<category>_<dataset>_profile_<YYYYMMDD>.md`（如 `eur_institutions_institutions6_profile_20261108.md`）
- 同名 JSON 原始目录在上一级目录 `tracking/EUR/reference/eur_<dataset>_fields.json`（平台 get_datafields 全量拉取）
- 一日多次更新时后缀 `_v2`、`_v3`；数据集重跑画像必须重新拉取平台目录，禁止沿用旧 cov/userCount

## 画像必含字段（六维）
1. 字段类型（MATRIX/VECTOR/GROUP）
2. 覆盖率（平台 cov，实测口径）
3. 更新频率（从字段描述/历史回测 TO 反推，标注证据）
4. 分布特征（历史证据或 Labs 离线体检；无证据标"待 Labs"）
5. 可用性（拥挤度 userCount/alphaCount + 判死记录 + sub 闸可达性）
6. 潜在 alpha 适用性（主信号/门控/小腿/分组轴，附 EUR 实证 alpha id）

## 索引
| category | dataset | 文件 | 结论速览 |
|---|---|---|---|
| institutions | institutions6 | eur_institutions_institutions6_profile_20261108.md | ATOM 判死(S≤0.56/2Y<0)；小腿/门控可用(leAXvaLn) |
| institutions | fund_holdings_panel | eur_institutions_fund_holdings_panel_profile_20261108.md | ATOM F-数学判死(returns 2.33%)；仅门控/辅助 |
| other | techindi_model | eur_other_techindi_model_profile_20261108.md | 400+ 字段 ML 分位预测；self 锁 LL5VwgO1，需新读数 |
| risk | risk60 | eur_risk_risk60_profile_20261108.md | 5 字段证券借贷；cov 0.8168 贴 sub 闸线，ATOM 待测 |
| news | news46 | eur_news_news46_profile_20261108.md | 关注度读数已验证(Xgojww1X)；极性分判死 |
| news | news7 | eur_news_news7_profile_20261109.md | 频率计数唯一可用（同 news46 族天花板 1.3）+ TO 风险；极性禁做 → 留档不投槽 |
| news | news50 | eur_news_news50_profile_20261109.md | 与 news46 同厂同构（天花板平移）；唯一独有读数 similarity_gap 留档 → 不投槽 |
| pv | pv37 | eur_pv_pv37_profile_20261109.md | 日内 delay 不可用 + OHLCV 与 pv1 重复 + 涨跌量已判死 → 结构性排除 |
| sentiment | sentiment21 | eur_sentiment_sentiment21_profile_20261109.md | 极性统计族家族判死；唯一未试=std 分歧度（低先验留档） |
| pv | pv29 | eur_pv_pv29_profile_20261109.md | 统计聚类分组轴（非信号）+ 换轴实测无效 → 结构性排除 |
| sentiment | sentiment27 | eur_sentiment_sentiment27_profile_20261109.md | 天花板 1.33 五次确认（存量结论）+ relpopularity1 已占用 → 关闭 |
| other | other455 | eur_other_other455_profile_20261109.md | Node2Vec 图嵌入近静态 0.010-0.012（存量结论）→ 排除 |
| insiders | insiders1 | eur_insiders_insiders1_profile_20261109.md | cov 0.5512 覆盖判死 + 同族 TO 前科 → 排除 |
| other | news_sentiment_dl | eur_other_news_sentiment_dl_profile_20261109.md | 文本可读性特征 cov 0.74-0.77 覆盖判死 + 低先验 → 排除 |
| insiders | insiders12 | eur_insiders_insiders12_profile_20261108.md | cov 0.19-0.26 → 覆盖判死，不投槽 |
| model(其它cat=other) | predictive_starmine | eur_model_predictive_starmine_profile_20261108.md | arm 字段平台归属 MODEL 塔(已点亮) → 降级不投主槽 |
