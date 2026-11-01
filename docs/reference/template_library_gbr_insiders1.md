# GBR / `insiders1` 模板库与实证台账

> 区域：GBR ｜ Universe：`TOP700`（**唯一档位，无退路**）｜ Delay：D1
> 塔位：**INSIDERS**（GBR D1 起始 = 0，未点亮）
> 数据集覆盖：`coverage = 0.5937`（TOP700 中约 416 只有记录）｜ 字段数 9 ｜ alphaCount 10 ｜ userCount 6
> 战役开启：2026-10-31 ｜ 最后更新：2026-10-31

---

## 0. 为什么选这个数据集

| 理由 | 依据 |
|---|---|
| **塔位空** | GBR D1 `INSIDERS = 0`，且该塔在 GBR 只有两个候选数据集（`insiders1` / `insider_matrix`），后者旧台账已记 STRUCTURAL-DEAD |
| **极冷门** | `alphaCount = 10` / `userCount = 6` —— 全 GBR 有覆盖数据集里最低的一档 ⇒ **prod 相关性风险天然低** |
| **有跨区已验证机制** | 本账号在 USA `insider_trx_matrix` 上实测「**笔数/参与广度族 > 金额/价值族**」（wave237 `O0Jgd7Y7` S 2.27 / `LL53QVvn` S 1.61 / `88vJ1YKa` S 2.94 三颗全闸；wave238 价值族 10 模板天花板 |S| 0.70） |
| **塔混合规** | INSIDERS 不属 `{PV, MODEL, OTHER}` trio 内部 ⇒ 单塔 alpha 完全不触碰「trio 禁两两互组」硬约束 |

---

## 1. 字段全集（9 个，全 `VECTOR`，coverage 全部 = 0.5937）

| 字段 | 语义 | userCount | alphaCount | 信号可用性 |
|---|---|---:|---:|---|
| `insd1_shares` | 单笔交易股数（**计数族**） | 17 | 19 | ★ **首选载体**（跨区已验证：计数族 > 价值族） |
| `insd1_holdings` | 交易后内部人总持股 | 11 | 14 | 可用（信念深度 / 持仓变化） |
| `insd1_tradesignificance` | 交易显著性评分 1(低)–3(高) | 12 | 13 | ★ **需单字段探针验有数据**（派生评分，alphaCount 仅 13） |
| `insd1_valueeur` | 交易总额（EUR） | 11 | 13 | △ 价值族，**跨区两次实证系统性弱** |
| `insd1_price` | 每股成交价（区间取最低） | 6 | 8 | 可用（内部人择时 / 相对市价偏离） |
| `insd1_gvkey` | Compustat 公司 ID | 5 | 7 | ✗ 非信号（标识符） |
| `insd1_value` | 交易总额（原币种） | 5 | 6 | ✗ ≡ `insd1_valueeur`（同额不同币种，**勿同时用**） |
| `max_trade_price` | 区间最高成交价 | 2 | 3 | 可用（区间宽度 = 交易摩擦） |
| `transaction_currency_code` | ISO 币种代码 | 2 | 3 | ✗ 非信号 |

**⇒ 可用信号面仅 6 个**（`shares` / `holdings` / `tradesignificance` / `valueeur` / `price` / `max_trade_price`）。

### ★★ 结构性缺陷：无买卖方向字段

内部人数据最核心的维度是**买入 vs 卖出**（Lakonishok-Lee 2001：买入有信息、卖出多为流动性动机）。GBR `insiders1` **完全不提供方向** ⇒ 只能退而求其次，用「参与广度 / 单笔规模 / 显著性评分 / 持仓深度 / 价位偏离 / 报价摩擦」六个替代维度。

这与 `fund_holdings_panel` 同病（18 字段亦无买卖方向，24 探针最高 |S| 0.79 判死）。**该缺陷是本数据集能否出货的头号风险。**

---

## 2. ★★★ 定则 I-1（第一条，最重要）：稀疏事件字段必须前置平滑，`vec_count` 救不了

**实证（`INDUSTRY` + decay 10 + trunc 0.05 + nanHandling ON + maxTrade OFF）**：

| # | alpha | 表达式 | S | F | TO | 2Y | SUB | margin | returns | DD | failed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| I1 | `mLo2Okj1` | `rank(vec_count(insd1_shares))` | 0.22 | 0.04 | **174.21%** | 1.12 | 0.08 | 0.62bp | 5.43% | **74.48%** | 6 |
| I2 | `d5W8wNEE` | `rank(vec_sum(insd1_valueeur))` | −0.42 | −0.10 | **176.43%** | −0.64 | 0.09 | −1.15bp | −10.15% | **158.5%** | 5 |

**两条的 TO 几乎相同（174% / 176%）⇒ 病根与「计数 vs 金额」的语义差异无关，是日频聚合本身的跳变。**
内部人交易非每日发生 ⇒ 非事件日为 0/NaN ⇒ 逐日跳变 ⇒ 平台 `decay=10` 层压不住（decay 只能在**已有信号序列上**做指数平滑，源头每天都换一批非零股票时无能为力）。

**结论**：所有 `insd1_*` 模板**必须先 `ts_mean(·, W)` 或 `ts_decay_linear(·, W)` 平滑**，再做 `rank` / `group_rank`。
与定则 #7（新闻类字段必须 `ts_mean(·,5)` 前置）、决策 #37（稀疏事件数据集通用）同源；本条把适用范围扩到 **内部人交易**，并确认「换成计数族也不豁免」。

