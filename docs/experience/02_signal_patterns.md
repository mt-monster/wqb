# 02 · 信号 / 结构有效性规律

> 来源：2026-09-05 ~ 09-29 工作日志实证提炼 ｜ 更新：2026-09-29

---

## 1. ★ 组合形态铁律（最高优先级）

**禁止把两条独立信号腿加权相加**——无论写成 `add(multiply(0.4,…))`、`0.4A+0.6B`，**还是等权 `add(rank(A), rank(B))`**（等权即 0.5A+0.5B，属同一违规族）。

**也禁止**靠增删腿数、或扫描混合权重去修不达标的信号。

> **事故背景（2026-09-28）**：wave189/190 产出 7 条 `add(group_rank(腿A), group_rank(腿B))`，
> 其中 `QPbp025Q` 表面极漂亮（S=2.11/F=1.80/2Y=1.89）但同样违规，**已全部作废**。
> 根因：闸 5 结构判定只拦"实参以 `系数*` 开头"的腿，其文档与原 SOP **明文豁免等权** → 7 条全部漏网。
> **门禁通过 ≠ 合规**：闸是兜底不是许可证。判合规看**本质**（是否两条独立信号腿相加），不看是否命中正则。

### 唯一合规方向 = Mode B

换字段组合 / 换信号概念 / 换算子几何 / 换分组轴；或**单信号结构化**。

**合规单信号结构白名单**：
- `ts_scale`
- `subtract(rank(A), rank(B))` —— **须有经济含义的单一价差**（如"核心盈利 vs 终止经营贡献"），不是拼腿
- `group_rank` / `group_zscore` / `ts_quantile`
- 事件门控 `trade_when` / `if_else`
- SuperAlpha combo

**放行 5 类运算**：`ts_corr` / `divide` / `subtract(rank,rank)` / `if_else·trade_when` / `group_zscore·group_rank`。

**闸 5 放行形态**（`_detect_equal_weight_leg_add`）：
- `add(abs(x), 0.01)` —— 1 腿 + epsilon
- `add(ts_mean(x,22), ts_mean(x,66))` —— 同形态仅窗口差异 = 单信号多窗平滑

---

## 2. 破闸旋钮（实测有效）

### 破 `IS_LADDER`

- **正确武器是 `trade_when` 交易条件门控，不是信号窗口参数**。
  HKG `O0r7lJ1J` = `trade_when(volume>adv20, 基底, -1)` → ladder **1.56 → 2.08**（+0.52）直接 ACTIVE。
  对照：拥挤度门 1.46 不够、prem 门全弱（1.11/0.63）→ **只有流动性门有效**。
- ⚠ **不要叠门**：流动性门 × 拥挤度门嵌套互相削弱（`dual_gate_o15` ladder 1.32，单流动性门 2.08）。
- **双层平滑 `add(短窗, 长窗)` 是 ladder 专用武器**：HKG vwap 族 `dual_decay` = add(88窗, 252窗) → ladder 1.80→2.04/2.08；单窗口 ladder 天花板 ~1.8。
- **decay 调快能拉开 IS_LADDER**：GBR dec12 → **dec8** 把 ladder 从 1.58 拉到 **2.07**；dec16（1.56）与换 STATISTICAL（1.55）**均无效**。

### 破 `LOW_SUB_UNIVERSE_SHARPE`（比值闸）

见 `01_platform_gates.md §2`。核心 = **换分组轴到 `market`**（决定性）或 `exchange`（给 2Y）。

### 破 `CONCENTRATED_WEIGHT`

**更正（2026-10-04）**：旧版写「唯一有效解法 = 降 truncation（0.08 → 0.04/0.02）+ 平滑」，与本文 §14 相反——CW 是数据品质问题，truncation / decay / 中性化修不了；降换手 53% 对 CW 零效果，补时间维覆盖率才过闸；且 truncation 在 IND / GLB 实测零杠杆（0.02 与 0.08 指标逐位相同、0.08→0.15 零影响）。排查顺序见 §14：覆盖率 → 数据类型 → 窗口 → `ts_backfill` 最小窗口 → 换思路；平滑要作用在**补过覆盖的原始字段**上，只对最终信号套 `ts_decay_linear` 不修 CW。
⚠ 但 GBR starmine 族实测连外层全市场 `rank()` 均匀化都 403 → **结构性拒绝时只有 `trade_when` 门控能过**。

### 破 turnover 墙

- **turnover 墙是"骨架"问题而非数据集问题**：GLB `intraday_pv_feats` 曾被判死（骨架 `corr_*_with_slippage` turnover >70%），
  换成 `-group_rank(ts_decay_linear(ts_backfill(F,66),34), industry)` 后 turnover 降到 **11.35%** → **判死范围应收缩到骨架，整集可重新纳入白名单**。
- **事件驱动信号必须重平滑**：IND `insiders1` 直接 rank 换手 1.08–1.30（限 0.4）；
  第二波 `decay=20 + 长窗(66/126/252) + trade_when 事件窗 + 存量水平替代净流量` → 换手压到 **0.05–0.17（≈26 倍改善）**，
  但 best sharpe 仅 0.61 → **换手是结构问题可解，sharpe 上不去是信号层失效**。
- 论坛降 turnover 清单里**只有 `ts_decay_linear` / `hump` / `trade_when` 可用**（`ts_decay_exp_window` 属 ghost_ops）。

---

## 3. decay / 中性化 / 分组轴

