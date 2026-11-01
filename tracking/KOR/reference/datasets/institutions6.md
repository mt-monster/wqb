# institutions6 · KOR/D1/TOP600 字段画像与机制库

> ## ⛔ 本数据集已判死（2026-10-30）
>
> `ledger_kv` 键 `institutions6_dead` 命中 ⇒ **不得再投配额**（`pipeline.py` 的 `dead_dataset_guard()`
> 会拦下开波）。同塔另一集 `fund_holdings_panel` 亦已判死 ⇒ **institutions 塔整体关闭**。
> 判死依据见 §3 实测读数（4 条探针全部 S < 0.61，连 1.0 的 near 线都够不着，
> 距 1.58 闸差 ~2.6 倍）。本文画像与字段表保留作历史/跨区参考，**不要据此再开波**。

> 数据集：`institutions6`（Institutional Ownership — 13F 式机构持股计数/流量类）
> 区域/宇宙/Delay：KOR / TOP600 / D1 · 塔位：**institutions（已关闭）** · 倍率 ×1.6
> 建档：2026-10-30（wave 205 依据）· 状态：**⛔ 判死（wave 205 实测）**

---

## §0 数据集选择

| 候选 | 覆盖 | 字段 | 平台 aC | 判断 |
|---|---|---|---|---|
| **institutions6** | **0.9976–1.0** | 11 | 60–249 | ✅ 选它：KOR 少见的高覆盖慢变量，季频阶梯披露 |
| 其他 category 队列 | — | — | — | 见 `_inventory_kor_d1_20261030.md` §4 |

选它的三条理由：
1. **覆盖率 1.0 量级**——KOR 新闻类只有 0.63，慢变量覆盖高，事件稀疏问题天然不存在。
2. **季频慢披露 ⇒ 换手低**——正面对冲 w203 的失败指纹（news 家族 TO>1.05，信号日频翻转）。
3. **塔位空白**：institutions 塔 KOR/D1 未点亮（0/3），且论坛已有 IND 同集冠军配方可迁移检验。

---

## §0.1 字段质量先验（alphaCount 降序）

| 字段 | 类型 | 覆盖 | aC | uC | 描述要点 |
|---|---|---|---|---|---|
| `aggregate_share_count_institutions` | MATRIX | 0.9976 | **249** | 143 | 机构持有总股数（期末） |
| `aggregate_share_count_all_owners` | MATRIX | 1.0 | 206 | 120 | 全体持有人总股数（去重父子） |
| `aggregate_equity_value_institutions` | MATRIX | 0.9976 | 114 | 82 | 机构持有总市值 |
| `quantity_institutional_shares_acquired` | MATRIX | 1.0 | 116 | 69 | 期间买入股数 |
| `market_value_institutional_shares_acquired` | MATRIX | 1.0 | 110 | 59 | 期间买入金额 |
| `quantity_institutional_shares_disposed` | MATRIX | 1.0 | 107 | 57 | 期间卖出股数 |
| `count_institutional_sellers_security` | MATRIX | 1.0 | 98 | 68 | **卖出机构家数** |
| `aggregate_equity_value_all_owners` | MATRIX | 1.0 | 90 | 63 | 全体持有市值 |
| `count_institutional_buyers_security` | MATRIX | 1.0 | 85 | 61 | **买入机构家数** |
| `count_institutional_holders_security` | MATRIX | 1.0 | 60 | 39 | **持有机构家数（参与广度基数）** |
| `market_value_institutional_shares_disposed` | MATRIX | 1.0 | 59 | 44 | 期间卖出金额 |

**头部轴判读**：aC 最高的是「持有股数/市值」这类**存量规模**（已高度拥挤，249/143），
而 **家数类（buyers/sellers/holders，aC 60–98）反而是低拥挤度的一层**。
⇒ 经济轴 = **参与广度（多少家机构在动）**，不是持仓规模。这与「未充分挖掘的高覆盖字段」一致。
⚠ 按 `brain-alpha-research-field-quality` §1：头部字段常给出最强经济轴 —— 这里头部是规模，
但规模已被挖穿（aC 249），所以**轴跟着拥挤度走，而不是跟着 aC 数值走**。

