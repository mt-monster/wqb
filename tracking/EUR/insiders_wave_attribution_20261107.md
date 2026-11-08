# EUR / Insiders 战役归因台账

- 日期：2026-11-07｜区域 EUR（固定）｜目标 10 个 ATOM regular alpha（REGULAR 通道，提交线 S>=1.58）
- 已实测 **16 条**，**全部未过闸**，历史最强 **S 0.58**（`YP1l5YvJ`），最好 robust 0.64（`A1VLvKmR`）；交付进度 **0/10**
- 数据集面：EUR 全平台仅 3 个 insiders 集（`insider_agg_matrix` 34 MATRIX 字段 cov 0.61 / `insiders1` 9 VECTOR cov 0.55 / `insiders12` 8 VECTOR cov 0.19 UK-only）

## 1. 已实测全表（按 S 降序）

| # | alpha | 骨架 | universe | S | F | TO | 2Y | sub | rob | 多/空 | 主要失败闸 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `YP1l5YvJ` | `group_rank(divide(total_buy_shares, avg_buy_shares), industry)`（买入广度=隐含人数） | TOPCS1600 | **0.58** | 0.20 | **114.4%** | 1.07 | 0.26 | 0.25 | **1/1** | 7 闸 |
| 2 | `VkxMaGzG` | `group_rank(ts_sum(subtract(total_top_buy_shares,total_top_sell_shares),63), industry)`（论坛配方） | **TOP2500** | 0.56 | 0.22 | 6.4% | 0.30 | 0.25 | - | 693/681 | LOW_SHARPE / LOW_FITNESS / LOW_2Y / LOW_SUB |
| 3 | `omEPLAMk` | 同 #2 但 **66 窗 / TOPCS1600** | TOPCS1600 | 0.37 | 0.13 | 5.9% | 0.10 | 0.45 | **0.54** | 350/351 | LOW_SHARPE / F / rob / 2Y |
| 4 | `rKR0OEX3` | `-group_rank(ts_sum(total_sell_shares,66), industry)`（卖压侧） | TOPCS1600 | 0.36 | 0.12 | 5.9% | 0.58 | 0.21 | -0.04 | 363/318 | LOW_SHARPE / F / rob / 2Y |
| 5 | `Jje3NGzW` | `group_rank(ts_mean(directional_indicator,22), industry)`（平台方向指标，**未翻号**） | TOP2500 | -0.46 | -0.10 | **29.7%** | -0.73 | - | - | 346/339 | LOW_SHARPE / F / 2Y |
| 6 | `58EGQYpJ` | `group_rank(divide(subtract(buy,sell), add(buy,sell)), industry)`（净买比率） | TOPCS1600 | 0.17 | 0.03 | **154.7%** | -0.78 | 0.30 | 0.21 | **3/3** | HIGH_TURNOVER / CONCENTRATED_WEIGHT |
| 7 | `P0oP2jO7` | `group_rank(ts_sum(vec_sum(insd12_positionchangetransactionamount),66), industry)` | TOPCS1600 | -0.50 | -0.55 | 2.2% | -0.26 | -0.54 | -0.64 | **1/1** | 6 闸 |
| 8 | `O0A6NKxq` | `group_rank(ts_sum(vec_sum(insd1_valueeur),66), industry)` | TOPCS1600 | -0.14 | -0.03 | 7.0% | -0.39 | -0.19 | 0.54 | 358/356 | 5 闸 |
| 9 | `vR1YkE3v` | 高管净买比率 − 全体净买比率（角色背离） | TOPCS1600 | 0.07 | 0.01 | 19.9% | 0.06 | -0.06 | -0.30 | **0/0** | 6 闸 |
| 10 | `A1VLvKmR` | `group_rank(ts_mean(avg_secondary_top_buy_shares,63), industry)`（高管直持**平均单笔规模**，Seyhun 轴） | TOPCS1600 | 0.51 | 0.20 | 6.0% | 0.72 | - | **0.64** | 227/378 | LOW_SHARPE / F / rob(0.64) / 2Y |
| 11 | `qML50qG2` | `group_zscore(divide(ts_sum(netbuy,63), ts_std_dev(netbuy,252)), industry)`（异常净买 z，CMP2012 机会型） | TOPCS1600 | 0.32 | 0.11 | 6.7% | 0.31 | - | 0.35 | 301/281 | LOW_SHARPE / F / rob / 2Y |
| 12 | `1YNGZAKk` | `group_rank(ts_mean(top_directional_significant_value_1,63), industry)`（显著性族最大单笔，a=5/u=5） | TOPCS1600 | 0.51 | 0.20 | 6.0% | - | - | 217/379 | LOW_SHARPE / F / rob / 2Y |
| 13 | `vR1Y2Xpb` | `group_rank(divide(ts_sum(top_buy,63), ts_sum(add(top_buy,top_sell),63)), industry)`（**聚合后**买入占比） | TOPCS1600 | 0.48 | 0.20 | 6.2% | - | - | **210/219**（对称） | LOW_SHARPE / F / rob / 2Y |
| 14 | `A1VLvKmR`-族 | 见 #10 | | | | | | | | |
| 15 | `leAgKRn5` | `group_rank(ts_mean(divide(total_secondary_top_buy_shares,avg_secondary_top_buy_shares),63), industry)`（集群买入度） | TOPCS1600 | -0.12 | -0.03 | 8.7% | 0.29 | - | **86/91** | 4 闸 |
| 16 | `GrWQO325` | `-group_rank(ts_mean(divide(total_secondary_top_sell_shares,avg_secondary_top_sell_shares),63), industry)`（集群卖出度） | TOPCS1600 | -0.32 | -0.12 | 8.2% | -1.04 | - | **120/118** | 4 闸 |
| 17 | `xArlYL0b` | `ts_delta(ts_mean(<净买比率>,22),66)`（趋势） | TOPCS1600 | -0.32 | -0.10 | 29.3% | -0.25 | -0.64 | -0.09 | 42/42 | 6 闸 |

