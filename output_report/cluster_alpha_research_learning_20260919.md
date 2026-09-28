# 《Cluster Alpha Research》学习笔记（论坛帖 43562853669655）

> 来源：WorldQuant BRAIN 官方社区，作者 **KJ42842**，2026-09-17 发布，**108 赞 / 0 评论**，正文 ~21.9k 字符，引用 **14 篇学术论文**。
> 已存入本地语料：`Claude/skills/brain-alpha-judge/data/forum_corpus/post_43562853669655.md`（index.json 21 篇）。

## 0. 一句话

BRAIN 的 **Cluster Test** 是"把你的 alpha 塌缩成**每个行业一个净头寸**后，这个行业账本本身够不够好"的**分类徽章**（不阻断提交）。文章给出：判定心法、构建法则（哪些算子建房、哪些是反 cluster）、**8 类可落地想法**（每类都锚定可引用论文）、以及评估循环与坑。

## 1. Cluster Alpha 是什么

BRAIN 在**两个层面**静默评估 alpha：

| 层面 | 含义 |
|---|---|
| 股票层面 | 常规视角：每只股票的权重 → PnL 的 Sharpe |
| **Cluster 层面** | 把 alpha 的暴露**按 cluster（一组相关标的）聚合**，测这个聚合账本的 **Cluster Sharpe** |

若 Cluster Sharpe 过线 → 打上 **Cluster Alpha** 徽章。

| 项 | 值 |
|---|---|
| 测试名 | Cluster Test Sharpe（`CLUSTER_TEST`）|
| 默认门槛 | **≥ 1.58** |
| 区域例外 | **KOR / JPS / TWN / HKG / IND / GBR / DEU → ≥ 1.0** |
| 性质 | **仅分类**：永不阻断提交、不影响其他测试；可与其他徽章并存 |

**心法**：把持仓塌缩成"每个 cluster 一个净头寸"，然后问——**如果我只能按行业下注，这个策略还赚钱吗？**
文章给了个关键标尺：把典型分散化股票账本塌缩到 cluster 层，主要区域的 Sharpe 大致落在 **1.0–1.5**。所以在 1.0 门槛区，"行业偏斜型"的 alpha **可能顺带**过线；在 1.58 门槛区，**必须刻意设计** cluster 层技法。

## 2. 构建法则（本文最硬的部分）

### 2.1 两步式：建房 + 打分

```
rank(group_mean(signal, cap, industry))
```
- `group_mean(x, weight, industry)` = **聚合 + 广播**：行业内每只股票都拿到该行业的（加权）平均值 → **这一步"造出"行业级信号**
- `rank(...)` / `zscore(...)` **市场级**（**不是** group 算子）= **跨行业打分** → 强的行业多、弱的行业空

### 2.2 关键区分：组内 vs 跨组

| 操作类 | 例子 | 对行业维度的效果 |
|---|---|---|
| 聚合+广播 | `group_mean(x, weight, industry)` | **Cluster 建房** |
| 跨行业打分（市场级） | `rank` / `zscore` / `scale` | **Cluster 建房**（强行业多、弱行业空）|
| **组内算子** | `group_zscore` / `group_rank` / `group_scale` | **不是 Cluster**（这是"行业内选股"，另一套概念）|
| 组均值剔除 | `group_neutralize(x, industry)` | **反 cluster**（直接删掉跨行业信息）|

推论（重要）：
- **广播之后再 `group_rank`/`group_zscore` 是退化的**——同行业成员数值完全相同，组内再排序等于空操作或噪声。
- 裸广播 + `rank` 会让行业仓位按成员数放大；广播后加 **`group_normalize(signal, industry)`** 可让 200 只股票和 15 只股票的行业贡献相同 gross。
- 配角：`group_count`（防薄行业）、`group_backfill`（聚合前补稀疏数据）、`group_sum`/`group_median`（替代聚合）。

### 2.3 中性化 = 总开关

| 设置 | 后果 |
|---|---|
| **Industry / Subindustry 中性化** | **按构造删掉行业结构** → 行业层聚合近似为零 → 想要 Cluster 就别用 |
| **Market（或无）中性化** | 行业偏斜能存活到聚合账本 |

**先决定你在做"行业技法"还是"行业内选股技法"——两者接近对立。**

## 3. 两大方法论

### 3.1 行业轮动（横截面）
信号 = 每个时点**行业强度的离散度**；强的多、弱的空。
```
industry_mom = group_mean(ts_delta(close, 126), cap, industry);
rank(industry_mom)
```
设计规则：形成期 **6–12 个月**、持有 **1–6 个月**（文献口径）；聚合权重用 `cap`（规模感知）或等权（纯宽度，**等权约把效应翻倍**）；用 `group_count(x, industry) > 5` 防薄行业。

