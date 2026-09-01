# IND delay1 other315（Equity Swap Data）特征工程文档

- **数据集**: other315 Equity Swap Data（OTC 股权互换交易报告）
- **区域/延迟/域**: IND / delay1 / TOP500
- **类目**: Other（未点亮金字塔，alphaCount=417，userCount=225，valueScore=3.0，pm=1.4）
- **生成方式**: brain-data-feature-engineering skill（standalone），字段清单源 `db fields/IND/other315`（32 字段）
- **日期**: 2026-08-31

---

## 1. 数据集理解（字段）

### 1.1 数据结构要点

- **32 个字段全部为 VECTOR 事件型**：每条记录是一笔互换交易（trade 级），同一股票某时点可能有多笔 → 进常规算子前必须先 `vec_*` 聚合（vec_avg/vec_sum/vec_stddev/vec_max/vec_count），否则平台报 event inputs 不支持（other128 死路实证）。
- **coverage 0.7256 为历史累计覆盖**：交易报告是事件流，任意时点有效股票数可能远低于 490 → 必须 `ts_backfill(x,66)` 填洞 + 长窗 `ts_mean` 平滑，防 CONCENTRATED_WEIGHT 结构性 FAIL（跨区铁律 SPARSE-EVENT-CW）。
- **字段语义**：交易级互换合约条款——名义本金（notional）、期权费/行权价（premium/strike）、spread 融资成本、支付/重置频率（tenor 结构）、执行时间戳（信息新鲜度）、leg1/leg2 两腿对照。

### 1.2 字段分类（字段画像）

| 类别 | 字段 | 含义 | 预处理决策 |
|---|---|---|---|
| 名义本金（规模流） | active_notional_value_leg1, contract_notional_value_leg1/2, leg1/2_aggregate_notional_quantity, leg2_notional_value_on_effective_date | 合成敞口需求规模；active vs contract 差 = 新生成仓位 | vec_sum 聚合（总量）或 vec_avg；ts_backfill(66)+ts_mean 长窗 |
| 期权条款（凸性需求） | option_premium_value, option_strike_value, leg1/2_call_option_value, leg1/2_put_option_value | 杠杆/对冲凸性需求；call-put 差 = 方向性偏斜 | vec_avg；比率化（除以 notional）后 quantile |
| 融资成本（spread） | leg1_spread_value, leg2_spread_value | 合成持仓融资成本/对冲难度 | vec_avg；水平+变化双信号（ts_mean 66 水平、ts_delta 151 变化） |
| tenor 结构 | leg1/2_fixed_payment_period_count, leg1/2_floating_payment/reset_period_count, leg1/2_quantity_frequency_count | 合约久期/资金稳定性结构 | vec_avg；整数计数类用 rank 不用 ts_mean 过度平滑 |
| 价格条款 | contract_trade_price, package_trade_price_format, price_expression_format, transaction_currency_exchange_rate | 成交价/表达格式（格式类多为枚举，信号弱） | 枚举格式字段慎用；价格类与 strike 比值=虚实度 |
| 信息新鲜度 | oth315_execution_timestamp | 交易发生时间；最新交易距今 = 信息流活跃度 | vec_max 取最新；ts_delta 捕捉信息流突变 |
| 数量条款 | leg1/2_notional_quantity_value | 非货币名义量 | vec_avg × frequency 组合成流量 |

### 1.3 数据讲述的故事

OTC 股权互换是机构**合成多空敞口**的主通道：名义本金扩张 = 合成需求升温；spread 走阔 = 拥挤/对冲成本上升；期权费/名义比 = 杠杆投机强度；call-put 差 = 方向性偏斜；新交易时间戳跳变 = 知情资金进场。这些都是**未反映在公开价量里的场外资金流信息**，与 IND 已判死的新闻/模型分数族完全正交。

---

## 2. 特征工程建议（按问题驱动分类）

### 2.1 稳定性特征
- **tenor 稳定性**：`vec_avg(fixed_payment_period_count) - vec_avg(floating_reset_period_count)`。固定支付周期长、浮动重置频繁 = 稳定融资结构，吸引低风险资金。方向：long 高值。

### 2.2 变化特征
- **信息流新近度**：`ts_delta(vec_max(execution_timestamp), N)`。执行时间戳跳变 = 新交易开闸，短窗漂移。
- **spread 水平-变化分离**：`ts_delay(spread,151) - ts_mean(spread,66)`（成本改善信号，复刻 IND pv106 成本脆弱度 WIN 机制）。

### 2.3 异常特征
- **spread 离散度（脆弱度溢价）**：`vec_stddev(spread)/vec_avg(spread)`。同一标的多笔合约成本离散 = 对冲碎片化，成本脆弱度溢价的互换版本。

### 2.4 交互特征
- **期权杠杆比**：`option_premium / notional`。高凸性投入 = 杠杆投机需求，短期价格延续。
- **数量流量**：`notional_quantity_value × quantity_frequency_count`。名义量×频率 = 年化流量强度。

### 2.5 结构特征
- **leg 名义残差**：`leg1 notional - leg2 scheduled notional`。做市商方向性库存/对冲残余，资产负债表约束信号。
- **call-put 偏斜**：`call_option_value - put_option_value`（同腿/跨腿四组合）。方向性偏斜暴露。

### 2.6 累积特征
- **名义流量累积**：`ts_mean(backfill(vec_sum(notional)), N)` 长窗累积，衡量场外需求趋势。

### 2.7 相对特征
- **合约集中度**：`vec_max(notional)/vec_avg(notional)`。单笔大单主导 = 知情大玩家。
- 所有信号统一经 `quantile(...)` 截面分位 + `group_rank(...,industry)` 行业中性化，与 IND win 配方（anl9/pv106）对齐。

### 2.8 本质特征
- **场外合成敞口一阶矩**：互换市场的本质是"不想出现在持仓披露里的仓位"。名义本金、spread、期权费三者分别度量该隐性仓位的**规模、成本、凸性**——这是该数据集的第一性信号轴。

---

## 3. 实现约束与主辅信号分配建议

1. **每条表达式只用 1-2 个字段**（用户约束）；同数据集字段组合允许。
2. **VECTOR 必包**：`vec_*` → `ts_backfill(x,66)` → 常规算子；禁止裸字段进 rank（ERROR 连坐整批）。
3. **防 CW**：优先 `group_rank(ts_mean(...,N),industry)` 行业分组结构 + 长窗平滑；稀疏时点由组内相对排名稀释。
4. **主辅分配**：主信号（名义流/spread 成本）权重 ≥0.7；辅助腿（tenor 结构/新鲜度）只做降换手与抬 robust，禁止同信号调权重（用户纪律）。
5. **中性化**：首轨 STATISTICAL（settings.json 默认）；analyst 族实证 SUBINDUSTRY 最优，本集为事件流型，若 robust 卡墙可开 SUBINDUSTRY/SECTOR A/B。
6. **判死止损线**：批 1（8 条内）若全 |S|<0.7 且窗口无梯度（死墙判别法），直接判死换数据集，不恋战。

## 4. 风险与局限

- 交易报告频率不可知：若 IND 市场互换披露稀疏，任意时点有效股票可能 <100 → CW 风险高（需回测中看 longCount 验证）。
- 枚举/格式类字段（*_format）多为类别值，数值聚合意义弱，仅作陪跑。
- alphaCount=417 非零竞争：prod_corr 需回测后查，≥0.7 一律回 Mode B 换字段组合。
