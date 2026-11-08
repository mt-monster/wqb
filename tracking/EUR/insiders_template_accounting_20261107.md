# EUR Insider 战役 · 模板核算表（用户质询「你试了哪些模板」的正面回答）

- 核算时间：2026-11-07｜口径：insiders 类别 3 集用 `nan_handling OFF`；`insider_feats` 用 `nan_handling ON`；其余设置同 EUR 区域档（TOPCS1600 / delay 1 / decay 4 / SUBINDUSTRY / truncation 0.08 / maxTrade OFF）
- **诚实结论先行**：模板池 21 个（NB1–NB15 + SP1–SP4 + CV1–CV2），我实际派发了 **8 个**，自建补充 **6 个**几何，`insider_feats` 上另跑 **8 个**几何 ⇒ 共 **24 条实测**。**池内仍有 13 个模板未派发**，所以之前说「已穷尽」讲早了。

## A. 已实测 24 条（模板 → alpha → 全指标）

### A1. insiders 类别（`insider_agg_matrix` / `insiders1` / `insiders12`，nanH OFF）

| 模板 | 名称 / 几何 | alpha | S | F | TO | 2Y | sub | rob | 多/空 | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| **NB1** | 净买入比率（全体董事）`divide(buy−sell, buy+sell)` | `58EGQYpJ` | 0.17 | 0.03 | **154.7%** | −0.78 | 0.30 | 0.21 | **3/3** | ❌ 持仓塌缩 + TO 爆炸 |
| **NB2** | 买入广度（隐含人数）`divide(total_buy, avg_buy)` | `YP1l5YvJ` | **0.58** | 0.20 | **114.4%** | 1.07 | 0.26 | 0.25 | **1/1** | ❌ 持仓塌缩 |
| **NB3** | 高管−全体角色背离 | `vR1YkE3v` | 0.07 | 0.01 | 19.9% | 0.06 | −0.06 | −0.30 | **0/0** | ❌ 零持仓 |
| **NB4** | 净买入趋势加速度 `ts_delta(ts_mean(NB,22),66)` | `xArlYL0b` | −0.32 | −0.10 | 29.3% | −0.25 | −0.64 | −0.09 | 42/42 | ❌ 方向错 |
| **NB8** | 平台方向指标 `group_rank(ts_mean(directional_indicator,22), industry)` | `Jje3NGzW` | −0.46 | −0.10 | 29.7% | −0.73 | — | — | 346/339 | ❌（但**定了符号**：正号=净卖出） |
| **SP1** | 卖压总额 `-group_rank(ts_sum(total_sell_shares,66), industry)` | `rKR0OEX3` | 0.36 | 0.12 | 5.9% | 0.58 | 0.21 | −0.04 | 363/318 | ❌ S 不足 |
| **SP4** | 净买卖额 66 窗（论坛对照基准） | `omEPLAMk` | 0.37 | 0.13 | 5.9% | 0.10 | 0.45 | **0.54** | 350/351 | ❌ S 不足 |
| SP4-变体 | 同 SP4 换 63 窗 + TOP2500（原样复现论坛配方） | `VkxMaGzG` | 0.56 | 0.22 | 6.35% | 0.30 | 0.25 | — | 693/681 | ❌ 论坛 S1.90 **不复现** |
| **NB15** | insiders1 欧元金额长窗 `ts_sum(vec_sum(insd1_valueeur),66)` | `O0A6NKxq` | −0.14 | −0.03 | 7.0% | −0.39 | −0.19 | 0.54 | 358/356 | ❌ 方向未知 |
| 自建-1 | insiders12 带符号金额长窗 | `P0oP2jO7` | −0.50 | −0.55 | 2.2% | −0.26 | −0.54 | −0.64 | **1/1** | ❌ cov 0.19 |
| 自建-2 | **平均单笔规模**（Seyhun 规模轴）`group_rank(ts_mean(avg_secondary_top_buy_shares,63), industry)` | `A1VLvKmR` | 0.51 | 0.20 | 6.0% | 0.72 | — | **0.64** | 227/378 | ❌ S 不足，**rob 全战役最好** |
| 自建-3 | 异常净买 z（自基线标准化）`group_zscore(divide(ts_sum(netbuy,63), ts_std_dev(netbuy,252)), industry)` | `qML50qG2` | 0.32 | 0.11 | 6.7% | 0.31 | — | 0.35 | 301/281 | ❌ 比裸水平更差 |
| 自建-4 | 集群买入强度（人数/活跃日） | `leAgKRn5` | −0.12 | −0.03 | 8.7% | 0.29 | — | −0.41 | **86/91** | ❌ 持仓过窄 |
| 自建-5 | 集群卖出强度（负号） | `GrWQO325` | −0.32 | −0.12 | 8.2% | −1.04 | — | −0.43 | **120/118** | ❌ |
| 自建-6 | **聚合后买入占比**（修 NB1 的 0/0）`divide(ts_sum(buy,63), ts_sum(add(buy,sell),63))` | `vR1Y2Xpb` | 0.48 | 0.20 | 6.2% | — | — | — | **210/219 对称** | ❌ 0/0 修好但 S 弱 |
| 自建-7 | 显著性族最大单笔 `group_rank(ts_mean(top_directional_significant_value_1,63), industry)` | `1YNGZAKk` | 0.51 | 0.20 | 6.0% | — | — | — | 217/379 | ❌ |