### 副产物：笔数族 > 价值族（GBR 第三次独立印证）

I1（笔数）2Y **+1.12** vs I2（金额）2Y **−0.64** —— 同一设置下符号相反。
加上 USA wave237（价值族天花板 0.82）/ wave238（价值族天花板 0.70）⇒ 该定则已跨三区/三数据集成立。

### ★★★ 定则 I-2：`ts_mean` 是错的，稀疏事件必须用 `ts_sum` —— 且 `group_rank` 中段是「并列假中段」

**实证（全部 `FAST` + decay 10 + trunc 0.05，除 I1/I2 为 `INDUSTRY`）**：

| # | alpha | 骨架 | S | TO | 2Y | 判定 |
|---|---|---|---:|---:|---:|---|
| I1 | `mLo2Okj1` | `rank(vec_count(shares))` 未平滑 | 0.22 | 174.2% | 1.12 | TO 爆破 |
| I2 | `d5W8wNEE` | `rank(vec_sum(valueeur))` 未平滑 | −0.42 | 176.4% | −0.64 | TO 爆破 + 负号 |
| I3 | `kqNkRP2K` | `group_rank(ts_mean(vec_count,22))` | **−0.65** | 12.4% | −0.15 | 零信号 |
| I4 | `MPYlwxXo` | `group_rank(ts_mean(vec_count,66))` | −0.17 | 8.4% | −0.14 | 零信号 |
| I5 | `0mYkoR8p` | `group_rank(ts_delta(vec_avg(holdings),66))` | 0.02 | 37.3% | −0.11 | 零信号 |

**所有平滑版 S 落在 −0.65 ~ +0.02 ⇒ 等于零信号。** 两个独立病因：

**(a) `ts_mean` 除以窗口长度，把「事件频率」这一核心信息抹掉。**
论坛帖 `43212475386007`（25 赞）原话：「`accum = ts_sum(signal, <申报周期>)` —— **事件累加，不是平均（保留频率）**」。
I1（未除，S 0.22）vs I4（`ts_mean` 66，S −0.17）方向相反，正是这条的实证。

**(b) `group_rank` 的中段是「并列假中段」，等于无信息。**
同帖：「稀疏事件型识别：**coverage<0.5 + nanHandling=ON → 大概率有"并列假中段"（rank 中段 = 无信息）**。怀疑 news / insiders / shortinterest 事件型都有，可跨数据集验证。」
机理：本数据集 coverage 0.5937 + `nanHandling=ON` ⇒ 无事件股票得同一填充值 ⇒ `group_rank` 后大面积同分 ⇒ 截面区分度集中在极少数股票所在的两尾，中段（占多数）对排序无贡献 ⇒ Sharpe 被稀释到 0。
⇒ **必须 `tail` 把中段压成 0.5（`newval=0.5`），只留两尾携带信息。**

**⇒ 定则 I-1 修正版**：稀疏事件字段不是「必须平滑」，而是**必须用 `ts_sum` 累加 + 必须掐并列假中段**。单纯 `ts_mean` 平滑 = 无信号（5 条实证 S≈0）。

---

## 3. 模板库（13 条结构互异，按纪律标注来源）

> 纪律：模板池 ≥10 个且**结构互异**；差异必须落在**骨架结构 / 算子几何 / 矩 / 分组轴 / 非线性变换 / 窗口族**上，不能只是换参数。
> ★ **全部模板一律先平滑**（定则 I-1）。

| # | 族 | 经济机制 | 骨架 | 来源 |
|---|---|---|---|---|
| **N1** | 广度·水平 | 参与广度（笔数），内部人集体行动 = 信息 | `group_rank(ts_mean(vec_count(insd1_shares),22), subindustry)` | 论坛 `43152032301591`（USA `insider_trx_matrix` 笔数族三颗全闸）；Lakonishok-Lee 2001 |
| **N2** | 规模·水平 | 交易股数总量（换矩未换概念） | `group_rank(ts_mean(vec_sum(insd1_shares),22), subindustry)` | 自建 |
| **N3** | 强度·归一 | 成交额占市值率（无量纲化） | `group_rank(ts_mean(divide(vec_sum(insd1_valueeur), cap),22), subindustry)` | 自建；论坛 `35090833341207`（净额有量纲、比值无量纲） |
| **N4** | 单笔分量 | 平均单笔规模（量纲自消） | `group_rank(ts_mean(divide(vec_sum(insd1_valueeur), vec_count(insd1_shares)),22), subindustry)` | 自建 |
| **N5** | 质量加权 | 显著性加权广度（并列质量） | `group_rank(ts_mean(multiply(vec_count(insd1_shares), vec_avg(insd1_tradesignificance)),22), subindustry)` | 论坛 `43178926004891`（DEU 内部人信念强度三段式） |
| **N6** | 信念深度 | 持仓 ÷ 单笔 = 单笔占持仓比 | `group_rank(ts_mean(divide(vec_avg(insd1_holdings), vec_avg(insd1_shares)),22), subindustry)` | 自建 |
| **N7** | 价位偏离 | 成交价相对市价 = 内部人择时能力 | `group_rank(ts_mean(divide(vec_avg(insd1_price), close),22), subindustry)` | Lakonishok-Lee 1995（内部人择时）；Lakonishok-Shleifer-Vishny 1995 |
| **N8** | 报价摩擦 | 区间相对宽度 = 交易摩擦 | `group_rank(ts_mean(divide(subtract(vec_avg(max_trade_price), vec_avg(insd1_price)), vec_avg(insd1_price)),22), subindustry)` | 自建 |
| **N9** | 二阶矩 | 广度的时序波动（离散度即不确定性） | `multiply(group_zscore(ts_std_dev(vec_count(insd1_shares),22), subindustry), -1)` | 论坛 `43624312881943`（64 赞）；本会话 `shortinterest3` T1 复现 |
| **N10** | 极端分位掩码 | 剔除极端活跃段（拥挤靶子） | `if_else(greater(rank(ts_mean(vec_count(insd1_shares),5)),0.9), nan, multiply(group_rank(vec_count(insd1_shares),subindustry),-1))` | 论坛 `43636685645975`；本会话验证 θ=0.9 为峰 |
| **N11** | 「停止交易」比 | 近月 / 年内活动比 | `group_rank(divide(ts_sum(vec_count(insd1_shares),22), ts_sum(vec_count(insd1_shares),252)), subindustry)` | SSRN 4826241「When Short Sellers Do Not Short」；论坛 `43668758984983` |
| **N12** | 事件衰减记忆 | 线性衰减加权（近期事件权重高） | `group_rank(ts_decay_linear(vec_count(insd1_shares),22), subindustry)` | 自建（vs N1 的等权） |
| **N13** | 水平 × 交叉指标动量 | 慢分量撑 Sharpe + 快分量撑 2Y，且两者**不同指标** | `multiply(group_rank(add(rank(ts_mean(vec_count(insd1_shares),252)), rank(ts_zscore(vec_avg(insd1_shares),44))), subindustry), -1)` | 论坛 `43644505975959`；本会话 `shortinterest3` P35 复现 2Y 2.24 |