---

## §0.2 字段分类（以 description 为准）

| 族 | 字段 | 语义 | 时间性 |
|---|---|---|---|
| **F1 参与广度（计数）** | `count_institutional_buyers_security` / `count_institutional_sellers_security` / `count_institutional_holders_security` | 本季增持家数 / 减持家数 / 持有家数 | 季频阶梯 |
| **F2 流量（股数）** | `quantity_institutional_shares_acquired` / `_disposed` | 期间买入 / 卖出股数 | 季频流量 |
| **F3 流量（金额）** | `market_value_institutional_shares_acquired` / `_disposed` | 期间买入 / 卖出金额 | 季频流量 |
| **F4 存量（机构）** | `aggregate_share_count_institutions` / `aggregate_equity_value_institutions` | 机构持有总股数 / 总市值 | 季频存量 |
| **F5 存量（全体）** | `aggregate_share_count_all_owners` / `aggregate_equity_value_all_owners` | 全体持有人总股数 / 总市值（含散户） | 季频存量 |

**name vs description 差异表**（漏掉的资产都在这里）：

| 字段名暗示 | description 实际 | 影响 |
|---|---|---|
| `aggregate_*_all_owners` 像是「机构+散户」 | 明确「**去重父子持有人**」 | 可安全做 `institutions / all_owners` 的**渗透率**（F4/F5），不必担心重复计数 |
| `count_institutional_holders_security` 像「股东数」 | 「**holds > 0** 的机构家数」 | 是**参与基数**，可做分母锚；不是持仓量 |
| `quantity_*_acquired` 像「净买入」 | 是**单边买入总量**，卖出在 `_disposed` | **净额必须自己 `subtract`**，字段本身不含净额 |
| `market_value_*` 像「市值」 | 是**期间成交金额**（流量） | 与 F4 的「期末市值」量纲不同，不能直接相减 |

---

## §0.3 字段画像五问 + 预处理决策

| # | 问题 | 答案（来自 §0.1–0.2 读数） | ⇒ 预处理决策 |
|---|---|---|---|
| 1 | 时间维度 | **存量（F4/F5）+ 流量（F2/F3）混装** | 存量取 `ts_delta`；流量可水平直接用（铁律 A 只约束「中心趋势单边恒正」的存量） |
| 2 | 相对性 | 水平差异（股数/家数量纲差异极大） | 必须 `rank` / `divide` 归一化，禁裸水平 |
| 3 | 被定价的是谁 | **参与广度（家数）** > 规模（已被 aC 249 挖穿） | 主腿走 F1；规模只作对照 |
| 4 | 有无博弈 | 有——机构拥挤 → 崩盘风险（论坛实证 NCSKEW +14.8%） | 需**状态门控**（参与度新鲜度），不是纯截面水平 |
| 5 | 事件性 | **非事件型**（覆盖 1.0，每季都有值） | 可裸 rank；但**季频阶梯需平滑分母**（`ts_mean(holders,72)`）剥离披露跳变 |

**关键预处理结论**：
- 季频 ⇒ 窗口下限 63d（论坛实测「63 天保留信号最好」）。
- `ts_backfill` 不需要（覆盖 1.0）。
- `divide` 的分母必须用 `ts_mean(...,72)` 平滑，否则季度阶梯跳变会污染比值（论坛实测这是 FT>1.0 的首破点）。

---

## §1 机制概念块（A-3，供 GEM/手工复用）

### M1 · 参与新鲜度门 × 买家广度比值（★ 本波主腿，IND 已 18/18 PASS）

