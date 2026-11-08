# HKG 全数据集清单与逐 category 画像（2026-11-03，MCP get_datasets 实拉）

> 来源：`mcp__wq-brain-http__get_datasets(region=HKG, delay=1, universe=TOP800)` 一次全量拉取，共 **203** 个数据集。
> 塔位：HKG/D1/** 全部未点亮（`recommend_datasets` 实测每个 category `category_alpha_count=0`, `need_to_light=3`）。
> 塔倍率（平台塔表）：analyst/model/other **1.7** > sentiment/fundamental/news **1.6** > pv **1.5** > institutions 1.4 > earnings/risk/shortinterest 1.3 > insiders/macro 1.2 > socialmedia 1.1 > imbalance 1.0。

## 0. category 总览

| category | 数据集数 | 非目标塔? | 塔倍率 | 备注 |
|---|---:|---|---:|---|
| model | 59 | ❌(trio) | 1.7 | |
| other | 29 | ❌(trio) | 1.7 | |
| news | 24 | ✅ | 1.6 | |
| analyst | 20 | ✅ | 1.7 | |
| fundamental | 20 | ✅ | 1.6 | |
| pv | 18 | ❌(trio) | 1.5 | |
| sentiment | 8 | ✅ | 1.6 | |
| shortinterest | 7 | ✅ | 1.3 | |
| risk | 7 | ✅ | 1.3 | |
| socialmedia | 3 | ✅ | 1.1 | |
| earnings | 2 | ✅ | 1.3 | |
| institutions | 2 | ✅ | 1.4 | |
| insiders | 2 | ✅ | 1.2 | |
| imbalance | 1 | ✅ | 1 | |
| macro | 1 | ✅ | 1.2 | |

## model（59）

| dataset | 名称 | 字段 | alphaCount | userCount | cov | valueScore |
|---|---|---:|---:|---:|---:|---:|
| model77 | Analysts' Factor Model | 23 | 1 | 1 | 0.5692 | 8 |
| model307 | Global Sales Allocation Model Data | 15 | 1 | 1 | 0.4434 | 7 |
| behavioral_signals | Behavioral Finance Signal Factors | 7 | 6 | 4 | 0.768 | 7 |
| analyst_revision_horizons | Multi Horizon Analyst Revision Signals | 851 | 112 | 59 | 0.7108 | 6 |
| predictive_starmine | Predictive Analyst-Company Signal Set | 645 | 118 | 59 | 0.8486 | 6 |
| model135 | Alternative technical factor models | 137 | 80 | 51 | 0.7572 | 6 |
| model138 | Stock Selection from Accounting-based Factors | 120 | 70 | 42 | 0.7656 | 6 |
| model176 | Non-Financial Metric Models | 84 | 66 | 37 | 0.3187 | 6 |
| model37 | Text Mining Data | 79 | 43 | 22 | 0.9407 | 6 |
| model50 | International Scorings Data | 56 | 34 | 25 | 0.5692 | 6 |
| quant_factor_lib | Multi-Domain Quantitative Factor Library | 32 | 37 | 21 | 0.6649 | 6 |
| model244 | Insider Transaction Analytics | 30 | 14 | 5 | 0.5262 | 6 |
| price_signal_dl | Deep Learning Price Signal Dataset | 28 | 22 | 16 | 0.8154 | 6 |
| model141 | Interest Rate Sensitivity Measures | 10 | 8 | 5 | 0.2497 | 6 |
| model313 | Intangible Asset Factors | 9 | 12 | 5 | 0.633 | 6 |
| model68 | Risk-Alleviated Momentum Scores | 4 | 22 | 15 | 0.7592 | 6 |
| model140 | Sensitivity to the Inflation Change | 3 | 4 | 3 | 0.6656 | 6 |
| chart_cnn_alpha | Deep Learning Chart-Based Alpha | 1010 | 132 | 72 | 0.6297 | 5 |
| global_seasonal_model | Global Seasonal Regime Return Signals | 681 | 292 | 119 | 0.6982 | 5 |
| multifactor_return_pred | Multi Factor Market Return Predictions | 648 | 295 | 114 | 0.7247 | 5 |
| ai_equity_alpha | AI Equity Alpha Forecasts | 582 | 205 | 94 | 0.8803 | 5 |
| model262 | DNN prediction of fundamentals | 140 | 249 | 95 | 0.7007 | 5 |
| model216 | Analyst Revisions Model Data | 88 | 268 | 73 | 0.6838 | 5 |
| model29 | EBITDA Estimate Model | 71 | 112 | 55 | 0.6496 | 5 |
| multi_source_model | Multi-Source Market Return Prediction | 60 | 67 | 37 | 0.7269 | 5 |
| model53 | Creditworthiness Risk Measure Model | 52 | 89 | 54 | 0.8605 | 5 |
| model33 | Revenue Estimate Model | 28 | 166 | 71 | 0.6243 | 5 |
| model16 | Fundamental Scores | 24 | 32 | 27 | 0.7056 | 5 |
| other83 | Insider Transaction Analytics | 15 | 13 | 4 | 0.4042 | 5 |
| model106 | Analysts rating model | 14 | 94 | 35 | 0.347 | 5 |
| model170 | Asia Technical and Fundamental ranking model | 11 | 65 | 34 | 0.9175 | 5 |
| model207 | Asian Insider Transaction Data | 6 | 36 | 14 | 0.6354 | 5 |
| model242 | Global Quantitative Stock Selection Data | 5 | 52 | 36 | 0.9689 | 5 |
| other54 | Global Quantitative Stock Selection Data | 4 | 42 | 19 | 0.7424 | 5 |
| event_stock_model | Corporate Event Driven Stock Model | 3 | 11 | 8 | 0.7658 | 5 |
| model252 | Systematic Hedging for Investors to Evade Large Drawdowns | 3 | 26 | 19 | 0.7347 | 5 |
| model28 | Structural Credit Risk Model | 125 | 546 | 160 | 0.9692 | 4 |
| model30 | EPS Estimate Model | 51 | 306 | 125 | 0.6378 | 4 |
| model238 | SmartHoldings Model | 44 | 552 | 234 | 0.9829 | 4 |
| model36 | SmartRatios Model | 43 | 719 | 148 | 0.9793 | 4 |
| model32 | Price Momentum Model | 36 | 504 | 161 | 0.9704 | 4 |
| analyst_earnings_ibes | Global Analyst Earnings Forecasts | 28 | 177 | 81 | 1 | 4 |
| ai_factor_transfer | AI Enhanced Equity Factor Transfer | 19 | 108 | 64 | 1 | 4 |
| model144 | Stock Selection DL model | 2 | 203 | 84 | 0.7614 | 4 |
| model109 | Fundamentals and Technical Indicators Model | 542 | 989 | 255 | 0.6954 | 3 |
| model26 | Analyst Revisions | 529 | 1622 | 373 | 0.712 | 3 |
| model31 | Earnings Quality Model | 80 | 686 | 220 | 0.9663 | 3 |
| other193 | Systematic Hedging for Investors to Evade Large Drawdowns | 3 | 322 | 66 | 0.5858 | 3 |
| model139 | Inflation based stock selection model | 2 | 160 | 82 | 0.7635 | 3 |
| model25 | Earnings Quality | 365 | 5320 | 656 | 0.82 | 2 |
| other432 | DNN prediction of fundamentals | 140 | 8708 | 491 | 0.6669 | 2 |
| model38 | Growth Valuation Model | 120 | 1536 | 357 | 0.7085 | 2 |
| model250 | Nonlinear adaptive model | 20 | 1398 | 329 | 0.7643 | 2 |
| other176 | Nonlinear adaptive model | 20 | 3051 | 514 | 0.6374 | 2 |
| shortinterest6 | SmartHoldings Model | 11 | 3153 | 385 | 0.82 | 2 |
| model110 | Big data and machine learning based model | 8 | 4418 | 669 | 0.7669 | 2 |
| model243 | Combined Alpha Model | 4 | 254 | 110 | 0.9313 | 2 |
| other72 | Combined Alpha Model | 4 | 592 | 112 | 0.7421 | 2 |
| model39 | Valuation Momentum Data | 24 | 3312 | 494 | 0.8719 | 1 |

## other（29）

| dataset | 名称 | 字段 | alphaCount | userCount | cov | valueScore |
|---|---|---:|---:|---:|---:|---:|
| other571 | Wikipedia Viewing Data | 30 | 16 | 8 | 0.3861 | 7 |
| other546 | Institutional Network Analysis Dataset | 8 | 4 | 4 | 0.4464 | 7 |
| event_relation | Text-Based Event Relationship Analysis | 6 | 2 | 2 | 0.4169 | 7 |
| other455 | Relationship enhanced with AI/ML | 1500 | 297 | 115 | 0.7097 | 6 |
| mmp_nlp_sentiment | Multilingual NLP News Sentiment Signals | 521 | 61 | 40 | 0.9476 | 6 |
| ai_news_scores | AI News Sentiment Scores | 97 | 42 | 24 | 0.749 | 6 |
| other315 | Equity Swap Data | 32 | 49 | 19 | 0.2353 | 6 |
| insider_feats | Global Insider Transaction Features | 29 | 73 | 33 | 0.7039 | 6 |
| news_sentiment_nlp | News Sentiment Signal Features | 19 | 19 | 6 | 0.865 | 6 |
| news_sentiment_dl | Deep Learning News Sentiment Signals | 17 | 22 | 8 | 0.8632 | 6 |
| other78 | Earnings and conference call data | 12 | 116 | 35 | 0.8952 | 6 |
| other16 | Indications of Interest (IOI) insights dataset | 6 | 46 | 21 | 0.3656 | 6 |
| other635 | Thomson Reuters News Analytics Equities | 6 | 13 | 8 | 0.6965 | 6 |
| other545 | Linked Firms Momentum Data | 4 | 24 | 17 | 0.7381 | 6 |
| other567 | Employee Review Data | 2 | 7 | 5 | 0.2733 | 6 |
| other496 | Intraday FX rates | 107 | 281 | 86 | 0.7318 | 5 |
| other128 | Global Executive Performance Factors | 18 | 285 | 77 | 0.373 | 5 |
| acquisition_model | Corporate Acquisition Likelihood Model | 15 | 85 | 48 | 0.8264 | 5 |
| other327 | Sensitivity to Interest Rates Model | 3 | 34 | 17 | 0.6491 | 5 |
| other424 | Dividend prediction model | 3 | 42 | 26 | 0.5734 | 5 |
| other436 | Dividend model | 3 | 40 | 26 | 0.5754 | 5 |
| other532 | Specific Returns | 2 | 47 | 26 | 1 | 5 |
| other165 | Hong Kong Exchange Announcement | 1 | 32 | 13 | 1 | 5 |
| other323 | Global Equity Premarket Data | 11 | 230 | 94 | 1 | 4 |
| other543 | Shareholdings, trade statistics data | 4 | 496 | 138 | 0.8921 | 4 |
| other479 | China Classification data | 1 | 38 | 18 | 1 | 4 |
| dl_riskfree_returns | Deep Learning Risk Free Returns | 57 | 1200 | 388 | 0.6514 | 3 |
| other85 | China Flow Data | 3 | 410 | 134 | 0.686 | 3 |
| other335 | Multi-Region Dividend Alpha Model Dataset | 10 | 2875 | 582 | 0.5839 | 2 |

## news（24）

| dataset | 名称 | 字段 | alphaCount | userCount | cov | valueScore |
|---|---|---:|---:|---:|---:|---:|
| news23 | MnA Deals Data | 53 | 10 | 5 | 0.3437 | 6 |
| news38 | News Analytic Model Data | 45 | 62 | 31 | 0.8302 | 5 |
| news46 | Relevant News Analytics Data | 44 | 86 | 36 | 0.6374 | 5 |
| news36 | News Analytics Data | 43 | 50 | 26 | 0.7657 | 5 |
| news84 | Headline Sentiment Analysis using DNN | 23 | 53 | 31 | 0.7419 | 5 |
| news73 | Story by Story Sentiment | 22 | 18 | 12 | 0.8438 | 5 |
| news29 | Significant Developments Data | 12 | 23 | 13 | 0.6849 | 5 |
| other7 | Archive News Data | 11 | 22 | 13 | 0.7513 | 5 |
| news76 | Textual News Feed Data | 6 | 12 | 7 | 0.9013 | 5 |
| news79 | Global Corporate News Analytics | 85 | 319 | 123 | 0.9341 | 4 |
| news50 | Web News Analytics Data | 81 | 83 | 44 | 0.7953 | 4 |
| news31 | News Analytics on Equities | 25 | 58 | 33 | 1 | 4 |
| news20 | Web Sources News Sentiment Data | 24 | 88 | 49 | 0.6533 | 4 |
| news85 | News Sentiment Analysis using DNN | 23 | 53 | 33 | 0.7714 | 4 |
| news48 | Global Media News Data | 22 | 44 | 24 | 0.5534 | 4 |
| news3 | Dow Jones News Analytics Data | 19 | 86 | 37 | 0.8122 | 4 |
| news21 | Macro Economic Event Data | 15 | 76 | 43 | 0.6327 | 4 |
| news104 | Archive News Data | 11 | 99 | 38 | 0.8694 | 4 |
| news66 | Webpage View Statistics | 5 | 32 | 12 | 0.5 | 4 |
| news59 | Corporate Events Data | 2 | 29 | 15 | 0.8125 | 4 |
| news7 | Real Time News Feed Data | 63 | 424 | 166 | 0.8468 | 3 |
| news17 | PR Edition Data | 24 | 167 | 66 | 0.6052 | 3 |
| news18 | Ravenpack News Data | 44 | 898 | 297 | 0.6236 | 2 |
| news54 | Key Developments Data | 40 | 1245 | 231 | 0.7643 | 2 |

## analyst（20）

| dataset | 名称 | 字段 | alphaCount | userCount | cov | valueScore |
|---|---|---:|---:|---:|---:|---:|
| analyst16 | Real Time Estimates | 141 | 79 | 47 | 0.4972 | 6 |
| analyst11 | ESG scores | 126 | 31 | 23 | 0.4756 | 6 |
| analyst21 | Indicators of Interest Data | 16 | 21 | 13 | 0.4509 | 6 |
| analyst81 | Creditworthiness model | 3 | 9 | 7 | 0.211 | 6 |
| analyst_consensus | Standardized Analyst Consensus Forecasts | 1729 | 191 | 105 | 0.7045 | 5 |
| analyst45 | Analyst Trade Ideas | 241 | 44 | 21 | 0.3326 | 5 |
| analyst48 | Dividend estimation data | 69 | 55 | 35 | 0.3539 | 5 |
| analyst47 | Alternative Analyst Investment Insight Data | 17 | 89 | 38 | 0.397 | 5 |
| analyst_base_ref | Analyst Estimates Base Reference | 13 | 25 | 17 | 0.4979 | 5 |
| analyst44 | Integrated Broker Estimates | 552 | 1350 | 351 | 0.7181 | 4 |
| analyst10 | Performance-Weighted Analyst Estimates | 528 | 514 | 169 | 0.7423 | 4 |
| analyst9 | Analyst Estimate Daily Data | 48 | 98 | 57 | 0.5011 | 4 |
| analyst_factor_signals | Global Analyst Factor Signals | 25 | 133 | 82 | 0.67 | 4 |
| analyst46 | Analyst Investment insight Data | 6 | 51 | 28 | 0.4271 | 4 |
| analyst39 | Analyst estimates & financial ratios | 49 | 1038 | 350 | 0.7804 | 3 |
| analyst94 | Fundamental Income and Dividend Model | 17 | 315 | 158 | 0.4271 | 3 |
| analyst15 | Earnings forecasts | 307 | 4479 | 617 | 0.5221 | 2 |
| analyst4 | Analyst Estimate Data for Equity | 176 | 2624 | 565 | 0.6112 | 2 |
| analyst14 | Estimations of Key Fundamentals | 125 | 1416 | 410 | 0.5 | 2 |
| other423 | Fundamental Income and Dividend Model | 17 | 453 | 159 | 0.3674 | 2 |

## fundamental（20）

| dataset | 名称 | 字段 | alphaCount | userCount | cov | valueScore |
|---|---|---:|---:|---:|---:|---:|
| fundamental1 | Management and Executive Data | 118 | 12 | 10 | 0.4515 | 6 |
| fundamental22 | Environmental and Social Governance Data | 2 | 1 | 1 | 0.3112 | 6 |
| fundamental21 | ESG Scores Data | 156 | 257 | 102 | 0.5864 | 5 |
| fundamental90 | Governance, Accounting, Management, and Equality | 55 | 192 | 100 | 0.6696 | 5 |
| fundamental89 | Accrual based Earnings Model | 15 | 20 | 16 | 0.3244 | 5 |
| other395 | Accrual based Earnings Model | 15 | 11 | 6 | 0.3244 | 5 |
| fundamental93 | Earnings Tax Data | 7 | 15 | 7 | 0.297 | 5 |
| other452 | Earnings Tax Data | 7 | 13 | 8 | 0.297 | 5 |
| fundamental25 | Company Operating Metrics | 6 | 8 | 5 | 0.3141 | 5 |
| fundamental4 | Hong Kong Fundamental Data | 708 | 733 | 206 | 0.6073 | 4 |
| other401 | Governance, Accounting, Management, and Equality | 53 | 236 | 89 | 0.5404 | 4 |
| fundamental6 | Company Fundamental Data for Equity | 268 | 1509 | 358 | 0.5 | 3 |
| fundamental94 | Aggregated Fundamental Data | 150 | 560 | 227 | 0.762 | 3 |
| fundamental44 | Accounting Quality Models | 12 | 312 | 106 | 0.7315 | 3 |
| fundamental86 | Stock Reports Plus | 10 | 204 | 109 | 0.7901 | 3 |
| model56 | Stock Reports Plus | 9 | 183 | 79 | 0.7227 | 3 |
| fundamental17 | Direct Fundamental Data | 369 | 3749 | 799 | 0.9216 | 2 |
| fundamental23 | Fundamental Point in Time Data | 351 | 2998 | 611 | 0.6794 | 2 |
| fundamental28 | Global Fundamental Data | 193 | 1934 | 401 | 0.5 | 2 |
| other466 | Aggregated Fundamental Data  | 114 | 3895 | 490 | 0.7114 | 2 |

## pv（18）

| dataset | 名称 | 字段 | alphaCount | userCount | cov | valueScore |
|---|---|---:|---:|---:|---:|---:|
| pv149 | Holidays and Trading Hours Calendar | 2 | 0 | 0 | 1 | 8 |
| continuation_score | Price Chart Continuation Pattern Similarity | 560 | 227 | 110 | 1 | 5 |
| pattern_scores | Chart Pattern Similarity Scores | 504 | 151 | 74 | 1 | 5 |
| pv70 | Relation Dataset | 33 | 24 | 14 | 0.2241 | 5 |
| pv109 | Bond Yield Data | 25 | 8 | 8 | 0.2357 | 5 |
| pv173 | Corporate Bond Pricing Data | 21 | 8 | 5 | 0.2472 | 5 |
| univ1 | Universe Dataset | 2 | 4 | 2 | 1 | 5 |
| pv37 | Equity Interval Data | 691 | 1487 | 348 | 0.6937 | 3 |
| pv30 | Alternate Industry Classification | 690 | 2649 | 298 | 0.9329 | 3 |
| intraday_pv_feats | Daily Intraday Price Volume Features | 579 | 1216 | 271 | 0.9812 | 3 |
| pv13 | Relationship Data for Equity | 45 | 640 | 191 | 0.7022 | 3 |
| pv106 | Microstructure Spread Data | 29 | 425 | 127 | 0.973 | 3 |
| pv103 | Interval and MOO&MOC statistics | 7 | 154 | 79 | 1 | 3 |
| pv20 | Daily Spot and Cross Rate Data | 6 | 78 | 55 | 0.7988 | 3 |
| pv47 | Specific Return Dataset | 5 | 72 | 38 | 0.9545 | 3 |
| pv14 | Futures Market Data | 2 | 94 | 40 | 0.8526 | 3 |
| pv29 | Derived Industry Classification | 45 | 1723 | 286 | 0.5302 | 2 |
| pv1 | Price Volume Data for Equity | 24 | 38089 | 2009 | 1 | 1 |

## sentiment（8）

| dataset | 名称 | 字段 | alphaCount | userCount | cov | valueScore |
|---|---|---:|---:|---:|---:|---:|
| other553 | Financial Opinion Mining | 21 | 27 | 20 | 0.6228 | 6 |
| sentiment7 | Webpage Views  Data | 4 | 3 | 1 | 0.3594 | 6 |
| sentiment23 | Textual Sentiment Analysis Data | 156 | 124 | 59 | 0.8121 | 5 |
| sentiment21 | AI Sentiment Score Data | 138 | 187 | 90 | 0.9993 | 5 |
| news_sentiment_transfer | Transferred News Sentiment Analytics | 23 | 57 | 36 | 1 | 5 |
| sentiment26 | Website Popularity Ranking Dataset | 19 | 76 | 42 | 0.3961 | 5 |
| sentiment27 | Website Popularity Rankings | 31 | 1099 | 285 | 0.4598 | 3 |
| sentiment19 | HKEX MD&A Sentiment Classification Data | 14 | 651 | 156 | 0.562 | 3 |

## shortinterest（7）

| dataset | 名称 | 字段 | alphaCount | userCount | cov | valueScore |
|---|---|---:|---:|---:|---:|---:|
| shortinterest5 | Daily Price Limit Data | 3 | 23 | 13 | 1 | 6 |
| other58 | Hong Kong Secutiries Futures Data | 2 | 57 | 24 | 0.4746 | 5 |
| shortinterest55 | Short-Selling Dataset | 5 | 367 | 132 | 0.7898 | 4 |
| shortinterest44 | Short Sale Activity | 2 | 129 | 64 | 0.815 | 4 |
| shortinterest52 | Hong Kong Securities Futures Data | 2 | 183 | 45 | 0.6538 | 4 |
| shortinterest3 | Securities Lending Files Data | 56 | 1192 | 387 | 0.865 | 3 |
| other534 | Short-Selling Dataset | 5 | 495 | 145 | 0.8028 | 3 |

## risk（7）

| dataset | 名称 | 字段 | alphaCount | userCount | cov | valueScore |
|---|---|---:|---:|---:|---:|---:|
| risk88 | Other Multi-Factor Risk Models | 80 | 1031 | 338 | 0.9003 | 3 |
| risk59 | Securities Lending and Short Market Dynamics Dataset | 16 | 436 | 190 | 0.8843 | 3 |
| risk71 | Daily Specific Return Profiling Dataset | 9 | 172 | 83 | 0.5565 | 3 |
| risk60 | Securities Lending Insight Data | 5 | 120 | 69 | 0.8577 | 3 |
| risk72 | Specific return of extended factors | 2 | 63 | 41 | 0.5463 | 3 |
| risk68 | Forecast Data | 5 | 866 | 175 | 0.9869 | 2 |
| risk70 | Multi-Factor Model | 98 | 5069 | 810 | 0.9308 | 1 |

## socialmedia（3）

| dataset | 名称 | 字段 | alphaCount | userCount | cov | valueScore |
|---|---|---:|---:|---:|---:|---:|
| socialmedia12 | Sentiment Data for Equity | 6 | 726 | 206 | 0.5615 | 2 |
| other100 | Investor views | 1 | 173 | 77 | 1 | 2 |
| socialmedia39 | Investor views | 1 | 255 | 91 | 1 | 2 |

## earnings（2）

| dataset | 名称 | 字段 | alphaCount | userCount | cov | valueScore |
|---|---|---:|---:|---:|---:|---:|
| earnings6 | International Findings Data | 40 | 232 | 92 | 0.328 | 4 |
| earnings3 | Earnings Date Data | 8 | 1734 | 392 | 0.5983 | 1 |

## institutions（2）

| dataset | 名称 | 字段 | alphaCount | userCount | cov | valueScore |
|---|---|---:|---:|---:|---:|---:|
| fund_holdings_panel | Global Institutional Fund Holdings | 30 | 119 | 63 | 0.8135 | 4 |
| institutions6 | Institutions and Beneficial Stake Ownership | 11 | 763 | 209 | 0.9989 | 2 |

## insiders（2）

| dataset | 名称 | 字段 | alphaCount | userCount | cov | valueScore |
|---|---|---:|---:|---:|---:|---:|
| insiders1 | Global Insider Trading Data | 9 | 912 | 219 | 0.4538 | 3 |
| insiders5 | Corporate Insider Trading Activities Dataset | 1 | 232 | 100 | 0.999 | 3 |

## imbalance（1）

| dataset | 名称 | 字段 | alphaCount | userCount | cov | valueScore |
|---|---|---:|---:|---:|---:|---:|
| imbalance5 | Oil Price Resilience Scores | 2 | 1360 | 374 | 0.7652 | 1 |

## macro（1）

| dataset | 名称 | 字段 | alphaCount | userCount | cov | valueScore |
|---|---|---:|---:|---:|---:|---:|
| macro63 | Index Reconstitution Data | 1 | 93 | 38 | 1 | 4 |

## S0 数据集候选排名（口径：0.4*cov + 拥挤度罚 + 0.2*log1p(字段数) + 0.1*valueScore/10；已判死集剔除）


### sentiment（塔倍率 1.6）

| dataset | 名称 | 分 | 字段 | cov | alphaCount | 近十年可用性 |
|---|---|---:|---:|---:|---:|---|
| sentiment21 | AI Sentiment Score Data | 0.7426 | 138 | 0.9993 | 187 | ✅ 直接可用 |
| other553 | Financial Opinion Mining | 0.6986 | 21 | 0.6228 | 27 | ❌ 覆盖不足，需逐字段核 |
| news_sentiment_transfer | Transferred News Sentiment Analytics | 0.692 | 23 | 1 | 57 | ✅ 直接可用 |
| sentiment23 | Textual Sentiment Analysis Data | 0.6712 | 156 | 0.8121 | 124 | ⚠️ 需 ts_backfill / if_else 兜底 |
| sentiment7 | Webpage Views  Data | 0.5504 | 4 | 0.3594 | 3 | ❌ 覆盖不足，需逐字段核 |
| sentiment26 | Website Popularity Ranking Dataset | 0.4452 | 19 | 0.3961 | 76 | ❌ 覆盖不足，需逐字段核 |
| sentiment19 | HKEX MD&A Sentiment Classification Data | 0.3832 | 14 | 0.562 | 651 | ❌ 覆盖不足，需逐字段核 |
| sentiment27 | Website Popularity Rankings | 0.3642 | 31 | 0.4598 | 1099 | ❌ 覆盖不足，需逐字段核 |

### risk（塔倍率 1.3）

| dataset | 名称 | 分 | 字段 | cov | alphaCount | 近十年可用性 |
|---|---|---:|---:|---:|---:|---|
| risk59 | Securities Lending and Short Market Dynamics Dataset | 0.6157 | 16 | 0.8843 | 436 | ⚠️ 需 ts_backfill / if_else 兜底 |
| risk60 | Securities Lending Insight Data | 0.5749 | 5 | 0.8577 | 120 | ⚠️ 需 ts_backfill / if_else 兜底 |
| risk88 | Other Multi-Factor Risk Models | 0.5673 | 80 | 0.9003 | 1031 | ✅ 直接可用 |
| risk70 | Multi-Factor Model | 0.5353 | 98 | 0.9308 | 5069 | ✅ 直接可用 |
| risk68 | Forecast Data | 0.5166 | 5 | 0.9869 | 866 | ✅ 直接可用 |
| risk71 | Daily Specific Return Profiling Dataset | 0.4693 | 9 | 0.5565 | 172 | ❌ 覆盖不足，需逐字段核 |
| risk72 | Specific return of extended factors | 0.4303 | 2 | 0.5463 | 63 | ❌ 覆盖不足，需逐字段核 |

### institutions（塔倍率 1.4）

| dataset | 名称 | 分 | 字段 | cov | alphaCount | 近十年可用性 |
|---|---|---:|---:|---:|---:|---|
| institutions6 | Institutions and Beneficial Stake Ownership | 0.5415 | 11 | 0.9989 | 763 | ✅ 直接可用 |

### shortinterest（塔倍率 1.3）

| dataset | 名称 | 分 | 字段 | cov | alphaCount | 近十年可用性 |
|---|---|---:|---:|---:|---:|---|
| shortinterest5 | Daily Price Limit Data | 0.8001 | 3 | 1 | 23 | ✅ 直接可用 |
| shortinterest55 | Short-Selling Dataset | 0.5578 | 5 | 0.7898 | 367 | ⚠️ 需 ts_backfill / if_else 兜底 |
| other534 | Short-Selling Dataset | 0.553 | 5 | 0.8028 | 495 | ⚠️ 需 ts_backfill / if_else 兜底 |
| shortinterest44 | Short Sale Activity | 0.5478 | 2 | 0.815 | 129 | ⚠️ 需 ts_backfill / if_else 兜底 |
| shortinterest3 | Securities Lending Files Data | 0.543 | 56 | 0.865 | 1192 | ⚠️ 需 ts_backfill / if_else 兜底 |
| shortinterest52 | Hong Kong Securities Futures Data | 0.4833 | 2 | 0.6538 | 183 | ❌ 覆盖不足，需逐字段核 |
| other58 | Hong Kong Secutiries Futures Data | 0.4216 | 2 | 0.4746 | 57 | ❌ 覆盖不足，需逐字段核 |

### analyst（塔倍率 1.7）

| dataset | 名称 | 分 | 字段 | cov | alphaCount | 近十年可用性 |
|---|---|---:|---:|---:|---:|---|
| analyst11 | ESG scores | 0.6905 | 126 | 0.4756 | 31 | ❌ 覆盖不足，需逐字段核 |
| analyst_consensus | Standardized Analyst Consensus Forecasts | 0.6818 | 1729 | 0.7045 | 191 | ❌ 覆盖不足，需逐字段核 |
| analyst45 | Analyst Trade Ideas | 0.6419 | 241 | 0.3326 | 44 | ❌ 覆盖不足，需逐字段核 |
| analyst_base_ref | Analyst Estimates Base Reference | 0.6256 | 13 | 0.4979 | 25 | ❌ 覆盖不足，需逐字段核 |
| analyst21 | Indicators of Interest Data | 0.6224 | 16 | 0.4509 | 21 | ❌ 覆盖不足，需逐字段核 |
| analyst10 | Performance-Weighted Analyst Estimates | 0.5685 | 528 | 0.7423 | 514 | ❌ 覆盖不足，需逐字段核 |
| analyst44 | Integrated Broker Estimates | 0.5601 | 552 | 0.7181 | 1350 | ❌ 覆盖不足，需逐字段核 |
| analyst16 | Real Time Estimates | 0.5523 | 141 | 0.4972 | 79 | ❌ 覆盖不足，需逐字段核 |

### insiders（塔倍率 1.2）

| dataset | 名称 | 分 | 字段 | cov | alphaCount | 近十年可用性 |
|---|---|---:|---:|---:|---:|---|
| insiders5 | Corporate Insider Trading Activities Dataset | 0.5997 | 1 | 0.999 | 232 | ✅ 直接可用 |
| insiders1 | Global Insider Trading Data | 0.3282 | 9 | 0.4538 | 912 | ❌ 覆盖不足，需逐字段核 |

### macro（塔倍率 1.2）

| dataset | 名称 | 分 | 字段 | cov | alphaCount | 近十年可用性 |
|---|---|---:|---:|---:|---:|---|
| macro63 | Index Reconstitution Data | 0.6101 | 1 | 1 | 93 | ✅ 直接可用 |

### earnings（塔倍率 1.3）

| dataset | 名称 | 分 | 字段 | cov | alphaCount | 近十年可用性 |
|---|---|---:|---:|---:|---:|---|
| earnings6 | International Findings Data | 0.4287 | 40 | 0.328 | 232 | ❌ 覆盖不足，需逐字段核 |
| earnings3 | Earnings Date Data | 0.3629 | 8 | 0.5983 | 1734 | ❌ 覆盖不足，需逐字段核 |

### socialmedia（塔倍率 1.1）

| dataset | 名称 | 分 | 字段 | cov | alphaCount | 近十年可用性 |
|---|---|---:|---:|---:|---:|---|
| other100 | Investor views | 0.5901 | 1 | 1 | 173 | ✅ 直接可用 |
| socialmedia39 | Investor views | 0.5901 | 1 | 1 | 255 | ✅ 直接可用 |
| socialmedia12 | Sentiment Data for Equity | 0.3509 | 6 | 0.5615 | 726 | ❌ 覆盖不足，需逐字段核 |

### imbalance（塔倍率 1）

| dataset | 名称 | 分 | 字段 | cov | alphaCount | 近十年可用性 |
|---|---|---:|---:|---:|---:|---|
| imbalance5 | Oil Price Resilience Scores | 0.3979 | 2 | 0.7652 | 1360 | ⚠️ 需 ts_backfill / if_else 兜底 |

### fundamental（塔倍率 1.6）

| dataset | 名称 | 分 | 字段 | cov | alphaCount | 近十年可用性 |
|---|---|---:|---:|---:|---:|---|
| fundamental1 | Management and Executive Data | 0.6789 | 118 | 0.4515 | 12 | ❌ 覆盖不足，需逐字段核 |
| fundamental17 | Direct Fundamental Data | 0.6098 | 369 | 0.9216 | 3749 | ✅ 直接可用 |
| fundamental90 | Governance, Accounting, Management, and Equality | 0.5844 | 55 | 0.6696 | 192 | ❌ 覆盖不足，需逐字段核 |
| fundamental21 | ESG Scores Data | 0.5809 | 156 | 0.5864 | 257 | ❌ 覆盖不足，需逐字段核 |
| fundamental86 | Stock Reports Plus | 0.5655 | 10 | 0.7901 | 204 | ⚠️ 需 ts_backfill / if_else 兜底 |
| fundamental89 | Accrual based Earnings Model | 0.56 | 15 | 0.3244 | 20 | ❌ 覆盖不足，需逐字段核 |
| other395 | Accrual based Earnings Model | 0.56 | 15 | 0.3244 | 11 | ❌ 覆盖不足，需逐字段核 |
| fundamental44 | Accounting Quality Models | 0.5469 | 12 | 0.7315 | 312 | ❌ 覆盖不足，需逐字段核 |

### news（塔倍率 1.6）

| dataset | 名称 | 分 | 字段 | cov | alphaCount | 近十年可用性 |
|---|---|---:|---:|---:|---:|---|
| news76 | Textual News Feed Data | 0.7669 | 6 | 0.9013 | 12 | ✅ 直接可用 |
| other7 | Archive News Data | 0.7225 | 11 | 0.7513 | 22 | ⚠️ 需 ts_backfill / if_else 兜底 |
| news29 | Significant Developments Data | 0.6982 | 12 | 0.6849 | 23 | ❌ 覆盖不足，需逐字段核 |
| news59 | Corporate Events Data | 0.6968 | 2 | 0.8125 | 29 | ⚠️ 需 ts_backfill / if_else 兜底 |
| news31 | News Analytics on Equities | 0.6843 | 25 | 1 | 58 | ✅ 直接可用 |
| news48 | Global Media News Data | 0.6521 | 22 | 0.5534 | 44 | ❌ 覆盖不足，需逐字段核 |
| news38 | News Analytic Model Data | 0.6429 | 45 | 0.8302 | 62 | ⚠️ 需 ts_backfill / if_else 兜底 |
| news50 | Web News Analytics Data | 0.6357 | 81 | 0.7953 | 83 | ⚠️ 需 ts_backfill / if_else 兜底 |

### pv（塔倍率 1.5）

| dataset | 名称 | 分 | 字段 | cov | alphaCount | 近十年可用性 |
|---|---|---:|---:|---:|---:|---|
| pv149 | Holidays and Trading Hours Calendar | 0.8118 | 2 | 1 | 0 | ✅ 直接可用 |
| continuation_score | Price Chart Continuation Pattern Similarity | 0.7832 | 560 | 1 | 227 | ✅ 直接可用 |
| univ1 | Universe Dataset | 0.7818 | 2 | 1 | 4 | ✅ 直接可用 |
| pattern_scores | Chart Pattern Similarity Scores | 0.7802 | 504 | 1 | 151 | ✅ 直接可用 |
| pv106 | Microstructure Spread Data | 0.6677 | 29 | 0.973 | 425 | ✅ 直接可用 |
| intraday_pv_feats | Daily Intraday Price Volume Features | 0.6567 | 579 | 0.9812 | 1216 | ✅ 直接可用 |
| pv30 | Alternate Industry Classification | 0.6424 | 690 | 0.9329 | 2649 | ✅ 直接可用 |
| pv103 | Interval and MOO&MOC statistics | 0.6402 | 7 | 1 | 154 | ✅ 直接可用 |

### model（塔倍率 1.7）

| dataset | 名称 | 分 | 字段 | cov | alphaCount | 近十年可用性 |
|---|---|---:|---:|---:|---:|---|
| model37 | Text Mining Data | 0.8631 | 79 | 0.9407 | 43 | ✅ 直接可用 |
| price_signal_dl | Deep Learning Price Signal Dataset | 0.7836 | 28 | 0.8154 | 22 | ⚠️ 需 ts_backfill / if_else 兜底 |
| behavioral_signals | Behavioral Finance Signal Factors | 0.7374 | 7 | 0.768 | 6 | ⚠️ 需 ts_backfill / if_else 兜底 |
| predictive_starmine | Predictive Analyst-Company Signal Set | 0.7368 | 645 | 0.8486 | 118 | ⚠️ 需 ts_backfill / if_else 兜底 |
| ai_equity_alpha | AI Equity Alpha Forecasts | 0.7365 | 582 | 0.8803 | 205 | ⚠️ 需 ts_backfill / if_else 兜底 |
| quant_factor_lib | Multi-Domain Quantitative Factor Library | 0.7272 | 32 | 0.6649 | 37 | ❌ 覆盖不足，需逐字段核 |
| model16 | Fundamental Scores | 0.7254 | 24 | 0.7056 | 32 | ❌ 覆盖不足，需逐字段核 |
| model68 | Risk-Alleviated Momentum Scores | 0.7103 | 4 | 0.7592 | 22 | ⚠️ 需 ts_backfill / if_else 兜底 |

### other（塔倍率 1.7）

| dataset | 名称 | 分 | 字段 | cov | alphaCount | 近十年可用性 |
|---|---|---:|---:|---:|---:|---|
| ai_news_scores | AI News Sentiment Scores | 0.7923 | 97 | 0.749 | 42 | ❌ 覆盖不足，需逐字段核 |
| other532 | Specific Returns | 0.7818 | 2 | 1 | 47 | ✅ 直接可用 |
| other165 | Hong Kong Exchange Announcement | 0.7701 | 1 | 1 | 32 | ✅ 直接可用 |
| other479 | China Classification data | 0.7601 | 1 | 1 | 38 | ✅ 直接可用 |
| other545 | Linked Firms Momentum Data | 0.7018 | 4 | 0.7381 | 24 | ❌ 覆盖不足，需逐字段核 |
| other635 | Thomson Reuters News Analytics Equities | 0.6949 | 6 | 0.6965 | 13 | ❌ 覆盖不足，需逐字段核 |
| other455 | Relationship enhanced with AI/ML | 0.6939 | 1500 | 0.7097 | 297 | ❌ 覆盖不足，需逐字段核 |
| other323 | Global Equity Premarket Data | 0.6619 | 11 | 1 | 230 | ✅ 直接可用 |