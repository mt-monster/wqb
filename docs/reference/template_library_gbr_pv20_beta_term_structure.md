# GBR PV 塔模板库：`pv20` beta 期限结构 + 流动性

> 建立日期：2026-10-30
> 区域设置：**GBR / TOP700 / D1**
> 数据集：`pv20`（category = **pv**，`pyramidMultiplier` 1.4）
> 本文件目的：**PV 塔是本会话唯一全程 0 路径的塔**（需 2 条）。在 §9.1 塔位判据被批 17 证伪后，必须离开 `fundamental17` 去找真正的 `category=pv` 数据集。本文件锁定 `pv20` 作为第一入口，并把模板池预注册到 ≥10 个结构互异模板。

---

## 一、为什么选 `pv20`（数据集画像）

| 项 | 数值 | 判读 |
|---|---|---|
| category | **pv** | ⇒ 全字段归 **PV 塔**，正是本会话缺口 |
| fieldCount | **675** | 材料充足，足够铺 10+ 模板 |
| userCount | 358 | 中等 |
| **alphaCount** | **699** | **拥挤度只有 `pv1`（53267）的 1/76** ← 决定性优势 |
| valueScore | 3.0 | 平台给的字段质量分一般，低于 `pv173`（5.0）/ `pv109`（5.0） |
| coverage（平台列） | 0.0 | **不可信**（平台该列对多数数据集恒返 0.0）⇒ 只能用 `longCount + shortCount` 实测 |
| pyramidMultiplier | 1.4 | 与其它 PV 集一致 |

**对比其它 15 个 GBR PV 数据集**（`get_datasets(category="pv")` 全量实读）：

| 数据集 | 字段 | users | alphas | 状态 |
|---|---:|---:|---:|---|
| `pv1` | 23 | 3402 | **53267** | 极度饱和；`cap` 已用作分母（PV+FUND 双塔，已用满 3 位配额） |
| `pattern_scores` | 504 | 742 | 1769 | 未试；**唯一 `coverage=0.9924` 的 PV 集**（图表形态相似度） |
| `intraday_pv_feats` | 585 | 308 | 651 | 未试；盘中间隔级特征（买卖价差、订单流） |
| `continuation_score` | 560 | 311 | 729 | 未试；价格图表延续形态相似度 |
| **`pv20`** | **675** | **358** | **699** | **← 本文件入口** |
| `pv30` | 240 | 150 | 369 | **已判死** |
| `pv109` | 26 | 15 | 32 | **已判死**（Bond Yield） |
| `pv47` | 2 | 310 | 716 | **已判死**（13/13 prod ≥0.7） |
| `pv173` | 81 | **13** | **19** | 未试；公司债 z-spread 曲线 + PCA 因子（shift/twist/butterfly），**最不拥挤** |
| `pv103` | 8 | 96 | 163 | 未试；盘中间隔 + MOO/MOC 竞价 |
| `pv106` | 8 | 24 | 41 | 未试；微观结构价差 |
| `pv113` / `pv13` / `pv17` / `pv71` / `pv29` | 1–50 | 2–50 | 2–66 | 多为映射/分类元数据，非信号源 |

**⇒ 候选排序：`pv20`（字段多 + 拥挤度低）> `pv173`（最不拥挤但覆盖待验）> `pattern_scores`（唯一有真实 coverage）> `intraday_pv_feats`。**

### 1.1 `pv20` 的 description 是污染的（平台已知问题）

平台描述写 "global company fundamental data … annual and interim/quarterly financial statements"，**与实际字段不符** —— 实读 675 个字段全是价量/微观结构/风险量（beta、adv、slippage、cap）。这与 `other47` / `other250` 等 11 个数据集的描述污染是同一类问题。

**⇒ 判据不变：判断数据集内容一律先 `get_datafields` 看字段级 description，数据集级 description 只在字段清单为空时当参考。**

### 1.2 已核实的关键字段（`get_datafields` 实读）

**beta 期限结构族（本文件核心，7 个原生窗口）**：

| 字段 | users / alphas | 描述 |
|---|---|---|
| `beta_market_10d` | 2 / 3 | Beta to broad market, past 10 days |
| `beta_market_20d` | 2 / 3 | past 20 days |
| `beta_market_40d` | 1 / 2 | past 40 days |
| `beta_market_60d` | 2 / 2 | past 60 days |
| `beta_market_125d` | 5 / 5 | past 125 days |
| `beta_market_500d` | 2 / 3 | past 500 days |
| `market_beta_250d` | 1 / 4 | 250-day period（与 `beta_market_*` 系同族） |