### decay

- **对 SELF 恒为负向杠杆**（单调）：KOR decay 12→300 使 SELF 0.816 → 过闸（12→0.816 / 40→0.774 / 100→0.729 / 200→0.702 / 300→过闸），指标同步下降但可预期。
- ★ **对 PROD 的方向取决于篮宽**（修正旧规律）：窄篮（limit 10）decay↑PROD↓；**宽篮（USA limit ≥ 池上限）decay 3→0.8527、10→0.8738、60→0.9084，即 decay↑PROD↑**。
  → 旧规律"decay 越大双降"来自 top-10 窄篮实验，**不可迁移到宽篮**。
- **decay 是压 SA「SELF 闸」的单调杠杆**，牺牲指标平滑可预期（V3 起点 sh3.13/fit4.07 → sh2.07/fit2.36 完全可承受）。

### 中性化

- **中性化是 SA 的决定性杠杆，且逐区不同、不可照搬**：
  - IND 三变体对照：V1 `SUBINDUSTRY/dec10` → self/prod 0.6875/0.6879 **PASS**；V3 `STATISTICAL/dec15` → 0.7996 **FAIL**。
  - KOR 存量最优 SA 是 STATISTICAL，但**新 SA 靠 SUBINDUSTRY/dec10 差异化才过**（0.8571）。
  - **SA 同构必死**：新 SA 的 `(neutralization, decay)` 若与存量某颗相同（`STATISTICAL/dec5`↔`rKOPg9gd`、`STATISTICAL/dec30`↔`j23jgb8Z`），self 直接 **0.89~0.97**。
    → **差异化的关键是错开 (nu, decay) 组合，不是组件微调**。
- ⚠ **勿靠换中性化解 `LOW_ROBUST_UNIVERSE_SHARPE`**：IND 9 档全劣化 = `STOP_STRUCTURAL`，换中性化只是烧预算。
  （基线 STATISTICAL 0.91 最优；CROWDING 0.08 / INDUSTRY 0.40 / SECTOR 0.31 / SUBINDUSTRY 0.32 / SLOW_AND_FAST 0.62 / MARKET -0.0 / NONE -0.0）
- **USA 的 SUBINDUSTRY 是子宇宙/ladder 闸的解药**（STATISTICAL 必挂 LOW_SUB_UNIVERSE_SHARPE）。
- **窗口白名单 = `[1, 5, 22, 66, 252, 504, 1008, 1260]`**：`operator_coverage.py` 曾为 `[20,60,120,5,10,252]`（6 里 4 违规）**是违规污染源**，全库 23% 用了非白名单窗口（违规 Top 恰是 20/10/120/60）；已改为 `[66,22,5,252]`。

### ★ 跨区移植配方时，中性化必须"逐字对齐"（2026-09-30 HKG w43 踩坑）

**REGULAR 配方跨区移植 = 端口**：表达式（形状/字段/窗/分组轴）**和**
`(neutralization, decay, truncation, universe档位, nanHandling, maxTrade)` **必须一起搬**，
只搬表达式等于换了一个实验。

> **⚠ 2026-10-03 补档位（此前清单漏了两项杀伤力最大的）**：
> 原清单只有 `(neutralization, decay, truncation, universe档位)`，**不含 `nanHandling`
> 与 `maxTrade`**——而实测这两项才是「强度闸」级别的：
> IND behavioral_signals 族同表达式 decay8 下，**`nanHandling=OFF` 或 `maxTrade=ON`
> ⇒ `sharpe 2.19 → 0.46`**。它们看起来像无害的风格开关，实际能把信号打掉 4 倍。
> ⇒ 移植前必须读源配方的这两个值，不能依赖任何工具的缺省。
> 进一步：**工具缺省互不相同**（`tools/submit_batch.py` / MCP `create_simulation` /
> MCP `create_multi_simulation` / `brain-sim-alphas-in-batch-and-track` 纯透传无缺省），
> 「用哪套工具跑」会静默改变结论 ⇒ **跨工具结果不可比**，详见
> [`ra-pipeline` 步 6「设置档不可比」](Claude/skills/wq-brain-ra-pipeline/SKILL.md)。

**战例**：KOR `zq87zzqO` 成功配方（S=1.76/F=1.38/T=0.1361）移植到 HKG w43 时，表达式逐字照搬，但中性化**擅自填了 `INDUSTRY`**（未抄 KOR 的 `STATISTICAL`）→
  - w43 全部 A 族 `S ≤ 1.25`（`core_market_neg` 1.25 / `core_industry` 0.96 / `core_subindustry` 0.99）
  - w44 仅改 `neutralization: INDUSTRY → STATISTICAL`（其余逐字不变）→ 见 10.4 实测

**纪律**：
1. 移植前先 `SELECT neutralization, universe, turnover FROM alphas WHERE alpha_id='<源>'` **读源配方的设置**，不凭印象填。
2. `decay` 一并核对；**源配方 decay 未知时不要默认沿用上一波的 12**，用小幅扫描（如 0/4/22）定标。
3. **universe 档位必须查 `config.REGIONS[region].universes`**（HKG=`TOP800/TOP500`，KOR=`TOP600`）——跨区档位不可外推，非法档位平台 400 直接拒。
4. **诊断顺序**：跨区移植结果显著低于源配方时，先查设置（nu/decay/universe）再查表达式，**设置差异的杀伤力 > 几何微调**。
   - 反面教训：w43 结果出来后，第一反应是"加几何变体（窗/指数）救"，而真正的根因是中性化填错——**先对齐设置，再谈几何**。