**Concept**: 机构参与的「时间结构」而非水平——覆盖人数峰值距今越近 = 拥挤交易刚完成；峰值已过 + 买家/持有人比值抬升 = 新价值判断者在逆势吸筹。
- **Fields Used**: count_institutional_buyers_security, count_institutional_holders_security
- **Definition**: `divide(buyers, ts_mean(holders,72))` → `ts_quantile(·,840,driver=gaussian)` → `signed_power(·,1.6)`，外层 `trade_when(ts_arg_max(holders,G)<T, ·, -1)`
- **Logical Meaning**: 被定价的是**慢披露信息的扩散时滞**（13F 季末 + 最长 45 天披露延迟）。机构不是连续调仓，而是季度内集中介入；参与度「突增→保持→回落」的节奏就是定价滞后窗口。错在**注意力与资金同步性**：拥挤刚形成时价格被推高无人接盘，参与已落定后买家比值抬升才是真信号。修复期 = 1–2 个季度。
- **Directionality**: 门条件成立（峰值距今 < T 日）时，买家/持有人比值分位越高 ⇒ 未来一季超额收益越高（正向）。
- **Boundary Conditions**: 计数类字段（连续型未验证）；G/T 需按披露节奏重扫；`ts_arg_max` 作**门控**有效、作**信号**是摧毁器（本族 864/958/1097 三次实证）。
- **Expected Exposure**: flow
- **Implementation Example**: `trade_when(ts_arg_max(count_institutional_holders_security, 90) < 33, signed_power(ts_quantile(divide(count_institutional_buyers_security, ts_mean(count_institutional_holders_security, 72)), 840, driver=gaussian), 1.6), -1)`

### M2 · 净广度（breadth of ownership）Δ

**Concept**: 增持家数 − 减持家数 = 机构净参与广度变化。Chen-Hong-Stein 型：卖空约束下广度上升携带乐观信息。
- **Fields Used**: count_institutional_buyers_security, count_institutional_sellers_security
- **Definition**: `ts_delta(subtract(buyers, sellers), 63)`
- **Logical Meaning**: 被定价的是**意见分歧的可表达程度**；有卖空约束时，看空者只能不持有，广度下降才是负信息的载体。修复期 1 季。
- **Directionality**: 净广度上升 ⇒ 未来正收益。
- **Boundary Conditions**: ⚠ **IND 同族已证伪**（「美元净流」0.44 / 「sellers 反向」0.71 / 「渗透率比值」0.20）——本区若重启须换窗口与门控，不得裸跑。
- **Expected Exposure**: flow
- **Implementation Example**: `hump(subtract(rank(ts_delta(subtract(count_institutional_buyers_security, count_institutional_sellers_security), 63)), 0.5), hump=0.003)`

### M3 · 机构黏性（持仓相对换手）

**Concept**: 持有基数相对当季交易量越高 = 越「黏」的机构底盘 ⇒ 浮筹少、价格冲击大。
- **Fields Used**: aggregate_share_count_institutions, quantity_institutional_shares_acquired, quantity_institutional_shares_disposed
- **Definition**: `subtract(rank(ts_mean(holdings,63)), rank(ts_mean(add(acq,disp),63)))`
- **Logical Meaning**: 被定价的是**浮筹稀缺性**；黏性持仓降低可交易供给，同等信息冲击下价格弹性更高。修复期数季。
- **Directionality**: 黏性高 ⇒ 正向（低换手溢价）。
- **Boundary Conditions**: 与规模高度相关，需中性化；未实测。
- **Expected Exposure**: liquidity
- **Implementation Example**: `hump(subtract(rank(ts_mean(aggregate_share_count_institutions, 63)), rank(ts_mean(add(quantity_institutional_shares_acquired, quantity_institutional_shares_disposed), 63))), hump=0.003)`

---

## §2 双通道取证

### 通道 A｜论坛（已读全文）