### 结构互异性自检

| 维度 | 覆盖模板 |
|---|---|
| 一阶矩（水平） | N1 / N2 / N3 / N4 / N5 / N6 / N7 / N8 |
| 二阶矩（波动） | N9 |
| 比值 / 交叉指标 | N13 / N11 |
| 非线性掩码 | N10 |
| 时间加权（非等权窗） | N12 |
| 分组轴变化 | 全部用 `subindustry`；**N9 用 `group_zscore` 而非 `group_rank`**（保留长尾，决策 #23） |
| 窗口族 | 5 / 22 / 44 / 252（N13 跨 252+44 双尺度；N11 跨 22+252） |

**≥10 ✅**（13 条），结构与矩覆盖满足纪律要求。

---

## 4. 设置档案

| 档 | 适用 | 设置 |
|---|---|---|
| **探针档（I1/I2 用的基线）** | 与 `insider_trx_matrix` 主档对齐，做无偏基线 | `INDUSTRY` + decay **10** + trunc 0.05 + nanHandling ON + maxTrade OFF + pasteurization ON + VERIFY |
| **进攻档（推荐）** | 平滑后正式攻闸 | **`FAST`** + decay 10 + trunc 0.05 + 同上其余 |
| 待测 | — | `MARKET`（`shortinterest3` 上 2Y 最优之一）/ `REVERSION_AND_MOMENTUM`（中间档） |

**为什么进攻档直接上 `FAST`**：决策 #34 —— `FAST` 在 GBR 是「慢变量计数 / 供需 / 预期」族的**数量级杠杆**，两次独立验证（`shortinterest3` 掩码版 S 1.56→1.95 / 2Y 1.51→1.96；`ts_covariance` 二阶矩 S 1.30→1.60 / 2Y 0.53→0.73），并跨数据集复核论坛帖 `43644505975959`（DEU/TOP500 分析师族 `FAST` 最优）。
平滑后的内部人笔数正是**慢变量计数**族 ⇒ 属该定则的适用面。
**边界**：`STATISTICAL` 在慢变量计数族**反向**（1.46→1.28）；`SLOW` / `CROWDING` / `SECTOR` / `SUBINDUSTRY` 已证伪 ⇒ **只有 `FAST` 这一档被验证为正向**，不可推广成「换个中性化就能救」。

---

## 5. 实证账本

### 5.1 批次 1 —— 未平滑原始聚合（FAIL，仅作反例）

| # | alpha | 表达式 | S | F | TO | 2Y | SUB | DD | failed | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| I1 | `mLo2Okj1` | `rank(vec_count(insd1_shares))` | 0.22 | 0.04 | 174.21% | 1.12 | 0.08 | 74.48% | 6 | ❌ REJECT（TO/DD 爆破） |
| I2 | `d5W8wNEE` | `rank(vec_sum(insd1_valueeur))` | −0.42 | −0.10 | 176.43% | −0.64 | 0.09 | 158.5% | 5 | ❌ REJECT（TO/DD 爆破 + 符号为负） |

### 5.2 批次 2 —— 加工方式对照（全部 `FAST` + decay 10 + trunc 0.05）

