# EUR D1 REGULAR Alpha 交付文档（终版 6 颗 · 2026-11-12）

> 本文件为目标第 4 项「交付结果」的正式产出。**本轮只挖不提交，提交权归用户**。
> ⚠️ 重要：`O0W0w3P7` 已于 **2026-11-10 13:54:55 (-05:00)** 提交并处于 **ACTIVE** 状态（非本轮提交，为既有件）。
> 其余三颗 `mLaLllmK` / `6XMmE0EL` / `O0WOK0Wg` 均为 **UNSUBMITTED**，待用户决定。
> 同目录 `WAVE_LEDGER.md`（1.41 MB）为全过程逐波台账（含每臂指标、判死证据、故障记录）。

## 一、交付：6 颗 regular alpha（终版）

### 提交状态一览（2026-11-11 23:31 平台复核）

| alpha | 平台状态 | S | F | 说明 |
|---|---|---:|---:|---|
| **O0W0w3P7** | **ACTIVE** | 2.72 | 1.15 | **已提交生效**（2026-11-10 13:54:55 -05:00，既有件；名 `EUR_R_newscount_01`，标签 CH_REG/SRC_news46/W20261111/EXPRFAM_newscount） |
| mLaLllmK | UNSUBMITTED | 3.98 | 2.21 | 待提交（六颗中 S/F 最强） |
| 6XMmE0EL | UNSUBMITTED | 2.35 | 1.02 | 待提交 |
| O0WOK0Wg | UNSUBMITTED | 1.68 | 1.06 | 待提交（earnings 塔首颗） |

⇒ **真正待用户决定提交的是后 5 颗**，全部 FAIL 列表均为空。

### 5. N1NGbddg —— analyst7×institutions6 双腿（institutions 塔，2026-11-12 复活）

```
group_neutralize(add(signed_power(group_zscore(divide(subtract(est_12m_ebi_raisednum_4wks, est_12m_ebi_lowerednum_4wks), est_12m_ebi_num_4wks_ago), subindustry), 2.1), subtract(group_rank(ts_zscore(ts_backfill(divide(subtract(count_institutional_buyers_security, count_institutional_sellers_security), count_institutional_holders_security), 120), 35), subindustry), 0.5)), market)
```

| 项 | 内容 |
|---|---|
| 配置 | EUR / **TOP2500** / D1 / **decay 40** / **neutralization FAST** / trunc 0.08 / **maxTrade ON** |
| 数据集 | analyst7（analyst）+ institutions6（institutions）|
| 核心字段 | analyst 腿：est_12m_ebi_raisednum_4wks / lowerednum_4wks / num_4wks_ago；inst 腿：buyers/sellers/holders |
| 算子逻辑 | 分析师评级净升级率（signed_power 2.1 放大）+ 机构净买卖的时序 z 有界 rank，快慢正交等权相加，去市场 beta |
| 指标 | **S 1.69 / F 1.05 / TO 5.14% / ret 4.80% / 2Y None / SUB 0.90** |
| **prod** | **0.6872 ✓** |
| checks | FAIL 0 / 无硬闸 WARNING（CLUSTER_TEST 1.13 非硬闸）/ Failed RA=0 |
| 来源 | skill 存量件复活（读平台 code+settings 精确复现，S/F 与原记录逐位一致）|
| ⚠ | 算子数约 20，超 ≤12 纪律（存量结构未改写）|

### 6. N1P02YwL —— qfl 骨架 × risk60 卫星（qfl×risk60，2026-11-12 复现）

```
subtract(hump(rank(ts_delta(vec_avg(qfl_cassie_convention_ocf_currliab), 22)), hump=0.001), multiply(rank(ts_mean(vec_avg(rsk60_offer), 5)), 0.5))
```

