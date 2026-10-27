# ATOM 生产流程 + 回测归因（论坛经验整合，2026-10-15）

> 源：①《【新人科普】BRAIN 平台上的四类 Alpha（RA, ATOM, PPAC, SA）》(MH33574, 199 赞 / 85 评论)
> ②《【经验分享】从 Gold 到 Master》》(FF65210, 69 赞) ③《⚡极端事件中因子表现的归因分析》(DA98440)
> ④《📊绩效归因实操：把你的 PnL 拆成 Alpha 和 Beta》》(DA98440) ⑤《新人保姆级别跑因子流程》(TT73161)
> ⑥ 关键实测评论（XW76815, 2026-09-11；YL61874）

---

## 一、流程确认：是「发给 AI 出模板 → 回测」吗？

**方向对，但顺序要改。** 论坛「保姆级流程」（TT73161）原文：

> `ai生成模板 → 总结论坛优化模板 → 生成实验因子并分析 → 调整模板 → 一键跑因子`

**但你已经做了体检，情况不同了。** 关键区别：

| 阶段 | 没有体检数据 | **有体检数据（你的情况）** |
|---|---|---|
| AI 的角色 | **发明**模板（开放式） | **翻译**体检结论为表达式（受约束） |
| 模板来源 | 论坛模板库 / 让 AI 自由发挥 | **体检读数已经确定了模板骨架** |
| 风险 | 模板与字段性质不匹配 → 白跑（我 d276-A 波踩过） | 风险大幅下降 |

**高赞帖（FF65210, 69 赞）的三条反直觉结论**：
1. **「模板少即是多」** —— 选 3–5 个理解透彻的模板深挖，不要贪多；同模板 × 不同字段/区域/周期，产出的 alpha 多样性已经足够
2. **「数据选择比模板更重要」** —— 好的数据 + 简单模板 > 差的数据 + 复杂模板
3. **坑 2「忽视数据理解」** —— 无脑跑模板效率很低；**这正是体检要解决的问题**

⇒ **修正后的流程**：
```
体检六法读数
  ↓ （已确定骨架：用什么算子 / 什么窗口 / 禁用什么）
生成表达式（AI 可代劳，但必须受体检结论约束）
  ↓
ATOM 合规检查（字段是否同数据集 / 算子数）
  ↓
回测（multisim 8 条/批）
  ↓
★ 归因（四类，见 §三）
  ↓
判活（→ S4/S5 推闸）/ 半活（→ 换构型）/ 死（→ 回写）
```

---

## 二、ATOM 的硬约束（论坛原文 + 实测评论）

### 2.0 官方锚定（2026-10-26 复核，**判据以此为准**）

平台文档 `single-dataset-alphas`（标题「❗ Single Dataset Alphas」，`Creating Alphas` / sequence 150 /
lastModified 2026-09-18）只有两条属性，逐字引用：

> ①「Single Dataset Alphas must utilize data fields from **only one dataset**, with exceptions for the
> following **6 permitted grouping fields** – country, exchange, market, sector, industry and subindustry.」
>
> ②「The use of **`inst_pnl()` and `convert()`** operators is considered as utilizing the **pv1** dataset
> since these operators rely on pv1 data for calculations.」

**"ATOM" 是论坛简称**（MH33574《四类 Alpha》199 赞），平台正式名是 **Single Dataset Alpha**。
⇒ 本文所有经验条目都是对这两条的展开；与之冲突的按官方原文。

**项目实现的三处纠正（2026-10-26，`src/wqb/expression/atom.py`）**：

| # | 旧 | 新 |
|---|---|---|
| a | 基础行情记作伪数据集 `BASE_MARKET` | 属 **`pv1`** ⇒ `pv1 字段 + returns` 仍是 ATOM（旧版误判 combined） |
| b | 只看字段不看算子 | `inst_pnl()` / `convert()` 计为引用 pv1（旧版假阳） |
| c | 分组豁免名单含 region/asset/group 等自造键 | 官方**恰好 6 个**（见上），其余不豁免 |
| d | 按模板族判（`res`/`reslag`/`pp` 一律非 ATOM） | 模板族只是**代理预警**；判据永远是字段级 dataset id 唯一 |

⚠ 文档表格的 2Y 阈值（D1 2.38 / D0 3.96）与平台实际回报的 limit 不一致：IND/D1 `O0JLn561`
（单数据集、2Y=1.73）在 `checks` 里是 **`LOW_2Y_SHARPE` PASS** ⇒ 实线 ≤1.73。**以平台回报为准**。