### A2. `insider_feats`（118 MATRIX，`_filled` 族 cov 0.9157，nanH ON，塔 EUR/D1/OTHER ×1.5）

| 模板 | 名称 / 几何 | alpha | S | F | TO | returns | 2Y | margin | 多/空 | 失败闸 |
|---|---|---|---|---|---|---|---|---|---|---|
| F1 | 预聚合金额比 60d `group_rank(buy_sell_ratio_all_60d_filled, industry)` | `mLoKYL6W` | 0.71 | 0.30 | 3.86% | 2.28% | **1.27** | 11.8bp | 637/735 | S/F/2Y |
| F2 | 预聚合笔数比 60d | `RRE5ARAj` | 0.74 | 0.33 | 3.84% | 2.45% | 1.20 | 12.8bp | 637/734 | S/F/2Y |
| F2-变体 | 同 F2 换 top5 角色 + 250d 窗 | `Jje3Ppvj` | 0.66 | 0.27 | 1.93% | 2.11% | 0.81 | **21.9bp** | 613/760 | S/F/2Y |
| F2-变体 | 同 F2 换 5d 短窗（提换手） | `6XdGAM65` | 0.72 | 0.31 | **10.47%** | 2.37% | 1.15 | **4.5bp** | 794/507 | S/F/2Y |
| F3 | **双字段秩乘积** `group_rank(multiply(rank(A), rank(B)), industry)` | `bl6x8LdM` | **0.80** | 0.37 | 3.26% | 2.61% | 1.25 | 16.0bp | 621/763 | S/F/2Y |
| F4 | buy-only 计数广度 250d `group_rank(total_buy_tx_count_250d, industry)` | `N1NKePdo` | 0.69 | 0.29 | 2.04% | 2.26% | 0.62 | 22.2bp | 530/823 | S/F/2Y |
| F5 | 幂次 3.0 on F3 | `WjOYOEzQ` | 0.81 | 0.38 | 3.87% | 2.68% | 1.11 | 13.8bp | 466/920 | S/F/**rob 0.60**/2Y |
| F5 | 幂次 3.0 on F1 | `pwdWdqGV` | 0.65 | 0.27 | 4.81% | 2.11% | 0.91 | 8.8bp | 461/912 | S/F/rob 0.61/2Y |

## B. 模板池里**还没派发**的 13 个（这是「未穷尽」的实证）

