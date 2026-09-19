# insiders1 Feature Engineering Analysis Report

**Dataset**: insiders1
**Region**: IND
**Delay**: 1

- **Dataset**: `insiders1`
- **Category**: `insiders`
- **Region**: `IND`
- **Delay**: `1`
- **Universe**: `TOP500`
- **Fields Analyzed**: 9

---

## 数据集画像（2026-09-11）

全球 insider 交易数据集，9 个 VECTOR 字段，coverage 0.3877（稀疏事件流，需 ts_backfill+trade_when 门控）。
信号核心：交易显著性(insd1_tradesignificance 1-3)、交易金额(insd1_value/valueeur)、交易股数(insd1_shares)、交易后持股(insd1_holdings)。
注意无 buy/sell 方向字段，信号靠显著性/金额强度/持股变化。users 145-265 偏高（prod_corr 风险，提交前必实测）。
IND 长窗结构区：慢变量基本面，长窗(≥250d)+大 decay(≥10)优先；scale(-rank) 语法用于方向反转型。
全部 VECTOR 字段必须先 vec_* 聚合。

## GEM 兼容模板（Concept Blocks）

> IND 长窗结构 insider 信号：机制 → 具体字段 → 一个实现。占位符用字段族后缀。
> 稀疏事件流必须 ts_backfill/trade_when 门控；长窗(≥250d)优先；scale(-rank) 用于方向反转。

**Concept**: insider 交易显著性强度（长窗累积）
- **Mechanism**: 高显著性 insider 交易长窗累积=公司内部人信心信号，强信号→long
- **Fields Used**: `insd1_tradesignificance`
- **Implementation Example**: `rank(ts_sum(vec_avg({insd1_tradesignificance}), 250))`
- **Direction**: High → long

**Concept**: insider 交易金额强度（长窗累积）
- **Mechanism**: 大额 insider 交易长窗累积=内部人真金白银投入，强信号→long
- **Fields Used**: `insd1_valueeur`
- **Implementation Example**: `rank(ts_sum(vec_avg({insd1_valueeur}), 250))`
- **Direction**: High → long

**Concept**: insider 持股变化（长窗动量）
- **Mechanism**: insider 交易后持股的长窗变化，增持累积=利好→long
- **Fields Used**: `insd1_holdings`
- **Implementation Example**: `rank(ts_delta(vec_avg({insd1_holdings}), 250))`
- **Direction**: High → long

**Concept**: 显著性×金额交互（强信号加权）
- **Mechanism**: 显著性加权的交易金额=高质量 insider 信号，强→long
- **Fields Used**: `insd1_tradesignificance`, `insd1_valueeur`
- **Implementation Example**: `rank(ts_sum(vec_avg({insd1_tradesignificance}) * vec_avg({insd1_valueeur}), 250))`
- **Direction**: High → long

**Concept**: insider 交易显著性行业相对（group_rank 中性化）
- **Mechanism**: 显著性在行业内相对定位，剥离行业 insider 活跃度差异
- **Fields Used**: `insd1_tradesignificance`
- **Implementation Example**: `group_rank(ts_sum(vec_avg({insd1_tradesignificance}), 250), subindustry)`
- **Direction**: High → long

**Concept**: insider 交易频率（长窗计数）
- **Mechanism**: insider 交易次数长窗累积=内部人活跃度，高频=信息优势→long
- **Fields Used**: `insd1_price`
- **Implementation Example**: `rank(ts_sum(vec_count({insd1_price}), 250))`
- **Direction**: High → long

**Concept**: 显著性反向（低显著性=噪声反转，scale(-rank) 语法）
- **Mechanism**: 低显著性交易是噪声，scale(-rank) 反转型结构
- **Fields Used**: `insd1_tradesignificance`
- **Implementation Example**: `scale(-rank(ts_sum(vec_avg({insd1_tradesignificance}), 250)))`
- **Direction**: Low（高显著性） → long（反向）

**Concept**: 交易金额 zscore 离群（截面异常）
- **Mechanism**: 交易金额截面 zscore 识别异常大的 insider 交易
- **Fields Used**: `insd1_valueeur`
- **Implementation Example**: `rank(zscore(ts_sum(vec_avg({insd1_valueeur}), 250)))`
- **Direction**: High → long

## 字段白名单（Field Whitelist）

```
insd1_tradesignificance
insd1_value
insd1_valueeur
insd1_shares
insd1_holdings
insd1_price
max_trade_price
```