| 项 | 规则 | 出处 |
|---|---|---|
| **字段** | 所有数据字段必须来自**同一数据集** | 正文 |
| **豁免** | **恰好 6 个** group 字段不计入数据集限制：`country` / `exchange` / `market` / `sector` / `industry` / `subindustry` | **平台文档 `single-dataset-alphas`**（lastModified 2026-09-18）；⚠ 本文旧版只写「`industry` / `country` 等」并记为 4 个，**已按平台原文更正为 6 个** |
| **检测差异** | **免 IS Ladder Sharpe 测试**，改为「Last 2Y Avg IS Sharpe ≥ 阈值」：D1 = **2.38** / D0 = **3.96**；且「**若 turnover < 30%，IS Sharpe Ladder PASS_THRESHOLDS × 0.85**」⇒ D1 低换手实际线 **2.023** | 平台文档 `single-dataset-alphas` |
| ⚠ **口径冲突（未解，按平台实测线执行）** | 文档写 2.38/2.023，但 EUR/D1 实测 `checks` 数组里 `LOW_2Y_SHARPE` 的 `limit` = **1.58**；`786pLKnb` 2Y=1.78 / TO=0.1124 / `failed_ra=0` / **ACTIVE** ⇒ 按文档线它该被拦，实际已提交成功。**裁决：以平台按区域回报的 `limit` 为准，文档表格视为全局缺省** | 本轮实测 |
| ⚠ **陷阱** | `inst_pnl()` / `convert()` **计为使用 pv1** ⇒ `inst_pnl(<非 pv1 字段>)` **不算 ATOM**。**平台原文**：「The use of inst_pnl() and convert() operators is considered as utilizing the pv1 dataset since these operators rely on pv1 data for calculations.」⇒ 这条是文档级明文，不只是论坛评论 | 平台文档 + YL61874 评论 |
| ⚠ **陷阱** | 判「同一数据集」要看 **dataset id**，**不要按字段名/前缀猜** —— 名字像同库、实际属另一类别 | XW76815 评论 |
| ⚠ **陷阱** | `vector_neut(x, size)` 之类以 **pv1 字段**（`size` / `cap` / `returns` / `close`…）为第二参数的写法 = 混 pv1 ⇒ **破坏 ATOM**（同 `inst_pnl` 法理） | 由上条明文推出 |
| 特别提示 | 平台把部分**硬性**检查放在 WARNING 里（Weight Concentration、RA 的 2Y）；「只有 WARNING」≠ 可提交。**本轮实测坐实**：`d5KR2gOY` 的 `checks.fail = []`（空）但 `failed_ra_count = 1`，因为 `LOW_2Y_SHARPE 1.50 vs 1.58` 落在 `warning` 数组里 | YL61874 评论 + 本轮实测 |
| 配额 | `REGULAR_SUBMISSION` 配额满时 `LOW_SHARPE`/`LOW_2Y` 会降级为 WARNING ⇒ 先查配额再判读 | 同上 |

### 2.1 ★ 「混数据集」与 ATOM 的边界（平台定义，2026-10-19 查证）

**三层结构，边界画在第二层：**

```
category（类别，如 pv / analyst / fundamental / model / risk …）
   └── dataset（数据集，有唯一 dataset id，如 pv87 / pv30 / analyst_factor_signals）
          └── data field（字段，如 pv87_daily_ann_matrix_r1_ebit_consensus_mean_numup）
```

**平台原文两句，直接把两层对立起来：**

> 「BRAIN offers a wide array of datasets spanning various **categories**, including fundamental, price-volume, analyst, and options data. While an alpha can incorporate data fields from **multiple datasets**, this approach if not implemented correctly, may potentially lead to overfitting due to the mixing of conflicting signals **between datasets**.」
>
> 「Single Dataset Alphas must utilize data fields from **only one dataset**, with exceptions for the following **6 permitted grouping fields** – country, exchange, market, sector, industry and subindustry.」

⇒ **ATOM 的计数单位是 dataset id，不是 category。** 同 category 下的两个不同 dataset id 混用 = 混两个数据集 = **不是** Single Dataset Alpha。

**EUR/D1/TOPCS1600 实测取证**（`get_datasets`，count=91）：category `pv` 下并列 **20 个** dataset id —
`continuation_score` / `intraday_pv_feats` / `investor_activity` / `pattern_scores` / `pv1` / `pv103` / `pv106` / `pv109` / `pv13` / `pv141` / `pv149` / `pv173` / `pv20` / `pv29` / **`pv30`**（Alternate Industry Classification，558 字段）/ `pv37` / `pv47` / **`pv87`**（Aggregated dataset，1649 字段）/ `univ1` / `univ2`。
⇒ `pv87` 与 `pv30` 是**同一 category、两个独立 dataset id**，`group_rank(pv87字段, pv30标签)` **确实破坏 ATOM**。原判断成立。

**为什么容易混（三处结构性原因）：**