| 帖 | 关键内容 | 采信 |
|---|---|---|
| #43358755666967「机构参与"新鲜度门"」（IND，23 票，已提交 OS） | **冠军配方全文**：`trade_when(ts_arg_max(holders,90)<33, signed_power(ts_quantile(divide(buyers,ts_mean(holders,72)),840,driver=gaussian),1.6), -1)`；SUBINDUSTRY / decay 9 / trunc 0.03；S 1.62 / FT 1.37 / 2Y 2.47 / 18 项全 PASS；分年 2014–2023 全正或微正 | ✅ 主腿原样迁移 + 设置重扫 |
| 同帖「五代数维演进」 | 同族**已证伪**：裸比值不可行 / `ts_corr(buyers,holders,66)` 0.38 / 美元净流 0.44 / 渗透率 0.20 / sellers 反向 0.71 | ⛔ 五类结构不进 KOR quota |
| 同帖「门控轴」 | G∈[66,180]×T∈[22,45]：**66/33 与 90/33 是甜点**；66/22 崩到 1.02；G≥120 单调衰减；G 66→90 使 ROBUST +0.21 | ✅ 只测 90/33 与 66/33，**不重扫全网格** |
| 同帖「分母轴 / 凸化轴」 | `ts_mean(_,72)` 分母锚是 FT>1.0 首破点；`signed_power(1.6)`+W=840 高斯分位 = 18 项 PASS；分母窗 m↑ ⇒ 曲线平滑下降、SH 上升（1.45→1.62） | ✅ M 轴取 126 一点（延伸 m↑ 方向）；p 轴取 2.0 |
| #43151729306647「institutions18 拥挤反转」（GLB） | 机构持仓变化 → 拥挤反转 | 存档，未采（GLB 不可跨区照搬） |
| 「13F 披露时滞下的思考」（institutions18） | 13F 最长季末后 45 天披露 ⇒ 慢扩散窗口真实存在 | ✅ 机制支撑（Boundary 写入 M1） |
| 「信息比率分解：广度、深度与 Alpha 组合效率」 | 广度 vs 深度是两套独立信息 | ✅ M1 用广度、规模存量作对照 |
| 「机构持仓结构：谁在买、谁在挤 — IVA/MFM/CNI 三分法」 | 保险/顾问型持仓比例高 ⇒ 底盘稳 | 存档（需 CNI 字段，本集无） |

### 通道 B｜外部论文

| 论文 | 结论（可证伪） | 采信 |
|---|---|---|
| **Chen, Hong & Stein (2002), "Breadth of Ownership and Stock Returns", JFE 66** | 卖空约束下，**持有广度的变化**（而非水平）预测横截面收益：广度上升 ⇒ 未来收益高 | ✅ M2 的机制出处（但 IND 已证伪实测，**降为存档**） |
| **Gabaix & Koijen (2023), "In Search of the Origins of Financial Fluctuations: The Inelastic Markets Hypothesis"** | $1 机构资金流入 → 约 $5 市值提升，且**流量停止后价格影响仍持续** ⇒ 参与变化未被即时定价 | ✅ M1 的方向句与修复期（1–2 季） |
| **Feng, He, Wang & Xiao (2026), "Active Mutual Fund Co-Holdings and the Buy-Side Peer Network"** | 机构参与变化 → 下月焦点股超额收益，**形成后持续而非反转**，且集中在高摩擦小盘股 | ✅ M1 的持有期与「小盘更有效」边界 |
| **Da, Larrain, Sialm & Tessada (2016), "Coordinated Noise Trading: Evidence from Pension Fund Reallocations"** | 协调性大额机构流造成价格短暂偏离，随后回补 ⇒ 参与「突增→保持→回落」节奏即窗口 | ✅ M1 的时间结构 |
| **Gabaix, Gopikrishnan, Plerou & Stanley (2005), "Institutional Investors and Stock Market Volatility"** | 大机构在流动性不足市场制造无基本面 price spike | ✅ 门控另一侧（拥挤期退出）的依据 |

### 双通道裁决

