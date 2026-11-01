# other553 — Financial Opinion Mining（KOR / TOP600 / Delay 1）

> 画像日期 **2026-10-30**（`get_datasets` + `get_datafields(filter_sharpe=false)` 实测，21/21 字段）。
> **平台 category = `sentiment`（金字塔乘数 1.6）**，不是 `other` ⇒ **按名字归类会把它错归到 macro/other 塔**。
> ⚠ 归属另有隐患：用户约束 5 点名 "OTHER 下字段"。本集**名字前缀是 other**、平台 category 是 sentiment ⇒
> **本集一律只做 ATOM，不参与任何组腿**（既避开 `other` 组腿禁令的争议，也避开跨塔混淆）。

## 0. 元信息（平台实测）

| 项 | 值 |
|---|---|
| coverage | **0.6243**（sentiment 塔中最高的非死集） |
| fieldCount | 21（**全 VECTOR**） |
| userCount / alphaCount | 66 / 96 |
| valueScore | 5 |
| pyramidMultiplier | 1.6（未点亮塔） |

## 1. 字段分类（按 description 语义；21 字段 = 4 标的口径 × 4 属性 + 1 元数据）

| 族 | 字段 | coverage | aC | 语义 |
|---|---|---|---|---|
| **价格目标 ptg** | `oth553_ptgvalue` | .5838 | 2 | **当前**价格目标 |
| | `oth553_preptgvalue` | .5049 | 2 | **上一期**价格目标 ⇒ **与 ptgvalue 成对** |
| | `oth553_ptg_analyst` | .5838 | 1 | 给 PT 的分析师家数 |
| | `oth553_ptg_isprevspeak` / `_yearspeakcnt` | .5838 | 1 / 0 | 是否有"相关演讲" / 年内演讲次数 |
| **评级 rec** | `oth553_recvalue` | .4844 | 7 | **当前**评级值 |
| | `oth553_prerecvalue` | .4844 | 7 | **上一期**评级 ⇒ **成对** |
| | `oth553_rec_analyst` | .4844 | 4 | 给评级的家数 |
| | `oth553_rec_isprevspeak` / `_yearspeakcnt` | .4844 | 1 / 1 | 演讲标记 / 次数 |
| **盈利预测 est** | `oth553_est_estvalue` | .7397 | 33 | **当前**一致预期值（本集 aC 最高） |
| | `oth553_est_preestvalue` | .6555 | 9 | **上一期**预期 ⇒ **成对** |
| | `oth553_est_analyst` | .7397 | 12 | 家数（**广度轴**） |
| | `oth553_est_isprevspeak` / `_yearspeakcnt` | .7397 | 6 / 1 | 演讲标记 / 次数 |
| **营收预测 sal** | `oth553_sal_estvalue` | .7485 | 11 | **当前**营收预期 |
| | `oth553_sal_preestvalue` | .6565 | 0 | **上一期**（aC=0 ⇒ **全库没人用过**） |
| | `oth553_sal_analyst` | .7485 | 8 | 家数 |
| | `oth553_sal_isprevspeak` / `_yearspeakcnt` | .7485 | 7 / 1 | 演讲标记 / 次数 |
| **元数据** | `oth553_horizon` | .5838 | 0 | 时间跨度 ⇒ **禁作信号**（与 `_t` 时戳同类） |

## 2. 名 vs description 差异表（★ 本集最大坑）

