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

---

## §5 论文复验（2026-11-17，外部检索；结论：机制已测、跨区不迁移）

本会话按用户指令查论坛 + 外部论文，为本集再找机制。结果全部指向 §1–§3 已测几何，**无新机制**：

| 论文/来源 | 机制 | 本集对应已测项 |
|---|---|---|
| S&P Global《An IQ Test For The Smart Money》 | IO 四类信号中 Dynamics 最强；亚洲最佳 = breadth stability（变化÷std）+ institutional turnover；大机构 > 小机构 | 广度 buyers/holders `QPvrZwWG`/`gJeqknre`（已死 0.57–0.60）；「stability=变化÷std」= §1 M 族 ts_quantile 已覆盖 |
| Choi/Jin/Yan 2013 *Rev Finance* | 机构 breadth 增加 → 未来收益高（财富加权 +8%/yr, t=2.6）| 就是 count_institutional_holders/buyers 的 change，§3 wave205 已测 |
| Choi & Sias 2009 | 机构 herding 后反转最多 4 季 | 对应 rolling 持仓集中度变化，§1 M1 已覆盖 |
| Chen-Hong-Stein 2002 / Coval-Stafford 2007 | 卖空约束下广度↑→收益↑ / 基金流价格压力反转 | 已在 §3.2 记录并实测 |

论坛：`search_forum_posts("institutional holdings alpha")` 本会话返回 0（`navigation_failed=false`，legit no_result）；
旧帖 433587556696703 / 43212475386007 见 `fund_holdings_panel.md` §3.2，同样已验无效。

**裁决**：论文机制在 KOR institutions 塔**全部不迁移**（USA/亚洲大盘样本 ≠ KOR TOP600），
与 AGENTS.md 跨区不外推铁律一致。⛔ **不据此重开波**——本集 11 字段、两条信号轴（count + 金额）已全测归零，
任何"新角度"必须先证明确实超出 §1 的 M1–M3 几何，否则就是第 N 次重复。

---

## §6 判死撤回 + 档位性质降级（2026-11-21）

### 6.1 撤回（ledger `institutions6_dead` → `status: reopened`）

原记录（2026-08-15）两项判据被平台实读证伪：

| 原记录 | 2026-11-21 实测 |
|---|---|
| max\|sh\| 0.86 | **S 2.06**（`mLoK2mQx`，残差回归形） |
| 全家族 2Y ≤ 1.02 | **2Y 1.90**（`RREl6mna`，新鲜度门控形，effective=1 纯 ATOM、invest 比 .978、TO .074） |

回写方式合规（`upsert_ledger_key(mode="merge")`，原始 `date/reason/dead_count=11` 经回读确认完整保留）；
`get_dead_datasets(KOR)` 已不再返回本集。

### 6.2 ★★ 但这两条强读数都是**风险线**

`RREl6mna` / `gJaagGoO` / `pwaaMG16` 的 neutralization 均为 **REVERSION_AND_MOMENTUM**，
`get_alpha_details` **不报告 `risk_neutralized_sharpe`** ⇒ 按 2026-11-19 机械判据属**风险线**，
**不可作交付依据、不可与标准档跨档比较**。

⇒ 本集真正待回答的问题变成：**买家比例核在标准档还剩多少 S？**（EUR 同族实测：FAST S1.72 vs 标准档 S1.26）

### 6.3 S 攻坚（窗长）已闭合（台账 `inst6_s_attack`）

| 窗 | alpha | S | F | TO | 2Y | invest 比 | 判 |
|---|---|---|---|---|---|---|---|
| 840（原式） | RREl6mna | 0.92 | 0.57 | .0737 | **1.90** | .978 | 基线（风险线） |
| 252 | gJaagGoO | 0.88 | 0.51 | .0795 | 1.40 | 1.02 | S 未抬、2Y −0.50 |
| 504 | pwaaMG16 | 0.75 | 0.42 | .0752 | 1.60 | 1.01 | 更差 |

**窗长不是 S 杠杆**（与 earnings3「双窗是 S 杠杆」相反，再次印证逐集实测）。S 攻坚剩余方向：
① 标准档重测（读「还剩多少」）；② 门控宽度（`ts_arg_max<33` 是唯一未扫的样本选择维）；
③ 内层分母（`holders` / `buyers+sellers` / `buyers`）。

