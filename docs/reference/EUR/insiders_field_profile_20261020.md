# EUR × Insiders 类别 — 字段画像与回测档案

> 日期：2026-10-20 ｜ 目标：10 个 regular alpha（最好 ATOM）｜ 设置：TOPCS1600 / SUBINDUSTRY / decay4 / trunc0.08 / maxTrade ON / nanHandling ON（区域缺省）
> 纪律：full-coverage（字段 100% 覆盖 / 模板族 ≥3 / 边界算子档穷举），三道覆盖闸已过

## 一、数据集全量清单（平台 EUR/TOPCS1600 实时枚举）

| ID | 名称 | 字段 | 覆盖 | 已有alpha | valueScore | 金字塔倍率 |
|---|---|---:|---:|---:|---:|---:|
| insider_agg_matrix | Smart Insider Transaction Aggregates | 34 | 0.612 | 156 | 2.0 | 1.1 |
| insiders1 | Global Insider Trading Data | 9 | 0.551 | 393 | 2.0 | 1.1 |
| insiders12 | UK Insider Transaction Data | 8 | 0.201 | 201 | 2.0 | 1.1 |

**合计 51 字段，全部实测覆盖（34/34 + 9/9 + 8/8 = 100%）**

## 二、字段画像

### 2.1 insider_agg_matrix（34 字段，全 MATRIX，cov 0.612）
| 维度 | 字段 | 经济含义 | 实测结论 |
|---|---|---|---|
| **D1 总买入股数** | total_buy_shares / total_top_buy_shares / total_secondary_buy_shares / total_secondary_top_buy_shares | 全体董事 / 高管 / 直接 / 直接高管 买入总量 | 净价差 S 0.26–0.36（弱） |
| **D2 总卖出股数** | total_sell_shares / total_top_sell_shares / total_secondary_sell_shares / total_secondary_top_sell_shares | 同上（卖出） | 同上 |
| **D3 均买入** | avg_buy_shares / avg_top_buy_shares / avg_secondary_buy_shares / avg_secondary_top_buy_shares | 单笔平均规模 | 均笔/总量比 S −0.39~0.44 |
| **D4 均卖出** | avg_sell_shares / avg_top_sell_shares / avg_secondary_sell_shares / avg_secondary_top_sell_shares | 同上（卖出） | 同上 |
| **D5 方向指标** | directional_indicator / directional_indicator_2 | 整体方向偏置 | S −0.28~−0.06 |
| **D6 方向显著值** | directional_significant_value_1..4 | 按显著度排序的**带方向**交易额 | ★ **过稀疏 → no-alpha**（仅重大方向性交易日有值） |
| **D7 显著值** | significant_value_1..4 | 最显著交易额（不分方向） | S 0.08–0.36 |
| **D8 高管方向显著值** | top_directional_significant_value_1..4 | 高管版 D6 | ★ **过稀疏 → no-alpha** |
| **D9 高管显著值** | top_significant_value_1..4 | 高管版 D7 | S 0.08–0.36 |

**更新频率**：日频快照，但有效值只在内部人交易发生时更新（大量重复值）→ 需 ts_backfill。
**分布特征**：右偏（交易额/股数长尾），极端值集中在大额交易。
**可用性**：cov 0.612 ⇒ 39% 宇宙无数据，sub/robust 天然受限。

### 2.2 insiders1（9 字段，全 VECTOR 事件型，cov 0.551）
| 字段 | 经济含义 | 实测结论 |
|---|---|---|
| **insd1_shares** | 交易股数 | ★★ **`vec_sum` = 内部人交易总股数 → S 0.80 / F 0.88 / 2Y 1.52 / ret 17.6%（全类别最强）** |
| **insd1_gvkey** | Compustat 公司 ID | ★★ **`vec_sum` = 交易笔数（ID 求和即计数）→ S 0.70 / 2Y 1.49** |
| insd1_valueeur / insd1_value | 交易金额（欧元/原币） | `vec_sum` S 0.31–0.77 |
| insd1_tradesignificance | 交易显著度（1=低） | `vec_sum` S 0.08–0.7 |
| insd1_holdings | 交易后内部人持股 | ★ **作分母方向相反**（持股多=仓位重=低换手）⇒ divide 形式 S 负 |
| insd1_price / max_trade_price | 成交价 | `vec_sum` 价格无信号（价格水平） |
| transaction_currency_code | 币种代码 | 分类字段，仅可 vec_count |

**⚠ 平台约束（实测报错）**：**VECTOR 事件型字段不支持 `multiply`**（`multiply(insd1_shares, insd1_price)` → `Operator multiply does not support event inputs`）⇒ 无法在事件层算「股数×价格」；只能先 vec_* 聚合再运算。

### 2.3 insiders12（8 字段，VECTOR，cov 0.19–0.26，UK 专属）
| 字段 | 经济含义 | 实测结论 |
|---|---|---|
| **insd12_positionchangetransactionamount** | **带符号净持股变动（买+ / 卖−）** | `vec_sum` S −0.76；stack 后 S 0.67 / 2Y 0.86 |
| insd12_percent | 交易后内部人持股比例 | `vec_avg` S −0.11 |
| insd12_sharesheld | 交易后持股数 | S −0.57 |
| insd12_mktprice | 市场价 | S −0.15 |
| insd12_transactioncode | 交易类型代码 | 分类字段 |
| option_exercise_price_{reported,eur,gbp} | 期权行权价 | S −0.22~−0.46 |