| # | 模板 | 几何 | 表达式 | 未派原因 / 备注 |
|---|---|---|---|---|
| 1 | **NB5** | 最窄角色（高管直持）净买入 | `group_rank(NB(total_secondary_top), industry)` | 应有 0/0 风险，需改聚合口径 |
| 2 | **NB6** | 广度差（买人数 − 卖人数） | `group_rank(subtract(divide(total_buy,avg_buy), divide(total_sell,avg_sell)), industry)` | 双侧 0/0，需改聚合口径 |
| 3 | **NB7** | 显著性支配度（头号/次号） | `group_rank(divide(significant_value_1, significant_value_2), industry)` | 符号未知 |
| 4 | **NB9** | 方向指标增强版 | `group_rank(ts_mean(directional_indicator_2,22), industry)` | 项目历史测过 S−0.05 / TO 1.43 |
| 5 | **NB10** | 净买入年度峰值（极值矩） | `group_rank(ts_max(NB(all),252), industry)` | 比率型 ts_max，0/0 |
| 6 | **NB11** | 机会型 z（`ts_zscore` 原算子） | `group_rank(ts_zscore(NB(all),252), industry)` | 只测过 `divide(x,ts_std_dev)` 变体，**原算子未测** |
| 7 | **NB12** | 高管单笔规模占比 | `group_rank(ts_mean(divide(avg_top_buy_shares, avg_buy_shares),22), industry)` | 均值比，0/0 |
| 8 | **NB13** | 买压基线（对照组） | `group_rank(ts_mean(total_buy_shares,66), industry)` | **第 13 波在测** |
| 9 | **NB14** | 净买入时序秩 | `group_rank(ts_rank(NB(all),252), industry)` | 未测（时序秩矩） |
| 10 | **SP2** | 卖压占比 | `group_rank(divide(total_sell_shares, add(total_buy_shares,total_sell_shares)), industry)` | 未测 |
| 11 | **SP3** | 高管卖压总额 | `group_rank(ts_sum(total_top_sell_shares,66), industry)` | **第 13 波在测**（论坛称 GLB 卖压做到 2.18） |
| 12 | **CV1** | 仓位比（交易股数/交易后持股） | `group_rank(divide(vec_sum(insd1_shares), vec_sum(insd1_holdings)), industry)` | 依赖 insiders1 方向诊断，未测 |
| 13 | **CV2** | 显著交易集中度 | `group_rank(divide(significant_value_1, add(significant_value_1,significant_value_2)), industry)` | 未测 |

## C. 池外仍未测的算子几何（不是换窗口，是换几何）

| 几何 | 算子 | 用途 |
|---|---|---|
| 时序秩 | `ts_rank` / `ts_quantile` | 把稀疏水平转成自身历史分位（NB14） |
| 偏离自身均值 | `ts_av_diff` | 机会型偏离（与 z-score 同轴不同矩） |
| 残差化 | `vector_neut` / `ts_regression` | 剔除「是否有内部人活动」这一覆盖因子 |
| 分桶 | `bucket` / `quantile` | 非线性分组，替代 group_rank |
| 门控 | `trade_when` | 只在内部人活动活跃时持仓 |
| 换手控制 | `hump` / `ts_target_tvr_decay` | 已有换手过低问题，暂无必要 |
| 二阶矩 | `ts_kurtosis` / `ts_corr` | 内部人交易与价格的相关性 |
| 符号 | `sign` | 纯方向（丢幅度）的极简对照 |

## D. 一句话结论

**已测 24 条、19 个结构互异几何；池内 13 个模板 + 池外 8 类算子几何未测。** 所以「EUR insider 面已穷尽」这个判断我撤回——正确的表述是：**已测的 24 条全部未过闸（最高 S 0.81 / F 0.38，or insiders 类别最高 0.58），且 insider_feats 存在 F 闸的 returns 结构性瓶颈（无论怎么换窗口，returns 恒定在 2.1–2.6%，而过 F≥1.0 需 S≥2.2 或 returns≥5%）**。剩余 21 个未测项正在按优先级补测。
