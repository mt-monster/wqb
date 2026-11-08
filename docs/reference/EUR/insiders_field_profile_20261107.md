# EUR / Insiders 字段画像（3 数据集全量梳理）· TOPCS1600 / D1

- 采集时间：2026-11-07｜采集口径：`get_datasets(region=EUR, universe=TOPCS1600, delay=1)` → 逐集 `get_datafields(filter_sharpe=false, max_fields=200)`
- **EUR 全平台仅 3 个 Insiders 数据集**（分母来自平台全表，不是本地 `field_coverage` 缓存）；EUR/D1 其它类计数对照：pv 20 / model 46 / other 36 / news 20 / fundamental 13 / analyst 16。

## 1. 三集总览

| 数据集 | 名称 | 字段 | 类型 | 覆盖率 | alphaCount | userCount | 判决倾向 |
|---|---|---|---|---|---|---|---|
| `insider_agg_matrix` | Smart Insider Transaction Aggregates | 34 | **全 MATRIX** | **0.6083–0.6149** | 165 | 78 | **主战场**（有显式买/卖拆分 + 四档角色 + 显著性分层） |
| `insiders1` | Global Insider Trading Data | 9 | 全 VECTOR | 0.5512 | 393 | 190 | 次选（**无显式买卖方向字段**，方向需实测推断） |
| `insiders12` | UK Insider Transaction Data | 8 | 全 VECTOR | **0.1925–0.2592** | 201 | 113 | 第三（仅 UK，cov 0.19 ≪ 0.85 结构线） |

> ⚠ 覆盖率口径注意：平台 `coverage` 是「该字段在全集上的可用比例」的粗聚合，**不等于每天有值的股票占比**（对照实证：`analyst45` 报 cov=1.0，实际每天仅 4–5% 的股票有活跃构想）。三个 insiders 集都属**稀疏型**，必须按「有值股票占比」再做一次行为学核验，方法见 §4。

## 2. `insider_agg_matrix` 字段解剖（34 字段，全 MATRIX ⇒ 无向量语义障碍）

### 2.1 主轴 A：角色档（4 档，从上到下信息含量递增）
| 档 | 买入 | 卖出 | 含义 |
|---|---|---|---|
| 全体董事 | `total_buy_shares` / `avg_buy_shares` | `total_sell_shares` / `avg_sell_shares` | 最宽口径 |
| 董事直持 | `total_secondary_buy_shares` / `avg_secondary_buy_shares` | `total_secondary_sell_shares` / `avg_secondary_sell_shares` | 直接持有（排除间接/信托） |
| 高管直持 | `total_secondary_top_buy_shares` / `avg_secondary_top_buy_shares` | `total_secondary_top_sell_shares` / `avg_secondary_top_sell_shares` | 高管 + 直接持有，**最严口径** |
| 全体高管 | `total_top_buy_shares` / `avg_top_buy_shares` | `total_top_sell_shares` / `avg_top_sell_shares` | 高管（含间接） |

### 2.2 主轴 B：矩（合计 vs 均值）
`total_*` = 股数**合计**（规模口径）｜`avg_*` = **平均**每笔股数（单笔规模口径）。
> **推导量**：`total_* ÷ avg_*` = **参与的内部人数（隐含计数）**。这是该数据集唯一能拿到「广度」的路径，而广度是内部人文献里最重要的维度之一（多数人买 > 单人大买）。

### 2.3 主轴 C：方向与显著性（平台自带）
- `directional_indicator` / `directional_indicator_2`：平台自算的「内部人活动整体方向/偏置」指标（后者为增强版）。
- `significant_value_1..4`：第 1–4 大显著交易的价值（降序）。
- `directional_significant_value_1..4`：方向性显著交易中的第 1–4 大值。
- `top_significant_value_1..4` / `top_directional_significant_value_1..4`：高管口径的同构序列。
> 三个 `*_significant_value_*` 家族互相构成「显著性梯度」与「角色梯度」，可做差（大单相对第 2 大单的支配度）与角色背离。

## 3. `insiders1` / `insiders12` 字段与致命缺口

### insiders1（9 字段全 VECTOR）
`insd1_value` / `insd1_valueeur`（交易总额，欧元口径可直接跨市场比较）｜`insd1_shares`（股数）｜`insd1_price`（每股价，区间取最小值）｜`max_trade_price`｜`insd1_holdings`（交易后持股）｜`insd1_tradesignificance`（**1=低 / 3=高** 显著性评分）｜`insd1_gvkey`（公司标识）｜`transaction_currency_code`。
> **致命缺口：没有买卖方向字段**。方向必须靠实测推断（见 §4 诊断 3）。这是它虽然 alphaCount 393 却难以做出干净 ATOM 的结构性原因。

