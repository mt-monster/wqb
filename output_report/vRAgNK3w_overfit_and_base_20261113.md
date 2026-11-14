# `vRAgNK3YEJ` 结构合规性、过拟合判定与提交对收益/Base 的影响评估

> 时间：2026-11-13｜对象：`vRAgNK3w`（上轮 op-min 交付件）
> 表达式：`group_rank(add(ts_mean(F,504), multiply(ts_delta(F,22), 0.18)), country)`，`F = rsk70_mfm2_euetrd_anlystsn`
> 结论基于：平台官方文档 2 篇、平台论坛 8 篇（含评论）、本地闸 5 源码实测、平台 `mix_audit` / payment / pyramid API 实读。

---

## 0 三问速答

| 问题 | 结论 |
|---|---|
| **是 `add(a,b)` 毒模式吗？** | **机械上不是**。本地闸 5 三条正则全不命中、`is_add_mix=False`、平台 `mix_audit=two_leg / coef_legs=1 / blocked=False`。它是「单系数腿」，不是毒模式定义的「双系数权重网格」。但处在灰区：仍需答三问，且 **`prior` 一问我无法如实回答**（见 §2.3）。 |
| **算过拟合吗？** | **结构上不算，参数选择过程高度疑似「隐性过拟合」**。论坛「纪律红线」三条判定线**全部命中**；官方 Dos and Don'ts 两条被违反。有反面证据（单字段 ATOM、5 算子、经济含义清楚、十年零负年），但 **F 1.01 / sub 1.01 双贴线**正是论坛点名的「刚好过线但 OS 即塌」形态。 |
| **提交影响收益和 base 吗？** | **会，但方向和幅度不能线性外推**。最确定的是 **Quantity +1**（ET 11-13 REGULAR 0/4 剩 4）；最不确定也最危险的是 **Value Factor 与 Combined OS Performance**（提交不可逆）。点亮的是 **EUR/D1/RISK ×1.0 全区垫底倍率塔**，Quality 增益有限；且已有论坛实测「追加 2 条较差 alpha 后 base 从 50 掉到 9」的反例。 |

**一句话建议**：能交，但**不建议把它当高质量新增信号主力交**。今天是配额空窗期，若手上有 `wpo8olA6` / `omEdka3v` / `ZYQ116ln`（点亮 other ×1.5 / GBR other ×1.6 / KOR pv 等高倍率塔）应优先；它适合当第 4 席补位。

---

## 1 「add(a,b) 毒模式」到底是什么

**这是本项目术语，不是平台/论坛通用叫法。** 来源链：

```
官方 platform_constraints.json :: poison_patterns
   → toolkit config 闸 5（毒模式）
   → src/wqb/store/submit_queue.py :: _MIX_REGEXES
   → docs/design/structural_reconstruction.md / campaign_kickoff_prompt.md D2
```

### 1.1 精确定义

`submit_queue.py` 三条正则（逐字取自官方 `poison_patterns`）：

| # | 抓的形态 | 例 |
|---|---|---|
| 1 | 中缀双系数加权 | `0.4*rank(A) + 0.6*rank(B)` |
| 2 | `add(multiply(常数, X), ...)` 函数式加权 | `add(multiply(0.4, A), multiply(0.6, B))` |
| 3 | 两条系数腿 | `add(multiply(A, 0.4), multiply(B, 0.6))` |

结构判定补充：`best_coef >= 2` → `weight_grid`（**硬拦，force 不豁免**）；`add` 展平 ≥4 腿 → `stack`（**硬拦**）；2–3 腿 → `two_leg/three_leg`（**放行但必答三问**）。

本项目的纪律文本：
- `docs/design/structural_reconstruction.md:16`「❌ 禁止 `add(A,B)` 混信号调参」、`:17`「❌ 禁止权重网格扫描（0.4/0.6 → 0.3/0.7）」
- `docs/reference/campaign_kickoff_prompt.md` D2「组合权重仅**单次设置**（0.5/0.5 或 0.6/0.4 或 0.7/0.3），禁止权重网格扫描。同信号不达标换字段组合/换概念，不调权重」
- `docs/design/operator_modeb_research.md:263`「`prod_corr ≥ 0.7` … 禁用操作：`add(A,B)` 调权重」

### 1.2 对 `vRAgNK3w` 的实测判定

本地源码直跑 + 平台 `workflow_submit_alpha` 只读预检：

