# S1 · institutions6 全字段画像（KOR / TOP600 / D1）

> 数据源：MCP `get_datafields(dataset_id=institutions6, region=KOR, universe=TOP600, delay=1, **filter_sharpe=false**)`
> 返回 `count=11 / platform_count=11 / complete=true` ⇒ **11/11 全字段覆盖，无截断**。
> 画像六维：字段类型 · 覆盖率 · 更新频率 · 量纲/取值域 · 分布特征 · 可用性（能否作信号腿 / 分组腿 / 分母腿）。

## 0. 数据集级事实

| 项 | 值 | 含义 |
|---|---|---|
| 数据集 | `institutions6` · Institutions and Beneficial Stake Ownership | 全球股权机构/共同基金/受益股东持仓 |
| 平台 cov | **.9996** | KOR TOP600 几乎满覆盖 ⇒ 约束 6「近十年有数据」在**字段层**无覆盖瓶颈 |
| 字段数 | 11，**全 MATRIX** | 无 VECTOR ⇒ 不需要 `vec_*` 包裹，无 `vec_avg` 量纲陷阱 |
| aC 头部 | `aggregate_share_count_institutions` **257** | 头部指向**机构持股规模轴**，不是「流量净额轴」 |
| 披露节奏 | **季度（13F 式）** | 名义日频铺平、实际每 ~63 交易日一次阶梯跳变 ⇒ **所有时序窗口下限 63d，分母必须平滑 63–72d** |
| 单位 | 美元 / 股数 / **家数** | 三套量纲混在同一集 ⇒ 任何跨字段运算前必须先比值去量纲 |

## 1. 全 11 字段画像

| # | 字段 | 类型 | cov | aC | user | 语义 | 取值域 | 分布特征 | 更新频率 | 可用性 |
|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | `aggregate_equity_value_all_owners` | MATRIX | 1.0 | 91 | 64 | 全体股东（去母子重复）持有**市值** | ≥0，美元 | 重尾右偏，跨 6+ 数量级 | 季度阶梯 | ✅ **分母腿**（占比归一） |
| 2 | `aggregate_equity_value_institutions` | MATRIX | .9976 | 119 | 85 | **机构**持有市值 | ≥0，美元 | 重尾右偏 | 季度阶梯 | ✅ 分子腿 / 分母（建仓速率） |
| 3 | `aggregate_share_count_all_owners` | MATRIX | 1.0 | 212 | 124 | 全体股东持股**数** | ≥0，股 | 重尾右偏 | 季度阶梯 | ✅ **分母腿** |
| 4 | `aggregate_share_count_institutions` | MATRIX | .9976 | **257** | **147** | **机构**持股数（aC 头部） | ≥0，股 | 重尾右偏 | 季度阶梯 | ✅ 分子腿（占比 / 变化率） |
| 5 | `count_institutional_buyers_security` | MATRIX | 1.0 | 88 | 64 | 期内**买入**机构**家数** | 0–数百，整数 | 右偏、零堆积中等 | 季度阶梯 | ✅ **流强度分子**（论坛冠军核） |
| 6 | `count_institutional_holders_security` | MATRIX | 1.0 | 63 | 41 | 期末**持有**机构**家数** | ≥1，整数 | 右偏较轻、**最平滑** | 季度阶梯 | ✅ **分母锚 + 门控输入**（`ts_arg_max`） |
| 7 | `count_institutional_sellers_security` | MATRIX | 1.0 | 101 | 71 | 期内**卖出**机构**家数** | 0–数百，整数 | 右偏、零堆积中等 | 季度阶梯 | ✅ 净额对侧腿 |
| 8 | `market_value_institutional_shares_acquired` | MATRIX | 1.0 | 112 | 61 | 期内买入**金额** | ≥0，美元 | **重尾最重**（单笔大额） | 季度阶梯 | ✅ 净额腿 + 均价腿分子 |
| 9 | `market_value_institutional_shares_disposed` | MATRIX | 1.0 | 62 | 46 | 期内卖出**金额** | ≥0，美元 | **重尾最重** | 季度阶梯 | ✅ 净额对侧腿 + 均价腿分母 |
| 10 | `quantity_institutional_shares_acquired` | MATRIX | 1.0 | 119 | 72 | 期内买入**股数** | ≥0，股 | 重尾右偏 | 季度阶梯 | ✅ 均价腿分母 |
| 11 | `quantity_institutional_shares_disposed` | MATRIX | 1.0 | 107 | 57 | 期内卖出**股数** | ≥0，股 | 重尾右偏 | 季度阶梯 | ✅ 均价对侧腿 |

### 1.1 可用性分档（决定谁进哪一层）

| 档 | 字段 | 用法 |
|---|---|---|
| **分母腿**（平滑、低噪声） | `count_institutional_holders_security`、`aggregate_*_all_owners` | 任何比率的分母；**必须配 `ts_mean(·, 63~72)`** 剥季度阶梯 |
| **分子腿**（信息载体） | `count_institutional_buyers_security`、`market_value_*_acquired`、`quantity_*_acquired` | 信号主体 |
| **对侧腿**（构净额/价差） | `*_disposed`、`count_institutional_sellers_security` | 只与同族分子腿配对，**不单独作信号** |
| **分组腿** | — | 本集无 GROUP 类型；分组只能用平台的 `sector` / `industry` / `subindustry` / `market` |

### 1.2 预处理决策（0.3 五问 → 算子与窗口）