### insiders12（8 字段全 VECTOR，仅 UK）
`insd12_positionchangetransactionamount`（**带符号**：买入 (+) / 卖出 (−)）｜`insd12_transactioncode`（交易类型码）｜`insd12_percent`（交易后持股比例）｜`insd12_sharesheld`｜`insd12_mktprice`｜`option_exercise_price_eur/gbp/reported`（3 个期权行权价，**alphaCount 全 0，零人用过**）。
> 唯一有**显式符号**的字段是 `positionchangetransactionamount`；但 cov 0.19 且 UK-only ⇒ 在 EUR 宇宙里最多覆盖约 1/5，sub 宇宙闸结构性不可达（除非 EUR 宇宙几乎全 UK）。

## 4. 三个必须先做的诊断（决定后续一切）

1. **覆盖注入诊断（最高优先级）**：`insider_agg_matrix` cov 0.61 ⇒ **约 39% 的股票无内部人数据**。若 `nanHandling ON` 把这批填 0，经中性化后它们会变成**系统性空头**，alpha 内容被替换成「有没有内部人交易」这个流动性/规模代理。
   - 判据：跑一条正负对称骨架看 `longCount/shortCount`；比例严重失衡即命中。
   - **这与论坛结论高度吻合**：论坛帖《高管买入还是买压本身？》在同源姊妹集上用 `total_top_buy_shares/total_buy_shares/total_top_sell_shares` 做「内部人异常买入」，被自己的对照组证伪，并称该数据集「几乎无人生还」——最可能的解释就是所有人都在 `nanHandling ON` 下把 39% 的无覆盖股票做成了空头。
2. **历史深度**：目标要求「近十年都要有数据」。`insider_agg_matrix` 的 cov 0.61 是否由「某些年完全无数据」造成，必须用 `get_alpha_yearly_stats` 逐年 `longCount>0 && pnl≠0` 核验，**不得用汇总 S/F/2Y 代替**。
3. **`insiders1` 方向诊断**：对 `insd1_value` 取 `vec_min` 与 `vec_max`，看是否出现负值区间；若全为正则该字段不带方向，只有 `insd1_tradesignificance` 与持股变化能间接定方向 ⇒ 该集大概率无法做干净的方向 ATOM。

## 5. 文献与论坛证据映射

| # | 机制 | 来源 | 对应字段 |
|---|---|---|---|
| 1 | 内部人**净买入**（不是买入总额）预测收益；买入比卖出更有信息量 | **Lakonishok & Lee (2001), RFS, "Are Insider Trades Informative?"** | `total_buy_shares` / `total_sell_shares` 的比值 |
| 2 | 交易规模越大越有信息量；内部人是信息交易者 | **Seyhun (1986, JFE; 1998)** | `avg_*_shares`、`significant_value_1..4` |
| 3 | **常规（routine）vs 机会型（opportunistic）** 内部人交易；只有机会型预测收益 | **Cohen, Malloy & Pomorski (2012), JF, "Decoding Inside Information"** | 需要「与自身历史模式的偏离」⇒ `ts_zscore` / `ts_delta` |
| 4 | 内部人买入组合获得显著超额收益 | **Jeng, Metrick & Zeckhauser (2003), REStat** | 净买入比率 × 广度 |
| 5 | 「异常买入」可能只是**买压本身**；对照组可证伪 | 论坛《高管买入还是买压本身？》（同源 `insider_agg_matrix`，GLB） | 需与 `ts_mean(净买入,66)` 做基线对照 |
| 6 | `net_buy` 类字段换手可高达 ~117%，需分层治理 | 论坛《高换手率的分层治理——net_buy 类字段 117% 换手的驯服记录》 | 影响 `ts_mean`/`decay`/`hump` 选档 |

## 6. 已知与未知（诚实边界）

- **已知**：三集字段全集与类型；cov 读数；alphaCount/userCount 拥挤度；`insider_agg_matrix` 是唯一有显式买卖拆分且无向量语义障碍的集。
- **未知**：① 三集的真实「每日有值股票占比」；② 历史起止年份；③ `directional_indicator` 的符号约定（正=买入还是净卖出）；④ `*_significant_value_*` 是否带符号；⑤ `insiders1` 的方向编码方式。以上五项都要靠首批回测与逐年读数回答，不得凭字段名假定。