| 机制 | A（论坛） | B（论文） | 裁决 |
|---|---|---|---|
| **M1 新鲜度门 × 买家广度** | 有完整可落地模板 + IND 18/18 实证 | Gabaix-Koijen + Feng 2026 + Da 2016 三方支撑方向与持有期 | ⭐ **A∩B 同向 ⇒ 最高优先**（本波主腿） |
| M2 净广度 Δ | 同族 5 类结构全灭 | Chen-Hong-Stein 支撑机制 | ⛔ **A 实证否决优先于 B 理论**：不采（本波已删） |
| M3 机构黏性 | 无对应帖 | 无直接论文 | 降级存档，不占本波配额 |

⚠ **跨区警示**：M1 全部实证在 **IND/TOP500**，KOR 的 13F 式披露节奏、机构化程度、TOP600 流动性均不同 ⇒ **只作假说，必须本区实测**（铁律：杠杆逐字段/逐族实测，不可跨区移植）。

---

## §3 实测记录（wave 205，已收批）

multisim `1ip4rtgDn4nLbtR6OrLGi2n`，设置统一 SUBINDUSTRY / decay=9 / truncation=0.08 / KOR TOP600 D1。

| 波 | alpha | 表达式骨架 | S | 2Y | Fit | TO | 结论 |
|---|---|---|---|---|---|---|---|
| 205 | `QPvrZwWG` | `trade_when(ts_arg_max(holders,90)<33, signed_power(ts_quantile(buyers/ts_mean(holders,72),840,driver=gaussian),1.6), -1)` | **0.60** | 0.86 | 0.31 | 0.056 | ⛔ 距闸 2.6× |
| 205 | `gJeqknre` | 同上 G=66 | **0.57** | 1.24 | 0.29 | 0.060 | ⛔ 距闸 2.8× |
| 205 | — | M=126 / p=2.0 两条 | — | — | — | — | 已 dropped（死集硬闸拦截后未发） |

全维读数（两条一致）：CW / subU / investability / TO 全 PASS，**只卡 S / Fit / 2Y** ——
即「结构干净、强度不足」，不是可修的参数问题。`sub_universe_sharpe` 0.47 / 0.46 ≈ 主 S，
说明不是大盘股独有；`risk_neutralized_sharpe` 0.59 / 0.67 与 raw 同量级 ⇒
**信号自身弱（铁律 E 的「raw 与 RN 同步走弱」分支 ⇒ 换字段/机制族，不是换中性化档）**。

⚠ 由此关塔，不留 "再试一次" 的口：同塔 `fund_holdings_panel` 亦在死表 ⇒
**institutions 塔 0/3 位全部判死**（`ledger_kv`: `institutions6_dead` / `fund_holdings_panel_dead`）。

## §4 近十年数据核验（用户硬要求 #4）— ✅ 通过

`QPvrZwWG` 的 `get_alpha_yearly_stats`（2014–2023 逐年）：

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| longCount | 189 | 262 | 276 | 280 | 294 | 299 | 301 | 302 | 297 | 283 |
| shortCount | 182 | 237 | 244 | 255 | 265 | 259 | 256 | 284 | 278 | 290 |
| Sharpe | 0.33 | 0.83 | 1.16 | **-0.21** | 0.44 | **-0.01** | 0.64 | 0.89 | 0.62 | 1.08 |

- **十年数据完整**：每年多空各 180–300 只，无整年空白 ⇒ 用户硬要求 #4 达标。
- **但逐年 S 分布致命**：S<1.0 占 **8/10**，其中 2 年为负 ⇒ 按铁律「S<1.0 年份 ≥3 成 ⇒ 2Y 结构性不可达」，
  该结构在任何 decay/窗口参数档都过不了 2Y 闸。
- ⭐ **归因结论：这是「信号弱」的死，不是「数据缺」的死** —— 同一判据要用于后续每个候选集
  （数据够 ≠ 该集能出 alpha；两者必须分开核）。
