# EUR / INSTITUTIONS 面 机构持仓战役台账

日期：20261106｜区域：EUR TOP2500 D1｜category：INSTITUTIONS（塔位 0，需 3 颗点亮）

## 1. 为什么选这里（两次否决后的收敛）

1. **IND 的未点亮塔全部贫瘠**：earnings3 只有 8 字段且 alphaCount 7075、institutions6 alphaCount 9419、
   imbalance5 15559、socialmedia 无数据集、option 两个都 cov<0.55 ⇒ 构图空间为零，不值得投仿真。
2. **EUR 是全盘唯一厚实的未点亮点塔面**：6 个 category 停在 2（pv/other/risk/sentiment 各差 1 颗），
   未点亮塔里 institutions(0)/news(1)/insiders(1) 还有低拥挤数据集；EUR/PV 形态面已上轮封盘。
3. **机构持仓腿已被证实是强腿**：IND 最强的四颗（E5VNe67L S 3.20 / KPmvEYeE 3.07 / N1eLRWML 2.98 / kqNrvwA8 2.92）
   全部是 PV x INSTITUTIONS 组合；GBR 的 institutions4 单腿只有 0.24，配成 2:1 后到 1.84。
   ⇒ 机构持仓数据不是噪声，只是单腿弱、需要正确几何。本战役改为**单数据集内**做，避开塔混配额。

## 2. 数据集体检

| 数据集 | 字段 | 类型 | 覆盖 | EUR alphaCount | 内容 |
|---|---:|---|---:|---:|---|
| institutions6 | 11 | MATRIX | 0.9976 | 6 | 13F 式：持股金额/股数、持有人数、买家数/卖家数、买入/卖出金额与股数 |
| fund_holdings_panel | 30 | VECTOR | 0.843-0.918 | 3 | 基金层面板：HHI 集中度、持有账户数、边界交易（新建仓/清仓）、信念持仓、交易金额分布 |

要点：
- institutions6 全 MATRIX，**不需要 vec_avg**；fund_holdings_panel 全 VECTOR，**必须 vec_avg**（否则报 does not support event inputs）。
- 两个数据集在 EUR 的 alphaCount 只有 6 与 3，但同名字段在全球被用得很多（100-353）⇒ **本区低拥挤、机制本身已知有效**，
  正好落在「零拥挤不等于有信号」的补集上：这是「有信号但本区没人做」。
- `_active` 后缀版覆盖面更窄（0.843 vs 0.908），非必要不用。

## 3. 机制来源（论坛 + 论文）

- **Gompers & Metrick (2001), Institutional Investors and Equity Prices, QJE**：机构持股比例与股票收益正相关，
  机构持股是独立于规模/流动性的定价因素。
- **Bennett, Sias & Starks (2003), Greener Pastures and the Impact of Dynamic Institutional Preferences, RFS**：
  **机构持股的变动**（而非水平）预测未来收益，且变化可预测未来变化。
- **Sias (2004), Institutional Herding, RFS** 与 **Nofsinger & Sias (1999)**：机构羊群行为使需求冲击持续，形成收益可预测性。
- **Lakonishok, Shleifer & Vishny (1992), The impact of institutional trading on stock prices, JFE**：
  机构交易（尤其养老金）对价格有实质冲击，且冲击不立即完全反转。
- 论坛：IND/GBR 战役里 institutions6 的 `count_institutional_buyers - count_institutional_sellers` 已被反复用作强腿，
  说明「买卖家数差」是这批字段里最稳定的表达；本轮把它提到单数据集主腿来测。

## 4. 模板池（12 个结构互异模板）