### 分组轴

- **分组轴选择显著影响 SELF**：`group_rank(..., industry)` → SELF 0.58；`subindustry` 版 SELF 0.91 全灭。
- **分组轴换到 `market` 是破 SUB 比值闸的决定性旋钮**。

---

## 4. 首颗成功范式（KOR，2026-09-28）

```python
signed_power(ts_rank(group_rank(<核心盈利资产收益率价差>, market), 504), 0.5)
```

- KOR **`wpZkk1Mp`** → **ACTIVE**，prod **0.6476** / self **0.187**，MATCHES_PYRAMID `KOR/D1/FUNDAMENTAL` ×1.6。
- 信号源是**冷门 fundamental 字段** `other466`（users 0–14）→ **冷门字段仍有 alpha**。
- 价差两腿派生自同一组 3 个字段（`(CNI−DO)/TA` 与 `DO/TA`），经济含义为「核心盈利 vs 终止经营贡献」→ **属单一信号而非拼腿**（合规）。

---

## 5. 结构-指标映射（KOR other466 族，可复用知识）

| 结构 | S | 2Y | SUB | 定位 |
|---|---|---|---|---|
| `ts_rank` 双腿价差 | **2.04** | 1.34 | 1.25 | **S 强、2Y/SUB 弱** |
| 原始比率双腿价差 | 1.13 | 1.57 | 0.95 | 2Y 近线 |
| `group_rank(原始价差, industry)` | 1.55 | **1.93** | 0.74 | **2Y 强、S/SUB 弱** |
| `group_rank(ts_rank价差, industry)` | 2.12 | 1.23 | 1.30 | S+SUB 强、2Y 弱 |
| **`add(两条 group_rank)`** | 1.96 | 1.69 | 1.01 | ⚠ **违规（等权混腿），已作废** |

**⇒ 结构-指标映射结论**：`ts_rank 价差`给 S、`原始比率价差`给 2Y、`group_rank` 给稳健。
**慢×快价差结构**（`subtract(group_rank(慢腿), group_rank(快腿))`）**稳定有效**——相对基座同时抬三项 S 1.23→1.30 / F 0.89→0.94 / 2Y 1.33→1.87，near 率 1/10 → 6/8。

---

## 6. 信号族有效 / 无效的实测判据

### 有效

- **冷门数据集是破饱和的现实路径**：数据集头部集中（multifactor_return_pred 等 5 个 dataset 占 ~45% 表达式），
  而**历史 ACTIVE 全走冷门 dataset**（pv106 / transaction_cost / anl9 / oth696 / fnd86 / mdl177 / **other466**）。
- **低成本造高正交组件配方 = 同一持仓腿 + 互斥触发时段**（`trade_when` 分状态，触发器不同：earnings `ern3_pre_interval` / imbalance `imb5_mktcap` / news `headline_item_count`，持仓腿同为 `-rank(ts_mean(corr_last_trade_price_with_volume,5))`）
  → 三颗骨架各异、持仓时段近乎互斥，实测大幅降低组合相关性。
- **`trade_when` 条件择时能把同源字段显著正交化**：`ZYbqREW1` 与 `pwRJmvP3` 共用 `mean_flash_estimate_pretax_annual12`，SELF 仅 **0.2271** vs 0.3093。

### 无效

- **一阶优先、算子数控制**：op ≤ 3，禁止二阶套二阶（论坛实证：二阶套二阶 VF 0.9→0.1）。
  9 条一阶骨架 = slope / growth_rate / ar_slope / squared_momentum / decay_momentum / rank_reversal / log_smooth / signed_power / delta_stack。
- **HKG 市场 RISK/MODEL/IMBALANCE 类因子横截面方向普遍为负**：`rsk70_mfm2_*`、`mdl110_score`、`imb5_score` 裸 `group_rank` 全负 sharpe，**取反后全正**（一致性结论不是噪声）。
- **`ts_zscore` 制度腿方向与原 sign 结构天然相反**，变体必须带 negate。
- **字段语义判定不能只看名字**（缩写歧义：`is` = Income Statement vs `is_` 标志；`indicator` = 技术指标 vs 布尔指示）
  → 名字只用于无歧义强标识符（gvkey/cusip/isin/exrate/currency_code/日期），其余一律**看描述文**。
  两处误杀实证：`oth466_is_ebit_oper_q`（利润表 EBIT，users=248）被当布尔标志误杀 39/177；model109 的 Bollinger Bands / Altman Z-score 被误杀 51/539。
- **风险模型因子载荷不是超额来源**：risk70 = 风险模型因子载荷（96 字段），best S=**0.87** 全灭。
  **推广规律**：字段描述含 Factor Loading / Exposure 的数据集，其载荷就是模型要中性化掉的暴露 → **只可作辅助腿**。
- **`ts_max` 是完全未开垦算子**（已提交 231 条里 0 次、全库精确 `ts_max(` 0 次）。
  近亲 `ts_arg_max` 已落地 2 次说明极值思路可行；但 `ts_max_diff` 试 146 次几乎全 dropped、4 次实跑全负 Sharpe
  → **说明"最大值族"的差分形态切入点效果差，不代表 ts_max 本身无效**。

---

## 7. IS → OS 衰减

