# GBR 未点亮塔 数据集与字段画像（2026-10-31）

> 区域口径：GBR / TOP700 / delay=1 / decay=15 / neutralization=FAST / truncation=0.05 /
> nanHandling=ON / maxTrade=OFF / pasteurization=ON。
> 所有 coverage / alphaCount / userCount 均为 `get_datasets` / `get_datafields`
> 在 **GBR·TOP700·D1** 下的实测返回，不是跨区推断值。

---

## 0. 塔位现状与目标

`get_pyramid_alphas()` 实测 GBR/D1 已点亮塔位：model 5 / analyst 3 / news 1 / other 1 /
pv 1 / fundamental 1。

**未点亮 9 塔**（本战役目标区）与鼓励倍数：

| 塔 | 倍数 | 是否 trio |
|---|---|---|
| sentiment | 1.7 | 否 |
| insiders | 1.5 | 否 |
| option | 1.5 | 否 |
| institutions | 1.4 | 否 |
| earnings | 1.3 | 否 |
| macro | 1.3 | 否 |
| socialmedia | 1.3 | 否 |
| risk | 1.3 | 否 |
| shortinterest | 1.2 | 否 |

9 塔**全部非 trio** ⇒ 与本区已点亮的 fundamental / analyst / news 组腿不受
「PV/MODEL/OTHER 两两禁混」约束，但受「单两塔组合 ≤3」「trio×非trio 总量 ≤5」配额约束。

---

## 1. 数据集覆盖率总表（实测）

**核心结论：GBR TOP700 上，未点亮塔的可挖数据集只有 7 个有实际覆盖，其余 coverage = 0.0。**

| 塔 | 数据集 | coverage | 字段数 | alphaCount | userCount | 判定 |
|---|---|---|---|---|---|---|
| shortinterest | **shortinterest3** Securities Lending Files | **0.849** | 25 | 1569 | 536 | ✅ 主力 |
| risk | **risk60** Securities Lending Insight | **0.6694** | 5 | 197 | 123 | ✅ 可用 |
| risk | risk88 Other Multi-Factor Risk Models | 1.0 | 1 | 544 | 300 | ⚠️ 仅 1 字段 |
| risk | risk68 Forecast Data | **0.0** | 5 | 682 | 345 | ❌ 无覆盖 |
| risk | risk71 Daily Specific Return Profiling | **0.0** | 6 | 568 | 287 | ❌ 无覆盖 |
| risk | risk72 Specific return of extended factors | **0.0** | 23 | 578 | 297 | ❌ 无覆盖 |
| sentiment | **sentiment27** Website Popularity Rankings | **0.8003** | 18 | 790 | 329 | ✅ 可用 |
| sentiment | sentiment33 Sentiment by NLP | 0.3218 | 255 | 205 | 100 | ⚠️ 已实测弱 |
| sentiment | **sentiment7** Webpage Views (Wikipedia) | 0.5784 | 3 | 93 | 55 | ✅ 可用 |
| option | option1 Options Volatility Surfaces | **0.0** | 22 | 280 | 115 | ❌ 无覆盖 |
| earnings | earnings6 International Findings | **0.0** | 18 | 278 | 131 | ❌ 无覆盖 |
| earnings | earnings_sent_matrix Earnings Call Sentiment | **0.0** | 7 | 600 | 262 | ❌ 无覆盖 |
| institutions | institutions6 | 1.0 | 11 | 881 | — | ⚠️ 已实测弱 |
| insiders | insider_agg_matrix | 0.6175 | 34 | — | — | ⚠️ 部分字段无数据 |
| insiders | insiders12 UK Insider Transaction | **0.0** | 7 | 381 | — | ❌ 无覆盖 |

**待补测**：macro / socialmedia / institutions（其余数据集）尚未在 GBR 口径下枚举。

### 1.1 结构性判读

- **coverage = 0.0 密集出现**（risk 3/5、option 1/1、earnings 2/2、insiders 1/2）⇒
  英国 TOP700 小宇宙对多数另类数据供应商不覆盖。这不是「数据集差」，是**区域结构性缺失**。
- 平台 dataset `description` 字段在 GBR 下**严重错配**（例：risk68 名为 Forecast Data，
  description 却描述 order book；risk71 description 描述 fundamental）⇒
  **不可用 description 判断数据集内容，只信 fields 与 coverage**。

---

## 2. shortinterest3 字段画像（25 字段，cov 0.82–0.87）

三套变体：裸名 / `_main` / `_p5_d1`。**`_p5_d1` 覆盖率最高（0.8719）且 userCount 最高**，
是首选口径（本文件后续模板统一用 `_p5_d1`）。

| 字段 | 语义 | coverage | alphaCount |
|---|---|---|---|
| `loaned_share_count_p5_d1` | 出借股数（做空存量） | 0.8719 | 288 |
| `loaned_market_value_usd_p5_d1` | 出借市值 USD | 0.8719 | 249 |
| `transaction_count_p5_d1` | 借贷成交笔数（市场活跃度） | 0.8719 | 164 |
| `shrt3_bar` | **借券需求评级 1–10**（预计算） | 0.8669 | 109 |
| `mean_loan_rate_p5_d1` | 加权平均借券费率 | 0.8719 | 75 |
| `max_loan_rate_p5_d1` | 最高借券费率 | 0.8719 | 49 |
| `min_loan_rate_p5_d1` | 最低借券费率 | 0.8719 | 39 |
| `loan_rate_volatility_p5_d1` | 费率标准差（借贷市场不确定性） | 0.8719 | 45 |
| `average_loan_duration_days_p5_d1` | **借贷久期（做空已持续天数）** | 0.8719 | 49 |

**可构造的高阶量（纯 SHORTINTEREST 单塔，不引入第二塔）**：
- 借券利率价差：`subtract(max_loan_rate_p5_d1, mean_loan_rate_p5_d1)` =  desperate-borrower 尾部
- dealer 价差：`subtract(mean_loan_rate_p5_d1, min_loan_rate_p5_d1)`
- 平均单笔规模：`divide(loaned_market_value_usd_p5_d1, transaction_count_p5_d1)`
- 久期 × 费率交互：`multiply(rank(average_loan_duration_days_p5_d1), rank(mean_loan_rate_p5_d1))`

⚠️ 归一化**不要用 `cap`**（`cap` 属 PV/trio，会引入 trio×非trio 的 ≤5 配额）。
用 `ts_zscore` / `ts_rank` 做时序标准化即可自动消掉公司规模。

---

## 3. risk60 字段画像（5 字段，cov 0.6694）

| 字段 | 语义 | alphaCount |
|---|---|---|
| `rsk60_crowding` | **带符号日度做空活动**（正=加空/拥挤，负=平空） | 88 |
| `rsk60_offer` | 空头支付的借券费率（年化） | 49 |
| `lending_fee_bid_rate` | 多头出借获得的费率 | 35 |
| `rsk60_last` | 最新借贷费率快照 | 30 |
| `rsk60_datatime` | 快照时间戳（HHMMSS，非信号） | 9 |

高阶量：借贷价差 `subtract(vec_avg(rsk60_offer), vec_avg(lending_fee_bid_rate))` =
做市商在证券借贷市场的买卖价差（压力/紧迫度代理）。

---

## 4. sentiment33 字段画像（255 字段，cov 0.3218）

**全部 VECTOR**，需 `vec_*` 聚合。命名规律：

- `snt33_sefke1v1_fkw{1..5}_*` — 主力族，`fkw1..5` 为 5 个时间/关键词桶
- `snt33_{1..5}_{event_title,headline,...}` — **文本字段，α 不可用**
- `sentiment_model{6..9}_*` — 独立模型分数

主族内部结构：`method_{1..9}_{pos,neg,neut,obj}`，另有 `_filtered_` 前缀版本
（多一层 NLP 过滤）。

| 字段 | 语义 | alphaCount |
|---|---|---|
| `snt33_sefke1v1_fkw1_method_1_pos` | 正情绪 token 数（族内最常用） | 13 |
| `snt33_sefke1v1_fkw1_method_1_neg` | 负情绪 token 数 | 7 |
| `snt33_sefke1v1_fkw1_group_level_3_count` | 文档 token 数（注意力代理） | 1 |
| `snt33_sefke1v1_fkw*_valid_tokens_total` | 有效 token 总数 | — |