| 子系统 | 计数单位 | 证据 |
|---|---|---|
| **金字塔（pyramid）** | **category** | `pv87` → `EUR/D1/PV`（mult 1.1）；`analyst_factor_signals` → `EUR/D1/ANALYST`（mult 1.3） |
| **ATOM 资格** | **dataset id** | 平台文档原文「only one dataset」 |
| **数据 API** | **dataset id** | `get_datafields` 的 `dataset_id` 是**必填**参数；`fieldCount` 逐 dataset 计（`analyst_factor_signals` = 108） |

⇒ 「塔按 category 点亮、ATOM 按 dataset 判合规」是**两套并行口径**，不能互相代入。DB 曾把 `786pLKnb` 的 `dataset_id` 写成 `analyst_factor_signals+pv1`（`+` 拼接形态），正是把豁免的 `industry` 误当成 pv1 数据集的产物 —— 该 alpha 实际只用了 `analyst_factor_signals` 字段 + 豁免 group 字段 `industry`，**是合规 ATOM**（平台侧 `failed_ra=0` / ACTIVE 佐证）。

**可操作判据（发批前自查三问）：**

1. 表达式里每个**非豁免**字段的 dataset id 是否**唯一**？（豁免名单只有那 6 个，`sector`/`industry`/`subindustry`/`country`/`exchange`/`market`）
2. 是否出现 `inst_pnl()` / `convert()`？出现即**视为引入 pv1** ⇒ 除非本体就是 pv1，否则不合规。
3. 是否用 pv1 字段（`size`/`cap`/`close`/`returns`/`volume`/`vwap`…）当**算子参数**（`vector_neut(x, size)`、`group_neutralize(x, bucket(rank(cap)))` 等）？同样视为引入 pv1。
   ⚠ 反之，`bucket(rank(<本数据集字段>))` 自建分组是**安全**的 —— 平台《Group Data Fields》明文：「you can also create new group using bucket() operator … based on value of **any data field**」，只要那个 data field 属于本数据集。

### ★ 对本项目的直接含义（重要）
**我本轮体检选的数据集（`fundamental44` / `fundamental90` / `other395` / `other452` / `other401`）全部是单数据集字段**
⇒ **天然满足 ATOM 的字段条件**，且**免 IS Ladder**（只需过 2Y）。
⇒ 这意味着：**体检工作顺带把 ATOM 的字段合规问题解决了**。之前担心的「混信号」在 ATOM 框架下从设计上被排除。

---

## 三、★ 论坛最强的 ATOM 经验：2Y 是唯一真瓶颈

**XW76815（2026-09-11）实测原话**：

> 「ATOM 的真瓶颈不是字段数，**是 2Y**。我们有一批组合把 Sharpe 做到 1.61、fitness 0.74、Sub-Universe 1.01，**2Y 却只有 1.11**（门槛 1.58）；那一批里单腿最好的 2Y 也只有 1.39。卡住的时候通常不是参数没调够，**是结构不对**。」
>
> **「抬 2Y 最有效的一招：把『水平』和『变化』两种视角叠起来」**
> `min(group_rank(X, sector), rank(ts_delta(X, 66)))`
> 「同族两腿的版本把我们的 **2Y 从 1.39 抬到 1.76**，Sharpe 也稳住了。」
>
> **反例**：「横截面核外面再裹一层 `ts_mean`」是**纯负收益**（Sharpe 0.94→0.23，margin 6.11bp→1.60bp），2Y 也没救回来。
>
> ⚠ **「2Y 不能拿『分年度最小 Sharpe』去预判」** —— 两者口径不一致。

### ★ 但本条配方在 KOR/fundamental44 上**不成立**（本轮实测，6/6 全负）

| 表达式 | alpha | S | 2Y |
|---|---|---|---|
| `min(group_rank(mscore, sector), rank(ts_delta(mscore, 66)))` | `A1QKKJ9Q` | **−0.35** | 0.24 |
| `min(group_rank(mscore, sector), rank(ts_delta(mscore, 252)))` | `rKdXX6Ya` | −0.24 | 0.28 |
| `multiply(group_rank(mscore, sector), rank(ts_delta(mscore, 66)))` | `JjPKK0wl` | −0.42 | −0.00 |
| `min(group_rank(wc_accruals, sector), rank(reverse(ts_delta(wc_accruals, 66))))` | `GrgJJ0ao` | −0.57 | −1.41 |
| `min(group_rank(yoon, sector), rank(reverse(ts_delta(yoon, 66))))` | `omoOOwpE` | −0.46 | −0.85 |
| `min(group_rank(mscore, sector), rank(reverse(ts_delta(mscore, 66))))` | `9qE00Pv2` | +0.06 | 0.53 |

