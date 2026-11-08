# EUR / TOP2500 / D1 · 全量数据集清单（穷尽式盘点）

> 数据源：平台 `get_datasets`（region=EUR, universe=TOP2500, delay=1）实时拉取。
> 采集时间：2026-11-06。**总计 173 个数据集 / 14 个 category**。
> 用法：按 category 逐行做字段画像 → 按画像匹配模板 → 派发。`画像状态` 列由后续轮次回填。
> **画像进度：80 / 173（2026-11-06 §277 更新）**。已全覆盖的 category：insiders 3/3、risk 5/5、socialmedia 2/2、macro 2/2、earnings 2/2、institutions 2/2、imbalance 1/1。剩余 TODO 集中在 model 46（已点亮塔，不选）、pv 15、news 11、analyst 8（已点亮塔，不选）、fundamental 7（已点亮塔，不选）、other 6、sentiment 2、insiders 0。

## 一、category 汇总

| category | 数据集 | 字段总数 | 累计 alphaCount | 画像完成 |
|---|---|---|---|---|
| model | 46 | 9242 | 181662 | 0/46 |
| other | 36 | 3841 | 48180 | 31/36 |
| news | 20 | 922 | 24046 | 9/20 |
| pv | 20 | 5972 | 415416 | 5/20 |
| analyst | 16 | 8251 | 358068 | 8/16 |
| fundamental | 13 | 6019 | 68991 | 6/13 |
| risk | 5 | 370 | 213876 | **5/5** |
| sentiment | 5 | 356 | 12586 | 3/5 |
| insiders | 3 | 51 | 5704 | **3/3** |
| earnings | 2 | 73 | 4672 | 2/2 |
| institutions | 2 | 41 | 2133 | 2/2 |
| macro | 2 | 34 | 2923 | **2/2** |
| socialmedia | 2 | 51 | 3404 | **2/2** |
| imbalance | 1 | 2 | 15748 | 1/1 |

## 二、逐数据集清单（按 category，内按 alphaCount 降序）

