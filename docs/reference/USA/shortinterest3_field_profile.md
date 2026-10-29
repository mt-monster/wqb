# USA · `shortinterest3` 字段画像

> 由 `tools/fields/profile_dataset_fields.py` 生成，输入为 `get_datafields` 原始返回。零平台配额。

## 1 规模与完整性

| 项 | 值 |
|---|---|
| 本次返回字段数 | 31 |
| 平台声明数 `platform_count` | 31 |
| 返回 `count` | 31 |
| 是否完整 `complete` | True |
| 类型分布 | {'VECTOR': 31} |
| 平均 coverage | 1.0000 |
| 判定 | ✅ 完整 |

## 2 可用性分档

### 2.1 coverage

| 档 | 字段数 |
|---|---|
| ≥0.90（可直接做尽） | 31 |

### 2.2 拥挤度（决定 prod 相关性风险）

| 档 | 字段数 |
|---|---|
| 中拥挤（51–500） | 17 |
| 低拥挤（≤50 alpha） | 12 |
| 高拥挤（501–5000） | 2 |

零竞争字段（`userCount==0`）：**0** / 31；描述带单位标注：6

## 3 语义结构

| 语义族 | 字段数 | 示例字段 |
|---|---|---|
| 未归类 | 28 | `available_share_count`, `average_loan_duration_days`, `average_loan_duration_days_main`, `borrow_activity_score` |
| 规模/水平 | 3 | `available_market_value_usd`, `loaned_market_value_usd`, `loaned_market_value_usd_main` |

**时间朝向**（`forecast`=前瞻/预测，`realized`=已实现/事后，`mixed`=差值构造）：

| 朝向 | 字段数 |
|---|---|
| unknown | 31 |

## 4 名字前缀聚类（前 15）

| 前缀 | 字段数 |
|---|---|
| `loaned_share` | 4 |
| `rate_bin` | 4 |
| `average_loan` | 2 |
| `loan_rate` | 2 |
| `loan_utilization` | 2 |
| `loaned_market` | 2 |
| `max_loan` | 2 |
| `mean_loan` | 2 |
| `min_loan` | 2 |
| `new_loaned` | 2 |
| `transaction_count` | 2 |
| `available_market` | 1 |
| `available_share` | 1 |
| `borrow_activity` | 1 |
| `shrt3_bar` | 1 |

## 5 候选短名单（Top 25，按打分排序）

打分 = 覆盖 40 + 低拥挤 25 + 语义可解释 20 + 前瞻 5（非信号 −30）。**只做排序参考**，仍须过单位闸与机制假设。