## 2. 归因：三层结论

### 2.1 第一层——稀疏集上「比率型」公式结构性失效（已确证）
`divide(buy-sell, buy+sell)` 对**无内部人交易**的股票是 0/0，`nanHandling OFF` 直接把它剔出宇宙，持仓塌缩：
- 净买比率 → **3 多 / 3 空**（`58EGQYpJ`）
- 买入广度 `total/avg` → **1 多 / 1 空**（`YP1l5YvJ`），Sharpe 由 1-2 只股票决定，读数无意义
- 角色背离 → **0 多 / 0 空**（`vR1YkE3v`）
- `insd12` 长窗求和 → **1/1**（cov 0.19）

**修正形态：水平量 + 长窗聚合**（`ts_sum(净买, 63/66)`）。对无交易股票天然是 0 而非 NaN，不产生覆盖注入，持仓恢复到 350+/350+，换手从 155% 降到 5.9%。
但**修正覆盖率换不来 Sharpe**：换手降到 5.9% 后 S 仍只有 0.37——说明低 S 不是覆盖问题，是**信号本身弱**。

### 2.2 第二层——「近十年有数据」已达标，弱是信号弱不是年份缺口
`VkxMaGzG`（TOP2500 / 63 窗）逐年：

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| S | 0.08 | 0.69 | **1.85** | 1.12 | 0.30 | 1.10 | 0.89 | **-0.78** | 0.66 | **-0.23** |
| 多头数 | 576 | 619 | 649 | 686 | 698 | 700 | 728 | 790 | 774 | 713 |

⇒ 十年 **longCount 576-790 全部 > 0、pnl 全部非零**，覆盖闸达标；Sharpe 在 2016 曾到 1.85 但 2021/2023 转负，**全期均值约 0.57**。
⇒ 该信号对 regime 敏感（2021 成长股崩盘 + 2023 银行股行情），不是稳定可提交的件。

### 2.3 第三层——论坛 S1.90 配方在本配置下不复现（重要负结论）
论坛公开配方 `ts_sum(top_buy - top_sell, 63)` on EUR/TOP2500：
- 我按 **TOP2500 / 63 窗 / SUBINDUSTRY / decay 4 / nanH OFF** 原样复现 → **S 0.56 / F 0.22 / 2Y 0.30**，与声称的 S1.90 差 1.34。
- 差异不是 universe（已用 TOP2500）、不是窗口（已用 63）、不是方向（方向若反 S 会是 -0.56，仍不是 1.9）。
- 最可能解释：论坛读数出自**不同回测期**（如 2010-2018，我这里是 2014-2023 含 2021/2023 两个负年）或不同 `pasteurization`/`delay` 档。
⇒ **不要再用论坛的 S1.90 当可行性锚**，它在本账号当前设置下不成立。

