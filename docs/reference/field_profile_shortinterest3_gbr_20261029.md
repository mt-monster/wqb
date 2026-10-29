# shortinterest3 字段画像与机制地图（GBR / TOP700 / D1）

> 实测日期：2026-10-29 ｜ 数据源：`get_datafields(region="GBR", universe="TOP700", delay=1, dataset_id="shortinterest3")`
> 平台口径：`complete: true` / `platform_count: 25` / 25 字段**全部 VECTOR**
> 塔位价值：GBR/D1 当前 **SHORTINTEREST 塔 0/3 未点亮**（16 类中未点亮 14 类之一）

---

## 0. 一句话结论

**这是「证券借贷（securities lending）」数据，不是传统 short interest 报告数据。** 它记录的是**出借人（lender）与借券方（borrower）之间的实际成交合约**：谁借了多少股、按什么费率、借了多久、同一个主键组里有多少笔成交。因此它的核心信息不是「空头持仓多少」，而是**做空的边际成本与供给紧张度**。

覆盖率 0.82–0.87 是 GBR 已接触数据集中最高的，25 个字段全部 VECTOR（必须 `vec_avg` / `vec_sum` 聚合后才能进 `ts_*` / `rank` / `group_*`）。

---

## 1. 字段清单与拥挤度

平台按「主键组（primary key group）」聚合，同一语义字段有 **3 个口径版本**，共享底层成交：

| 后缀 | 含义 | 覆盖率 | 说明 |
|---|---|---|---|
| 无后缀 | 基础口径 | 0.8217 | 组最细，覆盖率最低 |
| `_main` | 主键口径 | 0.8512 | 主键组聚合，覆盖率中等 |
| `_p5_d1` | 主键 + 5 日/1 日口径 | 0.8719 | **覆盖率最高**，字段最全 |

**三口径共享同一底层成交**，属「姊妹口径」：换口径信号应几乎不变（论坛帖 `43624312881943` 实测 `_main` 与 `_p5_d1` 版指标近乎逐位相同）。⇒ **口径选择不是研究对象，覆盖率优先取 `_p5_d1`，个股缺失补充取 `_main`。**

### 1.1 字段语义 + 拥挤度（`alphaCount` 越高越拥挤）

**费率族（loan rate）—— 拥挤度低，机制最纯**

| 字段 | `_p5_d1` alphaCount | 语义 | 经济含义 |
|---|---|---|---|
| `mean_loan_rate` | 75 | 加权平均借券费率 | **做空难度的价格**（D'Avolio 2002 JFE） |
| `max_loan_rate` | 49 | 组内最高费率 | 被极端合约主导，噪音大 |
| `min_loan_rate` | 39 | 组内最低费率 | 最容易借到的那部分供给价格 |
| `loan_rate_volatility` | 45 | **组内全部交易的费率标准差** | **★ 日内跨出借人的报价分歧**（截面，不是时序） |

**券量族（loan quantity）—— 拥挤度最高**

| 字段 | `_p5_d1` alphaCount | 语义 | 经济含义 |
|---|---|---|---|
| `loaned_share_count` | **288** | 借出股数 | 借券余额（SIR 的量纲版） |
| `loaned_market_value_usd` | **249** | 借出市值 USD | 同上，美元计价 |
| `transaction_count` | **164** | 组内成交笔数 | 借券参与广度 |

**期限族**

| 字段 | `_p5_d1` alphaCount | 语义 | 经济含义 |
|---|---|---|---|
| `average_loan_duration_days` | 49 | 借贷加权平均年龄（天） | 合约持续性 = 空头信心强度 |

**厂商预计算族**

| 字段 | alphaCount | 语义 | 注意 |
|---|---|---|---|
| `shrt3_bar` | 109 | 借券需求评级 **1–10**（10=需求最高） | 厂商已消化过 ⇒ 信息损耗大、拥挤度中高 |

### 1.2 拥挤度排序（决定 prod 撞墙风险）

```
loaned_share_count_p5_d1        288  ← 最拥挤
loaned_market_value_usd_p5_d1   249
loaned_share_count_main         220
transaction_count_p5_d1         164
transaction_count_main          147
loaned_market_value_usd_main    124
shrt3_bar                       109
mean_loan_rate_p5_d1             75
loaned_market_value_usd          67
max_loan_rate_p5_d1              49
average_loan_duration_days_p5_d1 49
...（费率/离散度族 16–49，最不拥挤）
loan_rate_volatility             16  ← 最不拥挤
```