- 期望 **OS ≈ 0.32 × IS**（区间 0.05 ~ 0.65）。IS 1.58（提交门槛）→ OS 期望 ≈ 0.50；要 OS 中位 ≥ 0.7 需 IS ≥ 2.19。
- **IS 对 OS 无预测力**：`corr(IS, 保留率) = +0.001`、`corr(IS, OS) = +0.092`。
- **负 OS 比例恒 ~22%**（IS 0~1.5 / 1.5~2.0 / 2.0~2.5 三桶均 20–22%）
  → **抬 IS 门槛不能降风险，只能略微抬期望**。
- **降风险三杠杆** = 分散（数量 × 跨区）+ `os.sharpe60` 事后监控 + 族去相关。
- **过拟合四信号**：decay 断崖 / 年际方差 > 1.0 / 去头尾腰斩 / 逐年 corr 跳变 > 0.4。

---

## 8. ★ 漏斗真相：瓶颈是 prod，不是 gate 也不是生成量

| 指标 | 实测值 |
|---|---|
| gate 通过率 | 49.7% |
| **prod 淘汰率** | **68%**（421 已测中仅 135 ≤ 0.7） |
| **端到端成功率** | **0.10%** |
| 回测 Sharpe > 1.58 | 14.8% |
| 2Y > 1.58 | 11.8% |
| prod < 0.7 | 31.1%（均值 0.767，平均就贴红线） |

- **prod 分布中心在闸门之外**：中位 **0.7606** / 均值 0.7554 → 是整体问题不是尾部问题。
- **⇒ 作用在 IS 或生成量上的优化无终局价值，唯结构性降相关。**
- 全库 19,567 条表达式**仅 5.7% 被回测**；复合 ≈ **0.54% / 次回测** → **瓶颈是"选得准"不是"挖得多"**。
- **勿加大 S2 吞吐**（89.7% 未消化 + 32% 未过门禁，再生成只加深积压）。

### IS 闸失败分布（602 条抢救池）

| 闸 | 条数 |
|---|---|
| `IS_LADDER_SHARPE` | 272 |
| `LOW_SHARPE` | 90 |
| `LOW_ROBUST_UNIVERSE_SHARPE` | 61 |
| `CONCENTRATED_WEIGHT` | 35 |
| `LOW_2Y_SHARPE` | 10 |
| `LOW_SUB_UNIVERSE_SHARPE` | 8 |
| `HIGH_TURNOVER` | 3 |

→ **IS 强度不足是结构层问题，参数层救不了。**

---

## 9. 其他实测规律

- **结构差异化优于参数微调**：HKG 第 3 颗 `WjPPjVQd`（双门嵌套）SELF 0.5894 成功避开孪生风险；同参数姊妹颗 `d5OO50dE` SELF 0.9936 全灭。
- **指标最优 ≠ 可提交（反直觉）**：HKG 波 5 中 sh/ladder 最高的 `grp_none`/`grp_market`（1.79/2.22）SELF 反而 0.9105 全灭；唯一 SELF 干净的 `0mRrmlPr` sh1.57/ladder1.79 双闸贴线未过。
- **truncation 在小宇宙上是无效旋钮**：HKG TOP800 上 trunc 0.05/0.06/0.10/0.12 四变体指标完全一致。
- **门控 `trade_when` 能 gated 掉 fitness，但代价明确**：套到 f12m/40d 上 IS 从 S1.68/F1.05 掉到 **S1.44/F0.84**（F<1.0 提交层必挂）。
- **`quality_predictor` 预筛有效**：DEU `other699` 预估 0.45–0.46 vs 实测 best|S| 0.48 → 可作烧配额前预筛。
- **`reverse(x)` ≡ `-x`**（逐元素取负），而 `-rank(x)` ≠ `rank(-x)` → 两者是不同构的独立变体。

---

## 10. ★ 稀疏/低频字段的几何：判别标准是「时变频率」不是「coverage」（2026-09-30 两轮实证，含修正）

### 10.1 现象（HKG 三波 + KOR 两轮）

| 波 | 数据集 | 字段性质 | 结构 | 最佳 \|S\| | T |
|---|---|---|---|---|---|
| HKG w34 | behavioral_signals | 稀疏 | 裸 `group_rank` | 0.49 | 0.15 |
| HKG w35 | ai_news_scores | 稀疏 | 裸 `group_rank` | 0.59 | 0.06 |
| HKG w36 | insider_feats | 稀疏 | 裸 `group_rank` | 0.63 | 0.05 |
| KOR w39 | news_sentiment_dl | 日频事件型 | 裸 `group_rank` | **-0.03** | **0.248** |
| KOR w41 G1 | news_sentiment_dl | 日频事件型 | **长窗** `ts_rank(504)`+`signed_power` | **-0.20** | **0.251** |

⇒ **关键否证**：KOR w41 证明**长窗 ts_rank 对日频事件型字段无效**（S 反而从 -0.03 掉到 -0.20）。**§10 初版"稀疏字段就上长窗"的表述过于宽泛，已修正。**

### 10.2 修正后的判别标准

**不是 coverage（稀疏度），而是输入的「时变频率」**：

| 输入性质 | 代表 | 长窗平滑 | 原因 |
|---|---|---|---|
| **低频**（季度财报、窗口聚合后稳定） | KOR other466 价差 | **有效** ✅ | 输入本身稳定，长窗提纯 |
| **高频**（日频新闻情绪、逐日跳变） | news_sentiment_dl | **无效** ❌ | 输入每天跳，平滑只把噪声平均成 0 |