**9 个 method 是结构性资产**：同一篇文档被 9 种 NLP 算法打分 ⇒
method 间分歧度（`ts_std_dev` 跨 method 的正负极性比）本身就是「情绪不确定性」信号，
是与「情绪水平」正交的独立机制。

---

## 5. 探针实测结果（8 条，全灭）

| # | 数据集 | 模板（机制） | S | F | TO | SUB | 2Y |
|---|---|---|---|---|---|---|---|
| 1 | institutions6 | 机构买卖家净流 / (1+持有者数) | 0.11 | 0.02 | 8.96% | −0.19 | 0.05 |
| 2 | insider_agg_matrix | `directional_indicator` 22d 均值 | 0.00 | 0.00 | 0% | — | — |
| 3 | sentiment33 | 净语调（pos−neg）252d z-score | −0.36 | −0.08 | 28.4% | −0.31 | 0.10 |
| 4 | sentiment33 | 文档 token 数 22d delta 加速度 | −0.35 | −0.11 | 28.8% | 0.07 | 0.14 |
| 5 | risk60 | 借券费率水平 252d z-score | 0.18 | 0.03 | 18.0% | 0.06 | −0.09 |
| 6 | risk60 | 费率 vs 1y 均值偏离 ts_quantile | −0.46 | −0.12 | 19.0% | −0.46 | −1.14 |
| 7 | risk60 | 费率水平 **+ ts_backfill(120)** | 见 §6 消融 | | | | |
| 8 | shortinterest3 | 借券股数 + ts_backfill(120) | 见 §6 消融 | | | | |

### 5.1 「无数据」类失败要单独识别

第 2 条 `A1VbgY1l` 返回 `longCount=0 / shortCount=0 / turnover=0 / pnl=0` ——
这不是「信号弱」，是**字段在 GBR 完全无值**。判据：
`longCount == 0 && shortCount == 0 && turnover == 0` ⇒ 字段级不可用，
不要浪费第二轮同样几何。

### 5.2 探针换手率普遍偏高（18–28%）

对照本区 19 条全闸通过的 alpha，换手率集中在 **8–19%**（多数 8–13%）。
探针 TO 明显偏高是「稀疏字段 + 无 backfill」的直接后果（见 §6）。

---

## 6. ★ 引擎假设：稀疏 VECTOR 字段必须 `ts_backfill`

### 6.1 观察

复盘本区 19 条全闸通过的 alpha，`ts_backfill` 出现 7 次，且分布有规律：

- **用了 `ts_backfill`**：全部建立在稀疏/慢变字段上（`smest_*` estimate、
  `mdl28_*` model、`expected_dividend_yield`、`ep_yield_pct_*`、
  `forward_pe_mean_f12m_4`、`volume`）
- **没用 `ts_backfill`**：全部建立在稠密字段上（`fnd6_*`、`annual_*`、
  `quarterly_*`、`current_enterprise_value`、`returns`）

### 6.2 推论

本文件 §5 的 6 条有效探针**全部使用 coverage 0.32–0.67 的稀疏 VECTOR 字段，
却一条 `ts_backfill` 都没有**。缺失值会让截面信号在两个相邻交易日之间跳变，
这既解释了换手率偏高（18–28% vs 8–13%），也解释了 S 落在 ±0.5 噪声带。

### 6.3 消融实验（单自由度）

对照组与实验组**只差 `ts_backfill(..., 120)` 一个算子**：

```
对照 (MPYXb7Pz, S=0.18):
  -rank(ts_zscore(vec_avg(rsk60_offer), 252))
实验 (?):
  -rank(ts_zscore(ts_backfill(vec_avg(rsk60_offer), 120), 252))
```

若实验组 S 显著抬升 ⇒ 确认 `ts_backfill` 是本区稀疏字段的**必要前置**，
7 个可用数据集的全部模板都应带 backfill 重跑一遍。

---

## 7. 模板池（shortinterest3，≥10 个结构互异）

按用户硬约束「每轮模板库 ≥10 个结构互不相同」列出。差异落在
**矩（水平/一阶差分/二阶方差）/ 算子几何 / 分组轴 / 非线性变换 / 交互**上。

| # | 机制 | 结构 | 表达式骨架 | 来源 |
|---|---|---|---|---|
| T1 | 做空存量水平 | 水平 | `-rank(ts_zscore(ts_backfill(vec_sum(loaned_share_count_p5_d1),120),252))` | Boehmer-Jones-Zhang 2008 |
| T2 | 做空存量变化 | 一阶差分 | `-rank(ts_zscore(ts_delta(ts_backfill(vec_sum(loaned_share_count_p5_d1),120),22),252))` | 自建 |
| T3 | 借券需求评级 | 水平（预计算） | `-rank(ts_zscore(ts_backfill(vec_avg(shrt3_bar),120),252))` | 数据集自带 |
| T4 | 借券费率水平 | 水平 | `-rank(ts_zscore(ts_backfill(vec_avg(mean_loan_rate_p5_d1),120),252))` | Engelberg-Reed-Ringgenberg 2018 |
| T5 | 借券费率变化 | 一阶差分 | `-rank(ts_zscore(ts_delta(ts_backfill(vec_avg(mean_loan_rate_p5_d1),120),22),252))` | 同上（该文核心：变化>水平） |
| T6 | 借贷久期（做空年龄） | 水平 | `-rank(ts_zscore(ts_backfill(vec_avg(average_loan_duration_days_p5_d1),120),252))` | 自建（久期长=空头顽固） |
| T7 | 费率不确定性 | 二阶方差 | `-rank(ts_zscore(ts_std_dev(ts_backfill(vec_avg(mean_loan_rate_p5_d1),120),66),252))` | 自建（借贷市场压力） |
| T8 | dealer 价差 | 差值 | `-rank(ts_zscore(ts_backfill(subtract(vec_avg(max_loan_rate_p5_d1),vec_avg(mean_loan_rate_p5_d1)),120),252))` | 自建（急迫借款人尾部） |
| T9 | 借贷市场活跃度 | 变化 | `-rank(ts_zscore(ts_delta(ts_backfill(vec_sum(transaction_count_p5_d1),120),22),252))` | 自建（借贷周转） |
| T10 | 久期×费率交互 | 交互 | `-rank(multiply(rank(ts_zscore(ts_backfill(vec_avg(average_loan_duration_days_p5_d1),120),252)), rank(ts_zscore(ts_backfill(vec_avg(mean_loan_rate_p5_d1),120),252))))` | 自建 |
| T11 | 平均单笔规模 | 比值 | `-rank(ts_zscore(ts_backfill(divide(vec_sum(loaned_market_value_usd_p5_d1),add(1,vec_sum(transaction_count_p5_d1))),120),252))` | 自建（机构 vs 散户做空） |
| T12 | 分组轴换 subindustry | 分组轴 | `group_rank(ts_zscore(ts_backfill(vec_sum(loaned_share_count_p5_d1),120),252), subindustry)` | 自建 |
| T13 | 非线性变换 | ts_quantile | `-rank(ts_quantile(ts_backfill(vec_avg(mean_loan_rate_p5_d1),120),22))` | 本区 E1 引擎几何 |

**去重纪律**：T1 与 T12 只差分组轴、T4 与 T13 只差非线性变换 ——
用于「同机制不同几何」的对照实验，**不可同时当成两条独立候选提交**
（互相关会 ≈1.0，参见第 118 条：指标逐项相同 + 互相关 ≈1.0 = 同 PnL 变体）。

---

## 8. 下一步

1. 跑完 §6.3 消融，确认 `ts_backfill` 是否为本区稀疏字段的必要前置。
2. 若确认：§7 的 13 个模板全部带 backfill 重跑。
3. 若未确认（S 仍 ±0.5）：GBR 未点亮塔在 TOP700 上**结构上无法出全闸 alpha**，
   需向用户报告并讨论改区或改塔位策略。
4. 补测 macro / socialmedia / institutions 其余数据集在 GBR 的 coverage。

---

## 9. 探针实测总表（2026-10-31 第二轮，16 条）

固定设置：`GBR / TOP700 / D1 / decay 15 / neutralization FAST / truncation 0.05 / nanHandling ON / maxTrade OFF`。
每条只动**数据集或字段或几何**一个自由度。

