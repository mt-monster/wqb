# KOR D1 wave96 特征工程 Ideas（未点亮金字塔探针波）

> 生成：2026-09-01 | region=KOR | universe=TOP600 | delay=1
> 数据集：intraday_pv_feats（PV）/ risk59（Risk）/ shortinterest38（Short Interest）/ mmp_nlp_sentiment（News 情绪）
> 定位：REGULAR 战役 wave96 探针波——单字段裸探针 + 骨架升级，验证 4 个未点亮数据集的信号有无

## 1. 数据集理解

| 数据集 | 类别 | data_type | 字段数 | 覆盖 | alphaCount | 白名单档 |
|---|---|---|---|---|---|---|
| intraday_pv_feats | PriceVolume | MATRIX | 573 | 0.9925 | 187 | tier1 |
| risk59 | Risk | VECTOR | 16 | 0.9806 | 463 | tier2 |
| shortinterest38 | Short Interest | VECTOR 82+MATRIX 6 | 88 | 0.9953 | 1758 | tier2 |
| mmp_nlp_sentiment | News | MATRIX | 521 | 0.6187 | 10 | tier1 |

要点观察：
- intraday_pv_feats 为**日盘内微观结构**数据（bid/ask 与 VWAP 偏离、价差、量价相关），573 字段覆盖 0.99 且竞争极低（187 α），是 PriceVolume 金字塔少见的未饱和区
- risk59 为 **S3 借贷/卖空市场**数据（16 字段全部 VECTOR），短动量/轧空评分字段 alphaCount<50，低竞争
- shortinterest38 为 **KRX 交易所日度卖空 + 机构投资者分账户**数据（88 字段），覆盖 0.96-1.0，卖空额权重字段竞争极低（6 α）
- mmp_nlp_sentiment 为新闻 NLP 情绪（521 字段），KOR 覆盖 0.62、10 α——极度未点亮但有 GLB emotion 死路风险，仅作探针

## 2. 字段解构分析

### intraday_pv_feats（盘口微观结构）
- `avg_bid_to_ask_price_ratio_last_half`：**收盘段**（last half）bid/ask 平均比值。测的是收盘竞价期买卖盘报价收敛程度；比值高=买价贴近卖价=买盘主导收盘定价。时间维度：日内段快照聚合。逻辑：收盘价是次日锚点，收盘段买压强的股票次日惯性
- `avg_ask_price_to_vwap_ratio_first_half`：**早盘** ask 相对 VWAP 的溢价。测卖方报价激进程度；溢价高=卖方要价高于成交中枢=早盘卖压。逻辑：早盘卖压大 → 日内承压
- `avg_bid_price_to_vwap_ratio_first_half`：**早盘** bid 相对 VWAP 的折价。测买方报价强度；折价小=买方贴近中枢=买盘积极

### risk59（借贷市场拥挤度）
- `rsk59_short_momentum`：做空/回补动量（相对流通盘）。正=空头在加仓，负=空头在回补。事件型日度变化
- `rsk59_squeeze_risk`：S3 多因子轧空风险评分（short interest + float + loan liquidity 合成）。高=易被逼空。**逻辑**：轧空风险高 + 空头拥挤 → 正向收益（逼空行情）

### shortinterest38（KRX 卖空/机构流）
- `shrt38_stk_short_sellshort_sell_amt_wgt`：日度卖空额 / 总成交额权重。高=当日空头参与度高。**逻辑**：卖空占比极端化 → 反转（过度做空后回补）
- `shrt38_stk_invactnet_buy_qty`：机构账户（0100 系列）净买入量。**逻辑**：机构净买=聪明钱流入，韩国市场机构行为有持续性

### mmp_nlp_sentiment（新闻情绪）
- `avg_bullish_topic_score`：主题级看涨情绪均值。稀疏事件流（有新闻才更新）

## 3. 按问题类型分类的特征工程建议

### 3.1 稳定性特征（什么是不变的？）
- **收盘段价差收敛度**：`ts_std_dev(avg_bid_to_ask_price_ratio_last_half, 20)`——收盘段买卖价收敛的稳定性；稳定收敛=定价效率高
- **借贷利率平台期**：`ts_mean(vec_avg(rsk59_bid_rate), 60) > 0.05` 门控——借贷利率处于高位平台期的股票空头成本刚性

### 3.2 变化特征（什么在变化？）
- **卖空动量加速度**：`ts_delta(vec_avg(rsk59_short_momentum), 5)`——空头加减仓速度变化
- **机构净买趋势**：`ts_decay_linear(vec_avg(shrt38_stk_invactnet_buy_qty), 10)`——机构流入的平滑趋势

### 3.3 异常特征（什么是异常的？）
- **卖空占比极端化**：`-rank(vec_avg(shrt38_stk_short_sellshort_sell_amt_wgt))` 或分位数 `bucket(rank(...), 5)`——卖空极端时反转
- **轧空风险极端**：`rank(vec_avg(rsk59_squeeze_risk))`——高轧空风险+高空头=逼空候选