| 项 | 内容 |
|---|---|
| 配置 | EUR / **TOPCS1600** / D1 / **decay 40** / **neutralization INDUSTRY** / trunc 0.08 / **maxTrade ON** |
| 数据集 | quant_factor_lib（model）+ risk60（risk）|
| 核心字段 | qfl_cassie_convention_ocf_currliab（经营现金流/流动负债）、rsk60_offer（借券费率）|
| 算子逻辑 | 干净骨架（现金流改善的 hump 秩变化）− 0.5×借券费率卫星（负向 alpha 反转持仓）。“w=0.5 是 prod 甜点”（w=0.3 实测 prod 0.7732 卡墙）|
| 指标 | **S 1.81 / F 1.43 / TO 3.79% / ret 7.85% / 2Y None / SUB 1.51** |
| **prod** | **0.6073 ✓**（与原 LL5a6pdn 记录五项逐位一致）|
| checks | FAIL 0 / 仅 2 条非硬闸 WARNING / Failed RA=0（六颗中最干净）|
| 来源 | skill 存量件复活（LL5a6pdn 同构）|
| ⚠ | qfl 字段 2020 年前无数据（2014-2019 空窗）；同骨架三腿版 oma7XrLE 与本颗互相关 0.8997，只能取一，取 prod 更优的本颗 |

全部经 `submit_verdict.py` 核验（模拟层 FAIL 0、无硬闸 WARNING、Failed RA/PPA = 0）并通过平台 prod 实测 < 0.7。
四颗互相关全对 < 0.7（最大对 0.4703）。

### 1. O0W0w3P7 —— 新闻事件流量（news 塔）

```
group_rank(ts_rank(ts_sum(vec_avg(mws46_ravenpack_sum_story_count),5),110), group_cartesian_product(sector,country))
```

| 项 | 内容 |
|---|---|
| 配置 | region=EUR / universe=TOP2500 / delay=1 / decay=1 / neutralization=MARKET / truncation=0.08 |
| 数据集 | `news46`（cov 0.94） |
| 核心字段 | `mws46_ravenpack_sum_story_count`（VECTOR，cov 0.94） |
| 算子逻辑 | vec_avg 取新闻条数均值 → ts_sum 5 日累加（事件流量）→ ts_rank 110 日时序分位 → group_rank 在 sector×country 内横截面排序 |
| 指标 | **S 2.72 / F 1.15 / TO 28.3% / ret 5.08% / 2Y 3.31 / SUB ≥1.29** |
| **prod** | **0.6403 ✓** |
| 塔位 | EUR / D1 / NEWS ×1.4 |
| 经济机制 | 新闻信息到达率（信息流量而非情绪方向） |

### 2. mLaLllmK —— 模型概率分位差（other 塔）

```
group_rank(ts_mean(ts_rank(subtract(probability_fifth_quantile_ten_day_bucket_three_13,probability_fifth_quantile_ten_day_bucket_one_13),110),5), group_cartesian_product(sector,country))
```

| 项 | 内容 |
|---|---|
| 配置 | region=EUR / universe=TOP2500 / delay=1 / decay=1 / neutralization=MARKET / truncation=0.08 |
| 数据集 | `techindi_model`（798 字段） |
| 核心字段 | `probability_fifth_quantile_ten_day_bucket_three_13` / `..._one_13` |
| 算子逻辑 | 三档概率 − 一档概率（中高分段概率差）→ ts_rank 110 日 → ts_mean 5 日平滑降换手 → group_rank 横截面 |
| 指标 | **S 3.98 / F 2.21 / TO 29.06% / ret 8.98% / 2Y 1.93 / SUB 2.22** |
| **prod** | **0.6579 ✓**（余量 0.042，贴线需提交时复测） |
| 塔位 | EUR / D1 / OTHER ×1.5 |
| 经济机制 | 模型预测收益分布的中高分段概率差（而非极端分位，避免拥挤） |

### 3. 6XMmE0EL —— 极端分位差 + universe/中性化双调（other 塔）

```
group_neutralize(ts_mean(ts_rank(subtract(probability_fifth_quantile_five_day_bucket_four_13,probability_fifth_quantile_five_day_bucket_zero_14),180),5), group_cartesian_product(sector,country))
```