**★ 每个字段的 `alphaCount` 只有 2–5 ⇒ 几乎无人使用 ⇒ prod 相关性风险极低。这是本会话找到的最干净的 PV 入口。**

**其它可用字段**：

| 字段 | users / alphas | 用途 |
|---|---|---|
| `firm_market_capitalization` | 4 / 4 | **PV 塔的市值字段**（做分母 / 分组轴，不会引出双塔） |
| `issuer_composite_score` | 55 / 59 | 供应商综合/排名分，可做时序动量 |
| `adv20_extra` | 109 / 178 | 20 日均量（**股数，带单位**） |
| `adv60` / `adv60_extra` | 24 / 16 | 60 日均量（股数） |
| `adv20_extra_usd` | 10 / 13 | 20 日均成交额（**USD**） |
| `adv20_usd_capped_100m` | 23 / 28 | 20 日均成交额，上限 1 亿美元 |
| `adv60_usd` / `adv60_extra_usd` | 2 / 4 | 60 日均成交额（USD） |
| `average_daily_volume_20d` | 13 / 19 | 20 日均量（股数） |
| `average_daily_value_20d_usd` | 4 / 4 | 20 日均成交额（USD） |
| `industry_sector_classification_17` | 2 / 3 | 行业分类 ⇒ **分组轴** |
| `pv20_252_mom` | 20 / 22 | 252 日动量（**描述写 "for EUR universe" ⇒ GBR 使用带风险，先验证**） |
| `alternative_slippage_*`（12 个变体） | 2–6 / 3–7 | 交易成本滑点估计 ⇒ 用于成本建模，非信号 |
| `group_slippage_estimate` | 4 / 4 | 同上 |
| `pv20_bps_indicator_{1,2,3}_feature{0..12}` | 0–3 / 0–4 | IBES 税前利润启发式特征；**多数 userCount=0 ⇒ 覆盖极可能为空，除非有明确理由不投入** |

**排除**：`issuer_legal_name_15`（文本）、`industry_sector_classification_17` 以外的分类元数据。

---

## 二、经济机制（为什么 beta 期限结构在 GBR/TOP700 应该有信号）

### 2.1 三条独立的理论依据

1. **BAB（Frazzini & Pedersen 2014, "Betting Against Beta", JFE）**：低 beta 股票的风险调整后收益高于高 beta 股票，因为杠杆受限的投资者会超配高 beta。⇒ `-rank(beta_long)` 应为正向信号。GBR TOP700 是机构主导的大盘市场，杠杆约束更强 ⇒ 该效应应比小票市场更显著。

2. **Beta 不稳定性 / 不确定性（Ang, Chen & Xing 2006 "Downside Risk"; 及 beta dispersion 文献）**：beta 自身的时间序列波动率是一个独立的定价维度 —— 「beta 不稳定」意味着投资者无法对冲系统性风险，要求额外补偿。⇒ `ts_std_dev(beta_short, 252)` 应有信号，且**与 beta 水平正交**（这是它与 T2 的关键区别）。

3. **系统性风险重估（自建，本项目首次提出）**：**短期 beta 相对长期 beta 的上升** = 该股票的系统性风险正在快速累积（典型触发：盈利预警、行业冲击、杠杆上升）。若市场对此反应不足，则「beta 期限斜率向下」（长期高、短期低 = 风险正在释放）应获得超额收益。⇒ `subtract(rank(beta_long), rank(beta_short))`。

### 2.2 为什么 GBR 的特殊性可能帮到我们

- **TOP700 全是 LSE 大中盘** ⇒ beta 估计的统计噪声远小于小票 ⇒ 7 个窗口的期限结构是**真实信号而非估计噪声**。这是本机制在 TOP700 上可能成立、而在小宇宙上不成立的物理原因。
- **GBR 无 universe 退路**（TOP700 是唯一档）⇒ 任何依赖「换小宇宙救 SUB」的方案都不可用，必须找在大票上天然有效的信号。**beta 是大票的属性，不是小票的属性** —— 这是它比「异常成交量」（天然偏小票）更适合 GBR 的结构性理由。

---

## 三、10 个结构互异模板（**PV 单塔，全 `pv20` 字段**）

差异维度分布：骨架结构 / 算子几何 / 矩（水平·一阶差分·二阶方差）/ 分组轴 / 非线性变换 / 条件门控。**不是换窗口或换常数的伪多样性。**