**结论**：`min()` 是 AND 门（要求「水平排名高」**且**「变化排名高」同时成立）。
对 KOR `fnd44_mscore` 这种**单边恒正**字段，「水平」本身无区分度 ⇒ AND 门把样本过滤器杀空。
⇒ **再次印证项目铁律「结构最优性逐字段实测，不是普适规律」—— 移植结构前必须在该字段实测。**
⇒ 论坛配方的适用前提是「水平与变化都有效」的字段；本字段只满足「变化有效」。

---

## 四、★ 回测归因框架（DA98440 四类）

> 「当 Alpha 在某个时期出现异常收益（无论正负），厘清收益来源对于判断可靠性至关重要。」

### 4.1 因子暴露归因
时间序列回归：`R_alpha = α + β₁F₁ + β₂F₂ + … + ε`
- β 反映对各风险因子的平均暴露；**ε 是剔除已知因子后的纯 alpha 收益**
- **判据：若突出表现完全可被风险因子解释（α ≈ 0）⇒ 收益来自风险补偿，不是选股技能**

### 4.2 行业归因
按行业分解收益贡献（行业内权重 × 行业内收益，再求和）。
- **判据：收益高度集中在少数几个行业 ⇒ 信号可能只是捕捉行业轮动，不是选股能力**
- 检查行业贡献的**分散度**

### 4.3 市值分位归因
universe 按市值分 5/10 等分，算每分位收益贡献。
- **判据：收益主要来自最小或最大市值分位 ⇒ 结构性问题**（小市值流动性不足、大市值超额空间小）

### 4.4 时期归因
全样本按年份/市场阶段切分，分别算夏普与收益贡献。
- **判据：若约 70% 的正收益都来自某个单一年份 ⇒ 可靠性打折**

### 4.5 平台工具映射
| 归因 | 平台工具 | 本项目现状 |
|---|---|---|
| 时期归因 | **`get_alpha_yearly_stats`** | ✅ 已在用（2Y ladder 就是它的内置版）|
| 风险因子暴露 | **`performance_comparison`** | ⚠️ **本轮未用，应补** |
| 行业 / 市值分位 | 需导出 PnL 到外部工具分解 | ❌ 未做 |
| 滚动 β 估计 | 建议 **12 或 24 个月滚动窗口**反复估计（3 年静态 β 会失效）| ❌ 未做 |

**提交前最低要求（论坛原文）**：**至少完成「时期归因」+「大的风险因子暴露归因」**。

---

## 五、把归因落到本项目的具体动作

| 步 | 动作 | 工具 | 状态 |
|---|---|---|---|
| 1 | 时期归因（逐年 Sharpe） | `get_alpha_yearly_stats` | ✅ 已在用（判 2Y 就是此步）|
| 2 | 风险因子暴露归因（α 是否 ≈ 0） | `performance_comparison` | ⬜ **应补** |
| 3 | 行业贡献分散度 | 导出 PnL | ⬜ 未做 |
| 4 | 市值分位贡献 | 导出 PnL | ⬜ 未做 |
| 5 | 滚动 β（12/24 月窗） | 导出 PnL | ⬜ 未做 |

⚠ **注意口径陷阱（论坛实测）**：**2Y 与「分年度最小 Sharpe」口径不一致**，不能用后者预判前者。

---

## 六、一句话总结

1. **流程**：是「AI 出模板 → 回测」，但**体检数据已经把模板骨架定死了**，AI 只负责翻译成表达式，不负责发明。
2. **ATOM**：字段同数据集（你的数据集本来就满足）+ 免 IS Ladder，**但必须过 2Y** —— 2Y 是 ATOM 的**唯一真瓶颈**。
3. **归因**：四类（因子暴露 / 行业 / 市值分位 / 时期），提交前至少做**时期归因 + 风险因子暴露归因**；平台侧 `get_alpha_yearly_stats` + `performance_comparison`。
4. **论坛配方不可盲抄**：`min(group_rank, rank(ts_delta))` 在 KOR/fnd44 上 6/6 全负 —— 移植前必须逐字段实测。
---

## 七、★ 实战演示：对最佳候选 `omoMKXbJ`（S1.53）做时期归因

工具：`get_alpha_yearly_stats`。这是**归因四类里的第 ④ 类**，也是论坛要求的提交前最低两件之一。

| 年份 | PnL | 占比 | Sharpe |
|---|---|---|---|
| 2014 | 1,737,111 | 11.7% | 3.27 |
| 2015 | 1,269,775 | 8.5% | 1.28 |
| 2016 | 1,920,863 | 12.9% | 2.60 |
| 2017 | 779,525 | 5.2% | 1.11 |
| 2018 | 1,167,156 | 7.8% | 0.91 |
| 2019 | 2,741,649 | **18.4%**（最大）| 3.76 |
| 2020 | 946,188 | 6.3% | 0.80 |
| 2021 | 2,203,046 | 14.8% | 2.03 |
| 2022 | 2,040,651 | 13.7% | 2.24 |
| **2023** | **98,991** | **0.7%** | **0.08** ← 塌陷 |