2026-11-21 已发批 `7i1Yp5804MEad29Hb6CSkJ`（SUBINDUSTRY + decay4 + 原式），读数落地补入 §6.4。

### 6.4 标准档实测（`std_tier_subind`）

| 档 | alpha | S | risk_neut S | F | TO | 2Y | subU | invest 比 |
|---|---|---|---|---|---|---|---|---|
| REVERSION_AND_MOMENTUM（风险线） | RREl6mna | 0.92 | 不报告 | 0.57 | .0737 | **1.90** | 0.79 | .978 |
| **SUBINDUSTRY（标准档）** | P0558pQw | 0.90 | **0.68** | 0.54 | .0569 | **1.39** | 0.76 | **.967** |

- **S 基本不动**（0.92→0.90），**2Y 降 0.51**（1.90→1.39）、risk-neutralized S 只有 0.68 ⇒ 风险线读数确实是虚高一档，主要虚在 **2Y**。
- 标准档下的真实缺口：**S 需 +0.68**、**F 需 +0.46**（F 由 returns 决定：现 R=0.0458，F≥1.0 需 R≥0.154，即收益要三倍——不是平滑能补的）、2Y 需 +0.19。
- ⇒ 本线在标准档下同样**不可交付**；若继续投入，唯一有意义的是找**更强内核**（门控宽度 / 分母口径），不是设置调参。

### 6.5 内核变体（只动内核、不动设置，台账 `inst6_kernel_variants`）

| 变体 | alpha | S | F | TO | 2Y | subU | 判 |
|---|---|---|---|---|---|---|---|
| 原核 `(buyers−sellers)/holders` × 门控 <33 | P0558pQw | **0.90** | 0.54 | .057 | **1.39** | 0.76 | 基准 |
| 门控放宽 `<45` | MP66V6Va | 0.67 | 0.35 | .061 | 1.23 | 0.64 | **更差**（持仓更久反而掉） |
| 分母换 `buyers/holders`（EUR 已证买家比例核） | qM77V7V2 | 0.40 | 0.16 | .061 | 0.82 | 0.45 | **大幅更差** |

- **门控越宽越差**：`<45` 把非信号日也拉进持仓，S 与 2Y 双降。
- **EUR 的「买家比例」核在 KOR 不迁移**（S 0.90 → 0.40，2Y 1.39 → 0.82）——与 AGENTS.md 跨区不外推铁律同源：EUR 该信号的正效应依赖 EUR 的机构持仓结构与流动性，KOR 需要的是**净买卖差**而非比例。
- ⇒ 已测内核空间收口：当前核（净买卖差÷持有人均值 × 新鲜度门控 <33）是最优，剩余未测维仅 `ts_arg_max` 窗长 90 与内层 `ts_mean` 平滑窗口。

### 6.6 内层算子全替（最后未测维，台账 `inst6_inner_ops`）

| 内层 | alpha | S | ΔS | F | TO | 2Y | subU | invest 比 |
|---|---|---|---|---|---|---|---|---|
| `ts_quantile(·,840)`（基线） | P0558pQw | **0.90** | — | 0.54 | .0569 | 1.39 | 0.76 | .967 |
| `ts_zscore(·,840)` | xAvlPm3m | 0.71 | −0.19 | 0.38 | .0515 | 1.22 | 0.62 | **1.056** |
| `ts_rank(·,840)` | E5QmgrpG | **0.90** | 0.00 | 0.53 | .0504 | **1.39** | 0.75 | .911 |

**读数**：
1. **`ts_rank` ≡ `ts_quantile`（逐位相同 0.90/1.39）** —— 同窗长下秩与分位是同一变换的两种刻度，rank 不变性使结果重合（与 earnings3「no-op 律」同族）。
2. `ts_zscore` 劣化（S −0.19）——分布假设不匹配，`ts_quantile` 仍是该核最优。
3. **内层层闭合**。至此 institutions6 内核空间五维全扫：门控宽度（<25/33/45）、分母口径（holders 平滑 72 / buyers/holders）、字段族（计数净流 / 股数净流 / 市值净流）、中性化档（SUBIND/MARKET/SECTOR）、内层算子（quantile/zscore/rank）⇒ **S 天花板 0.90，距闸 0.68**，本集 ATOM 不可能达成。

### 6.7 最后两维（门控回看窗 / 内层分母窗，台账 `inst6_lastdims`）