| # | 数据集（塔） | 机制 / 几何 | alpha | S | F | TO | 2Y | SUB |
|---|---|---|---|---|---|---|---|---|
| 1 | institutions6（institutions） | 机构净流水平 | `leA2Qkex` | 0.11 | 0.02 | 8.96% | 0.05 | −0.19 |
| 2 | insider_agg_matrix（insiders） | `directional_indicator` 水平 | `A1VbgY1l` | — | — | 0.00% | — | — |
| 3 | sentiment33（sentiment） | 净语调水平 | `6Xd1aLZO` | −0.36 | −0.08 | 28.4% | — | −0.31 |
| 4 | sentiment33（sentiment） | 注意力加速度 | `bl6Mo1JR` | −0.35 | −0.11 | 28.8% | — | 0.07 |
| 5 | risk60（risk） | 费率水平 | `MPYXb7Pz` | 0.18 | 0.03 | 18.0% | −0.09 | 0.06 |
| 6 | risk60（risk） | 费率偏离 | `78LQxj7b` | −0.46 | −0.12 | 19.0% | −1.14 | −0.46 |
| 7 | risk60（risk） | 费率水平 **+backfill** | `qMLdnQXE` | 0.40 | 0.13 | 11.45% | 0.10 | 0.14 |
| 8 | **shortinterest3（shortinterest）** | **借券存量水平 +backfill** | **`1YNLorgM`** | **1.25** | **0.67** | **9.34%** | **2.26** | **1.43** |
| 9 | shortinterest3 | 同上，decay 8 / INDUSTRY | `kqNXQJxk` | 0.85 | 0.41 | 8.12% | 1.40 | 1.28 |
| 10 | shortinterest3 | 同上，decay 8 / SUBINDUSTRY | `N1N6AKEE` | 0.68 | 0.29 | 8.77% | 1.41 | 1.06 |
| 11 | shortinterest3 | 借券需求评级 `shrt3_bar` | `E56bK1eK` | 0.17 | 0.03 | 16.43% | −0.08 | 0.51 |
| 12 | shortinterest3 | 借券费率水平 `mean_loan_rate` | `d5WmQpRY` | −0.20 | −0.04 | 14.14% | −0.91 | −0.13 |
| 13 | sentiment27（sentiment） | 网站关注度水平 | `78LQd9k2` | −0.31 | −0.08 | 9.36% | −0.26 | 0.51 |
| 14 | sentiment27 | 网站关注度 一阶差分 | `LLM6RJLL` | −0.49 | −0.15 | 13.11% | 0.04 | 0.10 |
| 15 | insider_agg_matrix | 内部人买卖比水平 | `9qxKRKNe` | 0.51 | 0.18 | 10.18% | −0.06 | 0.81 |
| 16 | insider_agg_matrix | 卖出加速度 | `LLM6RXPa` | 0.21 | 0.04 | 12.23% | −0.15 | −0.03 |

### 9.1 设置轴扫描：降 decay 全线变差，且 TO 反而下降

同一表达式（`1YNLorgM`）decay 15→8，两条中性化轴同时测：

| decay | neutralization | S | F | TO | 2Y |
|---|---|---|---|---|---|
| **15** | **FAST** | **1.25** | **0.67** | 9.34% | **2.26** |
| 8 | INDUSTRY | 0.85 | 0.41 | 8.12% | 1.40 |
| 8 | SUBINDUSTRY | 0.68 | 0.29 | 8.77% | 1.41 |

**结论（与「降 decay 换换手换拟合度」的常见直觉相反）**：
降 decay 后 TO **不升反降**，S 与 2Y 同步崩塌。机理是
`vec_sum(loaned_share_count_p5_d1)` 是稀疏阶梯型字段，decay 15 的平滑
实质在**填补稀疏日期之间的空档**；降到 8 后平滑不足，信号在缺失日被切断，
既没换来换手，也损失了有效暴露。

⇒ **`1YNLorgM` 的指标抬升不能走设置轴，只能走表达式本身。**
（对应 `fitness = S × √(returns / max(TO, 0.125))`：TO 9.34% 仍在 12.5% 地板下，
本来就没有「靠提 TO 换 returns」的空间。）

### 9.2 GBR 特有方向：借券费率与网站关注度都与美股文献反向

| 机制 | 美股文献方向 | GBR 实测 | 判读 |
|---|---|---|---|
| 借券**费率**水平（`mean_loan_rate`） | 高费率 ⇒ 后续跑输（取负） | S **−0.20**（取负后为负） | **反向**：高费率在 GBR 正向预测收益 |
| 网站**关注度**水平（`snl27_relpopularity1`） | 高关注 ⇒ 过度定价 ⇒ 反转（取负） | S **−0.31**（取负后为负） | **反向**：关注度在 GBR 是正向动量 |
| 网站关注度**变化** | 同上 | S **−0.49** | **反向** |
| 借券**数量**水平（`loaned_share_count`） | 高借券量 ⇒ 跑输（取负） | S **+1.25** | ✅ 与文献一致 |

⇒ **只有「借券数量」族在 GBR 与文献同向**；费率族与关注度族都反号。
即便翻正号，sentiment27 也只有 +0.31 / +0.49，量级仍远不够。
**教训**：跨区平移模板必须逐族验符号，不能假设美股文献方向成立。

### 9.3 结构性结论：GBR 未点亮塔的产量率 ≈ 1/16

16 条探针里 **只有 1 条**（`1YNLorgM`，S 1.25）越过 S>1.0，
且仍未达闸（需 S≥1.58 且 F≥1.0）。次优是 `9qxKRKNe` 的 0.51。

按此产量率外推，要在 GBR 未点亮塔再造 40 条全闸 alpha
需要约 **640 条探针**——不是算力问题，是**该区未点亮塔的可挖面本身不够**：

- option / earnings / macro 三塔在 GBR TOP700 **coverage 全为 0.0**（§2），
  名义 9 塔实际只有 9 个数据集、6 个塔有数据。
- 剩余可挖数据集里，cov 0.85 的只有 shortinterest3 一个；
  risk88 仅 1 字段、socialmedia39 仅 1 字段。
- `directional_indicator` 平台标 cov=1.0 / alphaCount=61，说明
  **第一轮「字段无数据」的判定是表达式几何错**（`A1VbgY1l` 全零），
  换成买卖比后立刻出 S 0.51 —— 该字段本身有值。

### 9.4 自我诊断：前 16 条探针用了同一个几何（模板单一）

16 条里 14 条共用 `rank(ts_zscore(ts_backfill(x,120),252))` 这一个骨架，
只换了字段。这正是「一个骨架刷 N 条」的伪覆盖，会把
**骨架选错**误判成**字段没信号**。

本区已通过的 19 条全闸 alpha 里，8 条用的是 E1 引擎：

```
rank(ts_quantile(ts_av_diff(<字段>, 252), 22))      # 本区 8/19
ts_target_tvr_decay(rank(ts_delta(ts_backfill(<慢变字段>,500),N)), ...)   # 本区 8/19
```

⇒ 已补发 E1 引擎到 `loaned_share_count` 与 `snl27_relpopularity1` 两条最有望的字段上，
用以判断「到底是字段不行还是骨架不行」。
`E1` 才是本区强先验，前面 16 条的结论只能作为**字段级弱信号筛选**，不能当机制判死。

---

## 10. 下一步（修订）

1. 读 E1 引擎结果：若 E1 显著优于通用 zscore 骨架 ⇒ 用 E1 重跑全部 6 个有数据塔；
   若 E1 也不行 ⇒ GBR 未点亮塔确实无货，需与用户讨论改区。
2. 继续 shortinterest3 的 T2 / T5 / T6 / T8 / T11（数量族与久期族，避开已判反向的费率族）。
3. 补测 macro / socialmedia / institutions 其余数据集在 GBR 的 coverage（todo）。
4. 向用户报告产量率与 60 条目标的差距，请求「是否允许跨区补足」的决策。
---

## 11. E1 引擎对照实验：本区引擎不可平移到未点亮塔（2026-10-31 追加）

§9.4 提出「前 16 条模板单一」的自我诊断，据此补做 E1 引擎对照。
结论是**否定的**，而且机理比结论更有价值。

