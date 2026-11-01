# risk68 — KOR/D1 字段画像（2026-10-30 建）

> 数据来源：`get_datafields(dataset_id="risk68", region="KOR", universe="TOP600", delay=1, filter_sharpe=false)`
> ⇒ **平台仅 5 个字段，全部 MATRIX**（无 VECTOR、无 GROUP）。
> 塔位：**risk**（KOR/D1 未点亮，倍率 1.3）。

## 1. 字段全表（平台实测）

| # | field | 类型 | cov | aC | userCount | description（平台原文摘要） |
|---|---|---|---|---|---|---|
| 1 | `rsk68_weight_volatility_short` | MATRIX | **1.0** | **503** | **258** | Short-term volatility estimate（decimal） |
| 2 | `rsk68_residual_return` | MATRIX | 0.9569 | 178 | 99 | 1-day idiosyncratic return = 实际收益 − β×market_return（decimal） |
| 3 | `rsk68_weight_edadv` | MATRIX | 1.0 | 98 | 51 | 指数衰减 dollar ADV，用作**流动性权重**（dollar units） |
| 4 | `rsk68_weight_dadv` | MATRIX | 1.0 | 94 | 53 | 简单移动平均 dollar ADV，用作**流动性权重**（dollar units） |
| 5 | `rsk68_beta` | MATRIX | 1.0 | 73 | 39 | Unitless stock beta vs 区域流动性加权 market_return（约 504 日窗口） |

## 2. 名 vs description 差异表（0.2 纪律，逐条记录）

| 差异 | 事实 | 下游后果 |
|---|---|---|
| **`weight_*` 前缀 ≠ 都是权重** | `dadv`/`edadv` 确是**权重**（dollar 量纲）；`weight_volatility_short` 是**波动率估计值**（decimal，无量纲） | 按名前缀分类会把 `weight_volatility_short` 误当规模权重丢弃 —— 而它恰是本集**最强经济轴**（aC 503） |
| **description 地域标注与本区不符** | 5 条全部写 "European asset / European instruments"，但 KOR cov = 1.0 / 0.9569 | vendor 统一管线套用到 KOR 实体。**不阻碍使用**，但说明「描述里的欧洲口径」不可用于判断样本域；以 cov 为准 |
| `beta` 的市场基准是**流动性加权** | 不是市值加权 | 与 PV 的 `cap`-加权 beta 不完全同源；若要 beta 中性化必须用它自己的 beta，不能拿 PV 字段替 |

## 3. 质量先验（0.1：按 aC 降序，TOP5 即全表）

**头部 = `weight_volatility_short`（aC 503 = 第二名的 2.8 倍，userCount 258）**
⇒ 本集**最强经济轴 = 波动率水平**（low-vol / vol-shock），不是 residual reversal。
⚠ 同时它是**全库最拥挤字段之一**：任何**水平型** low-vol 信号在被 258 个用户用过的方向上做，prod 必撞墙。

## 4. 五问（0.3）

| # | 问 | 答 |
|---|---|---|
| 1 时间维度 | beta / vol = **存量水平（恒正）**；residual_return = 日频**流量**；dadv/edadv = 存量美元额 |
| 2 相对性 | 全部为横截面可比的连续值（水平差异，非排序差异） |
| 3 被定价的是谁 | vol / beta 定价的是**风险承担**（CAPM/BAB 风险溢价，拥挤交易）；residual_return 定价的是**特质信息消化速度** |
| 4 有无博弈 | **是，且极强**：vol 字段 258 users / 503 alphas ⇒ 拥挤度最高档 |
| 5 事件性 | 均非稀疏事件；vol 平滑、dadv 平滑、residual_return 日频非稀疏 |

## 5. 机制判定（★ 开波前必读：一半字段已被别处判死）