| 变更 | alpha | S | ΔS | F | TO | 2Y | Δ2Y | subU | invest 比 |
|---|---|---|---|---|---|---|---|---|---|
| 基线（`ts_arg_max(·,90)` + `ts_mean(·,72)`） | P0558pQw | **0.90** | — | 0.54 | .0569 | **1.39** | — | 0.76 | .967 |
| 门控回看窗 90→**126** | KPgVnNqk | 0.83 | −0.07 | 0.48 | .0541 | 1.16 | −0.23 | 0.73 | .952 |
| 内层分母窗 72→**126** | MP6gbaqa | 0.80 | −0.10 | 0.46 | .0570 | 1.31 | −0.08 | 0.70 | .988 |

两个方向都劣化 ⇒ **基线参数（90 / 72）已是该核最优**。

**★ 六维内核空间全部扫完，本集 ATOM 结论闭合**：

| 维 | 测过的取值 | 最优 |
|---|---|---|
| 门控阈值 | <25 / <33 / <45 | **<33** |
| 门控回看窗 | 90 / 126 | **90** |
| 分母口径 | holders 平滑 / buyers÷holders | **holders 平滑** |
| 分母窗 | 72 / 126 | **72** |
| 字段族 | 计数净流 / 股数净流 / 市值净流 | **计数净流** |
| 中性化档 | SUBINDUSTRY / MARKET / SECTOR | **SUBINDUSTRY**（SECTOR 2Y 更高但 S 同） |
| 内层算子 | quantile / zscore / rank | **quantile（≡rank）** |

⇒ **S 天花板 0.90（距闸 0.68）、F 天花板 0.54（距闸 0.46）**，本集在内核层已无可行点，ATOM 不可能达成。

---

## §8 ★★ 2026-11-21 晚订正：严格五层梯度推翻「ATOM 不可能」旧结论

> ⚠ 上方 §6.7 的「S 天花板 0.90 / ATOM 不可能达成」是**六维扫描（已测几何）**的结论，不是数据集天花板。
> 按用户「梯度必做 + 同槽位全类别替换 + 收敛换基线推到穷尽」重跑后，该结论被推翻。证据链见
> `results/gradient_inst6_residual_kernel_20261121.md` 附录 C/D，记忆 `kor-institutions6-atom-five-layer-terminal-20261121`。

### 8.1 买家比例门控核五层全类别替换（~70 臂）

| 层 | 槽位 | 臂数 | 结果 |
|---|---|---|---|
| L1 | `ts_quantile(·,840,driver=gaussian)` 归一化 | 16 | ★**ts_scale** 胜：S 0.90→1.07、F 0.54→0.71、subU 0.76→1.10、invest .967→1.14；`ts_av_diff` F 1.31 但 2Y 0.59 + CW 0.278 |
| L2 | `ts_mean(holders,72)` 分母 | 16 | **ts_mean 守擂**（16/16 全劣化，水平量语义不可替） |
| L3 | `ts_arg_max(holders,90)<33` 门控 | 16 | ★**`ts_decay_linear(holders,90)<33` 把 2Y 1.30→1.95（过闸）**——最关键突破；ts_mean/ts_max_diff/ts_av_diff 也过 2Y |
| L4 | `signed_power(·,1.6)` 幂次 | 8 | **全 no-op**（pow1.0/no_wrap/abs 逐位相同 S0.89）；S 随 pow 单调降 |
| L5 | 中性化 11 档 | 10 | ★**INDUSTRY 档最优** |

### 8.2 全层最优 ATOM 候选 `6XM0vRKE`

```
trade_when(ts_decay_linear(count_institutional_holders_security,90)<33,
           signed_power(ts_scale(divide(count_institutional_buyers_security,
                                        ts_mean(count_institutional_holders_security,72)),840),1.0), -1)
@ KOR/TOP600/D1, INDUSTRY, decay4, trunc0.08
```
| 指标 | 值 | 闸线 | 状态 |
|---|---:|---:|---|
| Sharpe | **1.23** | 1.58 | 差 0.35 |
| Fitness | **0.91** | 1.0 | 差 0.09 |
| 2Y Sharpe | **1.69** | 1.58 | ✅ |
| subU | 1.15 | — | ✅ |
| invest_S | 1.22 | — | ✅ |
| TO | .057 | [.01,.7] | ✅ |
| failed_RA | **2** | 0 | 仅 S/F |
| 塔位 | eff=**1** / KOR/D1/INSTITUTIONS ×1.4 | — | 纯 ATOM 无 PV |