| # | 字段 | 类型 | cov | user | alpha | 语义族 | 朝向 | 分 | 描述（截断） |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `available_market_value_usd` | VECTOR | 1.000 | 34 | 40 | 规模/水平 | - | 80.0 | USD market value of the units reported as available to lend for this group |
| 2 | `loaned_market_value_usd` | VECTOR | 1.000 | 11 | 14 | 规模/水平 | - | 80.0 | US dollar market value of the units lent in the transactions in this group |
| 3 | `loaned_market_value_usd_main` | VECTOR | 1.000 | 11 | 12 | 规模/水平 | - | 80.0 | USD market value of the units lent in transactions in this primary key group |
| 4 | `average_loan_duration_days` | VECTOR | 1.000 | 24 | 26 | 未归类 | - | 60.0 | Weighted average age of loans in this group, measured in days |
| 5 | `average_loan_duration_days_main` | VECTOR | 1.000 | 20 | 26 | 未归类 | - | 60.0 | The weighted average age of loans in this primary key group, measured in days |
| 6 | `loaned_share_count` | VECTOR | 1.000 | 27 | 34 | 未归类 | - | 60.0 | Number of units (shares or par value) lent in the transactions in this group |
| 7 | `loaned_share_count_main` | VECTOR | 1.000 | 14 | 18 | 未归类 | - | 60.0 | Number of units (shares or par value) lent in the transactions in this primary key group |
| 8 | `loaned_share_count_r2` | VECTOR | 1.000 | 6 | 8 | 未归类 | - | 60.0 | Number of units (shares or par value) lent in transactions that fall into this primary ke… |
| 9 | `loaned_share_count_r2_d1` | VECTOR | 1.000 | 10 | 13 | 未归类 | - | 60.0 | Number of units (shares or par value) lent in transactions that fall into this bin and ke… |
| 10 | `new_loaned_share_count_d1` | VECTOR | 1.000 | 15 | 17 | 未归类 | - | 60.0 | Number of units (shares or par value) lent in new loans within this bin; subset of Units |
| 11 | `rate_bin_lower_limit_d1` | VECTOR | 1.000 | 38 | 40 | 未归类 | - | 60.0 | Inclusive lower bound of the loan rate bin, expressed in percent (e.g., 1.23 = 1.23%) |
| 12 | `rate_bin_upper_limit_d1` | VECTOR | 1.000 | 42 | 50 | 未归类 | - | 60.0 | Upper bound of loan rate bin, in percent; pairs with LowerBound to define the bin |
| 13 | `available_share_count` | VECTOR | 1.000 | 92 | 129 | 未归类 | - | 52.0 | Number of units (shares or par value) reported as available to lend for this group |
| 14 | `borrow_activity_score` | VECTOR | 1.000 | 55 | 75 | 未归类 | - | 52.0 | Demand score from 1 to 10 indicating how high the borrow demand is for the stock (1=low, … |
| 15 | `loan_rate_volatility` | VECTOR | 1.000 | 87 | 115 | 未归类 | - | 52.0 | The standard deviation of loan rates for all transactions in this primary key group |
| 16 | `loan_rate_volatility_main` | VECTOR | 1.000 | 74 | 100 | 未归类 | - | 52.0 | Standard deviation of loan rates across transactions in this primary key group |
| 17 | `loan_utilization_ratio` | VECTOR | 1.000 | 101 | 172 | 未归类 | - | 52.0 | Ratio of shares on loan to shares available from lending programs for the security (Units… |
| 18 | `loan_utilization_ratio_d1` | VECTOR | 1.000 | 57 | 84 | 未归类 | - | 52.0 | Share utilization ratio: aggregate shares on loan divided by shares available for lending… |
| 19 | `max_loan_rate` | VECTOR | 1.000 | 63 | 96 | 未归类 | - | 52.0 | The maximum loan rate among all transactions in this primary key group |
| 20 | `max_loan_rate_main` | VECTOR | 1.000 | 59 | 84 | 未归类 | - | 52.0 | Maximum loan rate among transactions in this group |
| 21 | `mean_loan_rate` | VECTOR | 1.000 | 150 | 241 | 未归类 | - | 52.0 | The weighted average loan rate for all transactions in this primary key group |
| 22 | `mean_loan_rate_main` | VECTOR | 1.000 | 77 | 115 | 未归类 | - | 52.0 | Weighted average loan rate for transactions in this group |
| 23 | `min_loan_rate` | VECTOR | 1.000 | 99 | 143 | 未归类 | - | 52.0 | The minimum loan rate among all transactions in this primary key group |
| 24 | `min_loan_rate_main` | VECTOR | 1.000 | 119 | 234 | 未归类 | - | 52.0 | Minimum loan rate among transactions in this group |
| 25 | `new_loaned_share_count` | VECTOR | 1.000 | 41 | 53 | 未归类 | - | 52.0 | Number of units (shares or par value) lent in new loans within this bin; a subset of Units |

> ⚠ 上方 §3/§5 的语义族与时朝向分类是**正则启发式**产物：31 个字段里 28 个落进「未归类」、31 个朝向全 `unknown`。这些列**不能当机制先验用**。真正的语义结构见下方人工分析 §6–§10。

---

## 6 VECTOR 语义（本数据集最关键的一条，决定所有算子写法）

31 个字段**全部是 VECTOR**。向量维度 = **费率离散度分箱（rate-dispersion bin）× 合约/抵押类型**的组合，不是时间、不是同业集合。

识别证据：`rate_bin_lower_limit` / `rate_bin_upper_limit`（"Lower/Upper bound of the loan rate bin (in percent), defining the minimum rate included in this dispersion range"）是**箱边界**；`loaned_share_count_r2` 的描述直接写 "transactions that fall into this primary key group/**rate-dispersion bin**"。

由此产生三条硬约束：

1. **`vec_avg(x)` = 跨箱等权平均，不是该股票的真实成交量加权费率。** 真实借券成本应按成交量加权，而 FASTEXPR 没有 vec 逐元素乘法 ⇒ 拿不到箱级加权。**这是数据结构级的硬边界，任何骨架都绕不过去**，只能用等权统计量近似。
2. **`vec_sum(x)` 只对「可加量」有意义**（`*_share_count`、`*_market_value_usd`、`transaction_count`）；对费率/利用率/评分做 `vec_sum` 无经济含义。
3. **箱边界字段是分组轴候选，不是信号**：`rate_bin_*`（4 个）适合当 `group_*` 的第二参或构造分层，直接当信号腿没有经济解释。

## 7 命名变体去重（先做这一步，否则白烧仿真槽）

四套后缀，名义 31 个字段，**去重后独立信息量约 18–20 个**：

| 变体 | 字段 | 描述特征 | 判断 |
|---|---|---|---|
| 裸名 | `mean_loan_rate` / `min_loan_rate` / `max_loan_rate` / `loan_utilization_ratio` / `loan_rate_volatility` / `available_share_count` / `loaned_share_count` / `loaned_market_value_usd` / `new_loaned_share_count` / `transaction_count` / `average_loan_duration_days` | 一律写 "in this **primary key group**" | 与 `_main` **描述逐字级相同** |
| `_main` | `max_loan_rate_main` / `min_loan_rate_main` / `mean_loan_rate_main` / `loan_rate_volatility_main` / `loan_utilization_ratio`(无 main) / `loaned_share_count_main` / `loaned_market_value_usd_main` / `new_loaned_share_count`(无 main) / `transaction_count_main` / `average_loan_duration_days_main` | 同样写 "primary key group" | ⚠ **裸名 vs `_main` 极可能是同一内容的两个 vendor 快照** ⇒ 两者并列测 = 结构重复，只当**稳健性交叉验证**用，不当新模板 |
| `_d1` | `loan_utilization_ratio_d1` / `new_loaned_share_count_d1` / `loaned_share_count_r2_d1` / `rate_bin_lower_limit_d1` / `rate_bin_upper_limit_d1` | 强调 "on the date" / "inclusive" | delay-1 口径重发布；与对应裸名高度重叠 |
| `_r2` | `loaned_share_count_r2` / `loaned_share_count_r2_d1` | 明确 "fall into this … **rate-dispersion bin**" | **真正的箱级字段（仅 2 个）**，信息维度不同，值得单独用 |

## 8 拥挤度三档（决定 prod 相关性风险，是本数据集的选字段主标尺）

| 档 | 字段（userCount / alphaCount） | 用法 |
|---|---|---|
| **极拥挤·半禁区** | `shrt3_bar` **604 / 2028**、`shrt3_utilizationpercent_units` **441 / 1080** | 平台主打、alpha 密度最高 ⇒ prod 撞墙概率最高。实测 `shrt3_bar` 水平值只有 S 0.49 / F 0.08。只可当**辅助信号**（条件/分组），不宜当主腿 |
| **中拥挤·主战场** | `mean_loan_rate` 150/241、`min_loan_rate_main` 119/234、`loan_utilization_ratio` 101/172、`min_loan_rate` 99/143、`available_share_count` 92/129、`loan_rate_volatility` 87/115、`loan_rate_volatility_main` 74/100、`mean_loan_rate_main` 77/115、`max_loan_rate` 63/96、`max_loan_rate_main` 59/84、`loan_utilization_ratio_d1` 57/84 | 已证实能出货（`mean_loan_rate_main` → S 1.81 / 1.90）。但 alpha 密度已不低，prod 需实测 |
| **低拥挤·金矿** | **`loaned_market_value_usd` 11/14**、**`loaned_market_value_usd_main` 11/12**、**`loaned_share_count_r2` 6/8**、`loaned_share_count_r2_d1` 10/13、`loaned_share_count_main` 14/18、`new_loaned_share_count_d1` 15/17、`average_loan_duration_days_main` 20/26、`average_loan_duration_days` 24/26 | **几乎无人使用**，美元口径 / 箱级股数 / 期限是三个全新维度，是 prod < 0.70 的最大机会。M13（期限）已在飞；美元口径与流量比尚未测 |

## 9 七族语义 × 已实测强度（把 M 波结果挂回族上）

| 族 | 字段 | 已测最优 | 判定 |
|---|---|---|---|
| **费率二阶矩** | `mean_loan_rate(_main)` 经 `ts_covariance` / `vec_stddev`；厂商版 `loan_rate_volatility(_main)` | **M10 S 1.90 / F 1.80 / fRA 0；M1R S 1.81 / F 1.50；M3 翻转 S 1.66 / F 0.93** | ✅ **唯一强族**。机制=借券费率不确定性→借券风险溢价 |
| 费率水平 | `mean_loan_rate_main` | M2 S 1.26 / F 0.43 | 中弱（水平信息已被二阶矩覆盖） |
| 利用率 | `loan_utilization_ratio(_d1)` / `shrt3_utilizationpercent_units` | M2 S **2.04** 但 F 0.81、inv_ratio 0.57；水平仅 0.30 | ⚠ 信号强但**落在不可投资区** ⇒ 换字段问题，不是调骨架能修 |
| 需求评分 | `shrt3_bar` / `borrow_activity_score` | M6 S 0.49 / F 0.08 | 弱 |
| 数量/存量 | `available_share_count` / `loaned_share_count` / `transaction_count(_main)` | M12 S 1.07 / F 0.32 / SUB 0.11 | 弱 |
| **期限** | `average_loan_duration_days(_main)` | **M13 在飞** | 未测 |
| **美元口径 / 流量比** | `*_market_value_usd` / `new_loaned_share_count(_d1)` | **未测** | 未测，且**最不拥挤** |

## 10 单位闸与下一批弹药

**单位铁律**：`*_market_value_usd` 带 USD 单位、`*_share_count` 带股数单位、`*_rate*` 带百分比。比值**一律同单位相除**，**绝不加 ε**（`add(x, 0.0001)` 会让整条表达式 `WARNING` 失败，本仓已实证整批 8 条全灭）。

尚未使用、但结构成立的推导量（下一批模板弹药）：

| 推导量 | 表达式 | 经济含义 | 风险 |
|---|---|---|---|
| 价值口径利用率 | `divide(vec_sum(loaned_market_value_usd), vec_sum(available_market_value_usd))` | 按金额而非股数算的利用率 | 与 `loan_utilization_ratio`（172 alpha）口径不同 ⇒ **天然低相关**，是本族最好的低相关候选 |
| 借贷周转率 | `divide(vec_sum(new_loaned_share_count), vec_sum(loaned_share_count))` | 新借 / 存量 = 流量存量比 | 股数单位约掉；`new` 是 `loaned` 的子集 ⇒ 比值 ∈ [0,1]，语义干净 |
| 隐含每股价格 | `divide(vec_sum(loaned_market_value_usd), vec_sum(loaned_share_count))` | 每借出股份的美元价值 | ⚠ **与 PV 高度相关**，会拉高 prod 且破坏 ATOM ⇒ 慎用 |
| 价格分层厚度 | `vec_count(rate_bin_lower_limit)` | 当日活跃费率箱数 | 若分箱是固定网格则退化为常量，一次探测即可判定 |
| 箱间价格歧视 | `subtract(vec_max(min_loan_rate), vec_min(max_loan_rate))` | 最贵箱底 − 最便宜箱顶：重叠度 | 同单位相减合法；符号需实测判读 |

**时间跨度已实测**：`coverage=1.0` 是**股票覆盖率**，不是时间跨度。`E56AnWgP` 的 `get_alpha_yearly_stats` 逐年 longCount 1864–1947、2014–2023 全覆盖 ⇒ 本数据集满足「近十年都有数据」的选集要求。▼

