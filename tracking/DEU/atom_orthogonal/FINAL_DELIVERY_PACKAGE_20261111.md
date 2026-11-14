# ★DEU D1 交付包（终局版，2026-11-11）

> 目标第 4 条要求的完整交付物：每颗 alpha 的**所属数据集 / 核心字段 / 算子逻辑 / 回测指标** + **字段画像存档索引**。
> 交付 11 颗 = 6 ACTIVE + 5 待授权；互相关全对 <0.7（最大对 zq3eb7No~RREPm361 = 0.6879，最大独立集 11，missing_pnl 0）；
> 逐年 2014-2023 零空窗（除 QPveY7Kg 2014-2018 前段空窗 → 已按口径除名）。

## 一、交付清单

### 已 ACTIVE（6 颗，已上线）

| # | alpha | 塔 | 数据集 | 核心字段 | 算子逻辑 | S | F | 2Y | TO | self | prod |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | vR1oxZA3 | — | 多源组合 | — | 多引擎混合（10 算子内） | **3.27** | 3.09 | 4.39 | 0.183 | 0.599 | 0.599 |
| 2 | zq3eb7No | ANALYST | analyst | est_12m_ebt_mean / est_12m_pre_mean | zscore(240) + Δ4wks 修正 | 2.01 | 1.28 | 1.64 | 0.226 | 0.364 | 0.617 |
| 3 | rKRx2Alj | MODEL+ANALYST | model + analyst | mean_estimate_change_pct_f12m_earnings_7d_4 + netprofit_y1_estimate_change_3mo | 双腿等权 rank 和 | 1.95 | 1.80 | 2.23 | 0.140 | 0.563 | 0.656 |
| 4 | GrW9OxmG | ANALYST | anl93 | anl93_recprofitabilityprev_estimator_profitability2 | 盈利预期水平标准化 | 1.62 | 1.56 | 1.93 | 0.046 | 0.266 | 0.664 |
| 5 | bl6AvMkN | MODEL+ANALYST | predictive_starmine + analyst_factor_signals | eps_y1_estimate_change_3mo + predicted_surprise_f12m_ebitda_4 | group_neutralize + bucket 分组 | 1.61 | 1.36 | 2.15 | 0.110 | 0.514 | 0.647 |
| 6 | 78Yk8VR1 | SHORTINTEREST | shortinterest3 | shrt3_bar | ts_target_tvr_decay(rank(Δ264)×rank(Δ132)) | 1.68 | 1.21 | 2.27 | 0.113 | 0.266 | — |

### 待授权（5 颗，七层验证全绿，待用户明确文字授权后 POST 提交）

| # | alpha | 塔 | 数据集 | 核心字段 | 算子逻辑 | S | F | 2Y | TO | self | prod |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|
| 7 | RREPm361 | ANALYST | analyst | est_12m_ebi_median / est_12m_ebt_mean / est_12m_ebt_mean_4wks_ago | group_rank(zscore240 + zscore44 修正和) | **2.02** | 1.25 | 1.82 | 0.251 | 0.3275 | **0.6881**（余量 0.012） |
| 8 | 9qlz29Oe | SHORT+NEWS | shortinterest3 + news20 | max_loan_rate_p5_d1 + nws20_multiple_comp_event_sentiment_score | 借券挤兑(Δ220) × 新闻情绪(Δ66+mean11) | 1.86 | 1.34 | 2.02 | 0.173 | 0.4552 | 0.47 |
| 9 | qM7KxkQV | SHORT+INSIDERS | shortinterest3 + insiders1 | shrt3_bar + insd1_holdings | 借券拥挤(Δ220) × 内部人持仓 52 周位置 | 1.72 | 1.34 | 2.43 | 0.143 | 0.5429 | 0.543 |
| 10 | Jj8VQwoe | SHORT+OTHER | shortinterest3 + other47 | shrt3_bar + oth47_organic_traffic | 借券拥挤 × 网站流量 ts_quantile | 1.65 | 1.24 | 2.42 | 0.147 | 0.5645 | 0.6124 |
| 11 | d5a2vxzY | SHORTINTEREST | shortinterest3 | max_loan_rate_p5_d1 + mean_loan_rate_p5_d1 | 最高利率(Δ220) × 平均利率(Δ132) | 1.60 | 1.08 | 2.05 | 0.180 | 0.6038 | 0.6039 |

### 换防选项（与 qM7KxkQV 同族互斥，取一）