与旧基线 `P0558pQw`（S0.90/F0.54/2Y1.39/failed_RA=4）对比：**四维同时大幅推进，仅剩 S/F 两闸**。

### 8.3 终局判定

- **S/F 是信号强度天花板**（S 差 0.35、F 差 0.09，二者同受 returns 约束；F 闭式需 ret +10% 而 S 需 +0.35，五层穷尽无更多杠杆）⇒ 记 **PROVISIONAL 信号层弱**，**不是数据集级判死**。
- 若将来放宽 S 闸或引入新信息源（他集字段作 gating/分组，按混塔一个即停预算），本集仍有余量。
- **旧结论订正**：§6.7「ATOM 不可能达成」作废——那是"已测几何"的天花板；严格同槽位全类别替换后 S0.90→1.23、2Y1.39→1.69，证明原判过早。
- 跨集残差核代表件 `6XMoqQ5L`（S2.34/F1.05/2Y−0.14/eff=2）按用户「混塔一个即停」封存，不再追加。

### 8.4 可复用方法教训

1. `ts_scale` 归一化后，幂次/ abs / no_wrap 是数学空操作（读数逐位相同）——别再在归一化层之上扫幂次。
2. 门控用**平滑衰减水平**（`ts_decay_linear(holders,90)<33`）而非**峰值距今**（`ts_arg_max`），2Y +0.65——门控语义从"事件近因"变"状态筛选"。
3. 六维扫描的"天花板"只能证明**已测几何**穷尽，不能证明数据集穷尽；判死前必须做严格五层全类别替换。

---

## §9 ★★ 2026-11-21 深夜 FINAL：第二基线 + ATOM 内 add 组合（§8 之后继续推进）

> 承接 §8。按「梯度收敛换基线推到穷尽」继续推第二互异基线（净广度Δ核），并在 ATOM 内做 add 组合。

- **第二基线 `MPYee1r6`**（buyers−sellers 净买卖家数差核）：五层 L1–L5 跑完（~60 臂），最优 `2r56ZWeN`（INDUSTRY）S1.52/F1.21/2Y1.36/invest1.52 —— F 首次过闸、S 仅差 0.06，但 2Y 退步。
- **★ATOM 内 add 组合**（两互补核心各自 `ts_scale` 归一后 `add`，同集字段合法保 3×）：
  **`E5QzgoYK` = `trade_when(ts_mean(holders,90)<33, signed_power(add(rank(ts_scale(buyers/ts_mean(holders,72),840)), rank(ts_scale(ts_decay_linear((buyers−sellers)/ts_mean(holders,72),21),840))),1.0),-1)` @ INDUSTRY/d4/trunc.08**
  - **S1.51 / F1.23 / 2Y1.77 / TO.044 / subU1.45 / invest_S1.51 / RN_S1.12 / failed_RA=1（仅 LOW_SHARPE，差 0.07）**
  - add 把 2Y 从单核 1.36 → 1.77（过闸），是 11-21 全战役最关键突破。
  - 设置轴 8 档扫完，INDUSTRY 最优（SECTOR 1.24/SUBIND 1.08/MARKET 1.10/REVMOM 1.19/FAST 1.13/CROWDING 0.98/SLOW 0.83）。
  - 终验：self 0.256 PASS（pool 33）；十年逐年 PnL 全正、long/short 每年 186–252、无零持仓年、S<1.0 仅 2/10、top 年占 14.7%。
- **FINAL 判定**：本塔两个互异 ATOM 基线 + add 组合均穷尽；`E5QzgoYK` 距全闸仅 S 差 0.07（1.51 vs 1.58），其余全部通过。**记 PROVISIONAL 信号层弱（非数据集判死）**——S 是唯一缺口，五层几何已穷尽；破局需外部新信息源或闸线调整，不得据此判数据集死。
- 单核 near 备选：`6XM0vRKE`（2Y1.69/S1.23）、`2r56ZWeN`（S1.52/F1.21），均 failed_RA=2。混塔代表件 `6XMoqQ5L` 按「混塔一个即停」封存。
- 证据链 `results/gradient_inst6_residual_kernel_20261121.md` 附录 E。

