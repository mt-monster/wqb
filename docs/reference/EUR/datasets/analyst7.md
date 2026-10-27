# analyst7 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `analyst7` |
| 名称 | Broker Estimates |
| 类别 | ANALYST |
| 数据字段数(平台) | 1111 |
| 覆盖率 | 0.5 |
| 平台已有 alpha | 3101 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides concise, real-time summaries of major company news events that are likely to move markets. Each event is tagged by topic (such as M&A, earnings guidance, product launches, regulatory actions, and more) and assigned a significance level, allowing users to filter for the most impactful developments. The data includes detailed headlines, descriptions, event categorization, and metadata such as company identifiers, event timing, and industry classification. By focusing on material news and filtering out less relevant information, this dataset enables quantitative analysts and traders to integrate event-driven signals into their models, backtest the impact of specific news types, and react quickly to market-moving corporate actions, thereby improving the prediction of shor

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **1111** |
| 类型分布 | MATRIX×1111 |
| 平均覆盖率 | **0.500** |
| 覆盖率区间 | 0.50 ~ 0.50 |
| 更新频率（推断） | 低频（季/年） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 1111 | 100.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 1111 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 1111 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 修正与预期 | 993 | 0.50 | act_q_bps_surprisemean、act_q_bps_surprisenum、act_q_bps_surprisestd |
| 盈利与财务 | 98 | 0.50 | act_12m_cps_value、act_12m_ebi_value、act_12m_ebt_value |
| 价量与波动 | 12 | 0.50 | chgprice、high_52wks、low_52wks |
| 其他 | 7 | 0.50 | act_12m_cpx_value、act_q_bps_value、eps_12m |
| 风险与质量 | 1 | 0.50 | marketbeta |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `act_12m_cps_value` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | actual cash flow per share regarding the last 4 quarters |
| 2 | `act_12m_cpx_value` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | actual capital expenditure regarding the last 4 quarters |
| 3 | `act_12m_ebi_value` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | actual EBIT regarding the last 4 quarters |
| 4 | `act_12m_ebt_value` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | actual EBITDA regarding the last 4 quarters |
| 5 | `act_12m_eps_value` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | actual earnings per share regarding the last 4 quarters |
| 6 | `act_12m_gps_value` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | actual GAAP earnings per share regarding the last 4 quarters |
| 7 | `act_12m_grm_value` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | actual gross margin in percent regarding the last 4 quarters |
| 8 | `act_12m_ner_value` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | actual net profit as reported regarding the last 4 quarters |
| 9 | `act_12m_net_value` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | actual net income regarding the last 4 quarters |
| 10 | `act_12m_opr_value` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | actual operating profit regarding the last 4 quarters |
| 11 | `act_12m_pre_value` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | actual pre-tax profit regarding the last 4 quarters |
| 12 | `act_12m_prr_value` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | actual pretax profit as reported regarding the last 4 quarters |
| 13 | `act_12m_sal_value` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | actual sales/revenue regarding the last 4 quarters |
| 14 | `act_q_bps_surprisemean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean surprise (actual - estimate) of actual book value per share regarding the last quarter |
| 15 | `act_q_bps_surprisenum` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for surprise calculation of actual book value per share regarding the last quarter |
| 16 | `act_q_bps_surprisestd` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of surprise (actual - estimate) of actual book value per share regarding the last quarter |
| 17 | `act_q_bps_value` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | actual book value per share regarding the last quarter |
| 18 | `act_q_cps_surprisenum` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for surprise calculation of actual cash flow per share regarding the last quarter |
| 19 | `act_q_cpx_surprisenum` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for surprise calculation of actual capital expenditure regarding the last quarter |
| 20 | `act_q_csh_surprisenum` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for surprise calculation of actual cash earnings per share regarding the last quarter |
| 21 | `act_q_dps_surprisemean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean surprise (actual - estimate) of actual dividend per share regarding the last quarter |
| 22 | `act_q_dps_surprisenum` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for surprise calculation of actual dividend per share regarding the last quarter |
| 23 | `act_q_ebi_surprisemean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean surprise (actual - estimate) of actual EBIT regarding the last quarter |
| 24 | `act_q_ebi_surprisenum` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for surprise calculation of actual EBIT regarding the last quarter |
| 25 | `act_q_ebi_surprisestd` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of surprise (actual - estimate) of actual EBIT regarding the last quarter |
| 26 | `act_q_ebi_value` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | actual EBIT regarding the last quarter |
| 27 | `act_q_ebs_surprisenum` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for surprise calculation of actual EBITDA per share regarding the last quarter |
| 28 | `act_q_ebt_surprisemean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean surprise (actual - estimate) of actual EBITDA regarding the last quarter |
| 29 | `act_q_ebt_surprisenum` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for surprise calculation of actual EBITDA regarding the last quarter |
| 30 | `act_q_ebt_surprisestd` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of surprise (actual - estimate) of actual EBITDA regarding the last quarter |
| 31 | `act_q_ebt_value` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | actual EBITDA regarding the last quarter |
| 32 | `act_q_ent_surprisemean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean surprise (actual - estimate) of actual enterprise value regarding the last quarter |
| 33 | `act_q_ent_surprisenum` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for surprise calculation of actual enterprise value regarding the last quarter |
| 34 | `act_q_eps_surprisemean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean surprise (actual - estimate) of actual earnings per share regarding the last quarter |
| 35 | `act_q_eps_surprisenum` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for surprise calculation of actual earnings per share regarding the last quarter |
| 36 | `act_q_eps_surprisestd` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of surprise (actual - estimate) of actual earnings per share regarding the last quarter |
| 37 | `act_q_eps_value` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | actual earnings per share regarding the last quarter |
| 38 | `act_q_fcf_surprisenum` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for surprise calculation of actual free cash flow per share regarding the last quarter |
| 39 | `act_q_gps_surprisemean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean surprise (actual - estimate) of actual GAAP earnings per share regarding the last quarter |
| 40 | `act_q_gps_surprisenum` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for surprise calculation of actual GAAP earnings per share regarding the last quarter |
| 41 | `act_q_gps_surprisestd` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of surprise (actual - estimate) of actual GAAP earnings per share regarding the last quarter |
| 42 | `act_q_gps_value` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | actual GAAP earnings per share regarding the last quarter |
| 43 | `act_q_grm_surprisemean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean surprise (actual - estimate) of actual gross margin in percent regarding the last quarter |
| 44 | `act_q_grm_surprisenum` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for surprise calculation of actual gross margin in percent regarding the last quarter |
| 45 | `act_q_nav_surprisemean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean surprise (actual - estimate) of actual net asset value regarding the last quarter |
| 46 | `act_q_nav_surprisenum` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for surprise calculation of actual net asset value regarding the last quarter |
| 47 | `act_q_nav_surprisestd` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of surprise (actual - estimate) of actual net asset value regarding the last quarter |
| 48 | `act_q_nav_value` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | actual net asset value regarding the last quarter |
| 49 | `act_q_ndt_surprisemean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean surprise (actual - estimate) of actual net debt regarding the last quarter |
| 50 | `act_q_ndt_surprisenum` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for surprise calculation of actual net debt regarding the last quarter |
| 51 | `act_q_ndt_surprisestd` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of surprise (actual - estimate) of actual net debt regarding the last quarter |
| 52 | `act_q_ndt_value` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | actual net debt regarding the last quarter |
| 53 | `act_q_ner_surprisemean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean surprise (actual - estimate) of actual net profit as reported regarding the last quarter |
| 54 | `act_q_ner_surprisenum` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for surprise calculation of actual net profit as reported regarding the last quarter |
| 55 | `act_q_ner_surprisestd` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of surprise (actual - estimate) of actual net profit as reported regarding the last quarter |
| 56 | `act_q_ner_value` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | actual net profit as reported regarding the last quarter |
| 57 | `act_q_net_surprisemean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean surprise (actual - estimate) of actual net income regarding the last quarter |
| 58 | `act_q_net_surprisenum` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for surprise calculation of actual net income regarding the last quarter |
| 59 | `act_q_net_surprisestd` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of surprise (actual - estimate) of actual net income regarding the last quarter |
| 60 | `act_q_net_value` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | actual net income regarding the last quarter |
| 61 | `act_q_opr_surprisemean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean surprise (actual - estimate) of actual operating profit regarding the last quarter |
| 62 | `act_q_opr_surprisenum` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for surprise calculation of actual operating profit regarding the last quarter |
| 63 | `act_q_opr_surprisestd` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of surprise (actual - estimate) of actual operating profit regarding the last quarter |
| 64 | `act_q_pre_surprisemean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean surprise (actual - estimate) of actual pre-tax profit regarding the last quarter |
| 65 | `act_q_pre_surprisenum` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for surprise calculation of actual pre-tax profit regarding the last quarter |
| 66 | `act_q_pre_surprisestd` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of surprise (actual - estimate) of actual pre-tax profit regarding the last quarter |
| 67 | `act_q_pre_value` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | actual pre-tax profit regarding the last quarter |
| 68 | `act_q_prr_surprisemean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean surprise (actual - estimate) of actual pretax profit as reported regarding the last quarter |
| 69 | `act_q_prr_surprisenum` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for surprise calculation of actual pre-tax profit as reported regarding the last quarter |
| 70 | `act_q_prr_surprisestd` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of surprise (actual - estimate) of actual pretax profit as reported regarding the last quarter |
| 71 | `act_q_prr_value` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | actual pretax profit as reported regarding the last quarter |
| 72 | `act_q_roa_surprisenum` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for surprise calculation of actual return on assets in percent regarding the last quarter |
| 73 | `act_q_roe_surprisenum` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for surprise calculation of actual return on equity in percent regarding the last quarter |
| 74 | `act_q_sal_surprisemean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean surprise (actual - estimate) of actual sales/revenue regarding the last quarter |
| 75 | `act_q_sal_surprisenum` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for surprise calculation of actual sales/revenue regarding the last quarter |
| 76 | `act_q_sal_surprisestd` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of surprise (actual - estimate) of actual sales/revenue regarding the last quarter |
| 77 | `act_q_sal_value` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | actual sales/revenue regarding the last quarter |
| 78 | `act_q_tbv_surprisenum` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for surprise calculation of actual tangible book value per share regarding the last quarter |
| 79 | `annualdiv` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Indicated annual dividend |
| 80 | `chgprice` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Difference in weekly price today and 4 weeks ago |
| 81 | `eps_12m` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Actual EPS in the last 4 quarters |
| 82 | `est_12m_bps_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of book value per share regarding the next 4 quarters |
| 83 | `est_12m_bps_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of book value per share regarding the next 4 quarters, made in the past 3 months |
| 84 | `est_12m_bps_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of book value per share regarding the next 4 quarters, made in past 4 weeks |
| 85 | `est_12m_bps_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of book value per share regarding the next 4 quarters |
| 86 | `est_12m_bps_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of book value per share regarding the next 4 quarters, made in past 3 months |
| 87 | `est_12m_bps_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of book value per share regarding the next 4 quarters, made in the past 4 weeks |
| 88 | `est_12m_bps_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 89 | `est_12m_bps_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 90 | `est_12m_bps_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of book value per share regarding the next 4 quarters, where old and new estimates were made in the past |
| 91 | `est_12m_bps_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of book value per share regarding the next 4 quarters |
| 92 | `est_12m_bps_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of book value per share regarding the next 4 quarters, made in the last 28 days |
| 93 | `est_12m_bps_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of book value per share regarding the next 4 quarters, made in past 3 months |
| 94 | `est_12m_bps_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of book value per share regarding the next 4 quarters, made in the past 4 weeks |
| 95 | `est_12m_bps_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of book value per share regarding the next 4 quarters |
| 96 | `est_12m_bps_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of book value per share regarding the next 4 quarters, made in the past 3 months |
| 97 | `est_12m_bps_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of book value per share regarding the next 4 quarters, made in past 4 weeks |
| 98 | `est_12m_bps_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of book value per share regarding the next 4 quarters |
| 99 | `est_12m_bps_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of book value per share regarding the next 4 quarters, made in the last 28 days |
| 100 | `est_12m_bps_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of book value per share regarding the next 4 quarters, made in the past 3 months |
| 101 | `est_12m_bps_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of book value per share regarding the next 4 quarters, where old and new estimates were made in the past 4 weeks |
| 102 | `est_12m_bps_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of book value per share regarding the next 4 quarters, compared to the last weekly update |
| 103 | `est_12m_bps_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of book value per share regarding the next 4 quarters, compared to the last monthly update |
| 104 | `est_12m_bps_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of book value per share regarding the next 4 quarters, where old and new estimates were made in past 4 we |
| 105 | `est_12m_bps_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of book value per share regarding the next 4 quarters |
| 106 | `est_12m_bps_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimates of book value per share regarding the next 4 quarters, made in the last 28 days |
| 107 | `est_12m_bps_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of book value per share regarding the next 4 quarters, made in past 3 months |
| 108 | `est_12m_bps_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimates of book value per share regarding the next 4 quarters, made in the past 4 weeks |
| 109 | `est_12m_cps_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of cash flow per share regarding the next 4 quarters |
| 110 | `est_12m_cps_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of cash flow per share regarding the next 4 quarters, made in past 3 months |
| 111 | `est_12m_cps_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of cash flow per share regarding the next 4 quarters, made in the past 4 weeks |
| 112 | `est_12m_cps_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of cash flow per share regarding the next 4 quarters |
| 113 | `est_12m_cps_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of cash flow per share regarding the next 4 quarters, made in past 3 months |
| 114 | `est_12m_cps_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of cash flow per share regarding the next 4 quarters, made in the past 4 weeks |
| 115 | `est_12m_cps_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 116 | `est_12m_cps_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 117 | `est_12m_cps_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of cash flow per share regarding the next 4 quarters, where old and new estimates were made in the past  |
| 118 | `est_12m_cps_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of cash flow per share regarding the next 4 quarters |
| 119 | `est_12m_cps_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of cash flow per share regarding the next 4 quarters, made in the last 28 days |
| 120 | `est_12m_cps_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of cash flow per share regarding the next 4 quarters, made in the past 3 months |
| 121 | `est_12m_cps_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of cash flow per share regarding the next 4 quarters, made in past 4 weeks |
| 122 | `est_12m_cps_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of cash flow per share regarding the next 4 quarters |
| 123 | `est_12m_cps_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of cash flow per share regarding the next 4 quarters, made in the past 3 months |
| 124 | `est_12m_cps_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of cash flow per share regarding the next 4 quarters, made in past 4 weeks |
| 125 | `est_12m_cps_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of cash flow per share regarding the next 4 quarters |
| 126 | `est_12m_cps_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of cash flow per share regarding the next 4 quarters, made in the last 28 days |
| 127 | `est_12m_cps_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of cash flow per share regarding the next 4 quarters, made in past 3 months |
| 128 | `est_12m_cps_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of cash flow per share regarding the next 4 quarters, where old and new estimates were made in the past 4 weeks |
| 129 | `est_12m_cps_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of cash flow per share regarding the next 4 quarters, compared to the last weekly update |
| 130 | `est_12m_cps_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of cash flow per share regarding the next 4 quarters, compared to the last monthly update |
| 131 | `est_12m_cps_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of cash flow per share regarding the next 4 quarters, where old and new estimates were made in the past 4 |
| 132 | `est_12m_cps_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of cash flow per share regarding the next 4 quarters |
| 133 | `est_12m_cps_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of cash flow per share regarding the next 4 quarters, made in the last 28 days |
| 134 | `est_12m_cps_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of cash flow per share regarding the next 4 quarters, made in past 3 months |
| 135 | `est_12m_cps_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of cash flow per share regarding the next 4 quarters, made in the past 4 weeks |
| 136 | `est_12m_cpx_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of capital expenditure regarding the next 4 quarters |
| 137 | `est_12m_cpx_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of capital expenditure regarding the next 4 quarters, made in the past 3 months |
| 138 | `est_12m_cpx_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of capital expenditure regarding the next 4 quarters, made in the past 4 weeks |
| 139 | `est_12m_cpx_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of capital expenditure regarding the next 4 quarters |
| 140 | `est_12m_cpx_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of capital expenditure regarding the next 4 quarters, made in the past 3 months |
| 141 | `est_12m_cpx_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of capital expenditure regarding the next 4 quarters, made in the past 4 weeks |
| 142 | `est_12m_cpx_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 143 | `est_12m_cpx_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 144 | `est_12m_cpx_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of capital expenditure regarding the next 4 quarters, where old and new estimates were made in the past  |
| 145 | `est_12m_cpx_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of capital expenditure regarding the next 4 quarters |
| 146 | `est_12m_cpx_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of capital expenditure regarding the next 4 quarters, made in the last 28 days |
| 147 | `est_12m_cpx_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of capital expenditure regarding the next 4 quarters, made in past 3 months |
| 148 | `est_12m_cpx_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of capital expenditure regarding the next 4 quarters, made in past 4 weeks |
| 149 | `est_12m_cpx_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of capital expenditure regarding the next 4 quarters |
| 150 | `est_12m_cpx_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of capital expenditure regarding the next 4 quarters, made in past 3 months |
| 151 | `est_12m_cpx_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of capital expenditure regarding the next 4 quarters, made in the past 4 weeks |
| 152 | `est_12m_cpx_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimate of capital expenditure regarding the next 4 quarters |
| 153 | `est_12m_cpx_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of capital expenditure regarding the next 4 quarters, made in the last 28 days |
| 154 | `est_12m_cpx_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of capital expenditure regarding the next 4 quarters, made in the past 3 months |
| 155 | `est_12m_cpx_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of capital expenditure regarding the next 4 quarters, where old and new estimates were made in the past 4 weeks |
| 156 | `est_12m_cpx_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of capital expenditure regarding the next 4 quarters, compared to the last weekly update |
| 157 | `est_12m_cpx_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of capital expenditure regarding the next 4 quarters, compared to last monthly update |
| 158 | `est_12m_cpx_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of capital expenditure regarding the next 4 quarters, where old and new estimates were made in the past 4 |
| 159 | `est_12m_cpx_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimate of capital expenditure regarding the next 4 quarters |
| 160 | `est_12m_cpx_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of capital expenditure regarding the next 4 quarters, made in the last 28 days |
| 161 | `est_12m_cpx_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of capital expenditure regarding the next 4 quarters, made in the past 3 months |
| 162 | `est_12m_cpx_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimates of capital expenditure regarding the next 4 quarters, made in past 4 weeks |
| 163 | `est_12m_csh_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of cash earnings per share regarding the next 4 quarters |
| 164 | `est_12m_csh_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of cash earnings per share regarding the next 4 quarters, made in the past 3 months |
| 165 | `est_12m_csh_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of cash earnings per share regarding the next 4 quarters, made in the past 4 weeks |
| 166 | `est_12m_csh_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of cash earnings per share regarding the next 4 quarters |
| 167 | `est_12m_csh_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of cash earnings per share regarding the next 4 quarters, made in the past 3 months |
| 168 | `est_12m_csh_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of cash earnings per share regarding the next 4 quarters, made in past 4 weeks |
| 169 | `est_12m_csh_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 170 | `est_12m_csh_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 171 | `est_12m_csh_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of cash earnings per share regarding the next 4 quarters, where old and new estimates were made in the p |
| 172 | `est_12m_csh_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of cash earnings per share regarding the next 4 quarters |
| 173 | `est_12m_csh_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of cash earnings per share regarding the next 4 quarters, made in the last 28 days |
| 174 | `est_12m_csh_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of cash earnings per share regarding the next 4 quarters, made in the past 3 months |
| 175 | `est_12m_csh_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of cash earnings per share regarding the next 4 quarters, made in the past 4 weeks |
| 176 | `est_12m_csh_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of cash earnings per share regarding the next 4 quarters |
| 177 | `est_12m_csh_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of cash earnings per share regarding the next 4 quarters, made in the past 3 months |
| 178 | `est_12m_csh_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of cash earnings per share regarding the next 4 quarters, made in past 4 weeks |
| 179 | `est_12m_csh_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of cash earnings per share regarding the next 4 quarters |
| 180 | `est_12m_csh_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of cash earnings per share regarding the next 4 quarters, made in the last 28 days |
| 181 | `est_12m_csh_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of cash earnings per share regarding the next 4 quarters, made in the past 3 months |
| 182 | `est_12m_csh_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of cash earnings per share regarding the next 4 quarters, where old and new estimates were made in past 4 weeks |
| 183 | `est_12m_csh_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of cash earnings per share regarding the next 4 quarters, compared to last weekly update |
| 184 | `est_12m_csh_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of cash earnings per share regarding the next 4 quarters, compared to the last monthly update |
| 185 | `est_12m_csh_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of cash earnings per share regarding the next 4 quarters, where old and new estimates were made in the pa |
| 186 | `est_12m_csh_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of cash earnings per share regarding the next 4 quarters |
| 187 | `est_12m_csh_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of cash earnings per share regarding the next 4 quarters, made in the last 28 days |
| 188 | `est_12m_csh_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of cash earnings per share regarding the next 4 quarters, made in the past 3 months |
| 189 | `est_12m_csh_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimates of cash earnings per share regarding the next 4 quarters, made in past 4 weeks |
| 190 | `est_12m_dps_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of dividend per share regarding the next 4 quarters |
| 191 | `est_12m_dps_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of dividend per share regarding the next 4 quarters, made in past 3 months |
| 192 | `est_12m_dps_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of dividend per share regarding the next 4 quarters, made in past 4 weeks |
| 193 | `est_12m_dps_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of dividend per share regarding the next 4 quarters |
| 194 | `est_12m_dps_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of dividend per share regarding the next 4 quarters, made in the past 3 months |
| 195 | `est_12m_dps_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of dividend per share regarding the next 4 quarters, made in the past 4 weeks |
| 196 | `est_12m_dps_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 197 | `est_12m_dps_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 198 | `est_12m_dps_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of dividend per share regarding the next 4 quarters, where old and new estimates were made in the past 4 |
| 199 | `est_12m_dps_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of dividend per share regarding the next 4 quarters |
| 200 | `est_12m_dps_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of dividend per share regarding the next 4 quarters, made in the last 28 days |
| 201 | `est_12m_dps_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of dividend per share regarding the next 4 quarters, made in the past 3 months |
| 202 | `est_12m_dps_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of dividend per share regarding the next 4 quarters, made in past 4 weeks |
| 203 | `est_12m_dps_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of dividend per share regarding the next 4 quarters |
| 204 | `est_12m_dps_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of dividend per share regarding the next 4 quarters, made in the past 3 months |
| 205 | `est_12m_dps_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of dividend per share regarding the next 4 quarters, made in the past 4 weeks |
| 206 | `est_12m_dps_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of dividend per share regarding the next 4 quarters |
| 207 | `est_12m_dps_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of dividend per share regarding the next 4 quarters, made in the last 28 days |
| 208 | `est_12m_dps_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of dividend per share regarding the next 4 quarters, made in past 3 months |
| 209 | `est_12m_dps_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of dividend per share regarding the next 4 quarters, where old and new estimates were made in the past 4 weeks |
| 210 | `est_12m_dps_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of dividend per share regarding the next 4 quarters, compared to the last weekly update |
| 211 | `est_12m_dps_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of dividend per share regarding the next 4 quarters, compared to the last monthly update |
| 212 | `est_12m_dps_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of dividend per share regarding the next 4 quarters, where old and new estimates were made in the past 4  |
| 213 | `est_12m_dps_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimate of dividend per share regarding the next 4 quarters |
| 214 | `est_12m_dps_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimates of dividend per share regarding the next 4 quarters, made in the last 28 days |
| 215 | `est_12m_dps_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimates of dividend per share regarding the next 4 quarters, made in the past 3 months |
| 216 | `est_12m_dps_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of dividend per share regarding the next 4 quarters, made in the past 4 weeks |
| 217 | `est_12m_ebg_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of earnings before goodwill per share regarding the next 4 quarters |
| 218 | `est_12m_ebg_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of earnings before goodwill per share regarding the next 4 quarters |
| 219 | `est_12m_ebg_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of earnings before goodwill per share regarding the next 4 quarters |
| 220 | `est_12m_ebg_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of earnings before goodwill per share regarding the next 4 quarters |
| 221 | `est_12m_ebg_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of earnings before goodwill per share regarding the next 4 quarters |
| 222 | `est_12m_ebg_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of earnings before goodwill per share regarding the next 4 quarters |
| 223 | `est_12m_ebi_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of EBIT regarding the next 4 quarters |
| 224 | `est_12m_ebi_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of EBIT regarding the next 4 quarters, made in the past 3 months |
| 225 | `est_12m_ebi_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of EBIT regarding the next 4 quarters, made in the past 4 weeks |
| 226 | `est_12m_ebi_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of EBIT regarding the next 4 quarters |
| 227 | `est_12m_ebi_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of EBIT regarding the next 4 quarters, made in past 3 months |
| 228 | `est_12m_ebi_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of EBIT regarding the next 4 quarters, made in the past 4 weeks |
| 229 | `est_12m_ebi_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 230 | `est_12m_ebi_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 231 | `est_12m_ebi_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of EBIT regarding the next 4 quarters, where old and new estimates were made in the past 4 weeks |
| 232 | `est_12m_ebi_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of EBIT regarding the next 4 quarters |
| 233 | `est_12m_ebi_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of EBIT regarding the next 4 quarters, made in the last 28 days |
| 234 | `est_12m_ebi_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of EBIT regarding the next 4 quarters, made in the past 3 months |
| 235 | `est_12m_ebi_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of EBIT regarding the next 4 quarters, made in past 4 weeks |
| 236 | `est_12m_ebi_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of EBIT regarding the next 4 quarters |
| 237 | `est_12m_ebi_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of EBIT regarding the next 4 quarters, made in the past 3 months |
| 238 | `est_12m_ebi_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of EBIT regarding the next 4 quarters, made in the past 4 weeks |
| 239 | `est_12m_ebi_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of EBIT regarding the next 4 quarters |
| 240 | `est_12m_ebi_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of EBIT regarding the next 4 quarters, made in the last 28 days |
| 241 | `est_12m_ebi_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of EBIT regarding the next 4 quarters, made in the past 3 months |
| 242 | `est_12m_ebi_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of EBIT regarding the next 4 quarters, where old and new estimates were made in the past 4 weeks |
| 243 | `est_12m_ebi_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of EBIT regarding the next 4 quarters, compared to the last weekly update |
| 244 | `est_12m_ebi_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of EBIT regarding the next 4 quarters, compared to last monthly update |
| 245 | `est_12m_ebi_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of EBIT regarding the next 4 quarters, where old and new estimates were made in past 4 weeks |
| 246 | `est_12m_ebi_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of EBIT regarding the next 4 quarters |
| 247 | `est_12m_ebi_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimates of EBIT regarding the next 4 quarters, made in the last 28 days |
| 248 | `est_12m_ebi_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of EBIT regarding the next 4 quarters, made in the past 3 months |
| 249 | `est_12m_ebi_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimates of EBIT regarding the next 4 quarters, made in past 4 weeks |
| 250 | `est_12m_ebs_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of EBITDA per share regarding the next 4 quarters |
| 251 | `est_12m_ebs_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of EBITDA per share regarding the next 4 quarters, made in the past 3 months |
| 252 | `est_12m_ebs_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of EBITDA per share regarding the next 4 quarters, made in the past 4 weeks |
| 253 | `est_12m_ebs_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of EBITDA per share regarding the next 4 quarters |
| 254 | `est_12m_ebs_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of EBITDA per share regarding the next 4 quarters, made in past 3 months |
| 255 | `est_12m_ebs_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of EBITDA per share regarding the next 4 quarters, made in the past 4 weeks |
| 256 | `est_12m_ebs_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 257 | `est_12m_ebs_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 258 | `est_12m_ebs_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of EBITDA per share regarding the next 4 quarters, where old and new estimates were made in the past 4 w |
| 259 | `est_12m_ebs_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of EBITDA per share regarding the next 4 quarters |
| 260 | `est_12m_ebs_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of EBITDA per share regarding the next 4 quarters, made in the last 28 days |
| 261 | `est_12m_ebs_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of EBITDA per share regarding the next 4 quarters, made in the past 3 months |
| 262 | `est_12m_ebs_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of EBITDA per share regarding the next 4 quarters, made in the past 4 weeks |
| 263 | `est_12m_ebs_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of EBITDA per share regarding the next 4 quarters |
| 264 | `est_12m_ebs_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of EBITDA per share regarding the next 4 quarters, made in the past 3 months |
| 265 | `est_12m_ebs_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of EBITDA per share regarding the next 4 quarters, made in the past 4 weeks |
| 266 | `est_12m_ebs_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of EBITDA per share regarding the next 4 quarters |
| 267 | `est_12m_ebs_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of EBITDA per share regarding the next 4 quarters, made in the last 28 days |
| 268 | `est_12m_ebs_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of EBITDA per share regarding the next 4 quarters, made in the past 3 months |
| 269 | `est_12m_ebs_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of EBITDA per share regarding the next 4 quarters, where old and new estimates were made in the past 4 weeks |
| 270 | `est_12m_ebs_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of EBITDA per share regarding the next 4 quarters, compared to the last weekly update |
| 271 | `est_12m_ebs_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of EBITDA per share regarding the next 4 quarters, compared to the last monthly update |
| 272 | `est_12m_ebs_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimate of EBITDA per share regarding the next 4 quarters, where old and new estimates were made in past 4 weeks |
| 273 | `est_12m_ebt_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of EBITDA regarding the next 4 quarters |
| 274 | `est_12m_ebt_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of EBITDA regarding the next 4 quarters, made in the past 3 months |
| 275 | `est_12m_ebt_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of EBITDA regarding the next 4 quarters, made in the past 4 weeks |
| 276 | `est_12m_ebt_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of EBITDA regarding the next 4 quarters |
| 277 | `est_12m_ebt_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of EBITDA regarding the next 4 quarters, made in the past 3 months |
| 278 | `est_12m_ebt_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of EBITDA regarding the next 4 quarters, made in the past 4 weeks |
| 279 | `est_12m_ebt_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 280 | `est_12m_ebt_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 281 | `est_12m_ebt_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimate of EBITDA regarding the next 4 quarters, where old and new estimate were made in past 4 weeks |
| 282 | `est_12m_ebt_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of EBITDA regarding the next 4 quarters |
| 283 | `est_12m_ebt_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of EBITDA regarding the next 4 quarters, made in the last 28 days |
| 284 | `est_12m_ebt_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of EBITDA regarding the next 4 quarters, made in the past 3 months |
| 285 | `est_12m_ebt_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of EBITDA regarding the next 4 quarters, made in past 4 weeks |
| 286 | `est_12m_ebt_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of EBITDA regarding the next 4 quarters |
| 287 | `est_12m_ebt_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of EBITDA regarding the next 4 quarters, made in the past 3 months |
| 288 | `est_12m_ebt_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of EBITDA regarding the next 4 quarters, made in past 4 weeks |
| 289 | `est_12m_ebt_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of EBITDA regarding the next 4 quarters |
| 290 | `est_12m_ebt_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of EBITDA regarding the next 4 quarters, made in the last 28 days |
| 291 | `est_12m_ebt_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of EBITDA regarding the next 4 quarters, made in the past 3 months |
| 292 | `est_12m_ebt_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of EBITDA regarding the next 4 quarters, where old and new estimates were made in the past 4 weeks |
| 293 | `est_12m_ebt_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of EBITDA regarding the next 4 quarters, compared to the last weekly update |
| 294 | `est_12m_ebt_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of EBITDA regarding the next 4 quarters, compared to the last monthly update |
| 295 | `est_12m_ebt_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of EBITDA regarding the next 4 quarters, where old and new estimates were made in past 4 weeks |
| 296 | `est_12m_ebt_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of EBITDA regarding the next 4 quarters |
| 297 | `est_12m_ebt_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of EBITDA regarding the next 4 quarters, made in the last 28 days |
| 298 | `est_12m_ebt_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimates of EBITDA regarding the next 4 quarters, made in the past 3 months |
| 299 | `est_12m_ebt_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of EBITDA regarding the next 4 quarters, made in the past 4 weeks |
| 300 | `est_12m_ent_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of enterprise value regarding the next 4 quarters |
| 301 | `est_12m_ent_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of enterprise value regarding the next 4 quarters, made in the past 3 months |
| 302 | `est_12m_ent_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of enterprise value regarding the next 4 quarters, made in the past 4 weeks |
| 303 | `est_12m_ent_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of enterprise value regarding the next 4 quarters |
| 304 | `est_12m_ent_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of enterprise value regarding the next 4 quarters, made in past 3 months |
| 305 | `est_12m_ent_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of enterprise value regarding the next 4 quarters, made in past 4 weeks |
| 306 | `est_12m_ent_lowered_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of enterprise value regarding the next 4 quarters, since the last weekly update |
| 307 | `est_12m_ent_lowerednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimate of enterprise value regarding the next 4 quarters, since last monthly update |
| 308 | `est_12m_ent_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of enterprise value regarding the next 4 quarters, where old and new estimates were made in past 4 weeks |
| 309 | `est_12m_ent_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of enterprise value regarding the next 4 quarters |
| 310 | `est_12m_ent_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of enterprise value regarding the next 4 quarters, made in the last 28 days |
| 311 | `est_12m_ent_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of enterprise value regarding the next 4 quarters, made in the past 3 months |
| 312 | `est_12m_ent_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of enterprise value regarding the next 4 quarters, made in the past 4 weeks |
| 313 | `est_12m_ent_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of enterprise value regarding the next 4 quarters |
| 314 | `est_12m_ent_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of enterprise value regarding the next 4 quarters, made in the past 3 months |
| 315 | `est_12m_ent_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of enterprise value regarding the next 4 quarters, made in past 4 weeks |
| 316 | `est_12m_ent_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of enterprise value regarding the next 4 quarters |
| 317 | `est_12m_ent_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of enterprise value regarding the next 4 quarters, made in the last 28 days |
| 318 | `est_12m_ent_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of enterprise value regarding the next 4 quarters, made in the past 3 months |
| 319 | `est_12m_ent_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of enterprise value regarding the next 4 quarters, where old and new estimates were made in the past 4 weeks |
| 320 | `est_12m_ent_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of enterprise value regarding the next 4 quarters, compared to the last weekly update |
| 321 | `est_12m_ent_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of enterprise value regarding the next 4 quarters, compared to the last monthly update |
| 322 | `est_12m_ent_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of enterprise value regarding the next 4 quarters, where old and new estimates were made in the past 4 we |
| 323 | `est_12m_ent_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of enterprise value regarding the next 4 quarters |
| 324 | `est_12m_ent_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of enterprise value regarding the next 4 quarters, made in the last 28 days |
| 325 | `est_12m_ent_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of enterprise value regarding the next 4 quarters, made in the past 3 months |
| 326 | `est_12m_ent_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of enterprise value regarding the next 4 quarters, made in the past 4 weeks |
| 327 | `est_12m_eps_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of earnings per share regarding the next 4 quarters |
| 328 | `est_12m_eps_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of earnings per share regarding the next 4 quarters, made in the past 3 months |
| 329 | `est_12m_eps_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of earnings per share regarding the next 4 quarters, made in the past 4 weeks |
| 330 | `est_12m_eps_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of earnings per share regarding the next 4 quarters |
| 331 | `est_12m_eps_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of earnings per share regarding the next 4 quarters, made in the past 3 months |
| 332 | `est_12m_eps_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of earnings per share regarding the next 4 quarters, made in past 4 weeks |
| 333 | `est_12m_eps_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 334 | `est_12m_eps_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 335 | `est_12m_eps_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of earnings per share regarding the next 4 quarters, where old and new estimates were made in the past 4 |
| 336 | `est_12m_eps_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of earnings per share regarding the next 4 quarters |
| 337 | `est_12m_eps_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of earnings per share regarding the next 4 quarters, made in the last 28 days |
| 338 | `est_12m_eps_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of earnings per share regarding the next 4 quarters, made in the past 3 months |
| 339 | `est_12m_eps_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of earnings per share regarding the next 4 quarters, made in the past 4 weeks |
| 340 | `est_12m_eps_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of earnings per share regarding the next 4 quarters |
| 341 | `est_12m_eps_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of earnings per share regarding the next 4 quarters, made in the past 3 months |
| 342 | `est_12m_eps_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of earnings per share regarding the next 4 quarters, made in the past 4 weeks |
| 343 | `est_12m_eps_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of earnings per share regarding the next 4 quarters |
| 344 | `est_12m_eps_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of earnings per share regarding the next 4 quarters, made in the last 28 days |
| 345 | `est_12m_eps_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of earnings per share regarding the next 4 quarters, made in the past 3 months |
| 346 | `est_12m_eps_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of earnings per share regarding the next 4 quarters, where old and new estimates were made in the past 4 weeks |
| 347 | `est_12m_eps_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of earnings per share regarding the next 4 quarters, compared to last weekly update |
| 348 | `est_12m_eps_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of earnings per share regarding the next 4 quarters, compared to the last monthly update |
| 349 | `est_12m_eps_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of earnings per share regarding the next 4 quarters, where old and new estimates were made in the past 4  |
| 350 | `est_12m_eps_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of earnings per share regarding the next 4 quarters |
| 351 | `est_12m_eps_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of earnings per share regarding the next 4 quarters, made in the last 28 days |
| 352 | `est_12m_eps_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of earnings per share regarding the next 4 quarters, made in past 3 months |
| 353 | `est_12m_eps_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of earnings per share regarding the next 4 quarters, made in past 4 weeks |
| 354 | `est_12m_fcf_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of free cash flow per share regarding the next 4 quarters |
| 355 | `est_12m_fcf_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of free cash flow per share regarding the next 4 quarters, made in the past 3 months |
| 356 | `est_12m_fcf_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of free cash flow per share regarding the next 4 quarters, made in past 4 weeks |
| 357 | `est_12m_fcf_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of free cash flow per share regarding the next 4 quarters |
| 358 | `est_12m_fcf_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of free cash flow per share regarding the next 4 quarters, made in the past 3 months |
| 359 | `est_12m_fcf_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of free cash flow per share regarding the next 4 quarters, made in past 4 weeks |
| 360 | `est_12m_fcf_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 361 | `est_12m_fcf_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 362 | `est_12m_fcf_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of free cash flow per share regarding the next 4 quarters, where old and new estimates were made in the  |
| 363 | `est_12m_fcf_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of free cash flow per share regarding the next 4 quarters |
| 364 | `est_12m_fcf_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of free cash flow per share regarding the next 4 quarters, made in the last 28 days |
| 365 | `est_12m_fcf_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of free cash flow per share regarding the next 4 quarters, made in the past 3 months |
| 366 | `est_12m_fcf_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of free cash flow per share regarding the next 4 quarters, made in past 4 weeks |
| 367 | `est_12m_fcf_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of free cash flow per share regarding the next 4 quarters |
| 368 | `est_12m_fcf_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of free cash flow per share regarding the next 4 quarters, made in past 3 months |
| 369 | `est_12m_fcf_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of free cash flow per share regarding the next 4 quarters, made in the past 4 weeks |
| 370 | `est_12m_fcf_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of free cash flow per share regarding the next 4 quarters |
| 371 | `est_12m_fcf_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of free cash flow per share regarding the next 4 quarters, made in the last 28 days |
| 372 | `est_12m_fcf_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of free cash flow per share regarding the next 4 quarters, made in the past 3 months |
| 373 | `est_12m_fcf_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of free cash flow per share regarding the next 4 quarters, where old and new estimates were made in the past 4 w |
| 374 | `est_12m_fcf_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of free cash flow per share regarding the next 4 quarters, compared to the last weekly update |
| 375 | `est_12m_fcf_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of free cash flow per share regarding the next 4 quarters, compared to last monthly update |
| 376 | `est_12m_fcf_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of free cash flow per share regarding the next 4 quarters, where old and new estimates were made in the p |
| 377 | `est_12m_fcf_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of free cash flow per share regarding the next 4 quarters |
| 378 | `est_12m_fcf_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of free cash flow per share regarding the next 4 quarters, made in the last 28 days |
| 379 | `est_12m_fcf_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimates of free cash flow per share regarding the next 4 quarters, made in past 3 months |
| 380 | `est_12m_fcf_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of free cash flow per share regarding the next 4 quarters, made in the past 4 weeks |
| 381 | `est_12m_gps_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of GAAP earnings per share regarding the next 4 quarters |
| 382 | `est_12m_gps_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of GAAP earnings per share regarding the next 4 quarters, made in past 3 months |
| 383 | `est_12m_gps_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of GAAP earnings per share regarding the next 4 quarters, made in the past 4 weeks |
| 384 | `est_12m_gps_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of GAAP earnings per share regarding the next 4 quarters |
| 385 | `est_12m_gps_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of GAAP earnings per share regarding the next 4 quarters, made in the past 3 months |
| 386 | `est_12m_gps_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of GAAP earnings per share regarding the next 4 quarters, made in the past 4 weeks |
| 387 | `est_12m_gps_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 388 | `est_12m_gps_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 389 | `est_12m_gps_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of GAAP earnings per share regarding the next 4 quarters, where old and new estimates were made in the p |
| 390 | `est_12m_gps_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of GAAP earnings per share regarding the next 4 quarters |
| 391 | `est_12m_gps_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of GAAP earnings per share regarding the next 4 quarters, made in the last 28 days |
| 392 | `est_12m_gps_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of GAAP earnings per share regarding the next 4 quarters, made in the past 3 months |
| 393 | `est_12m_gps_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of GAAP earnings per share regarding the next 4 quarters, made in past 4 weeks |
| 394 | `est_12m_gps_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of GAAP earnings per share regarding the next 4 quarters |
| 395 | `est_12m_gps_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of GAAP earnings per share regarding the next 4 quarters, made in the past 3 months |
| 396 | `est_12m_gps_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of GAAP earnings per share regarding the next 4 quarters, made in past 4 weeks |
| 397 | `est_12m_gps_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of GAAP earnings per share regarding the next 4 quarters |
| 398 | `est_12m_gps_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of GAAP earnings per share regarding the next 4 quarters, made in the last 28 days |
| 399 | `est_12m_gps_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of GAAP earnings per share regarding the next 4 quarters, made in past 3 months |
| 400 | `est_12m_gps_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of GAAP earnings per share regarding the next 4 quarters, where old and new estimates were made in the past 4 we |
| 401 | `est_12m_gps_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of GAAP earnings per share regarding the next 4 quarters, compared to the last weekly update |
| 402 | `est_12m_gps_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of GAAP earnings per share regarding the next 4 quarters, compared to the last monthly update |
| 403 | `est_12m_gps_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of GAAP earnings per share regarding the next 4 quarters, where old and new estimates were made in the pa |
| 404 | `est_12m_gps_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of GAAP earnings per share regarding the next 4 quarters |
| 405 | `est_12m_gps_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of GAAP earnings per share regarding the next 4 quarters, made in the last 28 days |
| 406 | `est_12m_gps_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of GAAP earnings per share regarding the next 4 quarters, made in the past 3 months |
| 407 | `est_12m_gps_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of GAAP earnings per share regarding the next 4 quarters, made in the past 4 weeks |
| 408 | `est_12m_grm_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of gross margin in percent regarding the next 4 quarters |
| 409 | `est_12m_grm_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of gross margin in percent regarding the next 4 quarters, made in the past 3 months |
| 410 | `est_12m_grm_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of gross margin in percent regarding the next 4 quarters, made in the past 4 weeks |
| 411 | `est_12m_grm_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of gross margin in percent regarding the next 4 quarters |
| 412 | `est_12m_grm_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of gross margin in percent regarding the next 4 quarters, made in the past 3 months |
| 413 | `est_12m_grm_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of gross margin in percent regarding the next 4 quarters, made in the past 4 weeks |
| 414 | `est_12m_grm_lowered_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimate of gross margin in percent regarding the next 4 quarters, since last weekly update |
| 415 | `est_12m_grm_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 416 | `est_12m_grm_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of gross margin in percent regarding the next 4 quarters, where old and new estimates were made in the p |
| 417 | `est_12m_grm_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of gross margin in percent regarding the next 4 quarters |
| 418 | `est_12m_grm_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of gross margin in percent regarding the next 4 quarters, made in the last 28 days |
| 419 | `est_12m_grm_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of gross margin in percent regarding the next 4 quarters, made in past 3 months |
| 420 | `est_12m_grm_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of gross margin in percent regarding the next 4 quarters, made in the past 4 weeks |
| 421 | `est_12m_grm_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of gross margin in percent regarding the next 4 quarters |
| 422 | `est_12m_grm_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of gross margin in percent regarding the next 4 quarters, made in past 3 months |
| 423 | `est_12m_grm_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of gross margin in percent regarding the next 4 quarters, made in the past 4 weeks |
| 424 | `est_12m_grm_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of gross margin in percent regarding the next 4 quarters |
| 425 | `est_12m_grm_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of gross margin in percent regarding the next 4 quarters, made in the last 28 days |
| 426 | `est_12m_grm_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of gross margin in percent regarding the next 4 quarters, made in the past 3 months |
| 427 | `est_12m_grm_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of gross margin in percent regarding the next 4 quarters, where old and new estimates were made in the past 4 we |
| 428 | `est_12m_grm_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of gross margin in percent regarding the next 4 quarters, compared to the last weekly update |
| 429 | `est_12m_grm_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of gross margin in percent regarding the next 4 quarters, compared to the last monthly update |
| 430 | `est_12m_grm_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of gross margin in percent regarding the next 4 quarters, where old and new estimates were made in the pa |
| 431 | `est_12m_grm_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of gross margin in percent regarding the next 4 quarters |
| 432 | `est_12m_grm_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimates of gross margin in percent regarding the next 4 quarters, made in the last 28 days |
| 433 | `est_12m_grm_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimates of gross margin in percent regarding the next 4 quarters, made in past 3 months |
| 434 | `est_12m_grm_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of gross margin in percent regarding the next 4 quarters, made in the past 4 weeks |
| 435 | `est_12m_nav_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of net asset value regarding the next 4 quarters |
| 436 | `est_12m_nav_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of net asset value regarding the next 4 quarters, made in past 3 months |
| 437 | `est_12m_nav_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of net asset value regarding the next 4 quarters, made in the past 4 weeks |
| 438 | `est_12m_nav_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of net asset value regarding the next 4 quarters |
| 439 | `est_12m_nav_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of net asset value regarding the next 4 quarters, made in the past 3 months |
| 440 | `est_12m_nav_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of net asset value regarding the next 4 quarters, made in the past 4 weeks |
| 441 | `est_12m_nav_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 442 | `est_12m_nav_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 443 | `est_12m_nav_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of net asset value regarding the next 4 quarters, where old and new estimates were made in past 4 weeks |
| 444 | `est_12m_nav_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net asset value regarding the next 4 quarters |
| 445 | `est_12m_nav_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net asset value regarding the next 4 quarters, made in the last 28 days |
| 446 | `est_12m_nav_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net asset value regarding the next 4 quarters, made in past 3 months |
| 447 | `est_12m_nav_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net asset value regarding the next 4 quarters, made in the past 4 weeks |
| 448 | `est_12m_nav_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of net asset value regarding the next 4 quarters |
| 449 | `est_12m_nav_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of net asset value regarding the next 4 quarters, made in the past 3 months |
| 450 | `est_12m_nav_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of net asset value regarding the next 4 quarters, made in the past 4 weeks |
| 451 | `est_12m_nav_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net asset value regarding the next 4 quarters |
| 452 | `est_12m_nav_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net asset value regarding the next 4 quarters, made in the last 28 days |
| 453 | `est_12m_nav_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net asset value regarding the next 4 quarters, made in the past 3 months |
| 454 | `est_12m_nav_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net asset value regarding the next 4 quarters, where old and new estimates were made in the past 4 weeks |
| 455 | `est_12m_nav_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimate of net asset value regarding the next 4 quarters, compared to last weekly update |
| 456 | `est_12m_nav_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of net asset value regarding the next 4 quarters, compared to the last monthly update |
| 457 | `est_12m_nav_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of net asset value regarding the next 4 quarters, where old and new estimates were made in past 4 weeks |
| 458 | `est_12m_nav_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of net asset value regarding the next 4 quarters |
| 459 | `est_12m_nav_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of net asset value regarding the next 4 quarters, made in the last 28 days |
| 460 | `est_12m_nav_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimates of net asset value regarding the next 4 quarters, made in the past 3 months |
| 461 | `est_12m_nav_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of net asset value regarding the next 4 quarters, made in the past 4 weeks |
| 462 | `est_12m_ndt_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of net debt regarding the next 4 quarters |
| 463 | `est_12m_ndt_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of net debt regarding the next 4 quarters, made in past 3 months |
| 464 | `est_12m_ndt_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of net debt regarding the next 4 quarters, made in past 4 weeks |
| 465 | `est_12m_ndt_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of net debt regarding the next 4 quarters |
| 466 | `est_12m_ndt_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of net debt regarding the next 4 quarters, made in past 3 months |
| 467 | `est_12m_ndt_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of net debt regarding the next 4 quarters, made in past 4 weeks |
| 468 | `est_12m_ndt_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 469 | `est_12m_ndt_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 470 | `est_12m_ndt_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of net debt regarding the next 4 quarters, where old and new estimates were made in the past 4 weeks |
| 471 | `est_12m_ndt_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net debt regarding the next 4 quarters |
| 472 | `est_12m_ndt_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net debt regarding the next 4 quarters, made in the last 28 days |
| 473 | `est_12m_ndt_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net debt regarding the next 4 quarters, made in the past 3 months |
| 474 | `est_12m_ndt_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net debt regarding the next 4 quarters, made in the past 4 weeks |
| 475 | `est_12m_ndt_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of net debt regarding the next 4 quarters |
| 476 | `est_12m_ndt_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of net debt regarding the next 4 quarters, made in past 3 months |
| 477 | `est_12m_ndt_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of net debt regarding the next 4 quarters, made in the past 4 weeks |
| 478 | `est_12m_ndt_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net debt regarding the next 4 quarters |
| 479 | `est_12m_ndt_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net debt regarding the next 4 quarters, made in the last 28 days |
| 480 | `est_12m_ndt_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net debt regarding the next 4 quarters, made in the past 3 months |
| 481 | `est_12m_ndt_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net debt regarding the next 4 quarters, where old and new estimates were made in the past 4 weeks |
| 482 | `est_12m_ndt_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimate of net debt regarding the next 4 quarters, compared to last weekly update |
| 483 | `est_12m_ndt_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of net debt regarding the next 4 quarters, compared to the last monthly update |
| 484 | `est_12m_ndt_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of net debt regarding the next 4 quarters, where old and new estimates were made in the past 4 weeks |
| 485 | `est_12m_ndt_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of net debt regarding the next 4 quarters |
| 486 | `est_12m_ndt_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of net debt regarding the next 4 quarters, made in the last 28 days |
| 487 | `est_12m_ndt_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of net debt regarding the next 4 quarters, made in the past 3 months |
| 488 | `est_12m_ndt_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of net debt regarding the next 4 quarters, made in the past 4 weeks |
| 489 | `est_12m_ner_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of net profit as reported regarding the next 4 quarters |
| 490 | `est_12m_ner_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of net profit as reported regarding the next 4 quarters, made in the past 3 months |
| 491 | `est_12m_ner_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of net profit as reported regarding the next 4 quarters, made in past 4 weeks |
| 492 | `est_12m_ner_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of net profit as reported regarding the next 4 quarters |
| 493 | `est_12m_ner_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of net profit as reported regarding the next 4 quarters, made in the past 3 months |
| 494 | `est_12m_ner_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of net profit as reported regarding the next 4 quarters, made in the past 4 weeks |
| 495 | `est_12m_ner_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 496 | `est_12m_ner_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 497 | `est_12m_ner_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of net profit as reported regarding the next 4 quarters, where old and new estimates were made in the pa |
| 498 | `est_12m_ner_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net profit as reported regarding the next 4 quarters |
| 499 | `est_12m_ner_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net profit as reported regarding the next 4 quarters, made in the last 28 days |
| 500 | `est_12m_ner_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net profit as reported regarding the next 4 quarters, made in past 3 months |
| 501 | `est_12m_ner_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net profit as reported regarding the next 4 quarters, made in the past 4 weeks |
| 502 | `est_12m_ner_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of net profit as reported regarding the next 4 quarters |
| 503 | `est_12m_ner_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of net profit as reported regarding the next 4 quarters, made in the past 3 months |
| 504 | `est_12m_ner_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of net profit as reported regarding the next 4 quarters, made in the past 4 weeks |
| 505 | `est_12m_ner_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net profit as reported regarding the next 4 quarters |
| 506 | `est_12m_ner_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net profit as reported regarding the next 4 quarters, made in the last 28 days |
| 507 | `est_12m_ner_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net profit as reported regarding the next 4 quarters, made in the past 3 months |
| 508 | `est_12m_ner_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net profit as reported regarding the next 4 quarters, where old and new estimates were made in past 4 weeks |
| 509 | `est_12m_ner_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of net profit as reported regarding the next 4 quarters, compared to last weekly update |
| 510 | `est_12m_ner_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of net profit as reported regarding the next 4 quarters, compared to the last monthly update |
| 511 | `est_12m_ner_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of net profit as reported regarding the next 4 quarters, where old and new estimates were made in the pas |
| 512 | `est_12m_ner_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of net profit as reported regarding the next 4 quarters |
| 513 | `est_12m_ner_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of net profit as reported regarding the next 4 quarters, made in the last 28 days |
| 514 | `est_12m_ner_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimates of net profit as reported regarding the next 4 quarters, made in the past 3 months |
| 515 | `est_12m_ner_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of net profit as reported regarding the next 4 quarters, made in past 4 weeks |
| 516 | `est_12m_net_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of net income regarding the next 4 quarters |
| 517 | `est_12m_net_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of net income regarding the next 4 quarters, made in past 3 months |
| 518 | `est_12m_net_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of net income regarding the next 4 quarters, made in the past 4 weeks |
| 519 | `est_12m_net_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of net income regarding the next 4 quarters |
| 520 | `est_12m_net_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of net income regarding the next 4 quarters, made in the past 3 months |
| 521 | `est_12m_net_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of net income regarding the next 4 quarters, made in the past 4 weeks |
| 522 | `est_12m_net_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 523 | `est_12m_net_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 524 | `est_12m_net_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of net income regarding the next 4 quarters, where old and new estimates were made in the past 4 weeks |
| 525 | `est_12m_net_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net income regarding the next 4 quarters |
| 526 | `est_12m_net_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net income regarding the next 4 quarters, made in the last 28 days |
| 527 | `est_12m_net_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net income regarding the next 4 quarters, made in the past 3 months |
| 528 | `est_12m_net_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net income regarding the next 4 quarters, made in past 4 weeks |
| 529 | `est_12m_net_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of net income regarding the next 4 quarters |
| 530 | `est_12m_net_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of net income regarding the next 4 quarters, made in the past 3 months |
| 531 | `est_12m_net_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of net income regarding the next 4 quarters, made in the past 4 weeks |
| 532 | `est_12m_net_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net income regarding the next 4 quarters |
| 533 | `est_12m_net_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net income regarding the next 4 quarters, made in the last 28 days |
| 534 | `est_12m_net_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net income regarding the next 4 quarters, made in the past 3 months |
| 535 | `est_12m_net_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net income regarding the next 4 quarters, where old and new estimates were made in the past 4 weeks |
| 536 | `est_12m_net_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of net income regarding the next 4 quarters, compared to the last weekly update |
| 537 | `est_12m_net_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of net income regarding the next 4 quarters, compared to the last monthly update |
| 538 | `est_12m_net_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of net income regarding the next 4 quarters, where old and new estimates were made in past 4 weeks |
| 539 | `est_12m_net_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimate of net income regarding the next 4 quarters |
| 540 | `est_12m_net_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of net income regarding the next 4 quarters, made in the last 28 days |
| 541 | `est_12m_net_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of net income regarding the next 4 quarters, made in the past 3 months |
| 542 | `est_12m_net_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of net income regarding the next 4 quarters, made in the past 4 weeks |
| 543 | `est_12m_opr_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of operating profit regarding the next 4 quarters |
| 544 | `est_12m_opr_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of operating profit regarding the next 4 quarters, made in the past 3 months |
| 545 | `est_12m_opr_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of operating profit regarding the next 4 quarters, made in the past 4 weeks |
| 546 | `est_12m_opr_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of operating profit regarding the next 4 quarters |
| 547 | `est_12m_opr_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of operating profit regarding the next 4 quarters, made in past 3 months |
| 548 | `est_12m_opr_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of operating profit regarding the next 4 quarters, made in past 4 weeks |
| 549 | `est_12m_opr_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 550 | `est_12m_opr_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 551 | `est_12m_opr_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of operating profit regarding the next 4 quarters, where old and new estimates were made in the past 4 w |
| 552 | `est_12m_opr_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of operating profit regarding the next 4 quarters |
| 553 | `est_12m_opr_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of operating profit regarding the next 4 quarters, made in the last 28 days |
| 554 | `est_12m_opr_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of operating profit regarding the next 4 quarters, made in past 3 months |
| 555 | `est_12m_opr_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of operating profit regarding the next 4 quarters, made in the past 4 weeks |
| 556 | `est_12m_opr_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of operating profit regarding the next 4 quarters |
| 557 | `est_12m_opr_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of operating profit regarding the next 4 quarters, made in the past 3 months |
| 558 | `est_12m_opr_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of operating profit regarding the next 4 quarters, made in the past 4 weeks |
| 559 | `est_12m_opr_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of operating profit regarding the next 4 quarters |
| 560 | `est_12m_opr_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of operating profit regarding the next 4 quarters, made in the last 28 days |
| 561 | `est_12m_opr_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of operating profit regarding the next 4 quarters, made in the past 3 months |
| 562 | `est_12m_opr_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of operating profit regarding the next 4 quarters, where old and new estimates were made in the past 4 weeks |
| 563 | `est_12m_opr_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of operating profit regarding the next 4 quarters, compared to the last weekly update |
| 564 | `est_12m_opr_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of operating profit regarding the next 4 quarters, compared to the last monthly update |
| 565 | `est_12m_opr_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of operating profit regarding the next 4 quarters, where old and new estimates were made in the past 4 we |
| 566 | `est_12m_opr_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of operating profit regarding the next 4 quarters |
| 567 | `est_12m_opr_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of operating profit regarding the next 4 quarters, made in the last 28 days |
| 568 | `est_12m_opr_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimates of operating profit regarding the next 4 quarters, made in past 3 months |
| 569 | `est_12m_opr_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of operating profit regarding the next 4 quarters, made in past 4 weeks |
| 570 | `est_12m_pre_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of pre-tax profit regarding the next 4 quarters |
| 571 | `est_12m_pre_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of pre-tax profit regarding the next 4 quarters, made in the past 3 months |
| 572 | `est_12m_pre_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of pre-tax profit regarding the next 4 quarters, made in past 4 weeks |
| 573 | `est_12m_pre_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of pre-tax profit regarding the next 4 quarters |
| 574 | `est_12m_pre_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of pre-tax profit regarding the next 4 quarters, made in the past 3 months |
| 575 | `est_12m_pre_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of pre-tax profit regarding the next 4 quarters, made in the past 4 weeks |
| 576 | `est_12m_pre_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 577 | `est_12m_pre_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 578 | `est_12m_pre_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of pre-tax profit regarding the next 4 quarters, where old and new estimates were made in the past 4 wee |
| 579 | `est_12m_pre_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of pre-tax profit regarding the next 4 quarters |
| 580 | `est_12m_pre_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of pre-tax profit regarding the next 4 quarters, made in the last 28 days |
| 581 | `est_12m_pre_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of pre-tax profit regarding the next 4 quarters, made in the past 3 months |
| 582 | `est_12m_pre_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of pre-tax profit regarding the next 4 quarters, made in the past 4 weeks |
| 583 | `est_12m_pre_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of pre-tax profit regarding the next 4 quarters |
| 584 | `est_12m_pre_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of pre-tax profit regarding the next 4 quarters, made in the past 3 months |
| 585 | `est_12m_pre_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of pre-tax profit regarding the next 4 quarters, made in the past 4 weeks |
| 586 | `est_12m_pre_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of pre-tax profit regarding the next 4 quarters |
| 587 | `est_12m_pre_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of pre-tax profit regarding the next 4 quarters, made in the last 28 days |
| 588 | `est_12m_pre_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of pre-tax profit regarding the next 4 quarters, made in the past 3 months |
| 589 | `est_12m_pre_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of pre-tax profit regarding the next 4 quarters, where old and new estimates were made in the past 4 weeks |
| 590 | `est_12m_pre_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of pre-tax profit regarding the next 4 quarters, compared to last weekly update |
| 591 | `est_12m_pre_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of pre-tax profit regarding the next 4 quarters, compared to the last monthly update |
| 592 | `est_12m_pre_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of pre-tax profit regarding the next 4 quarters, where old and new estimates were made in the past 4 week |
| 593 | `est_12m_pre_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of pre-tax profit regarding the next 4 quarters |
| 594 | `est_12m_pre_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of pre-tax profit regarding the next 4 quarters, made in the last 28 days |
| 595 | `est_12m_pre_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of pre-tax profit regarding the next 4 quarters, made in the past 3 months |
| 596 | `est_12m_pre_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of pre-tax profit regarding the next 4 quarters, made in past 4 weeks |
| 597 | `est_12m_prr_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of pretax profit as reported regarding the next 4 quarters |
| 598 | `est_12m_prr_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of pretax profit as reported regarding the next 4 quarters, made in past 3 months |
| 599 | `est_12m_prr_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of pretax profit as reported regarding the next 4 quarters, made in the past 4 weeks |
| 600 | `est_12m_prr_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of pre-tax profit as reported regarding the next 4 quarters |
| 601 | `est_12m_prr_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of pretax profit as reported regarding the next 4 quarters, made in the past 3 months |
| 602 | `est_12m_prr_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of pre-tax profit as reported regarding the next 4 quarters, made in past 4 weeks |
| 603 | `est_12m_prr_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 604 | `est_12m_prr_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 605 | `est_12m_prr_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of pretax profit as reported regarding the next 4 quarters, where old and new estimates were made in the |
| 606 | `est_12m_prr_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of pretax profit as reported regarding the next 4 quarters |
| 607 | `est_12m_prr_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of pretax profit as reported regarding the next 4 quarters, made in the last 28 days |
| 608 | `est_12m_prr_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of pretax profit as reported regarding the next 4 quarters, made in the past 3 months |
| 609 | `est_12m_prr_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of pretax profit as reported regarding the next 4 quarters, made in the past 4 weeks |
| 610 | `est_12m_prr_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of pre-tax profit as reported regarding the next 4 quarters |
| 611 | `est_12m_prr_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of pretax profit as reported regarding the next 4 quarters, made in the past 3 months |
| 612 | `est_12m_prr_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of pretax profit as reported regarding the next 4 quarters, made in the past 4 weeks |
| 613 | `est_12m_prr_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of pretax profit as reported regarding the next 4 quarters |
| 614 | `est_12m_prr_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of pretax profit as reported regarding the next 4 quarters, made in the last 28 days |
| 615 | `est_12m_prr_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of pretax profit as reported regarding the next 4 quarters, made in the past 3 months |
| 616 | `est_12m_prr_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of pretax profit as reported regarding the next 4 quarters, where old and new estimates were made in the past 4  |
| 617 | `est_12m_prr_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of pretax profit as reported regarding the next 4 quarters, compared to the last weekly update |
| 618 | `est_12m_prr_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of pretax profit as reported regarding the next 4 quarters, compared to the last monthly update |
| 619 | `est_12m_prr_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of pretax profit as reported regarding the next 4 quarters, where old and new estimates were made in past |
| 620 | `est_12m_prr_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of pretax profit as reported regarding the next 4 quarters |
| 621 | `est_12m_prr_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of pretax profit as reported regarding the next 4 quarters, made in the last 28 days |
| 622 | `est_12m_prr_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of pretax profit as reported regarding the next 4 quarters, made in the past 3 months |
| 623 | `est_12m_prr_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of pretax profit as reported regarding the next 4 quarters, made in the past 4 weeks |
| 624 | `est_12m_roa_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of return on assets in percent regarding the next 4 quarters |
| 625 | `est_12m_roa_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of return on assets in percent regarding the next 4 quarters, made in the past 3 months |
| 626 | `est_12m_roa_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of return on assets in percent regarding the next 4 quarters, made in the past 4 weeks |
| 627 | `est_12m_roa_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of return on assets in percent regarding the next 4 quarters |
| 628 | `est_12m_roa_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of return on assets in percent regarding the next 4 quarters, made in the past 3 months |
| 629 | `est_12m_roa_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of return on assets in percent regarding the next 4 quarters, made in the past 4 weeks |
| 630 | `est_12m_roa_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 631 | `est_12m_roa_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 632 | `est_12m_roa_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of return on assets in percent regarding the next 4 quarters, where old and new estimates were made in t |
| 633 | `est_12m_roa_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of return on assets in percent regarding the next 4 quarters |
| 634 | `est_12m_roa_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of return on assets in percent regarding the next 4 quarters, made in the last 28 days |
| 635 | `est_12m_roa_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of return on assets in percent regarding the next 4 quarters, made in the past 3 months |
| 636 | `est_12m_roa_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of return on assets in percent regarding the next 4 quarters, made in the past 4 weeks |
| 637 | `est_12m_roa_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of return on assets in percent regarding the next 4 quarters |
| 638 | `est_12m_roa_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of return on assets in percent regarding the next 4 quarters, made in the past 3 months |
| 639 | `est_12m_roa_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of return on assets in percent regarding the next 4 quarters, made in past 4 weeks |
| 640 | `est_12m_roa_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of return on assets in percent regarding the next 4 quarters |
| 641 | `est_12m_roa_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of return on assets in percent regarding the next 4 quarters, made in the last 28 days |
| 642 | `est_12m_roa_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of return on assets in percent regarding the next 4 quarters, made in the past 3 months |
| 643 | `est_12m_roa_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of return on assets in percent regarding the next 4 quarters, where old and new estimates were made in the past  |
| 644 | `est_12m_roa_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of return on assets in percent regarding the next 4 quarters, compared to the last weekly update |
| 645 | `est_12m_roa_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of return on assets in percent regarding the next 4 quarters, compared to the last monthly update |
| 646 | `est_12m_roa_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of return on assets in percent regarding the next 4 quarters, where old and new estimates were made in th |
| 647 | `est_12m_roa_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of return on assets in percent regarding the next 4 quarters |
| 648 | `est_12m_roa_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of return on assets in percent regarding the next 4 quarters, made in the last 28 days |
| 649 | `est_12m_roa_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of return on assets in percent regarding the next 4 quarters, made in past 3 months |
| 650 | `est_12m_roa_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of return on assets in percent regarding the next 4 quarters, made in the past 4 weeks |
| 651 | `est_12m_roe_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of return on equity in percent regarding the next 4 quarters |
| 652 | `est_12m_roe_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of return on equity in percent regarding the next 4 quarters, made in the past 3 months |
| 653 | `est_12m_roe_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of return on equity in percent regarding the next 4 quarters, made in the past 4 weeks |
| 654 | `est_12m_roe_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of return on equity in percent regarding the next 4 quarters |
| 655 | `est_12m_roe_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of return on equity in percent regarding the next 4 quarters, made in the past 3 months |
| 656 | `est_12m_roe_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of return on equity in percent regarding the next 4 quarters, made in past 4 weeks |
| 657 | `est_12m_roe_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 658 | `est_12m_roe_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 659 | `est_12m_roe_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of return on equity in percent regarding the next 4 quarters, where old and new estimates were made in t |
| 660 | `est_12m_roe_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of return on equity in percent regarding the next 4 quarters |
| 661 | `est_12m_roe_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of return on equity in percent regarding the next 4 quarters, made in the last 28 days |
| 662 | `est_12m_roe_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of return on equity in percent regarding the next 4 quarters, made in the past 3 months |
| 663 | `est_12m_roe_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of return on equity in percent regarding the next 4 quarters, made in the past 4 weeks |
| 664 | `est_12m_roe_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of return on equity in percent regarding the next 4 quarters |
| 665 | `est_12m_roe_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of return on equity in percent regarding the next 4 quarters, made in past 3 months |
| 666 | `est_12m_roe_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of return on equity in percent regarding the next 4 quarters, made in past 4 weeks |
| 667 | `est_12m_roe_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of return on equity in percent regarding the next 4 quarters |
| 668 | `est_12m_roe_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of return on equity in percent regarding the next 4 quarters, made in the last 28 days |
| 669 | `est_12m_roe_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of return on equity in percent regarding the next 4 quarters, made in the past 3 months |
| 670 | `est_12m_roe_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of return on equity in percent regarding the next 4 quarters, where old and new estimates were made in the past  |
| 671 | `est_12m_roe_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of return on equity in percent regarding the next 4 quarters, compared to last weekly update |
| 672 | `est_12m_roe_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of return on equity in percent regarding the next 4 quarters, compared to last monthly update |
| 673 | `est_12m_roe_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of return on equity in percent regarding the next 4 quarters, where old and new estimates were made in pa |
| 674 | `est_12m_roe_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimate of return on equity in percent regarding the next 4 quarters |
| 675 | `est_12m_roe_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of return on equity in percent regarding the next 4 quarters, made in the last 28 days |
| 676 | `est_12m_roe_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of return on equity in percent regarding the next 4 quarters, made in the past 3 months |
| 677 | `est_12m_roe_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of return on equity in percent regarding the next 4 quarters, made in the past 4 weeks |
| 678 | `est_12m_sal_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of sales/revenue regarding the next 4 quarters |
| 679 | `est_12m_sal_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of sales/revenue regarding the next 4 quarters, made in the past 3 months |
| 680 | `est_12m_sal_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of sales/revenue regarding the next 4 quarters, made in the past 4 weeks |
| 681 | `est_12m_sal_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of sales/revenue regarding the next 4 quarters |
| 682 | `est_12m_sal_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of sales/revenue regarding the next 4 quarters, made in the past 3 months |
| 683 | `est_12m_sal_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of sales/revenue regarding the next 4 quarters, made in the past 4 weeks |
| 684 | `est_12m_sal_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 685 | `est_12m_sal_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 686 | `est_12m_sal_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of sales/revenue regarding the next 4 quarters, where old and new estimates were made in the past 4 week |
| 687 | `est_12m_sal_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of sales/revenue regarding the next 4 quarters |
| 688 | `est_12m_sal_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of sales/revenue regarding the next 4 quarters, made in the last 28 days |
| 689 | `est_12m_sal_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of sales/revenue regarding the next 4 quarters, made in past 3 months |
| 690 | `est_12m_sal_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of sales/revenue regarding the next 4 quarters, made in the past 4 weeks |
| 691 | `est_12m_sal_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of sales/revenue regarding the next 4 quarters |
| 692 | `est_12m_sal_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of sales/revenue regarding the next 4 quarters, made in past 3 months |
| 693 | `est_12m_sal_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of sales/revenue regarding the next 4 quarters, made in the past 4 weeks |
| 694 | `est_12m_sal_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of sales/revenue regarding the next 4 quarters |
| 695 | `est_12m_sal_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of sales/revenue regarding the next 4 quarters, made in the last 28 days |
| 696 | `est_12m_sal_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of sales/revenue regarding the next 4 quarters, made in the past 3 months |
| 697 | `est_12m_sal_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of sales/revenue regarding the next 4 quarters, where old and new estimates were made in the past 4 weeks |
| 698 | `est_12m_sal_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of sales/revenue regarding the next 4 quarters, compared to the last weekly update |
| 699 | `est_12m_sal_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of sales/revenue regarding the next 4 quarters, compared to the last monthly update |
| 700 | `est_12m_sal_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of sales/revenue regarding the next 4 quarters, where old and new estimates were made in past 4 weeks |
| 701 | `est_12m_sal_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of sales/revenue regarding the next 4 quarters |
| 702 | `est_12m_sal_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of sales/revenue regarding the next 4 quarters, made in the last 28 days |
| 703 | `est_12m_sal_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of sales/revenue regarding the next 4 quarters, made in the past 3 months |
| 704 | `est_12m_sal_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of sales/revenue regarding the next 4 quarters, made in the past 4 weeks |
| 705 | `est_12m_tbv_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of tangible book value per share regarding the next 4 quarters |
| 706 | `est_12m_tbv_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of tangible book value per share regarding the next 4 quarters, made in the past 3 months |
| 707 | `est_12m_tbv_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of tangible book value per share regarding the next 4 quarters, made in the past 4 weeks |
| 708 | `est_12m_tbv_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of tangible book value per share regarding the next 4 quarters |
| 709 | `est_12m_tbv_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of tangible book value per share regarding the next 4 quarters, made in the past 3 months |
| 710 | `est_12m_tbv_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of tangible book value per share regarding the next 4 quarters, made in the past 4 weeks |
| 711 | `est_12m_tbv_lowered_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimate of tangible book value per share regarding the next 4 quarters, since last weekly update |
| 712 | `est_12m_tbv_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 713 | `est_12m_tbv_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimate of tangible book value per share regarding the next 4 quarters, where old and new estimate were made in p |
| 714 | `est_12m_tbv_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of tangible book value per share regarding the next 4 quarters |
| 715 | `est_12m_tbv_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of tangible book value per share regarding the next 4 quarters, made in the last 28 days |
| 716 | `est_12m_tbv_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of tangible book value per share regarding the next 4 quarters, made in past 3 months |
| 717 | `est_12m_tbv_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of tangible book value per share regarding the next 4 quarters, made in the past 4 weeks |
| 718 | `est_12m_tbv_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of tangible book value per share regarding the next 4 quarters |
| 719 | `est_12m_tbv_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of tangible book value per share regarding the next 4 quarters, made in past 3 months |
| 720 | `est_12m_tbv_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of tangible book value per share regarding the next 4 quarters, made in past 4 weeks |
| 721 | `est_12m_tbv_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of tangible book value per share regarding the next 4 quarters |
| 722 | `est_12m_tbv_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of tangible book value per share regarding the next 4 quarters, made in the last 28 days |
| 723 | `est_12m_tbv_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of tangible book value per share regarding the next 4 quarters, made in the past 3 months |
| 724 | `est_12m_tbv_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of tangible book value per share regarding the next 4 quarters, where old and new estimates were made in the pas |
| 725 | `est_12m_tbv_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of tangible book value per share regarding the next 4 quarters, compared to the last weekly update |
| 726 | `est_12m_tbv_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of tangible book value per share regarding the next 4 quarters, compared to the last monthly update |
| 727 | `est_12m_tbv_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of tangible book value per share regarding the next 4 quarters, where old and new estimates were made in  |
| 728 | `est_12m_tbv_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimate of tangible book value per share regarding the next 4 quarters |
| 729 | `est_12m_tbv_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimates of tangible book value per share regarding the next 4 quarters, made in the past 3 months |
| 730 | `est_12m_tbv_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of tangible book value per share regarding the next 4 quarters, made in the past 4 weeks |
| 731 | `est_q_bps_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of book value per share regarding the next quarter |
| 732 | `est_q_bps_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of book value per share regarding the next quarter, made in the past 4 weeks |
| 733 | `est_q_bps_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of book value per share regarding the next quarter |
| 734 | `est_q_bps_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of book value per share regarding the next quarter, made in the past 4 weeks |
| 735 | `est_q_bps_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 736 | `est_q_bps_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 737 | `est_q_bps_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of book value per share regarding the next quarter, where old and new estimates were made in the past 4  |
| 738 | `est_q_bps_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of book value per share regarding the next quarter |
| 739 | `est_q_bps_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of book value per share regarding the next quarter, made in the last 28 days |
| 740 | `est_q_bps_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of book value per share regarding the next quarter, made in the past 4 weeks |
| 741 | `est_q_bps_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of book value per share regarding the next quarter |
| 742 | `est_q_bps_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of book value per share regarding the next quarter, made in the past 4 weeks |
| 743 | `est_q_bps_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of book value per share regarding the next quarter |
| 744 | `est_q_bps_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of book value per share regarding the next quarter, made in the last 28 days |
| 745 | `est_q_bps_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of book value per share regarding the next quarter, made in past 3 months |
| 746 | `est_q_bps_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of book value per share regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 747 | `est_q_bps_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of book value per share regarding the next quarter, compared to the last weekly update |
| 748 | `est_q_bps_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of book value per share regarding the next quarter, compared to last monthly update |
| 749 | `est_q_bps_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of book value per share regarding the next quarter, where old and new estimates were made in the past 4 w |
| 750 | `est_q_dps_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of dividend per share regarding the next quarter |
| 751 | `est_q_dps_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of dividend per share regarding the next quarter, made in past 3 months |
| 752 | `est_q_dps_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of dividend per share regarding the next quarter, made in past 4 weeks |
| 753 | `est_q_dps_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of dividend per share regarding the next quarter |
| 754 | `est_q_dps_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of dividend per share regarding the next quarter, made in past 3 months |
| 755 | `est_q_dps_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of dividend per share regarding the next quarter, made in the past 4 weeks |
| 756 | `est_q_dps_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 757 | `est_q_dps_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 758 | `est_q_dps_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of dividend per share regarding the next quarter, where old and new estimates were made in past 4 weeks |
| 759 | `est_q_dps_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of dividend per share regarding the next quarter |
| 760 | `est_q_dps_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of dividend per share regarding the next quarter, made in past 3 months |
| 761 | `est_q_dps_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of dividend per share regarding the next quarter, made in the past 4 weeks |
| 762 | `est_q_dps_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of dividend per share regarding the next quarter |
| 763 | `est_q_dps_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of dividend per share regarding the next quarter, made in the past 3 months |
| 764 | `est_q_dps_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of dividend per share regarding the next quarter, made in past 4 weeks |
| 765 | `est_q_dps_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of dividend per share regarding the next quarter |
| 766 | `est_q_dps_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of dividend per share regarding the next quarter, made in the last 28 days |
| 767 | `est_q_dps_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of dividend per share regarding the next quarter, made in past 3 months |
| 768 | `est_q_dps_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of dividend per share regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 769 | `est_q_dps_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of dividend per share regarding the next quarter, compared to the last weekly update |
| 770 | `est_q_dps_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of dividend per share regarding the next quarter, compared to last monthly update |
| 771 | `est_q_dps_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of dividend per share regarding the next quarter, where old and new estimates were made in past 4 weeks |
| 772 | `est_q_ebi_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of EBIT regarding the next quarter |
| 773 | `est_q_ebi_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of EBIT regarding the next quarter, made in the past 3 months |
| 774 | `est_q_ebi_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of EBIT regarding the next quarter, made in the past 4 weeks |
| 775 | `est_q_ebi_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of EBIT regarding the next quarter |
| 776 | `est_q_ebi_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of EBIT regarding the next quarter, made in the past 3 months |
| 777 | `est_q_ebi_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of EBIT regarding the next quarter, made in past 4 weeks |
| 778 | `est_q_ebi_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 779 | `est_q_ebi_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 780 | `est_q_ebi_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of EBIT regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 781 | `est_q_ebi_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of EBIT regarding the next quarter |
| 782 | `est_q_ebi_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of EBIT regarding the next quarter, made in the last 28 days |
| 783 | `est_q_ebi_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of EBIT regarding the next quarter, made in past 3 months |
| 784 | `est_q_ebi_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of EBIT regarding the next quarter, made in the past 4 weeks |
| 785 | `est_q_ebi_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of EBIT regarding the next quarter |
| 786 | `est_q_ebi_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of EBIT regarding the next quarter, made in the past 3 months |
| 787 | `est_q_ebi_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of EBIT regarding the next quarter, made in past 4 weeks |
| 788 | `est_q_ebi_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of EBIT regarding the next quarter |
| 789 | `est_q_ebi_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of EBIT regarding the next quarter, made in the last 28 days |
| 790 | `est_q_ebi_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of EBIT regarding the next quarter, made in the past 3 months |
| 791 | `est_q_ebi_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of EBIT regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 792 | `est_q_ebi_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of EBIT regarding the next quarter, compared to the last weekly update |
| 793 | `est_q_ebi_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of EBIT regarding the next quarter, compared to the last monthly update |
| 794 | `est_q_ebi_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of EBIT regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 795 | `est_q_ebi_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimate of EBIT regarding the next quarter |
| 796 | `est_q_ebi_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of EBIT regarding the next quarter, made in the last 28 days |
| 797 | `est_q_ebt_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of EBITDA regarding the next quarter |
| 798 | `est_q_ebt_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of EBITDA regarding the next quarter, made in the past 3 months |
| 799 | `est_q_ebt_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of EBITDA regarding the next quarter, made in the past 4 weeks |
| 800 | `est_q_ebt_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of EBITDA regarding the next quarter |
| 801 | `est_q_ebt_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of EBITDA regarding the next quarter, made in the past 3 months |
| 802 | `est_q_ebt_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of EBITDA regarding the next quarter, made in past 4 weeks |
| 803 | `est_q_ebt_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 804 | `est_q_ebt_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 805 | `est_q_ebt_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of EBITDA regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 806 | `est_q_ebt_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of EBITDA regarding the next quarter |
| 807 | `est_q_ebt_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of EBITDA regarding the next quarter, made in the last 28 days |
| 808 | `est_q_ebt_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of EBITDA regarding the next quarter, made in the past 3 months |
| 809 | `est_q_ebt_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of EBITDA regarding the next quarter, made in past 4 weeks |
| 810 | `est_q_ebt_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of EBITDA regarding the next quarter |
| 811 | `est_q_ebt_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of EBITDA regarding the next quarter, made in the past 3 months |
| 812 | `est_q_ebt_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of EBITDA regarding the next quarter, made in the past 4 weeks |
| 813 | `est_q_ebt_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of EBITDA regarding the next quarter |
| 814 | `est_q_ebt_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of EBITDA regarding the next quarter, made in the last 28 days |
| 815 | `est_q_ebt_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of EBITDA regarding the next quarter, made in the past 3 months |
| 816 | `est_q_ebt_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of EBITDA regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 817 | `est_q_ebt_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of EBITDA regarding the next quarter, compared to last weekly update |
| 818 | `est_q_ebt_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of EBITDA regarding the next quarter, compared to last monthly update |
| 819 | `est_q_ebt_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of EBITDA regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 820 | `est_q_ebt_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimate of EBITDA regarding the next quarter |
| 821 | `est_q_ebt_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of EBITDA regarding the next quarter, made in the last 28 days |
| 822 | `est_q_ent_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of enterprise value regarding the next quarter |
| 823 | `est_q_ent_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of enterprise value regarding the next quarter |
| 824 | `est_q_ent_lowered_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of enterprise value regarding the next quarter, since last weekly update |
| 825 | `est_q_ent_lowerednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of enterprise value regarding the next quarter, since the last monthly update |
| 826 | `est_q_ent_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of enterprise value regarding the next quarter, where old and new estimates were made in the past 4 week |
| 827 | `est_q_ent_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of enterprise value regarding the next quarter |
| 828 | `est_q_ent_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of enterprise value regarding the next quarter |
| 829 | `est_q_ent_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of enterprise value regarding the next quarter |
| 830 | `est_q_ent_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimate of enterprise value regarding the next quarter, made in the last 28 days |
| 831 | `est_q_ent_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of enterprise value regarding the next quarter, made in past 3 months |
| 832 | `est_q_ent_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of enterprise value regarding the next quarter, where old and new estimates were made in past 4 weeks |
| 833 | `est_q_ent_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of enterprise value regarding the next quarter, compared to the last weekly update |
| 834 | `est_q_ent_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of enterprise value regarding the next quarter, compared to last monthly update |
| 835 | `est_q_ent_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of enterprise value regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 836 | `est_q_eps_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of earnings per share regarding the next quarter |
| 837 | `est_q_eps_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of earnings per share regarding the next quarter, made in the past 3 months |
| 838 | `est_q_eps_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of earnings per share regarding the next quarter, made in the past 4 weeks |
| 839 | `est_q_eps_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of earnings per share regarding the next quarter |
| 840 | `est_q_eps_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of earnings per share regarding the next quarter, made in the past 3 months |
| 841 | `est_q_eps_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of earnings per share regarding the next quarter, made in past 4 weeks |
| 842 | `est_q_eps_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 843 | `est_q_eps_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 844 | `est_q_eps_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of earnings per share regarding the next quarter, where old and new estimates were made in the past 4 we |
| 845 | `est_q_eps_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of earnings per share regarding the next quarter |
| 846 | `est_q_eps_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of earnings per share regarding the next quarter, made in the last 28 days |
| 847 | `est_q_eps_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of earnings per share regarding the next quarter, made in the past 3 months |
| 848 | `est_q_eps_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of earnings per share regarding the next quarter, made in the past 4 weeks |
| 849 | `est_q_eps_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of earnings per share regarding the next quarter |
| 850 | `est_q_eps_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of earnings per share regarding the next quarter, made in past 3 months |
| 851 | `est_q_eps_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of earnings per share regarding the next quarter, made in past 4 weeks |
| 852 | `est_q_eps_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of earnings per share regarding the next quarter |
| 853 | `est_q_eps_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of earnings per share regarding the next quarter, made in the last 28 days |
| 854 | `est_q_eps_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimate of earnings per share regarding the next quarter, made in the past 3 months |
| 855 | `est_q_eps_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of earnings per share regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 856 | `est_q_eps_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of earnings per share regarding the next quarter, compared to last weekly update |
| 857 | `est_q_eps_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of earnings per share regarding the next quarter, compared to last monthly update |
| 858 | `est_q_eps_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of earnings per share regarding the next quarter, where old and new estimates were made in the past 4 wee |
| 859 | `est_q_eps_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of earnings per share regarding the next quarter |
| 860 | `est_q_eps_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of earnings per share regarding the next quarter, made in the last 28 days |
| 861 | `est_q_eps_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimates of earnings per share regarding the next quarter, made in past 3 months |
| 862 | `est_q_eps_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of earnings per share regarding the next quarter, made in the past 4 weeks |
| 863 | `est_q_gps_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of GAAP earnings per share regarding the next quarter |
| 864 | `est_q_gps_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of GAAP earnings per share regarding the next quarter, made in the past 3 months |
| 865 | `est_q_gps_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of GAAP earnings per share regarding the next quarter, made in past 4 weeks |
| 866 | `est_q_gps_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of GAAP earnings per share regarding the next quarter |
| 867 | `est_q_gps_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of GAAP earnings per share regarding the next quarter, made in past 3 months |
| 868 | `est_q_gps_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of GAAP earnings per share regarding the next quarter, made in the past 4 weeks |
| 869 | `est_q_gps_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 870 | `est_q_gps_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 871 | `est_q_gps_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of GAAP earnings per share regarding the next quarter, where old and new estimates were made in past 4 w |
| 872 | `est_q_gps_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of GAAP earnings per share regarding the next quarter |
| 873 | `est_q_gps_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of GAAP earnings per share regarding the next quarter, made in the last 28 days |
| 874 | `est_q_gps_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of GAAP earnings per share regarding the next quarter, made in the past 3 months |
| 875 | `est_q_gps_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of GAAP earnings per share regarding the next quarter, made in past 4 weeks |
| 876 | `est_q_gps_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of GAAP earnings per share regarding the next quarter |
| 877 | `est_q_gps_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of GAAP earnings per share regarding the next quarter, made in past 3 months |
| 878 | `est_q_gps_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of GAAP earnings per share regarding the next quarter, made in the past 4 weeks |
| 879 | `est_q_gps_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of GAAP earnings per share regarding the next quarter |
| 880 | `est_q_gps_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of GAAP earnings per share regarding the next quarter, made in the last 28 days |
| 881 | `est_q_gps_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of GAAP earnings per share regarding the next quarter, made in the past 3 months |
| 882 | `est_q_gps_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of GAAP earnings per share regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 883 | `est_q_gps_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of GAAP earnings per share regarding the next quarter, compared to the last weekly update |
| 884 | `est_q_gps_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of GAAP earnings per share regarding the next quarter, compared to the last monthly update |
| 885 | `est_q_gps_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of GAAP earnings per share regarding the next quarter, where old and new estimates were made in past 4 we |
| 886 | `est_q_gps_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimate of GAAP earnings per share regarding the next quarter |
| 887 | `est_q_grm_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of gross margin in percent regarding the next quarter |
| 888 | `est_q_grm_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of gross margin in percent regarding the next quarter |
| 889 | `est_q_grm_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 890 | `est_q_grm_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 891 | `est_q_grm_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimate of gross margin in percent regarding the next quarter, where old and new estimate were made in past 4 wee |
| 892 | `est_q_grm_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of gross margin in percent regarding the next quarter |
| 893 | `est_q_grm_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of gross margin in percent regarding the next quarter |
| 894 | `est_q_grm_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of gross margin in percent regarding the next quarter |
| 895 | `est_q_grm_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of gross margin in percent regarding the next quarter, made in the last 28 days |
| 896 | `est_q_grm_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of gross margin in percent regarding the next quarter, made in the past 3 months |
| 897 | `est_q_grm_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of gross margin in percent regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 898 | `est_q_grm_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimate of gross margin in percent regarding the next quarter, compared to the last weekly update |
| 899 | `est_q_grm_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of gross margin in percent regarding the next quarter, compared to last monthly update |
| 900 | `est_q_grm_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of gross margin in percent regarding the next quarter, where old and new estimates were made in the past  |
| 901 | `est_q_nav_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of net asset value regarding the next quarter |
| 902 | `est_q_nav_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of net asset value regarding the next quarter, made in past 3 months |
| 903 | `est_q_nav_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of net asset value regarding the next quarter, made in past 4 weeks |
| 904 | `est_q_nav_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of net asset value regarding the next quarter |
| 905 | `est_q_nav_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of net asset value regarding the next quarter, made in past 3 months |
| 906 | `est_q_nav_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of net asset value regarding the next quarter, made in the past 4 weeks |
| 907 | `est_q_nav_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 908 | `est_q_nav_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 909 | `est_q_nav_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of net asset value regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 910 | `est_q_nav_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net asset value regarding the next quarter |
| 911 | `est_q_nav_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net asset value regarding the next quarter, made in the last 28 days |
| 912 | `est_q_nav_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net asset value regarding the next quarter, made in past 3 months |
| 913 | `est_q_nav_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net asset value regarding the next quarter, made in the past 4 weeks |
| 914 | `est_q_nav_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of net asset value regarding the next quarter |
| 915 | `est_q_nav_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of net asset value regarding the next quarter, made in past 3 months |
| 916 | `est_q_nav_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of net asset value regarding the next quarter, made in the past 4 weeks |
| 917 | `est_q_nav_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net asset value regarding the next quarter |
| 918 | `est_q_nav_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net asset value regarding the next quarter, made in the last 28 days |
| 919 | `est_q_nav_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net asset value regarding the next quarter, made in the past 3 months |
| 920 | `est_q_nav_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net asset value regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 921 | `est_q_nav_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of net asset value regarding the next quarter, compared to the last weekly update |
| 922 | `est_q_nav_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of net asset value regarding the next quarter, compared to the last monthly update |
| 923 | `est_q_nav_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of net asset value regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 924 | `est_q_ndt_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of net debt regarding the next quarter |
| 925 | `est_q_ndt_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of net debt regarding the next quarter, made in the past 3 months |
| 926 | `est_q_ndt_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of net debt regarding the next quarter, made in the past 4 weeks |
| 927 | `est_q_ndt_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of net debt regarding the next quarter |
| 928 | `est_q_ndt_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of net debt regarding the next quarter, made in past 3 months |
| 929 | `est_q_ndt_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of net debt regarding the next quarter, made in the past 4 weeks |
| 930 | `est_q_ndt_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 931 | `est_q_ndt_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 932 | `est_q_ndt_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of net debt regarding the next quarter, where old and new estimates were made in past 4 weeks |
| 933 | `est_q_ndt_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net debt regarding the next quarter |
| 934 | `est_q_ndt_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net debt regarding the next quarter, made in the last 28 days |
| 935 | `est_q_ndt_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net debt regarding the next quarter, made in past 3 months |
| 936 | `est_q_ndt_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net debt regarding the next quarter, made in the past 4 weeks |
| 937 | `est_q_ndt_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of net debt regarding the next quarter |
| 938 | `est_q_ndt_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of net debt regarding the next quarter, made in the past 3 months |
| 939 | `est_q_ndt_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of net debt regarding the next quarter, made in the past 4 weeks |
| 940 | `est_q_ndt_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net debt regarding the next quarter |
| 941 | `est_q_ndt_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net debt regarding the next quarter, made in the last 28 days |
| 942 | `est_q_ndt_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net debt regarding the next quarter, made in past 3 months |
| 943 | `est_q_ndt_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net debt regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 944 | `est_q_ndt_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of net debt regarding the next quarter, compared to the last weekly update |
| 945 | `est_q_ndt_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of net debt regarding the next quarter, compared to last monthly update |
| 946 | `est_q_ndt_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of net debt regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 947 | `est_q_ner_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of net profit as reported regarding the next quarter |
| 948 | `est_q_ner_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of net profit as reported regarding the next quarter, made in the past 3 months |
| 949 | `est_q_ner_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of net profit as reported regarding the next quarter, made in the past 4 weeks |
| 950 | `est_q_ner_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of net profit as reported regarding the next quarter |
| 951 | `est_q_ner_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of net profit as reported regarding the next quarter, made in past 3 months |
| 952 | `est_q_ner_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of net profit as reported regarding the next quarter, made in the past 4 weeks |
| 953 | `est_q_ner_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 954 | `est_q_ner_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 955 | `est_q_ner_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of net profit as reported regarding the next quarter, where old and new estimates were made in the past  |
| 956 | `est_q_ner_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net profit as reported regarding the next quarter |
| 957 | `est_q_ner_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net profit as reported regarding the next quarter, made in the last 28 days |
| 958 | `est_q_ner_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net profit as reported regarding the next quarter, made in the past 3 months |
| 959 | `est_q_ner_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net profit as reported regarding the next quarter, made in the past 4 weeks |
| 960 | `est_q_ner_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of net profit as reported regarding the next quarter |
| 961 | `est_q_ner_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of net profit as reported regarding the next quarter, made in the past 3 months |
| 962 | `est_q_ner_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of net profit as reported regarding the next quarter, made in past 4 weeks |
| 963 | `est_q_ner_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net profit as reported regarding the next quarter |
| 964 | `est_q_ner_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net profit as reported regarding the next quarter, made in the last 28 days |
| 965 | `est_q_ner_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net profit as reported regarding the next quarter, made in the past 3 months |
| 966 | `est_q_ner_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net profit as reported regarding the next quarter, where old and new estimates were made in past 4 weeks |
| 967 | `est_q_ner_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of net profit as reported regarding the next quarter, compared to last weekly update |
| 968 | `est_q_ner_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of net profit as reported regarding the next quarter, compared to last monthly update |
| 969 | `est_q_ner_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of net profit as reported regarding the next quarter, where old and new estimates were made in past 4 wee |
| 970 | `est_q_ner_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of net profit as reported regarding the next quarter |
| 971 | `est_q_ner_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimates of net profit as reported regarding the next quarter, made in the last 28 days |
| 972 | `est_q_net_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of net income regarding the next quarter |
| 973 | `est_q_net_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of net income regarding the next quarter, made in the past 3 months |
| 974 | `est_q_net_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of net income regarding the next quarter, made in the past 4 weeks |
| 975 | `est_q_net_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of net income regarding the next quarter |
| 976 | `est_q_net_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of net income regarding the next quarter, made in the past 3 months |
| 977 | `est_q_net_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of net income regarding the next quarter, made in past 4 weeks |
| 978 | `est_q_net_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 979 | `est_q_net_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 980 | `est_q_net_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of net income regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 981 | `est_q_net_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net income regarding the next quarter |
| 982 | `est_q_net_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net income regarding the next quarter, made in the last 28 days |
| 983 | `est_q_net_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net income regarding the next quarter, made in past 3 months |
| 984 | `est_q_net_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of net income regarding the next quarter, made in the past 4 weeks |
| 985 | `est_q_net_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of net income regarding the next quarter |
| 986 | `est_q_net_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of net income regarding the next quarter, made in the past 3 months |
| 987 | `est_q_net_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of net income regarding the next quarter, made in past 4 weeks |
| 988 | `est_q_net_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net income regarding the next quarter |
| 989 | `est_q_net_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net income regarding the next quarter, made in the last 28 days |
| 990 | `est_q_net_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net income regarding the next quarter, made in past 3 months |
| 991 | `est_q_net_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of net income regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 992 | `est_q_net_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of net income regarding the next quarter, compared to the last weekly update |
| 993 | `est_q_net_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of net income regarding the next quarter, compared to the last monthly update |
| 994 | `est_q_net_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of net income regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 995 | `est_q_net_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimate of net income regarding the next quarter |
| 996 | `est_q_net_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of net income regarding the next quarter, made in the last 28 days |
| 997 | `est_q_net_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of net income regarding the next quarter, made in the past 4 weeks |
| 998 | `est_q_opr_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of operating profit regarding the next quarter |
| 999 | `est_q_opr_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of operating profit regarding the next quarter |
| 1000 | `est_q_opr_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 1001 | `est_q_opr_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 1002 | `est_q_opr_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of operating profit regarding the next quarter, where old and new estimates were made in the past 4 week |
| 1003 | `est_q_opr_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of operating profit regarding the next quarter |
| 1004 | `est_q_opr_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of operating profit regarding the next quarter, made in the last 28 days |
| 1005 | `est_q_opr_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of operating profit regarding the next quarter |
| 1006 | `est_q_opr_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of operating profit regarding the next quarter |
| 1007 | `est_q_opr_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimate of operating profit regarding the next quarter, made in the last 28 days |
| 1008 | `est_q_opr_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of operating profit regarding the next quarter, made in the past 3 months |
| 1009 | `est_q_opr_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of operating profit regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 1010 | `est_q_opr_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of operating profit regarding the next quarter, compared to the last weekly update |
| 1011 | `est_q_opr_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of operating profit regarding the next quarter, compared to last monthly update |
| 1012 | `est_q_opr_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of operating profit regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 1013 | `est_q_pre_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of pre-tax profit regarding the next quarter |
| 1014 | `est_q_pre_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of pre-tax profit regarding the next quarter, made in the past 3 months |
| 1015 | `est_q_pre_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of pre-tax profit regarding the next quarter, made in past 4 weeks |
| 1016 | `est_q_pre_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of pre-tax profit regarding the next quarter |
| 1017 | `est_q_pre_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of pre-tax profit regarding the next quarter, made in the past 3 months |
| 1018 | `est_q_pre_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of pre-tax profit regarding the next quarter, made in past 4 weeks |
| 1019 | `est_q_pre_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 1020 | `est_q_pre_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 1021 | `est_q_pre_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimate of pre-tax profit regarding the next quarter, where old and new estimates were made in past 4 weeks |
| 1022 | `est_q_pre_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of pre-tax profit regarding the next quarter |
| 1023 | `est_q_pre_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of pre-tax profit regarding the next quarter, made in the last 28 days |
| 1024 | `est_q_pre_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of pre-tax profit regarding the next quarter, made in the past 3 months |
| 1025 | `est_q_pre_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of pre-tax profit regarding the next quarter, made in the past 4 weeks |
| 1026 | `est_q_pre_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of pre-tax profit regarding the next quarter |
| 1027 | `est_q_pre_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of pre-tax profit regarding the next quarter, made in the past 3 months |
| 1028 | `est_q_pre_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of pre-tax profit regarding the next quarter, made in the past 4 weeks |
| 1029 | `est_q_pre_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of pre-tax profit regarding the next quarter |
| 1030 | `est_q_pre_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of pre-tax profit regarding the next quarter, made in the last 28 days |
| 1031 | `est_q_pre_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of pre-tax profit regarding the next quarter, made in past 3 months |
| 1032 | `est_q_pre_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of pre-tax profit regarding the next quarter, where old and new estimates were made in past 4 weeks |
| 1033 | `est_q_pre_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of pre-tax profit regarding the next quarter, compared to the last weekly update |
| 1034 | `est_q_pre_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimate of pre-tax profit regarding the next quarter, compared to last monthly update |
| 1035 | `est_q_pre_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of pre-tax profit regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 1036 | `est_q_pre_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of pre-tax profit regarding the next quarter |
| 1037 | `est_q_pre_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimates of pre-tax profit regarding the next quarter, made in the last 28 days |
| 1038 | `est_q_prr_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of pre-tax profit as reported regarding the next quarter |
| 1039 | `est_q_prr_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of pre-tax profit as reported regarding the next quarter, made in past 3 months |
| 1040 | `est_q_prr_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of pretax profit as reported regarding the next quarter, made in the past 4 weeks |
| 1041 | `est_q_prr_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of pretax profit as reported regarding the next quarter |
| 1042 | `est_q_prr_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of pretax profit as reported regarding the next quarter, made in past 3 months |
| 1043 | `est_q_prr_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of pretax profit as reported regarding the next quarter, made in the past 4 weeks |
| 1044 | `est_q_prr_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 1045 | `est_q_prr_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 1046 | `est_q_prr_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of pretax profit as reported regarding the next quarter, where old and new estimates were made in the pa |
| 1047 | `est_q_prr_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of pretax profit as reported regarding the next quarter |
| 1048 | `est_q_prr_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of pre-tax profit as reported regarding the next quarter, made in the last 28 days |
| 1049 | `est_q_prr_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of pretax profit as reported regarding the next quarter, made in the past 3 months |
| 1050 | `est_q_prr_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of pretax profit as reported regarding the next quarter, made in the past 4 weeks |
| 1051 | `est_q_prr_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of pretax profit as reported regarding the next quarter |
| 1052 | `est_q_prr_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of pretax profit as reported regarding the next quarter, made in the past 3 months |
| 1053 | `est_q_prr_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of pretax profit as reported regarding the next quarter, made in the past 4 weeks |
| 1054 | `est_q_prr_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of pretax profit as reported regarding the next quarter |
| 1055 | `est_q_prr_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of pretax profit as reported regarding the next quarter, made in the last 28 days |
| 1056 | `est_q_prr_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of pretax profit as reported regarding the next quarter, made in the past 3 months |
| 1057 | `est_q_prr_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of pretax profit as reported regarding the next quarter, where old and new estimates were made in the past 4 wee |
| 1058 | `est_q_prr_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimate of pretax profit as reported regarding the next quarter, compared to last weekly update |
| 1059 | `est_q_prr_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of pre-tax profit as reported regarding the next quarter, compared to the last monthly update |
| 1060 | `est_q_prr_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of pretax profit as reported regarding the next quarter, where old and new estimates were made in the pas |
| 1061 | `est_q_prr_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of pretax profit as reported regarding the next quarter |
| 1062 | `est_q_sal_high` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of sales/revenue regarding the next quarter |
| 1063 | `est_q_sal_high_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of sales/revenue regarding the next quarter, made in the past 3 months |
| 1064 | `est_q_sal_high_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of sales/revenue regarding the next quarter, made in past 4 weeks |
| 1065 | `est_q_sal_low` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of sales/revenue regarding the next quarter |
| 1066 | `est_q_sal_low_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of sales/revenue regarding the next quarter, made in the past 3 months |
| 1067 | `est_q_sal_low_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of sales/revenue regarding the next quarter, made in the past 4 weeks |
| 1068 | `est_q_sal_lowered_1wk` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 1069 | `est_q_sal_lowerednum_1mth` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 1070 | `est_q_sal_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst estimates of sales/revenue regarding the next quarter, where old and new estimates were made in past 4 weeks |
| 1071 | `est_q_sal_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of sales/revenue regarding the next quarter |
| 1072 | `est_q_sal_mean_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of sales/revenue regarding the next quarter, made in the last 28 days |
| 1073 | `est_q_sal_mean_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of sales/revenue regarding the next quarter, made in the past 3 months |
| 1074 | `est_q_sal_mean_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst estimate of sales/revenue regarding the next quarter, made in the past 4 weeks |
| 1075 | `est_q_sal_median` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of sales/revenue regarding the next quarter |
| 1076 | `est_q_sal_median_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of sales/revenue regarding the next quarter, made in the past 3 months |
| 1077 | `est_q_sal_median_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of sales/revenue regarding the next quarter, made in the past 4 weeks |
| 1078 | `est_q_sal_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of sales/revenue regarding the next quarter |
| 1079 | `est_q_sal_num_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of sales/revenue regarding the next quarter, made in the last 28 days |
| 1080 | `est_q_sal_num_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of sales/revenue regarding the next quarter, made in past 3 months |
| 1081 | `est_q_sal_num_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of sales/revenue regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 1082 | `est_q_sal_raised_1wk` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of sales/revenue regarding the next quarter, compared to the last weekly update |
| 1083 | `est_q_sal_raisednum_1mth` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of sales/revenue regarding the next quarter, compared to the last monthly update |
| 1084 | `est_q_sal_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst estimates of sales/revenue regarding the next quarter, where old and new estimates were made in the past 4 weeks |
| 1085 | `est_q_sal_std` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of sales/revenue regarding the next quarter |
| 1086 | `est_q_sal_std_28d` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of sales/revenue regarding the next quarter, made in the last 28 days |
| 1087 | `est_q_sal_std_3mth_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of sales/revenue regarding the next quarter, made in the past 3 months |
| 1088 | `est_q_sal_std_4wks_ago` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimate of sales/revenue regarding the next quarter, made in the past 4 weeks |
| 1089 | `growth` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Historical 5-year growth |
| 1090 | `high_52wks` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Highest price in the past 52 weeks |
| 1091 | `low_52wks` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Lowest price in the past 52 weeks |
| 1092 | `marketbeta` | MATRIX | 0.500 | 风险与质量 | 0 | — | — | — | UNUSABLE | Market beta |
| 1093 | `price` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Yesterday's price |
| 1094 | `price_26wks` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price 26 weeks ago |
| 1095 | `ptg_high` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Highest price target |
| 1096 | `ptg_low` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Lowest price target |
| 1097 | `ptg_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of price targets, where old and new estimates were made in the past 4 weeks |
| 1098 | `ptg_mean` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Mean price target |
| 1099 | `ptg_median` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Median price target |
| 1100 | `ptg_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates used for price target |
| 1101 | `ptg_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised price targets, where old and new estimates were made in past 4 weeks |
| 1102 | `ptg_std` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Standard deviation of the price target |
| 1103 | `rec_lowerednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of lowered analyst recommendations, where old and new estimates were made in the past 4 weeks |
| 1104 | `rec_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean estimate of the analyst recommendation |
| 1105 | `rec_num` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates of the analyst recommendation |
| 1106 | `rec_raisednum_4wks` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of raised analyst recommendations, where old and new estimates were made in the past 4 weeks |
| 1107 | `shares` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Number of shares outstanding |
| 1108 | `sp500` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | S&P 500 indicator |
| 1109 | `stability` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Historical 5-year stability |
| 1110 | `totalreturn` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Yesterday's return |
| 1111 | `volume_10wks` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Weekly median volume of the last 10 weeks (in millions/billions) |

