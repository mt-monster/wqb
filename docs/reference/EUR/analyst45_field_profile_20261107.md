# analyst45 (Analyst Trade Ideas) 字段画像 · EUR/TOPCS1600/D1

- 采集时间：2026-11-07
- 采集口径：`get_datasets(region=EUR, universe=TOPCS1600, delay=1)` → `get_datafields(dataset_id=analyst45, filter_sharpe=false, max_fields=200)`
- 平台读数：**61 字段 / 全部 VECTOR / field coverage 全 1.0 / alphaCount 246 / userCount 149**
- 定位：EUR 16 个 analyst 数据集中 **唯一 field-cov=1.0** 的一个；61 个字段里 60 个 userCount ≤ 10（唯一被开采的是 `net_market_exposure`，alphaCount 118 / userCount 86）⇒ 近乎处女地。

## 1. 覆盖率与可用性（硬事实）

| 维度 | 读数 | 判定 |
|---|---|---|
| 字段覆盖率 | 61/61 字段 coverage = 1.0000 | 通过 EUR「cov ≥ 0.85」门槛，sub 闸结构可达 |
| 字段类型 | 61 个全 VECTOR（每股票-日一个构想向量） | 必须先用 `vec_*` / `reduce_*` 降维，任何裸字段进 `group_rank` 会失败 |
| 非数值字段 | 4 个（`benchmark_currency_code` `conversion_rate_summary` `investment_currency_code` `security_trading_currency_3`） | 币种/汇率摘要，**不可进表达式** |
| 明确废弃 | `bias_weighted_ret` 描述为 **"Non-Functional"** | 平台自标不可用，禁用 |
| 拥挤度 | 246 alphas / 149 users（对照 analyst69 14254 / analyst4 3112） | 低拥挤 |

## 2. 平台可用向量算子（实测算子清单，103 个算子中筛出）

- 7 个 `vec_*`：`vec_avg(x)` `vec_sum(x)` `vec_count(x)` `vec_max(x)` `vec_min(x)` `vec_stddev(x)` `vec_range(x)`
- 14 个 `reduce_*`：`reduce_avg(input,threshold=0)` `reduce_sum` `reduce_stddev(input,threshold=0)` `reduce_max` `reduce_min` `reduce_range` `reduce_norm` `reduce_ir(input)` `reduce_skewness(input)` `reduce_kurtosis(input)` `reduce_percentage(input,percentage=0.5)` `reduce_choose(input,nth,ignoreNan=true)` `reduce_powersum(input,constant=2,precise=false)` `reduce_count(input,threshold)`
- 二阶/三阶矩只有 `reduce_*` 提供（`vec_stddev` 是唯一 vec 侧二阶矩）；`vec_ir`/`vec_skewness` **不存在**，写错即整批 CANCELLED。

## 3. 字段七轴分类（按语义，非按命名）

### A 方向 / 估值锚（目标价 vs 价格）
`target_prc` = 作者声明的目标出场价｜`prc` = 投资变动对应的价格｜`latest_prc` = 当前价｜`prev_close_prc` `closed_prc` `period_start_prc` `period_end_prc` `index_period_start_prc` `index_period_end_prc`
> 经济含义：`target_prc/prc` = 建仓时隐含空间（存量信息）；`target_prc/latest_prc` = 剩余空间（前瞻）。二者是**不同机制**，但同一「目标价溢价」族，只占 1 席。

### B 资本 / 仓位（信念强度的可观测量）
`initial_inv` `current_inv` `ang_inv`（时间加权平均投入）`net_market_exposure`（多空净敞口，**拥挤字段，规避**）`new_value` / `old_value`（止损%、目标价、资本配置三者的**修订对**）`transaction_charge`

### C 已实现 / 未实现收益
已实现：`real_ret` `real_ret_today` `real_value` `tot_ret` `tot_ret_per` `tot_ret_wo_fx` `ad_ret_per` `ad_rel_ret_per` `rel_index_ret` `rel_index_ret_per` `stock_ret_per` `stock_ret_per_relative` `ret_per_today` `rel_ret_per_today` `bm_ret` `bm_ret_wo_fx` `bm_fx_ret` `index_ret_per`
未实现：`unreal_ret` `unreal_ret_today` `unreal_value`（`risk_free_rate` 的描述"unrealised return on an open idea"实为未实现回报，非无风险利率）

### D 风险调整质量
`beta`（对市场 20 个月滚动）`jensensalpha`（超额于市场的风险调整表现）`treynor_ratio`

### E 生命周期
`days_since_inception`（建仓至今交易日数）`avg_dur`（选定期间内平均年龄）`time`（构想的时间跨度）

### F 信念标签
`probability`（量化信念度 tag）`idea_count`（组内构想数，仅用于分组场景）

### G 成本 / 汇率
`avg_initial_prc`（量加权初始买价）`avg_initial_prc_wfee`（含佣金）`inv_exchange_rate` `bm_exchange_rate` `currency_gain_percentage` `currency_gain_value`
> `avg_initial_prc_wfee − avg_initial_prc` 是**唯一可直接读出的实施成本**，经济含义 = 交易摩擦/流动性折价。

## 4. 机制假设 → 文献映射

| # | 机制假设 | 文献 / 来源 | 本数据集对应字段 |
|---|---|---|---|
| 1 | 交易构想有价格冲击，跟随构想可获显著超额收益 | **Birru, Gokkaya, Liu & Stulz (2022), JF 77(3):1829–1875**, DOI 10.1111/jofi.13130 | `target_prc`/`prc` 的方向差、`probability` |
| 2 | 基于"未来事件"的构想比"纠正错定价"的构想更有信息量 | 同上 | `time`（时间跨度）、`days_since_inception` |
| 3 | 共识目标价 `PRET=(target−price)/price` 有效性受 **dispersion 调节**，低扩散被放大 | 论坛帖《【直通通过】Consensus Analyst Target Prices》（Brav–Lehavy 线） | `reduce_stddev(target_prc)` / `vec_stddev` 做调节量 |
| 4 | 意见分歧 → 高估（Miller 1977 卖空约束 + 分歧） | 论坛《分析师共识的三种读法：水平、修订与扩散》 | `vec_stddev` / `vec_range` / `reduce_skewness` |
| 5 | 覆盖广度 = 注意力 → 短期高估后反转（Barber–Odean 注意力） | 论坛《分析师一致预期：121 个字段里最值得做的 5 个信号》 | `vec_count(target_prc)` = 活跃构想条数 |
| 6 | 修订（revision）比水平更有信息量 | 论坛《水平、修订与扩散》第三层 | `new_value` vs `old_value` |
| 7 | 分析师过往业绩可外推（herding / 明星分析师） | Altınkılıç–Hansen 2013；Crane–Crotty 2020 | `jensensalpha` `treynor_ratio` `tot_ret_per` |

## 5. 仍未知（不得当作已知）

- **历史深度未测**：平台 `get_datafields` 只返回 coverage，不返回起止日期。可交易构想库通常是较近期的产品，「近十年都有数据」这一条必须靠 `get_alpha_yearly_stats` 逐年 `longCount>0 && pnl≠0` 实测确认，**本次尚未验证**。
- **向量元素配对语义未测**：两个 VECTOR 字段做逐元素算术（如 `multiply(probability, target_prc)`）时平台如何对齐元素（同顺序？同长度才对齐？）尚无实测；若不对齐语义会退化为乱序，需用「先降维再算术」做对照。

