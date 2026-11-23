# insiders1 模板族设计（EUR / TOP2500 / D1）—— 未满塔 INSIDERS 剩 1 席

> 数据集：`insiders1`（9 字段 · 全 VECTOR · cov 0.5512 · INSIDERS 塔 2/3）
> 采集：2026-11-22（本轮此前未测，属遗漏补齐）
> 历史：11-20 会话做过算子全替换（基线 S1.01/F0.52/2Y1.30，16 个同类别替换全劣）；
> 11-13 判 insd1_valueeur 符号随配置翻转 ⇒ 信号层死的旧结论（**需用本族矩阵复核**）

## 字段清单（9/9）

| 字段 | aC | 语义 | 可用性判据 |
|---|---:|---|---|
| `insd1_valueeur` | 428 | 交易金额（欧元） | ✅ 核心流量 |
| `insd1_shares` | 549 | 交易股数 | ✅ 流量 |
| `insd1_holdings` | 462 | 交易后持股总量 | ✅ **存量（流量÷存量的分母）** |
| `insd1_tradesignificance` | 381 | 交易显著性 1–3 | ✅ 权重 |
| `insd1_price` | 462 | 交易价 | ⚠ 价格类，易与 PV 混 |
| `insd1_value` | 262 | 原币金额 | ⚠ 同 valueeur |
| `max_trade_price` | 41 | 区间上限价 | ⚠ 稀疏 |
| `transaction_currency_code` | 65 | 货币码 | ⛔ 分类变量 |
| `insd1_gvkey` | 576 | 公司 ID | ⛔ 标识符 |

## 5 个结构互异模板族（族级定义见 template_family_exhaustion_20261122.md）

### T1 · B 流量÷存量（历史基线，最核心）
```
rank(group_scale(tail(winsorize(group_zscore(
  ts_sum(divide(multiply(vec_sum(insd1_valueeur), vec_avg(insd1_tradesignificance)),
                  vec_sum(insd1_holdings)), 44),
  industry), std=2), lower=0.25, upper=0.75, newval=0.5), industry))
```
- 机制：内部人**净买入占其持仓的比例**（流量/存量）⇒ 增持强度
- 历史读数：S1.01 / F0.52 / 2Y1.30（算子轴已穷尽，16/16 替换更差）

### T2 · H 累积水平（不做时序标准化）
```
group_rank(ts_sum(multiply(vec_sum(insd1_valueeur), vec_avg(insd1_tradesignificance)), 63), industry)
```
- 机制：**绝对**买入金额累积（不除以持仓）⇒ 大额内部人交易
- 与 T1 的区别：T1 是相对强度（小公司也能上榜），T2 是绝对规模（偏大票）

### T3 · E 事件密度（笔数）
```
group_rank(ts_sum(vec_count(insd1_valueeur), 63), industry)
```
- 机制：内部人**申报笔数**（关注度/一致性）⇒ 多人同时交易 = 强信号
- 与 T1/T2 的区别：不计金额，只看人数/频次

### T4 · R 相对自身历史（时序 z）
```
group_rank(ts_zscore(ts_backfill(divide(vec_sum(insd1_shares), add(vec_sum(insd1_holdings), 1)), 22), 252), industry)
```
- 机制：股数占比相对自身一年历史的标准分 ⇒ 异常增持
- ⚠ 11-13 曾判「insd1 族 ts_rank/ts_zscore 全灭」，本族用**占比**（非裸值）重测

### T5 · P 显著性加权分位
```
group_rank(ts_sum(multiply(vec_avg(insd1_tradesignificance), vec_count(insd1_valueeur)), 63), industry)
```
- 机制：显著性 × 笔数（高显著性多笔 = 高管集体行动）
- 与 T3 的区别：给高管交易（sig=3）更高权重

## T6（备） · X 买卖双向分离
```
group_rank(ts_sum(vec_sum(insd1_shares), 63), industry)   # 仅股数流向（sign 由平台 vector 语义决定）
```

## 派批纪律

- **先跑 1 臂字段存在性探针（T3 的 vec_count）**：确认 `vec_count` 在该 VECTOR 字段上可用且 TO>0
- 每族首波 1 臂；有效族（|S|≥1.0）再做完整梯度（同类别算子全替换 + 参数档位）
- 塔位：INSIDERS 2/3（剩 1 席）⇒ 本集最多交 1 颗

## 已知风险

1. 11-13 判「insd1_valueeur 符号随配置翻转 ⇒ 信号层死」⇒ T1/T2 需先做**符号一致性检验**（3 配置）
2. 11-20 算子全替换 16/16 劣 ⇒ 说明 T1 的 ts_sum 是最优实现，**算子轴不必再扫**
3. `insd1_price` / `max_trade_price` 属价格类，与 PV 语义重叠 ⇒ 不作为单独族