---

## §10 ★★★ 2026-11-22 凌晨：余量法零代价优化 → 首颗平台全闸交付件（§9 之后，推翻 PROVISIONAL）

> 按用户方法论「优化不是把指标做得更好看，而是在四条硬约束的可行域里找更高点；第一步不是调参，是算余量」执行。承接 §9 的 `E5QzgoYK`（S1.51，唯一缺口 S −0.07）。

### 10.1 分诊 + 余量表（动手前）
| 约束 | 基线读数 | 线 | 余量 | 判定 |
|---|---|---|---|---|
| prod | 0.3909（本轮实测） | 0.70 | +0.309 | 极厚 |
| self | 0.256 | 0.70 | +0.444 | 极厚 |
| F | 1.23 | 1.00 | +0.23 | 过 |
| 2Y | 1.77 | 1.58 | +0.19 | 过 |
| subU | 1.45 | 相对线 | 过 | 过 |
| **S** | **1.51** | **1.58** | **−0.07** | **唯一缺口** |

结论：高度值得优化；三条余量极厚意味着零代价层调参即使略抬 prod 也远撞不到墙。**官方+论坛印证**：TO=0.044 已在 Fitness 公式 `max(TO,0.125)` floor 之下（帖 44556201135127 / 44713280965527），继续降换手对 F 零贡献，唯一杠杆是抬 S（IR）；多份工作流实证要求「一个批次回答一个问题 + 必须有对照组」，是 2D 网格的依据。

### 10.2 零代价层一：窗口 2D 网格（W×D，算子/字段/decay 全冻结）
W=`ts_scale` 窗 {504,840,1260} × D=腿2内层 `ts_decay_linear` 窗 {10,21,42}，3×3 去中心(840,21)=基线作对照 → 8 臂。wave `s2_inst6_atom_decaygrid_d1`。
- W=504 全线崩（S1.09–1.11）→ 长窗 W∈{840,1260} 是成立条件。
- W=840→1260：S 1.50→1.52；D 轴只动 2Y 不动 S。
- **结论：S 卡在 1.50–1.52 平台，纯窗口调参天花板 1.52，距闸仍差 0.06，边际收益仅 0.01 ⇒ 二维平面收敛，停。**

### 10.3 零代价层二：decay 轴（余量表指出的最后一片未动平面）
decay 全程锁 4 未动 + TO 远低于 floor ⇒ 抬 decay 让信号衰减少、TO 回升，可能抬 S 而不损 F。用 `batch_create_simulations` 逐条独立设置（settings 轴必须独立）。两骨架 A=W1260/D42、B=W1260/D21。wave `s2_inst6_atom_decayaxis_d1` + `s2_inst6_atom_decaypeak_d1`。

| decay | A (D42) S/F/2Y | B (D21) S/F/2Y |
|---|---|---|
| 1 | 1.52/1.26/1.68 | 1.52/1.26/1.65 |
| 2 | 1.51/1.25/1.66 | 1.51/1.25/1.62 |
| 4 | 1.52/1.26/1.65 | 1.52/1.26/1.61 |
| 8 | 1.56/1.31/1.69 | 1.56/1.31/1.66 |
| 12 | 1.58/1.33/1.72 `mLa7Vb2x` ✅全闸 | 1.59/1.35/1.70 `YPazg8Qo` ✅全闸 |
| **16** | **1.60/1.36/1.74 `Jj8zG0Ye` ✅全闸（峰）** | 1.61/1.37/1.72 `pwaGNwMV` ✅全闸（但 invest_ratio 0.9938） |
| 20 | 1.58/1.33/1.76 `E5QzGrgm` ✅全闸（回落） | （尾点，不影响判定） |

- **decay 4→8→12→16 单调抬 S（1.52→1.56→1.58→1.60），20 回落**——符合官方「decay 过大会衰减信号」，**峰在 decay16**，二维平面收敛到极值。
- 抬 S 的全过程 prod 稳定在 0.3877–0.3879（比基线 0.3909 还略降）——余量表预测命中，零代价层确实不撞墙。