**⇒ 派发优先级铁律：券量族（T4/T5/T9）prod 撞墙风险最高，费率族与离散度族（T1/T2/T3/T6/T7/T10）风险最低。** 先出费率族，凑塔时再用券量族做「机制真分离」的补充。

---

## 2. 三个必须先搞清的陷阱

### 2.1 `loan_rate_volatility` 是**截面**离散度，不是时序方差

平台原文：*"The standard deviation of loan rates **for all transactions in this primary key group**"*。

即：**同一天、同一只票、不同出借人之间**的费率报价分歧。它与 `ts_covariance(mean_loan_rate, mean_loan_rate, 22)`（**同一只票，费率随时间的波动**）是**两个完全不同的机制**：

| 维度 | `loan_rate_volatility` | `ts_covariance(x,x,22)` |
|---|---|---|
| 变化来源 | 出借人之间报价差异（横截面） | 时间上费率不稳定（纵截面） |
| 经济学 | 出借人异质信念 / 搜寻摩擦 | 空头面临的风险不确定性（ERR 2018） |
| 对应文献 | Duffie-Gârleanu-Pedersen (2002) 搜寻摩擦 | Engelberg-Reed-Ringgenberg (2018, JF) |

**✓ 这个差异对我们有利**：两者天然正交，是凑「三颗两两 <0.7」的现成机制分离轴。

### 2.2 GBR 缺少两个关键字段 ⇒ 利用率只能用 `shrt3_bar` 代理

论坛帖 `43636685645975` 的核心机制「券池利用率 ≥90% ⇒ 做空弹药枯竭 ⇒ 物极必反做多」依赖 `available_share_count`（可借券余量）与 `loan_utilization_ratio`（利用率）。**GBR 的 25 个字段里这两个都没有。**

⇒ **只能用 `shrt3_bar`（1–10 借券需求评级）做代理**。但需求评级 ≠ 利用率：评级高可能是「想借的人多」，也可能是「券池小」。这是本区机制的**结构性缺口**，必须承认。

### 2.3 GBR 无 `exchange` / `country` 变体

论坛帖最有效的分组轴是 **`exchange`（交易所制度边界）**——帖子里 `exchange` 版 S 1.89 PASS，而 `industry` 版 1.93 却因 robust 比例闸 FAIL。**GBR 只有 LSE 一个交易所**（TOP700 单一市场），`exchange` 轴退化为常数。

⇒ **分组轴只能退到 `sector` / `subindustry`。这是本区最大的未知点**：帖子的分组收益有多少来自「制度边界」、多少来自「同业可比」，无法在 GBR 分离。

**对策**：T1（无分组）/ T2（`group_zscore(subindustry)`）/ T3（`sector`）构成三档对照，直接测出「GBR 分组轴是否有效」。

---

## 3. 八问机制地图（每问对应可证伪假设）

| # | 问题 | 经济机制 | 文献 | 模板 |
|---|---|---|---|---|
| Q1 | 费率**时序不确定性**高 ⇒ ？ | 空头面临的风险不可预测 ⇒ 要求更高风险溢价，或干脆退出 ⇒ 后续跑输/跑赢 | Engelberg-Reed-Ringgenberg (2018, JF) "Short-Selling Risk" | T1 / T2 |
| Q2 | 费率**截面分歧**大 ⇒ ？ | 出借人报价分散 = 搜寻摩擦大 = 券源难找 ⇒ 做空成本隐性抬升 | Duffie-Gârleanu-Pedersen (2002) | T6 |
| Q3 | 借券**余额水平**高 ⇒ ？ | 空头拥挤 ⇒ 后续平仓压力 / 反向轧空风险 | Asquith-Pathak-Ritter (2005, JF) | T4 |
| Q4 | 借券**余额变化**（供给冲击）⇒ ？ | 借券量突增 = 知情做空入场 | Cohen-Diether-Malloy (2007, JF) | T5 |
| Q5 | **报价区间宽度**（max−min）/mean ⇒ ？ | 出借人定价分歧的相对强度，比绝对费率更可比 | — | T7 |
| Q6 | 借券**需求评级**相对自身历史异常高 ⇒ ？ | 稀缺性冲击 ⇒ 后续反转 | 论坛 `43636685645975`（≥90% 物极必反） | T8 |
| Q7 | 借券**参与广度**（成交笔数）⇒ ？ | 大量小额出借人参与 = 供给碎片化 = 借券难度上升 | — | T9 |
| Q8 | **长借期 × 高需求** ⇒ ？ | 借期长说明空头确信、需求高说明拥挤 ⇒ 强知情空头信号 | — | T10 |