| 机制 | 字段 | 判定 |
|---|---|---|
| **残差反转**（residual reversal） | `rsk68_residual_return` | ⛔ **已判死，直接继承** `KOR-RISK71-RESIDUAL-REVERSAL-2Y-DEAD`。本字段是 **1-day specific return**，与 risk71/risk72 的 `dsrt` 是**同一个量**；risk71 已把 setting / expression / mechanism 三类轴全试过（wave183/184，2Y 修法九种全灭），死因 = **2022–2023 结构性符号翻转**（retail theme momentum + 2023-11 卖空禁令）。翻转是**市场 regime 属性**，换数据集不换 regime ⇒ **不再投任何残差反转变体** |
| **低波动 / 低 beta 异象** | `weight_volatility_short`、`beta` | ⚠ 未判死，但**禁裸水平**（铁律 A：恒正/结构性字段裸水平 = 纯因子暴露，STATISTICAL 中性化后≈0，且 258 users 已把水平方向占满） |
| 流动性权重 | `dadv`/`edadv` | ⛔ 禁作信号（dollar 量纲、纯权重）。KOR 有 PV 的流动性字段更优，而 PV 组腿受限（用户约束 5），本集不承担该角色 |

### 5.1 本集唯一白空间 = **波动率冲击（变化率）**

拥挤的是 vol 的**水平**方向，白空间在**变化率 / 相对偏离**：`vol` 短期相对长期基准抬升 ⇒ 波动率卖方被动去杠杆 ⇒ 后续反转。
配合 KOR lit alpha 已验证几何（同源比率 → `group_rank(sector)` → `ts_rank`），主形态为**同源比值**：

```
divide(ts_mean(vol, 5), ts_mean(vol, 66))          # 波动率冲击比率（同源、无量纲）
```

## 6. A-2 收益来源声明（若开波，缺项即不许组装）

| 声明项 | 内容 |
|---|---|
| **谁在被定价** | 波动率卖方 / 追涨的散户（KOR 散户占比高，波动率外推偏差最大的人群） |
| **为什么会被错** | **波动率冲击被过度外推**：短期 vol 抬升被解读为风险扩散（风险平价与 vol-target 资金机械减仓），实际多为流动性冲击，随后均值回复（Nagel 2012 机制） |
| **错了多久修复** | 5–22 日（冲击 → 月内回复） |
| **预期方向** | vol 冲击抬升 ⇒ 后续跑输 ⇒ `multiply(-1, vol_ratio)` 做空冲击 |

## 7. 双通道取证

**通道 A（论坛）**：✅ **已取证（2026-10-30，`search_forum_posts("volatility shock")`）**，结论 = **本机制专属模板不存在**，
只捞到两条**可迁移的邻近件**：

| post | 票 | 内容 | 可用性 |
|---|---|---|---|
| `41939959839895` | 41 | **波动率 regime 门控模板**：`trade_when(rank(volatility,60)>0.3, <signal>)` —— 高波动状态下才持仓 | ⭐ **直接可迁移**：与 Nagel (2012)「高波动期反转收益更大」同向 ⇒ 本波第 4 条腿用它把主信号限定在高波动状态 |
| `43607291078935` | 29 | 特质波动率之谜（IVOL 高 ⇒ 后续低收益） | ⛔ **不可迁移**：该帖的落地集是 **risk60**，`KOR-RISK60-CROWDING-NOSIGNAL` 已判死；且 IVOL 是**水平型**，与 258 users 占满的方向重叠 |

⚠ **无结果 ≠ 无机制**：检索式偏窄（只用「volatility shock」）⇒ 记为「**本机制无平台表达模板**」，
按 ②.d 归入「B 有机制、A 无对应表达」⇒ **按 A-1 五问自建骨架**（即 §9 的 1–3 条），第 4 条用 A 通道给出的 regime 门控。

**通道 B（论文）**：

| 文献 | 可证伪结论 | 本区可迁移性 |
|---|---|---|
| **Nagel (2012, RFS) "Evaporating Liquidity"** | 短期波动率抬升 ⇒ 短期反转收益变大（做市商退出）⇒ 给「vol 冲击 → 反转」的**方向句 + 数日持有期** | ⭐ **最贴本波**：把本集的 vol 变化率与反转方向直接接上 |
| Ang, Hodrick, Xing, Zhang (2006, JF) | 高 IVOL ⇒ 后续低收益（IVOL 异象，USA 1963–2000） | 机制依据，但**是水平型**；本区水平已被 258 users 占满 ⇒ 只借机制、不借形态 |
| Frazzini & Pedersen (2014, JFE) BAB | 低 beta 组合经**杠杆**后跑赢高 beta | ⚠ **REGULAR 无杠杆** ⇒ 纯 beta 价差强度必然被砍半，只作次选 |
| Bali, Cakici, Whitelaw (2011, JFM) MAX | 高极端日收益 ⇒ 后续低收益 | ⚠ 需日收益分布，本集无 ⇒ 不可迁移 |