```
_MIX_REGEXES 命中 = [False, False, False]
is_add_mix = False
mix_review = {'kind':'two_leg', 'legs':2, 'coef_legs':1, 'blocked':False,
              'narrative_required':True, 'narrative_missing':['holders','polarity','prior']}
平台 mix_audit = two_leg / 2 腿 / coef_legs=1 / blocked=False / ATOM:LAST_2Y
```

⇒ **不是毒模式，平台不会机械拒绝**。原因：只有**一条**系数腿（`multiply(ts_delta, 0.18)`），另一条是裸 `ts_mean`；权重是「主信号 + 小权重修正腿」，不是「两个信号按权重网格配比」。

### 1.3 但有一处实质性灰区（必须知道）

平台/本项目三问中的 `prior` 原文：

> **「组合方向与权重是否在回测前由逻辑/文献钉死（不是从回测网格里试出来的）」**

而本轮事实是：同族扫了 **112 个唯一 (表达式, decay, truncation, neutralization) 组合**，权重覆盖 0.10 / 0.12 / 0.15 / 0.18 / 0.20 / 0.30 / 0.40 / 0.50，`vRAgNK3w` 的 **w=0.18 正是从这张网格里挑出来让 F 与 sub 刚好过线的那一个**。

⇒ **`prior` 无法如实回答「是」**。硬答会留下审计痕迹；如实答「否」则三问不完整、`confirm_submit=True` 会被 `mix_audit` 拦下（`force` 可豁免，但那正是绕纪律）。这是比「是否毒模式」更实际的问题。

---

## 2 过拟合判定

### 2.1 官方原文（`Consultant Dos and Don'ts`，learn 文档 `consultant-dos-and-donts`，更新 2026-09-18）

**Dos（推荐实践）**
- 「**DO improve Alphas by refining ideas, not by adding or fitting parameters, factors or reversion elements.**」
- 「DO restrict parameter search to **simple & reasonable** ones. For example **5, 20, 60, 120, 252** in case of days, instead of 37, 14 etc.」
- 「DO run simulations with **different sub-universe (TOP500/1000/2000/3000)** while tuning the Alpha parameters. **This reduces the risk of universe fitting.**」
- 「DO check your Alpha's performance stability across sub-universe, super-universe and **across other regions** for higher OS performance.」
- 「DO make sure your Alpha has economic foundation … explain within a minute.」
- 「DO simplify the implementation … remove unnecessary elements.」
- 「DO use **different datasets & operators** to build Alphas to ensure diversification.」

**Don'ts**
- 「**DO NOT spend too much time on a single simple idea.**」
- 「**DO NOT over fit your Alpha to enhance performance or to reduce correlation by: Trying many different parameters or using too many data fields; Using too many if else; Shortening IS period; Filtering or presetting signals.**」
- 「DO NOT add an existing Alpha from one data source to enhance the signal from another data source without any strong economic sense.」
- 「DO NOT incorporate noise in the Alpha to reduce production correlation.」

**逐条比对本轮**：`DO NOT ... Trying many different parameters` ✅ 命中（112 组合）；`DO NOT spend too much time on a single simple idea` ✅ 命中（同一字段同一骨架）；`restrict parameter search to simple & reasonable ones` ⚠️ 命中（w=0.18 不属于标准档；504/22 是标准窗口，权重不是）；`different sub-universe / other regions` ❌ 未做（只跑 EUR/TOP2500）；`different datasets & operators` ⚠️ 单字段 ATOM，与分散化建议相反（但官方另有 Single Dataset Alphas 鼓励 ATOM，见下）。

### 2.2 论坛判定线（逐条命中，这部分最关键）