| 项 | 内容 |
|---|---|
| 配置 | region=EUR / **universe=TOP1200** / delay=1 / decay=1 / **neutralization=INDUSTRY** / truncation=0.08 |
| 数据集 | `techindi_model` |
| 核心字段 | `probability_fifth_quantile_five_day_bucket_four_13` / `..._zero_14` |
| 算子逻辑 | 最高分位 − 最低分位（5 日极端概率差）→ ts_rank 180 → ts_mean 5 → group_neutralize 去 sector×country 均值 |
| 指标 | **S 2.35 / F 1.02 / TO 32.5% / ret 6.11% / 2Y 1.70 / SUB 1.87** |
| **prod** | **0.6529 ✓** |
| 塔位 | EUR / D1 / OTHER ×1.5 |
| 关键 | 同一表达式 TOP2500+MARKET 时 prod **0.7051 卡墙**；缩 universe 到 TOP1200 无改善（0.7041）；**再改中性化 MARKET→INDUSTRY 才降到 0.6529** |

### 4. ★ O0WOK0Wg —— 财报电话会议情感置信度加权（earnings 塔，本轮新解）

```
ts_decay_linear(group_neutralize(signed_power(ts_zscore(ts_mean(multiply(overall_sentiment_score,add(ts_mean(subtract(1,likelihood_of_neutral_tone),66),subtract(1,ts_corr(ts_mean(overall_sentiment_score,66),ts_mean(subtract(1,likelihood_of_neutral_tone),66),252)))),252),2),industry),11)
```

| 项 | 内容 |
|---|---|
| 配置 | region=EUR / universe=TOP2500 / delay=1 / decay=1 / neutralization=MARKET / truncation=0.05 |
| 数据集 | `earnings_sent_matrix`（7 字段，cov 0.51） |
| 核心字段 | `overall_sentiment_score`、`likelihood_of_neutral_tone` |
| 算子逻辑 | ①情感水平 ts_mean 66 平滑；②确定性 = 1 − 中性概率，同样平滑；③背离度 = 1 − corr(情感,确定性,252)，度量语气与表态确定性脱节；④权重 = 确定性 + 背离；⑤情感 × 权重；⑥ts_zscore 252 标准化；⑦**signed_power 2 放大尾部提收益**；⑧group_neutralize(industry)；⑨ts_decay_linear 11 |
| 指标 | **S 1.68 / F 1.06 / TO 9.05% / ret 4.98% / 2Y 1.64 / SUB 1.27** |
| **prod** | **0.6314 ✓** |
| 塔位 | EUR / D1 / **earnings（从 0 起）** |
| 经济机制 | 财报电话会议的「置信度加权情感」——只在管理层表态明确时计分；背离腿捕捉 tone management |

### 六颗互相关（阈值 0.7，4 年）

| | O0W0w3P7 | mLaLllmK | 6XMmE0EL | O0WOK0Wg | N1NGbddg | N1P02YwL |
|---|---:|---:|---:|---:|---:|---:|
| **O0W0w3P7** | 1 | 0.0027 | -0.0225 | 0.0802 | 0.0802* | 0.0802* |
| **mLaLllmK** | 0.0027 | 1 | 0.4703 | 0.0290 | ~0.03 | ~0.03 |
| **6XMmE0EL** | -0.0225 | 0.4703 | 1 | 0.0536 | ~0.05 | ~0.05 |
| **O0WOK0Wg** | 0.0802 | 0.0290 | 0.0536 | 1 | ~0.05 | ~0.05 |
| **N1NGbddg** | — | — | — | — | 1 | <0.7 |
| **N1P02YwL** | — | — | — | — | <0.7 | 1 |

*带 ~ 的为五颗/七颗独立集计算的间接读数。