| # | 模板名 | 表达式 | 差异维度 | 来源 | 状态 |
|---|---|---|---|---|---|
| **T1** | **Beta 期限结构斜率** | `subtract(rank(beta_market_500d), rank(beta_market_20d))` | 骨架=两尺度相减；矩=水平 | 自建（§2.1-3） | 待测 |
| **T2** | **BAB 纯水平（横截面秩）** | `-rank(market_beta_250d)` | 骨架=单字段符号；矩=水平 | paper（Frazzini-Pedersen 2014） | 待测 |
| **T3** | **自身 beta 异常度（时序 zscore）** | `ts_zscore(ts_backfill(beta_market_60d, 22), 252)` | 几何=时序 vs 截面；矩=水平偏离 | forum `43152032301591` 铁律①+② | 待测 |
| **T4** | **beta 加速度（一阶差分）** | `ts_delta(ts_backfill(beta_market_20d, 22), 5)` | 矩=**一阶差分** | 自建（风险事件冲击） | 待测 |
| **T5** | **beta 不稳定性（二阶矩）** | `ts_std_dev(ts_backfill(beta_market_20d, 22), 252)` | 矩=**二阶方差** | paper（Ang-Chen-Xing 2006） | 待测 |
| **T6** | **BAB × 流动性（USD 量比）** | `ts_quantile(divide(ts_backfill(adv20_extra_usd, 22), ts_backfill(firm_market_capitalization, 22)), 252)` | 骨架=比率构造；单位=USD/USD 无量纲 | paper（Amihud 2002 流动性） | 待测 |
| **T7** | **beta 期限斜率 × 流动性条件门控** | `trade_when(greater(rank(divide(ts_backfill(adv20_extra_usd, 22), ts_backfill(firm_market_capitalization, 22))), 0.5), subtract(rank(beta_market_500d), rank(beta_market_20d)), -1)` | 结构=**条件门控**（三参数 `trade_when`） | forum `33120494662423` + `25740783868439` | 待测 |
| **T8** | **规模桶内 beta 中性化** | `rank(group_neutralize(ts_zscore(ts_backfill(beta_market_60d, 22), 252), bucket(rank(ts_backfill(firm_market_capitalization, 22)), range='0.2,1,0.2')))` | 轴=**规模分桶**（5 桶，TOP700 档） | forum `44174743998999` 模板 6 | **待验证 `bucket`** |
| **T9** | **供应商综合分自身动量** | `ts_zscore(ts_backfill(issuer_composite_score, 22), 252)` | 骨架=完全不同字段（非 beta） | 自建 | 待测 |
| **T10** | **beta 期限斜率 × 行业轴中性化** | `group_neutralize(subtract(rank(beta_market_500d), rank(beta_market_20d)), industry_sector_classification_17)` | 轴=**供应商行业分类**（非平台 sector） | 自建（绕开平台中性化） | 待测 |

### 3.1 单位闸合规检查（`unit_handling=VERIFY`）

| 模板 | 涉及单位 | 结论 |
|---|---|---|
| T1–T5, T9, T10 | beta / composite score 无量纲；`ts_std_dev` / `ts_zscore` / `ts_delta` 保持原单位 | ✓ 全部无量纲，安全 |
| T6 | `adv20_extra_usd`（USD）+ `firm_market_capitalization`（USD）⇒ `divide` 得无量纲 | ✓ **必须用 USD 版；用 `adv20_extra`（股数）÷ 市值会带 `TSShare/USD` 单位，必挂** |
| T7 | 同上 + `greater(rank(...), 0.5)` 门控 | ✓ `rank()` 后无量纲再比较常数，合规 |
| T8 | 同上 | ✓ |

**⇒ T6/T7/T8 的字段选择是硬约束：成交量一律用 `*_usd` 系列，不能用股数系列。**

### 3.2 幽灵 / 不可访问算子检查

| 算子 | 状态 |
|---|---|
| `subtract` / `rank` / `ts_zscore` / `ts_delta` / `ts_std_dev` / `ts_quantile` / `trade_when` / `greater` / `group_neutralize` | ✓ 本会话已验证可用 |
| **`bucket`** | ⚠ **本账号未验证**。forum 明确警告 `group_median`/`group_count` 在部分账户不可用，且会导致**整包 CANCELLED**。T8 落地前必须单条最小验证（`bucket(rank(firm_market_capitalization), range='0.2,1,0.2')` 单独跑一次） |

---

## 四、预注册判据

