# HKG 未点亮塔数据集优先级地图（2026-11-06）

> 数据源：`tracking/mining/field_coverage_HKG_d1_TOP800.json`（2026-08-05 抓取，209 个数据集）。
> 评分式：`coverage × fieldCount^0.35 / log1p(alphaCount)` —— 兼顾覆盖、字段广度、拥挤度。
> 目的：为「穷尽所有 category 下的数据集（已点亮塔不选）」提供开波排队顺序。

## 塔位前提

HKG/D1 实测 **14 个 category 全部为 0 或未到 3**（连 pv 都只有 1）⇒ **HKG 一个塔都未点亮**，
全部 209 个数据集都在可选范围内。以下按 category 分布：

`model 63 / other 30 / news 24 / fundamental 21 / analyst 20 / sentiment 8 / shortinterest 7 /
risk 7 / socialmedia 3 / earnings 2 / institutions 2 / insiders 2 / imbalance 1 / macro 1`

## 优先级 Top 20

| # | 评分 | category | dataset | cov | 字段数 | aC | uC | 备注 |
|---|---:|---|---|---:|---:|---:|---:|---|
| 1 | 4.03 | other | `mmp_nlp_sentiment` | 0.948 | 521 | **2** | 1 | 极低拥挤 + 高覆盖，首选 |
| 2 | 3.16 | model | `analyst_revision_horizons` | 0.711 | **851** | **3** | 3 | 多周期分析师修正，字段极广 |
| 3 | 2.63 | analyst | `analyst_consensus` | 0.705 | **1729** | 13 | 8 | 字段最多，标准化一致预期 |
| 4 | 2.54 | model | `chart_cnn_alpha` | 0.630 | 1010 | 5 | 2 | 深度学习图表 alpha |
| 5 | 2.47 | model | `predictive_starmine` | 0.849 | 645 | 9 | 4 | **本轮 wave1 已开波** |
| 6 | 2.42 | other | `news_sentiment_nlp` | 0.865 | 19 | **0** | 0 | **完全处女地**（aC=0、uC=0） |
| 7 | 2.37 | model | `multifactor_return_pred` | 0.725 | 648 | 6 | 3 | 多因子市场收益预测 |
| 8 | 2.32 | model | `global_seasonal_model` | 0.698 | 681 | 6 | 4 | 全球季节性 regime |
| 9 | 2.24 | model | `quant_factor_lib` | 0.665 | 32 | **0** | 0 | **完全处女地** |
| 10 | 2.20 | model | `ai_equity_alpha` | 0.880 | 582 | 14 | 9 | 全 VECTOR，须 `vec_avg` |
| 11 | 1.64 | other | `ml_factor_proj` | 1.000 | 332 | 38 | 13 | cov 满分 |
| 12 | 1.56 | other | `ai_news_scores` | 0.749 | 97 | 3 | 3 | |
| 13 | 1.55 | model | `price_signal_dl` | 0.815 | 28 | 1 | 1 | |
| 14 | 1.52 | model | `behavioral_signals` | 0.768 | 7 | **0** | 0 | 行为金融因子 |
| 15 | 1.43 | other | `other455` | 0.710 | **1500** | 229 | 82 | 字段最广但已较拥挤 |
| 16 | 1.42 | model | `model219` | 0.785 | 1012 | 187 | 42 | |
| 17 | 1.37 | other | `news_sentiment_dl` | 0.863 | 17 | 1 | 1 | 近处女地 |
| 18 | 1.17 | model | `model37` | 0.941 | 79 | 14 | 11 | cov 最高档 |
| 19 | 1.17 | model | `multi_source_model` | 0.727 | 60 | 4 | 2 | |
| 20 | 1.09 | other | `insider_feats` | 0.704 | 29 | 2 | 2 | 内部人交易特征 |

## ⚠️ 已判死面（不得重复开波）

| 面 | TO 实测 | \|S\| 实测 | 判据 |
|---|---|---|---|
| `news_sentiment_transfer`（sentiment） | 42–50% | ≤0.25 | 高频刷新噪声 |
| `other553`（sentiment 归类，实为卖方目标价修正） | 45–47% | ≤0.51 | 高频刷新噪声 |
| `fund_holdings_panel`（institutions） | 1.65–2.24% | ≤0.42 | 慢变结构描述符 |

⇒ **推论**：Top 20 里 `mmp_nlp_sentiment` / `news_sentiment_nlp` / `news_sentiment_dl` / `ai_news_scores`
四个「新闻情绪系」大概率同属高频刷新噪声档 —— 虽然拥挤度极低（aC 0–3），
但按 HKG 已两次实证的字段级刷新率属性，**建议排在 model 系之后**，且首轮只派 2 条探针验证 TO，
不要因为 aC=0 就一次投入 10 个模板。

## 建议开波顺序

1. **`analyst_revision_horizons`**（model 塔，851 字段，aC 3）—— 分析师修正多周期信号，
   与 GBR 已出货的 `analyst7`/`predictive_starmine` 同族但周期维度更丰富，迁移风险最低。
2. **`analyst_consensus`**（analyst 塔，1729 字段，aC 13）—— 字段最多，可支撑 10+ 互异模板。
3. **`ai_equity_alpha`**（model 塔，582 字段）—— 已有字段画像（全 VECTOR，须 `vec_avg`）。
4. **`quant_factor_lib`** / **`behavioral_signals`**（aC=0、uC=0 完全处女地）—— 字段少，适合快验。
5. 新闻情绪四兄弟 —— 只派 2 条 TO 探针，验证是否落入 >40% 噪声档。