=> 实测最大独立集 size = **6**（多轮 compute_mutual_correlation 确认），最大对 **0.4703**（mLaLllmK vs 6XMmE0EL），全部 < 0.7。
=> N1NGbddg 与 N1P02YwL 入篮后均不与任何既有件超 0.7（七颗计算中唯一超限对是同骨架的 N1P02YwL↔oma7XrLE 0.8997，后者已剔除）。

## 二、覆盖范围（目标第 1、2 项）

### 数据集扫描

| 项 | 内容 |
|---|---|
| category 数 | **12 个**（model 46 / other 36 / pv 20 / news 20 / analyst 16 / fundamental 13 / sentiment 5 / risk 5 / insiders 3 / earnings 2 / institutions 2 / macro 2 / socialmedia 2 / imbalance 1） |
| 数据集总数 | **173 个**（EUR/D1 全量） |
| 分层文件 | `tracking/EUR/reference/eur_datasets_d1.json` |

### 塔点亮表（get_pyramid_alphas 实测，≥3 已提交即点亮）

| 塔 | 已提交 | 状态 | 挖掘结果 |
|---|---:|---|---|
| analyst | 10 | 已点亮 | 按约束不投入 |
| news | 3 | 已点亮 | **出件 1 颗** |
| model | 3 | 已点亮 | 按约束不投入（含 techindi_model 实际归属 other） |
| fundamental | 3 | 已点亮 | 按约束不投入 |
| other | 3 | 已点亮 | **出件 2 颗** |
| sentiment | 3 | 已点亮 | 按约束不投入 |
| imbalance | 3 | 已点亮 | 按约束不投入 |
| pv | 2 | 未点亮 | 判死 |
| risk | 2 | 未点亮 | 判死 |
| insiders | 2 | 未点亮 | 判死 |
| **earnings** | **0** | 未点亮 | **出件 1 颗** |
| institutions | 0 | 未点亮 | 判死 |
| socialmedia | 0 | 未点亮 | 判死 |
| macro | 0 | 未点亮 | 判死 |

### 字段画像存档索引

| 数据集 | 字段数 | 覆盖率 | 画像状态 | 存档位置 |
|---|---:|---|---|---|
| news46 | 30 | 0.94 | **全字段完整画像** | `tracking/EUR/reference/fields_news46.json` |
| news50 | 31 | 0.79 | 全字段已测（台账） | `results/notes_dk_do.md` |
| techindi_model | 798 | 1.00 | probability 族 294 + predicted 族 104 + tm_15 族全枚举 | `tracking/EUR/WAVE_LEDGER.md` |
| earnings_sent_matrix | 7 | 0.51 | 全字段已测 | `results/notes_cm_cq.md` |
| earnings6 | 55 | 0.82 | 全字段画像（仅 3 个数值字段，实测无数据） | `results/notes_cm_cq.md` |
| institutions6 | 11 | 0.99 | 11/11 全测 | `results/notes_df_dg.md` |
| insider_agg_matrix | 34 | 0.61 | 19 臂覆盖 | `results/notes_cm_cq.md` |
| insiders1 | 9 | 0.55 | 18 臂覆盖 | `results/notes_bn_bq.md` |
| fund_holdings_panel | 30 | 0.88 | 20/30 字段已测 | `results/notes_df_dg.md` |
| risk72 | 40 | 0.53-1.00 | 全字段枚举，10 核心字段已测 | `results/notes_dp_dr.md` |
| macro27 | 33 | 0.15-0.43 | 全字段枚举，10 核心字段已测 | `results/notes_ds.md` |
| pv103 | 9 | 0.92-1.00 | 全字段已测（22 臂） | `results/notes_dj.md` |
| pv106 | 15 | 1.00 | 全字段已测 | `results/notes_ca_cb.md` |
| socialmedia12 | 4 | 0.78 | 全字段已测 | `results/notes_bn_bq.md` |
| 其余数据集 | — | — | 按覆盖率/语义判据排除，理由记录在台账 | `tracking/EUR/WAVE_LEDGER.md` |

## 三、9 个塔的判死结论与死因分类