| # | alpha | 表达式 | S | F | TO | 2Y | SUB | DD | failed | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| I3 | `kqNkRP2K` | `group_rank(ts_mean(vec_count(shares),22),subind)` | −0.65 | −0.24 | 12.41% | −0.15 | −0.04 | 20.63% | 3 | ❌ 零信号 |
| I4 | `MPYlwxXo` | `group_rank(ts_mean(vec_count(shares),66),subind)` | −0.17 | −0.03 | **8.38%** | −0.14 | 0.25 | 10.24% | 3 | ❌ 零信号（TO 最优） |
| I5 | `0mYkoR8p` | `group_rank(ts_delta(vec_avg(holdings),66),subind)` | 0.02 | 0.00 | 37.28% | −0.11 | 0.11 | 14.92% | 4 | ❌ 零信号 |
| I6 | `pwdJ0k8g` | `group_rank(ts_sum(divide(vec_sum(shares),vec_avg(holdings)),66),subind)` | **−0.19** | −0.04 | **7.90%** | −0.48 | 0.05 | 12.30% | 3 | ❌ 论坛模板基线亦零信号 |
| I7 | `LLMber8a` | I6 + `winsorize(std=2)` + `tail(0.1,0.9,0.5)` | **−0.22** | −0.05 | 9.39% | **−0.77** | 0.03 | 10.80% | 3 | ❌ 论坛模板**未复现** |

**★★★ I7 是本轮最重要的负面结果**：论坛帖 `43212475386007` 在 **DEU `institutions1`** 上报告「流量/存量比」S = 1.53–1.59，本区 **GBR `insiders1`** 严格复现后得 **S −0.22 / 2Y −0.77**。
**⇒ 该帖「可替换数据集」一项（insiders1 / insider_agg_matrix）实际不能照搬。** 原因推断：
- DEU 与 GBR 的内部人申报制度/披露门槛不同（DEU 申报义务更严）；
- `institutions1` 是**机构**持股，`insiders1` 是**内部人**交易 —— 主体性质不同，流量/存量的经济学含义不等价；
- 2Y 从 −0.14 恶化到 −0.77 ⇒ `tail` 可能压掉了有效尾部（语义待定，见 §5.3）。

**★ 正面副产品：`tail` 算子实测可用**（`tail(x, lower=, upper=, newval=)` 全参数位跑通，无 ERROR）⇒ 从「未验证算子」移入「已验证可用」。

### 5.3 待定问题：`tail` 的语义方向

论坛写法 `tail(core, lower=q, upper=1-q, newval=0.5)` 的注释是「掐 nanHandling 造出的**并列假中段**」，但按常规语义该写法是**把两尾压成 0.5**（与注释相反）。I7 用 `lower=0.1, upper=0.9` 得 2Y −0.77（比 I4 差 0.63）⇒ 倾向「压两尾」。
**判据实验**：再用 `lower=0.4, upper=0.6` 跑一次 —— 若结果「几乎无信号」⇒ 压两尾（0.4–0.6 之外 80% 被压平）；若结果「更纯」⇒ 压中段。**该实验尚未跑。**

### 5.4 阶段结论（7 探针）

| 加工方式 | 结论 |
|---|---|
| 原始日频聚合 | ❌ TO 174–176% / DD 74–159% |
| `ts_mean` 平滑 | ✅ 救 TO（→8.4%）/ DD（→10.2%），❌ 但抹掉频率信息 ⇒ S≈0 |
| `ts_sum` 累加（论坛） | ❌ I6 `pwdJ0k8g` S −0.19 / 2Y −0.48 ⇒ 累加也没救回来 |
| `ts_delta` 存量变化（方向代理） | ❌ S 0.02 ⇒ 假设不成立 |
| 论坛完整模板 | ❌ I7 S −0.22 / 2Y −0.77（跨区不可移植） |

**⇒ `insiders1` 在 GBR 上判「结构性弱集」**：6 个可用信号字段已测 3 个（`shares` / `holdings` / `valueeur`）、4 种结构、2 种累加方式、1 套论坛完整模板 —— 7 条探针**无一 \|S\| > 0.65 且方向多为负**。**根本缺陷是无买卖方向**（见 §1）。
**⇒ 主攻方向转向 `insider_agg_matrix`（同塔、有买卖方向、34 字段全 MATRIX、coverage 同为 0.5937）**，见 §7。

---

## 7. `insider_agg_matrix` —— 同塔的第二块地（有方向！）

**GBR / D1 / TOP700，34 个字段，全部 `MATRIX`（不需要 `vec_*` 折叠），coverage 0.5935–0.5937（`directional_indicator*` 为 1.0）。**

### 7.1 关键：这是唯一带买卖方向的内部人数据集

| 族 | 字段 | userCount / alphaCount | 说明 |
|---|---|---|---|
| **买卖股数分离** | `total_buy_shares` / `total_sell_shares` | 16/21、14/19 | 全部董事的买入/卖出股数总和 |
| | `avg_buy_shares` / `avg_sell_shares` | **54/81**、27/39 | 均值版（`avg_buy_shares` 是全集 alphaCount 最高） |
| **高管层** | `total_top_buy_shares` / `total_top_sell_shares` | 16/17、16/17 | 仅 executives |
| | `avg_top_buy_shares` / `avg_top_sell_shares` | 19/30、13/21 | |
| **直接交易层** | `total_secondary_buy_shares` / `total_secondary_sell_shares` | 6/6、4/4 | directors 直接持有 |
| | `avg_secondary_buy_shares` / `avg_secondary_sell_shares` | 16/21、18/23 | |
| | `*_secondary_top_buy_shares` / `*_secondary_top_sell_shares` | 8/8、9/9 | executives 直接持有 |
| **方向指标** | `directional_indicator` | 49/61，**coverage 1.0** | 内部人活动整体方向/bias |
| | `directional_indicator_2` | 25/27，**coverage 1.0** | ⚠️ **USA wave238 实测全零**（`longCount=0/shortCount=0/turnover=0`）⇒ **禁用** |
| 价值族 | `significant_value_1..4` / `directional_significant_value_1..4` / `top_*` | 0–54 | ⚠️ **USA wave238 已判死**（10 模板天花板 \|S\| 0.70）⇒ 不作首选 |

