# 平台算子盘点 · 未使用清单与低频算子的回测（2026-11-14 16:3x GMT+8）

> 数据源：平台实时 `GET /operators`（103 个）+ 本地库 **151,833** 条历史表达式 + 平台账号 1,530 条 alpha。
> 结论先行：**REGULAR 通道 84 个算子已 100% 名义覆盖，「从未使用」严格计数 = 0**；
> 真正未开发的是**频次极低**的 10 个（`not` 2 次、`kth_element` 11 次），本轮据此重做 30 条金融含义模板并已派发回测。

## 0 结论速览

| 项 | 数值 | 说明 |
|---|---:|---|
| 平台算子总数 | **103** | `GET /operators` 实时拉取，与 2026-09-07 本地目录逐条一致（无新增） |
| REGULAR 可用 | **84** | `scope` 字段含 `REGULAR` 才算 |
| 非 REGULAR | **19** | COMBO-only 17 + SELECTION-only 2，**Regular 表达式里写不了** |
| 本地已用 | **84 / 84** | 151,833 条表达式，覆盖率 **100%** |
| 严格「从未使用」 | **0** | 频次 >0 的 REGULAR 算子 = 84 |
| 低频未探索（<100 次） | **10** | 占 REGULAR 的 11.9%，`not` 2 次 / `kth_element` 11 次 |
| 本轮回测模板 | **30 条 / 3 批** | 覆盖 38 个算子，其中 22 个属低频族；四闸全过 + 覆盖签核 |

## 1 那 19 个「用不了」的算子

平台 `scope` 字段直接给出，三行可复现。**Reduce 整族 14 个全是 COMBO-only**——它们安静地躺在
「本季还没用过」清单里，看着像一大块肥肉，实际一个都动不了（实测写入即报错）。

| 族 | 算子 | scope | 为什么 Regular 用不了 |
|---|---|---|---|
| Reduce | `reduce_avg` `reduce_choose` `reduce_count` `reduce_ir` `reduce_kurtosis` `reduce_max` `reduce_min` `reduce_norm` `reduce_percentage` `reduce_powersum` `reduce_range` `reduce_skewness` `reduce_stddev` `reduce_sum` | COMBO | 输入契约要 `dates, alphas:N`，Regular 拿不到该维度 |
| Special | `self_corr` | COMBO | 组合层专用 |
| Special | `combo_a` `generate_stats` | COMBO | 组合层专用 |
| Special | `in` `universe_size` | SELECTION | 选股层专用 |