| 字段 | 通用骨架 `rank(ts_zscore(ts_backfill(x,120),252))` | 本区 E1 `rank(ts_quantile(ts_av_diff(x,252),22))` | Δ |
|---|---|---|---|
| shortinterest3 `loaned_share_count` | **+1.25**（`1YNLorgM`） | +1.15（`KPJ6LOrz` 取负得 −1.15） | −0.10 |
| sentiment27 `snl27_relpopularity1` | +0.31（`78LQd9k2` 取负得 −0.31） | +0.24（`bl6M9R8p`） | −0.07 |
| insider_agg_matrix 买卖比 | **+0.51**（`9qxKRKNe`） | +0.10（`akKlOQV1`） | **−0.41** |

**⇒ E1 引擎在未点亮塔上并不占优，甚至更差。**

**机理**：本区 19 条全闸 alpha 里 E1 之所以强，靠的**不是** `ts_av_diff`
这个矩几何，而是它的分母 `current_enterprise_value` —— 即
「会计科目 ÷ 企业价值」本质是**估值收益率信号**（收益率 = 分母价格位移）。
把 E1 平移到未点亮塔时，`ts_av_diff` 保留了、**分母丢了**，
剩下的只是一个朴素的历史偏离度，自然退化。

⇒ **推论（可迁移）**：判断「本区引擎能否平移到新数据集」，要看
**引擎的收益来源（分母/核心算子）在新数据集里有没有对应物**，
不能只看外层算子形状。E1 的核心是分母，不是 `ts_av_diff`。

⇒ **可执行方向**：给未点亮塔字段补一个「份额/规模」分母，
把「水平量」变成「比率」——这才复现了 E1 的真正机制。
已派发 `divide(<借券市值>, current_enterprise_value)` 与
`divide(<内部人买入股数>, current_enterprise_value)` 两条做验证
（SHORTINTEREST×FUNDAMENTAL / INSIDERS×FUNDAMENTAL 两塔组合，
均非 trio 内部互组，合规；每两塔组合配额 ≤3）。

### 11.1 追加 4 条探针结果（第 17–20 条）

| # | 数据集 | 机制 | alpha | S | F | TO | 2Y | SUB |
|---|---|---|---|---|---|---|---|---|
| 17 | shortinterest3 | E1 引擎（`ts_av_diff`+`ts_quantile`） | `KPJ6LOrz` | −1.15（翻正 +1.15） | −0.52 | 15.04% | −1.57 | −0.60 |
| 18 | sentiment27 | E1 引擎 | `bl6M9R8p` | 0.24 | 0.05 | 13.92% | −0.16 | −0.30 |
| 19 | insider_agg_matrix | E1 引擎（买卖比） | `akKlOQV1` | 0.10 | 0.02 | 10.18% | 0.79 | −0.05 |
| 20 | shortinterest3 | 借券存量**一阶差分** T2 | `LLM6Rm5m` | −0.42 | −0.12 | 14.00% | 0.71 | −0.03 |

**第 20 条的意义**：短租信号是**水平（存量）**而不是**变化（流量）**。
`loaned_share_count` 的水平 S 1.25，换成 `ts_delta(…,22)` 立刻变 −0.42。
这与美股文献（Engelberg-Reed-Ringgenberg：做空**变化**比水平更有信息）
**相反**，是本区第二个符号/形式反转。

### 11.2 20 条探针的完整排序（判死线：S ≥ 1.0 视为有机制）

| 排名 | alpha | 数据集 | S | 结论 |
|---|---|---|---|---|
| 1 | `1YNLorgM` | shortinterest3 | **1.25** | 唯一近闸，仍差 S +0.33 / F +0.33 |
| 2 | `9qxKRKNe` | insider_agg_matrix | **0.51** | 有信号但距闸远 |
| 3 | `qMLdnQXE` | risk60 | 0.40 | 加 backfill 后才到 0.40 |
| 4 | `bl6M9R8p` | sentiment27 | 0.24 | E1 形态，翻正后可用 |
| 5 | `LLM6RXPa` | insider_agg_matrix | 0.21 | |
| 6 | `MPYXb7Pz` | risk60 | 0.18 | |
| 7 | `E56bK1eK` | shortinterest3 | 0.17 | |
| 8 | `akKlOQV1` | insider_agg_matrix | 0.10 | |
| 9 | `leA2Qkex` | institutions6 | 0.11 | |
| — | 其余 11 条 | | ≤0 或 |S|<0.1 | 含 5 条符号反向 |

**⇒ 20 条探针里 S≥1.0 的只有 1 条（5%），S≥0.5 的只有 2 条（10%）。**

### 11.3 关于「60 条」目标的现实判断

GBR 未点亮塔按当前产量率（1/20）无法在合理成本内补出 40 条全闸 alpha。
真正限制不是探针数量，而是本区这三条结构性事实：

1. **9 塔里只有 6 塔有数据**，option / earnings / macro 全 coverage=0（§2）。
2. **唯一 cov>0.8 的数据集只有 shortinterest3 一个**，其余在 0.32–0.80。
3. **本区强引擎的核心（EV 分母）在未点亮塔里没有对应物**（§11），
   而补分母需要跨数据集组腿，吃两塔配额。

⇒ 若要达成 60 条，只有三条路：
- **A** 继续在 GBR 深挖（预期再出 2–5 条，达不到 60）
- **B** 把「未点亮塔」的战场扩到其他区域（各区的未点亮塔不同，倍率也不同）
- **C** 两者并行：GBR 深挖 + 其他区补量
---

# 12. ★ 突破：E3 引擎（days-to-cover）与 `ts_rank(504)` 放大器

> **⚠ 2026-10-31 追记（必读）**：本节所说的「全闸通过」只覆盖 **IS / RA 层**。该引擎的两条代表 alpha
> （`leA23Jae` / `QPvj9m0K`）在生产池相关性层实测 **0.7445 / 0.7044，双双撞墙** ⇒ **整枝已封盘、0 颗可提**。
> 结论以**文末 §18** 为准；本节保留原样只为留存实验过程与几何对比。

> 本节写于 §11 之后，**取代 §11.3 的「预期再出 2–5 条」估计**：
> 实际结果是未点亮塔**首次产出 2 条全闸通过**（互相关 0.85，实际可提 1 颗），
> 并新开 institutions6 第二条机制线。§11.3 的三条结构性事实仍然成立，
> 但「唯一可行路 = 继续深挖 A」已被验证为**能出全闸 alpha，只是产量上限极低**。

## 12.1 E3 引擎定义

```
-rank( ts_rank( ts_backfill( divide( vec_sum(loaned_share_count_p5_d1),
                                      ts_mean(volume, W) ), 120), 504) )
```

- **经济含义**：days-to-cover —— 借券股数 ÷ 日均成交量 = 「按当前流动性，空头需要几天平仓」。
  它是**流动性标准化后的空头拥挤度**，不是「借券规模的绝对水平」。
- **W = ADV 窗口**，取 22 或 126 均优（见 §12.3）。
- **符号为负**：DTC 越高 ⇒ 空头越拥挤 ⇒ 未来收益越低。

## 12.2 标准化口径的对照矩阵（同字段、同外层几何）

| 口径 | alpha | S | F | TO | 2Y | SUB | 结论 |
|---|---|---:|---:|---:|---:|---:|---|
| **÷ `ts_mean(volume,22)`** | `leA23Jae` | **1.72** | **1.08** | 9.95% | 2.60 | 1.79 | ★ 全闸通过 |
| **÷ `ts_mean(volume,126)`** | `QPvj9m0K` | **1.71** | **1.06** | 9.16% | 2.73 | 1.80 | ★ 全闸通过 |
| ÷ `sharesout`（真实 SIR） | `E56blbEP` | 1.46 | 0.85 | 9.17% | 2.38 | 1.56 | 差 F 0.15 |
| ÷ `current_enterprise_value` | `npvoWEe3` | 1.07 | 0.59 | 10.29% | — | 1.29 | 差 S 0.51 |
| 裸存量 | `1YNLorgM` | 1.25 | 0.67 | 9.34% | 2.26 | 1.43 | 差 S 0.33 |

**⇒ 判据（第 130 条）**：增量不在「除一个规模量」，而在「**分母含交易活跃度**」。
÷sharesout 与 ÷EV 都是规模量，只得 1.46 / 1.07；÷ADV 得 1.72。
**同一字段换分母 = +0.65 Sharpe**，这是本轮最大的单点增益。