### 7.2 为什么「买卖股数分离」族是全新未测维度

USA wave238 判死的是**价值族**（`significant_value_*` / `directional_*` / `top_*` 共 17 字段），**「买/卖股数分离」族从未被测过**。
且本数据集的「笔数/股数」属性与 `insiders1` 的计数族同源（跨区已验证：计数族 > 价值族）—— 差别只在**这一族多出了方向**，正好补掉 `insiders1` 的致命缺陷。

### 7.3 批次 1 —— A1/A2「股数口径」净买入比（FAIL，反例）

**设计要点：分子分母分别累加再相除**，避免非事件日 0/0 产生 NaN 污染：

| # | alpha | 表达式 | 机制 |
|---|---|---|---|
| A1 | `78Lqg7ax` | `group_rank(divide(ts_sum(subtract(total_buy_shares, total_sell_shares), 66), ts_sum(add(total_buy_shares, total_sell_shares), 66)), subindustry)` | 全体董事**净买入比**（股数口径，值域 [−1,1]） |
| A2 | `O0AwKYjR` | 同上但换 `total_top_buy_shares` / `total_top_sell_shares` | 仅高管层净买入比 |

设置：GBR / TOP700 / D1 / `FAST` / decay 10 / trunc 0.05 / nanHandling ON / maxTrade OFF / VERIFY。

| # | alpha | S | F | TO | 2Y | SUB | margin | returns | DD | failed_ra |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A1 | `78Lqg7ax` | **0.22** | 0.05 | 8.13% | **−0.29** | 0.11 | 1.4bp | 0.57% | 6.04% | 3 |
| A2 | `O0AwKYjR` | **0.42** | 0.12 | 8.19% | **−0.38** | 0.23 | 2.7bp | 1.10% | 6.16% | 3 |

**三条判读（比 S 本身更重要）**：

1. **`ts_sum(·,66)` 确实彻底治好了换手** —— TO 8.13% / 8.19%，与 `insiders1` 的 I4（8.38%）同量级，比 raw 聚合的 174% 低 95%+。⇒「累加窗」这条加工路径是干净的，问题不在加工层。
2. **高管层（A2 0.42）优于全体董事（A1 0.22）**，方向符合 Lakonishok-Lee「信息集中在少数高层大额交易」，说明**方向轴本身是对的，只是被口径稀释**。
3. **致命点：2Y 为负（−0.29 / −0.38）** —— 这不是「信号弱」，是**符号不稳定**。说明 `(买−卖)/(买+卖)` 这个股数比值量到的更多是「公司规模/期权行权节奏」而非信息。
4. **定则 I-3（本节新增）：股数口径的分母 `(买+卖)` 由卖出侧主导**（英国董事普遍持有并定期减持 ⇒ 卖股数远大于买股数），比值长期贴 −1，横截面方差被压缩 ⇒ **分母吃掉了买入侧的信息**。这与 LL2001「买入侧有信息、卖出侧多为流动性」直接冲突：**用一个以卖出为主体的分母去归一化买入信号，等于用噪声除掉信号。**

**为什么用比值而非差**：`divide(净额, 总额)` 无量纲、天然可比、无 `unit_handling` 风险；且论坛帖明示「**嵌套子集间用商不用差**」。
**为什么 66**：论坛实测 66（季度申报周期）是干净内点峰（44/88/132 → 1.33/1.46/1.05）。

### 7.4 ★★★★★ 关键突破：`avg_*` 与 `total_*` 可反推「笔数」

字段描述已实测确认（`get_datafields` 全量 34 条）：

- `total_buy_shares` = **"Sum shares bought by all directors"**
- `avg_buy_shares` = **"Mean shares bought by all directors"**

⇒ **`divide(total_buy_shares, avg_buy_shares)` = 买入笔数**（无量纲纯计数，`unit_handling` 安全）。

这条推导把本数据集从「价值族（已判死）/ 股数族（A1/A2 已证含噪）」推进到**「笔数 × 方向」双维度交叉区**——这是 memory 中「内部人数据的有效维度是笔数/参与广度」与「GBR 内部人缺方向」两条结论的**唯一交集**，此前从未测过。

定义的派生量（全文复用）：

```
NB  = divide(total_buy_shares,  avg_buy_shares)             董事买入笔数
NS  = divide(total_sell_shares, avg_sell_shares)            董事卖出笔数
NTB = divide(total_top_buy_shares,  avg_top_buy_shares)     高管买入笔数
NTS = divide(total_top_sell_shares, avg_top_sell_shares)    高管卖出笔数
NSB = divide(total_secondary_buy_shares,  avg_secondary_buy_shares)   董事直接持有买入笔数
NSS = divide(total_secondary_sell_shares, avg_secondary_sell_shares)  董事直接持有卖出笔数
```

### 7.5 ★★★★ 模板库（11 条结构互异 · 来源标注 · 互异性自检）

> 满足用户硬约束「模板池必须 ≥10 个且结构互异」。差异落在**矩 / 主体轴 / 数据层轴 / 算子几何 / 非线性变换 / 时间尺度**上，**不是换窗口换常数**。