| category | dataset | 字段数 | coverage | alphaCount | userCount | valueScore | 画像状态 |
|---|---|---|---|---|---|---|---|
| analyst | analyst69 | 813 | 0.648 | 184267 | 4963 | 1 | TODO |
| analyst | analyst4 | 776 | 0.6638 | 104719 | 3427 | 1 | TODO |
| analyst | analyst7 | 1111 | 0.5 | 30643 | 2541 | 1 | TODO |
| analyst | analyst15 | 1744 | 0.511 | 17755 | 2335 | 2 | TODO |
| analyst | analyst10 | 961 | 0.7695 | 7817 | 2176 | 2 | TODO |
| analyst | analyst39 | 24 | 0.8755 | 4304 | 869 | 2 | TODO |
| analyst | analyst14 | 121 | 0.5 | 3371 | 997 | 1 | TODO |
| analyst | analyst_consensus | 1929 | 0.7027 | 1626 | 655 | 3 | TODO |
| analyst | analyst_factor_signals | 108 | 0.5458 | 1191 | 504 | 2 | ✅★ 盈利预测因子 108字段 cov0.22–0.48，ac≤24 白地：trend_slope 1–4yr / zscore(意外) / change_1mo / skewness / coeff_var / asymmetry ⇒ A7修正动量+A4意外+A6分歧+A9偏度 |
| analyst | analyst11 | 445 | 0.8489 | 939 | 403 | 3 | ✅ ESG 评分族 445字段 cov0.78–0.91：anl11_2_e/g（E/G 综合分 ac8–15）+ 子项 KPI ⇒ ESG 水平量/动量（Hong-Kacperczyk 罪恶股溢价） |
| analyst | analyst9 | 111 | 0.6166 | 645 | 210 | 2 | ⚠️ 一致预期面板（dataitemvalue + effectivetime）需键过滤，cov0.56 |
| analyst | analyst45 | 61 | 1 | 397 | 245 | 2 | ✅ 投资想法绩效 61字段 cov1.0：net_market_exposure(ac158)/jensensalpha/bias_weighted_ret ⇒ 持仓暴露 |
| analyst | analyst_base_ref | 17 | 0.5523 | 228 | 148 | 3 | ✅ 一致预期+股数 17字段 cov0.32/0.97：consensus_surprise_percentage_annual(ac6)/stddev/issued_shares(80) |
| analyst | analyst40 | 22 | 0.301 | 74 | 45 | 5 | ✅ 董事会结构 22字段 cov0.27–0.36：turnoverrate/age/genderratio ⇒ 治理模板（覆盖薄） |
| analyst | model52 | 3 | 0.1986 | 48 | 31 | 5 | ⚠️ 信用违约概率 3字段 cov0.1986，覆盖过薄 |
| analyst | analyst81 | 5 | 0.2402 | 44 | 30 | 5 | ✅ 边缘：违约概率族 cov0.23 |
| earnings | earnings6 | 66 | 0.8203 | 3367 | 990 | 1 | ✅ 财报日历+实际EPS 66字段：日期类为主（ern6_*q），数值仅 eps_change_percentage(9)/absolute(16) ⇒ 事件时点工具，非信号主体 |
| earnings | earnings_sent_matrix | 7 | 0.5062 | 1305 | 578 | 1 | ⚠️ 电话会语气 7字段 cov0.5062：method1(ac432)/method2(222)/正负概率 ⇒ A14双口径差（拥挤） |
| fundamental | fundamental17 | 523 | 0.7054 | 27988 | 4353 | 1 | TODO |
| fundamental | fundamental23 | 2332 | 0.6641 | 22017 | 3971 | 1 | TODO |
| fundamental | fundamental28 | 1605 | 0.5 | 8992 | 2089 | 1 | TODO |
| fundamental | fundamental6 | 279 | 0.5 | 5175 | 1450 | 1 | TODO |
| fundamental | fundamental72 | 876 | 0.4976 | 2722 | 1095 | 2 | TODO |
| fundamental | other401 | 65 | 0.707 | 952 | 380 | 2 | DONE · 65 全 MATRIX 会计质量族(cov 0.68–0.88)：**game_noa(0.858/aC20)、game_asset_turnover_chg(0.859/16)、game_equity_dilution(0.862/57)、game_receivable_days(0.865/6)、game_earning_smooth(0.759/5)、game_optimism_sale(0.833/5)** ⇒ 应计/稀释/效率经典异象、aC 极低；FUNDAMENTAL 塔已 3/3 点亮，仅作品质备份 |
| fundamental | fundamental90 | 66 | 0.4825 | 610 | 305 | 2 | HOLD · get_datafields 返回 **0 字段**（全被 sharpe 过滤或字段不可用）⇒ 暂挂，不投入批次 |
| fundamental | fundamental1 | 183 | 0.5096 | 380 | 196 | 4 | TODO |
| fundamental | fundamental25 | 8 | 0.2596 | 56 | 30 | 4 | ⚠️ 运营指标 key-value 面板，需 metriccode 过滤，低优先 |
| fundamental | fundamental93 | 46 | 0.3285 | 34 | 19 | 5 | ⛔ EUR不深挖：税应计/BTD 探针 S−0.24 + 欧洲应计异象论文否定；迁美国区 |
| fundamental | other452 | 29 | 0.3727 | 26 | 13 | 5 | ⛔ =fnd93 同源递延税率矩阵版，同判 |
| fundamental | fundamental22 | 1 | 0.6866 | 24 | 22 | 4 | ✅ 单字段 ESG KPI fnd22_value(cov0.69,ac26) |
| fundamental | digital_ad_spend | 6 | 0.1725 | 15 | 12 | 5 | ⛔ cov0.1725 过低 |
| imbalance | imbalance5 | 2 | 0.5545 | 15748 | 2835 | 1 | ⚠️ 仅2字段，imb5_score ac15128 极拥挤 |
| insiders | insiders1 | 9 | 0.5512 | 2782 | 724 | 2 | DONE · 9 全 VECTOR cov 0.5512：原始内部人交易记录（gvkey/holdings/price/shares/**tradesignificance**(aC 379)/value/valueeur/max_trade_price/currency_code）⇒ 事件型、需 vec_* 聚合、cov 偏低、aC 高 ⇒ **低优先** |
| insiders | insiders12 | 8 | 0.2008 | 1599 | 587 | 2 | DONE · 8 全 VECTOR **cov 仅 0.19–0.26**：mktprice/percent/positionchangetransactionamount/sharesheld/transactioncode + option_exercise_price_{eur,gbp,reported} ⇒ **覆盖率远低于 0.7 判死线，且以期权行权价元数据为主 ⇒ 判死，不投入批次** |
| insiders | insider_agg_matrix | 34 | 0.6116 | 1323 | 538 | 2 | DONE · 34 全 MATRIX、cov 统一 0.6116。四层结构：①**总量族** `total_{,secondary_,top_,secondary_top_}{buy,sell}_shares`（aC 34–122）②**均值族** `avg_*` 同前缀（aC 40–138）③**显著值族** `significant_value_1..4`（aC 40–62）/`top_significant_value_1..4`（aC 12/60/136/122）④**方向显著值族** `directional_*`。★★ **aC 最低的干净字段 = `top_significant_value_2`(12)、`total_secondary_sell_shares`(34)、`total_secondary_top_buy_shares`(39)、`avg_secondary_top_buy_shares`(40)、`total_secondary_top_sell_shares`(42)、`avg_secondary_buy_shares`(45)** ⇒ 这是本集剩余白地（「高管直接持有」的次级口径比总口径冷 3–4 倍）。⚠ **毒字段族 `directional_indicator` / `directional_indicator_2` / `directional_significant_value_1..4` 一律回避**。★ 本集是当前唯一出货集：`A1VxEZ1d`(S1.96/F1.00/2Y1.63) 与 `xArvZPNq`(S2.17/F1.14/2Y2.19) 的强腿都出自这里 |
| institutions | institutions6 | 11 | 0.9915 | 1394 | 559 | 2 | ✅★ 覆盖王 cov0.9976：机构买入家数(ac331)/卖出家数(327)/持有人数/持股金额 ⇒ A4持股广度+A6方向纯度（论坛37137602566679） |
| institutions | fund_holdings_panel | 30 | 0.8805 | 739 | 339 | 2 | ✅ 基金持仓面板 30字段 cov0.84–0.92：持仓/交易HHI、边界交易、large_trade、conviction ⇒ 集中度模板 |
| macro | macro27 | 33 | 0.3273 | 1696 | 553 | 2 | DONE · 33 全 VECTOR、**cov 0.15–0.43 极薄**（LinkUp 招聘岗位面板）：`mcr27_company_jobsactive`(aC **537**，唯一被开采过的)/`num_jobs_active`(48)/`company_ajnet`(5)/`num_jobs_created`(8)/`num_jobs_removed`(6)/`avg_days_job_posting_active`(18)/`mean_days_job_active`(13)；另大量元数据/质量标志 `verified_ds1..4`/`normalizedflag`/`postlength2`/`zip`/`country`/`companyidmap`/`bucket_*`(cov 0.15)。⇒ **信号主体 = 招聘数水平与其净变化（hiring rate 代理）；有效字段仅 6–8 个**。⚠ EUR 招聘面已实测判死（`N1NrOvYX` S 0.31 / `zq3mW1lo` S −0.88）**且主因是 cov 0.35–0.43 太薄**，与模板无关 ⇒ **MACRO 塔不从此集补位**，需换 macro 的另一集或换 category |
| macro | macro10 | 1 | 1 | 1227 | 415 | 2 | ⛔ 单字段 mcr10_value 泛值，需键过滤 |
| model | model38 | 145 | 0.7774 | 69401 | 4421 | 1 | TODO |
| model | model26 | 671 | 0.7478 | 47165 | 3582 | 1 | TODO |
| model | model25 | 417 | 0.5954 | 11324 | 2017 | 2 | TODO |
| model | model110 | 8 | 0.8525 | 9094 | 999 | 1 | TODO |
| model | model77 | 150 | 0.7826 | 6288 | 1062 | 3 | TODO |
| model | model138 | 120 | 0.5537 | 5218 | 1150 | 2 | TODO |
| model | model39 | 24 | 0.8044 | 3095 | 947 | 1 | TODO |
| model | predictive_starmine | 638 | 0.798 | 3023 | 853 | 3 | TODO |
| model | analyst_revision_horizons | 1089 | 0.6885 | 2739 | 642 | 4 | TODO |
| model | other460 | 1393 | 1 | 2433 | 397 | 3 | TODO |
| model | model30 | 77 | 0.713 | 2354 | 816 | 2 | TODO |
| model | model37 | 87 | 0.6978 | 2048 | 632 | 2 | TODO |
| model | model31 | 74 | 0.6672 | 1952 | 586 | 2 | TODO |
| model | global_seasonal_model | 449 | 0.9886 | 1934 | 642 | 4 | TODO |
| model | model264 | 1393 | 1 | 1918 | 391 | 4 | TODO |
| model | model50 | 168 | 0.8551 | 1486 | 576 | 2 | TODO |
| model | model135 | 137 | 0.5525 | 1421 | 419 | 3 | TODO |
| model | analyst_earnings_ibes | 42 | 0.9976 | 1092 | 330 | 3 | TODO |
| model | ai_equity_alpha | 582 | 0.8601 | 1056 | 501 | 4 | TODO |
| model | stock_alpha_model | 9 | 0.5545 | 886 | 376 | 2 | TODO |
| model | ai_factor_transfer | 20 | 1 | 828 | 350 | 2 | TODO |
| model | model28 | 83 | 0.8708 | 770 | 308 | 3 | TODO |
| model | model243 | 4 | 0.7494 | 415 | 218 | 2 | TODO |
| model | model36 | 43 | 0.8509 | 373 | 200 | 2 | TODO |
| model | model144 | 2 | 0.5511 | 361 | 203 | 3 | TODO |
| model | model354 | 236 | 1 | 355 | 202 | 4 | TODO |
| model | chart_cnn_alpha | 122 | 0.6916 | 339 | 199 | 4 | TODO |
| model | quant_factor_lib | 126 | 0.5117 | 326 | 101 | 5 | TODO |
| model | model238 | 44 | 0.8702 | 318 | 129 | 4 | TODO |
| model | model16 | 24 | 0.635 | 207 | 113 | 3 | TODO |
| model | multi_source_model | 60 | 0.5785 | 194 | 118 | 4 | TODO |
| model | shortinterest6 | 11 | 1 | 179 | 78 | 2 | TODO |
| model | multifactor_return_pred | 648 | 0.568 | 177 | 122 | 5 | TODO |
| model | event_stock_model | 3 | 0.5463 | 153 | 90 | 3 | TODO |
| model | model27 | 14 | 0.8931 | 143 | 78 | 2 | TODO |
| model | price_signal_dl | 28 | 0.9729 | 126 | 71 | 5 | TODO |
| model | behavioral_signals | 7 | 0.557 | 117 | 77 | 4 | TODO |
| model | model68 | 4 | 0.5515 | 72 | 58 | 4 | TODO |
| model | model307 | 15 | 0.625 | 62 | 44 | 4 | TODO |
| model | model140 | 3 | 0.5077 | 58 | 39 | 4 | TODO |
| model | model313 | 8 | 0.6624 | 50 | 32 | 3 | TODO |
| model | option_chart_model | 39 | 0.4352 | 32 | 19 | 6 | TODO |
| model | model257 | 8 | 0.323 | 31 | 25 | 3 | TODO |
| model | other351 | 3 | 0.3262 | 20 | 18 | 3 | TODO |
| model | model182 | 7 | 0.4381 | 17 | 15 | 6 | TODO |
| model | london_sentiment | 7 | 0.1634 | 12 | 10 | 6 | TODO |
| news | news18 | 124 | 0.61 | 11285 | 2122 | 1 | TODO |
| news | news7 | 118 | 0.715 | 4833 | 1148 | 1 | TODO |
| news | news21 | 47 | 0.5266 | 1326 | 526 | 1 | TODO |
| news | news31 | 53 | 0.7843 | 1172 | 471 | 1 | TODO |
| news | news17 | 88 | 0.7824 | 966 | 396 | 2 | TODO |
| news | news46 | 30 | 0.9382 | 764 | 384 | 2 | TODO |
| news | news50 | 37 | 0.8227 | 628 | 261 | 2 | TODO |
| news | news59 | 2 | 0.9505 | 499 | 168 | 1 | DONE · 仅 2 字段：mws59_event_fiscal_year / mws59_event_time_value ⇒ **纯元数据，无信号价值，判死** |
| news | news20 | 68 | 0.8079 | 461 | 196 | 3 | DONE · 64 全 VECTOR；两套口径：`nws20_*`(cov 0.72) 与 `nws20_multiple_comp_[d1_]*`(cov 0.96/0.84)。可用数值：event_sentiment_score / event_relevance / event_similarity_days(重复新闻距今天数=新奇度代理) / nip(影响度) / qcm。**全 event 型，ts_mean/ts_backfill 可能不支持（news46 mws46_mcp 前科）⇒ 先探针** |
| news | news85 | 22 | 0.8387 | 427 | 214 | 2 | DONE · **22 字段里 20 个 MATRIX cov 0.8387**（仅 2 个 raw_score 为 VECTOR 0.7182）：双情绪通道 `sentiment1_*` / `sentiment2_*` × {aggregate_total, average_value, median_value, central_tendency, distribution_skewness, lowest_score, highest_score} + `aggregate_sentiment_total` / `sentiment_overall_{average,median,minimum}` / `peak_sentiment_value` / `sentiment_distribution_skewness` / `headline_item_count`(aC 120) / `normalized_headline_count`。**aC 仅 6–37（分布矩族）⇒ 几乎未挖；有「总量(水平量)+均值+偏度+极值+条数」五种几何** |
| news | news23 | 136 | 0.4462 | 278 | 160 | 3 | ⚠️ 融资事件（发行价/投资轮/可转债比）cov0.19–0.77，需事件过滤 |
| news | news84 | 23 | 0.7811 | 263 | 160 | 2 | ✅ 新闻情绪转移族 20字段 cov0.66–0.80：mean/median/max/min/skew/sum + news_item_count(37) ⇒ A1+A9偏度+关注度 |
| news | news38 | 30 | 0.6821 | 227 | 112 | 2 | ✅ 白地 ac≤12：market_impact_indicator(8)/positive_score(1)/negative_score(5)/relevances(12) |
| news | news76 | 8 | 0.7245 | 208 | 105 | 2 | ✅ 半白地 cov0.72：mws76_score(86，−1/0/1情绪+MMN)；score_value 恒0=毒字段 |
| news | news48 | 22 | 0.6326 | 146 | 80 | 3 | TODO |
| news | news36 | 15 | 0.7713 | 144 | 83 | 2 | ✅ 白地 cov0.77：novelty(18)/sentiment_phrase_negative(26)/positive(11)/key_event_confidence(8)/relevance(8)/event_effect_magnitude(ac0) |
| news | news73 | 22 | 0.813 | 142 | 93 | 2 | TODO |
| news | news54 | 40 | 0.9002 | 106 | 60 | 4 | ✅ 低产：时间戳/日历/布尔/文本；仅 mws54_factor(ac29) |
| news | news52 | 24 | 0.4698 | 102 | 75 | 3 | TODO |
| news | news29 | 12 | 0.6888 | 69 | 45 | 3 | TODO |
| other | techindi_model | 798 | 0.9999 | 17594 | 2351 | 2 | DONE · **798 全 MATRIX、cov≈1.00（全市场稠密，无空窗风险）**。本质 = **ML 模型预测面板**，非原始技术指标。命名骨架 = `predicted_<分位>_quantile_<horizon>_<variant>_<model>` 与 `probability_<分桶>_bucket_<horizon>_label_<0..4>_<model>`：①`predicted_first..fifth_quantile_{one,five,ten}_day_return_{13,14,15,16,17,18,131,141,142}` = 各分位的预测收益（连续回归输出）②`probability_<bucket>_<horizon>_label_<k>_<model>` = 落入第 k 桶的 softmax 概率 ③`tm_{15..19}_r1_r5_r10_rh_{glb,ah3}_d1_r{1,5,10}_q{1..5}(_p0..p4)` = 另一套「回归输出 q1 / 分桶指派 q2..q5 / log-softmax 分量 _p0.._p4」命名。★ **aC 极不均匀：连续回归输出 q1 最挤（`predicted_first_quantile_five_day_return_14` aC 1185、`predicted_fifth_quantile_five_day_return_14` 1460），而 `probability_*_label_two_*`/`_three_*` 桶概率最冷（aC **0–27**，大量 0–5）** ⇒ **白地在概率桶侧，不在预测收益侧**。⇒ 模板方向（结构互异，非换窗口）：①**分位价差** `predicted_fifth − predicted_first`（模型预测的截面离散度/多空强度）②**概率桶价差** `probability_label_zero − probability_label_four`（最悲观桶 vs 最乐观桶，抗回归量纲）③**概率熵/分歧** `−ts_std_dev(概率桶向量,22)` ④**预测分位指派的变化** `ts_delta(q2 指派,5)`（模型判断迁移）⑤**log-softmax 置信度** `_p{k}` 的极值作门控。⚠ 全为**预测值非观测值** ⇒ 与真实收益天然高相关风险，prod 需重点验；且 `tm_*` 与 `predicted_*` 是**两套独立模型**，二者背离本身可作信号（模型间分歧） |
| other | other335 | 10 | 0.5589 | 16431 | 2352 | 1 | ⚠️ 预建模型分(hedge/SHIELD/MIND/linear) cov0.43–0.68，ac≤6188 极拥挤 |
| other | other455 | 1500 | 0.9599 | 3407 | 753 | 3 | ✅★ **画像完成（§other455-W1）**：1500字段 = `oth455_<relation>_<param>_<w>_<output>`，relation∈{competitor,customer,partner,relation}(cov 0.9705/0.8691/1.0/—)、param∈{n2v_p10_q50,p10_q200,p50_q50,p50_q200,roam}、w=w1..w5（**5 次独立随机游走**）、output∈{`pca_fact1..3_value`(MATRIX 信号腿) , `kmeans_cluster_{5,10,20}` 与 `pca_fact{k}_cluster_{5,10,20}`(GROUP 分组轴)}。★ 三条天然轴：**关系轴**（供应链 Cohen-Frazzini / 国际证据 Rizova FAJ 2010）、**超参数轴**（长窗 vs 短窗嵌入漂移）、**实现轴**（w1..w5 集成方差）。12 个结构互异模板已落 `tracking/EUR/s1_other455_wave1_template_pool.md`。派发：B1 `1FQeLB4jS5ifaqcoLfJ5imq`(T2+T1) / B2 `2gEyuF8vI4OCajbFb20DeAy`(T4+T6) / B3 `3ogMlqaIQ4kuasF1bHjQTcaq`(T7+T8) ⇒ **6 个结构互异骨架全部 S ≤ 0.31（最优 T1 0.31、T4 −0.05），TO 仅 2.7–3.5% ⇒ 信号腿判死**；换分组轴（industry→cluster_20）反而 0.31→0.22，证明该因子与行业高度共线。**GROUP 字段（~1100 个）保留作外挂分组轴**，但属 OTHER×其它两塔混合，受配额约束。 |
| other | dl_riskfree_returns | 133 | 0.9429 | 3310 | 1029 | 2 | TODO |
| other | earningscall_sentiment | 167 | 0.5061 | 1236 | 495 | 2 | ✅★ 167字段 cov0.5115：主题×章节(P/Q/A/Summary)×极性 ⇒ A5 Q&A−Presentation章节差 |
| other | insider_matrix | 33 | 0.6107 | 1206 | 424 | 3 | DONE · 33 全 MATRIX(cov 0.6068/0.6149)：`eur_[top_][director_]{value,signal_value}_1..4`；**最少开采子族 `eur_top_director_value_1..4` aC 6–11**；`eur_signal_value_*` aC 119–308 已饱和 |
| other | euro_equity_imbalance | 31 | 0.3089 | 957 | 363 | 3 | ✅ 31字段 cov0.3175：参与者级主动买卖+HHI集中度 |
| other | insider_feats | 118 | 0.5447 | 526 | 247 | 4 | DONE · 118 全 MATRIX；**A 族金额买卖比 13 字段 cov 0.9157/aC 4–23**（主用）；计数族 D/E cov 0.16–0.72 先验死；§273-F 开波 |
| other | insider_trx_matrix | 33 | 0.6109 | 470 | 218 | 4 | DONE · 33 全 MATRIX：笔数族(mean/total × buy/sell × top/secondary) + `usd_[top_]*_signal_value`(**aC 2–8 最少开采**)；⚠ `directional_indicator_score` 与毒字段同族 ⇒ 回避 |
| other | other424 | 3 | 0.6935 | 351 | 154 | 3 | ✅ 股息增长因子分(GRID ac237)+divyld+mktcap，cov0.70 ⇒ A1 |
| other | other567 | 224 | 0.4665 | 284 | 173 | 5 | TODO |
| other | acquisition_model | 15 | 0.7484 | 280 | 166 | 3 | ✅ 并购目标概率 cov0.7484：valuation(124)/country(23)/global(13)/size/credit/text 四轴 |
| other | ai_news_scores | 105 | 0.7924 | 251 | 149 | 4 | ✅ 105字段 cov0.7924：情绪均值+95%置信上下界+离散度+极值 ⇒ 置信度加权/A9 |
| other | event_sentiment_signals | 26 | 0.3567 | 184 | 110 | 5 | DONE · 26 全 VECTOR cov 0.3567；事件计数(event_count_in_section_aggregation) + 事件权重(event_weight_aggregation) + 负面事件计数(负向) ⇒ 密度/权重两族；**cov<0.4 属论坛判死区，优先级低** |
| other | other571 | 30 | 0.7585 | 156 | 96 | 4 | ✅ Wikipedia浏览 25字段 cov0.78：1d/7d/14d/28d/84d/1y×时段/设备 ⇒ A13自归一 |
| other | other296 | 19 | 0.5649 | 151 | 92 | 3 | ✅ 电话会情绪 16字段 cov0.56：prob_neg/ntr/sentiment/topic_count |
| other | other315 | 32 | 0.5191 | 137 | 69 | 4 | ⛔ OTC衍生品合约枚举(notional/strike/format)，机制弱 |
| other | other128 | 18 | 0.4607 | 119 | 67 | 5 | ✅ 高管任期/薪酬z-score 14字段 cov0.3893 |
| other | other699 | 7 | 0.2732 | 104 | 53 | 3 | ⛔ 机构持股变动 cov0.27，换手比值探针 S−0.11 |
| other | order_book_imbalance | 256 | 0.2122 | 98 | 40 | 5 | TODO |
| other | other545 | 4 | 0.5424 | 91 | 66 | 4 | ✅ NEMO2.0 复合分 4字段 cov0.5424：mpd动量+pln_omen NLP同业网络动量 |
| other | search_interest | 5 | 0.7815 | 88 | 54 | 3 | ✅ 标准化搜索兴趣 4字段 cov0.91 |
| other | other546 | 13 | 0.381 | 81 | 45 | 6 | ✅ 同业网络连接度 10字段 cov0.30–0.43 ⇒ 分组轴/门控 |
| other | stock_search_trends | 6 | 0.5401 | 81 | 44 | 5 | ✅★ 多窗搜索兴趣 6字段 MATRIX cov0.54(today/7d/14d/28d/84d/1y) ⇒ A13自归一天然 |
| other | other250 | 12 | 0.4899 | 77 | 58 | 5 | ✅ 电商产品 12字段 cov0.49：价格/评分/评论/畅销排名 |
| other | other327 | 3 | 0.5158 | 73 | 58 | 4 | ⚠️ 3字段 cov0.50：mktcap+SIRC敏感度，低优先 |
| other | news_sentiment_nlp | 23 | 0.9134 | 67 | 44 | 5 | ✅★ 全category最高覆盖白地 cov0.9134/ac≤13：vader(13)/sentiment_average(11)/readability族 |
| other | equity_conc_metrics | 18 | 0.1965 | 60 | 44 | 5 | ⚠️ 中介/自然人订单HHI集中度 18字段 cov0.1965，覆盖过低 |
| other | other635 | 6 | 0.6216 | 56 | 42 | 4 | ✅ 新闻标题情绪+长度 6字段 cov0.49–0.75 |
| other | other384 | 66 | 0.2803 | 51 | 31 | 5 | TODO |
| other | news_sentiment_dl | 66 | 0.7558 | 50 | 34 | 6 | DONE · 66 全 VECTOR(cov 0.744–0.772)；三族：①词情绪 max/mean/min pos·neg + entropy/stddev ②可读性 syllables/words-per-sentence/complexity/perplexity ③output_metric_1..4(未知 DL 输出，aC≤1)；aC 0–7 近乎未挖 |
| other | event_relation | 12 | 0.5769 | 45 | 22 | 5 | ✅ 实体关系强度 13字段 cov0.47–0.74(并购/合作/财务) |
| other | other436 | 3 | 0.4461 | 42 | 26 | 4 | ⛔ 仅 divyld+mktcap，价值信息重复 |
| other | equity_forum_data | 8 | 0.406 | 27 | 20 | 6 | ✅ 论坛买卖情绪+评论量+参与人数 8字段 cov0.406 ⇒ A6分歧度/A13 |
| other | workforce_flow_skills | 33 | 0.2456 | 20 | 16 | 6 | TODO |
| other | stock_cluster_dl | 5 | 0.4563 | 19 | 10 | 6 | ⛔ PCA特征无标签，不可解释 |
| pv | pv1 | 24 | 1 | 373943 | 8742 | 1 | TODO |
| pv | pv87 | 1649 | 0.5 | 15249 | 1923 | 1 | TODO |
| pv | pv37 | 251 | 1 | 7319 | 1043 | 1 | TODO |
| pv | pv13 | 73 | 0.6607 | 5867 | 1055 | 1 | TODO |
| pv | pv20 | 1475 | 0.6915 | 4496 | 1273 | 2 | TODO |
| pv | pv29 | 80 | 0.5633 | 2131 | 616 | 1 | TODO |
| pv | intraday_pv_feats | 585 | 0.9548 | 1652 | 531 | 2 | TODO |
| pv | pv47 | 2 | 1 | 1139 | 423 | 1 | ✅ 残差/特质收益 2字段 cov1.0：pv47_spret(ac553) ⇒ 残差反转/动量（与 risk68/72 同族） |
| pv | pv30 | 558 | 0.8222 | 898 | 385 | 2 | TODO |
| pv | continuation_score | 560 | 0.9924 | 759 | 326 | 4 | TODO |
| pv | pattern_scores | 504 | 0.9924 | 697 | 327 | 4 | TODO |
| pv | pv106 | 15 | 1 | 470 | 274 | 2 | ✅★ 流动性族 15字段 cov1.0：lastspreadbp(ac99)/spread/slippage/transaction_cost 百分位 ⇒ Amihud 非流动性溢价 |
| pv | pv103 | 8 | 0.9831 | 367 | 229 | 2 | DONE · 8 全 MATRIX：session_1600to1600_{final,max,min}_trade_price / volume_weighted_avg_price / market_value / total_traded_volume(**cov 1.0**) + ivam_sum / ntrd_sum(cov 0.9241)。**ntrd_sum=成交笔数（关注度/流动性代理）**；价格类需 ratios 才无量纲 |
| pv | investor_activity | 47 | 0.1644 | 220 | 133 | 4 | TODO |
| pv | pv173 | 105 | 0.3348 | 101 | 66 | 3 | TODO |
| pv | pv109 | 25 | 0.4397 | 61 | 50 | 4 | TODO |
| pv | pv141 | 2 | 0.5 | 37 | 29 | 3 | ⛔ 单字段收盘价 pv141_europe_1c |
| pv | pv149 | 1 | 1 | 10 | 7 | 5 | ⛔ 单字段状态码 pv149_status_5 |
| pv | univ1 | 6 | 1 | 0 | 0 | 5 | TODO |
| pv | univ2 | 1 | 0.67 | 0 | 0 | 5 | TODO |
| risk | risk70 | 87 | 0.9817 | 199557 | 4035 | 1 | DONE · 87 全 MATRIX、cov≈1.0。**Axioma 风格因子暴露（不是收益）**：`rsk70_mfm2_euetrd_*` 家族全覆盖 momentum/size/leverage/growth/btoq(btop)/earnqlty/earnvar/earnyild/divyild/ltrevrsl/strevrsl/indmom/resvol/srisk/srisku/shortint/newssent/analyst sn/midcap/market/cntadj/indadj/primaryindustry/season/exeurexp/midcap；aC 12k–115k 极饱和。低 aC 入口：`rsk70_mfm2_euetrd_market` 16208 / `cntadj` 17649 / `earnvar` 18613 / `leverage` 18692 / `market_cap_usd` 880。另含 40+ 行业暴露 `*_sector_exposure`（aC 106–603）、20+ 国家暴露 `country_*_exposure*`、`hedge_fund_ownership_percent_europe`(1145)/`european_hedge_fund_ownership_count`(651)/`industry_count_short`(981)、`rsk70_trsd_drteue_2mfm`=**specific returns**(aC 74493，等同残差收益，直接用=returns 墙)。⇒ **该集本质是「暴露向量」而非信号**：正确用法是 ①暴露的时序变化 `ts_delta(loading,W)` 作风格迁移/风险再平衡信号；②作**中性化/正交化基底**剥离风格；③`strevrsl`/`ltrevrsl` 暴露做反转分层。⚠ `industry_count_short`/`srtindcnt` 语义是「载荷计数」不是空头兴趣 |
| risk | risk62 | 233 | 0.9974 | 11191 | 1889 | 1 | DONE · 233 全 MATRIX：①`rsk62_1_100_val1..100`+intercept+ksrs（100 个匿名因子载荷，cov 1.0，aC 18–593）②`rsk62_1_1_100_val*`（第二套模型）③**具名暴露** `rsk62_risk_{volatility,growth,logcap,pb,mtl,mts,qe2d,spe,logadv20}`（cov 0.9348/aC 48–100）④对应 beta 族 `rsk62_beta[1]_1_100_*`（aC 25–280）⑤`rsk62_return`(aC 788)/`retseries_*`。⇒ **风险模型支持集：匿名载荷语义不明不可盲挖；具名暴露可承载 BAB(低波)/价值(pb)/规模(logcap)/动量(mtl) 经典异象**；⚠ `rsk62_return` 直接用=returns 墙 |
| risk | risk60 | 5 | 0.8168 | 1872 | 895 | 1 | ⚠️ 证券借贷 5字段 cov0.8168：rsk60_crowding(ac286)/offer(835)/last(718) ⇒ 卖空压力（极拥挤） |
| risk | risk68 | 5 | 1 | 634 | 388 | 1 | ✅ 风险模型构件 5字段 cov1.0：beta/residual_return(373)/dadv权重 ⇒ 残差反转 |
| risk | risk72 | 40 | 0.6023 | 622 | 367 | 2 | ✅ 风险模型残差收益 40字段：rsk72_top1200_dsrt(ac205)、top2500_equity_residualized_return(cov1.0) ⇒ 残差动量/反转 |
| sentiment | sentiment27 | 30 | 0.9427 | 6994 | 1203 | 2 | DONE · 30 全 VECTOR，**sentiment26 的下一代同名族（Tranco 域名排名）**：`snl27_*`（cov 0.75–0.91）+ `snt27_*`（cov 0.90–1.00）双前缀，字段名逐位对齐（avgranking/kurtosis/skewness/relpopularity08/relpopularity1/top50pctranking(avg)/top75pctranking(avg)/topranking/totaldomains/totalcountrydomains/dltcc/website）。⚠ aC 356–1055 明显高于 sentiment26（59–103）⇒ **同一机制面已被开采更狠**；且 sentiment26 所属「网页关注度」面在 EUR 已判 2021 后衰减（§272）⇒ **整集先验弱，不作主攻**，仅当需要 VECTOR 二阶矩（kurtosis/skewness）做分歧度辅助腿时取用 |
| sentiment | sentiment21 | 210 | 0.9659 | 3699 | 1167 | 2 | TODO |
| sentiment | other553 | 73 | 0.5458 | 1085 | 503 | 2 | ✅ 财报文本语言学 cov0.47–0.97：blamecnt归因/passiveratio/numericcnt/avgsentlen（p_=presentation）+ est_*估计 ⇒ 归因语言模板 |
| sentiment | sentiment26 | 17 | 0.7528 | 581 | 312 | 2 | DONE · 17 全 VECTOR；**网页人气/排名族**：relpopularity08/1(aC 91/103)、avgranking、top10/25/50/75pctranking(avg)、skewness、totaldomains/totalcountrydomains、dltcc(**cov 1.0**/aC 59)。⚠ 本区 Google Trends 关注度面已判「2021 后衰减」（§272）⇒ 同型先验弱 |
| sentiment | sentiment7 | 24 | 0.0625 | 227 | 147 | 2 | TODO |
| socialmedia | socialmedia12 | 6 | 0.7836 | 2471 | 827 | 1 | DONE · **仅 4 字段可见**（inventory 记 6）：真正信号只有 2 个 MATRIX —— `scl12_sentiment`（社媒情绪水平，cov 0.85，aC **912**）+ `scl12_buzz`（相对情绪**量/关注度**，cov 0.85，aC **884**），其余 2 个是元数据 `entity_profile_summary`/`entity_sector_name`（VECTOR cov 0.75）。★ **这是 SOCIALMEDIA 塔（EUR 0/3，全未点亮）唯一未画像的数据集，且「情绪 × 关注度」二元结构是 Barber-Odean 注意力 + Da-Engelberg-Gao FEARS 的标准形态**（buzz=异常关注 ⇒ 短期买入压力后反转）。aC 884/912 属中高拥挤但远低于 pv1(373943)/analyst69(184267)。⇒ 模板方向：情绪水平异常度、buzz 关注冲击（一阶差分）、buzz×sentiment 交互（高关注+悲观=做空）、buzz 的二阶矩（意见分歧）。**已派发首批 2 条探针（`GV1W3ea4huaos1aQ9qnuKp`）** |
| socialmedia | socialmedia15 | 45 | 0.3424 | 933 | 371 | 2 | ✅ 社媒多维情绪 45字段 cov0.26–0.37：anger/fear/optimism/stress/buzz/conflict/longshort（_d1_族 ac≤140）⇒ A6分歧度 |