| # | 模板名 | 信息维度 | 骨架要点 | 来源 | 状态 |
|---|---|---|---|---|---|
| T1 | 机构持股比例水平 | 水平 | 机构股数 / 全部股数 | Gompers-Metrick 2001 | 备料 |
| T2 | 机构买卖家数差（需求广度） | 变动广度 | buyers - sellers | Bennett-Sias-Starks 2003 | **已派发** |
| T3 | 机构净买入金额 | 变动金额 | acquired - disposed 市值 | 同上 | 备料 |
| T4 | 单持有人平均持仓（信念强度） | 强度 | 机构持股市值 / 持有人数 | 自建（conviction per holder） | 备料 |
| T5 | 持仓集中度 HHI | 拥挤 | vec_avg(herfindahl_index_holdings) | Sias 2004 羊群 + 拥挤度文献 | **已派发** |
| T6 | 持有账户广度 | 广度 | vec_avg(holder_account_total) | 自建 | 备料 |
| T7 | 边界交易率（换仓强度） | 事件 | boundary_transaction_total / holder_account_total | 自建（新建仓/清仓事件密度） | 备料 |
| T8 | 信念持仓账户占比 | 结构 | top_weighted_account_number / holder_account_total | 自建 | 备料 |
| T9 | 边界交易持续性 | 时序 | stable_boundary_trade_count_21d / boundary_transaction_total | 自建（稳定换仓 vs 反复进出） | 备料 |
| T10 | 大额交易占比 | 分布尾部 | large_trade_count_50bps / transaction_account_total | 自建 | 备料 |
| T11 | 持仓价值分布集中度 | 分布 | vec_avg(holding_value_distribution_score) | 自建 | 备料 |
| T12 | 交易金额分布集中度 | 分布 | vec_avg(transaction_value_distribution_score) | 自建 | 备料 |

差异落在信息维度（水平 / 变动广度 / 变动金额 / 强度 / 拥挤 / 广度 / 事件密度 / 结构 / 持续性 / 尾部 / 两个分布集中度）上。

## 5. 批次 A（mid = 2G84EYbyU4tQ9ylzSYe0Cs）

设置：EUR / TOP2500 / D1 / decay 8 / SLOW_AND_FAST / trunc 0.08 / unit VERIFY / nan ON / pasteurization ON / maxTrade ON。

E1（T2 机构买卖家数差，算子 1）：
group_rank(count_institutional_buyers_security - count_institutional_sellers_security, sector)

E2（T5 持仓集中度 HHI，算子 2）：
group_rank(vec_avg(herfindahl_index_holdings), sector)

gate：validate_expressions 在 EUR/TOP2500 返回 valid=true、unknown_fields=[]。

方向先验：T2 取正（机构净买入人数多 = 需求冲击向上，Bennett-Sias-Starks 的变动预测方向）；
T5 先取正测，若为明显负值且 |S| 更大再按「高集中度=拥挤=脆弱」翻号。

## 6. 待办

- [ ] 收批次 A：读 E1/E2 的 S/F/TO/2Y
- [ ] 若 E1 S ≥ 1.0，沿 T3/T4 同族换单位（金额/强度）扩展；若 E2 强则沿 T6/T11/T12 换集中度口径
- [ ] 若都 < 0.6，转 EUR/news（news54 40 字段 aC 12、news29 12 字段 aC 2）
- [ ] 本族 vol 可能偏低（季度数据），开波前先用 ret/S 估 vol，vol ≤ 2% 时按闭式先算所需 S

## 设置档 A/B 追记（STATISTICAL + decay 4，2026-11-06 收批）

| alpha | 模板 | S | F | TO | 2Y | sub | ret |
|---|---|---:|---:|---:|---:|---:|---:|
| `LLM8nK52` | T2 买卖家数差 | −0.02 | 0.00 | 4.83% | −2.37 | 0.04 | −0.03% |
| `O0A6nWJd` | T3 净买入金额 | 0.01 | 0.00 | 4.50% | 2.09 | 0.36 | 0.02% |

**结论**：SLOW_AND_FAST/decay8 档下 T2 = 0.07、T5 = −0.01；换到 STATISTICAL/decay4 档后 T2 = −0.02、T3 = 0.01 —— **两档 S 都在 ±0.07 内**，设置档完全不改变结论。
⇒ 直接证伪「SLOW_AND_FAST 中性化切掉了机构持仓的慢信号」这一假设，省下整族追查。EUR/institutions6 + fund_holdings_panel 在 TOP2500 单数据集内无横截面信号，判死。