## 六、本地回测证据

- 本地累计回测 **77** 条；其中 `ra_failed_checks` 为空的 **15** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `kqJZYdvk` | 2.27 | 1.61 | 1.61 | 1.13 | 0.05 | ["LOW_SUB_UN | eur_a7_ap | `group_neutralize(signed_power(group_zscore(divide(subtract(est_12m_ebt_mean_28d, est_12m_e` |
| `A1Q729Ll` | 2.23 | 1.60 | 1.82 | 1.27 | 0.05 | 0 | eur_a7_ap | `group_neutralize(signed_power(group_zscore(divide(subtract(est_12m_ebt_median, est_12m_ebt` |
| `58jk2xkX` | 2.18 | 1.80 | 1.39 | 1.20 | 0.05 | ["LOW_2Y_SHA | eur_a7_al | `group_neutralize(signed_power(group_zscore(divide(subtract(est_12m_pre_mean, est_12m_pre_m` |
| `e76xGOQO` | 2.15 | 1.59 | 1.93 | 1.12 | 0.05 | 0 | eur_a7_ae | `group_neutralize(signed_power(group_zscore(divide(subtract(est_12m_ebt_mean, est_12m_ebt_m` |
| `XgR8OGNX` | 2.07 | 1.31 | 1.54 | 1.30 | 0.06 | ["LOW_2Y_SHA | eur_a7_ap | `group_neutralize(signed_power(group_zscore(divide(subtract(est_12m_ebt_raisednum_1mth, est` |
| `npA8X3qE` | 2.05 | 1.31 | 1.53 | 1.17 | 0.04 | ["LOW_2Y_SHA | eur_a7_av | `group_neutralize(signed_power(group_zscore(ts_mean(divide(subtract(est_12m_ebi_raisednum_4` |
| `JjPv2bzW` | 2.04 | 1.30 | 1.52 | 1.18 | 0.04 | ["LOW_2Y_SHA | eur_a7_av | `group_neutralize(signed_power(group_zscore(ts_mean(divide(subtract(est_12m_ebi_raisednum_4` |
| `XgR8O1zx` | 2.04 | 1.30 | 1.43 | 1.26 | 0.05 | ["LOW_2Y_SHA | eur_a7_av | `group_neutralize(signed_power(group_zscore(divide(subtract(est_12m_ebi_raisednum_4wks, est` |
| `MP0L2Ogo` | 2.03 | 1.24 | 1.76 | 1.20 | 0.07 | 0 | eur_a7_ap | `group_neutralize(signed_power(group_zscore(divide(subtract(est_12m_ebt_raised_1wk, est_12m` |
| `qME6VPVP` | 2.01 | 1.39 | 1.10 | 1.03 | 0.05 | ["LOW_SUB_UN | eur_a7_aj | `group_neutralize(signed_power(group_zscore(divide(subtract(est_12m_sal_mean, est_12m_sal_m` |
| `JjPvrgrj` | 2.00 | 1.42 | 1.59 | 0.96 | 0.05 | ["LOW_SUB_UN | eur_a7_aj | `group_neutralize(signed_power(group_zscore(divide(subtract(est_12m_pre_mean, est_12m_pre_m` |
| `2rjNeaeZ` | 1.99 | 1.38 | 1.44 | 0.95 | 0.05 | ["LOW_SUB_UN | eur_a7_aj | `group_neutralize(signed_power(group_zscore(divide(subtract(est_12m_eps_mean, est_12m_eps_m` |
| `e76xWm3l` | 1.99 | 1.40 | 1.59 | 0.95 | 0.05 | ["LOW_SUB_UN | eur_a7_al | `group_neutralize(signed_power(group_zscore(divide(subtract(est_12m_pre_mean, est_12m_pre_m` |
| `1YjzKzp6` | 1.97 | 1.35 | 1.33 | 1.07 | 0.05 | ["LOW_2Y_SHA | eur_a7_ae | `group_neutralize(signed_power(group_zscore(divide(subtract(est_12m_eps_mean, est_12m_eps_m` |
| `Grge7PG0` | 1.94 | 1.40 | 1.60 | 0.97 | 0.05 | ["LOW_SUB_UN | eur_a7_al | `group_neutralize(signed_power(group_zscore(divide(subtract(est_12m_pre_mean, est_12m_pre_m` |

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