**覆盖限制**：cov 0.19（UK 股票仅占 EUR 宇宙小部分）⇒ 信号作用面窄，实测全弱。

## 三、适用模板（按字段类型匹配）

| 字段类型 | 模板 | 表达式骨架 | 实测 |
|---|---|---|---|
| VECTOR 事件型 | **聚合**（唯一入口） | `vec_sum(F)` / `vec_avg(F)` / `vec_count(F)` | ✅ 有效 |
| VECTOR 事件型 | 聚合后标准化 | `signed_power(ts_zscore(ts_backfill(vec_sum(F), 66), 126), 1.5)` | S 0.31（不如裸 vec_sum） |
| VECTOR 事件型 | ❌ 事件层算术 | `vec_sum(multiply(F1,F2))` | ❌ 平台拒绝 |
| MATRIX 慢变 | 净价差（同源） | `subtract(rank(bf(buy,66)), rank(bf(sell,66)))` | S 0.26–0.36 |
| MATRIX 慢变 | 冠军栈 | `signed_power(ts_zscore(bf(F,66),126),1.5)` | S 0.08–0.36 |
| MATRIX 慢变 | 均笔比 | `divide(avg_F, add(total_F, 0.0001))` | S −0.39~0.44 |
| 聚合后矩阵 | 置信度组合 | `multiply(rank(vec_sum(股数)), rank(vec_sum(笔数)))` | 测试中 |

## 四、回测结果台账

| wave | 表达式 | S | F | TO | 2Y | sub | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| w740 | `vec_sum(insd1_shares)` | **0.80** | **0.88** | 0.145 | **1.52** | 0.73 | ★ 全类别最强，近 2Y 闸 |
| w740 | `vec_sum(insd1_gvkey)`（笔数） | 0.70 | 0.71 | 0.139 | 1.49 | 0.73 | ★ 次强 |
| w740 | `vec_sum(insd1_tradesignificance)` | 0.77 | 0.79 | 0.150 | 1.44 | 0.42 | 可用 |
| w740 | agg_matrix 净价差 4 条 | 0.26–0.36 | 0.07–0.12 | 0.04 | 0.16–0.41 | 0.25–0.67 | 弱 |
| w740 | agg_matrix 显著值 8 条 | 0.08–0.36 | — | 0.04–0.07 | 0.02–0.33 | 0.13–0.67 | 弱 |
| w740 | directional_significant_value 族 | — | — | — | — | — | **no-alpha（过稀疏）** |
| w743 | agg_matrix @ INDUSTRY/decay1 | 0.35–0.50 | 0.12–0.20 | 0.04 | 0.07–0.44 | 0.50–0.81 | 设置杠杆无效 |
| w744 | `rank(vec_sum(insd1_shares))` | 0.82 | 0.85 | 0.145 | 1.33 | 0.76 | 秩归一化 S +0.02 |
| w744 | `hump(rank(vec_sum(shares)),0.01)` | 0.83 | 0.87 | 0.145 | 1.34 | 0.74 | 同上 |
| w744 | `divide(vec_sum(shares), vec_avg(holdings))` | −0.00 | — | 0.17 | 0.78 | −0.12 | 方向反（持股=仓位） |
| w744 | `ts_zscore(vec_sum(shares),252)` | 0.61 | 0.52 | 0.155 | 1.37 | 0.63 | 不如裸聚合 |
| w745 | insiders12 全 8 字段 × 模板 | −0.76~0.67 | — | 0.01–0.03 | −0.99~0.86 | 负 | 全弱（覆盖 0.19） |

## 五、★ 归因记录（`vec_sum(insd1_shares)`，纪律要求）

| 年 | 14 | 15 | 16 | 17 | **18** | 19 | 20 | **21** | **22** | 23 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| S | −0.03 | 0.05 | 0.56 | 0.41 | **2.78** | 0.19 | 1.18 | **−0.32** | **2.24** | 0.51 |
| 收益 | −0.5% | 1.1% | 10.8% | 11.5% | **40.7%** | 2.5% | 29.9% | **−5.2%** | **75.8%** | 10.8% |

- **形态：事件聚集型**——收益集中在 2018（40.7%）与 2022（75.8%）两个高波动年，其余年份接近零
- **2Y（1.52）> 全样本（0.80）** ⇒ 信号在近期变强，与 pv87 修正族的衰减形态相反
- **诊断**：原始股数总额未归一化 ⇒ 危机年极端值主导 PnL，波动（~22%）盖过收益（17.6%）
- **修复方向**：规模×频次信心度组合（大额且多笔）、秩归一化后的组合

## 六、存档索引
- 字段全集：`tracking/EUR/reference/eur_insiders_fields.json`
- 覆盖闸候选：`tracking/EUR/candidates/insider_agg_matrix.json`
- 本文档：`docs/reference/EUR/insiders_field_profile_20261020.md`