**设计纪律**：7 个机制维度、10 种不同算子几何（`ts_covariance` / `group_zscore` / `ts_std_dev` / `rank` / `ts_delta` / `group_rank` / 同单位比值 / `ts_zscore` / `trade_when` 门控），**刻意避开把 `ts_delta` 当主信号**（论坛帖安慰剂对照实测 `ts_delta(x,22)` = S 0.09 / TO 98.7% ⇒ 信号不是「费率在涨还是在跌」，而是「不确定性」）。

---

## 4. 十模板池（已双预检通过）

| # | 算子几何 | 机制维度 | 拥挤度风险 | 表达式 |
|---|---|---|---|---|
| T1 | `ts_covariance(x,x,22)` 无分组 | 费率时序不确定性（ERR2018） | 低 | `multiply(-1, ts_covariance(vec_avg(mean_loan_rate_main), vec_avg(mean_loan_rate_main), 22))` |
| T2 | 自协方差 + `group_zscore(subindustry)` | 同上，子行业内可比 | 低 | `multiply(-1, group_zscore(ts_covariance(vec_avg(mean_loan_rate_p5_d1), vec_avg(mean_loan_rate_p5_d1), 22), subindustry))` |
| T3 | `ts_std_dev` + `group_zscore(sector)` | **方差/标准差判据对照** | 低 | `multiply(-1, group_zscore(ts_std_dev(vec_avg(mean_loan_rate_main), 22), sector))` |
| T4 | `rank(vec_sum(...))` 水平 | 借券余额总量（SIR） | **高（288）** | `multiply(-1, rank(vec_sum(loaned_share_count_p5_d1)))` |
| T5 | `rank(ts_delta(vec_sum(...),22))` | CDM2007 借券供给冲击 | **高（288）** | `multiply(-1, rank(ts_delta(vec_sum(loaned_share_count_p5_d1), 22)))` |
| T6 | `group_zscore(vec_avg(...), subindustry)` | 出借人报价分歧（截面） | 低（45） | `multiply(-1, group_zscore(vec_avg(loan_rate_volatility_p5_d1), subindustry))` |
| T7 | 同单位比值 `divide(subtract(a,b), c)` | 报价区间相对宽度 | 低（39–75） | `multiply(-1, rank(divide(subtract(vec_avg(max_loan_rate_p5_d1), vec_avg(min_loan_rate_p5_d1)), vec_avg(mean_loan_rate_p5_d1))))` |
| T8 | `rank(ts_zscore(...,252))` | 利用率异常收紧 | 中（109） | `multiply(-1, rank(ts_zscore(vec_avg(shrt3_bar), 252)))` |
| T9 | `group_rank(..., sector)` | 借券参与广度 | **高（164）** | `multiply(-1, group_rank(vec_avg(transaction_count_p5_d1), sector))` |
| T10 | `trade_when` 门控 | 长借期 × 高需求 = 强知情空头 | 中（49） | `trade_when(greater(vec_avg(shrt3_bar), 7), multiply(-1, rank(vec_avg(average_loan_duration_days_p5_d1))), 0)` |

**符号统一取负**：所有机制的先验方向都是「借券成本/紧张度上升 ⇒ 未来跑输」（Miller 1977 异质信念 + 卖空约束 ⇒ 高估），故统一 `multiply(-1, ...)` 表达成「紧张度越高越做空」。**若某条 S 为负且 |S| 显著，说明该机制在 GBR 方向反转，那本身就是有价值的发现（但要按 regime-flip 纪律查全期与近 2Y 符号是否一致）。**

**单位安全**：T7 全部为费率÷费率，天然无量纲；T4/T5 用 `vec_sum` 后直接 `rank`，不跨单位相除；T10 门控与信号分别来自不同字段但不相除。**全池无一处给带单位字段加无量纲常数**（`unit_handling=VERIFY` 红线）。

---

## 5. 平台设置选择（依据论坛实证，非区域档案）

GBR 区域档案是 `SUBINDUSTRY / decay 4 / truncation 0.08 / maxTrade ON / nanHandling ON`。本轮**改用**：

