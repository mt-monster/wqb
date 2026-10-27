# sentiment21 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `sentiment21` |
| 名称 | AI Sentiment Score Data |
| 类别 | SENTIMENT |
| 数据字段数(平台) | 210 |
| 覆盖率 | 0.9659 |
| 平台已有 alpha | 687 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.4 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides comprehensive analytics on news items related to equities, including over 80 fields across five key categories: relevance, sentiment, novelty, volume, and headline classification. Each news item is processed to generate asset-specific scores, such as sentiment (positive, neutral, negative), relevance to the asset, and measures of news novelty and volume over various time windows. The dataset also includes metadata like headline tags, company identifiers, and timestamps. By quantifying the tone, frequency, and uniqueness of news coverage for each company, this dataset enables researchers and quantitative investors to systematically incorporate real-time and historical news sentiment into trading strategies. It is particularly useful for predicting short-term price move

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **210** |
| 类型分布 | MATRIX×210 |
| 平均覆盖率 | **0.966** |
| 覆盖率区间 | 0.93 ~ 1.00 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 210 | 100.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 204 | 97.1% |
| DEAD | 6 | 2.9% |

- 已实测字段：**6** 个（3%），best_sharpe 最高 **0.49**，中位 0.07

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 情绪与新闻 | 210 | 0.97 | snt21_2neg_conf_up、snt21_2neut_conf_up、snt21_2neut_std |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `snt21_2neg_conf_up` | MATRIX | 0.932 | 情绪与新闻 | 1 | 0.49 | 0.61 | 0.48 | DEAD | Upper confidence bound for negative sentiment scores. |
| 2 | `snt21_2neut_conf_up` | MATRIX | 0.932 | 情绪与新闻 | 1 | 0.43 | 0.09 | 0.34 | DEAD | Upper confidence bound for neutral sentiment scores. |
| 3 | `snt21_2neut_std` | MATRIX | 0.932 | 情绪与新闻 | 1 | 0.07 | -0.10 | 0.11 | DEAD | Standard deviation of neutral sentiment scores. |
| 4 | `snt21_2neg_std` | MATRIX | 0.932 | 情绪与新闻 | 1 | -0.12 | 0.03 | -0.16 | DEAD | Standard deviation of negative sentiment scores. |
| 5 | `snt21_2neg_mean_103` | MATRIX | 1.000 | 情绪与新闻 | 1 | -0.37 | 0.06 | -0.12 | DEAD | Mean value of negative sentiment scores. |
| 6 | `snt21_2pos_max_87` | MATRIX | 1.000 | 情绪与新闻 | 2 | -0.41 | 0.77 | 0.07 | DEAD | Maximum value of positive sentiment scores. |
| 7 | `snt21_2dts_gen_94` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of negative sentiment scores. |
| 8 | `snt21_2dts_sop_97` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of positive sentiment scores. |
| 9 | `snt21_2dts_tuen_100` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of neutral sentiment scores. |
| 10 | `snt21_2neg_conf_low_92` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for negative sentiment scores. |
| 11 | `snt21_2neg_conf_up_98` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for negative sentiment scores. |
| 12 | `snt21_2neg_max_93` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of negative sentiment scores. |
| 13 | `snt21_2neg_median_105` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of negative sentiment scores. |
| 14 | `snt21_2neg_min_104` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of negative sentiment scores. |
| 15 | `snt21_2neut_conf_low_90` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for neutral sentiment scores. |
| 16 | `snt21_2neut_conf_up_95` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for neutral sentiment scores. |
| 17 | `snt21_2neut_max_89` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of neutral sentiment scores. |
| 18 | `snt21_2neut_mean_102` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of neutral sentiment scores. |
| 19 | `snt21_2neut_median_101` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of neutral sentiment scores. |
| 20 | `snt21_2neut_min_91` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of neutral sentiment scores. |
| 21 | `snt21_2pos_conf_low_85` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for positive sentiment scores. |
| 22 | `snt21_2pos_conf_up_88` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for positive sentiment scores. |
| 23 | `snt21_2pos_mean_96` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of positive sentiment scores. |
| 24 | `snt21_2pos_median_99` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of positive sentiment scores. |
| 25 | `snt21_2pos_min_86` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of positive sentiment scores. |
| 26 | `snt21_3dts_gen_55` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of negative sentiment scores. |
| 27 | `snt21_3dts_sop_57` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of positive sentiment scores. |
| 28 | `snt21_3dts_tuen_51` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of neutral sentiment scores. |
| 29 | `snt21_3neg_conf_low_48` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for negative sentiment scores. |
| 30 | `snt21_3neg_conf_up_49` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for negative sentiment scores. |
| 31 | `snt21_3neg_max_59` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of negative sentiment scores. |
| 32 | `snt21_3neg_mean_53` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of negative sentiment scores. |
| 33 | `snt21_3neg_median_62` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of negative sentiment scores. |
| 34 | `snt21_3neg_min_50` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of negative sentiment scores. |
| 35 | `snt21_3neut_conf_low_58` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for neutral sentiment scores. |
| 36 | `snt21_3neut_conf_up_44` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for neutral sentiment scores. |
| 37 | `snt21_3neut_max_46` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of neutral sentiment scores. |
| 38 | `snt21_3neut_mean_43` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of neutral sentiment scores. |
| 39 | `snt21_3neut_median_47` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of neutral sentiment scores. |
| 40 | `snt21_3neut_min_61` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of neutral sentiment scores. |
| 41 | `snt21_3pos_conf_low_56` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for positive sentiment scores. |
| 42 | `snt21_3pos_conf_up_54` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for positive sentiment scores. |
| 43 | `snt21_3pos_max_52` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of positive sentiment scores. |
| 44 | `snt21_3pos_mean_63` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of positive sentiment scores. |
| 45 | `snt21_3pos_median_60` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of positive sentiment scores. |
| 46 | `snt21_3pos_min_45` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of positive sentiment scores. |
| 47 | `snt21_4dts_gen_35` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of negative sentiment scores. |
| 48 | `snt21_4dts_sop_29` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of positive sentiment scores. |
| 49 | `snt21_4dts_tuen_26` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of neutral sentiment scores. |
| 50 | `snt21_4neg_conf_low_32` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for negative sentiment scores. |
| 51 | `snt21_4neg_conf_up_33` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for negative sentiment scores. |
| 52 | `snt21_4neg_max_31` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of negative sentiment scores. |
| 53 | `snt21_4neg_mean_24` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of negative sentiment scores. |
| 54 | `snt21_4neg_median_28` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of negative sentiment scores. |
| 55 | `snt21_4neg_min_41` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of negative sentiment scores. |
| 56 | `snt21_4neut_conf_low_22` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for neutral sentiment scores. |
| 57 | `snt21_4neut_conf_up_30` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for neutral sentiment scores. |
| 58 | `snt21_4neut_max_27` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of neutral sentiment scores. |
| 59 | `snt21_4neut_mean_34` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of neutral sentiment scores. |
| 60 | `snt21_4neut_median_38` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of neutral sentiment scores. |
| 61 | `snt21_4neut_min_39` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of neutral sentiment scores. |
| 62 | `snt21_4pos_conf_low_23` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for positive sentiment scores. |
| 63 | `snt21_4pos_conf_up_25` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for positive sentiment scores. |
| 64 | `snt21_4pos_max_36` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of positive sentiment scores. |
| 65 | `snt21_4pos_mean_42` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of positive sentiment scores. |
| 66 | `snt21_4pos_median_40` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of positive sentiment scores. |
| 67 | `snt21_4pos_min_37` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of positive sentiment scores. |
| 68 | `snt21_5dts_gen_4` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of negative sentiment scores. |
| 69 | `snt21_5dts_sop_8` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of positive sentiment scores. |
| 70 | `snt21_5dts_tuen_11` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of neutral sentiment scores. |
| 71 | `snt21_5neg_conf_low_7` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for negative sentiment scores. |
| 72 | `snt21_5neg_conf_up_20` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for negative sentiment scores. |
| 73 | `snt21_5neg_max_13` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of negative sentiment scores. |
| 74 | `snt21_5neg_mean_14` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of negative sentiment scores. |
| 75 | `snt21_5neg_median_12` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of negative sentiment scores. |
| 76 | `snt21_5neg_min_5` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of negative sentiment scores. |
| 77 | `snt21_5neut_conf_low_19` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for neutral sentiment scores. |
| 78 | `snt21_5neut_conf_up_6` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for neutral sentiment scores. |
| 79 | `snt21_5neut_max_21` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of neutral sentiment scores. |
| 80 | `snt21_5neut_mean_3` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of neutral sentiment scores. |
| 81 | `snt21_5neut_median_18` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of neutral sentiment scores. |
| 82 | `snt21_5neut_min_10` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of neutral sentiment scores. |
| 83 | `snt21_5pos_conf_low_16` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for positive sentiment scores. |
| 84 | `snt21_5pos_conf_up_9` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for positive sentiment scores. |
| 85 | `snt21_5pos_max_17` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of positive sentiment scores. |
| 86 | `snt21_5pos_mean_2` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of positive sentiment scores. |
| 87 | `snt21_5pos_median_15` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of positive sentiment scores. |
| 88 | `snt21_5pos_min_1` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of positive sentiment scores. |
| 89 | `snt21dts_gen_76` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of negative sentiment scores. |
| 90 | `snt21dts_sop_68` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of positive sentiment scores. |
| 91 | `snt21dts_tuen_67` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of neutral sentiment scores. |
| 92 | `snt21neg_conf_low_65` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for negative sentiment scores. |
| 93 | `snt21neg_conf_up_74` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for negative sentiment scores. |
| 94 | `snt21neg_max_77` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of negative sentiment scores. |
| 95 | `snt21neg_mean_81` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of negative sentiment scores. |
| 96 | `snt21neg_median_82` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of negative sentiment scores. |
| 97 | `snt21neg_min_66` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of negative sentiment scores. |
| 98 | `snt21neut_conf_low_69` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for neutral sentiment scores. |
| 99 | `snt21neut_conf_up_75` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for neutral sentiment scores. |
| 100 | `snt21neut_max_79` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of neutral sentiment scores. |
| 101 | `snt21neut_mean_71` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of neutral sentiment scores. |
| 102 | `snt21neut_median_83` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of neutral sentiment scores. |
| 103 | `snt21neut_min_72` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of neutral sentiment scores. |
| 104 | `snt21pos_conf_low_64` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for positive sentiment scores. |
| 105 | `snt21pos_conf_up_73` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for positive sentiment scores. |
| 106 | `snt21pos_max_84` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of positive sentiment scores. |
| 107 | `snt21pos_mean_78` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of positive sentiment scores. |
| 108 | `snt21pos_median_70` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of positive sentiment scores. |
| 109 | `snt21pos_min_80` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of positive sentiment scores. |
| 110 | `snt21_2neg_conf_low` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for negative sentiment scores. |
| 111 | `snt21_2neg_max` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of negative sentiment scores. |
| 112 | `snt21_2neg_mean` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of negative sentiment scores. |
| 113 | `snt21_2neg_median` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of negative sentiment scores. |
| 114 | `snt21_2neg_min` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of negative sentiment scores. |
| 115 | `snt21_2neut_conf_low` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for neutral sentiment scores. |
| 116 | `snt21_2neut_max` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of neutral sentiment scores. |
| 117 | `snt21_2neut_mean` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of neutral sentiment scores. |
| 118 | `snt21_2neut_median` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of neutral sentiment scores. |
| 119 | `snt21_2neut_min` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of neutral sentiment scores. |
| 120 | `snt21_2pos_conf_low` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for positive sentiment scores. |
| 121 | `snt21_2pos_conf_up` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for positive sentiment scores. |
| 122 | `snt21_2pos_max` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of positive sentiment scores. |
| 123 | `snt21_2pos_mean` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of positive sentiment scores. |
| 124 | `snt21_2pos_median` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of positive sentiment scores. |
| 125 | `snt21_2pos_min` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of positive sentiment scores. |
| 126 | `snt21_2pos_std` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of positive sentiment scores. |
| 127 | `snt21_3neg_conf_low` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for negative sentiment scores. |
| 128 | `snt21_3neg_conf_up` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for negative sentiment scores. |
| 129 | `snt21_3neg_max` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of negative sentiment scores. |
| 130 | `snt21_3neg_mean` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of negative sentiment scores. |
| 131 | `snt21_3neg_median` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of negative sentiment scores. |
| 132 | `snt21_3neg_min` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of negative sentiment scores. |
| 133 | `snt21_3neg_std` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of negative sentiment scores. |
| 134 | `snt21_3neut_conf_low` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for neutral sentiment scores. |
| 135 | `snt21_3neut_conf_up` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for neutral sentiment scores. |
| 136 | `snt21_3neut_max` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of neutral sentiment scores. |
| 137 | `snt21_3neut_mean` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of neutral sentiment scores. |
| 138 | `snt21_3neut_median` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of neutral sentiment scores. |
| 139 | `snt21_3neut_min` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of neutral sentiment scores. |
| 140 | `snt21_3neut_std` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of neutral sentiment scores. |
| 141 | `snt21_3pos_conf_low` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for positive sentiment scores. |
| 142 | `snt21_3pos_conf_up` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for positive sentiment scores. |
| 143 | `snt21_3pos_max` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of positive sentiment scores. |
| 144 | `snt21_3pos_mean` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of positive sentiment scores. |
| 145 | `snt21_3pos_median` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of positive sentiment scores. |
| 146 | `snt21_3pos_min` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of positive sentiment scores. |
| 147 | `snt21_3pos_std` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of positive sentiment scores. |
| 148 | `snt21_4neg_conf_low` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for negative sentiment scores. |
| 149 | `snt21_4neg_conf_up` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for negative sentiment scores. |
| 150 | `snt21_4neg_max` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of negative sentiment scores. |
| 151 | `snt21_4neg_mean` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of negative sentiment scores. |
| 152 | `snt21_4neg_median` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of negative sentiment scores. |
| 153 | `snt21_4neg_min` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of negative sentiment scores. |
| 154 | `snt21_4neg_std` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of negative sentiment scores. |
| 155 | `snt21_4neut_conf_low` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for neutral sentiment scores. |
| 156 | `snt21_4neut_conf_up` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for neutral sentiment scores. |
| 157 | `snt21_4neut_max` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of neutral sentiment scores. |
| 158 | `snt21_4neut_mean` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of neutral sentiment scores. |
| 159 | `snt21_4neut_median` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of neutral sentiment scores. |
| 160 | `snt21_4neut_min` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of neutral sentiment scores. |
| 161 | `snt21_4neut_std` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of neutral sentiment scores. |
| 162 | `snt21_4pos_conf_low` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for positive sentiment scores. |
| 163 | `snt21_4pos_conf_up` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for positive sentiment scores. |
| 164 | `snt21_4pos_max` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of positive sentiment scores. |
| 165 | `snt21_4pos_mean` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of positive sentiment scores. |
| 166 | `snt21_4pos_median` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of positive sentiment scores. |
| 167 | `snt21_4pos_min` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of positive sentiment scores. |
| 168 | `snt21_4pos_std` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of positive sentiment scores. |
| 169 | `snt21_5neg_conf_low` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for negative sentiment scores. |
| 170 | `snt21_5neg_conf_up` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for negative sentiment scores. |
| 171 | `snt21_5neg_max` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of negative sentiment scores. |
| 172 | `snt21_5neg_mean` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of negative sentiment scores. |
| 173 | `snt21_5neg_median` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of negative sentiment scores. |
| 174 | `snt21_5neg_min` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of negative sentiment scores. |
| 175 | `snt21_5neg_std` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of negative sentiment scores. |
| 176 | `snt21_5neut_conf_low` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for neutral sentiment scores. |
| 177 | `snt21_5neut_conf_up` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for neutral sentiment scores. |
| 178 | `snt21_5neut_max` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of neutral sentiment scores. |
| 179 | `snt21_5neut_mean` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of neutral sentiment scores. |
| 180 | `snt21_5neut_median` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of neutral sentiment scores. |
| 181 | `snt21_5neut_min` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of neutral sentiment scores. |
| 182 | `snt21_5neut_std` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of neutral sentiment scores. |
| 183 | `snt21_5pos_conf_low` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for positive sentiment scores. |
| 184 | `snt21_5pos_conf_up` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for positive sentiment scores. |
| 185 | `snt21_5pos_max` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of positive sentiment scores. |
| 186 | `snt21_5pos_mean` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of positive sentiment scores. |
| 187 | `snt21_5pos_median` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of positive sentiment scores. |
| 188 | `snt21_5pos_min` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of positive sentiment scores. |
| 189 | `snt21_5pos_std` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of positive sentiment scores. |
| 190 | `snt21_neg_conf_low` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for negative sentiment scores. |
| 191 | `snt21_neg_conf_up` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for negative sentiment scores. |
| 192 | `snt21_neg_max` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of negative sentiment scores. |
| 193 | `snt21_neg_mean` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of negative sentiment scores. |
| 194 | `snt21_neg_median` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of negative sentiment scores. |
| 195 | `snt21_neg_min` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of negative sentiment scores. |
| 196 | `snt21_neg_std` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of negative sentiment scores. |
| 197 | `snt21_neut_conf_low` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for neutral sentiment scores. |
| 198 | `snt21_neut_conf_up` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for neutral sentiment scores. |
| 199 | `snt21_neut_max` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of neutral sentiment scores. |
| 200 | `snt21_neut_mean` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of neutral sentiment scores. |
| 201 | `snt21_neut_median` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of neutral sentiment scores. |
| 202 | `snt21_neut_min` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of neutral sentiment scores. |
| 203 | `snt21_neut_std` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of neutral sentiment scores. |
| 204 | `snt21_pos_conf_low` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower confidence bound for positive sentiment scores. |
| 205 | `snt21_pos_conf_up` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper confidence bound for positive sentiment scores. |
| 206 | `snt21_pos_max` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of positive sentiment scores. |
| 207 | `snt21_pos_mean` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of positive sentiment scores. |
| 208 | `snt21_pos_median` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of positive sentiment scores. |
| 209 | `snt21_pos_min` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of positive sentiment scores. |
| 210 | `snt21_pos_std` | MATRIX | 0.932 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of positive sentiment scores. |