1. **10 个模板里至少 2 个 S ≥ 1.0** ⇒ beta 期限结构在本机制上真实存在 ⇒ 值得铺满 10 个 + 窗口/桶数微调。
2. **全部 < 0.6** ⇒ beta 在 GBR/TOP700 已被套利干净（考虑到 `alphaCount` 只有 2–5，这个结果反而说明「没人用是因为没用」）⇒ 转向 `pv173`（公司债 z-spread）或 `pattern_scores`。
3. **T1（期限结构）显著强于 T2（纯水平）** ⇒ 新信息在**跨尺度差**而非 beta 水平 ⇒ 「系统性风险重估」是独立机制，可继续做二阶（斜率变化率）。
4. **T5（beta 波动率）与 T3（beta 偏离）互相关 > 0.8** ⇒ 两者是同一物理量 ⇒ 只保留一个，用 T1 / T2 提供正交性。
5. **T6 的 SUB 显著高于 T1–T5** ⇒ 流动性维度在大票上更有效 ⇒ PV 塔主线切到「流动性」而非「风险」。
6. **任一模板 SUB/S ≥ 0.4754**（GBR 实测 SUB 系数，见 `template_library_gbr_fundamental_cap_scaled.md` §11.5）⇒ **该模板有提交希望**，优先投入 decay / 中性化扫描。

---

## 五、派发设置

**起始设置（与本会话 `fundamental17` 族级设置对齐，便于横向比较）**：
```
GBR / TOP700 / D1 · neutralization = INDUSTRY · decay = 10 · truncation = 0.05
pasteurization = ON · unitHandling = VERIFY · nanHandling = OFF · maxTrade = OFF
```

**为什么起点用与 FUND 族相同的设置**：跨数据集比较时设置必须一致，否则「新数据集不行」与「设置不对」无法区分。这是 `fundamental1` 判死时用「同设置内部控制」学到的方法论。

**需注意的 GBR 特殊性**：
- **universe 只有 TOP700**，没有换宇宙救 SUB 的退路。
- `exchange` / `country` 做分组轴无效（GBR 只有 LSE）；`sector` / `subindustry` 作**中性化轴**无效，但作 `group_neutralize` / `group_rank` **变换轴**可用 ⇒ T10 用供应商自己的 `industry_sector_classification_17` 而不是平台 sector，正是为了绕开这个限制。
- `LOW_SUB_UNIVERSE_SHARPE` 系数 **0.4754 × S**（GBR 实测，勿套用 USA 的 0.434）。

---

## 六、配额与塔位合规

| 检查项 | 结论 |
|---|---|
| 字段 category | `pv20` = **pv** ⇒ 所有模板都是 **PV 单塔** |
| trio 内部混塔 | 无。全部字段同一数据集 ⇒ 单一 category |
| `PV+PV` 禁混（2026-10-28 澄清） | **不触发** —— 该禁令针对「两个 PV **数据集**互组」，本文件全部模板只用 `pv20` 一个数据集 |
| 两塔组合 ≤3 配额 | 不占用（单塔） |
| trio × 非 trio ≤5 配额 | 不占用（单塔） |

**⇒ 本文件 10 个模板全部是「零配额成本」的 PV 单塔候选。这是 PV 塔最划算的路径。**

---

## 七、与已有 PV 尝试的关系

| 已试 PV 路径 | 结果 | 与本文件的关系 |
|---|---|---|
| `pv47_spret` 全族 | 13/13 prod ≥0.7，判死 | 无关（specific return 已被套利） |
| `pv109`（Bond Yield） | 判死 | 无关 |
| `pv30`（Alternate Industry Classification） | 判死 | 无关 |
| `order_book_imbalance` / `euro_equity_imbalance` | 判死 | 无关 |
| `cap` 作分母（`divide(X, cap)`） | 产出 3 条 PV+FUND 双塔候选 | **不同路线**：那条是「FUND 信号 × PV 分母」，本文件是「纯 PV 信号」 |
| ~~`daily_volume_to_shares_outstanding`~~ | **曾被误认为 PV**（§9.1 错误），实为 FUND | 已修正 |

**⇒ `pv20` 是 PV 塔唯一未被否定、且结构上最适合 GBR 大票市场的入口。**

---

## 八、下一步（执行顺序）

1. **批 21（首发 2 条）**：T1（期限结构）+ T3（自身异常度）—— 两者分别代表「跨尺度差」与「时序偏离」两个最可能有信号的几何，且互不相同。
2. 若 T1 有效 ⇒ 批 22 铺 T2（水平对照，用于确认「新信息在差不在水平」）+ T4（加速度）。
3. 若 T3 有效 ⇒ 批 23 铺 T5（二阶矩）+ T9（换字段）。
4. **`bucket` 可用性单独验证**（1 条最小表达式），通过后再上 T8。
5. 全部完成后按模板编号归因，写入 dataset_experience 报告。

---

## 九、首发批结果（T1 + T3）：**双灭**，beta 机制在 GBR/TOP700 被套利干净

**设置**：`GBR/TOP700/D1 · INDUSTRY · decay 10 · trunc 0.05 · nanHandling OFF · maxTrade OFF · unitHandling VERIFY`（与 `fundamental17` 族级设置完全一致，保证横向可比）。