**佐证 = 换手率 T**：成功配方 T≈0.075~0.136；日频事件型失败组 T≈0.25（**2~3 倍**）。**T 高 = 信号逐日跳变 = 长窗救不了。**

**机理**：`ts_rank(vec_avg(新闻情绪), 504)` 里 `vec_avg` 每天对新闻做平均，新闻每天变 → 输入逐日跳变 → `ts_rank` 只是**重新排序跳变**，未降噪。正确修法是**先做时间聚合再排序**（`ts_mean(vec_avg(f), 60)` / `ts_decay_linear`），让输入本身先稳定下来。

### 10.3 两条独立约束（都需记住）

1. **`ts_backfill` 不支持事件型输入**：`Operator ts_backfill does not support event inputs`（KOR w40 26 条全挂）。事件型字段（news 类）**不能用 backfill 补 NaN**——这条是 §10 初版配方的硬边界。
2. **平台无 `ts_co_skewness`**：103 算子中时序类 26 个 `ts_*`，**无协偏度算子**。高阶共动的平台替代路径 = `ts_corr`（耦合强度）/ `ts_covariance`（共动幅度）/ `ts_regression(y,x,d,rettype=k)`（斜率/残差）。

**结论**：**"塔未点亮"≠"随便挖就能出"**——塔只决定收益归属；能否活，取决于「输入时变频率 × 几何匹配」。低频输入配长窗、高频输入配时间聚合，配错方向就是白跑。

---

## 11. ★ 多腿强度不可逆拆分：存量多腿**不能**当作单信号供给来源（2026-10-01 DEU w45 实证）

### 11.1 现象

DEU 91 颗 IS 合格存量**全部是 `add(add(add(rank(...), rank(...))))` 多腿混招**（违反组合形态铁律 §0，一颗不可提交）。直觉上「把强腿拆出来单独用」应当可行 —— **实测否证**：

| 层级 | 最佳 S |
|---|---|
| 原多腿组合（违规，不可提交） | **2.17** |
| 拆出的单腿（合规，单信号结构化） | **1.36** |

**w45 完整实验**：提取 DEU 存量中 47 个高复用单腿（分析师预期修正族被复用 87/67/56/52/44 次），取 Top-12 配 3 几何（`g1` 长窗 `signed_power` / `g2` `ts_decay_linear` 平滑 / `g3` 双层排序）× 2 分组轴 = **82 条**，设置逐字沿用 DEU 存量标准（TOP500/SUBINDUSTRY/decay4/trunc0.08）。

**结果：`S≥1.58` = 0 条**（`F≥1.0` 仅 1 条）。最高 `est_chg_eb90d22_g2_subindustry` S=1.36 / F=0.96 / 2Y=0.31 FAIL。

### 11.2 机理与判据

- **强度来自叠合，不在单腿**：多腿 S=2.17 的收益是各腿**弱信号（|S|≤1.36）叠加**后的效果，拆开即散。
- **历史佐证（DEU）**：该区所有 `best_S > 1.58` 的波次（`s2_grtransform_r83`=2.17 / `s2_lean_le89_r89`=2.15 / `s2_other455_r85`=2.09 …）**无一例外全是 `s2_*` 多腿/增强波**；纯单信号波从未越过 1.58。
- **前置判据**：评估某区存量能否抢救，**必须看「单腿峰值」而非「多腿峰值」**。若 `max(单腿 |S|) < 1.58` → **该存量族整体不可抢救**，换字段族或换区，不要浪费回测预算。

### 11.3 几何侧收获（次要，可复用）

- **`g2`（`ts_decay_linear` 平滑）系统性优于长窗 `signed_power`**：平均 |S| 0.86 vs 0.66（`g3` 0.62）。与 §10 一致 —— **先时间聚合再排序**优于直接长窗排序。
- 腿强度排序（DEU）：`est_chg_eb90d22`(1.36) > `est_chg_eb14d5`(1.32) > `est_chg_ern14d5`(1.27) > `armrev`(1.10) > `loan_rate_vol`(1.06)。

**结论**：**"从违规多腿里拆腿"是死路** —— 拆出来要么不够强（本例），要么就是原多腿的弱投影。**存量多腿不可用作单信号供给来源。**


---

## 12. ★ 等价算子替换：判定「天花板」前必须扫（2026-10-03 KOR 实证，首颗 ACTIVE 由此产出）

**机器消费层**：`methodology_rules.json::equivalent_operator_substitution_v1`（`RuleStore` 自动注入 S4/gate/review_wave）

### 12.1 核心命题

> **判定「不可能 / 天花板 / 已到顶 / 无解」之前，必须先扫等价算子替换。否则会把「实现路径的约束」误判为「结构性的约束」。**

**为什么**：等价算子数学含义相同但**数值路径不同**，能**同时改动多个闸门**；而几何调整（分子/分母/窗口/分组轴）往往一次只动一个闸门。

KOR other466 实证（`gJZ7AvZO` → ACTIVE 2026-10-03）：

| 步骤 | 包装 | 2Y | prod | 多空 |
|---|---|---|---|---|
| 基线 | `signed_power(·, 0.5)` | 1.51 ❌ | 0.6544 | 350/288 |
| 换实现算子 | `quantile(·)` | 1.56 ❌ | **0.6397** | **319/319** |
| 换外层轴 | `quantile(·)` + market | **1.62** ✅ | 0.6413 ✅ | 319/319 |