## 六、本地回测证据

- 本地累计回测 **7** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `LLN7GQaL` | 0.49 | 0.20 | 0.61 | 0.48 | 0.14 | ["LOW_SHARPE | 237 | `divide(ts_delta(ts_backfill(subtract(snt21_2neg_conf_up,snt21_2neg_conf_low),22),5), add(t` |
| `levjWmO8` | 0.43 | 0.16 | 0.09 | 0.34 | 0.14 | ["LOW_SHARPE | 237 | `divide(ts_delta(ts_backfill(subtract(snt21_2neut_conf_up,snt21_2neg_conf_low),22),5), add(` |
| `kqojP9AL` | 0.07 | 0.01 | -0.10 | 0.11 | 0.14 | ["LOW_SHARPE | 237 | `divide(ts_backfill(snt21_2neut_std,22), add(add(snt21_2pos_std,snt21_2neg_std),0.0001))` |
| `9qjXpk5V` | -0.12 | -0.04 | 0.03 | -0.16 | 0.19 | ["LOW_SHARPE | 237 | `group_count(snt21_2neg_std, sector)` |
| `9qjXpkn2` | -0.37 | -0.18 | 0.06 | -0.12 | 0.06 | ["LOW_SHARPE | 237 | `divide(ts_corr(ts_backfill(snt21_2neg_mean_103,22), ts_backfill(snt21_2neg_conf_up,22), 66` |
| `6XjlpNk7` | -0.41 | -0.22 | 0.77 | 0.07 | 0.14 | ["LOW_SHARPE | 237 | `divide(subtract(add(snt21_2pos_max_87, snt21_3pos_min), add(snt21_3pos_median, snt21_3pos_` |
| `N1a7b8dq` | -0.51 | -0.29 | 0.45 | -0.11 | 0.14 | ["LOW_SHARPE | 237 | `divide(subtract(add(snt21_2pos_max_87, snt21_2pos_min), add(snt21_3pos_median, snt21_3pos_` |

## 七、判死记录（sealed dead_end）

- `EUR-SNT26-ATTENTION-FITNESS-CEILING`（None）family=sentiment26 网站流行度/投资者注意力族：{"dataset": "sentiment26", "evidence": {"LL9d1JO9": "注意力水平 relpopularity08：S0.90/F0.45/2Y1.75 PASS/TVR0.0929/returns0.0319/longCount1061，仅 2 项 FAIL", "N1QRr0YE": "注意力广度动量 totaldomains：S0.09 无信号", "ZY0Kn563": "top10% 集中度：S-0.84（镜像后 +0.84 仍不达线）"}, "math_proof": "turnover 0.0929 已低于公式下限 0.125，分母钉死 → Fitness_upper = Sharpe_max * sqrt(returns_max/0.125) = 0.90*0.505 = 0.455，实测 0.45 已贴天花板。即使 Sharpe 达 1.
- `EUR-SENTIMENT21-WEAK`（2026-09-23T18:35:12）family=sentiment21 情绪评分族（snt21_* 210 字段）：{"family": "sentiment21 情绪评分族（snt21_* 210 字段）", "reason": "wave237 11 探针全灭 best /sharpe/=0.49 < 0.5 → 达 fast_kill 判死线。cov 0.97 高覆盖但 IS 无强度；SENTIMENT 塔差 3 但此路无供给。", "source": "registry_dead_end", "salvage": {"alpha_ids": [], "count": 0, "source_waves": [], "sealed_at": "2026-09-23T18:35:12", "note": "seal_dead_end 沉降：供 Mode B 组合腿救援消费（get_salvage_pool）；动用仍守 mode_b_qualification 资格线"}}