### 判读（对照论坛四条判据）

| 判据 | 实测 | 结论 |
|---|---|---|
| 正收益是否集中于单一年份（>70% 则打折）| **最大单年占比 18.4%** | ✅ **健康**，无单年依赖 |
| 是否多年份都有正贡献 | **10/10 年全正** | ✅ **优秀**（论坛说的「理想情况」）|
| 是否近期衰减 | **2023 Sharpe 0.08、占比 0.7%** | ❌ **这是真问题** |
| 近 3 年均值 | (2.03+2.24+0.08)/3 = **1.45** | ⚠ 被 2023 拖累 |

### ★ 归因结论：这直接解释了 2Y 为什么是瓶颈
- **2Y = 0.97** 不是「参数没调够」，而是 **2023 年信号失效**（Sharpe 0.08）。
- 2Y ladder 窗口正好覆盖 2021–2023 ⇒ 被 2023 的塌陷拉低。
- 前 9 年（2014–2022）Sharpe 均值 ≈ 2.0，说明**信号本体是有效的，近端衰减是主因**。
- ⇒ 下一步的正确方向**不是**继续调 decay/window（那是调参数），而是找**能解释 2023 失效的结构** ——
  与论坛 XW76815 的判断一致：「**卡住的时候通常不是参数没调够，是结构不对**」。

### 归因四类在本候选上的完成度

| 归因类 | 工具 | 状态 | 结果 |
|---|---|---|---|
| ④ 时期归因 | `get_alpha_yearly_stats` | ✅ **本次完成** | 10/10 正年，2023 塌陷 |
| ① 因子暴露归因 | `performance_comparison` | ⚠️ 工具 6 次重试失败 | 待补 |
| ② 行业归因 | 导出 PnL | ⬜ 未做 | — |
| ③ 市值分位归因 | 导出 PnL | ⬜ 未做 | — |

⚠ **工具故障记录**：`performance_comparison` 对本 alpha 连续 6 次 `failed after 6 attempts` ⇒ 当前不可用，需换路径（导出 PnL 本地回归）。

---

## 八、★「加腿合规」终稿（2026-10-25 单变量 A/B 实测 + 官方原文复核）

### 8.1 一句话判据

**加腿合不合规，只看「非豁免字段的 dataset id 是否唯一」。**
不唯一 ⇒ 降级为 RA（必须过完整 IS Ladder，而不是只过 2Y）；
**但金字塔（塔）归属不变**——金字塔按 `category` 计，与 ATOM 的 `dataset id` 口径是两套并行标准（见本文 §2.1）。

### 8.2 三种加腿方式与后果

| 方式 | 合规性 | ATOM | 金字塔归属 | 真实代价 |
|---|---|---|---|---|
| **A 同数据集换字段/换机制** | ✅ 完全合规 | **保** | 保（`effective=1`） | 同集内部相关高（实测 0.65–0.76）⇒ prod 不降 |
| **B 用 6 个内置分组字段当杠杆** | ✅ 完全合规 | **保** | 保 | 只能改截面分组，不引入新信息通道 |
| **C 跨数据集加腿** | ✅ 合法（RA） | ❌ **丢** | **保（同类别时）** | 改判 RA ⇒ 须过完整 IS Ladder（2–5 年每年达标） |

6 个豁免字段（官方原文，恰好六个）：`country` / `exchange` / `market` / `sector` / `industry` / `subindustry`。
`inst_pnl()` / `convert()` 官方明列「视为使用 pv1」。

### 8.3 单变量 A/B（决定性证据）

对照组与处理组**只差一个算子**，其余完全一致（KOR / TOP600 / D1 / INDUSTRY / trunc 0.04 / 同壳）：

| | 表达式 | `failed_ra_checks` | `pyramids` |
|---|---|---|---|
| 对照 `P0Mb82xW` | `...vec_avg(anl16_actsuescore)...` | `LOW_SHARPE`, `LOW_FITNESS`, **`LOW_2Y_SHARPE`** | `effective=1` → **KOR/D1/ANALYST** |
| 处理 `ZYm91ARY` | 同上 **+ `vector_neut(..., rank(cap))`** | `LOW_SHARPE`, `LOW_FITNESS`, **`IS_LADDER_SHARPE`(year 2)** | **`effective=2`** → **KOR/D1/PV** + KOR/D1/ANALYST |