## 3. `directional_indicator` 符号约定（本次解决）
`group_rank(ts_mean(directional_indicator,22), industry)` 直接取正 → **S -0.46**（TOP2500）。
⇒ **正号 `directional_indicator` = 净卖出方向**；做多信号需加前导负号（`-` 后预期 S 约 +0.46、TO 29.7%）。
⇒ 22 日均值下换手 29.7%，说明它是**快信号**；相比净买水平族（5.9% 换手），它才是事件型；后续应在 5-10 窗测试其衰减速度。

## 4. 已关闭 / 待测模板族

| 族 | 状态 | 证据 |
|---|---|---|
| F1 净买比率（divide 型） | **关闭** | 3/3 持仓塌缩 + 155% 换手 |
| F2 买入广度（total/avg） | **关闭** | 1/1 持仓塌缩 |
| F3 角色背离（高管 − 全体） | **关闭** | 0/0 持仓塌缩 |
| F4 净买水平 + 长窗求和 | 已测，上限 S 0.56 | #2 #3，rob 0.54 是唯一亮点 |
| F5 卖压水平 + 长窗求和 | 已测，S 0.36 | #4 |
| F6 趋势（ts_delta） | **关闭** | #10 S -0.32 |
| F7 `insd12` 符号额长窗 | **关闭** | #7 S -0.50、1/1 持仓 |
| F8 `insd1_valueeur` 金额长窗 | 弱，方向未知 | #8 S -0.14、持仓 358/356 健康 |
| F9 平台方向指标（快信号） | **在测** | #5 已定符号；第 6 波测快几何 |
| F10 平均单笔规模（Seyhun 规模轴） | **已测，最好 rob** | `A1VLvKmR` S 0.51 / **rob 0.64** / 2Y 0.72；多空 227/378 仍不对称 |
| F11 异常净买入 z-score（CMP 2012 机会型） | **关闭** | `qML50qG2` S 0.32 劣于裸水平 0.37-0.56 ⇒ 自基线标准化方向错，原始水平量更好 |
| F12 `significant_value_1..4` 显著性梯度 | **未测** | 符号未知（最高优先级待诊断） |
| F13 `top_directional_significant_value_*` 角色×显著性 | **未测** | 同上 |
| F14 `avg_secondary_*` 最严口径（高管直持） | **已测（就是 F10 的载体）** | `A1VLvKmR` |
| F16 集群买入/卖出强度（人数/活跃日 = breadth） | **关闭** | 第 7 波 `leAgKRn5` −0.12 / `GrWQO325` −0.32，持仓数塌到 86–120 |
| F17 聚合后买入占比（修 F1 的 0/0） | **已测，持仓问题修好但 S 仍弱** | `vR1Y2Xpb` S 0.48，多空 **210/219 完全对称** ⇒ 0/0 修法有效，但 S 上不去 |
| F18 显著性族 `top_directional_significant_value_1` | **已测** | `1YNGZAKk` S 0.51，217/379 |
| F15 `vector_neut` 去覆盖注入（净买 ⊥ 活跃度） | **未测** | 平台有 `vector_neut(x,y)`，可做横截面投影剔除 |

## 5. 在飞与下一步

- 在飞：`4b1tEJ7Jy4Jmaz0OjRl9CYl`（第 7 波，TOPCS1600，nanH OFF，decay 4，SUBINDUSTRY）
  - C `group_rank(ts_mean(divide(total_secondary_top_buy_shares, avg_secondary_top_buy_shares), 63), industry)` ← F16 买入集群度（人数/活跃日）
  - D `-group_rank(ts_mean(divide(total_secondary_top_sell_shares, avg_secondary_top_sell_shares), 63), industry)` ← F16 卖出集群度（负号）
- 已收：第 6 波 `g74LV5Sd4Zxb1aFZyHDAAF` → `qML50qG2` S 0.32 / `A1VLvKmR` S 0.51（rob 0.64）
- 下一步优先级：F12/F13 显著性族（字段自带符号，可能绕开 0/0）> F9 快信号衰减曲线 > F15 `vector_neut` 去覆盖

## 6. ★★★★★ 过程教训：本类别早在 2026-10-13 就已判死，我重走了 8 波

`Claude/skills/wq-brain-ra-eur/references/insiders.md` 的「判死记录」表里有一条：

> `EUR-INSIDER-AGG-MATRIX-COLD-ZERO-YIELD`｜内部人买入股数比例与二级买入广度｜命中 EUR profile fast_kill（新集 8 探针无 |S|>=0.5）｜insider_agg_matrix｜payload

