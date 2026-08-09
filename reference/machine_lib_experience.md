# machine_lib.py 经验总结（来自 WQ第五六节课代码2/consultant）

## 预处理
- MATRIX: winsorize(ts_backfill(FIELD, 120), std=4)
- VECTOR: winsorize(ts_backfill(vec_avg(FIELD), 120), std=4)

## 一阶算子（12 个）
reverse, inverse, rank, zscore, quantile, normalize + ts_rank, ts_zscore, ts_delta, ts_sum, ts_std_dev, ts_mean, ts_arg_min, ts_arg_max, ts_scale, ts_quantile
窗口: [5, 22, 66, 120, 240]

## 二阶：group_ops 包裹
group_neutralize / group_rank / group_zscore，分组用 densify(pv13_*_sector)
分组变量库: market/sector/industry/subindustry + pv13_*_sector + sta1/sta2 + bucket(rank(...))

## 三阶：trade_when 事件工程（关键）
开仓事件模板:
- ts_corr(close, volume, 5/20) < 0 或 > 0/0.3/0.5
- ts_mean(volume,10) > ts_mean(volume,60)
- ts_zscore(returns,60) > 2
- group_rank(ts_std_dev(returns,60), sector) > 0.7
- ts_arg_max(close, 5/20) == 0
- ts_std_dev(returns, 5) > ts_std_dev(returns, 20)
- ts_regression(returns, F, 5/20, lag=0, rettype=2) > 0
退出事件: abs(returns) > 0.1 或 -1

区域事件库:
- USA: rp_css_business, mws82_sentiment, nws48_ssc, mws50_ssc, scl12_alltype_buzzvec, pcr_oi_270
- EUR: mdl110_analyst_sentiment, oth429_research_reports, mws84/85_sentiment, nws3_scores_posnormscr, mws36_sentiment_words_positive
- ASI: mws38_score
- GLB: mdl109_news_sent_1m, nws20_ssc/bee/qmb
- CHN: oth111_xueqiu/guba/barage 情绪
- KOR: mdl110_analyst_sentiment, mws38_score
- TWN: mdl109_news_sent_1m, rp_ess_business

## 流程
一阶批量 → prune 按字段前缀去重（每字段保留 top N）→ 二阶 group 包裹 → 三阶 trade_when
turnover 自适应 decay: tvr>0.7→decay*4; >0.6→decay*3+3; >0.5→decay*3; >0.4→decay*2; >0.35→decay+4; >0.3→decay+2

## EUR 实战应用结论（2026-08-06）
- mdl110（Analyst Sentiment + Score）是 EUR 已验证最强数据集：coverage 0.85
- 最优配方：trade_when(rank(mdl110_analyst_sentiment) > 0.75, quantile(ts_mean(winsorize(ts_backfill(mdl110_score,60),std=4),5)), -1)
  @ EUR/D1/TOP2500/INDUSTRY/decay8/trunc0.04/nan ON = sh 1.58/fit 1.06/2Y 1.35/margin 4.38bp
- 关键：**trade_when 情绪事件把 2Y 从 0.93 提到 1.35**（结构性近两年衰减的解法）
- 阈值规律：阈值越低 sharpe 越高/2Y 越低（0.6→1.72/1.13；0.75→1.58/1.35）
- 教训：STATISTICAL 中性化在 EUR 更差（2Y 0.40）；**事件表达式不支持 and 连接**（语法错误）