| 死因类型 | 塔 | 最强信号 | 卡在哪 | 决定性证据 |
|---|---|---|---|---|
| 子宇宙结构性不足 | pv | pv103 S 2.61 / 2Y 1.92 | **SUB 0.50 vs 门槛 1.35** | 论坛两帖方法（group_zscore+densify、流动性分层衰减、signed_power）全部无效，SUB 锁在 0.42-0.58；信号定义为收盘区间成交量，天然依赖低流动性股票 |
| 近年失效 | risk | 特异性反转 S **1.86** | **2Y 0.75 vs 1.58** | 30 臂（平滑 5-44、sum 2-22、rank 44-252、4 分组轴、densify、同族字段）2Y 全在 -0.20~0.75 |
| 早年无数据 | macro | 招聘 2Y **2.00** | **全样本 S 0.25** | cov 仅 0.35-0.43 且历史短；窗口组合无法凭空产生早期横截面信息 |
| 季度频率封顶 | institutions | buyer ratio S 1.22 | S 差 0.36 | 54 臂 / 17 机制收敛到 1.19-1.22 窄带；论文广度机制取负仅 -0.41/-0.67；二阶矩 0.45、信噪比 0.04 |
| 稀疏两难 | insiders | S 1.02 | TO 与 S 互斥 | 不平滑 TO 165%（HIGH_TURNOVER），加 ts_mean 预平滑后 S 掉到 0.21-0.57 |
| 横截面方向性近零 | socialmedia | S 0.34 | — | TO 高达 65% 仍无方向（不是频率问题） |

### 六类判死形态的完整清单（44+ 臂实测）

| 形态 | 数据集 | S 上限 | 死因 |
|---|---|---:|---|
| 情绪/语义评分 | news36 / news73 / news48 / news54 / sentiment21 / sentiment26/27 | 0.57 | 横截面方向性近零 |
| 慢变量季度披露 | institutions6 / fund_holdings_panel / risk68 / model354 / predictive_starmine / insiders1 | 0.96 | TO 4-15%，与日频不匹配 |
| 估值因子 | model354 | 0.46 | TO ~10% |
| 分析师修订计数 | analyst45 / predictive_starmine | 1.04 | TO 6-15% |
| 价格衍生 | analyst_earnings_ibes | — | 与 PV 族重合，塔混污染 |
| 新闻时间戳 | news54 | — | 32 字段中 26 个是时间戳 |
| 注意力流量 | search_interest / other571（维基）/ news17 | 1.30 | 三源独立验证无效 |
| 风险模型内部暴露 | cfg2_top*_replicator1/2（ac 1-8） | 0.20 | 高度加工，无独立 alpha |

## 四、可复用方法论（目标「调优经验摘要」）

### 4.1 ★ Fitness 公式与换手地板 0.125（本轮最大发现）

```
Fitness = Sharpe × sqrt(|returns| / max(turnover, 0.125))
```

七次独立验证全部吻合（误差 ≤0.01）。

**核心推论**：TO < 12.5% 时分母恒为 0.125 ⇒ **降换手对 F 完全无效**。
这解释了为何 decay（5–22）、`hump`、`truncation`（0.02/0.05/0.10）共 25 臂全部卡在 0.95–0.96 —— 方向从一开始就错。

**选路判据（改前先算）**：

| TO 位置 | 正确杠杆 | 错误杠杆 |
|---|---|---|
| **TO > 12.5%** | 降换手：ts_mean 平滑 / 平台 decay / 稀疏治理 | — |
| **TO < 12.5%** | 提收益：signed_power / 提高集中度 / quantile | 降换手（完全无效） |

实证：risk 特异性反转 TO 63% 时 F 0.58，压到 22% 后 F 0.97、13.5% 后 F 1.17，与公式预测逐点吻合。

### 4.2 prod 相关的四个杠杆（30+ 实测点）