## 12.3 ADV 窗口是非单调的（谷在中间）

| ADV 窗 | S | F | TO |
|---:|---:|---:|---:|
| 22 | **1.72** | 1.08 | 9.95% |
| 66 | 1.62 | 0.98 | 9.25% |
| 126 | **1.71** | 1.06 | 9.16% |

**⇒ 22 与 126 是双峰，66 落谷底。** 这不是噪声能解释的形状，
但同时说明 **W 不是单调杠杆**，别把 W 当调参旋钮逐点扫（第 123 条同源教训：
设置轴 / 窗口轴都不是免费杠杆）。

## 12.4 `ts_rank(504)` 是稳定放大器（3/3 独立确证）

| 字段族 | `ts_zscore(252)` | `ts_rank(504)` | ΔS |
|---|---:|---:|---:|
| 借券裸存量 | 1.25（`1YNLorgM`） | **1.53**（`Xg9Ln5ox`） | +0.28 |
| DTC22 | 1.57（`pwdElM0v`） | **1.72**（`leA23Jae`） | +0.15 |
| 借贷集中度 CoV | 1.00（`6Xd19vpK`） | **1.18**（`QPvj9gbM`） | +0.18 |

**为什么有效**：`ts_zscore` 假设分布近似正态且平稳；`ts_rank` 只要**序**，
对借贷这笔重尾、有结构断点的数据更稳健（2 年百分位天然抗极值）。

**窗长必须取 504**：`ts_rank(252)` 版只得 S 1.15（`1YNLdMPR`），
比 504 版低 0.38 —— 252 太短，覆盖不到一次完整的做空周期。

**边界（第 128 条）**：`ts_rank(504)` 只能**放大**、不能**创造**信号。
内部人买入 ÷ADV 加 ts_rank 后仍只有 S 0.29、2Y −0.78（`2rARNWw5`）。

## 12.5 全族收敛：shortinterest3 只贡献 1 颗

| 变体 | alpha | S |
|---|---|---:|
| 借贷笔数水平 | `qMLdNGgV` | 1.35 |
| 借贷市值水平 | `mLoA5789` | 1.37 |
| 借贷股数（DTC22） | `leA23Jae` | 1.72 |
| 借贷股数（DTC126） | `QPvj9m0K` | 1.71 |
| DTC66 | `leA2lm92` | 1.62 |

`leA23Jae` ↔ `QPvj9m0K` 实测互相关 **0.8469**，
`compute_mutual_correlation` 的 `max_mutually_below_subset` = **1 条**。

**⇒ 第 127 条在本区再次成立**：同族变体互相关 ≈ 1，**一个机制族最多贡献 1 颗提交**。
DTC 这条线已经封盘，不要再换 W / 换外层算子刷变体。

## 12.6 institutions6：第二条机制线（卖方广度）

```
-rank( ts_rank( count_institutional_sellers_security, 504 ) )   → WjOd7edQ
S 0.95 / F 0.46 / TO 8.32% / 2Y 2.17 / SUB 0.41 / dd 5.37%
```

**2Y 2.17 > 全期 0.95** ⇒ 机制在近年增强（与 shortinterest3 的 2Y 2.4–2.8 同向），
不是衰减型。距闸差 S 0.63，跨度大但方向正确。

### 12.6.1 机制不是「方向」，是「机构活动广度」

| 变体 | alpha | S | 推论 |
|---|---|---:|---|
| `-sellers` | `WjOd7edQ` | **0.95** | 基准 |
| `-(sellers − buyers)` 净卖方广度 | `VkxE6aZY` | 0.64 | **减去买方 ⇒ 掉 0.31** |
| `-ts_delta(sellers,22)` 加速度 | `leA28vEA` | 0.27 | 变化形式无效 |
| 持股占比 ÷sharesout | `mLoAj6J6` | −0.20 | 存量占比无效 |

**⇒ 关键推论**：净广度（−0.31）劣于纯广度，说明 `sellers` 里携带信息的
是「**有多少家机构在这个标的上有动作**」（关注 / 覆盖强度），
不是「卖 vs 买的比例」。方向被价格内生化，家数没有。

### 12.6.2 对称性检验：假设被推翻，"广度说" 不成立（2026-10-31 实测）

我原先假设「`sellers` 强是因为广度而非方向」——若成立，`+buyers` 应同样为正。
**实测推翻了它**：

| 模板 | alpha | S | 2Y | SUB | 读法 |
|---|---|---:|---:|---:|---|
| `-ts_rank(sellers)` | `WjOd7edQ` | **0.95** | 2.17 | 0.41 | 基准 |
| `+ts_rank(buyers)` | `akKlbEoW` | −0.14 | **−0.47** | −0.40 | **买方家数同为负向** |
| `+ts_rank(holders)` | `ZYQxbKoY` | −0.19 | **−1.23** | −0.29 | 持有家数近年强负 |
| `-ts_rank(sellers − buyers)` | `VkxE6aZY` | 0.64 | 1.19 | 0.08 | 减法掉 0.31 |

**⇒ 真正的机理（三条一致性证据）**：

1. `+buyers` 为负 ⇒ **买、卖两个方向的家数增加都与未来收益负相关**，
   差别在**幅度**：卖方向 −a 强（0.95），买方向 −b 弱（0.14）。
   这是「**机构交易活动 = 拥挤度**」的典型形态，不是方向性 alpha。
2. `-(sellers − buyers)` = 0.64 < 0.95 ⇒ 做减法把买方的**弱反向**信息当噪声减掉了，
   与 a − b ≈ 0.95 − 0.14 = 0.81（rank 非线性损耗后 0.64）量级吻合。
3. `+holders` 全期 −0.19 但 **2Y −1.23** ⇒ 持有机构家数越多，近年表现越差，
   即**持仓拥挤度**在 2022–2023 被强烈定价。但它全期太弱，过不了 S 闸。

**⇒ 可迁移结论（第 132 条）**：机构类「家数」字段是**拥挤度代理**，
正向（家数多）一律负收益、卖方向最强。**做减法 / 做比值会把弱信号当噪声减掉**，
要的是「单一最强的拥挤维度」而不是「净额」。这解释了为什么 12.6.1 里
`mLoAj6J6`（持股**占比**）也是 −0.20：占比同样被价格内生化到一个很弱的水平。

**⇒ 但 holders 的 2Y −1.23 值得记一笔**：这是本区唯一一个「全期与近年方向一致
且近年极强」的家数字段。若将来有方法把全期 S 拉起来（例如与其他维度正交化），
`-ts_rank(holders, 504)` 是最有潜力的候选。当前判**留存不用**。

## 12.7 本轮判死清单（新增）

| 数据集 | 判死理由 | 证据 |
|---|---|---|
| **sentiment27**（Transcope 网站关注度） | 水平 / 差分 / 长窗百分位 / 正反号**全部无信号** | 水平 −0.31（`78LQd9k2`）、差分 −0.49（`LLM6RJLL`）、翻正 +ts_rank504 仅 0.17 且 SUB −0.32 / 2Y 0.08（`P0o676Oq`） |
| institutions6 **持股占比**族 | 存量占比被价格内生化，翻正仅 0.20 | `mLoAj6J6` S −0.20 / 2Y −0.27 / SUB −0.41 |
| shortinterest3 **加速度**族 | 短租是水平信号不是加速度信号 | `ts_av_diff`/`ts_quantile` 4/4 崩塌（`KPJ6LOrz` −1.15、`vR19LeOw` −0.84） |
| **sentiment7**（Wikipedia 浏览量） | 唯一未测的注意力数据集，实测弱且衰减 | `qMLdLM8V` S 0.49 / F 0.15 / **2Y −0.19** / TO 16.64% |
| **socialmedia39** | 唯一字段是「共同观看邻居的标的 ID 列表」，非数值经济量 | `scl39_top5_people_also_watch_ticker_ii`（VECTOR, cov 0.4948）；`vec_*` 只能给「ID 均值」（无意义）或「邻居数」（固定 top5 ⇒ 常数） |
| institutions6 **占比族**（持股数占比 / 持股市值占比） | 占比被价格内生化，一律无信号 | `mLoAj6J6` −0.20、`9qxKWneK` **0.00** |