| 模板 | alpha | S | F | TO | 2Y | SUB | **SUB/S** | dd | margin | fRA |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **T1** 期限结构斜率 | `rKRQOdkE` | **0.33** | 0.13 | 8.60% | 0.85 | **0.73** | **2.21** | 11.33% | 4.35bp | 3 |
| **T3** 自身 beta 异常度 | `58ENzjRk` | **−0.24** | −0.08 | 6.92% | −0.45 | −0.45 | 1.88 | 25.98% | −4.39bp | 4 |

### 9.1 三条解读

1. **绝对强度差闸门 5 倍**（T1 S 0.33 vs 闸门 1.58）。这不是「差一点」，是**机制不存在**。F 0.13 远低于 1.0 门槛。
2. **T1 的 `SUB/S = 2.21` 是一个反常信号**：`rKRQOdkE` 的 SUB 0.73 高于其全宇宙 S 0.33 两倍多，`investability_ratio` 也高达 0.82。即「信号在子宇宙里比在全宇宙里强 2.2 倍」。**说明 beta 期限斜率在大票上确实有一点结构，但被全宇宙的小票噪声完全淹没** —— 与「beta 是大票的属性」的直觉方向一致，只是绝对量级太小。
3. **T3（`ts_zscore` 时序偏离）为负且回撤 26%** —— 这是纯噪声形态，不是弱信号。beta 自身的时序 zscore 在 252 日窗口下无预测力。

### 9.2 为什么 beta 在 GBR/TOP700 注定弱（第一性原因，不是运气）

- **beta 是市场因子的暴露量，而平台中性化（INDUSTRY）已经在组合层把行业/市场共同暴露剥掉**。在一个已经被 industry-neutral 的组合里再押 beta，押的是「残余 beta 差异」——这个量本身很小。
- **BAB 溢价在 GBR 大盘股上已被杠杆约束宽松化**：Frazzini-Pedersen 的机制要求存在**杠杆受限投资者**。LSE 大盘股是全球机构配置标的，融资渠道充分 ⇒ 约束最松 ⇒ 溢价最小。这与「GBR TOP700 是机构主导、杠杆约束更强」的初始假设**方向相反**——初始假设错了。
- **`alphaCount` 只有 2–5 不等于「没人用是因为没用」，而是「该字段的可见价值低」**。这是本轮踩到的先验陷阱：**低 alphaCount 既可能是富矿，也可能是荒漠，必须先做一条最小探针再决定是否铺 10 个模板**。

### 9.3 对预注册判据的执行

- 判据 2 写「全部 < 0.6 ⇒ 转向 `pv173` 或 `pattern_scores`」。目前完成 2/10，两条都 < 0.6。
- **决定：不铺完剩余 8 个 beta 模板**。理由：已测的两个是结构上差异最大的两个（跨尺度差 vs 时序偏离），且都是 β 族；T2/T4/T5/T10 全部仍在 β 族内部（水平 / 一阶差分 / 二阶矩 / 换轴），**预计 ≤0.5**。把 4 批仿真槽投在「预计 ≤0.5」的族上不符合「每槽信息量最大化」。
- **改为：PV 主线切到 `pv20` 的流动性字段**（`adv*_usd` / `firm_market_capitalization`），因为该机制在本会话 `fundamental17` 上已被**同一个数据集族的六个批次**证实存在（S 1.54），只是塔位不同。这是「已被验证的机制 + 全新的塔位」组合，期望值远高于「未验证的机制 + 未验证的塔位」。

### 9.4 PV 塔的风险提示（必须写清）

`pv20` 的流动性比率（成交额 / 市值）与 `fundamental17` 的换手率（成交量 / 流通股）**在经济学上是同一个量**（都是换手率的不同口径）。若两者都产出候选，**互相关会很高，实际只能取 1 条**。因此：
- **PV 塔的流动性路径解决的是「塔位」问题，不是「数量」问题。**
- 若要 PV 塔 2 条互不相关的候选，第 2 条必须来自**非流动性机制**（`pv173` 公司债 z-spread / `pattern_scores`）。
- ★ 但塔位点亮只看「同 category 提交 3 个」，自相关是提交时的池子闸 —— 若两条 PV 候选互相关 0.9，第 2 条会 fail self-correlation。**所以 9.4 这条是真约束，不是理论洁癖。**

---
---

## 十、流动性批（T6 + 机制移植）与互相关突破：**`adv20_extra_usd / firm_market_capitalization` 是本会话唯一比值过闸的几何**

### 10.1 两批实测