**被推翻的结论**：d7 曾判定「2Y 与 prod 在分组轴上反向搬运、构成不可能三角、该族已到天花板」——换 quantile 包装后**互斥消失**。

### 12.2 已验证的替换清单（KOR other466）

| 替换 | 效果 | 判定 |
|---|---|---|
| `signed_power(x,0.5)` → **`quantile(x)`** | 2Y +0.05~0.11、prod −0.015、多空拉齐 | ★★ 最强 |
| 外层轴 sector→market（**quantile 包装下**） | 2Y +0.06 | ★★ 依赖包装，不可外推 |
| `divide(A,B)` → `multiply(A,inverse(B))` | 逐项完全相同 | 仅作数值稳定性探针 |
| `ts_rank` → `ts_quantile` | 2Y −0.05 | 反向 |
| `ts_rank` → `ts_zscore` | 2Y −0.13 | 反向 |
| `group_rank` → `group_zscore`（内或外层） | 2Y −0.5 以上 | 反向（该族 2Y 依赖组内秩） |
| `scale(-rank(x))` | **S −2.24 直接翻负** | ⚠ 记忆 IND 语法效应在 KOR **反向** |

### 12.3 三条纪律

1. **记忆里的语法级效应必须本区实测**。`SCALE-NEG-RANK-ROBUST-SYNTAX`（IND 实证 `scale(-rank(x))` 过 robust 闸）在 KOR other466 令 S 翻负。
2. **最优分组轴依赖包装算子**。signed_power 包装下 sector 最优（1.51>1.47），quantile 包装下 market 最优（1.62>1.56）⇒ **不可跨包装外推**。
3. **`quantile` 只接受 1 个位置参数**（`quantile(x, driver=uniform)` 被门禁判 ARITY 违规）；`ts_quantile` 才接受两参。

### 12.4 扫替换的标准动作

冻结骨架（分子/分母/分组轴/窗口）→ 只换实现算子 → 跑 batch → 对比四闸。
几何调到「差一点过线」时（尤其 2Y / SUB 这类被单个几何锁死的闸），**先扫替换再判死**。


---

## 13. ★ 同族 prod 撞墙时先查「是不是同分母」（2026-10-03 KOR 第二颗 ACTIVE 实证）

**机器消费层**：`methodology_rules.json::denominator_is_the_real_self_wall_variable_v1`

### 13.1 机理

`divide(A, B)` 的**分母 B 决定横截面比较基准**。同分母 ⇒ 持仓结构相似 ⇒ 与同族高相关。

> **换分子只改经济量，不改比较基准 ⇒ 撞同一面墙。换分母才是破 SELF 墙的真变量。**

KOR d11 实证（扫 8 个分子，分母固定 `bs_eq_tot_q`）：

| 分子 | S | 2Y | self vs 已提交 | prod |
|---|---|---|---|---|
| `oth466_is_net_inc_basic_q` | 1.77 | 2.12 | **0.7422** | 0.8061 ❌ |
| `oth466_is_ebit_oper_q` | 2.12 | 1.06 | — | 2Y 差 |
| 其余 6 个分子全部 raf≥1 | — | — | — | 无一过闸 |

**8 个分子全灭，而撞的都��自己 40 分钟前提交的 `gJZ7AvZO`（同分母）。**

### 13.2 破法：只换分母，两闸同时降

KOR d12（**同分子 `is_net_inc_basic_q`，只换分母**）：

| 分母 | 口径 | S | 2Y | self | prod |
|---|---|---|---|---|---|
| **`bs_assets_curr_q`** | **资产侧** | 1.79 | **2.22** | **0.6244** | **0.6843** ✅ |
| `bs_eq_tot_q` | 权益侧 | 1.77 | 2.12 | 0.7422 | 0.8061 ❌ |
| `des_mkt_cap_q` | 市值 | **1.87** | 1.48 | — | 2Y 差 |
| `q_qe_moc_sb` | 权益 | 1.14 | 1.12 | — | raf5 全灭 |
| `q_qe_srdlhs_sb` | 权益 | 1.30 | 1.13 | — | raf3 |
| `des_com_shs_out_secs_q` | 股本 | 1.13 | 1.18 | — | raf5 全灭 |

**只换分母 ⇒ self −0.12、prod −0.12，两个闸门同时受益。**

### 13.3 分母口径还决定信号强度（不只是相关性）

KOR 该族实证：**资产侧口径出 2Y，权益/股本侧口径全灭**。

- 资产侧：`bs_assets_curr_q` 2.22 / `bs_eq_tot_q` 2.12
- 权益与股本侧：`q_qe_moc_sb` 1.12 / `q_qe_srdlhs_sb` 1.13 / `des_com_shs_out_secs_q` 1.18
- 市值口径 `des_mkt_cap_q` S 最高（1.87）但 2Y 弱（1.48）⇒ **市值出强度、资产出 2Y**

⇒ 分子分母都是「比率型信号」时，**分母是经济基准的选择**，比分子更决定成败。

### 13.4 标准动作

1. `compute_mutual_correlation` 定位撞的是**哪一颗**（别猜）
2. 若撞的是同族已提交兄弟 → **比对分母**是否相同
3. 分母相同 → 换分母（优先试另一类口径：资产侧 ↔ 市值侧 ↔ 权益侧）
4. 分母不同仍撞 → 才是分子/窗口/轴的问题