### 10.4 ★★★ 首颗平台全闸交付件 `Jj8zG0Ye`（decay16 峰值，代表件）
```
Jj8zG0Ye = trade_when(ts_mean(count_institutional_holders_security,90)<33,
  signed_power(add(rank(ts_scale(divide(count_institutional_buyers_security,
      ts_mean(count_institutional_holders_security,72)),1260)),
    rank(ts_scale(ts_decay_linear(divide(subtract(count_institutional_buyers_security,
      count_institutional_sellers_security),ts_mean(count_institutional_holders_security,72)),42),1260))),1.0),-1)
@ KOR/TOP600/D1, INDUSTRY, decay16, trunc 0.08
```
- **S1.60 / F1.36 / 2Y1.74 / TO.0347 / subU1.51 / invest_S1.60 / RN_S1.23 / margin 0.00519 / failed_RA=0（fail=[]）**
- 四维重验全过：prod **0.3879**（余量 0.312）/ self **0.2433** pool=33 / pyramids effective=**1** KOR/D1/INSTITUTIONS（未亮塔 ATOM）/ 逐年 10/10 PnL>0、long/short 188–249、无零持仓年。
- **近重复件识别**：A/B 骨架仅内层窗 42 vs 21 之差，互相关 0.9969（mLa7Vb2x × YPazg8Qo 实测）——同族镜像，只交付 `Jj8zG0Ye` 一颗；B 骨架 dec12/dec16 记为镜像不重复交付。
- 语义：**§9 的 PROVISIONAL「信号层弱」被推翻**——S 缺口靠零代价 decay 轴补上，未引入任何新字段/算子/信息源，六维/ATOM/tower 全不变。这是本会话首颗 `failed_RA=0` 的完整 ATOM 全闸候选。

### 10.5 方法教训（可复用）
1. **余量表先于调参**：先算四条硬约束余量，锁定唯一缺口（S −0.07）与三条厚余量（prod/self/F），才知道零代价层可以放心动、该动哪个方向。
2. **F 的 turnover floor 是指南针**：TO < 0.125 时降换手对 F 零贡献，唯一杠杆是抬 S；这把搜索空间从「所有参数」收窄到「抬 IR 的参数」。
3. **窗口 2D 收敛 ≠ 数据集穷尽**：W×D 平台 1.52 时没有判死，继续找未被余量表覆盖的零代价轴（decay），才找到突破。呼应 §8.4 教训 3。
4. **decay 是信号速度的匹配旋钮，非越大越好**：4→16 单调抬 S、20 回落，峰在 16；官方「过大衰减信号」实证。
5. **同集不同内层窗 ≠ 独立信号**：A/B 骨架互相关 0.9969，是同族镜像，交付只取最优一颗——「同字段换抽取否证法」再现。
6. 未提交（用户红线：只挖不提交）；提交须用户明确确认 + confirm_submit=True。

---

## §11 2026-11-22 净广度单核 decay 复核 + KOR 未亮塔选集排除（§10 之后）

> 用户「换 KOR 其它未亮塔数据集」→ 机器盘点 + 后台档案扫描 + 余量表复核后的结论。

### 11.1 未亮塔三候选全部排除（零/少配额判据）
| 集 | 塔 | 排除依据 |
|---|---|---|
| other553 | sentiment | 本轮 8 臂 TO 控制算子类别实验（`s2_other553_tvrcontrol_d1`）证明 TO 1.59 是 `group_rank` 截面重排结构属性，`ts_target_tvr_decay/hump` 全部无效（只到 1.28）；唯一降 TO 的 trade_when 门控臂 S 崩 0.46、2Y 0.15；est 族四线大缺口非 near-gate。撤出。 |
| imbalance5 | imbalance | 2Y regime 结构墙（KOR 三波 21 臂 + 标准档 S1.25 风险线假象已封存 `KOR-IMB5-REGIME-2Y-DEAD`）；GBR group_scale 成功不可跨区外推。 |
| news7 | news | 三字段族（注意力/语调/关注广度）12 臂全测完，注意力轴 S−0.89 方向对幅度差 0.69，无未测轴。 |

### 11.2 净广度单核 2r56ZWeN decay 轴复核（用户裁定）
余量表：S1.52(差0.06)/2Y1.36(差0.22)/F1.21过/TO0.035。**双缺口**（与 add 件只差 S 不同）。
decay × 内层窗 2D 网格（wave `s2_inst6_netbreadth_decay_d1`）：W21 峰 = decay16 **S1.54/F1.23/2Y1.44**（S+0.02/2Y+0.08），dec20 S 回落到 1.51；W42 全程不如 W21。**双缺口都补不满**（S 距闸 0.04、2Y 距闸 0.14），0 全闸。