### 3.2 行业择时（时序）
信号 = 每个行业的**时序状态**（何时该多/空/空仓）。
```
industry_ret = group_mean(returns, cap, industry);
signal = ts_mean(industry_ret, 20);
rank(signal)
```
可用原料：趋势/regime（`ts_mean`/`ts_delta`，文献版 = 12 个月回看 + 符号 + 逆波动率缩放）、异常态（`ts_zscore`）、**风险开关**（`trade_when` 在 panic 态外才表达）。

### 3.3 轮动 × 择时（通常最强）
```
rank(group_mean(ts_delta(close, 126), cap, industry)) * (ts_mean(industry_ret, 20) > 0)
```
差别：纯轮动对行业永远美元中性；择时允许行业账本随时间产生净方向（换手需更小心）。

## 4. 想法库（8 类，均锚定论文）

| # | 类别 | BRAIN 构造 | 文献锚点与关键数字 |
|---|---|---|---|
| 5.1 | **行业动量**（经典 cluster 效应）| `rank(group_mean(ts_delta(close, 126), cap, industry))` | Moskowitz & Grinblatt (1999)：**0.43%/月**（市值加权）→ **0.81%/月**（行业等权）；**多头驱动**（赢家-中位 0.36%/月 vs 中位-输家 0.07%/月）；跳过一个月稳健。反例注记：Grundy & Martin (2001) 行业调整后动量更好；Arnott 等 (2023) 因子动量**包含**行业动量 |
| 5.2 | **不要做的**：短期行业反转 | —（`rank(-group_mean(returns, cap, industry))` 月频负期望）| Da, Liu & Schaumburg (2014)：1 个月反转里**跨行业分量平均为负**（因行业有动量），钱全在**行业内**分量——而行业内正是 cluster 要聚合掉的维度 |
| 5.3 | **行业择时**：趋势 + 波动缩放 + 崩盘态 | `trend=ts_mean(industry_ret,250); vol=ts_std_dev(industry_ret,60); rank(trend/vol)`；panic 门控 `trade_when(!panic, rotation, -1)` | Moskowitz, Ooi & Pedersen (2012)：divTSMOM 账本 **Sharpe > 1**，**波动缩放是结果的一部分**；Daniel & Moskowitz (2016)：状态条件化**约翻倍**动量 Sharpe（panic = 2 年回看 < 0 且 60 日波动 > 其 250 日均值）|
| 5.4 | **扩散/关联行业**（最具特色）| 用**相关行业**（供应链上下游）的过去收益排序，而非自身 | Menzly & Ozbas (2010)：信息沿供应链扩散；Cohen & Frazzini (2008)：客户→供应商 1–2 月 **>150bps/月**；Hong 等 (2007)：部分行业领先大盘最多 **2 个月**；Hou (2007)：行业内**龙头→跟随者**扩散驱动行业动量 |
| 5.5 | **宏观驱动轮动**（古典式）| 用 regime 哑变量/连续倾斜乘在行业账本上（周期 vs 防御按字段画像分类）| Conover 等 (2008)：货币条件预测周期/防御价差；Polk 等 (2020)：景气 regime 轮动 **IR ≈ 静态的 2 倍**；arXiv 2304.09947：行业收益比个股**更可预测更稳定** |
| 5.6 | **行业聚合信息面** | `rank(group_mean(基本面增长字段, cap, industry))`；分析师**修正广度**（上行修正占比）| 情绪是**诚实的零假设**：Molchanov & Stangl (2018) 发现情绪影响行业是**全市场性**的、横截面上区分度差 → 别指望行业情绪离散度当轮动信号。`group_mean` 的均值在这里真干活：剔单股噪声、留行业信息 |
| 5.7 | **把已有 alpha 行业化** | `clusterized = group_mean(your_signal, cap, industry); rank(clusterized)` | 预期 Sharpe **下降**（有效注数几十 vs 几千）但**相关性也降**；研究实践：行业化账本与原件的相关约 **0.5** = 健康区（真行业结构，非克隆）。改良：过滤"成员意见分歧大"的行业；成员数悬殊时用 `group_normalize` |
| 5.8 | **cluster-aware 选股**（1.0 门槛区顺带拿徽章）| 保留选股逻辑，但让 PnL 聚合得好：机制本身在行业层运作、**不要**行业中性化、避开特异事件 | 自检：`group_mean(signal, cap, industry)` 聚合后仍有横截面离散度与经济含义 → 兼容 cluster。KOR/JPS/TWN/HKG/IND/GBR/DEU（1.0 门槛）常无需专门工程即可过 |

## 5. 评估循环与坑

**循环**：构建 → 查常规提交指标（**什么都没放宽**）→ **自检行业层**（把 alpha 聚合到行业，自己算行业账本 Sharpe，或用 `rank(group_mean(your_signal, cap, industry))` 当独立 alpha 代理）→ 对比 1.0/1.58 → 查行业账本 vs 原件/其他提交的相关性（self-corr < 0.7 仍适用）。