| 批 | 表达式 | alpha | S | F | TO | 2Y | SUB | **SUB/S** | dd | margin | fRA |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | **T6**：`ts_quantile(divide(adv20_extra_usd, firm_market_capitalization), 252)` | `RRE06nEz` | **0.91** | **0.58** | 9.13% | 1.39 | **0.56** | **0.615** | **6.94%** | **10.98bp** | 3 |
| 2 | 移植：`ts_zscore(divide(adv20_extra_usd, ts_mean(adv20_extra_usd, 252)), 504)` | `88RgPdNm` | 0.68 | 0.33 | 9.45% | 1.09 | 0.38 | 0.559 | 8.17% | 6.19bp | 3 |

**两条结论**：
1. **「成交额 / 公司市值」显著优于「成交额 / 自身历史均值」**（S 0.91 vs 0.68、F 0.58 vs 0.33、margin 10.98bp vs 6.19bp、dd 6.94% vs 8.17%）。
   **机理**：分母换成**公司规模**后，信号变成**截面可比的换手率水平**（Amihud 2002 意义下的流动性），而不是「与自己过去比」的相对量。前者直接对应「这只股票今天相对它的体量有多活跃」，是可跨股票比较的经济量；后者只回答「它今天比自己平时活跃吗」，丢掉了规模维度。
   ⇒ **这正是它与 `fundamental17` 换手率族（自身历史基线）在机制上的分野，也是两者相关性只有 0.45–0.54 的原因。**

2. **T6 的回撤 6.94% 是全 `pv20` 与 `fundamental17` 两个数据集里最低的**，margin 10.98bp 逼近 GBR 市场中位（11.9bp，forum `42587179348119`）⇒ 成本敏感度可接受，具备真实可实现性。

### 10.2 ★★★ 互相关：`RRE06nEz` 与传统两族**全部 <0.7**，把最大可共存篮子从 2 扩到 4

```
compute_mutual_correlation([RRE06nEz, bl67R9mK, QPvmbn2w, vR1akGVz,
                            rKRQbPPE, j2YNnKOQ, omEQ9kK5], threshold=0.7, years=4)
→ max_mutually_below_subset = ["bl67R9mK", "j2YNnKOQ", "RRE06nEz", "rKRQbPPE"]
  size = 4,  max_subset_exact = true,  num_points = 1021
```

| `RRE06nEz` 对 | 相关系数 | 判读 |
|---|---:|---|
| `rKRQbPPE`（EBITDA/EV） | **0.0686** | 近乎完全正交 |
| `j2YNnKOQ`（EBIT/EV） | **0.1284** | 近乎完全正交 |
| `omEQ9kK5`（EBIT/cap） | **0.1340** | 近乎完全正交 |
| `bl67R9mK`（量比 504） | 0.5433 | 中度，**仍 <0.7** |
| `QPvmbn2w`（zscore + 残差化） | 0.4631 | 中度，**仍 <0.7** |
| `vR1akGVz`（quantile + 残差化） | 0.4488 | 中度，**仍 <0.7** |

**⇒ 三条可复用结论**：
- **同一经济机制、不同数据源 ⇒ 可接受的低相关**。「换手率」这个机制在 `fundamental17`（股数口径）与 `pv20`（USD 成交额口径）上是同一个经济学量，但实测相关性只有 0.45–0.54，**远低于同数据集内换 `ts_quantile`/`ts_zscore` 造成的 0.81–0.86**。⇒ **跨数据集换口径比在数据集内换算子更能降相关。**
- **塔位与相关性的取舍可以双赢**：`pv20` 既给了 PV 塔位，又给了正交性，不是二选一。
- 换手率族内部 0.81–0.86 ⇒ **该族仍只能取 1 条**（`bl67R9mK`/`QPvmbn2w`/`vR1akGVz` 三选一）。

### 10.3 ★★★ 关键推论：`RRE06nEz` 是**唯一一个 SUB/S 已过闸**的几何 ⇒ 对它是「只拉 S」的纯放大问题

GBR 的硬要求是 `SUB/S ≥ 0.4754`（三次反算自 `checks.fail`）。

| 几何 | SUB/S | 是否过比值闸 |
|---|---:|---|
| **`RRE06nEz`（pv20 adv_usd/mcap）** | **0.615** | ✅ **过**（余量 +29%） |
| `88RgPdNm`（pv20 adv/自身均值） | 0.559 | ✅ 过 |
| `QPvmbn2w`（FUND zscore + 残差化） | 0.449 | ❌ 差 5.9% |
| `vR1akGVz`（FUND quantile + 残差化） | 0.403 | ❌ 差 18% |
| `bl67R9mK`（FUND quantile 504） | 0.345 | ❌ 差 38% |
| `rKRQOdkE`（pv20 beta 期限结构） | 2.21 | ✅ 过，但 S 仅 0.33 |
| `58ENzjRk`（pv20 beta 自身异常度） | 1.88 | ✅ 过，但 S 为负 |