| 设置 | 值 | 依据 |
|---|---|---|
| neutralization | **SLOW** | 论坛实测 SLOW 是唯一能过 robust 比例闸的档（STATISTICAL 更强 S 2.44 但 robust 2.12 < 2.20 挂，且 prod 实测 0.8753） |
| decay | **0** | 帖子里 0/4/10/18 单调变差 |
| truncation | 0.08 | 帖子实测 0.08→0.15 逐位相同 = 死参数 |
| nanHandling | **ON** | 无成交填 0，把「券被召回」记为一次跳变 |
| maxTrade | **OFF** | ON 让 robust 93%→88% |
| unitHandling | VERIFY | 硬红线 |
| pasteurization | ON | 默认 |

⚠ **GBR `decay 0` 与 `decay 1` 输出逐位相同** ⇒ decay 轴实际只有 0/2/4 三档。
⚠ **`SLOW` 只经 ASI 单区实证**，GBR 是否同样最优**未验证** ⇒ T1（SLOW）与后续波次需对照 `CROWDING` / `STATISTICAL` 至少各一条。

---

## 6. 已知禁区（论坛实测，不要重试）

| 做法 | 结果 | 判据 |
|---|---|---|
| `ts_std_dev` 版替代方差版 | robust 1.70 < 1.78 = 1.98×0.9 **FAIL** | `LOW_ROBUST_UNIVERSE_SHARPE` 是**比例闸**（×0.9），方差是凸变换把尾部小票顶到 truncation 上限后在小票上主动少赚 ⇒ 过线。**跨区比例不统一（0.4 系到 0.9 系），每区须自测** |
| `divide(ts_std_dev(x,22), abs(ts_mean(x,22)))` CV 归一化 | S **0.61** / margin 0.8bp（窗口 66 时 −0.01） | **信号住在绝对量纲里，不能除水平** |
| `max_loan_rate` 作主信号 | 1.21 vs `mean_loan_rate` 1.89 | 最高费率被极端合约主导 |
| `group_rank` 替代 `group_zscore` | 0.71 vs 1.64 | 秩变换丢掉方差长尾 |
| `add(vec_avg(x), 0.0001)` 防除零 | 单位闸 WARNING 全灭 | 带单位字段不能加无量纲常数 ⇒ 比值一律同单位相除 |
| 无分组 | S 1.36 FAIL + `CONCENTRATED_WEIGHT` 0.114 | 必须组内归一化（欧洲各国融券合规差异） |
| 窗口 5 / 66 / 252 | 分别 F 挂 / 三挂 / S 1.09 | **22 天 = 一个交易月**，对应 ERR 2018 月度度量，不是扫出来的 |
| `ts_delta(x,22)` 作主信号 | S **0.09** / TO 98.7% | 安慰剂对照 ⇒ 收益来自「不确定性」不是「方向」 |
| `group_cartesian_product(country, exchange)` | 与 `exchange` PnL 逐位相同 | 嵌套轴是死参数 |

---

## 7. 待验证的三个 GBR 特有未知点

1. **分组轴是否有效**：GBR 无 `exchange`，退到 `sector`/`subindustry` 后是否仍能过 robust 比例闸 —— T1（无分组）/T2（subindustry）/T3（sector）三档对照直接回答。
2. **robust 比例闸在 GBR 是多少**：ASI 实测 ×0.90。GBR 比例未知，必须从第一条跑出的 alpha 的 `LOW_ROBUST_UNIVERSE_SHARPE.withRatio.limit` 反读。
3. **近十年数据是否连续**：平台 `coverage` 已多次实证造假，必须用 `get_alpha_yearly_stats` 逐年核 `longCount` / `pnl`。T1/T2 结果一回来就查。

## 8. 组合容量风险（最重要的一条）

论坛帖实测同数据集「价格维度五种实现」互相关 **0.47–0.78**，对「互相关 <0.4 篮子」容量 ≈ **1**。

⇒ **即便出了好 alpha，要凑 3 颗两两 <0.7 点亮 SHORTINTEREST 塔，必须靠机制维度真分离。** 本池按 7 个机制维度设计，但**维度多 ≠ 互相关低**——费率族的 T1/T2/T3 三个都建在 `mean_loan_rate` 上，互相关很可能 >0.7，只能算 1 颗。

**现实的点塔路径**：
- 第 1 颗：费率时序不确定性（T1 或 T2）
- 第 2 颗：费率截面分歧（T6，不同字段不同维度）
- 第 3 颗：券量族（T4 或 T5，完全不同字段族）——但 prod 拥挤度最高

⇒ **三颗必须横跨三个字段族，不能在同族里做三种算子。**
