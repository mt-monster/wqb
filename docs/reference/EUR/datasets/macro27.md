# macro27 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `macro27` |
| 名称 | Job records from job posting |
| 类别 | MACRO |
| 数据字段数(平台) | 33 |
| 覆盖率 | 0.3273 |
| 平台已有 alpha | 472 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.2 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Bloomberg Identifiers (BBID) and Reuters Instrument Codes (RIC), sourced from both Bloomberg and Refinitiv. It serves as a cross-reference tool for linking securities across two major financial data platforms, enabling seamless integration of market data, analytics, and research workflows. While not directly predictive of price movements, the dataset is essential for accurate data alignment, security identification, and multi-source analysis, which are foundational for quantitative research, portfolio management, and trading systems that rely on consistent and reliable security identifiers.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **33** |
| 类型分布 | VECTOR×33 |
| 平均覆盖率 | **0.327** |
| 覆盖率区间 | 0.15 ~ 0.43 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 33 | 100.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 33 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 33 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 其他 | 20 | 0.35 | avg_days_job_posting_active、avg_days_job_posting_closed、num_jobs_active |
| 宏观与行业 | 7 | 0.26 | mcr27_company_jobsactive_n、mcr27_normalizedflag、mcr27_verified_ds2 |
| 搜索与替代数据 | 3 | 0.31 | mcr27_verified_ds1、mcr27_unmapped_location、mcr27_companyidmap |
| 交易与微观结构 | 2 | 0.35 | mcr27_verified_ds3、mcr27_verified_ds4 |
| 元数据与非信号 | 1 | 0.34 | mcr27_zip |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `avg_days_job_posting_active` | VECTOR | 0.430 | 其他 | 0 | — | — | — | UNUSABLE | average length of time the job posts have been active |
| 2 | `avg_days_job_posting_closed` | VECTOR | 0.430 | 其他 | 0 | — | — | — | UNUSABLE | average length of time the deleted jobs were posted before removal |
| 3 | `num_jobs_active` | VECTOR | 0.430 | 其他 | 0 | — | — | — | UNUSABLE | Number of active job postings |
| 4 | `num_jobs_created` | VECTOR | 0.430 | 其他 | 0 | — | — | — | UNUSABLE | Number of job postings created |
| 5 | `num_jobs_removed` | VECTOR | 0.430 | 其他 | 0 | — | — | — | UNUSABLE | Number of job postings removed/deleted |
| 6 | `is_job_repost_flag` | VECTOR | 0.412 | 其他 | 0 | — | — | — | UNUSABLE | Indicator if the job is a repost (1) or original (0) |
| 7 | `continuous_value_break_flag` | VECTOR | 0.348 | 其他 | 0 | — | — | — | UNUSABLE | cvbbrksflag |
| 8 | `mcr27_bigdrpbrksflag` | VECTOR | 0.348 | 其他 | 0 | — | — | — | UNUSABLE | Binary flag indicating a “big drop” occurred since the previous scraping |
| 9 | `mcr27_company_ajnet` | VECTOR | 0.348 | 其他 | 0 | — | — | — | UNUSABLE | Net amount of active job postings added (net change in active jobs, e.g., created minus removed) |
| 10 | `mcr27_company_jobsactive` | VECTOR | 0.348 | 其他 | 0 | — | — | — | UNUSABLE | Number of currently active job postings for the company |
| 11 | `mcr27_company_jobsactive_n` | VECTOR | 0.348 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of active job postings after neutralization within the respective macro bucket |
| 12 | `mcr27_company_jobscreated` | VECTOR | 0.348 | 其他 | 0 | — | — | — | UNUSABLE | Number of job postings created for the company |
| 13 | `mcr27_company_jobsremoved` | VECTOR | 0.348 | 其他 | 0 | — | — | — | UNUSABLE | Number of job postings removed/deleted for the company |
| 14 | `mcr27_normalizedflag` | VECTOR | 0.348 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Binary flag indicating whether jobsactive was normalized within the respective macro bucket |
| 15 | `mcr27_postlength2` | VECTOR | 0.348 | 其他 | 0 | — | — | — | UNUSABLE | postlength2 |
| 16 | `mcr27_verified_ds1` | VECTOR | 0.348 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Binary flag indicating highest confidence that the company ID mapping is correct; 1 = verified, 0 = not |
| 17 | `mcr27_verified_ds2` | VECTOR | 0.348 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Binary flag indicating highest-confidence company ID mapping based on corporate action information |
| 18 | `mcr27_verified_ds3` | VECTOR | 0.348 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Binary flag indicating high confidence that the company ticker mapping is correct based on vendor information; 1 = verified, 0 = not |
| 19 | `mcr27_verified_ds4` | VECTOR | 0.348 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Binary flag indicating high confidence that the company ticker mapping is correct based on legal entity updates; 1 = verified, 0 = not |
| 20 | `mean_days_job_active` | VECTOR | 0.348 | 其他 | 0 | — | — | — | UNUSABLE | Average time job posts have been active, in days |
| 21 | `mean_days_job_closed` | VECTOR | 0.348 | 其他 | 0 | — | — | — | UNUSABLE | Average number of days the company’s removed jobs had been posted before deletion |
| 22 | `is_historically_hosted_job_flag` | VECTOR | 0.341 | 其他 | 0 | — | — | — | UNUSABLE | Historical indicator that the job was hosted by LinkUp (1=Yes, 0=No) |
| 23 | `is_hosted_job_flag` | VECTOR | 0.341 | 其他 | 0 | — | — | — | UNUSABLE | Boolean flag indicating if the job posting was hosted by LinkUp (1=yes, 0=no) |
| 24 | `is_sponsored_ad_flag` | VECTOR | 0.341 | 其他 | 0 | — | — | — | UNUSABLE | Binary flag indicating whether the job posting is part of a vendor-sponsored ad campaign (1=yes, 0=no) |
| 25 | `mcr27_country` | VECTOR | 0.341 | 宏观与行业 | 0 | — | — | — | UNUSABLE | country |
| 26 | `mcr27_unmapped_location` | VECTOR | 0.341 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Flag that the job’s location could not be identified by the vendor (1=Yes) |
| 27 | `mcr27_zip` | VECTOR | 0.341 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Postal/ZIP code for the job location |
| 28 | `mcr27_companyidmap` | VECTOR | 0.232 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | An integer mapped to the canonical company ID used in the dataset |
| 29 | `bucket_avg_days_job_active` | VECTOR | 0.148 | 其他 | 0 | — | — | — | UNUSABLE | Average time the jobs have been active (days) |
| 30 | `bucket_avg_days_job_closed` | VECTOR | 0.148 | 其他 | 0 | — | — | — | UNUSABLE | Average time the deleted/removed jobs were posted (days) |
| 31 | `mcr27_bucket_daily_jobsactive` | VECTOR | 0.148 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of active job postings in this macro bucket on this date |
| 32 | `mcr27_bucket_daily_jobscreated` | VECTOR | 0.148 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of job postings created in this macro bucket since the prior scrape |
| 33 | `mcr27_bucket_daily_jobsremoved` | VECTOR | 0.148 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of job postings removed/deleted in this macro bucket since the prior scrape |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

