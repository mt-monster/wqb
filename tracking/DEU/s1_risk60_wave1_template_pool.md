# risk60（Securities Lending Insight）模板池 — DEU / TOP500 / D1 波次 1

> 建立依据：台账 §68 与 L1153–L1269 显示 risk60 只被探过 **一条臂**（`1YNx3vnm`，S 0.75 / F 0.50 / 2Y 0.79 / margin 10.39bp / lc 137）就被列入「前一阶段判死」，
> 而该臂本身用了 `add(rank(A), rank(B))` 这种已知会系统性压低 margin 的秩和融合。S 0.75 已超「最优 < 闸值 40%（= 0.632）才允许快速停止」的阈值，
> 因此这次重开不算重复刷判死结论，而是补齐被漏掉的模板覆盖。

## 一、数据集画像（平台实测）

| 属性 | 值 |
|---|---|
| category | **risk**（非 trio，塔 RISK，pyramidMultiplier **1.5**） |
| coverage | **0.835** |
| 字段数 | 5，**全部 VECTOR** |
| alphaCount | 395 / userCount 198（高拥挤） |
| 首条探针 longCount | **137**（> 40，覆盖可用） |

字段：

| 字段 | ac | 含义 |
|---|---:|---|
| `rsk60_offer` | 196 | 空头方支付的综合借券费率（年化） |
| `lending_fee_bid_rate` | 145 | 出借方能成交的年化费率（bid 侧） |
| `rsk60_last` | 128 | 快照时刻最近一次观察到的借券费率 |
| `rsk60_crowding` | 53 | 带符号的每日做空活跃度（正 = 做空增加/拥挤上升） |
| `rsk60_datatime` | 11 | 供应商时间戳 HHMMSS（排序用，不构成信号） |

## 二、经济机制（为什么值得单独成波）

**卖空约束理论**（Chen–Hong–Stein 2002 *Breadth of Ownership and Stock Returns*；D'Avolio 2002 *The Market for Borrowing Stock*）：
借券费率是卖空约束的**直接价格**。费率越高 ⇒ 卖空越贵 ⇒ 悲观观点无法表达 ⇒ 股价被高估 ⇒ 后续**负收益**。
这正是 `offer` 取负号的先验来源，与「倍率/量」类常见因子无关，属独立机制。

`rsk60_crowding` 提供第二个维度：做空活跃度**上升**是知情交易者入场，后续负收益；但拥挤度过高时也可能是挤空风险的**反向**信号。
这条双重可能性正是要用多模板分辨的，不能用单臂定论。

## 三、模板池（12 个，结构互异）

编号规则：出处标注 **paper**（文献机制）/ **forum**（平台论坛）/ **self**（自建几何）。

| # | 模板 | 结构差异 | 出处 | 方向 | 算子数 |
|---|---|---|---|---|---|
| T1 | `-rank(ts_mean(vec_avg(rsk60_offer),22))` | 水平 · 横截面秩 · 单腿 | paper | 高费率→空 | 3 |
| T2 | `-rank(ts_mean(vec_avg(rsk60_crowding),22))` | 水平 · 换主字段 | paper | 高拥挤→空 | 3 |
| T3 | `rank(divide(subtract(vec_avg(rsk60_offer),vec_avg(lending_fee_bid_rate)),add(abs(vec_avg(lending_fee_bid_rate)),0.0001)))` | **费率特殊度**（offer−bid 相对价差） | paper | 价差大→空 | 5 |
| T4 | `-rank(ts_delta(vec_avg(rsk60_crowding),22))` | **一阶差分** · 动量几何 | self | 拥挤升→空 | 3 |
| T5 | `-rank(ts_delta(vec_avg(rsk60_offer),22))` | 一阶差分 · 换主字段（费率变化） | paper | 费率升→空 | 3 |
| T6 | `-rank(ts_zscore(vec_avg(rsk60_offer),252))` | **时序标准化**（自身一年基准） | self | 异常高→空 | 3 |
| T7 | `-group_rank(ts_mean(vec_avg(rsk60_offer),22),sector)` | **行业内相对**（换分组轴） | self | 同业最贵→空 | 4 |
| T8 | `trade_when(less(group_rank(vec_avg(rsk60_crowding),sector),0.7),-rank(ts_mean(vec_avg(rsk60_offer),22)),-1)` | **门控**（拥挤度当条件，费率当信号） | self | 非拥挤时才做空高费率 | 7 |
| T9 | `subtract(rank(ts_rank(vec_avg(rsk60_offer),252)),rank(ts_rank(vec_avg(rsk60_crowding),252)))` | **双分位价差**（同机制、两维度差） | self | 费率高而拥挤低→多 | 6 |
| T10 | `group_neutralize(-rank(ts_mean(vec_avg(rsk60_offer),22)),subindustry)` | 水平 + **中性化层** | self | 高费率→空 | 4 |
| T11 | `-rank(ts_std_dev(vec_avg(rsk60_crowding),22))` | **二阶矩**（波动而非水平） | self | 拥挤波动大→空 | 3 |
| T12 | `ts_target_tvr_decay(-rank(ts_mean(vec_avg(rsk60_offer),22)),target_tvr=0.05)` | 水平 + **换手抑制**（验证换手是否吃掉信号） | self | 同 T1 | 4 |

## 四、必须遵守的已知反模式

1. **禁止 `add(rank(A), rank(B))` 融合**——上一轮 `1YNx3vnm` 正是这样把费率与拥挤度相加，已知会系统性压低 margin（台账多处实证）。要合并两个维度只能走 T9 的价差或 T8 的门控。
2. **VECTOR 字段必须先 `vec_avg` 再参与任何跨字段算术**，`multiply(A, B)` 直接喂 VECTOR 会报 `does not support event inputs`。
3. 时间窗口只用白名单：1 / 5 / 22 / 66 / 252 / 504 / 756 / 1008 / 1260。T6 用 252（一年）是为了让「异常费率」相对自身一整年基准。
4. 算子数上限 12，能压到 8 以下更好；T8 的 7 个是上限附近的写法，只在 T1/T2 全灭时才上。

## 五、快速停止判据

- 首 2 条（T1 / T4）若最优 S < **0.632**（闸值 1.58 的 40%）⇒ 本数据集收手，不必补满模板。
- 若 T1/T4 任一 S ≥ 1.0 ⇒ 继续按 T3/T6/T7/T9 推进到 10 模板。
- 若 S 落在 [0.632, 1.0) ⇒ 只能小批补 3–4 个模板（T3/T6/T7），不得全池铺开。