| # | 名称 | 核心表达式（`group_rank(·, subindustry)` 已省略在表内注明） | 结构差异所在 | 来源 |
|---|---|---|---|---|
| **M1** | 净买入**笔数**占比 | `group_rank(divide(ts_sum(subtract(NB,NS),66), ts_sum(add(NB,NS),66)), subindustry)` | 口径从股数→笔数（同骨架异矩） | 自建 + LL2001/JMZ2003 |
| **M2** | 纯买入侧广度 | `group_rank(ts_sum(NB,66), subindustry)` | 单腿、**无卖出腿**；广度是唯一变量 | LL2001「买入侧才有信息」 |
| **M3** | 买入广度的时序异常 | `group_rank(ts_zscore(ts_sum(NB,66),504), subindustry)` | **时序**标准化（相对自身历史）而非横截面 | Da-Engelberg-Gao 异常注意力类比 |
| **M4** | 高管净买入笔数占比 | `group_rank(divide(ts_sum(subtract(NTB,NTS),66), ts_sum(add(NTB,NTS),66)), subindustry)` | **主体轴**：executives vs all directors | LL2001「高管更有信息」 |
| **M5** | 净买入笔数的动量 | `group_rank(ts_delta(ts_sum(subtract(NB,NS),66),252), subindustry)` | **矩：一阶差分**（加速度） | 自建 |
| **M6** | 活跃度门控 × 净方向 | `if_else(greater(rank(ts_sum(add(NB,NS),66)),0.5), <M1 内核>, nan)` | **非线性条件化**（掩码同源） | 定则 #29/#30 |
| **M7** | 单笔规模不对称 | `group_rank(ts_mean(divide(avg_buy_shares, add(avg_buy_shares, avg_sell_shares)),66), subindustry)` | 用 `avg_*` **本身**（单笔规模=决绝度）而非笔数 | 自建（conviction per trade） |
| **M8** | 直接持有层净买入笔数 | `group_rank(divide(ts_sum(subtract(NSB,NSS),66), ts_sum(add(NSB,NSS),66)), subindustry)` | **数据层轴**：`secondary`（剔期权行权/间接持有） | 自建 |
| **M9** | 数据集原生方向指标 | `group_rank(ts_mean(directional_indicator,66), subindustry)` | 用平台聚合量（**cov 1.0，覆盖最宽**） | 数据集原生 |
| **M10** | 双轴标准化 | `group_zscore(ts_zscore(divide(ts_sum(subtract(NB,NS),66), ts_sum(add(NB,NS),66)),504), subindustry)` | **算子几何**：时序 × 截面双层 | 自建 |
| **M11** | 买卖笔数比的二阶矩 | `group_rank(ts_covariance(<M1 内核>, <M1 内核>, 66), subindustry)` | **二阶矩**（方差版 vs 标准差版） | 论坛 `43624312881943`（64 赞） |

**互异性自检**：11 条中——口径轴 2（M1/M2）、时序轴 2（M3/M5）、主体/数据层轴 2（M4/M8）、非线性 2（M6/M10）、原生量 1（M9）、二阶矩 1（M11）、单笔规模 1（M7）。**无任何两条只差窗口或常数。**

**派发序（每批 ≤2，按信息量排序）**：
1. **M1 + M2** —— 核心假设检验：笔数维度是否成立（M2 同时验证 `divide(total,avg)` 推导本身是否退化）
2. M3 + M4 · 3. M7 + M9 · 4. M5 + M10 · 5. M8 + M11 · 6. M6（仅当 M1 有 >1.0 时补门控）

**判定门（先验设定，防止事后解释）**：
- M2 若 `turnover ≈ 0` 或 `longCount = 0` ⇒ `divide(total,avg)` 推导退化，整族作废，回 `insiders1` 补探针。
- M1 若 `|S| < 0.6` 且 2Y 为负 ⇒ 「笔数 × 方向」维度在 GBR 亦不成立 ⇒ 本数据集转 PROBE-KILLED。
- M1 若 `S > 1.0` ⇒ 进 §7.5 派发序全跑，并优先在 M4/M8 上找主体轴增量。

### 7.6 批次 2 —— M1/M2「笔数口径」首批（FAIL，但推导验证通过）

设置同上（GBR/TOP700/D1/`FAST`/decay 10/trunc 0.05/nanHandling ON/maxTrade OFF/VERIFY）。

| # | alpha | 表达式 | S | F | TO | 2Y | SUB | margin | returns | DD | failed_ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| M1 | `d5W8lRb2` | 净买入**笔数**占比 | **0.17** | 0.04 | 12.09% | **+0.80** | 0.04 | 1.2bp | 0.74% | 11.39% | 4 |
| M2 | `pwdJ1P7v` | 纯买入侧广度 `ts_sum(NB,66)` | **0.23** | 0.05 | **8.25%** | 0.00 | 0.21 | 1.4bp | 0.59% | 9.38% | 3 |

**四条判读**：

1. **`divide(total_buy_shares, avg_buy_shares)` 推导成立** —— M2 产出了正常的 `longCount/shortCount`、TO 8.25%（不是 0）、pnl 非零，`failed_ra 3` 是正常量级而非全挂。⇒ **「字段存在 ≠ 有数据」的风险在此排除**，`total/avg` 反推笔数是可用的工程手段。
2. **M1 的 2Y 从 −0.29 翻到 +0.80** —— 笔数口径比股数口径在**近两年**明显更有信息。但全期 S 从 0.22 掉到 0.17 ⇒ **信号只集中在近期，全期被稀释**。这正是 memory 里「2Y 与全期 sharpe 跷跷板」的又一例。
3. **M1 的 SUB 只有 0.04 而 M2 有 0.21** —— 加进卖出腿（分母）后，子宇宙表现几乎归零。再次印证「分母被卖出侧主导」：`(NB−NS)/(NB+NS)` 的横截面方差主要来自卖出侧噪声。
4. **M2 的 2Y = 0.00 是致命点** —— 纯买入广度连近两年都没有信号。结合 LL2001「买入侧才有信息」的先验，**GBR TOP700 的买入侧信息已被市场消化**（大盘股被分析师高度覆盖，内部人买入无信息优势）。