| 出处 | 判定线 | 本颗 |
|---|---|---|
| **`43583615387543`【纪律红线】"你很明显在拟合这个因子"（23 赞）** | ① 同一信号本体超过 **2 个批次**还在打磨（换 decay / 窗口 / 中性化 / 外层 quantile 都算同一本体） | ✅ **命中**（112 组合、远超 2 批） |
| 同上 | ② 候选之间**参数互变**，指标跟着参数来回晃、始终够不到线 —— 噪声带（实测 ±0.18 sharpe） | ✅ **命中**（F 0.85→0.95→0.99→1.01；w 0.10→0.15→0.18→0.20→0.30→0.40→0.50 来回；2Y/sub 反复贴线） |
| 同上 | ③ 新候选与已有候选 **PC ≈ 1** —— "你没有找到新信号，只是把同一个信号又调了一遍" | ✅ **命中**（7 颗全闸件 ρ = 0.7214–1.0000，`KPgaOx8p`~`E5QJv1QR` ρ=1.0000，最大独立集 = 1） |
| 同上 | 软规则：「**门槛差 0.05 以内的反复冲刺，产出的往往是刚好过线但样本外即塌的过拟合品**」 | ✅ **强命中**（F 1.01 vs 闸 1.00；sub 1.01 vs 闸 1.00；**双贴线各 0.01**） |
| **`41482855055383` 隐性过拟合（16 赞）** | 来源一：「每次只是微调一下权重（0.5-0.5 → 0.52-0.48）… 20 次微调累积后你从中选择了夏普最高的那次，**这个选择过程本身引入了向上的偏差**」 | ✅ 命中（w 网格挑最优） |
| 同上 | 检测方法三：「缩减参数空间（**多个权重固定为等权**）重跑，若 Sharpe 大幅下降，说明参数自由度在 IS 上做了拟合工作」 | ⚠️ 部分反证：删 `multiply`（w→1.0）后 **S 反而从 1.93 升到 2.49**，但 sub 掉闸 ⇒ 权重的作用不是抬 S，而是**把 S 压到 sub/S ≥ 0.521 的比值闸内**。机制可解释，不是纯噪声拟合 |
| 同上 | 建议：「最多 3 次有针对性调整」；「IS 内预留最后 20% 完全不用于优化」 | ❌ 均未遵守 |
| **`43807969440023` 稳健性诊断清单（5 赞）** | 「窗口稳健性：切 2 年 / 3 年 / 5 年各看一次，只在某一特定区间亮眼的基本是过拟合」；「中性化切换」 | ⚠️ 有 10 年逐年（零负年）+ 2Y 1.66 PASS，但未做切窗对照 |
| **`41877348653335` SUPER 组合多尺度融合（58 赞）** | 「`scale()` 归一后直接**求和**比**手动设定权重比例**更让数据本身决定贡献度，**减少了主观参数调优的过拟合风险**」 | ⚠️ 本颗恰是手动权重 |
| **`42884108933143` 组合优化 vs 简单平均（31 赞）** | 等权「零成本、零参数、零估计误差」；协方差最优权重理论上更好但估计误差大 | ⚠️ 同上 |
| **`43583602320151`【资源配置】op/data 多样性审计（23 赞）** | 「ρ 0.9997–1.0000 的教训——它们本来就是同一个信号」「重复 data 反复做，**对组合维度是零提升**」；纪律「默认新批投新 data，同字段重做需要给出新假设」 | ✅ 命中（本轮 112 组合全在同一字段 `rsk70_mfm2_euetrd_anlystsn`） |
| **`42623768265111` AI: 过线只是门槛（23 赞）** | 「每多一次针对失败项的修补，候选在未来失效的风险就高一分」 | ✅ 命中（本轮正是反复修补 F / sub 两项） |

### 2.3 减轻嫌疑的反面证据（要公允）

1. **单字段、单数据集 ATOM、仅 5 算子**，符合官方「simplify / remove unnecessary elements」。官方另有 `❗ Single Dataset Alphas` 文档明确鼓励 ATOM。
2. **论坛 `43807857519255`「单字段多形状」正面评价**：同一字段构造 level 形态 + 短窗口变化（如 60 日差分）+ ts_zscore 等不同形状，「经济含义各有出处（动量、反转、量价确认本来就是不同逻辑）」，天然比同一形状调参更不相干 —— **本颗正是「504 日水平 + 22 日变化」的组合**。
   - 但该帖评论（XZ17517）同时警告：「最容易『看着不同、实则同构』的一对是 **level 形态和短窗 zscore**，因为慢变字段的 zscore 主要由近期水平驱动… **月级 PnL 相关高于 0.8 就说明形状差异没真正转成持仓差异**」。本颗同族 ρ 0.72–1.0，**部分落在警戒区**。