| 五问 | 读数 | 决策 |
|---|---|---|
| 测什么 | 机构**参与广度/强度**的时序变化，不是静态持仓水平 | 任一表达式必须含时序差分 / 时序分位 / 门控 |
| 怎么测 | 家数类最平滑、金额类最重尾 | 家数类走 ratio；金额类必须先 `winsorize` 或转成 ratio |
| 时间维度 | 季度阶梯（~63 交易日一跳） | **窗口下限 63**；分母平滑 63–72；分位窗口 252–840 |
| 为何存在 | 13F 式强制披露 ⇒ 慢披露 + 慢扩散 = 定价滞后窗口 | 机制天然偏「延迟反应 / 后续漂移」，不是当日反转 |
| 可靠性 | cov ≥ .9976（两字段）/ 1.0（九字段） | 无需 `ts_backfill` 强制补；`nan` 处理可留 OFF（与 KOR 全绿件 `LLZ6wZO2` 一致） |

### 1.3 量纲跨度（决定能否裸比）

- 金额类（#1/#2/#8/#9）单值可达 1e12 量级；家数类（#5/#6/#7）0–数百。
- ⇒ **禁止跨档直接相减**（`market_value_acquired − count_buyers` 无意义）；同档相减必须再除同档之和去量纲。
- 均价腿 `mv/qty` 得到**每股价格**（KOR 为 KRW 计价但字段为 USD 口径）⇒ 买卖两个均价相除是无量纲比值，安全。

## 2. 名 vs description 差异表（0.2 强制项）

| 名字面 | description 实义 | 差异后果 |
|---|---|---|
| `aggregate_*` | 逐证券横截面，不是市场汇总 | 可直接做 `institutions/all_owners` 占比 |
| `count_*_buyers` | **家数**（investors count），不是股数 | 与 `quantity_*` 是两个量纲，可分离「广度」与「强度」 |
| `quantity_*` vs `market_value_*` | 股数 vs 美元金额 | 相除 = 机构**成交均价**，是独立轴 |
| `_acquired` / `_disposed` | **报告期流量**，非期末存量 | 必须比率化，禁裸水平（铁律 A 变形） |
| `all_owners` | 去母子重复后的**全体**股东 | 含机构 + 内部人 + 散户 ⇒ `all − inst` = 非机构持仓 |

## 3. 成对结构清单（本集唯一可构净额的资产）

| 对 | 腿 A | 腿 B | 可用构造 |
|---|---|---|---|
| 市值流量 | `market_value_institutional_shares_acquired` | `market_value_institutional_shares_disposed` | 净额比 (A−B)/(A+B) · 建仓速率 /持仓市值 · 均价价差 |
| 股数流量 | `quantity_institutional_shares_acquired` | `quantity_institutional_shares_disposed` | 净额比 · 均价价差 |
| 家数 | `count_institutional_buyers_security` | `count_institutional_sellers_security` | **净家数 / 持有人数**（广度净额） |
| 存量占比 | `aggregate_share_count_institutions` | `aggregate_share_count_all_owners` | 占比水平 · 一阶差分 · 加速度 |
| 存量市值占比 | `aggregate_equity_value_institutions` | `aggregate_equity_value_all_owners` | 占比水平（低配逆向） |

## 4. 历史实测边界（来自论坛 IND 冠军帖，KOR 需重测）

| 构造 | IND 实测 S | 结论 |
|---|---:|---|
| 同步比值 `divide(buyers, holders)` 裸信号 | — | 结构不可行（分母未平滑 ⇒ 季度阶梯噪声吃掉信号） |
| `ts_corr(buyers, holders, 66)` | 0.38 | 证伪 |
| 美元净流（= 本集 #8−#9 裸净额） | 0.44 | 证伪 |
| 渗透率比值 | 0.20 | 证伪 |
| sellers 反向 | 0.71 | 证伪 |
| **新鲜度门** `trade_when(ts_arg_max(holders,G)<T, signed_power(ts_quantile(buyers/ts_mean(holders,72), W, gaussian), 1.6), -1)` | **1.62** | ✅ 冠军（IND，18 硬项全过） |

**KOR 平移前提**：KOR 同为 13F 式季度披露、同字段名、cov 更高（1.0 vs IND 有限覆盖）⇒ 机制可推断；
**但 G/T/W/p 系数必须重扫**（论坛原帖明确写「系数必重扫，机制可推断」）。

## 5. 与外部论文的对照（S2 双通道的 B 通道摘要）

| 机制 | 文献 | 对本集的预测 |
|---|---|---|
| 非弹性市场：机构资金流对价格的影响被放大且缓慢补足（$1 流入 → $5 市值） | Gabaix & Koijen (2023) | 机构**流量**（#5/#8/#10）应领先价格，且效应持续 ⇒ 支持净额/广度轴 |
| 机构持仓网络 → 下一月焦点股超额收益，形成后**持续而非反转** | Feng, He, Wang & Xiao (2026) | 支持「参与广度扩张 → 后续漂移」而非即时反转 |
| 协调噪声交易（养老金再配置）造成价格短暂偏离 | Da, Larrain, Sialm & Tessada (2016) | 支持「突增 → 保持 → 回落」的**新鲜度**节奏 |
| 大机构交易在流动性不足市场制造价格 spike | Gabaix et al. (2005) | 小盘高摩擦段效应更强 ⇒ 分组轴用 `sector`/`industry` 细分 |

## 6. 落盘与索引

- 本文件 = `tracking/KOR/campaign_20261107_institutions_atom/s1_field_profile_institutions6.md`
- 姊妹文件：`s1_field_profile_fund_holdings_panel.md`（30 字段）
- 上游：`s0_dataset_scan.md` · 下游：`s2_mechanism_evidence.md` → `waves.md`