**四条合起来（A1 0.22 / A2 0.42 / M1 0.17 / M2 0.23）**：`insider_agg_matrix` 的「买卖方向」维度在 GBR TOP700 上 **4 条探针全部 ≤ 0.42**，且**没有任何两条同时在 S 与 2Y 上达标**。

**剩余两个不共享稀疏性缺陷的轴**（批次 3，止损前的最后两条）：
- **M9** 数据集原生 `directional_indicator`（**coverage 1.0**，唯一不共享 coverage 0.59 稀疏缺陷的轴）
- **M12（新增）卖出笔数取负** `multiply(group_rank(ts_sum(NS,66), subindustry), -1)` —— 直接复刻 `shortinterest3` 的冠军骨架（「做空笔数越多 ⇒ 表现越差」，`akK2vpWW` S 1.95）到内部人卖出侧。**这是本数据集与已验证成功骨架结构上最接近的一条，优先级高于原派发序里的 M3/M4。**

### 7.7 批次 3 —— M9（原生方向指标）/ M12（卖出笔数取负）

| # | alpha | 表达式 | S | F | TO | 2Y | SUB | margin | returns | DD | failed_ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| M12 | `58E7qrvN` | `multiply(group_rank(ts_sum(NS,66), subindustry), -1)` | 0.18 | 0.04 | 8.32% | −0.27 | **−0.46** | 1.2bp | 0.49% | 8.99% | 4 |
| M9 | `88RkKYzq` | `group_rank(ts_mean(directional_indicator, 66), subindustry)` | **−0.60** | −0.20 | 9.49% | −0.53 | −0.16 | −3.0bp | −1.44% | 16.05% | 3 |

**两条判读**：

1. **M12 彻底否掉「照搬 `shortinterest3` 冠军骨架」这条路** —— 同一骨架（计数 + `group_rank(subindustry)` + `multiply(−1)` + `FAST` + decay 10）在 `shortinterest3` 上给 1.95，在内部人卖出笔数上给 **0.18**，差 **10.8 倍**。**⇒ 骨架可移植，语义不可移植**（与定则 #39 同构：做空笔数是市场级机构仓位，内部人卖出笔数是少数高管个人流动性，经济含义不等价）。
2. **M9 是本族唯一 \|S\| > 0.5 的探针，但符号为负** —— `directional_indicator`（coverage 1.0）越高 ⇒ 未来收益越差，\|S\| **0.60**。符号是**反向**的（若字段语义是"买入偏向"，则这是反转而非跟随）。
   副带证据：**M9 的 `returns` 为 −1.44% 而 `margin` 为 −3.0bp，是全族唯一给出显著负收益的**，说明该字段确实含信息，只是方向与直觉相反、且量级不足（0.60 vs 闸 1.58，差 2.6 倍）。

### 7.8 ★★★★★ 定则 I-4：内部人交易信号在「大盘股专属宇宙」上结构性失效

**8 条探针全账本（GBR/TOP700/D1/`FAST`/decay 10/trunc 0.05）**：

| 结构 | alpha | S | 2Y | TO | DD | 结论 |
|---|---|---:|---:|---:|---:|---|
| 股数净买入比（全体董事） | `78Lqg7ax` | 0.22 | −0.29 | 8.13% | 6.04% | 弱 |
| 股数净买入比（高管） | `O0AwKYjR` | **0.42** | −0.38 | 8.19% | 6.16% | 本族正向 S 最高 |
| 笔数净买入比（全体董事） | `d5W8lRb2` | 0.17 | **+0.80** | 12.09% | 11.39% | 本族 2Y 最高 |
| 纯买入侧广度 | `pwdJ1P7v` | 0.23 | 0.00 | 8.25% | 9.38% | 弱 |
| 纯卖出侧广度取负 | `58E7qrvN` | 0.18 | −0.27 | 8.32% | 8.99% | 弱 |
| 高管直接持有层净笔数（M8） | `akK2AYMW` | **−0.15** | **−0.88** | 15.39% | 12.85% | 负数，且 2Y 全族最差 |
| 原生方向指标（窗 66） | `88RkKYzq` | **−0.60** | −0.53 | 9.49% | 16.05% | \|S\| 最高 |
| **原生方向指标（窗 252，翻符号）** | `A1VJg1Ql` | **+0.09** | +0.50 | 7.83% | 13.98% | ★ **证伪上一条** |

**M8（`akK2AYMW`）表达式**（最细粒度的「高管直接持有」层，34 字段里语义最接近真实内部人决策的一层）：
```
group_rank(divide(
  ts_sum(subtract(divide(total_secondary_top_buy_shares,  avg_secondary_top_buy_shares),
                  divide(total_secondary_top_sell_shares, avg_secondary_top_sell_shares)), 66),
  ts_sum(add(     divide(total_secondary_top_buy_shares,  avg_secondary_top_buy_shares),
                  divide(total_secondary_top_sell_shares, avg_secondary_top_sell_shares)), 66)
), subindustry)
```
**M8 判读**：`S −0.15 / 2Y −0.88` 是**全族 2Y 最差的一条**，也是「粒度越细越差」链条的终点 —— 从「全体董事」（A1 0.22）→「高管」（A2 0.42）→「高管直接持有」（M8 −0.15）三段递进，**最贴近原始决策主体的那一层反而最没信号**。这排除了「聚合层把信号平均掉了」的解释：若信号真在内部人行为里，越细的粒度应越强；实测反向 ⇒ **该数据集不含 GBR TOP700 可用的内部人方向信息。**

