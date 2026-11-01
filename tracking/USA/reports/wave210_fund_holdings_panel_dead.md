# 波 210：`fund_holdings_panel` × 10 结构互异模板 → 数据集级判死

- **multisim**：`3FTDh5bJB4Kybt71bTSY5xcF`（10/10 完成，0 error）
- **settings**：`USA / TOP3000 / D1 / NONE / decay 5 / trunc 0.08 / nanHandling ON`
- **塔位**：`USA/D1/INSTITUTIONS`（1.0×，本季度 0 颗）
- **结论**：**FAIL（0 pass / 0 near）—— `fund_holdings_panel` 在 USA/TOP3000/D1 数据集级判死**

---

## 1. 数据集画像（30 字段，全 VECTOR）

| 指标 | 值 |
|---|---|
| 字段数 | 30（全部 `VECTOR`，需 `vec_*` 聚合） |
| coverage | 0.9897 – 1.00 |
| alphaCount | 4 – 172（**多数 < 50，平台最不拥挤的数据集之一**） |
| 语义族 | 5 族（边界交易 / 集中度 / 广度 / 权重规模 / 信念） |

**VECTOR 聚合规则（本轮确立）**
- 计数类、USD 金额类 → `vec_sum`（语义是「总量」）
- 比率 / 指数 / 权重类 → `vec_avg`（语义是「平均持股比例」，多元素时 `vec_sum` 会稀释）

## 2. 十模板结果

| # | 模板结构 | 字段 | alpha | S | F | TO | 2Y | SUB | long/short |
|---|---|---|---|---|---|---|---|---|---|
| T1 | 持久仓位变化 zscore | `stable_boundary_trade_count_21d` | `9qxg6QdV` | 0.40 | 0.12 | 49.96% | 0.46 | 0.56 | 929/2011 |
| T2 | 集中度一阶差分 | `herfindahl_index_holdings` | `kqNem5Gd` | 0.33 | 0.26 | 5.20% | −0.30 | 0.28 | 1400/1225 |
| T3 | 交易集中度 reverse | `herfindahl_index_transactions` | `mLoezk7x` | 0.16 | 0.04 | 56.29% | 0.04 | −0.49 | 1714/1274 |
| **T4** | **广度水平 group_rank(subindustry)** | `holder_account_total` | `E56oaAzm` | **0.72** | 1.07 | **0.68%** | 0.07 | 0.45 | 2846/26 |
| T5 | 信念族 zscore | `top_weighted_transaction_number` | `GrWE8vxo` | 0.44 | 0.16 | 40.48% | 0.58 | −0.38 | 978/1603 |
| T6 | 大单占比 | `large_trade_count_50bps / transaction_account_total` | `YP1XkdJw` | 0.24 | 0.05 | 47.74% | −0.33 | −0.10 | 598/2053 |
| **T7** | **权重分位 ts_rank 504** | `mean_security_weight` | `LLMOXxrm` | 0.65 | 0.91 | 4.34% | −0.10 | −0.19 | **2997/0** |
| T8 | 边界交易/持仓 USD 比 | `boundary_usd / holding_usd` | `88Rg6qXm` | 0.16 | 0.02 | 54.05% | 0.36 | −0.58 | 1597/1343 |
| T9 | 头部账户占比 | `top_weighted_account_number / holder_account_total` | `gJe7PzdJ` | −0.18 | −0.08 | 10.80% | −0.45 | −0.29 | 1181/1547 |
| T10 | trade_when 事件门控 | `transaction_account_total` 突破 252 日均值 | `MPY98AV9` | −0.18 | −0.10 | 5.25% | −0.11 | 0.28 | 951/2019 |

**最高 S = 0.72，距 1.58 闸差 2.2 倍。无一条进入 near 区间。**

## 3. 归因：为什么这个数据集无承载能力

### 3.1 唯一「高分」的两条都是结构性死路
- **T4（S 0.72）**：`group_rank(holder_account_total, subindustry)` —— TO 只有 **0.68%**，触发 `LOW_TURNOVER`（限 1%）。这是**慢变量在行业内排序后几乎不动**的必然结果。long 2846 / short 26 也说明它其实是个纯多头暴露。
- **T7（S 0.65 / F 0.91）**：`ts_rank(mean_security_weight, 504)` —— **long 2997 / short 0，纯多头**，SUB −0.19。机构平均持仓权重高的公司就是大公司，横截面分位后等于做多规模因子。

⇒ **两条都是「规模/水平暴露」而非 alpha**，且都撞结构性闸（TO / long-only）。

### 3.2 比值模板全面失效
三条比值模板（T6 大单占比、T8 边界交易/持仓比、T9 头部账户占比）S 分别为 0.24 / 0.16 / −0.18。原因：分子分母来自同一机构持仓档案，**同源抵消**——大机构的账户数多、交易额也大，比值近似常数。

### 3.3 事件门控轴无预测力
T10（`transaction_account_total` 突破 252 日均值时交易）S −0.18。活跃账户数突破本身不携带未来收益信息。

### 3.4 ★ 与 earnings6 同型的「低 alphaCount 陷阱」二次确认
- `boundary_transaction_total`（aCnt **122**）/ `top_weighted_transaction_number`（aCnt **4**）/ `top_weighted_account_number`（aCnt **17**）全部无信号或负信号。
- 与波 209 的 `eps_change_percentage_value`（aCnt 3）/ `eps_change_absolute_value`（aCnt 5）**完全无数据**同型。

⇒ **判据确立：低 alphaCount 有两类成因 —— 「未被挖掘」和「挖了没用」。二者在 alphaCount 上不可区分，必须先用最小探针验信号存在性。**

## 4. 与波 209 的对照：两集死法不同

| | `earnings6`（波 209） | `fund_holdings_panel`（波 210） |
|---|---|---|
| 数据形态 | 52 字段全 VECTOR，事件型季度数据 | 30 字段全 VECTOR，机构持仓档案 |
| 死法 | 5/10 模板 `longCount=0`（无数据） | 10/10 有数据但信号弱 |
| 最高 S | 0.84 | 0.72 |
| 特异的失败模式 | 股息字段恒正 ⇒ 纯多头 | 水平量慢变量 ⇒ TO<1% 或 long-only |
| 共同点 | **慢速/季度型基本面在 USA D1 的横截面水平量上不产生日频 alpha** |

**合并结论**：USA/D1 的 `EARNINGS` 与 `INSTITUTIONS`（`fund_holdings_panel`）两个「季度披露型」数据集都缺日频变化信息。差距在于 `institutions18`（13F 持仓）**同时提供 `cur_` 与 `pre_` 两个时点**，可直接构造成流量差分 —— 这是它比 `fund_holdings_panel`（只有当期水平）更可能有信号的结构性原因，也是波 211 的立论基础。

## 5. 落地

- `wave_results` 已写入（verdict=FAIL, n_pass=0, n_near=0）
- 数据集状态：`fund_holdings_panel` **USA/TOP3000/D1 判死**；GLB/EUR 若字段口径一致可复用判定
- 波 211 改用 `institutions18`（同塔，但有 cur/pre 双时点）