# 13. 本轮新增口径知识（跨区可复用）

## 13.1 `LOW_SUB_UNIVERSE_SHARPE` 的 limit 是**动态**的，≈ S × 0.47

| alpha | S | SUB 实测 | SUB limit |
|---|---:|---:|---:|
| `WjOd7edQ` | 0.95 | 0.41 | **0.45** |
| `VkxE6aZY` | 0.64 | 0.08 | **0.30** |
| `leA28vEA` | 0.27 | 0.09 | **0.13** |
| `mLoAj6J6` | −0.20 | −0.41 | **−0.09** |

**⇒ 别再用固定的「SUB ≥ 0.45」口径读闸**。SUB 闸是与自身 S 挂钩的相对闸，
其含义是「子宇宙里信号不能比全宇宙塌太多」。之前台账里 `WjOd7edQ` 判「差 SUB 0.04」
是按固定 0.45 读的——恰好这次也是 0.45，但换一条 alpha 就会读错。

## 13.2 PV 塔是被**分母字段**点亮的，不是被主字段

| 表达式分子 | 分母 | 产出塔 |
|---|---|---|
| `loaned_share_count` | `ts_mean(volume,22)` | SHORTINTEREST×1.2 + **PV×1.4** |
| `loaned_share_count` | `sharesout` | SHORTINTEREST×1.2 + **PV×1.4** |
| `aggregate_share_count_institutions` | `sharesout` | INSTITUTIONS×1.4 + **PV×1.4** |
| `count_institutional_sellers_security` | 无 | **仅 INSTITUTIONS×1.4** |

**⇒ 派发前算配额时，要看「分母是不是 PV 字段」**。`volume` / `sharesout` 均属 PV。
当前 PV 已用 3/5（`leA23Jae`、`QPvj9m0K`、`2rARNWw5`），剩 2 槽。

## 13.3 risk88 的唯一字段其实是「市值」

`risk88` 只有 1 个字段：`alternative_market_cap_usd`（MATRIX, **cov 1.0**, ac 544）——
描述为「Market capitalization of each stock expressed in US dollars」。

**⇒ 它是分母候选，不是风险因子**。价值：可替代 `current_enterprise_value`
当分母同时点亮 RISK 塔（×1.3），且 cov=1.0 完全无缺失。
这是本区**最省成本的 RISK 点塔杠杆**（比 risk60 的 0.44 更值得试）。

## 13.4 fitness 公式（本区实测复现）

```
fitness ≈ S × √( returns / max(TO, 0.125) )
```

- TO < 12.5% ⇒ 分母恒为 0.125 地板 ⇒ **提换手永远提不了 fitness**。
- **破 fitness 只有两条路：① 提 S ② 提 returns（年化收益）**。
- 零成本提 returns 的手段 = **换中性化轴**（不动表达式、不占额外配额）。
- 实例：`leA2lm92` S 1.62 / F 0.98 / TO 9.25% ⇒ 需 returns 从 4.58% 提到 4.76%（+4%）
  即可过 F 闸。

# 14. sentiment7（Wikipedia）与 socialmedia39 —— 尚未测

| 数据集 | 字段 | 类型 | cov | ac | 备注 |
|---|---|---|---:|---:|---|
| sentiment7 | `snt7_views` | VECTOR | 0.5766 | 42 | Wikipedia 日浏览量 |
| sentiment7 | `snt7_all_languages_views` | VECTOR | 0.5819 | 37 | 全语言浏览量 |
| sentiment7 | `snt7_timestamp` | VECTOR | 0.5766 | 16 | 非信号 |
| socialmedia39 | — | — | 0.4948 | 273 | 仅 1 字段 |

cov < 0.9 ⇒ 按第 120 条必须带 `ts_backfill(x, 120~250)`。
**注意 sentiment27 已全族判死 ⇒ 同为「关注度」类的 sentiment7 先验应下调**，
若要测，优先测「浏览量 ÷ 自身长期均值」而非绝对水平（sentiment27 的教训是水平无效）。

---

*本节由 2026-10-31 GBR 未点亮塔深挖（wave `s2_unlit_dtc_rank_d1` + `s2_unlit_tsrank_family_d1`）实测产出，共 16 条新回测。*
---

# 15. ★ 未点亮塔挖掘穷尽盘点（2026-10-31 收口）

**结论：GBR 未点亮塔的全部 9 个塔 / 17 个候选数据集已逐一实测完毕，无剩余未探面。**

## 15.1 全量台账（按最好 S 排序）

| # | 塔 | 数据集 | cov | 已测模板数 | 最好 S | 状态 | 结论 |
|---:|---|---|---:|---:|---:|---|---|
| 1 | SHORTINTEREST | **shortinterest3** | 0.849 | 9 | **1.72** | ✅ **全闸通过** | 唯一产出可提 alpha 的集；族内互相关 0.85 ⇒ **封盘，只取 1 颗** |
| 2 | INSTITUTIONS | **institutions6** | 1.0 | 9 | **0.99** | ⚠️ 差 S 0.59 | 9 个模板收敛到唯一机制「卖方家数 ts_rank」；2Y 2.46 为全区新高 |
| 3 | INSIDERS | insider_agg_matrix | 0.594 | 6 | 0.51 | ❌ | 买卖比 0.51 / 卖出加速度 0.21 / ÷EV 0.31（2Y −0.31）/ ÷ADV 0.29（2Y −0.78） |
| 4 | SENTIMENT | sentiment7 | 0.577 | 1 | 0.49 | ❌ 判死 | Wikipedia 浏览量，2Y −0.19 衰减 |
| 5 | RISK | risk60 | 0.669 | 5 | 0.44 | ❌ | 费率水平 0.18 / 偏离 −0.46 / backfill 后 0.40 / ÷EV 0.44 / 波动率 0.78（2Y 1.34 但 S 差远） |
| 6 | SENTIMENT | sentiment27 | 0.800 | 5 | 0.24 | ❌ 判死 | 水平 / 差分 / 正反号 / 长窗百分位全无信号 |
| 7 | SOCIALMEDIA | socialmedia39 | 0.495 | 0 | — | ❌ 判死 | 唯一字段是非数值的标的 ID 列表 |
| 8 | SENTIMENT | sentiment33 | 0.322 | 2 | −0.36 | ❌ 判死 | NLP 净语调为负 |
| 9 | RISK | risk88 | 1.0 | 1 | 0.00 | ⚠️ 仅分母 | 唯一字段 `alternative_market_cap_usd` 是市值；当分母能点亮 RISK 塔但机制无信号 |
| — | OPTION / EARNINGS / MACRO / INSIDERS12 / SOCIALMEDIA12 / SOCIALMEDIA5 / RISK68 / RISK71 / RISK72 | 9 个集 | **0.0** | 0 | — | ❌ 无数据 | coverage = 0，不可用 |

## 15.2 产量上限的算术

- **有数据**的未点亮塔数据集 = 8 个（shortinterest3 / institutions6 / insider_agg_matrix / sentiment7 / risk60 / sentiment27 / socialmedia39 / sentiment33 / risk88 → 实为 9，其中 risk88 仅作分母）。
- **出全闸 alpha** 的 = 1 个（shortinterest3），贡献 **1 颗**（族内只能取 1）。
- **接近闸但未过** 的 = 1 个（institutions6，差 0.59）。
- ⇒ **GBR 未点亮塔的产量上限 = 1 颗可提 + 1 颗潜在**，与 §11.3 的事前判断一致，差距在于事前估「2–5 条」偏乐观。

**⇒ 若目标仍是 60 条，未点亮塔这条路在本区已封闭。** 可行的补充只能来自：
1. 已点亮塔（MODEL 5 / ANALYST 3 / NEWS 1 / OTHER 1 / PV 1 / FUNDAMENTAL 1）的深挖 —— 那里历史产量高得多；
2. 换区（用户 2026-10-31 已裁定不跨区）。

# 16. ★ 冻结篮纠错：18 条里有 3 条并非全闸通过

提交前复核 `batch_get_alpha_metrics`（2026-10-31 实测），发现 3 条的 `failed_ra_count = 1`：