同页还明确写了三件事：
- `insiders1`（9 VECTOR，cov 0.551）：8/8 探针 S<=0.50、**TO 1.52–1.61**、margin 0.1–1.2bp ⇒ 判死；
- `insiders12` cov **0.193 < 0.35** ⇒ 直接跳过；
- `insider_agg_matrix`：`directional_indicator_2` S −0.05 且 **TO 1.43**；`directional_significant_value_*` 同族 ⇒ 判死；
- ⇒ **insiders 类别 3 个数据集全部判死**，且有跨区 negative 结论（KOR/DEU/USA/EUR）。

**代价**：我今天从零重跑 8 波 16 条，得到同一个结论（上限 0.58）。差别只在 TO：项目历史读数 TO 1.43（nanH ON），我用 nanH OFF 把 TO 压到 6%，S 仍上不去 ⇒ 证实**低 S 的根因不是换手、不是覆盖，是信号本身**。

**纪律（已写入 Agent Memory）**：开波前必读 `Claude/skills/wq-brain-ra-<region>/references/<category>.md` 的「判死记录」+「胜绩」两表，再决定要不要派发。

## 7. 诚实的可行性判断

16 条实测、8 波、3 个数据集，面上限 0.58，距提交线 1.58 差 1.00。
论坛唯一对标配方不复现。insiders12 结构性不可用（cov 0.19 + 1/1 持仓）；insiders1 无买卖方向字段。
⇒ 剩余可挖面只在 `insider_agg_matrix` 的显著性族（`significant_value_1..4` / `top_directional_significant_value_1..4`）与平均单笔规模族。
若这两族仍在 0.7 以下，则「EUR Insiders 单类产出 10 个 S>=1.58 ATOM」在结构上不成立，需要用户在**同区换 category**与**放宽 S 线**之间做取舍。

---

## 8. ★ 换道 insider_feats（EUR 另一个 insider 交易数据集，平台类别=other）

**为什么换**：insiders 类别 3 个数据集已穷尽（§1–§7，16 条，上限 0.58）。EUR 另有 3 个 insider 交易数据集被平台归在 **other** 类，其中 `insider_feats`（118 MATRIX 字段、`_filled` 族 cov **0.9157**、约 95% 字段 a0/u0）历史曾出现 **S 1.11** 读数，是 EUR 唯一曾过 1.0 的 insider 数据。塔位实测 = **EUR/D1/OTHER，multiplier 1.5**（OTHER 未点亮，合规可挖）。

### 8.1 实测 6 条（全部未过闸，但全面优于 insiders 类别）

| alpha | 表达式 | S | F | TO | returns | 2Y | margin | 多/空 | 失败闸 |
|---|---|---|---|---|---|---|---|---|---|
| `bl6x8LdM` | `group_rank(multiply(rank(buy_sell_tx_count_ratio_all_60d_filled), rank(buy_sell_ratio_top20_250d_filled)), industry)` | **0.80** | 0.37 | 3.26% | 2.61% | 1.25 | 16.0bp | 621/763 | S / F / 2Y |
| `RRE5ARAj` | `group_rank(buy_sell_tx_count_ratio_all_60d_filled, industry)` | 0.74 | 0.33 | 3.84% | 2.45% | 1.20 | 12.8bp | 637/734 | S / F / 2Y |
| `6XdGAM65` | `group_rank(buy_sell_tx_count_ratio_all_5d_filled, industry)` | 0.72 | 0.31 | **10.47%** | 2.37% | 1.15 | **4.5bp** | 794/507 | S / F / 2Y |
| `mLoKYL6W` | `group_rank(buy_sell_ratio_all_60d_filled, industry)` | 0.71 | 0.30 | 3.86% | 2.28% | **1.27** | 11.8bp | 637/735 | S / F / 2Y |
| `N1NKePdo` | `group_rank(total_buy_tx_count_250d, industry)` | 0.69 | 0.29 | 2.04% | 2.26% | 0.62 | 22.2bp | 530/823 | S / F / 2Y |
| `Jje3Ppvj` | `group_rank(buy_sell_tx_count_ratio_top5_250d_filled, industry)` | 0.66 | 0.27 | 1.93% | 2.11% | 0.81 | 21.9bp | 613/760 | S / F / 2Y |

**三条全面优于 insiders 类别**：① 持仓广度 613–794（insiders 类别 210–350）；② **完全没有 rob / sub 闸失败**（insiders 类别每条都崩这两闸）；③ 2Y 最高 **1.27**（insiders 类别最高 1.07）。

### 8.2 ★★★★★ 决定性负结论：换手与单笔超额精确反向抵消，returns 打不上去