### 3.4 交互特征（什么被组合在一起？）
- **空头加速×轧空风险**：`if_else(rank(vec_avg(rsk59_short_momentum)) > 0.7, rank(vec_avg(rsk59_squeeze_risk)), 0)`——空头加速做空时，押注轧空风险高的股票（逼空机制）
- **机构买×卖空背离**：`ts_corr(vec_avg(shrt38_stk_invactnet_buy_qty), vec_avg(shrt38_stk_short_sellshort_sell_amt_wgt), 10)`——聪明钱与空头背离=信息优势方在反向

### 3.5 结构特征（什么是结构性的？）
- **行业内相对卖空**：`-group_rank(vec_avg(shrt38_stk_short_sellshort_sell_amt_wgt), sector)`——行业内相对做空强度（行业中性化）
- **行业内机构净买**：`group_rank(vec_avg(shrt38_stk_invactnet_buy_qty), sector)`——行业内部机构偏好差异

### 3.6 累积特征（什么是累积的？）
- **卖空压力累积**：`ts_sum(vec_avg(shrt38_stk_short_sellshort_sell_amt_wgt), 5)`——近 5 日累积卖空压力
- **情绪累积**：`ts_sum(ts_backfill(avg_bullish_topic_score, 5), 10)`——10 日累积看涨情绪

### 3.7 相对特征（什么是相对的？）
- **早盘 vs 收盘买卖强度对比**：`avg_bid_to_ask_price_ratio_last_half - avg_bid_price_to_vwap_ratio_first_half`——收盘买压相对早盘的变化（日内节奏信号）
- **早盘卖价溢价排名**：`-rank(avg_ask_price_to_vwap_ratio_first_half)`——早盘卖压的相对排名

### 3.8 本质特征（第一性原理）
- **买卖价差本质 = 交易成本与信息不对称**：`avg_ask_price_to_vwap_ratio_first_half - avg_bid_price_to_vwap_ratio_first_half`——价差=做市商对信息不对称的定价，价差收窄=信息透明期
- **轧空本质 = 强制回补需求**：短借利率 × 卖空占比——当 `vec_avg(rsk59_bid_rate) > 0.05` 且卖空占比高时，强制回补压力最大

## 4. 实现考量（wave96 实际采用）

| # | 表达式 | 特征来源 | 预处理 |
|---|---|---|---|
| 1 | `rank(avg_bid_to_ask_price_ratio_last_half)` | 3.1/3.8 收盘段买压 | MATRIX 直接 rank |
| 2 | `-rank(avg_ask_price_to_vwap_ratio_first_half)` | 3.7 早盘卖压 | MATRIX 直接 rank |
| 3 | `rank(vec_avg(rsk59_squeeze_risk))` | 3.3 轧空风险极端 | VECTOR→vec_avg |
| 4 | `rank(vec_avg(shrt38_stk_invactnet_buy_qty))` | 3.2 机构净买 | VECTOR→vec_avg |
| 5 | `bucket(rank(avg_bid_price_to_vwap_ratio_first_half), 5)` | 3.3 早盘买力分桶 | MATRIX 直接 bucket |
| 6 | `if_else(rank(vec_avg(rsk59_short_momentum)) > 0.7, rank(vec_avg(rsk59_squeeze_risk)), 0)` | 3.4 空头加速×轧空 | VECTOR→vec_avg；event_gated |
| 7 | `-group_rank(vec_avg(shrt38_stk_short_sellshort_sell_amt_wgt), sector)` | 3.5 行业内相对卖空 | VECTOR→vec_avg；group |
| 8 | `trade_when(rank(ts_backfill(avg_bullish_topic_score, 5)), rank(ts_backfill(avg_bullish_topic_score, 5)) > 0.5, 0)` | 3.6 情绪事件门控 | ts_backfill 稀疏填充；trade_when |

数据质量说明：
- risk59/shortinterest38 全 VECTOR：必须 vec_avg 聚合（约束铁律），禁 ts_backfill 直接作用 VECTOR
- mmp_nlp_sentiment 覆盖 0.62：稀疏事件流，ts_backfill(5)+trade_when 门控（SPARSE-EVENT-CONCENTRATED-WEIGHT）
- 覆盖与竞争：全部字段覆盖 ≥0.96（除情绪 0.62）；alphaCount 全部 <200（除 invactnet_buy_qty 83 中等）

## 5. 进一步探索的关键问题
- intraday_pv_feats 573 字段中还有 570 未探测——若本波 3 条有信号，值得扩 5 槽深挖盘口时段结构
- risk59 的 `rsk59_crowded_score`（9 α）/`rsk59_daystocover*`（35-95 α）是下波候选
- shortinterest38 的 `tot_amt_wgt`（21 α）/`accum_net_buy_*`（146-150 α）聚合窗口字段族可做窗口展开
- mmp_nlp_sentiment 若探针无信号 → registry 标记 KOR 新闻情绪聚合死路候选（与 GLB emotion 族对齐）
- 卖空族（risk59×shortinterest38）双腿若同时强 → 必须查互相关系数 <0.4，防族内自食（用户约束）