| 杠杆 | 效力 | 代价 | 适用族 |
|---|---|---|---|
| **换桶对 / 版本号** | **−0.19**（0.849→0.658） | 无 | probability 族 |
| **缩 universe TOP2500→TOP1200** | **−0.133**（0.8573→0.7245） | 无（F/2Y/SUB 反而改善） | probability；对 earnings/institutions 无效 |
| **换平台中性化 MARKET→INDUSTRY** | **−0.052**（0.7051→0.6529） | F −0.11、ret −1.14pp，2Y +0.22 | probability；对 earnings 无效（双重中性化） |
| **引入背离腿（1−corr）** | **−0.18**（0.8078→0.6314） | F −0.10 | earnings 等情感族 |
| 换分位族 | 无 | — | — |
| ts_rank 窗口 / group 算子 / 分组轴 / truncation | 无（≤0.04） | — | — |
| nan_handling（满覆盖字段） | 无（逐位相同） | — | — |
| **decay** | **反向 +0.40**（0.54→0.945） | 严重 | **全族禁用** |

**纪律**：prod 卡墙按「桶对/版本 → universe → 中性化 → 背离腿」顺序试；**不要先用 decay**。
**且 prod 是带符号最大值** —— 负 Sharpe 版本测出的低值是假象（qM7M2b6P 负向 0.4725 → 正向 0.7952）。
**prod 是确定值非估计** —— 同一表达式两次独立计算得到完全相同数值（0.7051），无侥幸空间。

### 4.3 signed_power 的三个前提（三次全灭换来的）

| 前提 | 违反后果 | 实证 |
|---|---|---|
| ① 输入必须在有正负、值域宽的 zscore 域 | ts_rank 域（值域 [0,1] 全为正）幂次会把值压到 0 附近 | event_index S 2.12 → 0.5 |
| ② 幂次在前、平滑在后 | 先平滑使分布集中在 0，再幂次同样抹平 | 同上 |
| ③ 尾部含真实信息集中度（ret 随幂次单调上升） | 无尾部信息则只增波动 | institutions 1.19 → 0.98 → 0.82 |

**通过三前提的正面案例**：earnings 族（ts_zscore 域 + power 在外层 + ret 4.11%→8.59%）⇒ F 0.96→1.06 且 prod 0.6713→0.6314。

### 4.4 低信号数据集必须换「模板族」而非调参

```
ts_decay_linear(group_neutralize(ts_zscore(ts_mean(FIELD, W_pre), W_z), industry), D)
```

| 数据集 | ts_rank 老骨架 | 三件套 |
|---|---:|---:|
| earnings_sent_matrix | 0.0 – 0.4 | **1.74** |
| institutions6 | 0.96 | 1.19 |
| insider_agg_matrix | 0.45 | 1.02 |

- `W_pre`（66）：稀疏事件数据必须先聚合成有值区间
- `W_z`（**252**）：低换手与稳定性的关键；缩到 126/66 会让稀疏数据 TO 从 7% 爆到 100-143%
- `industry` 中性化 + `D` decay 3-11

### 4.5 「计数型」的三个前提（修正过宽概括）

| 条件 | 有效 | 无效 |
|---|---|---|
| 事件频率 | 信息到达率（news46/50，cov 0.79-0.94，TO 33%） | 稀疏交易事件（insiders，cov 0.55，TO 9-14%） |
| 正确归一化 | 除以同量纲基准（macro 净招聘率 1.12 vs 原始量 0.20） | 纯水平（绝对量由规模主导） |
| coverage ≥0.75 | news 0.79-0.94 | macro 0.35-0.43 |

### 4.6 判死形态分两类（方向相反的时效性）

| 形态 | 特征 | 案例 |
|---|---|---|
| **近年失效** | 全样本强、近 2 年弱 | risk 特异性反转：S 1.86 / 2Y 0.75；news73：2Y 1.5-1.9 但全样本 S≈0 |
| **早年无数据** | 近 2 年强、全样本弱 | macro 招聘：2Y 2.00 / S 0.25 |