**⇒ 决策意义（这是本会话最重要的战略转向）**：
- 对 `fundamental17` 换手率族，**S 与 SUB 是双向约束**：S 提到 1.58 时 SUB 门槛同步升到 0.751，而比值只有 0.449 ⇒ 无论怎么拉 S 都过不去。**该族已到结构上限。**
- 对 `RRE06nEz`，**SUB 约束自动满足**：S 1.58 ⇒ SUB 0.97（门槛 0.751，余量 +29%）。**唯一要做的就是把 S 从 0.91 拉到 1.58（+74%）。**
- ⇒ **仿真槽应从「FUND 族破 SUB」全面转向「PV T6 族拉 S」。**

### 10.4 T6 的放大杠杆清单（按先验强度排序）

| # | 杠杆 | 依据 | 状态 |
|---|---|---|---|
| 1 | **外层窗口 252 → 504** | `fundamental17` 同族实测：252→504 使 SUB/S 0.238→0.345、2Y +24% | 批 3 在测 |
| 2 | **平台 `decay` 10 → 低档** | TO 仅 9.13%，距 `HIGH_TURNOVER`（0.70）有 7.7 倍余量；平台 decay 作用持仓权重，**不改 SUB/S** ⇒ 对本几何是**纯赚**（本会话 `fundamental17` 族实证 decay↓ ⇒ S↑、比值不动） | 待派 |
| 3 | **ADV 字段换成 60 日档** | `adv60` / `adv60_extra_usd` 比 20 日档噪声更低（分母更稳）；20 日 ADV 在单日异常时会被污染 | 待派 |
| 4 | `ts_zscore` 替代 `ts_quantile` | 批 24 实测 zscore 保幅度、比值更高但绝对 S 更低 ⇒ **对本几何是反向**（要 S 不要比值），暂不优先 | 批 3 在测 |
| 5 | `truncation` 0.05 → 更低/更高 | 只在平台层改权重集中度 | 待派 |

**★ 杠杆 2 的独特价值**：这是本会话第一次遇到「比值已过闸」的候选，于是 `decay` 从「换手治理工具」升级为**纯信号放大工具** —— 记忆里「平台 decay 不动 SUB/S」这条铁律第一次变成了**有利**属性而不是中性属性。

---

---

## 十一、批 27 实证：平台 decay 10→2 让 T6 提升 22%（2026-10-30）

### 11.1 因子设计

同一表达式族，只动 decay，隔离"持仓层平滑"这一个变量。

| # | 表达式 | alpha | decay | S | F | TO | 2Y | SUB | SUB/S | dd | margin | fRA |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A | `ts_quantile(divide(adv20_extra_usd, firm_market_capitalization), 252)` | `RRE06nEz` | 10 | 0.91 | 0.58 | 9.13% | 1.39 | 0.56 | 0.615 | 6.94% | 10.98bp | 3 |
| B | 同上 | `VkxKd1xV` | **2** | **1.11** | **0.71** | 14.91% | **1.50** | 0.65 | 0.586 | **6.56%** | 8.29bp | 3 |
| C | `ts_quantile(divide(ts_mean(adv20_extra_usd,66), firm_market_capitalization), 252)` | `kqNeJENK` | 2 | 0.71 | 0.41 | 10.43% | 0.44 | 0.55 | 0.775 | 9.75% | 8.08bp | 3 |

### 11.2 A→B：decay 是纯赚的放大杠杆

- S **0.91 → 1.11（+22%）**、F **0.58 → 0.71（+22%）**、2Y 1.39 → 1.50（+8%）、dd 6.94% → **6.56%（−5.5%）**
- 唯一代价：TO 9.13% → 14.91%（上限 0.70，**余量仍有 4.7 倍**）
- SUB/S 0.615 → 0.586，轻微下降但**仍过 0.4754 闸**（余量 23%）

**结论**：对已过 SUB/S 闸的几何，decay 降到 2 是纯赚。这与此前"decay 不改 SUB/S、只改 TO 与 invest_ratio"的结论一致——本批把该结论量化到 pv20 上：**decay 10→2 使 SUB/S −4.7% 但 S +22%，净收益为正**。

**未测**：decay 1 / 0。TO 才 14.91%，离 70% 上限极远，decay 继续下降的空间很大。**这是该族当前成本最低的剩余杠杆。**

### 11.3 B→C：分子 66 日平滑再次失败