⚠ **文献偏误**：全部 USA 大盘样本。KOR 散户占比高、卖空受限（2023-11 起禁令）⇒ 波动率异象方向可能相同但幅度更小、更容易被噪声淹没。**先当假说，本区实测定生死。**

**双通道裁决（2026-10-30 完成）**：B 有机制（Nagel 2012 给方向句 + 5–22 日持有期）、A **无本机制专属表达**但给了
**regime 门控模板**（`41939959839895`）⇒ 归入「B 有机制、A 无对应表达 = 最有价值」情形：**按 A-1 五问自建骨架**，
门控件作为第 4 条腿（见 §9）。**A 通道已完成检索并留证**，可发波。

## 8. 十年覆盖验证（用户约束 4）

cov 全 1.0（`residual_return` .9569）⇒ **无结构性缺年风险**，与 other106/sentiment27 完全不同档。
判定法仍照铁律：首波第一批落地后立刻 `get_alpha_yearly_stats`，看 2014–2018 的 `longCount` 是否非零。

## 9. 波次设计（wave 194，≤4 = 铁律 G 新线探针的收窄档）

> 只有 **1 个未判死机制**（波动率冲击），所以本波是**方向对照 + 门控对照 + 轴对照**，不是「4 个不同想法」。

| 序 | 表达式（草） | 判别目标 |
|---|---|---|
| 1 | `group_rank(multiply(-1, divide(ts_mean(rsk68_weight_volatility_short, 5), ts_mean(rsk68_weight_volatility_short, 66))), sector)` | ⭐ 主假设：vol 冲击反转（Nagel 方向；同源比值 ⇒ 无量纲） |
| 2 | `group_rank(divide(ts_mean(rsk68_weight_volatility_short, 5), ts_mean(rsk68_weight_volatility_short, 66)), sector)` | 铁律 B：显式反向各测（`reverse()` 非精确反号） |
| 3 | `group_rank(ts_delta(rsk68_beta, 66), sector)` | 次选机制：beta **漂移**（非水平）是否独立有效 |
| 4 | `trade_when(greater(ts_rank(rsk68_weight_volatility_short, 252), 0.6), group_rank(multiply(-1, divide(ts_mean(rsk68_weight_volatility_short, 5), ts_mean(rsk68_weight_volatility_short, 66))), market), -1)` | **A 通道 regime 门控**（帖子 41 票）+ `market` 轴对照：只在自身高波动状态做冲击反转（Nagel：高 vol 期反转更强） |

**设计纪律**：① 4 条全为 `risk68` 单集 ATOM；② 1–3 用 `sector`（KOR 禁 `industry`），第 4 条用 `market` 作轴对照；
③ **不碰 `residual_return`**（继承判死）；④ 首批 2 条落地**先读 yearly_stats**（虽 cov 1.0，仍照铁律执行），再看 prod（本集拥挤度最高，`prod_first_skeleton_v1`）；
⑤ **预置砍波判据**：批 1（1–2 条）落地若 max\|S\| < 1.0 **且** max\|2Y\| < 1.0 ⇒ 剩 2 条不发即 kill；
⑥ 若第 1 条过 near 线但 TO 超 .136，**先上 `hump` 压 TO**（不改持仓的平滑杠杆，`wq-prod-lever-self-lock-guard`），不加新腿。

## 10. 禁区