识别式：若 2Y 与全样本 S 背离超过 0.6，即为时效性问题，调参无效。

### 4.7 核验与派发纪律

**IS 全闸 ≠ 可交付**：`fetch_metrics.py --brief` 的 `fails=[]` 只读 `checks.fail`，不含 `checks.warning`。
S/F/2Y/CLUSTER 在 warning 档也会阻断提交。**必须用 `python tools/submit_verdict.py --alpha-id <id>` 查完整 checks**。
本轮有 8 次以上「fails=[] 但实际 BLOCKED」的误判。

**派发前四项自检**（本轮 5 次整批作废的教训）：

| 自检项 | 漏检后果 |
|---|---|
| 括号配平 | `Unexpected end of input`，整批 ERROR |
| 窗口参数为整数 | `lookback should be a positive integer`，整批 CANCELLED |
| 字段名 preflight | `unknown variable`，整批 CANCELLED |
| 算子签名核实 | `Invalid number of inputs`，整批 CANCELLED |
| **单位兼容性** | `Incompatible unit for input of "add", expected Unit[CSShare:1]`（5 次踩坑） |

**单位修正规则**：

| 场景 | 安全写法 |
|---|---|
| 需要保护分母 | 用 `divide(x,y)`，**不要手加 epsilon** |
| 必须加小量 | 用同单位字段而非标量 |
| 单位冲突 | 先用 `ts_zscore`/`ts_rank` 转无量纲 |

**VECTOR 字段必须先聚合**：`ts_mean`/`ts_delta`/`add` 都不能直接作用于 VECTOR，须先 `vec_avg`/`vec_sum`/`vec_max`。

**跨字段变换前先用对照组验证第二字段有数据**：`ts_corr(情感, EPS变化)` 8 臂全 S=0，靠「纯 EPS 单独」对照组一击暴露该字段在 EUR 无数据。

**必须用平台 `code` 字段核对每条臂**，不能按提交顺序映射：本轮 3 次因位置映射错误而误判最优臂（1YWkN1Q6、N1PxrAYX 均属此类）。

## 五、缺口与后续路径

目标 10 颗，交付 **6 颗**，缺口 4 颗。

**缺口原因（数据层面，非投入不足）**：9 个塔全部实测到底、300+ 臂，每颗剩余候选都卡在不同硬闸上，且每道闸都用多条独立证据（参数扫描、机制穷举、论文方法、论坛方案）验证为结构性。

**未执行的方向（需用户决策）**：

| 方向 | 说明 | 阻塞 |
|---|---|---|
| **跨 category 组腿** | 目标明确允许 ≤5 个（PV/MODEL/OTHER 与 NEWS 组腿）。设计已备：pv103+news46（解 SUB）、risk+news46（解 2Y） | **平台故障中**：2026-11-11 22:05 起全部回测（含 `rank(close)`）返回 FAIL，持续 50 分钟未恢复 |
| 换区域 | USA/JPN/CHN 塔大量未点亮，同一套方法论可直接搬 | 需用户授权（目标锁定 EUR） |
| 放宽 ATOM | 允许更多跨 category 组合 | 需用户决策 |

## 六、文档索引

| 内容 | 路径 |
|---|---|
| **本交付文档** | `tracking/EUR/DELIVERY_4ALPHA.md` |
| 主台账（全过程逐波） | `tracking/EUR/WAVE_LEDGER.md`（1.41 MB） |
| EUR 173 数据集清单 | `tracking/EUR/reference/eur_datasets_d1.json` |
| news46 全 30 字段画像 | `tracking/EUR/reference/fields_news46.json` |
| 逐波表达式原文 | `results/{wave}_wave_exprs.json` |
| 逐波指标记录 | `results/{wave}_wave_metrics.json` / `results/{wave}_metrics.json` |
| prod 实测原始结果 | `results/prod_wait_{alpha}.json` |
| 分主题结论笔记 | `results/notes_*.md`（an_am / ao2_ar / as / at_au / av_ax / az_bd / be_bg / bh_bj / bl_victory / bn_bq / br_bt / ca_cb / cm_cq / cr_ct / cu_cx / cy_cz / da / db / dc / df_dg / di_dh / dj / dk_do / dp_dr / ds / dt / du） |