| 字段 | 名字暗示 | description 实际 | 后果 |
|---|---|---|---|
| `est_preestvalue` / `sal_preestvalue` | "pre" 可能被当成"预测前" | description 写的是 **"Value of current estimates"**（与当期字段逐字相同）⇒ 按 description 会被当成**重复字段** | ⛔ **必须按名字 + 成对性判定**：这是**上期值**，是差值腿的对侧。若信 description，本集最强的「修正」几何会被整体错过 |
| `*_isprevspeak` | "speak" 像分析师电话会 | 是 **"previous speech related to …" 的存在性标记** = **话语披露事件**，不是分析师 | 这是一个**独立的注意力/披露轴**，别混进修正腿 |
| `*_yearspeakcnt` | 像"分析师人数" | **年内相关演讲次数** = 披露频率 | 与 `*_analyst`（家数）不同机制，**禁同时入式**（会变成注意力计数混信号） |
| `oth553_recvalue` | 像"推荐数量" | **评级值本身**（数值刻度） | `subtract(recvalue, prerecvalue)` 才是升降级 |
| 数据集名 "Financial Opinion Mining" | 像社媒/舆情挖掘 | 实际字段全是**卖方预测 + 价格目标 + 评级 + 演讲计数** | 机制是**卖方修正**，不是情绪 ⇒ 与已判死的 news 情绪族**不同机制**（可挖） |

## 3. 字段画像五问（A-1）

1. **时间维度**：`value` 是**存量水平**（PT/评级/预期），`pre*` 是上期快照 ⇒ **差值就是修正**（铁律 A：水平单边恒正 ⇒ 取变化率）。
2. **相对性**：修正幅度要横向比（`ts_delta` 后 `group_rank`），水平值要 `ts_zscore`。
3. **被定价的是谁**：**卖方分析师修正的方向**（不是"多少人在说"）。
4. **有无博弈**：有 —— 修正已被大量使用（aC 33）⇒ 需要规模/流动性中性，但本塔只有 1.6 倍率、**别加太多壳**。
5. **事件性**：`isprevspeak` / `yearspeakcnt` 是**离散事件**（稀疏）⇒ 若用必须 `trade_when` 门控，**禁裸 rank**；`value` 族是连续量，可裸 rank。

## 4. A-2 收益来源声明（主机制：价格目标/评级修正的**信息扩散滞后**）

| 项 | 内容 |
|---|---|
| **谁在被定价** | 迟到的买方（散户 + 小机构）：卖方修正先到，价格分 5–22 日才吸收完 |
| **为什么会被错** | 有限注意力 → 修正的**方向**被记住、**幅度**被低估；KOR 卖方覆盖薄（家数 1–3）⇒ 单条修正的信息含量被系统性低估 |
| **错了多久修复** | **5–22 日**（Womack 1996 的 1 月窗口；Brav-Lehavy 2003 的 PT 修正 1–3 月）⇒ 本区取 22 日 `ts_delta` |
| **预期方向** | PT 上调 / 评级上调 ⇒ 后续**涨**（正向）；下调 ⇒ 跌。**"被高估 ⇒ 后续跌"在修正轴 = 下调 ⇒ 跌** |
| **失效条件** | ① 分析师家数为 1 时修正 = 换人而非调观点（`*_analyst` 可当门控）；② 覆盖 .48–.75 ⇒ 无覆盖股不在域，不是缺数据 |

## 5. 双通道取证

**通道 A（论坛）** —— ✅ 完成（2026-10-30，`search_forum_posts("price target revision")` 50 命中，读正文 1 篇）：

| post | 票 | 可落地内容 |
|---|---|---|
| `42659792904343`「121 个字段里最值得做的 5 个信号」 | **30** | ⭐ **① 修订动量是首选**（"数据集通常没有原生 revision 字段，需 `ts_delta` 自造"；"比预期绝对水平更强"）；**⑤ `numofests` 作质量过滤**（覆盖稀疏股噪声大）；实现提醒：**coverage ~0.5 必须 `ts_backfill`**。其余 3 条（区间位置 / 预期偏度 / 利润率剪刀）需 low/high/median 字段，**本集没有 ⇒ 不可移植** |
| `34926922792855`「Consensus Analyst Target Prices」 | 4 | `PRET = (target − price)/price`，有效性受 **dispersion** 调节（低分歧更有效）⇒ **需要股价**，本集无价 ⇒ 非 ATOM，**不采** |
| `35026706128279`「分析师预期的动态估值因子」 | 15 | 已提交配方 = 目标价 / 市值 ⇒ **跨塔（需 PV cap）**，本轮 ATOM 不采 |