3. **经济含义可在 1 分钟内讲清**：分析师情绪暴露的长期水平（拥挤/反转）+ 月度修正事件（评级批量落地），小权重让水平主导、事件提供新鲜度。
4. **十年逐年零负年**（最低 2016 = 0.54）、2Y 1.66 PASS、末年 2.48 > 全期均值 2.00、末段单调回升。
5. **ΔS +0.28**（`EQUITY:EUR:1:POWER_POOL`，组合 S 4.32→4.60）、`dilutive=false`；self 0.2062 低；CW PASS；TO 4.15% 低、margin 16.5bp ⇒ 成本侧干净。
6. **权重的作用是结构性的**：sub 限值 = 0.5206×S 是比值闸，2/3/4 算子件 sub/S 只有 0.35–0.48 全掉闸，5 算子完整结构才 0.52–0.54 刚好过线 ⇒ `multiply` 与 `ts_delta` 是 sub 闸承重件，不是无意义装饰。

### 2.4 综合判定

> **结构合规、可提交；但参数选择过程高度疑似「隐性过拟合」，且精确命中论坛「纪律红线」三条线与「刚好过线」软规则。它不是一个高质量新增信号，而是「把同一个信号调到闸门线上」的产物。**

平台**没有** overfitting 检查项，`is.checks` 全 PASS、`submit_gate passed=True` 只代表机械闸门通过，**不代表 OS 会守住 IS 表现**。官方 Don'ts 是研究纪律，不是提交闸 —— 违反不会导致拒收，代价体现在 OS 与 Value Factor。

---

## 3 官方与论坛出处清单（可复核）

**官方文档**
| page_id | 标题 | 关键内容 |
|---|---|---|
| `consultant-dos-and-donts` | Consultant Dos and Don'ts | 上述 Dos / Don'ts 原文（2026-09-18 更新） |
| `brain-genius` | 💡 Brain Genius | Pyramid = region×delay×dataset category，≥3 颗算 formulated；Combined Alpha Performance = 全部已提交 alpha 的 **OS** 表现；tie-breaker 六维：Avg distinct Operators/Alpha（低好）、Avg distinct Fields/Alpha（低好）、Total distinct Operators（高好）、Total distinct Fields（高好）、Max Simulation Streak、Community leader |
| `consultant-faqs` / `osmosis-allocation-guide-consultants` | — | Base / Quarterly Payment 口径（论坛 43561782887575 引用） |
| `single-dataset-alphas` | ❗ Single Dataset Alphas | ATOM 免 IS-Ladder、只看 2Y（本轮 `mix_audit` 也回显 `ATOM:LAST_2Y`） |

**论坛**
| article_id | 标题 | 赞 |
|---|---|---|
| `43561782887575` | 如何提高 Base Payment：交满配额、每天行动与常见误区 | 65 |
| `41482855055383` | 🧠 隐性过拟合：当你的 Alpha 在 IS 上完美却在 OS 上平庸 | 16 |
| `43583615387543` | 【纪律红线】"你很明显在拟合这个因子"：死磕单一因子的三条判定线 | 23 |
| `43807969440023` | 稳健性诊断清单：如何区分真信号与过拟合 | 5 |
| `41877348653335` | SUPER Alpha 多时间尺度融合：scale 求和 vs 手动权重 | 58 |
| `42884108933143` | 组合优化 vs 简单平均：什么时候该认怂 | 31 |
| `43583602320151` | 【资源配置】op/data 多样性审计：重复 data 对组合维度零提升 | 23 |
| `43807857519255` | 单字段多形状：在有限字段数下构造低相关信号家族 | 3 |
| `42623768265111` | AI: 过线只是门槛 — DEU 五轮挖矿对「未来稳健性」的实证检验 | 23 |
| `42517702401047` | 过拟合 —— 聪明反被聪明误 🪤 | 37 |
| `44770798147735` / `43561782887575` | ATOM 篇 / Base Payment 篇（本地 `output_report/ranking_with_pyramid_20261111.md` 已引用） | 55 / 65 |

> ⚠️ 官方 Dos and Don'ts 另有「DO NOT disclose your Alpha details **or payout information** to any other person or post on any public forum or social media」。本报告含账户支付读数，属本地私有文件，**不要外发或转贴到论坛**。

---

## 4 提交对收益与 Base Payment 的影响

### 4.1 平台口径：Base 不是「每颗 alpha 各加一笔钱」

官方（论坛 `43561782887575` 引用的官方说明）：

> **"Your base payment has 4 components. Quality Factor, Quantity Factor, Self Growth Factor and Value Factor"**