⚠ 关联记忆 `SELF-CORR-FAMILY-CANNIBALISM` 记录的是"症状+幅度"（0.6476→0.6791），本条补的是**根因与破法**。

---

## 14. ★★★ CONCENTRATED_WEIGHT 破局方法论（论坛 66 赞手册 + KOR 实测印证，2026-10-03）

**来源**：LC97552《CONCENTRATED WEIGHT 系统性排查与修复手册-1》2026-06-04（66 赞 / 29 评）
**机器层**：`methodology_rules.json::concentrated_weight_is_data_quality_not_params_v1`

### 14.1 核心断言（已被本项目实测印证）

> **「90% 的 CW 失败不是参数问题。CW 是数据品质问题。truncation / decay / neutralization 修不了 CW。」**

**KOR shortinterest38 实测印证**（d18 vs d19）：

| 手法 | 类别 | 换手 | S | CW |
|---|---|---|---|---|
| 基线 | — | 0.298 | 2.00 | **FAIL 0.342** |
| `ts_decay_linear(22)` | **参数类** | 0.14（−53%） | 2.15（↑） | **FAIL 0.345（纹丝不动）** |
| **`ts_backfill(·, 66)`** | **数据类** | 0.30 | 2.00 | **PASS** ✅ |

**降换手 53% 对 CW 零效果；补时间维覆盖率直接过闸。** 「纹丝不动」在本地数据上精确复现。

### 14.2 排查决策流程（按此顺序，不要跳步）

1. **查数据集覆盖率** —— <40% → **立即换数据集**（最高 ROI，勿在算子上浪费变体）
2. **查数据类型**
   - VECTOR → `vec_avg` 转标量 + `ts_backfill`
   - 事件型（财报/一致预期）→ **跨 Category rank 加法**（同 Category 内算子修复有 50+ 变体失败的明确证明）
   - 时序型（PV/分析师目标价）→ 进第 3 步
3. **查窗口长度** —— 信号窗口拉长 2–5 天，CW 转 PASS？
4. 仍 FAIL → `ts_backfill` **最小窗口**（1–5 天起试）
5. 仍 FAIL → **换 alpha 思路**（某些想法天然无法合规表达）

### 14.3 修复工具清单（按手册分类）

- **缺失/覆盖**：`ts_backfill(x, d)`（推荐 d=2~40，基本面可 60）/ `group_backfill` / `group_extra` / `group_count(is_nan(a), market) > N ? a : nan`
- **分布控制**：`rank` / `ts_rank` / `group_rank`（最常用，转均匀分布）/ `zscore`（配 tighter truncation 0.01–0.05）/ `scale` / `truncate` / `left_tail`/`right_tail` / `log`（右偏）
- **平滑降噪**：`ts_decay_exp_window` / `exp_window` / `ts_weighted_delay` / `days_from_last_change` / `last_diff_value` / `keep`
- **中性化**：换层级（强行业倾斜时 market 中性化会产生大额对冲头寸）
- **交易/持仓**：`trade_when`（显著降低换手与权重波动）
- **新兴市场**：`group_count` 检测初期数据不全；「微小噪声填充法」`add(b, 0.0001 * group_rank(-t, industry), filter=true)`（⚠ 手册原文记录：这是加权拼腿，被闸 5 / 路线 A 禁止，本库**不得使用**；新兴市场数据不全请用 `ts_backfill` 或 `trade_when` 门控）

### 14.4 ⚠️ 算子可用性必须核实（本轮实测踩坑）

手册点名的 **`ts_decay_exp_window`（MEA 帖称"最终用它通关"）与 `exp_window` 在当前平台算子表中已不存在**，门禁报 `[GHOST] 平台不存在，回测 ERROR 并连坐整批 CANCELLED`。

> **论坛方法论可用，但算子名可能已下线 —— 任何论坛给的算子，写进表达式前必须先过门禁 GHOST 校验 / 查 `get_operators`。**

### 14.5 检索通道现状

- `tools/forum_recon.py` 报 `control_probe_failed`（对照检索 0 结果 ⇒ 通道失效，**不作为「论坛无解」证据**）
- **MCP `search_forum_posts` / `read_forum_post` 通道正常** ⇒ 论坛检索优先走 MCP
- `data/forum_cache.json` stale 32.9 天且 5 个 bundle 无 CW 主题 ⇒ CW 类问题必须定向 `search_forum_posts`

## 15. ★ 骨架多样性闸：收益在「组合层」不在「单波产出层」（2026-10-04 KOR 实证，818 波次）

**问题**：骨架多样性闸到底有没有收益？该不该为了「多样」而把波次骨架摊开？

**实证口径**：对本库 **818 个有回测的波次**，按「波内归一化骨架熵」（算子序列骨架的 Shannon 熵 / log(n)）分三档，看 `best Sharpe >= 1.58` 的命中率：

| 骨架多样性档 | 波数 | 平均 best S | 中位 best S | **S>=1.58 命中率** |
|---|---|---|---|---|
| 低（骨架单一） | 252 | 1.50 | 1.62 | **51.6%** |
| 中 | 252 | 1.45 | 1.36 | 42.9% |
| 高（骨架多样） | 254 | 1.17 | 0.96 | **25.2%** |

**结论：骨架越单一，单波产出率越高 —— 高多样性档命中率不到单一档的一半。**

### 15.1 为什么？（两条纪律在打架）