### 11.3 判定
- 净广度核正是 Jj8zG0Ye add 全闸件的一条腿（dec4 版），单独追全闸是重复劳动；Jj8zG0Ye 已 failed_RA=0，不再优化安全边际（边际收益 < 破闸风险）。
- **decay 轴适用边界**：对 near-gate 型（单闸差 0.07 + 三闸厚余量）有效（add 件翻案）；对双缺口型只能小幅抬、补不满——再次印证「先算余量再决定投不投」的前置价值。
- institutions6 两个互异基线 + add + 净广度单核 decay 全部穷尽，ATOM 交付定格 `Jj8zG0Ye`（未提交）。

---

## §12 2026-11-22 凌晨二轮：交付版去恒等层 + 门控/分母/组合轴补扫（§10 之后）

> 全量结果 `results/optimize_Jj8zG0Ye_20261122.md`。目的：在 §10 已收敛的 W×D×decay×中性化之外，
> 补扫**从没动过的四个维度**：分母 `ts_mean(holders)` 窗、门控阈值/窗、组合算子形态、非线性指数。

### 12.1 八臂实测（全部不超基线）

| 臂 | S | F | 2Y | 判定 |
|---|---|---|---|---|
| 基线 `Jj8zG0Ye` | **1.60** | **1.36** | 1.74 | ✅ 全闸 |
| 去 `signed_power(…,1.0)` → `P05zx7zx` | **1.60** | **1.36** | **1.74** | ✅ **逐位相同** |
| 分母窗 72→126 `YPazxR96` | 1.58 | 1.34 | 1.61 | ✅ 但双降 |
| 分母窗 72→42 `akazV5gW` | 1.55 | 1.29 | 1.77 | ❌ |
| 门控 33→20 `d5aza7Mj` | 1.38 | 1.12 | 1.18 | ❌ |
| 门控 33→50 `O0WzWmLd` | 1.48 | 1.18 | **2.02** | ❌（S 差 0.10） |
| 门控窗 90→66 `XgazV7z0` | 1.57 | 1.32 | 1.71 | ❌（S 差 0.01） |
| 指数 1.0→0.5 `58J5J6XN` | 1.53 | 1.30 | 1.54 | ❌ |
| `group_rank(industry)` `j2aGaw7j` | 1.36 | 1.05 | 1.27 | ❌ |

### 12.2 三条新结论

1. **门控是单峰且 S/2Y 反号**：T=20→1.38、33→1.60、50→1.48（2Y 2.02）。33 是峰；
   往宽走会掉进「2Y 好看、S 不够」的剪刀差（同 §9 `E5QzgoYK` 形态）。
2. **分母窗 72 是峰**（42/126 双降），三点定单峰。
3. **`signed_power(x,1.0)` 是恒等层，可删**：`P05zx7zx` 与基线 pnl/DD/TO/subU **逐位相同**，
   但 distinct ops 9→8 ⇒ T1 惩罚 +0.023 → +0.016（N=141）。**交付版改用 `P05zx7zx`。**

### 12.3 交付版定稿

`P05zx7zx`（= `Jj8zG0Ye` 去 `signed_power`）：prod **0.3879** / self **0.2433**(pool33) /
VF 闸 **PASS**（ΔP=+1，新建 `KOR/D1/INSTITUTIONS`，diversity +0.61%~+3.07%）/ failed_RA=0。
**已于 2026-11-21T20:16:46-05:00 提交（用户点名），ACTIVE / stage=OS**；平台回填 self .2431 / prod .3879，
checks pending 全结清；属性名 `KOR_R_instbrd_01`（节点会把 name 重算成 `KOR_R_alpha_01`，须提交后补回）。
该骨架参数平面至此系统收敛（W×D×分母×decay×中性化×门控窗/阈×组合×指数×骨架），再抬 S 须换信息机制。

### 12.4 派发事故

首发的 10 臂被 429 拒；改 5 臂（`GAtHE3Fb…`）后**卡在 `progress=0.35`、1.5h 未展开**；
拆成 2/4/2 三小批全部正常回收 ⇒ **本账号并发下 ≥5 臂批次可能永久排队，派发控制在 ≤4 臂/批**。