且 **Value Factor 同时是 Base Payment 与 Quarterly Payment 的组成**（官方 Quarterly Payment 文档）。论坛明确标注：0–1 归一化 + 四项等权平均只是**教学假设**，真实权重、未满时计分、美元换算公式均**未公开/未核实**。

⇒ **任何「交这颗能涨 X 美元」的说法都是编的**。下面只给方向性判断与可验证事实。

### 4.2 账户实际支付现状（`get_daily_and_quarterly_payment` 实读）

| 项 | 值（USD） |
|---|---|
| 昨日（2026-11-12） | **1.30** |
| 本季累计（11-01 ~ 12-31 至今） | **19.67** |
| 上季（09-01 ~ 10-31） | **85.32** |
| YTD（至 11-12） | **151.86** |
| 历史总计 | **157.37** |
| 近 30 日单日区间 | 约 1.20 – 1.94，日均 ≈ 1.6 |

近期单日在 1.3–1.9 区间，11-12 的 1.30 处于偏低端。**单颗 alpha 的边际金额无法从公开信息推算**。

### 4.3 四维度逐项评估

| 维度 | 提交这颗的影响 | 确定性 |
|---|---|---|
| **Quantity** | ET 2026-11-13 02:09 实读：REGULAR **0/4（剩 4）**、SUPER 0/1。交 1 颗是当日有效提交，向「交满即 Quantity 满分」推进；**这是唯一确定为正的一块**。但交满后边际归零。 | **高** |
| **Quality** | 点亮 **EUR/D1/RISK 2→3**，新增 1 座已 formulated pyramid（官方 Genius 资格项 #2 + Quality 侧计数）。**但 `get_pyramid_multipliers` 实读 EUR/D1/RISK = ×1.0，是 EUR D1 全类别垫底**（other 1.5 / news 1.4 / sentiment 1.4 / model 1.3 / analyst 1.3 / earnings 1.2）。`MATCHES_THEMES` 为 WARNING ⇒ **无当期主题加成**。塔倍率是 Quality Factor 组成，按数据集类别定档；本颗是纯净 ATOM，倍率 ×1.0 不被木桶短板进一步打折，但本身也拿不到高倍率。 | 中（方向正、幅度小） |
| **Value Factor** | 官方定义：隐藏 OS + 交易约束下，检查「新 alpha 组合自身表现」「加入你的池能否提升」「加入 BRAIN 池能否提升」，并把**过拟合、高换手、重复暴露**列为不利情形。本颗：过拟合嫌疑高（−）、prod 0.6745 贴线 ⇒ 对 BRAIN 大池增量有限（−）、self 0.2062 低 ⇒ 对自有池重复度低（+）、ΔS +0.28 正向（+）、TO 4.15% 低 / margin 16.5bp / CW PASS ⇒ 成本侧干净（+）。**净方向不确定，但「IS 1.93 → OS 大概率衰减」是主要下行风险**。 | **低（最大风险项）** |
| **Self Growth** | 看近期提交 alpha 的平均表现是否改善。本颗 S 1.93 / F 1.01，属中等偏下；若近期批次平均高于此，会小幅拉低该项。 | 低 |
| **Combined Alpha Performance / Genius** | 官方：全部已提交 alpha 的 **OS 表现**组合，是 Genius 等级三项 Eligibility 之一，且 tie-breaker 用 Avg distinct Operators/Alpha（5，偏低＝加分）与 Avg distinct Fields/Alpha（1，加分）。**若这颗 OS 塌，会拖累该指标 → 影响季度 Genius 等级 → 影响 Quarterly Payment 上限**。官方还提示：季度最后一月提交的 alpha 可能不计入当季 Combined Performance，但计入当季 Quantity 与 Value、以及下季 Combined。 | 中（长期、滞后） |

### 4.4 明确的反例与不可逆风险

- **论坛 `43561782887575` 评论（CW62372）实测**：先交 1 条 Theme Alpha，Base ≈ **50 USD**；追加 2 条质量较差的非 Theme Alpha 后，总 Base **掉到 9 USD**。作者归因于「不带加成且质量差的 alpha 稀释了当期整体 Quality，Quantity 的提升抵不过 Quality 下跌」。
  ⇒ **硬凑低质量提交会净拉低 base**，这不是理论推演。