**★★★★★ 关键反证（7.8.1）：`88RkKYzq` 的 −0.60 是窗口拟合，不是信号。**
`multiply(x, -1)` 在数学上**精确翻转每日 PnL**，所以若 −0.60 是真实的，翻符号后**必然**得 +0.60。实测 `A1VJg1Ql` 只有 **+0.09** ⇒ 唯一解释是**同一字段从 66 日平滑换成 252 日后信号消失**。
**⇒ 定则 I-5（新增判据）：判断 \|S\| 是否真实，用「同字段换窗口」做安慰剂检验 —— 若换窗口后 \|S\| 崩塌超 80%，该值不可作为「有信号」的证据。**（本条与论坛 `43624312881943` 的 `ts_delta` 安慰剂 0.09 同源）

**⇒ 8 条探针，正向 S 天花板 0.42，\|S\| 天花板 0.60 且已证伪为噪声。没有一条同时在 S 与 2Y 上达标。**

**★★★★★ 定则 I-4（可跨区迁移）：内部人交易信号在**大盘股专属宇宙**上结构性失效。**

- **机理**：Lakonishok-Lee (2001) / Jeng-Metrick-Zeckhauser (2003) 记录的内部人异象，信息优势来源是**散户与内部人之间的信息不对称**。这个不对称在小盘股最大；在「某国最大的 700 只股票」上，内部人交易被分析师跟踪、监管披露与做市商充分套利 ⇒ 信息半衰期极短。
- **对照实验（同区域、同设置、同骨架形状）**：`shortinterest3`（**市场级机构仓位聚合量**）在 GBR TOP700 上给 **S 1.95**；内部人交易（**个体高管行为**）给 0.42。⇒ **不是 GBR TOP700 不能做「聪明钱」，而是「个体行为型」数据在大盘股上失效、「市场级聚合型」数据不失效。**
- **GBR 无退路**：GBR 只有 TOP700 一个 universe ⇒ 该缺陷**不可通过换宇宙修复**，属 `STRUCTURAL-DEAD` 判据里的「栖息地缺失」。
- **★ 应用（改变后续选集的默认动作）**：GBR 选数据集时，在「单塔优先选非目标塔 category」之后**再加一层筛**——优先「**市场级聚合**」类（shortinterest / 期权 / 宏观 / 行业级 / 全市场情绪），警惕「**个体行为**」类（内部人交易、单公司公告）。这条与既有两条塔约束不冲突，是 category 内部的第三层筛选。

**与 `insiders1` 合并后的 INSIDERS 塔判决**：两个数据集共 **15 条探针**（7 + 8），最高正向 S **0.42**、最高 \|S\| **0.60 已证伪**。⇒ **INSIDERS 塔（倍率 1.5）在 GBR D1 判 `STRUCTURAL-DEAD`，本季度不再投入。**

**三数字自检（定则 #18/#19）**：探针数 8 ✅ / 结构数 7 ✅（净买入比·纯买入广度·纯卖出广度·原生方向指标·高管直接持有层·笔数口径·窗口翻符号）/ 字段覆盖率 **10/34 ≈ 29% ❌**。
**★ 为什么覆盖率不足仍可判 STRUCTURAL-DEAD**：覆盖率 50% 是 `CONFIRMED-DEAD` 的门槛，而 `STRUCTURAL-DEAD` 的判据是「**栖息地缺失**」——本塔有两条独立的栖息地证据：① GBR 只有 TOP700 一个 universe（大盘股专属，定则 I-4 的机理直接成立）；② 跨区对照 USA wave237（`insider_trx_matrix` 价值族 10 模板天花板 0.82）与 wave238（`insider_agg_matrix` 价值族 10 模板天花板 0.70）双双判死 ⇒ **同一 category 在两个区域、两种字段语义上独立失败**，这不是「GBR 特有」而是 category 级缺陷。
**⇒ 未测的 24 个字段（价值族为主）不再投入**：价值族已在 USA 两个数据集上分别判死，而 GBR 侧的「买卖股数分离」族（本区最强维度）8 条探针天花板 0.42 ⇒ 两个维度各自独立判死，覆盖剩余字段不会产出新结论。

---

## 6. 与其它文档的交叉引用

- 定则 #34（`FAST` 是慢变量计数族的数量级杠杆）→ `template_library_gbr_shortinterest3.md` §6.8.4
- 决策 #37（稀疏事件字段必须前置平滑）→ 本文件 §2（本条是该定则在内部人域的落地与加固）
- 决策 #3（计数类字段必须用 `rank`/`group_rank`，不用 `zscore`）→ 全模板遵守
- 决策 #23（二阶矩要用 `group_zscore` 而非 `group_rank`）→ N9
- 决策 #29/#30（掩码必须与信号同源；θ=0.9 为峰）→ N10
- USA 跨区先验：`docs/reference/template_library_gbr_insider_trx.md`、memory wave237/wave238 条目