**坑**：
1. **过拟合是首要风险**：行业账本有效注数只有几十（≈行业数），不是几千 → 优先行业级经济机制，别调回看窗口。**内部项目历史：cluster 账本 in-sample ~1.3 → out-sample ~0.7** → 要建在门槛之上留余量。
2. **薄行业是噪声**：永远用 `group_count` 兜。
3. **中性化错配**：对轮动/择时想法做行业中性化 = 自毁（见 §2.3）。
4. **择时换手**：`trade_when`/趋势条件容易抬高换手 → 先 `ts_decay_linear` 平滑行业聚合量再门控。
5. **别为徽章牺牲真闸**：只有当行业结构**同时是经济想法**时才做。
6. **区域影响两次**：门槛（1.0 vs 1.58）**和**行业字段粒度（各区域不同，典型 ~70 个行业）。

## 6. 对本仓（wqb）的直接影响 —— 实测

用本仓工具链做了一次只读核验（MCP venv + 平台 API）：

### 6.1 ★ 徽章取错了字段（可修）

- **`CLUSTER:CLUSTER`（name "Cluster Alpha"）存在于 `classifications` 数组**，**不在 `checks`**：
  实测 alpha 详情顶层键含 `classifications`（样例：`[{"id":"REGULAR:REGULAR",...},{"id":"CLUSTER:CLUSTER","name":"Cluster Alpha"}]`），而 `checks` 键在详情里根本不出现。
- 本仓 `tools/harvest_multisim.py:238` 却是 `cluster_test = _extract_check_value(checks, "CLUSTER_TEST")` → **取错字段** → 库内 `alphas.cluster_test` **0 / 4,918 行**。
- 对照：仓库在别处（`brain_mixin_correlation.py` 识别 Power Pool、`brain_mixin_spcread.py` 识别 SINGLE_DATA_SET）**已经**在读 `classifications` —— 这条链路是漏的。
- 附带发现：`classifications` 里还有 `POWER_POOL:POWER_POOL_ELIGIBLE`、`DATA_USAGE:SINGLE_DATA_SET` 等族，本仓同样未系统采集。

### 6.2 ★ 账号已有 26 颗 Cluster Alpha，此前不可见

抽样 24 条 ACTIVE alpha → **26 条命中 `CLUSTER:CLUSTER`**（样本含复检），分布：**IND 为主**，另有 **DEU / HKG / USA / KOR**。例：`DEU/blRnKEk6`、`HKG/gJQZOXrg`、`USA/xAdL5vmN`（同时带 `POWER_POOL_ELIGIBLE`）、`KOR/O0Gj6PqJ`。

含义：你已经在**无意识**的情况下产出了 cluster 合规的 alpha（多为 1.0 门槛区），但自己的库与分析完全看不到——与之前 `source` / `prod_corr` 的"链路未接线"是同一类问题。

### 6.3 与本仓现有 SOP 的张力（重要）

- 本仓 SOP 放行的**5 类结构交互**含 `group_zscore` / `group_rank` —— 本文明确把它俩归为 **"Not Cluster Alpha"**（行业内选股）。**要拿徽章，必须改用 `rank(group_mean(x, cap, industry))` 两段式。**
- 本仓按区域择优**中性化**（如 EUR `REVERSION_AND_MOMENTUM`、GBR `INDUSTRY`）——`INDUSTRY`/`SUBINDUSTRY` 属本文所说的**反 cluster** 设置。**想拿徽章须换 MARKET 或无中性化**。
- 例：`industry_mom = group_mean(ts_delta(close, 126), cap, industry); rank(industry_mom)` —— 形态是"算子几何"，**不违反**你的"禁加权混合"铁律（无系数腿、无 add 加权）。

### 6.4 建议（按 ROI，均待你确认）

| 序 | 动作 | 价值 | 风险 |
|---|---|---|---|
| ① | 把 `cluster_test` 采集源从 `checks` 改为 `classifications`（或新增 `classifications` 列存全族徽章）| 解锁 26 颗已有资产的可见性；与 prod_corr/self_corr 同一类修复 | 低（但需定 schema：徽章是布尔/文本，不是 DECIMAL） |
| ② | 对 **1.0 门槛区（IND/DEU/GBR/KOR/HKG）** 加一条 cluster 变体线：`rank(group_mean(信号, cap, industry))`，非行业中性化 | 顺带拿徽章 = 纯增益；IND 已证明可行（26 颗里多数是 IND）| 中（新增生成线，需闸门放行 `group_mean` 组合形态） |
| ③ | 若走 1.58 门槛区（USA/EUR 等），按 §5.1/5.3 刻意建行业技法，并留 in-sample→out-sample 衰减余量（~1.3→0.7）| 高价值但难度高 | 高（过拟合风险） |

## 7. 结论

这是一篇**把"行业层 alpha"系统化**的方法论文：核心就一句——**用 `group_mean` 把信号抬到行业层，用市场级 `rank` 跨行业打分，别用行业中性化**；再往上叠 8 类经过文献验证的机制。它同时泄露了一个容易被忽视的事实：**Cluster Test 只是分类徽章**，所以正确的做法不是"为徽章而挖"，而是**让行业结构本身就是经济想法**——那样徽章是副产品。