同一族信号只换窗口，得到一条极干净的对照链：

| 窗口 | alpha | TO | margin | returns |
|---|---|---|---|---|
| 250d（top5） | `Jje3Ppvj` | 1.93% | **21.9bp** | 2.11% |
| 60d | `RRE5ARAj` | 3.84% | 12.8bp | 2.45% |
| **5d** | `6XdGAM65` | **10.47%** | **4.5bp** | 2.37% |

⇒ 换手放大 **5.4 倍**（1.93%→10.47%），margin 缩小 **4.9 倍**（21.9bp→4.5bp），**returns 几乎不动（2.11%→2.37%）**。
⇒ **「靠短窗提换手来抬 returns」这条路被实测封死**。该信号的单位时间信息量是固定的。

### 8.3 F 闸的可行性算式（本集真正的瓶颈）

`F = S × sqrt(returns / max(TO, 0.125))`；本集 TO 恒 < 0.125 ⇒ `F = S × sqrt(returns/0.125)`。

| 目标 S | 过 F=1.0 所需 returns | 我的实测 returns | 结论 |
|---|---|---|---|
| 1.58（提交线） | **5.01%** | 2.11–2.61% | 差约 2 倍 |
| 1.80 | 3.86% | 同上 | 差 1.5 倍 |
| 2.20 | 2.58% | 同上 | **要 S≥2.2 才能用现 returns 过 F** |

⇒ **即使 S 达标，F 也会把本集卡死**；而反过来，要用现 returns 过 F，需要 S ≥ 2.2，而我实测最高 0.80、历史最高 1.11。
⇒ 这与项目历史判死条目 `EUR-INSIDER-FEATS-WEAK` 的记载（returns 天花板 3.9% ⇒ 需 S≥1.84）在机制上一致，只是我这次把「为什么 returns 打不上去」用窗口对照链直接证明了。

### 8.4 剩余未测杠杆（按预期增益排序）

| # | 杠杆 | 依据 | 状态 |
|---|---|---|---|
| 1 | `signed_power` 幂次 3.0 | 项目记载「S/F 提升器」 | **❌ 已测无效**（见 8.6）：`WjOYOEzQ` S 0.80→0.81 但 2Y 1.25→1.11、新增 rob 0.60 失败、持仓失衡 466/920；`pwdWdqGV` S 0.71→0.65 全面变差 |
| 2 | `*_volume_*` 族（Seyhun 规模轴） | 全族 a0/u0 未测 | 未测 |
| 3 | `ts_delta` 变化结构（非水平） | 记载「ts_delta 可提 TO 而不杀 S」 | 未测 |
| 4 | 中性化换 INDUSTRY / universe 换 TOP2500 | 记载 EUR 上 INDUSTRY 提 rob | 未测 |
| 5 | `_2` 后缀字段语义差异 | 未知 | 未测 |

### 8.6 第 12 波：`signed_power` 幂次 3.0 实测无效

| alpha | 表达式 | S | F | TO | returns | 2Y | rob | 多/空 |
|---|---|---|---|---|---|---|---|---|
| `WjOYOEzQ` | `signed_power(<bl6x8LdM 的乘积>, 3.0)` | 0.81 | 0.38 | 3.87% | 2.68% | 1.11 | **0.60 新失败** | 466/920 |
| `pwdWdqGV` | `signed_power(group_rank(buy_sell_ratio_all_60d_filled, industry), 3.0)` | 0.65 | 0.27 | 4.81% | 2.11% | 0.91 | 0.61 | 461/912 |

对照基线：`bl6x8LdM` S 0.80 / 2Y 1.25 / 无 rob 失败 / 621-763；`mLoKYL6W` S 0.71 / returns 2.28% / 2Y 1.27。
⇒ 幂次把权重压向两端：S 基本不动（+0.01 / −0.06），returns 微动（+0.07pp / −0.17pp），但**2Y 双降、rob 新失败、持仓从 621/763 失衡成 466/920**。**净负，弃用。**

### 8.5 诚实总和判断

**insider 交易数据在 EUR 的结构上限**：insiders 类别 S 0.58（16 条）；insider_feats S 0.80（6 条）/ 历史 1.11。两条线都**未过 F 闸**，且 insider_feats 的 F 闸是**数学上不可达**（returns 瓶颈）。
⇒ **「EUR insider 数据产出 10 个 S≥1.58 且 F≥1.0 的 ATOM regular alpha」目前无任何可行路径证据。**