`kqNeJENK`（分子再叠 `ts_mean(...,66)`）S 0.71，比 B 的 1.11 差 36%，且 2Y 从 1.50 崩到 0.44。

**机理**：`adv20_extra_usd` 本身已是 20 日均值（预先平滑），再叠 66 日 = **双重平滑、丢失响应性**。这与批 3"窗口 252→504 反而更差"、以及"FUND 用单日成交量才需要 504 去噪"是同一根因。

**⇒ 该族正确的平滑层级：0 层（不复用 ts_mean）。**

### 11.4 本族完整几何结论（按已验证顺序）

| 决策点 | 已证最优 | 证据 |
|---|---|---|
| 分母 | **公司规模**（`firm_market_capitalization`） | S 0.91 vs 自身历史均值 0.68 |
| 外层窗口 | **252** | 504 更差（0.79 / 0.72） |
| 分布变换 | **ts_quantile** | ts_zscore 更差（0.72） |
| 分子平滑 | **不做** | 66 日平滑 0.71 |
| 平台 decay | **2**（可继续下探到 1/0，未测） | 10→2 提 22% |
| **重估层（ts_av_diff）** | **未试 —— 批 29 在测** | 见下方 §11.5 |

### 11.5 ★ 骨架纠正：T6 缺的是 ts_av_diff 这一层

**这是本会话一处重大记忆错误，必须纠正。**

此前把 `rKRQbPPE` 记成"与 T6 骨架完全相同（`ts_quantile(divide(A, cap), 252)`）"。**实际读取平台 code 后确认两者骨架根本不同**：

```
rKRQbPPE = rank(ts_quantile(ts_av_diff(divide(annual_ebitda_value, current_enterprise_value), 252), 22, driver=gaussian))
T6       = ts_quantile(divide(adv20_extra_usd, firm_market_capitalization), 252)
```

三条估值族主力的**统一骨架**（已逐条实读确认）：

| alpha | code | ts_av_diff W | S |
|---|---|---:|---:|
| `rKRQbPPE` | `rank(ts_quantile(ts_av_diff(divide(annual_ebitda_value, current_enterprise_value), 252), 22, driver=gaussian))` | 252 | 2.48 |
| `j2YNnKOQ` | `rank(ts_quantile(ts_av_diff(divide(quarterly_ebit_value, current_enterprise_value), 504), 22, driver=gaussian))` | 504 | 2.15 |
| `P0ojvkkJ` | `rank(ts_quantile(ts_av_diff(divide(quarterly_total_liabilities_4, current_enterprise_value), 66), 22, driver=gaussian))` | 66 | 1.93 |

**统一形式**：
```
rank(ts_quantile(ts_av_diff(divide(<FUND 分子>, current_enterprise_value), W), 22, driver=gaussian))
```

**三层归一化，各层作用不同**：
1. `divide(分子, EV)` —— 该科目的收益率（_yield_）
2. **`ts_av_diff(..., W)` —— 相对 W 日均值的偏离 = 重估（re-rating）** ← **核心层**
3. `ts_quantile(..., 22, driver=gaussian)` —— 22 日时序分位，去量纲、抗尾部
4. `rank(...)` —— 横截面秩

**为什么核心是第 2 层**：`divide(分子, EV)` 的水平值混杂了行业、成长性、会计口径等固有差异；`ts_av_diff` 把每只股票与**自身历史**比较，只留"变便宜/变贵"的增量信息。这解释了为什么该族 margin 高达 16.07bp、dd 仅 9.3%——**它不是价值因子，是重估事件因子**。

**⇒ T6 的 S 0.91 与 rKRQbPPE 的 2.48 差距，不是"分子纯度"问题，是"缺了重估层"**。§十 的"骨架已证明，差别只在分子强度"这个结论**作废**。

**批 29 条 A 正是把这一层移植到 pv20**：
```
rank(ts_quantile(ts_av_diff(divide(ts_backfill(adv20_extra_usd, 22), ts_backfill(firm_market_capitalization, 22)), 252), 22, driver=gaussian))
```
经济学含义：**流动性相对自身年度均值的异常偏离（流动性冲击）**，而非流动性水平的静态高低。

### 11.6 W（ts_av_diff 窗口）是调参维度，不是固定值

三条成功案例的 W 分别是 252 / 504 / 66，对应分子 annual EBITDA / quarterly EBIT / quarterly 负债——**无单调规律**。⇒ 换分子时必须重扫 W ∈ {66, 252, 504}，不能套用。

### 11.7 本批新增负例

`VkxKd1xV`（S 1.11，差闸 30%）暂列**最强 PV 候选**但未过闸；`kqNeJENK`（0.71）判死该平滑方向。