**裁决**：A 与 B **指向同一机制**（PT 修正漂移，Brav-Lehavy 为主）⇒ ⭐ 优先组装；A 额外给两条**本区可用的实现纪律**：`ts_backfill` 前置 + `*_analyst` 家数作门控/过滤。
> ⚠ 本塔另一条前科必须先读：`analyst25/analyst14` 的 KOR 配方（`tracking/KOR/reference/datasets/analyst*.md`），避免与已点亮的 analyst 塔（2 颗）prod 撞墙。

**通道 B（论文）**：

| 文献 | 可证伪结论 | 本区可迁移性 |
|---|---|---|
| **Womack (1996, JF)** | 评级**变更**（不是水平）后有 1 月–6 月漂移，**上调弱、下调强** | ⭐ 直接给「双向不对称」：下调腿优先 |
| **Brav & Lehavy (2003, FAJ)** | **价格目标修正**比评级更有预测力；PT 上调后 1–3 月超额 | ⭐⭐ 本集 `ptgvalue/preptgvalue` 正是这个量的原生实现 |
| **Jegadeesh, Kim, Krische & Lee (2004, JF)** | 一致预期**修正幅度**与**广度变化**（家数变化）是两个独立因子 | ⭐ 给「`est_estvalue` 修正 × `est_analyst` 广度」两条腿的**分开判据** |
| **Bonini, Zanetti, Bianchini & Salvi (2010)** | 分析师"喊话"频率（speech count）与覆盖质量相关，可作门控 | ⚠ 弱证据；本集 `yearspeakcnt` 只能当门控 |

⚠ **文献偏误**：全部 USA/EU 样本，KOR 卖方以本土券商为主、覆盖家数少（1–3）⇒ **先当假说**。
⚠ **与已点亮 analyst 塔的重复风险**：本集机制 = 卖方修正，**analyst 塔在 KOR 已有 2 颗** ⇒ **首条腿必须先查 prod**（`prod_first_skeleton_v1`）。

## 6. 近十年覆盖验证（用户约束 4）

⚠ 本塔**已有覆盖前科**：sentiment27 死于 2014–2018 连续 5 年 `longCount=0`（wave 189）。
**判定法**：首波批 1 落地后立刻 `get_alpha_yearly_stats`，**2014 起任一空年 ⇒ 整集退出**。

## 7. 波次设计（wave 192，≤4 条；探针级 —— 本集与 analyst 塔同机制）

| 序 | 表达式（草） | 机制 / 目的 |
|---|---|---|
| 1 | `group_rank(ts_delta(ts_backfill(vec_avg(oth553_ptgvalue), 22), 66), sector)` | ⭐ **价格目标修正**（Brav-Lehavy 主腿 + 论坛 30 票帖「修订动量首选」） |
| 2 | `group_rank(multiply(-1, ts_delta(ts_backfill(vec_avg(oth553_ptgvalue), 22), 66)), sector)` | 铁律 B 显式反号 |
| 3 | `group_rank(ts_backfill(divide(vec_avg(oth553_ptgvalue), vec_avg(oth553_preptgvalue)), 22), sector)` | **同源比率**：PT 倍率（= 1 + 修正率，无量纲；与差值轴互补） |
| 4 | `group_rank(ts_delta(ts_backfill(vec_avg(oth553_est_analyst), 66), 66), sector)` | **广度变化**（Jegadeesh 第二因子；不是修正幅度） |

⚠ **预置砍波判据（照 189/190/191）**：批 1（1–2 条，主假设）落地后若 max\|S\| < 1.0 **且** max\|2Y\| < 1.0 ⇒ 剩 2 条**不发即 kill**，只写归因。
⚠ **批 1 落地后第一件事**：`get_alpha_yearly_stats` 验十年覆盖（本塔已有 sentiment27 前科）。批 1 第一条还须 `check_correlation(refresh=True)` 查 prod（`prod_first_skeleton_v1`，analyst 塔已有 2 颗）。