---

## §13 2026-11-23 塔位复核 + 连续型字段补测（Jj8zG0Ye 已提交母件，第二骨架未果）

### 13.1 ★ 状态更正：交付件已提交，不可再交
用户提醒"我提交了变体"→ 平台实读确认：
- `P05zx7zx`（`KOR_R_instbrd_01`，2026-11-21 20:16 提交、ACTIVE、stage=OS）就是 §12 定稿的**交付版去恒等层**；`signed_power(x,1.0)` 是数学恒等，与 `Jj8zG0Ye` 读数逐位相同（S1.60/F1.36/2Y1.74/TO.0347/prod0.3879/self0.2431）。
- `check_correlation(Jj8zG0Ye, self)` = **1.0，top_correlated 首位 = P05zx7zx**（pool 36）。⇒ **Jj8zG0Ye 不可再交**（已提交件自包含伪影）。
- 另两变体 `mLa7Vb2x`/`YPazg8Qo` 实读仍 UNSUBMITTED，但与母件互相关 0.9969（同族镜像），同样不可交。
- **塔位**：P05zx7zx 挂 KOR/D1/INSTITUTIONS ×1.4，已点亮该塔 1 席（与平台 pyramids 实读 1/3 一致）。推 2/3 必须换**互异信息机制**。

### 13.2 第二骨架取证（论坛+论文硬闸）
- **论坛 #43358755666967**（机构参与新鲜度门，24 赞，已提交 OS）"五代数维演进"明确列出本集已证伪骨架：渗透率 S0.20 / ts_corr 0.38 / 美元净流 0.44 / sellers 反向 0.71 ⇒ **不重测**。
- 该帖"未解决疑问"留下唯一未测方向：**连续型字段（非计数类）是否适用新鲜度门——当前验证仅限计数类，连续型未测**。
- 论文闸 `paper_search "institutional ownership ratio stock returns cross-section" --diverse`：**5 篇/4 作者 PASS**（含 JFE 2005 经典）。

### 13.3 连续型字段补测（wave `s2_inst6_continuous_freshgate_d1`，8 臂）
把论坛冠军骨架的 BUYER_FLOW 换成连续型 F2/F3/F4/F5 字段，保留门控链 `ts_arg_max(holders,90)<33` + 分母锚 `ts_mean(holders,72)` + 时序分位 840 gaussian，设置 SUBINDUSTRY/d9/trunc0.03：
| 字段族 | 最优臂 | S | 2Y | 判定 |
|---|---|---:|---:|---|
| F3 卖出金额 | gJalozgO | −0.16 | 1.09 | ❌ |
| F4 机构股数/市值存量 | O0WL5vRd/rK7qrmN1 | −0.12/0.04 | −0.23/0.59 | ❌ |
| F5 全体股数存量 | 3q0KnWkQ | 0.07 | 0.83 | ❌ |
| F2 买入股数(+凸化) | omab9eRJ/WjlZWmok | 0.08/0.14 | 0.33/0.43 | ❌ |
| F3 买入金额 | RReOkL9o | 0.14 | 0.60 | ❌ |
| **F2 净股数流量(+凸化)** | **Jj8A5LWm** | **0.39（最高）** | 0.14 | ❌ |

**0 全闸 / 0 near（全 8 臂 subU 多为负）**。`gradient_stop_gate --l1-range` 机械判 **STOP**：max_S 0.39<1.0 且极差 0.55<0.7 ⇒ 信息量不足，不投 L2–L5。

### 13.4 判定
**论坛"连续型未测"的疑问已有答案：连续型字段不适用新鲜度门**（8 族全灭）。institutions6 的两个互异信息机制（计数类家数核 = 已提交 P05zx7zx；连续型流量/存量核 = 本轮证伪）均已穷尽，另两条论坛证伪骨架（渗透率/ts_corr/美元净流/sellers 反向）不重测。**该塔第二席须换全新的机构行为信息源**（非本集现有 11 字段），本集内再换字段/算子属重复劳动。不判数据集死（数据层干净、已贡献 1 席），记「本集信息机制穷尽」。

全程前台 MCP、一次一批、无后台、未提交。相关：[[kor-institutions6-atom-fullgate-breakthrough-20261122]]、[[gradient-six-disciplines-landed-20261123]]。