**三条结论：**
1. **本文 §二 第 56 行的推断得到实测坐实**：`vector_neut(x, rank(cap))` **不是「归一化」，而是 pv1 数据引用**。
2. 判据制式随之翻转：ATOM ⇒ `LOW_2Y_SHARPE`；RA ⇒ `IS_LADDER_SHARPE`。**这是判断 ATOM 身份唯一可靠的二元信号**。
3. `effective` 从 1 变 2，`pyramid_short` 从 `analyst` 变 `pv/analyst` ⇒ 混入 PV 类别。

⚠ **同时订正 `MEMORY.md` 中一条错误记录**：曾记「`vector_neut(x,rank(cap))` 仍 `effective=1`，平台把 bucket 当数据引用、vector_neut 当归一化」。该记录**与本文冲突，本文与实测为准**——vector_neut 同样破 ATOM。

### 8.4 同类别跨集：丢 ATOM，但保住金字塔（实测）

`6XAQJQWG` = analyst44 + analyst16（两个 dataset id，同属 ANALYST category）：
- `pyramids`: `effective=1`、`KOR/D1/ANALYST ×1.6` ⇒ **塔归属保住**
- `failed_ra_checks`: `IS_LADDER_SHARPE`(year 6, 1.49 vs 1.58) ⇒ **已降级 RA，须过完整阶梯**

⇒ **订正此前「跨数据集加腿点不亮塔」的结论。真正的死因是 IS Ladder，不是失去塔归属。**

### 8.5 跨类别加腿：官方与实测不一致（未解，按保守侧执行）

- **官方 Brain Genius**：「A consultant is considered to have formulated a pyramid if they have submitted a minimum of 3 Alphas in it. **A single Alpha can belong to multiple pyramids as it could have multiple data fields.**」
- **实测**：`RRAvGrn0`（`effective=2`，EUR MODEL+INSIDERS）提交后 **model 2→2、insiders 0→0**，两侧均未 +1。

⇒ **两方冲突，裁决：不依赖跨类别加腿去点塔。** 要加腿且要塔，只用**同类别跨数据集**（保 `effective=1`）。

### 8.6 「本集有无 size 代理」= 能不能合规做 size 中性化

`vector_neut(x, rank(cap))` 是公认的 2Y 杠杆（+0.50），但它破 ATOM。合规替代 = **用本数据集内的市值字段**。
论坛原文（KH94146）：「`vector_neut()` … 这些因素必须使用来自相同数据集的数据字段。如果你在分析师修正数据集（model26）中创建 Alpha，对于规模因子或市值，可以使用 `mdl26_market_cap_u`。」

| 数据集 | 本集市值/size 字段 | 结论 |
|---|---|---|
| **analyst44（KOR）** | `search="market cap"` **零命中** | 做 size 中性化只能引 pv1 ⇒ **与 ATOM 互斥** |
| model26 | `mdl26_market_cap_u` | 可合规做 |

⇒ **开集第一步就查**：`get_datafields(dataset_id=X, search="market cap")`；零命中则该集上不要用 size 中性化，改用 6 内置分组 + 换字段。

### 8.7 与降 prod 的关系（重要边界）

「合规加腿」解决的是 **能不能提交 / 能不能点塔**，**不解决 prod**：
- 同集加腿：A 0.807 + B 0.791 ⇒ 合成 **0.8953**（升）
- 跨集加腿：A 0.807 + SUE 0.780 ⇒ 合成 **0.8859**（升）
⇒ 两条合规路径都让 prod 变差。**不要指望用「合规的加腿」去降 prod。**

### 8.8 每次加腿后的复核清单（两行命令级）

1. `ra.failed_ra_checks` 里是 `LOW_2Y_SHARPE`（仍是 ATOM）还是 `IS_LADDER_SHARPE`（已降级 RA）？
2. `pyramids.effective` 是否仍为 1、`pyramids.list` 是否只含目标 category？

### 8.9 ★ 政策更新：ATOM 不可满足时放开 Regular，但**禁止加权混信号**（2026-10-25 用户明令）

**政策**：ATOM 实在不可满足时，放开挖掘 **Regular Alpha**（跨数据集/跨类别），但加腿必须合规。

**★ 硬禁止**：**「放开」不等于「放开加权」——永远禁止加权混信号。**
不许出现 `add(multiply(w1, rank(A)), multiply(w2, rank(B)))`、`scale(add(multiply(...), multiply(...)))` 这类「按人为权重把两条信号平均」的写法。
理由是加权混信号既无经济含义、又会把两条腿的拥挤暴露叠在一起（§8.7），且权重本身是最容易过拟合的自由度。

**唯一合法的三种非加权加腿形态：**