| alpha | S | F | 2Y | 卡项 | 说明 |
|---|---:|---:|---:|---|---|
| `GrOMbGO5` | 1.94 | 1.29 | **1.17** | LOW_2Y_SHARPE | 差 0.41 |
| `3qV7Q2dO` | 1.77 | 1.07 | **0.48** | LOW_2Y_SHARPE | 差 1.10，最严重 |
| `mL68wNOK` | 1.63 | 1.07 | **1.58** | LOW_2Y_SHARPE | **压线失败**：limit = 1.58，严格小于才过 |

**⇒ 真实全闸通过 = 18 − 3 = 15 条。**（**RA 层口径**；随后 10-31 prod 全量刷新又漂死 7 条，**可提落定 8 条**，见 §17.6。）

**两条口径教训**：

1. **`checks.fail = []` 不等于过闸** —— 这三条的 `checks.fail` 都是空数组，
   卡项只在 `checks.warning` 里，而 `ra.failed_ra_count` 会计入 warning。
   判闸必须读 `ra.failed_ra_count == 0 && ra.failed_ppa_count == 0`。
2. **ATOM 不豁免 `LOW_2Y_SHARPE`** —— ATOM 只豁免 `IS_LADDER_SHARPE`。
   `mL68wNOK` 恰好证明 2Y 闸是**含等号严格**的：2Y = limit 时仍判失败。

**⇒ 提交前动作（2026-10-31 已实测更新）**：这 3 条**全部判死**。原计划「`mL68wNOK` 只差无穷小、值得试中性化轴 / decay」已被 §17 的 6 条设置轴实验证伪——nanHandling 开关对该字段零影响，STATISTICAL 本身就是 2Y 最优中性化轴，换任一轴只会把 2Y 打得更低。`3qV7Q2dO` 差 1.10、`GrOMbGO5` 差 0.41，更无路径。

---

*§15–16 写于 2026-10-31 收口，基于 wave `s2_unlit_tsrank_family_d1` 的 12 条回测 + 冻结篮全量平台复核。*

# 17. ★ 修压线 2Y 的设置轴实验：全部失败，三条判死（2026-10-31 封盘）

§16 留了一个出口：「`mL68wNOK` 只差无穷小，值得优先试中性化轴 / decay」。本节用 **6 条新回测**把这个出口彻底试完，结论是**此路不通**。

## 17.1 实验设计（严格控制变量）

| 组 | 自由度 | 固定项 | 条数 |
|---|---|---|---:|
| A 组 | `nanHandling` OFF→ON | decay 12 / STATISTICAL / trunc 0.1 / TOP700 / D1 | 2 |
| B 组 | `neutralization` 四档 | decay 12 / trunc 0.1 / **nanHandling ON** / TOP700 / D1 | 4 |

A、B 两组的公共基线是 `A1VbxnAw`（STATISTICAL + nanHandling ON），用于交叉校验设置无串扰 —— 它同时是 A 组的 ON 档与 B 组的 STATISTICAL 档，实测两侧读数完全一致（S 1.63 / F 1.07 / 2Y 1.58 / TO 12.84%），确认实验干净。

## 17.2 A 组：nanHandling 不是万能的

| alpha | 表达式来源 | nanHandling | S | F | TO | 2Y | SUB | 卡项 |
|---|---|---|---:|---:|---:|---:|---:|---|
| `mL68wNOK` | mdl28 结构性杠杆加速度 | OFF（原条） | 1.63 | 1.07 | 12.84% | **1.58** | 0.86 | 2Y 压线 |
| `A1VbxnAw` | 同上 | **ON** | 1.63 | 1.07 | 12.84% | **1.58** | 0.86 | 2Y 压线 |
| `GrOMbGO5` | forward_pe 加速度 | OFF（原条） | **1.94** | **1.29** | 12.50% | **1.17** | **0.95** | 2Y |
| `VkxENXW5` | 同上 | **ON** | 1.82 | 1.15 | 11.49% | **0.94** | **0.84** | 2Y + SUB |

**两条读数**：

1. **`A1VbxnAw` 与 `mL68wNOK` 逐位相同**（连 TO 12.84% 都一样）⇒ `mdl28_sm_structural_multiple_credit_structural_leverage` 覆盖率 100%，`nanHandling` 开关对它**没有任何作用**。此前「nanHandling 是季频/事件驱动字段的头号杠杆」的结论，**不能推广到高覆盖字段** —— 杠杆效力与字段缺失率成正比，缺失率为零时杠杆为零。
2. **`nanHandling` ON 对 analyst 字段是负作用**：`VkxENXW5` 相比 `GrOMbGO5` 三项同时退化（S 1.94→1.82 / F 1.29→1.15 / 2Y 1.17→0.94），并新增卡 `LOW_SUB_UNIVERSE_SHARPE`（0.84 < limit 0.86）。⇒ **nanHandling 不是「开着总比关着好」的安全选项**，它改变的是缺失票参与截面的方式，方向上可正可负，必须实测。

## 17.3 B 组：STATISTICAL 就是 2Y 最优轴

同一 `mL68wNOK` 表达式，只换中性化轴：

| 中性化 | alpha | S | F | returns | dd | margin | 2Y | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **STATISTICAL** | `mL68wNOK` / `A1VbxnAw` | **1.63** | 1.07 | 5.57% | **4.97%** | 8.67 bp | **1.58** | 2Y 压线（最接近） |
| INDUSTRY | `WjOdl0Jj` | 1.47 | 1.23 | **8.76%** | 7.66% | **16.96 bp** | 1.29 | S + 2Y 双卡 |
| SUBINDUSTRY | `A1VbxmJE` | 1.52 | **1.26** | 8.53% | 6.17% | 16.33 bp | 1.10 | S + 2Y 双卡 |
| SLOW_AND_FAST | `3qox0KRO` | 1.20 | 0.52 | 3.61% | 4.15% | 3.82 bp | 0.81 | S + F + 2Y 三卡 |
| FAST | `9qxKl3we` | 1.08 | 0.48 | 3.68% | 4.77% | 3.94 bp | 0.79 | S + F + 2Y 三卡 |

**2Y 单调排序：STATISTICAL 1.58 > INDUSTRY 1.29 > SUBINDUSTRY 1.10 > SLOW_AND_FAST 0.81 > FAST 0.79。**

**⇒ 换中性化轴不是修 2Y 的杠杆，是反向杠杆。** 当前设置已经是 2Y 的最优点，**没有任何设置自由度可以再榨**。

**附带一个结构性观察（可迁移）**：这四档把同一条 alpha 分成了两族——
- **低波动族**（STATISTICAL / SLOW_AND_FAST / FAST）：returns 3.6–5.6%、dd 4.2–5.0%、S 更高；
- **高收益族**（INDUSTRY / SUBINDUSTRY）：returns 8.5–8.8%（+55%~+57%）、dd 6.2–7.7%、F 1.23–1.26 更高。

**但 2Y 与这两族都不相关**：高收益族 2Y 只有 1.10–1.29，低波动族 0.79–0.81，中间夹着最优的 STATISTICAL 1.58。⇒ **中性化轴改的是「收益/波动配比」，改不了「信号在 2022–2023 是否存在」**。2Y 是信号的时序属性，不是截面属性。

## 17.4 三条卡 2Y 候选的最终裁定

| alpha | S | F | 2Y | 差距 | prod | self | 裁定 |
|---|---:|---:|---:|---:|---:|---:|---|
| `mL68wNOK` | 1.63 | 1.07 | 1.58 | **0.00（压线）** | 0.6608 | 0.4979 | **DEAD** —— 2Y 已是全区最优档，无自由度可动 |
| `GrOMbGO5` | 1.94 | 1.29 | 1.17 | 0.41 | 0.69 | — | **DEAD** —— nanHandling ON 反降至 0.94 |
| `3qV7Q2dO` | 1.77 | 1.07 | 0.48 | **1.10** | 0.6596 | 0.3669 | **DEAD** —— 差距过大，无路径 |

**三者的 prod / self 都在红线内**（prod 0.66–0.69、self 0.37–0.50）⇒ 它们**纯粹被 2Y 单闸拦下**，不是相关性/集中度问题。一旦 2Y 解决即可直通提交流程 —— 但 2Y 解决不了。

## 17.5 三条新规则（可迁移）