**准入**：sector/market 轴；全 VECTOR 必须 `vec_avg`；`horizon` / `*_isprevspeak` / `*_yearspeakcnt` **本轮不用**
（前者是元数据，后两者是事件计数 ⇒ 属另一轴，需 `trade_when` 门控，留次波）；每批 2 条串行。
**次波（若批 1 存活）**：把论坛给的 `*_analyst` 家数当 **`trade_when` 质量门**（`greater(ts_backfill(vec_avg(oth553_ptg_analyst),22), 3)`），套在存活腿上——这是 A 通道独有的可落地增量。

### 7.1 实测结果（wave 192，2026-10-30 收官；⛔ 机制判死）

批 1 = 主腿正/反（multisim `fXrtrbsX5jtbmGuIJ91C8K`，2 条 COMPLETE，err 0）：

| alpha | 表达式臂 | S | F | TO | 2Y | subU | CW |
|---|---|---|---|---|---|---|---|
| `rKRQ8MYa` | 正向 `ts_delta(ptgvalue,66)` | **+0.13** | 0.02 | .2474 | **+0.66** | −0.11 | PASS |
| `58ENYdbo` | 反向 | **−0.28** | −0.07 | .2475 | **−0.95** | −0.02 | PASS |

- **预置判据触发**：`max|S| = 0.28 < 1.0` **且** `max|2Y| = 0.95 < 1.0` ⇒ **legs 3–4 未发即 kill**（表达式留在 `expressions` 表 status=pending，未消耗配额）。
- ⭐ **十年覆盖 PASS（本集首次实测）**：`rKRQ8MYa` 逐年 longCount = 286/302/310/317/328/326/325/343/324/329（2014→2023），**无一空年** ⇒ 死因是**机制**不是数据，与 189 sentiment27（2014–2018 全空）形成对照。
- **归因①单年集中度**：2014 PnL `+1,208,467`，占正收益总和 `1,947,158` 的 **62%**（>30% ⇒ 过拟合指纹，按决策表换机制族、不扫参数）。
- **归因②符号不稳**：年度 S = +2.2 / −0.11 / −1.11 / −0.37 / +0.01 / −0.95 / −0.19 / +0.10 / +0.98 / +0.39 ⇒ 正反两臂都拿不到稳定符号（铁律 B 再次证明「猜方向系统性错」）。
- **归因③铁律 E**：raw 与 2Y **同步走弱**（2Y .66 / −.95 均远低于闸 1.58）⇒ 信号自身衰减，**不是中性化档问题** ⇒ 不扫中性化档。
- **归因④TO**：.2474 是成功带 .075–.136 的 **约 2 倍**，但 S 本身只有 0.13 ⇒ 降 TO / 平滑只修 F 不改 S，该族**不缺平滑**（不扫 hump/decay）。
- **未发余额**：legs 3–4（`ptg/preptg` 同源比率、`est_analyst` 广度变化）保留在表内。若要复燃，必须先给出**独立的新经济证据**（例如 est_analyst 覆盖广度轴在 KOR 的单独先验），不得无证据重发。

> **塔级继承**：sentiment 塔至此**三连死** —— 189 `sentiment27` 覆盖判死 / 190 `other106` 机制判死 / 192 `other553` 机制判死。
> 剩余唯一攻击面 = **`sentiment26`**（19 全 VECTOR、cov .356、aC ≤7 最不拥挤），且**开波前必须先验十年覆盖**（同塔已两次因覆盖/机制死）。

## 8. 禁区

- `oth553_horizon` **禁作信号**（元数据）。
- `*_isprevspeak` / `*_yearspeakcnt` **禁裸 rank**（稀疏事件/计数 ⇒ 与已判死的注意力计数族同形）。
- `est_*` 与 `sal_*` **禁同时入式**（同一"预测"机制的两个标的口径 ⇒ 混信号）。
- `ptgvalue` 与 `preptgvalue` **只允许差值/比率**，禁 `add`（同源相加 = 混信号铁律）。
- 本集**一律 ATOM**：不参与任何组腿（用户约束 5 的 `other*` 命名歧义 + 跨塔混淆风险）。