- **产出纪律**：信号强度来自「把一个机制挖透」——同骨架换字段 / 换轴，强度可累积（KOR other466 实证：同骨架换分母连出 2 颗 ACTIVE）。
- **组合纪律**：book 自相关要靠「分散在多个机制」来压——但每条都在浅尝，谁都过不了 1.58。
- ⇒ **多样性闸的收益在「组合层（降 book 自相关 / 提 SuperAlpha 质量）」，不是「单波产出层」。用单波产出率去衡量它是错口径。**

### 15.2 正确用法 = 分阶段（**不是**「取消这个闸」）

| 阶段 | 闸 | 理由 |
|---|---|---|
| **探针 / 深挖** | `--skip-diversity-gate` | 单骨架、纯归因。骨架摊开会让「是机制没信号、还是骨架没配好」无法归因 |
| **批量产出** | **开闸** | 骨架混合，为 book 多样性与 SuperAlpha 质量负责 |

- 逃生阀是**官方**的：`gate.py` L1545 `--skip-diversity-gate`；`repair` 批天然豁免（`gate.py` L952）。
- **反例警示**：不要因为「多样性档命中率低」就永久关闸——那是把「产出率口径」当成「闸的价值」的错误推理。

### 15.3 配套：探针波的正确形态（d29 / d30 实证）

**冷门数据集先 1-2 条裸探针验 IS 强度，再投入完整波次**，避免 d27 教训（直接发 8 条完整波、全灭、best S=0.56 才发现族无信号，白烧一波预算）：

| 波 | 数据集 | 裸探针结果 | 判定 |
|---|---|---|---|
| d27 | 某集（直接发完整波） | 8 条全灭 best S=0.56 | ❌ 反例：浪费预算 |
| d29 | `analyst_factor_signals` | 8 条裸 `group_rank(f,x)`，best S=0.99 | ✅ 判死 eps 增长因子族 |
| d30 | `other455` | 8 条裸 `ts_delta(f,22)`，best S=0.43 | ✅ 判死图嵌入漂移族 |

**判死线：裸探针 |S| < 0.5 即判死入库**（不入完整波）。

### 15.4 附带结论：图嵌入 PCA 分量不可作 alpha 输入（other455 实证）

`other455`（关系网络 Node2Vec/ROAM 图嵌入的 PCA 分量，300 字段 / coverage 0.77-1.0 / alphaCount 平均 0.2）在 KOR 验证：

- 字段形如 `*_pca_fact{1,2,3}_value`，`description` 明写 "N-th eigenvalue/principal component score"。
- d30 八条 `ts_delta(field, 22)`：best `relation_roam_w1_fact2` S=0.43 / 2Y=1.05；**`fact1` 全负、`fact2` 全正** ⇒ **PCA 分量符号随对齐随机翻转，两个分量是同一轴的镜像而非独立信号**。
- **规则**：`*_pca_fact*_value` 类字段（绝对水平无经济含义）不作 alpha 输入；若日后重试，需换**非 PCA 的连续 latent score**且先裸探针。

## §16 分母 ≠ prod 墙的唯一变量（KOR other466 d33 实证，2026-10-04）

**背景**：d33 固定已验证骨架 `quantile(group_rank(ts_rank(group_rank(divide(NUM,DEN),industry),1008),market))`，
把分母从权益侧 `oth466_bs_eq_tot_q` 换成资产侧 `oth466_bs_assets_tot_q`，扫 8 个净利族分子。

**结果**：vR29LgEz（`consol_net_inc_q / bs_assets_tot_q`）IS 全闸通过
（S 1.94 / F 1.53 / 2Y 2.51 / SUB 1.17），**但 prod = 0.7671 撞墙**。
对照组：同骨架已 ACTIVE 的 gJZ7AvZO（`ptx_inc_norm_q / bs_eq_tot_q`）prod = 0.6413；
0mrnWojG（`net_inc_basic_q / bs_assets_curr_q`）prod = 0.6843。

**根因**：vR29LgEz 的分子 `consol_net_inc_q`（Net Income - Consolidated）
与 0mrnWojG 的分子 `net_inc_basic_q`（Net Income Available to Common - Basic）
**经济含义同义**（都是"归属股东净利"），同义 ⇒ 同持仓 ⇒ 同 prod 墙。
**换分母完全没能破墙，prod 反而更高。**

**修正前认知**：`denominator_is_the_real_self_wall_variable_v1` 声称
"换分子只改经济量、不改比较基准，撞同一面墙；真变量是分母"。

**修正后判据（三段式）**：
1. 先查**分子经济概念**是否与已提交兄弟**同义** → 同义则必撞，换分母无用（d33 情形）。
2. 分子概念确实**不同**（如营业利润 vs 净利 vs 收入）→ 才谈换分母。
3. 分子不同 + 分母不同 → prod 才可能真正下降。

**副产物**：d33 扫出 4 条过 S/F 闸（vR29LgEz/ZYAxpG80/xAbQxgLn/P0g6p9Rx），
说明**同骨架换分子能稳定复制 IS 强度**（这正是骨架多样性的组合层价值），
但**IS 强度与 prod 新颖度负相关**——越强越像已提交的。

**下一步（d34）**：保有骨架 + 分母，换【非净利/非收入】经济概念分子
（ROCE / 再投资率 / 现金占比 / R&D / SGA / capex / PP&E / DPS），逐条查 prod。
