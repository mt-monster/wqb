# KOR wave96 特征工程文档（REGULAR 战役 2026-09-01）

## 战役背景
- 目标：KOR 区域 20 个可提交 REGULAR alpha（停止闸 20，非默认 4）
- 本波定位：**未点亮金字塔数据集的单字段探针波**——intraday_pv_feats（PriceVolume 类）/ risk59（Risk 类）/ shortinterest38（Short Interest 类）/ mmp_nlp_sentiment（News 类）
- 数据源：DB typed catalog（scan_fields 扫描入库），覆盖/竞争度来自平台实时体检（S0）

## 字段理解（S1）

### intraday_pv_feats（PriceVolume，MATRIX 型，覆盖 0.99）
- `avg_bid_to_ask_price_ratio_last_half`：收盘后半段 bid/ask 比值 → 收盘段买压强度（价差收窄=买盘主导）
- `avg_ask_price_to_vwap_ratio_first_half`：早盘卖价相对 VWAP 溢价 → 卖方报价溢价（溢价高=卖压）
- `avg_bid_price_to_vwap_ratio_first_half`：早盘买价相对 VWAP 折价 → 买方报价力度
- 预处理：MATRIX 字段可直接 rank；无需 vec_* 包裹
- 竞争度：alphaCount 近零（未点亮），信号新鲜

### risk59（Risk/S3 借贷卖空，VECTOR 型 16 字段，覆盖 0.98）
- `rsk59_short_momentum`：做空/回补动量（相对流通盘），alphaCount=9 低竞争
- `rsk59_squeeze_risk`：S3 多因子轧空风险评分，alphaCount=49
- 预处理：VECTOR 字段必须先 vec_avg 聚合再套 rank（KOR 约束铁律）
- 经济学意义：借贷市场拥挤度 → 轧空/回补行情

### shortinterest38（Short Interest，VECTOR 82 + MATRIX 6，覆盖 0.96-1.0）
- `shrt38_stk_short_sellshort_sell_amt_wgt`：KRX 日度卖空额权重（6 α 低竞争）
- `shrt38_stk_invactnet_buy_qty`：机构净买入量（83 α 中等竞争）
- 预处理：VECTOR 需 vec_avg；组内相对信号用 group_rank(…, sector)
- 经济学意义：卖空占比=空头压力；机构净买=聪明钱流入

### mmp_nlp_sentiment（News 情绪，MATRIX 80 字段）
- `avg_bullish_topic_score`：主题看涨情绪均值
- ⚠️ 跨区教训：KOR 新闻情绪聚合存在死路风险（GLB emotion 死路族），本波仅作 1 槽探针
- 预处理：稀疏事件流 → ts_backfill(5) 填充 + trade_when 门控（SPARSE-EVENT-CONCENTRATED-WEIGHT 配方）

## 特征工程建议（S2 候选池）

### 初始信号（单字段裸探针，测信号有无）
1. `rank(avg_bid_to_ask_price_ratio_last_half)` — 收盘段价差压力
2. `-rank(avg_ask_price_to_vwap_ratio_first_half)` — 早盘卖价溢价
3. `rank(vec_avg(rsk59_squeeze_risk))` — 轧空风险评分
4. `rank(vec_avg(shrt38_stk_invactnet_buy_qty))` — 机构净买

### 进阶信号（骨架升级，满足闸6 契约 + 经济机制）
5. `bucket(rank(avg_bid_price_to_vwap_ratio_first_half), 5)` — 早盘买力分桶（bucket 注入）
6. `if_else(rank(vec_avg(rsk59_short_momentum)) > 0.7, rank(vec_avg(rsk59_squeeze_risk)), 0)` — 空头加速时赌轧空（event_gated）
7. `-group_rank(vec_avg(shrt38_stk_short_sellshort_sell_amt_wgt), sector)` — 行业内相对卖空（group 骨架）
8. `trade_when(rank(ts_backfill(avg_bullish_topic_score, 5)), rank(ts_backfill(avg_bullish_topic_score, 5)) > 0.5, 0)` — 情绪事件门控（trade_when）

### 预处理决策汇总
| 字段类型 | 处理 | 依据 |
|---|---|---|
| MATRIX | 直接 rank | kor_preflight 实证 |
| VECTOR | vec_avg 聚合后 rank/group_rank | 约束铁律 |
| 稀疏事件流 | ts_backfill + trade_when | SPARSE-EVENT-CONCENTRATED-WEIGHT |

## 建议（S3 回测后）
- 按数据集分别统计 IS Sharpe：|S|≥1.0 的字段进近池，<0.5 不占槽
- risk59 与 shortinterest38 同属卖空族，若两条腿同时强 → 检查互相关系数，防族内自食
- mmp_nlp_sentiment 探针若 Sharpe 差 → 标记死路候选（KOR 新闻情绪聚合族）