- ⛔ `rsk68_residual_return` **禁作任何反转/动量信号**（继承 `KOR-RISK71-RESIDUAL-REVERSAL-2Y-DEAD`）。
- ⛔ `rsk68_weight_dadv` / `rsk68_weight_edadv` **禁作信号**（dollar 量纲 = 权重，不是信号）。
- ⛔ vol / beta **禁裸水平做多空**（铁律 A + 258 users 已占满水平方向）。
- ⛔ 不与 PV/MODEL/OTHER 组腿（用户约束 5 的 5 条额度留给更高价值组合，risk 塔乘数仅 1.3）。
- ⚠ 本集 prod 风险**结构性偏高**（`weight_volatility_short` aC 503 / userCount 258）⇒ 任何候选进 S5 前必须 `check_correlation(refresh=True)`，
  且**首颗就要查**（`prod_first_skeleton_v1`），不要摊完 4 条再查。

## 11. 实测记录

### 11.1 wave 194 实测（2026-10-30 收批）—— ⛔ 机制判死，risk 塔关闭

| alpha | 核心 | S | F | 2Y | TO | DD |
|---|---|---:|---:|---:|---:|---:|
| `leAJNQQA` | vol 5/66 短长比，**反向** | −0.50 | −0.22 | −1.23 | .1450 | .3341 |
| `78Lg2aa5` | 同式正向 | +0.18 | +0.05 | +0.64 | .1448 | .2068 |
| `A1Vq2z9Y` | `ts_delta(rsk68_beta,66)` | +0.09 | +0.02 | −0.54 | .1217 | .1307 |
| `omEQkG76` | `trade_when(ts_rank(vol,252)>0.6, …)` | −0.11 | −0.02 | −0.33 | .1210 | .1627 |

**`max|S| = 0.50`、`max|2Y| = 0.64`，0 candidates / 0 near ⇒ 预置砍波判据触发。**

1. **【铁律 B 已双测】** 波动率短长比正/反两臂 `+0.18 / −0.50`，**不精确反号** ⇒ 印证「猜方向系统性错」，但两侧都远低于 near 线。
2. **【⚠ 2Y 不可信】** 唯一 \|2Y\|>1 的 `leAJNQQA`（−1.23）与其 IS（−0.50）**同号但幅度 2.5 倍**。按决策表「IS 与 2Y 幅度严重背离 ⇒ 不可信」，
   **不得**把 −1.23 当成「有强 2Y 信号」的证据（若照抄会被骗去做参数微调）。
3. **【2Y 结构性不可达】** `78Lg2aa5` 逐年 S：2014 +2.21 / 2015 −0.51 / 2016 −2.13 / 2017 +0.46 / 2018 +1.32 / 2019 −1.56 / 2020 +0.74 / 2021 −0.23 / 2022 +0.30 / 2023 +0.93
   ⇒ **S<1.0 年份 6/10（>3 成）**，且正负翻转 6 次 ⇒ LADDER 上限被卡死，**任何 decay / 平滑档都不可达**。
4. **【单年集中度】** 2014 年 PnL 918,472 = 正收益合计的 **29.7%**（过拟合指纹，< 30% 但已贴近）。
5. **【覆盖 PASS】** longCount 290–341/年，2014–2023 无空年 ⇒ **死因是机制不是数据**（本区第 5 个满足约束 4 却机制判死的集）。
6. **【为何 STATISTICAL 吃掉了它】** 短长波动率比是**风格载荷很重**的构造（低波/高波切换），STATISTICAL 中性化正好把它投影到的风格因子上消掉。
   `volatility_short` aC 503 / userCount 258 是**全库最拥挤**字段 ⇒ 水平方向已被占满，变化率方向的残余信息在本区被中性化抹平。

**继承（下一波准入）**：
- ⛔ **risk 塔关闭**：risk68 机制死 + risk72 五字段同源拷贝（0 槽）+ risk88 `ri_*` 风格载荷。剩余 risk 数据集（risk70 属 IND 经验，未在 KOR 画像）不得在无新机制证据时投槽。
- ⛔ 波动率类构造**禁再做「短长比」形态**（本区已实测两侧皆弱）。

## 12. 追加禁区（wave 194 后）

- ⛔ **不做短长波动率比**（正反两臂 −0.50 / +0.18，KOR/STATISTICAL 下无残余）。
- ⛔ 看到 \|2Y\| 明显大于 IS 时**先按不可信处理**，不得作为加仓/微调依据。