| 形态 | 写法 | B 的作用 | 是否改变分数 |
|---|---|---|---|
| **① 门控** | `trade_when(<B 的条件>, A, -1)` | 只决定**何时**交易 | 否，只筛时点 |
| **② 分组** | `group_neutralize(A, bucket(rank(B), range="0,1,0.25"))` | 只定义**分组** | 否，只改截面基准 |
| **③ 投影（正交化）** | `vector_neut(A, rank(B))` | 把 A 中与 B 共线的分量**剥掉** | 否，是减法不是加法 |

⇒ 若三种形态都做不出收益，**结论是不加这条腿**，不是退回加权。

### 8.10 ★ 正交性的数学边界（为什么「低相关」是错的口径）

**命题**：若两条腿 A、B 都与同一个生产 alpha P 相关（系数 cA、cB），则必有 `ρ(A,B) ≥ cA·cB`。
⇒ **正交性被拥挤度乘积锁死**：两条都拥挤的腿，无论怎么构造都不可能真正交。
实测印证：A（修正幅度）与 B（修正广度）ρ=0.7609，而 `cA·cB = 0.8073×0.7912 = 0.6387` —— 已经贴近下界。

**合成 prod（等权）= `(cA + cB) / √(2 + 2ρ)`。** 代入下界 ρ = cA·cB：

| cA | 求 cB 使合成 prod < 0.70 |
|---|---|
| 0.8073 | **cB ≲ 0.29** |
| 0.60 | cB ≲ 0.47 |

⇒ **真正决定成败的是新腿自身的 prod（cB），不是它与主腿的相关性。**
`ρ` 是 cB 的函数、是结果不是原因；盯着「找个不相关的腿」会一直在拥挤池里打转。

**实证对照（同一条主腿 A，cA=0.8073）：**

| 新腿 | 自身 cB | ρ(A,B) | 合成 prod | 判定 |
|---|---:|---:|---:|---|
| 修正广度（同集） | 0.7912 | 0.7609 | **0.8953** | ❌ |
| analyst16 SUE | 0.7796 | 0.6515 | **0.8859** | ❌ |
| **shrt38 做空买卖比** | **0.4365–0.6002** | 待测 | 预期 ~0.65–0.72 | ⭕ 唯一有希望的腿 |

⇒ **KOR 的低 prod 家族已定位：`shrt38_stk_invactsell_amt / shrt38_stk_invactbuy_amt`（S 1.71–2.57 / F 1.19–2.09 / 2Y 1.89–2.37 / prod 0.4365–0.6002）**，来自反向检索本地库 53 条 KOR prod 记录（min 0.4365 / median 0.6873）。

### 8.11 ★ 首个「非加权加腿」全闸通过样本（2026-10-25，KOR）

**成品 `leMPe8vA`（`failed_ra_count=0` / `all_passed=true`）：**
```
hump(group_rank(group_neutralize(divide(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt)),
                                 bucket(rank(vec_avg(eps_estimate_4wk_change)), range="0,1,0.25")),
                industry), hump=0.003)
```
设置：KOR / TOP600 / D1 / `decay=30` / `trunc=0.02` / `SLOW_AND_FAST` / `maxTrade=OFF`
读数：**S 2.04｜F 1.60｜2Y 1.76（ladder 爬到 year 7 通过）｜TO 0.1531｜sub 1.53｜invest 1.88｜DD 5.0%**
**prod 0.6054（过）｜self 0.3197（过）｜`effective=2` → KOR/D1/SHORTINTEREST + KOR/D1/ANALYST**

**形态 = ② 分组**（B 只提供 `bucket` 分组，A 仍是分数）——**零加权**，符合 §8.9 硬规。

#### 三形态横向对照（同一主腿、同一设置）

| 形态 | 写法 | S | F | 2Y | 结论 |
|---|---|---:|---:|---:|---|
| **① 门控 0.5** | `trade_when(less(rank(eps_rev),0.5), <A>, -1)` | **0.83** | 0.48 | 0.78 | ❌ **把信号切碎** |
| **① 门控 0.3** | 同上收紧到 0.3 | **0.63** | 0.30 | 0.48 | ❌ 更严更差 |
| **② 分组** | `group_neutralize(<A>, bucket(rank(eps_rev),0.25))` | **2.07** | 1.64 | 1.57 | ⭕ 保住 S |
| ② 分组 3 档 | `range="0,1,0.3333"` | 2.07 | 1.65 | 1.55(y3) | ⭕ |
| ② 分组 5 档 | `range="0,1,0.2"` | 2.05 | 1.62 | 1.45 | ❌ 档多反而差 |
| **② 分组 4 档 + industry** | 外层由 sector 换 industry | **2.04** | 1.60 | **1.76** | ✅ **全闸通过** |

⇒ **形态排序：② 分组 ≫ ① 门控（门控=负贡献，S 掉 1.7–1.9）**。
原因：门控只改「何时交易」，会把截面切碎、持仓宽度崩塌；分组只改「截面基准」，持仓宽度与信号强度都保住。