| alpha | 数据集 | 核心字段 | 算子逻辑 | S | F | 2Y | TO | self | prod | 结论 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| **88NmN37X** | shortinterest3 + insiders1 | 同 qM7KxkQV（窗口变体） | 同族 | **1.79** | **1.53** | 2.37 | **0.091** | 0.5538 | **0.5541** | 指标全面优于 qM7KxkQV，替换即升级 |

## 一·B、★逐颗真实回测设置（平台 settings 实证，2026-11-12 补齐）

| alpha | universe | delay | decay | neutralization | truncation | nanHandling | unitHandling | pasteurization | S |
|---|---|---|---:|---|---|---|---|---|---:|
| RREPm361 | TOP500 | 1 | **0** | **FAST** | 0.08 | **OFF** | VERIFY | ON | 2.02 |
| 9qlz29Oe | TOP500 | 1 | 4 | SUBINDUSTRY | 0.08 | ON | VERIFY | ON | 1.86 |
| qM7KxkQV | TOP500 | 1 | 4 | SUBINDUSTRY | 0.08 | ON | VERIFY | ON | 1.72 |
| Jj8VQwoe | TOP500 | 1 | 4 | SUBINDUSTRY | 0.08 | ON | VERIFY | ON | 1.65 |
| d5a2vxzY | TOP500 | 1 | 4 | SUBINDUSTRY | 0.08 | ON | VERIFY | ON | 1.60 |
| 88NmN37X（换防） | TOP500 | 1 | **8** | SUBINDUSTRY | 0.08 | ON | VERIFY | ON | 1.79 |

**★关键发现**：**设置层是独立的一维杠杆**——同一表达式（RREPm361）在
「decay4/SUBINDUSTRY/nan ON」下只有 **S 0.51**，在平台记录的
「decay0/FAST/nan OFF」下是 **S 2.02**。
⇒ **nan_handling=ON 会把无数据股票填 0 → 事件型/缺失型字段产生巨大并列块 → 毁掉横截面排序**，
这与 BE51/57/71 三次独立实测同源（回填/掩码/门控造并列块）。
⇒ **后续波次必须做设置档扫描（nan ON/OFF × 中性化 SUBINDUSTRY/FAST/STATISTRIAL × decay 0/4/8）**，
不能固定用我们历史默认档。

## 二、字段画像存档索引

| 类别 | 路径 | 内容 |
|---|---|---|
| 全字段画像 | `tracking/DEU/atom_orthogonal/<dataset_id>_fields.csv` | 172 集 / 20,012 字段（id,type,cov,uc,ac,desc） |
| 画像索引 | `FIELD_PROFILE_INDEX.md` + `field_profile_index.json` | 按字段数 Top30 + 类型分布 + 机器可读索引 |
| 核心集画像 | `FIELD_PROFILE_CORE_DATASETS_20261111.md` | shortinterest3 / insiders1 / news20 / other47 / analyst 族逐字段画像 |
| 新增画像 | `FIELD_PROFILE_PATTERN_INSIDERAGG_20261111.md` | pattern_scores（285 GROUP 簇轴）/ insider_agg_matrix（34 字段四族） |
| 处置图谱 | `DATASET_DISPOSITION_MAP_20261111.md` | 每集处置结论 → 档案指针 |
| 塔级关闭清单 | `TOWER_CLOSURE_MASTER_20261111.md` | 12 未点亮塔逐塔天花板与封堵理由 |
| 占用图谱 | `OS_OCCUPANCY_MAP_20261111.md` | 20 颗 OS 的族签名（已占/仍开放） |
| 交付清单 | `FINAL_DELIVERY_REPORT_11ALPHAS_20261111.md` | 11 颗完整指标 + 九条可复用方法论 M1-M9 |

## 三、提交前提（本轮复核）

- OS 池 20 颗，最新 78Yk8VR1（2026-10-10）⇒ **池未漂移**；
- 5 颗待授权 self 全过：RREPm361 0.3275 / 9qlz29Oe 0.4552 / qM7KxkQV 0.5429 / Jj8VQwoe 0.5645 / d5a2vxzY 0.6038；
- prod 本轮 refresh=True 实测：0.543 / 0.6124 / 0.6039 / 0.47（4 颗）+ 0.6881（RREPm361，11-10 实测）；
- submit_verdict 提交层：6 颗全部 failed_ra=0 / failed_ppa=0 / sim_fails=[]（UNVERIFIABLE_404 为平台恒返 404 的正常态）；
- 篮子互相关：现篮与换防版均 all_below=true / 超阈对 0 / 最大独立集 11。