论坛佐证：[Operators used 的分母不是 103：Regular Alpha 能用的只有 84 个](https://support.worldquantbrain.com/hc/zh-cn/community/posts/42641705861655)
（TO38154，2026-08-11）独立算出同样的 84/103，并指出 `ts_backfill` / `group_backfill` 在六维 Operators used 里豁免不计 ⇒ 可计分池 82 个。

## 2 频次分布：名义覆盖 ≠ 实质探索

| 使用频次 | 算子数 | 占 REGULAR |
|---|---:|---:|
| 0 次（从未使用） | 0 | 0.0% |
| 1–4 次 | 1 | 1.2% |
| 5–19 次 | 1 | 1.2% |
| 20–99 次 | 8 | 9.5% |
| 100–999 次 | 28 | 33.3% |
| ≥1000 次 | 46 | 54.8% |

**10 个低频算子（<100 次 / 151,833 条表达式）**：

| # | 算子 | 类别 | 使用次数 | 频次占比 |
|---:|---|---|---:|---:|
| 1 | `not` | Logical | 2 | 0.0013% |
| 2 | `kth_element` | Time Series | 11 | 0.0072% |
| 3 | `greater_equal` | Logical | 67 | 0.0441% |
| 4 | `power` | Arithmetic | 72 | 0.0474% |
| 5 | `is_nan` | Logical | 74 | 0.0487% |
| 6 | `ts_step` | Time Series | 85 | 0.0560% |
| 7 | `ts_product` | Time Series | 88 | 0.0580% |
| 8 | `pasteurize` | Arithmetic | 90 | 0.0593% |
| 9 | `group_sum` | Group | 92 | 0.0606% |
| 10 | `sqrt` | Arithmetic | 92 | 0.0606% |

`not` 只用过 2 次、`kth_element` 11 次——这两个不是「不会用」，而是**从没进入过模板设计**。
论坛建议的切入点正好对上：**Logical 整族（11 个）全 REGULAR 可用，且是条件化写法**，与多数人长期用的加权求和骨架是两套东西。

## 3 论坛模板来源

| 帖子 | 用途 |
|---|---|
| [167 操作符全示例](https://support.worldquantbrain.com/hc/zh-cn/community/posts/38213050258839)（JX79797） | 每个算子的官方签名 + 示例（AMR d1 实测通过），本轮全部模板的语法底本 |
| [Operators used 分母 84](https://support.worldquantbrain.com/hc/zh-cn/community/posts/42641705861655)（TO38154） | REGULAR 84 口径、Reduce 族不可用、逐位不动的替换清单、`sqrt`/`log`/`tanh` 的实测位移 |
| [kth_element 用法](https://support.worldquantbrain.com/hc/zh-cn/community/posts/36539251668375)（WF37935） | `kth_element(x, d, k=1)` 的 k **必须命名传参**，否则报错 |

论坛给出的两条硬警告已写进本轮设计：`sqrt` 在特定结构上 S 掉 1.5+、`hump` 砍换手七成且 fitness 掉六成——
所以本轮 `sqrt` 只做**低波溢价**单一用途（不做外层再套），`hump` 不碰。

## 4 本轮 30 条模板（按算子族）

设置：`USA / TOP3000 / D1 / decay 4 / SUBINDUSTRY / trunc 0.08 / nanHandling ON / 2013-01-01~2023-12-31`（取自 `tracking/USA/config/settings.json`）。

| 批 | # | 主算子 | 金融含义 | 表达式 |
|---|---:|---|---|---|
| B1 | 1 | `not` | 5 日动量转负才开反转仓 | `trade_when(not(greater(ts_delta(close, 5), 0)), rank(-ts_delta(close, 5)), -1)` |
| B1 | 2 | `greater_equal` | 高波动分位（>=0.8）才做短期反转 | `if_else(greater_equal(rank(ts_std_dev(returns, 20)), 0.8), rank(-returns), 0)` |
| B1 | 3 | `less_equal` | 相对量能低（<=0.3 分位）才做 VWAP 均值回复 | `trade_when(less_equal(ts_rank(volume / adv20, 20), 0.3), rank(-ts_delta(vwap, 3)), -1)` |
| B1 | 4 | `equal` | 中期趋势向上时做短期反转 | `trade_when(equal(sign(ts_delta(close, 20)), 1), rank(-ts_delta(close, 5)), -1)` |
| B1 | 5 | `is_nan` | VWAP 缺失率作流动性质量信号（缺失多给负权） | `rank(-ts_mean(is_nan(ts_delta(vwap, 1)), 20))` |
| B1 | 6 | `not_equal` | 短中期动量方向背离时做反转 | `trade_when(not_equal(sign(ts_delta(close, 5)), sign(ts_delta(close, 20))), rank(-returns), -1)` |
| B1 | 7 | `greater` | 收益 z 超过 2 倍标准差时清仓（极值规避） | `if_else(greater(abs(ts_zscore(returns, 60)), 2), 0, rank(-ts_zscore(returns, 60)))` |
| B1 | 8 | `is_nan` | 有成交数据才持有低波组合（not∘is_nan 复合） | `trade_when(not(is_nan(ts_delta(close, 1))), rank(-ts_std_dev(returns, 20)), -1)` |
| B1 | 9 | `and` | 短中期同向上行时才持反转（双条件合取） | `if_else(and(greater(ts_delta(close, 5), 0), greater(ts_delta(close, 20), 0)), rank(-ts_delta(close, 5)), 0)` |
| B1 | 10 | `or` | 5 日或 20 日大跌后抄底（析取门控） | `if_else(or(less(ts_delta(close, 5), -0.03), less(ts_delta(close, 20), -0.08)), rank(-ts_delta(close, 5)), 0)` |
| B2 | 11 | `ts_kurtosis` | 低峰度偏好（规避厚尾） | `rank(-ts_kurtosis(returns, 60))` |
| B2 | 12 | `ts_product` | 20 日复合动量 | `rank(ts_product(1 + returns, 20))` |
| B2 | 13 | `power` | 收益 z 的保号幂压缩（abs(z)^0.5） | `rank(sign(ts_zscore(returns, 60)) * power(abs(ts_zscore(returns, 60)), 0.5))` |
| B2 | 14 | `sqrt` | 低波动溢价（波动率平方根） | `rank(-sqrt(ts_std_dev(returns, 60)))` |
| B2 | 15 | `group_std_dev` | 行业内收益分歧度（低分歧溢价） | `rank(-group_std_dev(ts_zscore(returns, 60), industry))` |
| B2 | 16 | `group_sum` | 行业内 5 日动量总量（行业轮动） | `rank(group_sum(ts_delta(close, 5), sector))` |
| B2 | 17 | `group_count` | 行业内有效标的数（小行业溢价） | `rank(-group_count(1, industry))` |
| B2 | 18 | `pasteurize` | 价格偏离 VWAP 的 z 分（先清 INF） | `rank(pasteurize(ts_zscore(close / vwap - 1, 20)))` |
| B2 | 19 | `ts_count_nans` | 日收益缺失次数（数据完整度溢价） | `rank(-ts_count_nans(ts_delta(close, 1), 120))` |
| B2 | 20 | `kth_element` | 一年与两年价格水平差（长周期变化） | `rank(kth_element(close, 250, k=1) - kth_element(close, 500, k=1))` |
| B3 | 21 | `ts_step` | 价格与时间趋势的相关性（趋势强度反转） | `rank(-ts_corr(close, ts_step(252), 252))` |
| B3 | 22 | `normalize` | 收益 z 的截面去均值 | `-normalize(ts_zscore(returns, 20))` |
| B3 | 23 | `ts_covariance` | 量价协方差（放量下跌风险） | `rank(-ts_covariance(returns, ts_delta(volume, 5), 60))` |
| B3 | 24 | `min` | 收益与量能两维 z 取较小（保守双确认） | `rank(min(ts_zscore(returns, 20), ts_zscore(volume / adv20, 20)))` |
| B3 | 25 | `inverse` | 相对换手倒数（低换手溢价） | `rank(inverse(ts_mean(volume / adv20, 20)))` |
| B3 | 26 | `vec_range` | 分析师聚类估计分歧度（低分歧溢价） | `rank(-vec_range(anl16_clusterestsup))` |
| B3 | 27 | `vec_min` | 风险报价最悲观值 | `rank(vec_min(rsk60_offer))` |
| B3 | 28 | `vec_range` | 社媒热度分布极差（低分歧溢价） | `rank(-vec_range(scl12_buzzvec))` |
| B3 | 29 | `vec_min` | 社媒热度最悲观值 | `rank(vec_min(scl12_buzzvec))` |
| B3 | 30 | `vec_range` | 风险报价分歧度（幂压缩） | `rank(-power(vec_range(rsk60_offer), 0.5))` |

**覆盖**：38 个算子（38/84 = 45.2% 的 REGULAR 池），其中 22 个属低频族；
`not` `greater_equal` `less_equal` `equal` `is_nan` `not_equal` `ts_kurtosis` `ts_product` `power` `sqrt`
`group_std_dev` `group_sum` `group_count` `pasteurize` `ts_count_nans` `kth_element` `ts_step`
`normalize` `ts_covariance` `min` `inverse` `vec_range` `vec_min` 全部落地。

## 5 发批前四闸（全部通过）

| 闸 | 结果 | 备注 |
|---|---|---|
| ① `op_arity` 参数数 | OK | **抓出 `is_not_nan` 不在平台目录**（论坛有、平台无，误用即整批 CANCELLED），已改为 `not(is_nan(...))` |
| ② 算子存在性（REGULAR scope） | OK | 38 个算子全部含 `REGULAR` |
| ③ 字段存在性 | OK | 8 个字段在 USA(region_id=1) 实测存在：pv1 覆盖 1.0、VECTOR 0.82–1.0 |
| ④ 单位闸 | OK | 无 `group_*(x, bucket(...))` 未 rank 的写法；无 `vector_neut` 轴错配 |
| 覆盖签核 | 已写 `results/op_coverage_signoff.jsonl` | coverage 45.24% |

## 6 回测批次

| 批 | multisim id | 条数 | 内容 |
|---|---|---:|---|
| B1 | `2usFprdZV4hsc2ZApbbUJW` | 10 | Logical 族条件化（not / greater_equal / less_equal / equal / is_nan / not_equal / and / or） |
| B2 | `3RSBiE4WY53N9xpenv6hOaw` | 10 | 分布形状 + 组内统计 + 缺失修补（ts_kurtosis / ts_product / power / sqrt / group_std_dev / group_sum / group_count / pasteurize / ts_count_nans / kth_element） |
| B3 | `1enkcpaAR4hMajO1k6QclZU` | 10 | 记忆/截面/协方差/向量（ts_step / normalize / ts_covariance / min / inverse / vec_range / vec_min） |
| B4 | `LGbNSb4R4kmcH91aiVpqH1e` + `30NbMLbbG4WNcLE1fzKiDOw3` | 12 | **修正批**：绕开 USA reversion 政策（全非价格反转）+ 修 3 个单位族错误 + 修 kth_element 中和 |

回测结果与失效分析见 [`lowfreq_operator_backtest_20261114.md`](lowfreq_operator_backtest_20261114.md)：18/42 指标可读，**双闸通过 0 条**；唯一有价值方向是「数据质量类」——`ts_count_nans` S.90/F.86/TO.04、`is_nan` 量能缺失 2Y 1.81/sub 1.00，定位应是辅助腿/门控而非主信号。

## 7 口径与边界

- **平台账号口径**：`GET /users/self/alphas` 深度分页在 `offset ≥ 1100` 返回异常（list 长度 1），
  故账号侧只取到 1,530 条（OS 430 + IS 1,100）；该口径覆盖 72/84，缺的 12 个是 `equal` `greater_equal`
  `inverse` `kth_element` `less_equal` `min` `not` `pasteurize` `ts_count_nans` `ts_covariance` `ts_product` `ts_step`
  ——**恰好就是本轮主攻的低频算子**，与本地库口径不冲突（本地库证明历史用过，频次 2–53411）。
- **Reduce 族不可用是结构性的**，不是遗漏；`in` / `universe_size` 只在 SELECTION 通道。
- 本轮为探索性回测，**只挖不提交**；结果出来后按 `LOW_SHARPE≥1.58 / LOW_FITNESS≥1.0 / 2Y / self<0.7 / prod<0.7 / CW` 全闸筛。
- 论坛的算子位移表是**单一账号、特定结构**的读数，跨区跨结构不保证复现——本轮统一 USA 设置，结论不外推到其它区。