#### 补那 0.01 的两个真实杠杆

| 杠杆 | 变化 | Δ2Y |
|---|---|---:|
| **外层 `group_rank` 分组轴** `sector → industry` | 1.57 → **1.76** | **+0.19** ⭐ 决定性 |
| `decay` 20 / 30 / 40 | 1.55 / 1.57 / 1.52 | **单峰，30 最优** |
| `bucket` 档数 3/4/5 | 1.55 / 1.57 / 1.45 | **4 档最优**（再次印证「4 档 > 5/7/40 档」） |

#### ⚠ 必须诚实说明的反向结论：这条腿是**负贡献**

| | S | F | 2Y | prod |
|---|---:|---:|---:|---:|
| 纯 shrt38（`KPNo2lgl`，无腿） | **2.57** | **2.09** | **2.18** | **0.5504** |
| 加 analyst 分组腿（`leMPe8vA`） | 2.04 | 1.60 | 1.76 | 0.6054 |

**加腿在四项指标上全部变差。** ⇒ **判据：原信号已能全闸通过时，不要加腿。**
加腿只在「原信号卡在某闸、且该闸恰好能被分组改善」时才有意义；本次唯一换到的东西是 **ANALYST 类别归属**（`effective` 由 1 变 2），而这一点能否换来塔的计数，仍未证实（§8.5）。

### 8.12 ★ `leMPe8vA` 优化至极致 → 终选 `d5KJLqEw`（2026-10-25）

按 skill `wq-alpha-gate-push-op-min` 六步走。基线审计：**9 调用点 / 全闸 PASS / 无自动可压缩点** ⇒ 空间在扩余量。

**终选表达式（9 调用点，零加权，分组形态）：**
```
hump(group_rank(group_neutralize(divide(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt)),
                                 bucket(rank(vec_avg(eps_estimate_4wk_change)), range="0,1,0.25")),
                subindustry), hump=0.003)
```
设置：KOR / TOP600 / D1 / **decay=18** / trunc=0.02 / SLOW_AND_FAST / maxTrade=OFF

| S | F | 2Y | ladder窗 | TO | sub | invest | **prod** | **self** | DD |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1.87 | 1.28 | **2.24** | **2** | 0.1717 | 1.49 | 1.74 | **0.5629** | **0.3053** | 5.2% |

`failed_ra_count = 0`、`all_passed = true`、`effective=2`（SHORTINTEREST + ANALYST）

#### 相对基线的净变化

| | S | F | 2Y | ladder窗 | prod | self | 最小余量 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `leMPe8vA` | 2.04 | 1.60 | 1.76 | 7 | 0.6054 | 0.3197 | **0.095** |
| `d5KJLqEw` | 1.87 | 1.28 | 2.24 | **2** | 0.5629 | 0.3053 | **0.28** |
| Δ | −0.17 | −0.32 | **+0.48** | 7→2 | **−0.043** | −0.014 | **+0.185** |

**最小余量 0.095 → 0.28（+195%）**，代价是 S/F 各降 0.17/0.32（仍在安全区）。

#### 三条可迁移结论

1. **外层分组轴是本族最强的 2Y 杠杆**：`sector → industry → subindustry` ⇒ 2Y **1.57 → 1.76 → 2.24**（+0.67），S 单调 **2.07 → 2.04 → 1.87**。远强于 decay（同轴 decay 18→35 只摆动 0.28）。
2. **删算子必须分轴验证**：`hump` 在 **subindustry 轴上是承重件**（删后 2Y 2.20→**1.53** 直接 FAIL，`mLYnpQeK`）；在 **industry 轴上不是**（删后仅 −0.09 S，`2rjV10pZ` 8 算子仍全闸通过）。⇒ **"省 1 个算子"的可行性依分组轴而变。**
3. **「ladder 通过窗口数」是稳健性判据**：`window=2` = 最近两年即达标（强）；`window=7` = 前几个窗口都没过、靠拉长才勉强过（脆）。同族里 S 更高（2.12）的 `E5VnZQ6G` 是 window 7，S 更低（1.87）的 `d5KJLqEw` 是 **window 2** ⇒ **选 window 小的那颗**。

#### 备选（若要 S/F 优先）
`E5VnZQ6G`（industry / decay 18）：S **2.12** / F **1.55** / 2Y 1.84（window 7）/ sub **1.59** / invest **1.95** / prod 0.5942 / self 0.3062 —— 指标更漂亮，但 ladder 是勉强过，最小余量仅 0.106。

**处置**：`leMPe8vA` 及 10 条中间变体全部 **SUPERSEDED**，最终保留 `d5KJLqEw`。