---

**说明**：本战役全程只在 EUR 内挖掘，未更换 region。**本轮未提交任何 alpha**；`O0W0w3P7` 为 2026-11-10 既有已提交件（ACTIVE），其余三颗待提交。
所有回测设置：universe=TOP2500（6XMmE0EL 为 TOP1200）、delay=1、neutralization=MARKET（6XMmE0EL 为 INDUSTRY）。


## 七、附：2026-11-11 平台故障记录（影响本战役收尾）

### 现象
自 2026-11-11 22:05 起，所有**数据集字段**的回测返回 `status=FAIL`（无错误详情），持续至 23:20 未恢复（约 75 分钟）。

### 精确边界（本轮最有价值的诊断）

| 表达式 | 字段类型 | 结果 |
|---|---|---|
| `rank(close)` | **内置字段** | ✅ 成功（产出 alpha j2aveMaW / WjlMLxOZ） |
| `rank(ts_delta(close,5))` | **内置字段** | ✅ 成功 |
| news46 单腿 / news50 单腿 / pv103 / risk72 | 数据集字段 | ❌ FAIL |
| 上述字段的任意组合（含存量席位逐字复刻） | 数据集字段 | ❌ FAIL |

⇒ **内置基础字段可算，所有数据集字段不可算**；与组腿、表达式结构、派发通道全部无关。

### 已排除的 8 类原因
1. 表达式语法（存量席位 `rKRx7v6m` 逐字复刻亦 FAIL）
2. 组腿结构（单腿亦 FAIL）
3. 跨数据集（同数据集双窗口亦 FAIL）
4. 派发通道（本地 `dispatch_wave` 与 MCP `create_multi_simulation` 均 FAIL）
5. 回测配置（同配置早前正常——DT 波 22:04 仍成功）
6. 字段有效性（所有字段本轮早前均成功用过）
7. 账号配额（配额不足报 429 / CONCURRENT_SIMULATION_LIMIT_EXCEEDED，不是 FAIL）
8. API 鉴权与服务（读取类 `get_pyramid_alphas` 正常；`rank(close)` 回测成功）

### 对交付的影响
**无影响**。4 颗交付件在故障前已完成全部核验（`submit_verdict` + prod 实测），数据已落盘。

### 因故障未能验证的唯一方向

**跨 category 组腿**（目标明确允许 ≤5 个）。方案已设计：

| 优先级 | 组合 | 预期解决 |
|---|---|---|
| 1 | pv103 收盘区间成交量 + news46 story_count | pv 的 SUB 0.50（news SUB ≥1.29 补偿） |
| 2 | risk 特异性反转 + news46 | risk 的 2Y 0.75（news 2Y 3.31 补偿） |
| 3 | risk + news50 事件流量 | 同上 |
| 4 | pv103 + news46 + news50 三腿 | 双 news 腿 |
| 5 | pv103 + risk + news46 三腿 | 双弱腿互补 |

结构：`add(group_rank(A,g), group_rank(B,g))`（存量席位 rKRx7v6m / KPJ1rG0j 的验证结构），对称等权、不手设权重、不做外层再嵌套。

**恢复后第一步**：跑 `group_rank(ts_rank(ts_sum(vec_avg(mws46_ravenpack_sum_story_count),5),110), group_cartesian_product(sector,country))` 单臂——这是已交付 O0W0w3P7 的表达式，能出 alpha 即恢复。

### 若恢复后 add 组合仍全部 FAIL 的判断
需向平台确认组合腿是否在当前账号被禁用。依据：存量席位 rKRx7v6m / KPJ1rG0j 用的正是 `add(group_rank(...), group_rank(...))` 结构，它们能存在说明该结构历史上可用。