- 同帖正文「候选 B」：**「与已有表达式高度相似，靠额外噪声过相关性，成本后表现差」→ 不因只差一个名额就提交，防止伤害其他维度**。
- 论坛 `43561782887575` 评论区（SL81184）：「少用 trade_when、if_else，用不好就成了过拟合的重灾区」；（WC36825）「IS Sharpe 再好看，过拟合、高换手、高度重复都会压低 Value」。
- **提交不可逆**：`POST /alphas/{id}/submit` 后状态 ACTIVE，无法撤回；OS 表现会长期计入 Combined Alpha Performance 与 Value Factor。
- **时效性**：论坛（ZH46460）提示模拟超过约 1 个月的 alpha 提交会被 `OLD_SIMULATION` 拒。本颗 `dateCreated = 2026-11-13T01:05:54-05:00`，**今天创建，无时效风险**。

### 4.5 机会成本（比绝对影响更值得看）

ET 11-13 REGULAR 剩 4 席。总体篮子里的可执行顺位（`output_report/full_basket_ranking_20261113.md`）：

| 候选 | 点亮塔 | 该塔倍率 | 备 |
|---|---|---|---|
| `wpo8olA6` | DEU/D1/OTHER 2→3 | **1.8**（DEU D1） | 全闭环、免三问、8 ops |
| `omEdka3v` | GBR/D1/OTHER 2→3 | **1.6**（GBR D1） | 8 ops、PASS |
| `ZYQ116ln` | KOR/D1/PV 2→3 | **1.4**（KOR D1） | 3 ops |
| **`vRAgNK3w`** | **EUR/D1/RISK 2→3** | **1.0（垫底）** | 本颗，5 ops、需三问、F/sub 双贴线 |

⇒ 同样是「点亮 1 座塔 + 占 1 席 Quantity」，**前三颗的 Quality 侧倍率显著更高、过拟合嫌疑更低**。若只交 1–3 颗，本颗不应排在前面。

---

## 5 建议

**结论：能交，但降级为「补位候选」，不作为主力。**

1. **优先交** `wpo8olA6` → `omEdka3v` → `ZYQ116ln`（高倍率塔、彼此 ρ < 0.09、全闸更稳）。
2. **若今天要交满 Quantity 且只剩第 4 席**，本颗可以补位：全闸通过、self 0.2062、ΔS +0.28、成本侧干净、无 `OLD_SIMULATION` 风险。
3. **提交前必须处理 `prior` 三问**：本颗 w=0.18 是网格产物，无法如实回答「回测前由逻辑钉死」。可选做法：
   - 改用一个**先验可辩护的标准权重**（如 0.2 或 0.25）重新验证是否仍全闸 PASS；若可行则换交付件，过拟合嫌疑与三问问题同时缓解；
   - 或如实写「0.18 来自参数稳健性检验，非单一先验」，接受 Quality 侧的诚实扣分。
4. **交付前补三项低成本稳健性验证**（官方 Dos 明确建议，本轮未做）：
   - 跨 sub-universe：TOP1000 / TOP2000 各跑一遍；
   - IS 内预留最后 20% 做一次不调参的验证；
   - 2Y / 3Y / 5Y 切窗对照（论坛 `43807969440023`）。
5. **不要在 description 里美化**：三段式第三段如实带 2016 = 0.54、2021 = 0.69、CV 0.550、CLUSTER_TEST 1.01 WARNING、F/sub 各 0.01 余量。
6. **prod 0.6745 余量仅 0.0255**，提交当刻 `refresh=True` 终验；F 1.01 / sub 1.01 双贴线一并复核。

**若你的目标是最大化 base**：按论坛四维度框架，Quantity 交满是门槛不是收益 amplifier；本颗的主要贡献是 +1 座垫底倍率塔和 +1 个提交数，**而它对 Value 的贡献因过拟合嫌疑存在明确下行风险**。在配额不紧张时，把这一席留给更干净的候选更划算。

---

## 6 边界声明

- 平台**未公开** Base Payment 的真实权重、归一化方式、美元换算公式；论坛四维度等权模型是教学假设，不能据此推算金额。
- `is.checks` 全 PASS / `submit_gate passed=True` **只代表机械提交闸通过**，平台不检查过拟合；OS 表现无法从 IS 推断。
- 本报告所有支付、配额、倍率读数均为 2026-11-13 当日 API 实读，会随平台调整变化。
- 本轮**未提交任何 alpha**（提交权归用户点名）。本报告为评估，不构成提交授权。