- **第 136 条：`nanHandling` 的杠杆效力与字段缺失率成正比。** cov = 1.0 的字段（mdl28）开关它读数为零差异；覆盖中等的字段（analyst 的 forward_pe）ON 甚至有害。⇒ **先查字段 cov，再决定是否把 nanHandling 当杠杆**；不要把「季频字段要开 nanHandling」当全域规则。
- **第 137 条：提 S 与提 2Y 在设置层是冲突目标。** INDUSTRY 轴把 returns 从 5.57% 提到 8.76%、F 从 1.07 提到 1.23，同时把 2Y 从 1.58 打到 1.29。**换轴的收益必须按「你要破的是哪个闸」来评，不存在同时优化 S 与 2Y 的设置。**
- **第 138 条：`ts_target_tvr_decay` 骨架下，STATISTICAL 是 2Y 的最优中性化轴。** 该算子在表达式内已做换手平滑，外层再用换手型/流动性型中性化（FAST / SLOW_AND_FAST）会叠乘平滑、把信号削平（S 掉到 1.08–1.20）。
- **第 139 条：判「2Y 能否修」不看差距大小，看「当前轴是否已是 2Y 最优轴」。** `mL68wNOK` 差距 0.00 却是最死的 —— 因为 STATISTICAL 已是五档最优。反过来若当前用的是 FAST 而 2Y 差 0.1，就有明确路径。⇒ **修 2Y 的第一步永远是先扫中性化轴（4 条回测），拿到 2Y 排序再决定是否继续投入**；若当前轴已居首，立即封盘，不要试 decay / truncation。

## 17.6 GBR 最终收口账（本战役）

| 项 | 条数 | 明细 |
|---|---:|---|
| 冻结篮 **RA 层**全闸通过 | 15 | `P0gvv5gE` `d51O1kOX` `O0AKLMKq` `vR1aEpa3` `rKRkL9QE` `wp9m9MW1` `MPYlNP8z` `pwdQb78v` `E56onL5r` `0mYoANkv` `MPYq0819` `WjOkLGWx` `9qWwZ3go` `6XKwmQgE` `RR62bMje` |
| **10-31 prod 全量 refresh 后可提** | **8** | `vR1aEpa3` `O0AKLMKq` `rKRkL9QE` `0mYoANkv` `MPYq0819` `P0gvv5gE` `WjOkLGWx` `9qWwZ3go`；**7 条漂死**：`d51O1kOX` **1.0** / `wp9m9MW1` **0.999** / `RR62bMje` **0.998** / `6XKwmQgE` 0.9633 / `MPYlNP8z` 0.9573 / `pwdQb78v` 0.7205 / `E56onL5r` 0.7033（5 条生产池克隆级，漂移窗口 ≤5 天） |
| 未点亮塔新候选 | **0** | `leA23Jae` prod **0.7445** ❌ / `QPvj9m0K` prod **0.7044** ❌ 双双卡生产池相关性 ⇒ 该族封盘（见 **§18**） |
| **可提合计** | **8** | 与旧包 `leAJn9e2`（prod 0.5507）二选一后仍 8 条（互相关 0.8493，见执行包 §7.1）；距 60 条目标差 **52 条** |
| 卡 2Y 判死 | 3 | `mL68wNOK` / `GrOMbGO5` / `3qV7Q2dO` |
| 未点亮塔已测 / 全灭 | 17 集 | 9 塔，仅 shortinterest3 产出 |

**⇒ 60 条在 GBR 未点亮塔内结构性达不到**（§15.2 已给算术）。本条不再重复论证。

---

*§17 写于 2026-10-31，基于 wave `s2_fix2y_settingaxis_d1` 的 6 条新回测（A1VbxnAw / VkxENXW5 / 9qxKl3we / A1VbxmJE / WjOdl0Jj / 3qox0KRO）。修压线 2Y 这条线至此封盘。*

---

# 18. ★★★ E3 引擎（days-to-cover）prod 封盘（2026-10-31，覆盖 §12 的「全闸通过」表述）

**§12 只说对了一半**：E3 引擎在 **IS/RA 层**确实是本战役唯一突破（S 1.71–1.72 / 2Y 2.60–2.73 / dd 5.6–6.9%），但**它在生产池相关性层整枝死掉**。本节是权威结论，与 §12 冲突处**以本节为准**。

## 18.1 实测值

```
check_correlation(leA23Jae, production) → 0.7445  ❌  (attempts=38, 49.3s)
check_correlation(QPvj9m0K, production) → 0.7044  ❌  (attempts=4,   4.1s)
leA23Jae self                          → 0.1034  ✅  (池 19 条，排除 4 条 PPAC)
```

## 18.2 直方图与「为什么不能靠换窗口救」

| alpha | ADV 窗 | prod | `n([0.7,0.8))` | `n([0.6,0.7))` |
|---|---:|---:|---:|---:|
| `leA23Jae` | 22 | 0.7445 | **1** | 4 |
| `QPvj9m0K` | 126 | 0.7044 | **1** | 14 |

按 `wq-window-valley-break-prod-wall` 的前置判据（实证 16/16 零例外）：

| `n([0.7,0.8))` | 判定 |
|---|---|
| **0** | 族内存在过线窗口 ⇒ 可扫窗口网格找谷 |
| **≥ 1** | **单钉子卡死**，调 W 无效 ⇒ **弃，别扫窗口** |

两条都是 **n = 1** ⇒ 判「单钉子卡死」。旁证：该 skill 记录 n=1 族的谷底**永远卡在 0.7019–0.7031**，本次 `QPvj9m0K` = **0.7044** 正落在同一窄带。

**而且「换窗口」已经实际试过一次**：ADV 22 → 126，prod 仅从 0.7445 降到 0.7044（−0.04），仍越线。继续沿 `ts_rank` 的 W 扫只是在同一条钉子周围打转。

## 18.3 封盘裁定与对后续挖掘的约束

1. **本族 0 颗可提**。可提总数由 16 修正为 **15**（同日 prod 全量刷新后进一步落定 **8**，见 §17.6）。
2. **塔位影响为零**：SHORTINTEREST 需 3 条才点亮，本族最多只能供 1 条 ⇒ 边际塔位收益本来就是 0；PV 增量由 1→9 修正为 **1→8**（PV、FUNDAMENTAL 两座塔仍点亮）。
3. **不要再用「换窗口 / 换 ADV 窗 / 换 ts_rank 的 W」重开此族** —— 已被 n=1 判据 + 一次实际窗口切换双重否决。
4. **重开的唯一合规路径 = 换字段或换几何**（例如换另一个借贷字段做分子、或换分母为 `sharesout` / 市值），且**必须先跑一次 prod 直方图看 `n([0.7,0.8))`**，n≥1 就立刻放弃，省掉整轮回测。
5. **§12.2 的「★ 全闸通过」应读作「IS/RA 全闸通过，prod 未测」** —— 这也是本战役最大的流程教训：**prod 未测 = 未定，不是「大概能过」**。

## 18.4 篮内互相关（同日实测，配套结论）

`compute_mutual_correlation(17 ids, threshold=0.7, years=4)`，1021 个交易日：

- 136 对里**只有 1 对 ≥0.7**（`leA23Jae`↔`QPvj9m0K` 0.8469），其余全在线下。
- `max_mutually_below_subset` = **16 条**，`max_subset_exact = true` ⇒ 16 条是 0.7 阈值下的**数学最大篮**。
- 但有两对贴线，属**提交顺序风险**：`vR1aEpa3`↔`E56onL5r` = **0.6954**（余量 0.0046）、`MPYlNP8z`↔`pwdQb78v` = **0.6868**（余量 0.0132）⇒ 必须相邻提交并立即读回平台自相关。

**★ 同日后续（prod 全量 refresh，覆盖上列数字的最终状态）**：15 条中 7 条漂死 ⇒ 实际可提篮 = **8 条**；上列两条贴线对**因对方漂死自动消解**；9 活口重核后唯一超线对为跨包 `O0AKLMKq`↔`leAJn9e2` = **0.8493**（二选一，取谁都是 8 条，`max_subset_exact=true`）。详见执行包 `gbr_submit_execution_pack_campaign16_20261031.md` §4.1 / §7.1。

---

*§18 写于 2026-10-31，为 E3 引擎的最终封盘记录。台账键 `shortinterest3_family_sealed_20261031`、wave `s2_shortinterest3_prod_verify_d1`。*
