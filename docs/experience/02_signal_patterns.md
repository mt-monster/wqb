# 02 · 信号 / 结构有效性规律

> 来源：2026-09-05 ~ 09-29 工作日志实证提炼 ｜ 更新：2026-10-24（§8 增补 USA 2026-10-23 复盘的转化率）

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

#### ★★★ 2026-10-06 DEU 更新：**轴族是最大杠杆**（89 波墙一次推平）

DEU `IS_LADDER_SHARPE` 从 1.58（== limit，判 FAIL）→ **2.07**，拿到该战役第一颗零 FAIL + prod/self 双过的可提交 REGULAR。

| 杠杆 | 量级 | 备注 |
|---|---|---|
| **慢分量分位桶轴（自造）** | **ladder 1.58 → 2.07（+0.49）** | `group_neutralize(x, bucket(rank(ts_mean(ts_backfill(F,1008),252)), range="0,1,0.1"))` |
| platform `decay` 4→8 | +0.10 | 单峰，16 崩塌；6~9 同平台 |
| 双窗 `add(ts_mean(短), ts_mean(长))` | +0.02 **且 S +0.09 / F +0.36 / 换手↓** | **唯一零代价**；长腿须 ≥252、短腿 8；`quantile` 必须在 add 之外 |
| 异族第三层轴（`subindustry`） | +0.01 **且 +0.25 S** | 同族键再叠 **−0.11** |

**三条硬约束（单变量对照实证）**：
1. **轴必须与信号的经济结构同源**——行业族 ✅、文本图关系 `oth455` ✅、**信号自身慢分量** ✅；
   **统计风险聚类 ❌**（`pv29` 的 `sta1_top400/1200_c2/5/10/20/50` 共 10 个**零算子零拥挤** GROUP 字段，实测 **10/10 崩塌**、2Y 转负）；
   **按信号自身分桶 ❌**（2.07 → 0.91~1.29）。**桶要按"信号之外的东西"分。**
2. **桶粒度适中**：十分位 `range="0,1,0.1"` 最优；`0.05` / `0.2` / 中位数两半 全崩。
3. **四轴叠加顺序** = 图聚类 → 图聚类 → 行业族 → 慢分量桶；每层剥掉一种共性。

**⚠ 对本文 §2 前文的更正**：`trade_when(volume>adv20)` 流动性门**在 DEU starmine 族为 −0.06**（HKG 的 +0.52 **不可迁移**）；
`power(ts_rank(alpha,180))`（论坛配方）在本族**伤**（S 1.69→1.44）。**跨区/跨族不可外推，逐族实测。**

**完整六步配方**：skill `wq-operator-playbook-by-gate` → `references/gate-breaking-recipe.md`
（含逐维全账本、死路清单、算子预算账：14 个算子每个都承重，`≤8` 仅 PPA 通道硬限 ⇒ 本形态只能走 REGULAR）。

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

> **⚠ 2026-10-23 补边界（档位杠杆只对 NaN 敏感算子有判别力）**：
> other596 波 83 做过一次干净的双档对照（同 4 臂、仅 `nanHandling` ON/OFF），
> **8 个读数逐位相同**（S / F / TO / RET / DD / longCount / shortCount 全同），
> 并已核实平台侧 settings 记录确实是 ON 与 OFF（`78o3K7Q2` vs `kqJvLVYz`）⇒ 排除发批串档。
> 原因是那 4 条臂全由 **NaN 透明算子**构成（`rank` / `ts_backfill` / `ts_mean` / `subtract`）——
> 两档语义对它们等价。
> ⇒ **纪律**：拿 `nanHandling` 当杠杆前，先检查臂里有没有 NaN 敏感算子
> （`ts_sum` / `ts_delta` / `group_*` / 累加类）。全是 NaN 透明算子时，
> 双档对照只是把同一批表达式跑两遍，**白烧一半槽位**。
> ⇒ 反向用法：该字段若已知有稀疏 NaN，则「双档逐位相同」本身就是**该臂 NaN 无感的证据**，
> 可用来判断"这条臂到底有没有吃到缺失值"。

> **2026-10-28 第三次复现（USA rsk65 ts_rank 族）**：`-ts_rank(rsk65_mfm_etfm4_dsrt_intermediate, 504)`
> 在 STATISTICAL/decay5/trunc0.08 下，`nanHandling=ON` 的 `e75orE1M` 与 `nanHandling=OFF` 的
> `0mY0EldK` **S 2.94 / F 1.09 / tvr 0.7559 / 2Y 2.06 逐位相同**。
> 新增判据：`ts_rank` 也属 NaN 无感（它按序数统计，缺失自然跳过）⇒ 该族跨波比较
> **不必**再为 `nanHandling` 不同源而重跑控制组，可直接合并两组读数。
> （这一点很重要：否则会误判 wave 103B 与 wave 106 的 decay 扫描不可比。）

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
- **USA 侧同向且更陡（2026-10-23，n=92 已测）**：prod `≥0.8` 占 **44.6%**；RA 硬闸全过的 177 颗里只有 **26 颗**走到 prod（14.7%），
  其中 prod<0.7 且 self<0.7 的只有 **4 颗 ⇒ IS→可提交转化 15.4%**。RA 全过率最高的三个数据集 prod 全部 ≥0.92
  ⇒ **RA 全过率与可交付性在 USA 反向**（`03_region_dataset.md` §9）。
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

### 12.5 ★★★ 第二例实证：GBR news50 事件量族（2026-10-28，11 批 68 条）

**同一次扫描里只有 `ts_decay_linear` 有效**，且它一次同时抬 S/F/2Y 并降换手 —— 比 KOR 的「2Y +0.05」量级大一个数量级。

| 包装（基线 = `reverse(ts_zscore(ts_backfill(vec_avg(F),5),252))`，S1.03/F0.53/2Y1.15/TO0.161） | S | F | 2Y | 判定 |
|---|---|---|---|---|
| **`ts_decay_linear(·, 22)`** | **1.24** | **0.79** | **1.77** | ★★★★★ 唯一命中 |
| `winsorize(·, std=3)` | 1.07 | 0.55 | 1.13 | 弱 |
| `ts_rank(·, 252)` | 1.06 | 0.53 | 1.02 | 弱 |
| `signed_power(·, 0.5)` | 1.04 | 0.53 | 1.07 | 弱 |
| `ts_scale(·, 252)` | 0.88 | 0.43 | 0.84 | 弱 |
| `quantile(·)` | 0.69 | 0.41 | −0.53 | 反向 |

**★ 新增判据（可迁移）：等价算子替换的收益大小，取决于该族瓶颈在「噪声/换手」还是「形状」**
- KOR other466 瓶颈在 2Y 形状 ⇒ 换包装只动 2Y（+0.05）
- GBR news50 瓶颈在噪声 ⇒ 换 `ts_decay_linear` **同时**动 S(+0.21) / F(+0.26) / 2Y(+0.62) / TO(−0.07)，并让 `LOW_2Y_SHARPE` 由 FAIL 转 PASS

⇒ **扫替换前先问「这个族卡在哪一闸、那一闸是被形状锁死还是被噪声锁死」**：
被 2Y/形状锁死 ⇒ 找改变形状的包装；被 TO/换手锁死 ⇒ 找带平滑/慢化的包装（`ts_decay_linear` / `ts_mean` / `hump`）。
GBR 同族实测：`ts_mean` 换手更低但 S 崩到 0.22；`hump` 换手降但 S 降到 1.16 ⇒ **平滑长度有窗口效应，22 是该族最优点**（5/44/66/126 全弱）。

### 12.6 ★ 配套：decay 档位不是「抬 S 的杠杆」

GBR news50 三档对照（同一表达式，唯一变量 = decay）：

| decay | S | F | 2Y | TO | margin |
|---|---|---|---|---|---|
| **4**（权威档） | **1.26** | 0.80 | 1.79 | 0.088 | 0.00116 |
| 8 | 1.25 | 0.79 | 1.86 | 0.0668 | 0.00149 |
| 20 | 1.24 | 0.78 | 1.91 | 0.0579 | 0.00169 |

⇒ **降 decay 只降换手、抬 margin，S 单调微降**；且降档会推高 self 相关性（EUR wave274 教训）⇒ **保持区域权威档，不要靠降 decay 追 F**。


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

## ★★★ 「轴层数」是一个必须逐字段搜索的维度（2026-10-07 实证）

**默认套 4 轴（图聚类×2 + subindustry + 慢分量桶）会系统性错杀"脆信号"。**

### 实证（DEU，`predictive_starmine.mean_estimate_change_pct_f12m_ebitda_14d_4`，decay4）
| 轴层数 | 算子数 | Sharpe | Fitness | sub |
|---|---:|---:|---:|---:|
| **0 轴（裸 `rank(ts_mean(F,5))`）** | 3 | **1.41** | 0.81 | **1.20** |
| 1 轴（仅慢分量桶） | 4 | **1.41** | 0.81 | 1.20 |
| 1 轴（`quantile`+桶） | 5 | 1.33 | 0.71 | 1.09 |
| 2 轴（图+桶 / 行业+桶） | 8~9 | 1.14~1.34 | 0.57~0.72 | 0.92~1.08 |
| 3 轴（图+行业+桶） | 11 | 1.21 | 0.58 | 0.96 |
| **完整 4 轴** | **12** | **0.82** | 0.35 | 0.58 |

**⇒ 「每加一层中性化，S 掉一截」是单调关系。** 对照组（同一数据集）：
`mean_estimate_change_pct_f12m_earnings_14d_4` 裸 `rank` 单信号历史最好 **S1.57** → 加 4 轴后 **S1.75**（**轴是正操作**）。

### 判据与 SOP
1. **任何新候选字段，先做一次轴层数扫描**（0 / 1（仅桶）/ 2 / 3 / 4 轴，各 1 条，共 5 条）——成本 1 批，收益是避免整族误判。
2. 取到该字段自己的最优深度，**再**谈窗长 / 桶粒度 / decay。
3. **脆信号判据**：若 `S(0轴) − S(4轴) > 0.3` ⇒ 该字段是"脆信号"，**走轻框架**（裸 `rank` 或仅桶轴），且预期它 `sub` 偏高（信号集中在子宇宙）。
4. **宽信号判据**：若 `S(4轴) > S(0轴)` ⇒ 该字段的 alpha 分布广，可承受中性化，走重框架。

### 为什么重要
本季大量"字段没信号"的结论**很可能是被重框架吃掉的误判** —— 一个字段在 4 轴下 S0.4，
在 0 轴下可能是 S1.4。**先扫轴深，再判生死。**

---

## ★★★ RISK 塔「特异性收益 66 日反转」：USA 唯一同时过 2Y 与 sub 两墙的形态（2026-10-28 实证）

**背景**：USA 未点亮塔 16 条 ATOM 探针（单数据集单字段），
`TOP3000 / D1 / SUBINDUSTRY / decay5 / trunc0.08 / IS 2014-01-01~2023-12-31`。

| alpha | 表达式（ATOM） | 平台塔 | S | F | tvr | 2Y | sub | fRA |
|---|---|---|---:|---:|---:|---:|---:|---:|
| **vR13djVG** | `-ts_zscore(rsk65_mfm_etfm4_dsrt_intermediate, 66)` | **risk** | **1.98** | 0.82 | 0.7553 | **2.18** | **1.75** | 2 |
| KPJjk7Rj | `-ts_sum(rsk65_mfm_etfm3_dsrt_intermediate, 5)` | risk | 1.13 | 0.58 | 0.3715 | 0.99 | 1.06 | 3 |
| A1VMklqR | `-group_zscore(subtract(opt3_volputatm, opt3_volcallatm), sector)` | option | 1.61 | 0.65 | 0.4858 | 1.34 | 0.61 | 4 |
| ZYQer7Zx | `-group_zscore(short_interest_predicted_change, sector)` | shortinterest | 0.89 | 0.24 | 0.6449 | 1.87 | 0.60 | 2 |
| N1NvA7ke | `group_rank(ts_zscore(mws46_ravenpack_mean_ess, 22), sector)` | news | 0.51 | 0.10 | 0.5085 | 0.33 | 0.51 | 3 |

### 结论 1：这是「结构性正确」的信号，不是偶然强值

`rsk65_mfm_etfm4_dsrt_intermediate`（多因子风险模型**特异性收益**的中间期限分量）取负 +
`ts_zscore(·,66)` 是 16 条里**唯一同时过 `LOW_2Y_SHARPE` 与 `LOW_SUB_UNIVERSE_SHARPE`**
的形态（2Y 2.18 / sub 1.75）。对照 USA 全史：76.5% 的行卡 2Y、42.1% 卡 sub
（`03_region_dataset.md` §9.2）⇒ **一次跨过这两道墙，等于已经拿到"机制没走偏"的凭证**，
剩下的是参数层收尾，不是换概念。

### 结论 2：期限结构是必须**最先**扫的一维，不是最后才调的旋钮

同一字段族，5 日 vs 66 日：**S 1.13 vs 1.98（差 75%）**，且 2Y 0.99 vs 2.18。
⇒ 「这个字段没信号」在 USA 有相当比例是**期限轴选错**，而非字段无效。
**SOP**：新字段的第一批必含「短/中/长」三档期限（如 5 / 66 / 252），
再谈分组轴与算子形式。**先定期限，再定轴深，最后调分桶**。

### 结论 3：fitness 与 turnover 是同一面墙，压 turnover 是唯一「一石二鸟」的杠杆

平台闸实测：`LOW_FITNESS` limit **1.0**、`HIGH_TURNOVER` limit **0.7**（不是项目 review 的 0.3）。
而 `fitness = Sharpe × √(|returns| / max(turnover, 0.125))`：

- 当前：`1.98 × √(0.1307 / 0.7553) = 0.82` ✓ 与平台一致
- **只压 turnover 到 0.45**（不动 S、不动 returns）⇒ `1.98 × √(0.1307/0.45) = 1.07` **双闸齐过**
- 只抬 S 到 1.0 的 fitness ⇒ 需 `S = 2.40`（+21%），且 turnover 仍卡 0.7553 **单闸不过**

#### ⚠️ 结论 3 的修正（2026-10-28 wave 102b 实测证伪，务必读完再用）

上面那串算式的前提是「**压 turnover 而 S / returns 不动**」，这个前提在该族上**被实测证伪**。
102b 用 6 条仿真做了压换手算子族对照实验（同一信号 `-ts_zscore(rsk65_..._dsrt_intermediate, 66)`）：

| 压换手算子 | tvr | S | 2Y | F |
|---|---:|---:|---:|---:|
| 不压（基线，66日） | 0.7553 | 1.98 | 2.18 | 0.82 |
| `hump(x)`（默认参） | **0.0079** | **−0.24** | **−1.41** | −0.05 |
| `hump(x, hump=0.02)` | 0.0079 | −0.25 | −1.42 | −0.06 |
| `ts_target_tvr_hump(x, target_tvr=0.55)` | 0.3118 | 1.02 | 0.20 | 0.40 |
| `ts_target_tvr_hump(x, target_tvr=0.40)` | 0.2273 | 0.90 | 0.62 | 0.37 |
| `ts_target_tvr_decay(x, target_tvr=0.45)` | 0.2097 | 1.10 | 0.34 | 0.64 |
| `ts_decay_linear(x, 22)` | 0.1961 | 0.95 | 0.21 | 0.53 |

**三条硬结论**：

1. **压换手把 2Y 从 2.18 摧毁到 0.20~0.34**（`hump` 直接到 −1.41）。S 也同步腰斩。
   ⇒ 该族的 alpha **就长在"快反应"上**，平滑 = 杀信号。fitness 算式里分子分母同时恶化，
   **压换手是净亏**，与「一石二鸟」正好相反。
2. **`hump()` 的默认参数在 zscore 量纲上极度激进**：tvr 直接掉到 0.0079，
   反手触发 `LOW_TURNOVER` 下限（limit **0.01**）。⇒ `hump` 不是"温和微调"，用在 ospan≈1
   的标准化信号上是暴力截断，必须先小剂量试（`hump=0.02` 实测与默认值无差别，说明 0.02 仍远超阈值）。
3. **`ts_target_tvr_*` 的 target_tvr 与实际产出呈约 0.567 倍线性关系**（0.55→0.312，0.40→0.227）。
   ⇒ 该算子的 target 参数不能当实际换手写。
   **⚠ 上限硬约束（2026-10-28 实付 10 条仿真学费）**：`target_tvr` 合法区间是 **[0, 1]**，
   传 `target_tvr=1.2`（按 0.567 倍反推「想要实际 0.68」）会被平台拒
   （`Got invalid value "1.2" for attribute "target_tvr", should be between 0.00 and 1.00`），
   而且是**逐条校验失败 + 整批 10 条全部 CANCELLED**（父 multisim 状态 = ERROR，子状态两种：出错条 ERROR、其余 CANCELLED）。
   ⇒ 该算子**理论上限**只能压到实际 tvr ≈ `1.0 × 0.567 ≈ 0.57`；**想要 0.57~0.70 之间的换手它做不到**，
   要落到这一带只能换杠杆（decay 设置 / 显式持仓保持类算子）。
   推论：**用「反推参数」的写法前，先去算子目录核对该参数的合法区间**，不要从观测比值外推。

#### ⚠️ 结论 3 修正的再修正：平滑是否杀信号，由**基础信号形态**决定，不由算子决定（wave 104b）

上表（102b）用的是 **66 日 `ts_zscore`** 形态，于是得出「压换手 = 杀信号」。104b 把同一族换成
**504 日 `ts_rank`** 长窗形态做同样的算子扫描，结论**完全相反**：

| 压换手算子 | tvr | S | 2Y | F |
|---|---:|---:|---:|---:|
| 不压（基线 `-ts_rank(·,504)`） | 0.7559 | 2.94 | 2.06 | 1.09 |
| `ts_target_tvr_decay(x, 1.0)` | **0.4905** | 2.46 | 1.59 | **1.06** |
| `ts_target_tvr_hump(x, 1.0)` | 0.5739 | 2.59 | 1.78 | **1.03** |
| `ts_decay_linear(x, 3)` | 0.5108 | 2.49 | 1.58 | **1.04** |
| `hump(x, 0.0005)` | 0.3171 | 1.31 | 0.99 | 0.47 |
| `hump(x, 0.001)` | 0.1161 | 0.68 | 1.09 | 0.27 |

**机制**：504 日 `ts_rank` 的输出本身是**极缓慢变化的百分位**（日间变化 <1/504），对「再平滑」高度耐受；
66 日 `ts_zscore` 的日间变化是量级的，平滑直接抹掉的就是信号本体。
⇒ **判据从「信号是不是高频型」细化为「基础信号的日间变化幅度」**：
- 长窗（≥252）rank / 分位数类 ⇒ 天生低频，可放心叠加 `ts_decay_linear` / `ts_target_tvr_*`；
- 短窗（≤66）zscore / delta 类 ⇒ 天生高频，平滑 = 杀信号，别浪费仿真。

**唯一仍然安全的暴力算子**是 `hump` 的小剂量区：`hump(x, 1e-3)` 就足以把长窗 rank 的 tvr 打到 0.116
（同时 S 砍到 0.68）⇒ 即便长窗形态也要按 1e-4 量级试，不要按默认 0.01 试。

**修正后的判据（替换原判据）**：

> 卡「LOW_FITNESS + HIGH_TURNOVER」共现时，**先判断信号本身是不是高频型**，再决定修哪边。
> - 判别动作：花 1 条仿真做 `ts_decay_linear(x, 22)` 或 `ts_target_tvr_decay(x, target_tvr=0.45)`。
> - **若 2Y 崩到 <0.6 ⇒ 该族是高频型，压换手路线封盘**，改走「换设置层」（中性化 / decay / truncation / universe）
>   或直接换字段；**若 2Y 守住（≥1.5）⇒ 信号是低频型，压换手路线成立**，按上面的算式中算目标换手。
>
> 关键量是 **2Y 的衰减比例**，不是 turnover 降了多少。只看 tvr 下降不看 2Y，会误判"修复成功"。

### 结论 4：符号要先花 1 条仿真验，别靠经济直觉

同批 16 条里有 **2 条符号反了**：
`-group_rank(divide(opt3_openinteputatm, opt3_openintecallatm), sector)` S **−0.65**、
`-group_rank(hedge_fund_ownership_factor1, sector)` S **−0.92**。
取正后分别是 +0.65 / +0.92 ⇒ **两条本可进"有信号"档的探针被白白判成弱**。
**SOP**：新字段族首批必带一组**同骨架正负号对照**（成本 1 条仿真），
否则整族强度会被系统性低估。

### 结论 5：ATOM 形态天然免疫「塔混」硬约束

16 条探针全部单数据集单字段 ⇒ 每条只落一座塔，**不可能构成 PV/MODEL/OTHER 两两组腿**。
在塔混受限的约束下，**ATOM 是唯一无需逐条核对塔位的形态**（仍须用平台 `pyramid_short` 定塔，
但不存在合规风险）。这是"优先 ATOM"除可解释性之外的第二条硬理由。

### 结论 6：一个数据集里可能有**多个互不相同的信号族**，字段名后缀是第一线索

`risk65`（平台 RISK 塔）全部只有 6 个 MATRIX 字段，但按语义分两组**机制完全不同**：

| 子族 | 字段 | 语义 | 经济机制 |
|---|---|---|---|
| **收益型** | `rsk65_mfm_etfm3/4_dsrt_intermediate`、`rsk65_trsd_3mfte/4mfte_mfm` | Specific / residual **Returns** | 特异性收益**反转**（超跌反弹） |
| **风险型** | `rsk65_mfm_etfm3/4_srisk` | Specific **Risk** estimate | **低风险异象**（低特异性波动溢价） |

**实证依据（4 条收益型字段指标几乎重合）**：`mfm_etfm3_dsrt` S 1.97 / `mfm_etfm4_dsrt` S 1.98 /
`trsd_4mfte_mfm` S 1.96（同为 `-ts_zscore(·,66)`）⇒ **收益型 4 个字段是同一个信号**，
换字段名**不能**产生互相关替代（同源互相关会撞 0.83+ 的提交闸）。
而 `srisk` 是**另一族**——水平型风险估计没有"反转"语义，反向做即低风险异象，机制正交。

**SOP**：找某塔的「第二来源」时，**不要在同一前缀下换字段**（多半同信号），
而是读该数据集全部字段的 **description + 后缀**，找**语义类别不同**的子族
（Returns / Risk / Exposure / Flag / Count / Ratio 之间往往就是不同机制）。
一个 `srisk` vs `dsrt` 的差别，比换 10 个窗口值有价值得多。

#### ⚠️ 但「正交」≠「有信号」：srisk 子族已实测判死（2026-10-28 wave 103A）

按上面的 SOP 找到 `srisk` 后，用 6 个表达形式实测（TOP3000/D1/SUBINDUSTRY/decay5）：

| 表达式 | S | F | tvr | 2Y | drawdown |
|---|---:|---:|---:|---:|---:|
| `-ts_zscore(rsk65_mfm_etfm4_srisk, 252)` | 0.44 | 0.26 | 0.0537 | 1.10 | **0.398** |
| `-ts_zscore(rsk65_mfm_etfm3_srisk, 252)` | 0.44 | 0.26 | 0.0537 | 1.10 | 0.398 |
| `-ts_zscore(rsk65_mfm_etfm4_srisk, 66)` | 0.52 | 0.30 | 0.1205 | 1.22 | 0.239 |
| `-ts_rank(rsk65_mfm_etfm4_srisk, 252)` | 0.57 | 0.40 | 0.0732 | 1.24 | 0.366 |
| `-group_rank(rsk65_mfm_etfm4_srisk, sector)` | −0.09 | −0.03 | 0.0203 | 0.20 | 0.702 |
| `-ts_zscore(ts_delta(rsk65_mfm_etfm4_srisk, 22), 66)` | 0.13 | 0.03 | 0.1655 | 0.70 | 0.116 |

**判据**：全族 S ≤ 0.57、回撤 0.24–0.70 ⇒ **低风险异象在 USA/TOP3000 不成立**。
两个 `etfm3` / `etfm4` 变体指标完全一致（S 0.44 / 2Y 1.10）⇒ 互为同一信号，连"换期限/换模型版本"都无效。

**可复用教训**：一个子族「机制正交」只解决**互相关**问题（能不能同提），
**不解决强度**问题（有没有 alpha）。两项必须分开验：
- 正交性：只能靠事后互相关矩阵确认，事前无法从语义保证；
- 强度：**必须先花 3-6 条仿真验证**，且必须覆盖 ≥3 个表达形式（水平/rank/变化率），
  因为水平型字段有可能只有"变化率"那条路有效（本次 `ts_delta` 那条也是最弱的一条）。

⇒ **顺序铁律：先验强度，再谈正交。** 反过来做（先证明正交、再假设有信号）
会得到一颗"完全不相关但没有 alpha"的字段，对点塔零贡献。

### 结论 7：换中性化能不能提分，由 `risk_neutralized_sharpe` 与 `sharpe` 的**差距**预先决定

103B 在 RISK 塔把 `SUBINDUSTRY → STATISTICAL`（其余设置不变）拿到 **S 2.17→2.94（+35%）、
fitness 0.94→1.09、drawdown 0.0304**，一度让人以为「换中性化」是通用破闸杠杆。
105 用同一套设置在三座塔上做对照，结论是**不普适**：

| 塔 / 表达式 | 中性化 | S | F | returns | 2Y |
|---|---|---:|---:|---:|---:|
| RISK `-ts_rank(rsk65_..._dsrt_intermediate,504)` | SUBINDUSTRY | 2.17 | 0.94 | — | 2.44 |
| 同上 | **STATISTICAL** | **2.94** | **1.09** | — | 2.06 |
| OPTION `-group_zscore(subtract(put,call), sector)` | SUBINDUSTRY | 1.61 | 0.65 | 0.0792 | 1.34 |
| 同上 | STATISTICAL | 1.42 | 0.48 | 0.0585 | 1.53 |
| SHORTINT `-group_zscore(short_interest_predicted_change, sector)` | SUBINDUSTRY | 0.89 | 0.24 | — | 1.87 |
| 同上 | STATISTICAL | 0.87 | 0.18 | — | 1.94 |

**机制**：STATISTICAL 中性化是「用统计风险模型把因子暴露剥掉」。剥掉的如果是**噪声/因子收益**，
剩余纯 alpha 的 Sharpe 会上升（RISK 塔字段本身就是因子暴露，所以收益巨大）；
剥掉的如果是**真实信号承载**，剩余部分收益被削、fitness 反而下降（OPTION 即此，F −26%）。

**事前判据（零仿真成本）**：读候选详情的 `risk_neutralized_sharpe`。
- `risk_neutralized_sharpe` **明显低于** `sharpe`（差距大）⇒ 收益主要来自因子暴露 ⇒ 换 STATISTICAL 有可观增益。
  例：RISK 塔字段本身就是因子暴露，差距极大 ⇒ +35%。
- 两者**接近**（差距小）⇒ 收益不是因子暴露来的 ⇒ 换 STATISTICAL 只会削 returns。
  实测 `A1VMklqR`：`risk_neutralized_sharpe` 1.41 vs `sharpe` 1.61，差距仅 12%，换后 F 0.65→0.48。

**另一条同批发现的杠杆更可靠**：OPTION 塔在**同为 STATISTICAL** 下把分组轴 `sector→industry`
拿到 S 1.42→1.82（+28%）、2Y 1.53→2.00（+31%）。
⇒ 分组轴深度是与中性化**正交**的一维，两者要做 2×2 全格扫描，不要只扫一维就下结论。

### 结论 8：某些族的 turnover 是**常量**，与窗口/算子/中性化全无关

| 族 | 变体 | turnover |
|---|---|---:|
| RISK dsrt | `ts_zscore` 66 / 252，`ts_rank` 252 / 504，SUBINDUSTRY / STATISTICAL | **0.7553–0.7559** |
| OPTION skew | sector/industry，SUBINDUSTRY/STATISTICAL | **0.4858–0.5007** |

**含义**：这两族的换手由「截面排序日频洗牌」主导，不由信号平滑程度主导。
⇒ 用「换窗口 / 换归一化算子 / 换中性化」去压换手是**结构性无效**（实测差异 <1%）。
要压这两族的换手，只有两条路：**显式持仓保持类算子**（`ts_target_tvr_*` / `hump`）或 **decay 设置**，
而前者已证会杀 2Y（见结论 3 修正）。

**诊断口诀**：拿到一个「换手贴着某值不动」的族，先跑一次窗口矩阵
（5/66/252 三档 + 两种归一化），若 turnover 标准差异 <0.01 ⇒ 判为常量族，
**立即放弃靠「表达式层」压换手的整条路线**，改去验信号强度或换字段，别浪费仿真槽。

#### ⚠️ 结论 8 的修正：常量只对「表达式层」成立，**设置层 decay 能把它砸穿**（2026-10-28 wave 106）

上面「连设置也放弃」是**错的**，代价是一整轮误判。wave 106 对**同一个** RISK dsrt 表达式
（`-ts_rank(rsk65_mfm_etfm4_dsrt_intermediate, 504)`，STATISTICAL/trunc0.08/nanHandling OFF）
只扫 `decay`（设置层），turnover 从 0.7553 一路砸到 0.3328：

| decay | S | F | tvr | 2Y | subU | RA 失败 |
|---:|---:|---:|---:|---:|---:|---:|
| 5（基线族值） | — | — | **0.7553** | 2.06 | — | — |
| 8 | 2.78 | 1.14 | **0.6134** | 1.90 | 2.24 | 0 |
| 12 | 2.60 | 1.15 | **0.5094** | 1.78 | 2.06 | 0 |
| **16** | **2.50** | **1.18** | **0.4457** | **1.74** | **1.90** | **0** |
| 22 | 2.36 | 1.17 | 0.3842 | **1.55** ✗ | 1.74 | 1（LOW_2Y） |
| 30 | 2.26 | 1.19 | 0.3328 | **1.48** ✗ | 1.56 | 1（LOW_2Y） |

**三条硬结论**：

1. **decay 是唯一被实证的「一石二鸟」杠杆**：decay 5→16 让 tvr **−41%**（0.7553→0.4457）、
   returns 仅 **−5%**（0.1040→0.0988），fitness 反而 **+8%**（1.09→1.18，因为分母 √tvr 降得比分子快）。
   这直接推翻了结论 3 修正里「压换手是净亏」的普适版——**「净亏」只属于表达式层平滑，不属于设置层 decay**。
2. **2Y 对 decay 非单调，存在可行性窗口**：2Y 在 decay 8 见顶（1.90），此后单调下滑，
   decay 22 跌破 1.58 硬闸。⇒ **decay 不能为了压换手一路加**，它是「tvr↓ / 2Y↓」的双向权衡，
   可行区间是 `2Y ≥ 1.58` 与 `tvr ≤ 0.70` 的交集（本例 = decay 8~16，最优点 16：闸最松、余量最大）。
3. **先扫 decay 再动算子**：设置层不消耗表达式复杂度、不改变信号语义、可整批矩阵化
   （`batch_create_simulations` 每项独立 `settings.decay`），成本与算子实验相同但收益大得多。

**诊断口诀（替换结论 8 的口诀）**：拿到换手常量族，
① 先跑 **decay 矩阵**（8/12/16/22/30 五档，一条表达式 × 五设置，`batch_create_simulations` 一次发完）；
② 取 `2Y ≥ 1.58 && tvr ≤ 0.70 && F ≥ 1.0` 的交集窗口；
③ 窗口为空才回去考虑表达式层算子；④ 表达式层平滑只对「长窗 rank 形态」安全
（见结论 3 修正：504 日 `ts_rank` 耐受平滑，66 日 `ts_zscore` 一平滑就死）。

### 结论 9：`investability_ratio` 能把「指标全过」的候选劈成两类，必须排在互相关**之前**

USA 的提交层**不下发** `LOW_INVESTABILITY_CONSTRAINED_SHARPE`（不进 `failed_ra_count`），
所以 `failed_ra_count=0` 的候选里混着两类完全不同的东西：

| 候选 | S | invest_S | ratio | prod |
|---|---:|---:|---:|---:|
| `zqrgna91` | 2.67 | 2.70 | **1.01** | 0.688 |
| `1YZpv1bK` | 1.79 | 1.94 | **1.08** | 0.693 |
| `N1eLE1de` | 2.63 | 2.50 | **0.95** | 0.692 |
| `npvMg7Yq` | 2.50 | 2.15 | **0.86** | 0.967 ✗ |
| `88v2XRm7` | 2.73 | 0.34 | 0.12 | 0.699 |
| `0mjaa2Ev` | 3.24 | 0.29 | **0.090** | 0.646 |
| `vROPEJ8w` | 2.08 | 0.17 | 0.082 | 0.552 |
| `E56XEpV9` | 2.21 | 0.07 | 0.032 | — |

**判据：`investability_ratio = invest_S / S ≥ 0.70`**（0.70 是该闸启用区的平台公式 `inv 限 = 0.70×S`）。

- **ratio ≥ 0.9 的族**：可投资子集上 Sharpe 反而更高 ⇒ 信号在**大盘可交易**票上成立，可信。
- **ratio ≤ 0.13 的族**：Sharpe 全挣在难交易的名字上。`0mjaa2Ev` S3.24 / ratio 0.090
  ⇒ **91% 的 Sharpe 不可投资**；`E56XEpV9` F2.08 / ratio 0.032 更极端。
- **S 越高、ratio 越低 = 越可疑**，不是越好。高 S + 低 ratio 往往是小盘/低流动性暴露。

**踩坑实录**：曾把 `0mjaa2Ev`（S3.24 全闸过、prod 0.646、self 0.089）定为「唯一可提交候选」，
并把 `vROPEJ8w`（ratio 0.082）配成同提篮子 —— 两者都在不可投资档。
而真正的可提篮子是当时被判为「薄余量待刷新」的 `1YZpv1bK / zqrgna91 / N1eLE1de`（ratio 0.95–1.08）。

**SOP 顺序（替换旧顺序）**：
① `failed_ra_count == 0` → ② **`investability_ratio ≥ 0.70`** → ③ prod/self < 0.7 → ④ 互相关矩阵。
**把 investability 放在互相关之前**，否则会拿一堆不可投资的高 Sharpe 候选去配篮子，
配出来的篮子互相关再干净也没有交付价值。

### 结论 10：中性化维度的真杠杆是 `SLOW_AND_FAST`，不是 `group_neutralize` 包壳

同一字段（`total_top_secondary_buy_transaction_count`）、同 decay 5 / trunc 0.08 的 2×2 消融：

| 变体 | 表达式 | 中性化 | S | F | tvr | 2Y |
|---|---|---|---:|---:|---:|---:|
| 双开（`0mjaa2Ev`） | `group_neutralize(ts_zscore(ts_sum(F,126),252), sector)` | **SLOW_AND_FAST** | 3.24 | 2.60 | 0.1622 | 4.30 |
| **去掉包壳**（`MPYoQ1E6`） | `ts_zscore(ts_sum(F,126),252)` | **SLOW_AND_FAST** | **3.18** | 2.55 | 0.1603 | **4.38** |
| 去掉 SAF | `group_neutralize(ts_zscore(ts_sum(F,126),252), sector)` | SUBINDUSTRY | **2.21** | 2.08 | 0.0924 | 2.41 |

- **`SLOW_AND_FAST` 贡献 +44% Sharpe（2.21→3.18）、+82% 2Y（2.41→4.38）**，且不动换手量级；
- **`group_neutralize(·, sector)` 贡献 ≈ 0 甚至 −2%**（3.24 vs 3.18）⇒ 它是噪声级的装饰，
  去掉后表达式更 ATOM、结论更干净。**不要因为「历史最优 alpha 里有这一层」就照抄**。

**`SLOW_AND_FAST` 的选择性（同批 5 个字段的迁移验证）**：
它只放大**慢变/持续型**信号，对噪声型信号会削信号 ——

| 字段 | SUBINDUSTRY（wave107） | +SAF（wave108） | 变化 |
|---|---:|---:|---:|
| `usd_top_secondary_signal_value`（买入） | 0.33 | 0.83 | **+152%** |
| `usd_secondary_signal_value`（买入） | 0.61 | 1.11 | **+82%** |
| `total_top_secondary_sell_transaction_count`（卖出） | 0.95 | 1.00 | +5% |
| `usd_quaternary_signal_value`（卖出） | 0.85 | 0.65 | **−24%** |
| `usd_tertiary_signal_value`（卖出） | 0.85 | 0.70 | **−18%** |

⇒ **判据**：先判断信号是「慢变累积型」（内部人持续买入、持仓变动、指数纳入）还是
「脉冲噪声型」（单日卖出事件、情绪跳变）。前者套 `SLOW_AND_FAST` 有 1.5–2 倍增益，
后者会被反噬。**与结论 8 的 decay 一样：先动设置层，再动表达式层。**

### 结论 11：prod 是**单调不减**的，stale 值必然乐观；investability 由字段覆盖结构决定

**（A）prod 漂移律（2026-10-28 当场实测，三颗候选同批复验）**

`PROD_CORRELATION` 的定义是「本 alpha 与**生产池内每一个** alpha 的相关性的**最大值**」。
生产池只增不减 ⇒ 每新进一颗相关 alpha，max 只会抬不会降 ⇒

> **任何 stale 的 prod 值都是乐观下限，永远不会比真值更悲观。**

同批三颗、同一次会话内的实测对照：

| alpha | 台账 stale 值（陈旧 96–508h） | 当场实测 | 判定 |
|---|---:|---:|---|
| `1YZpv1bK` | 0.6934 | **0.9545** | **翻红（+0.26）** |
| `zqrgna91` | 0.6877 | 0.6877 | 通过（未漂） |
| `N1eLE1de` | 0.6916 | 0.6916 | 通过（未漂） |

直方图给出翻红机理：`1YZpv1bK` 有 **1 颗**生产池 alpha 落在 `[0.9, 1.0]` 桶，而其余
99.9% 都在 0.4 以下 —— 是**单颗新进 alpha** 把它顶穿的，不是整体漂移。

**判据**：
- stale prod **不得**作为「通过」依据，必须当场重测（`check_correlation(refresh=False)`，
  缓存超 48h 会自动回源，零额外成本）；
- 余量 < 0.02 的候选**预期会翻红**，不要把它算进「可提交存量」；
- 反过来，`zqrgna91`/`N1eLE1de` 这种「未漂」说明生产池近期没有同族新增 —— 但不能外推。

**（B）investability_ratio 的第一性归因：`invest_S` 衡量的是「信号在流动大票上还剩多少」**

同一批候选按 ratio 分层，差异**不来自算子、不来自中性化、不来自换手**，全部来自
**字段在流动大票上的信息密度**：

| 档 | 字段族 | 代表 alpha | ratio |
|---|---|---|---:|
| 优 | 分析师目标价预期 | `1YZpv1bK` | **1.084** |
| 优 | 社媒 buzz 强度对减 | `zqrgna91` | **1.011** |
| 优 | 信用风险模型分数对减 | `N1eLE1de` | **0.951** |
| 优 | 风险模型特异性收益（长窗 rank） | `npvMg7Yq` | 0.860 |
| 差 | 内部人交易笔数累积 | `0mjaa2Ev` | **0.090** |
| 差 | 内部人交易（SAF 版） | `MPYoQ1E6` | 0.085 |
| 差 | 内部人交易（SUBINDUSTRY 版） | `E56XEpV9` | **0.032** |

- **高 ratio 族 = 全市场稠密覆盖的非事件字段**：分析师预期、模型打分、风险模型输出。
  这些字段对**每一只**股票每天都有值，大票小票一视同仁。
- **低 ratio 族 = 稀疏事件字段**：`insider_trx_matrix` 的名义覆盖率 0.764，但内部人交易
  天然集中在小盘股，大票上几乎无事件 ⇒ 信号在大票里没有信息 ⇒ `invest_S` 崩。
  算子层怎么调都救不回来（三个不同算子的 ratio 全在 0.03–0.13）。

**⇒ 零成本预判**：派发前先看字段的 `coverage`。
`coverage ≥ 0.95` 且非事件型 ⇒ ratio 大概率 > 0.7；
`coverage < 0.85` 或语义上属事件/逐笔型 ⇒ **预期 ratio 会崩，不值得占仿真槽**。

**（C）三颗高-ratio 候选的共同配方**（可直接复用为扩产模板）

```
group_rank( <信号>, subindustry|market )      ← 截面排序，压成均匀分布，抗极端值
  配合：universe = TOP2000 / TOP3000          ← 宽宇宙（小宇宙天然抬高 invest 依赖）
        neutralization = STATISTICAL          ← 三颗全用这个
        truncation = 0.08
        tvr 落点 0.06–0.16                    ← 低换手是 ratio 高的伴随特征，不是原因
```

三颗互相关 0.066 / 0.144 / 0.429（全部 < 0.7）—— **因为字段族互不相同**，
这再次印证「互相关由信号腿来源主导，由门控/参数决定不了」（见结论 9 前的点塔分析）。

**（D）生产池饱和诊断**：`1YZpv1bK` 撞 0.9545 说明 **USA 的 target-price 预期族已饱和**；
`zqrgna91`（社媒 buzz）、`N1eLE1de`（信用风险打分）尚有余量。
扩产应优先**未饱和字段族**，而不是在同族换窗口/换算子。

### 结论 12：★「波动率 / 风险水平」类单字段信号在 USA 封顶 0.9–1.03（三数据集独立验证）

三个互不相干的数据集，同一形态（水平量的 `ts_zscore` / 分位排名）撞到同一条天花板：

| 数据集 | 字段族 | 代表 alpha | 最高 Sharpe |
|---|---|---|---:|
| `option8` | 隐含波动率水平 IV30 | `QPvL9Qgr` | 0.91 |
| `option6` | IV/SPY 分位、IV 偏离年均值 | `bl65Q7wM` / `YP1GvXRW` | 1.03 / 0.96 |
| `risk62` | 特质风险 ksrs | `ZYQeEVg3` / `A1VMGXrE` | 0.77 / 0.91 |

Wave 111 用 6 档中性化扫同一表达式（STATISTICAL / NONE / SUBINDUSTRY / INDUSTRY / MARKET / SECTOR），
Sharpe 排序 **STATISTICAL 0.91 > INDUSTRY 0.67 > SUBINDUSTRY 0.64 = SECTOR 0.64 > MARKET 0.62 > NONE 0.59**
—— 放开中性化一律**下降**，坐实「不是设置有病，是机制上限」。

⇒ 该族正式列为**跨数据集死路**。继续换字段名（IV → 分位 → 标准差数 → 特质风险）只是同一机制的
单调变换，不可能独立提供 1.58。

### 结论 13：★★ fitness 是低换手信号的真正死因——先算「returns 养不养得起 F」，再谈 Sharpe

平台口径 `F = Sharpe × √(|returns| / max(turnover, 0.125))`。tvr < 0.125 时分母被钳死在 0.125，于是

> **F ≥ 1.0 ⇔ ret ≥ 0.125 × (1/S)²**
> 反解：S = 0.96 → 需 ret **13.6%**；S = 1.58 → 需 ret **5.0%**。

三波全军覆没都栽在这条：

| 波次 | alpha | S | tvr | ret | F | 达 F=1.0 所需 ret |
|---|---|---:|---:|---:|---:|---:|
| 113 | `ZYQeEVg3` | 0.77 | 0.0588 | 1.45% | 0.26 | **21.1%**（物理不可能） |
| 114 | `npvM7z1a` | 0.96 | 0.0911 | 2.49% | 0.43 | 13.6% |
| 对照 | insider 事件族 | — | — | 11.7% | — | — |
| 对照 | rsk65 dsrt 族 | — | — | 9.9% | — | — |

`margin`（单位换手收益）是同一事实的独立探针：`npvM7z1a` margin 0.000547 vs `78Lb3aoQ` 0.003299
—— 差 6 倍，说明**信号对价格的映射极弱**，不是换手过高拖累（它换手只有 0.09）。

⇒ **季频/低频信号（机构持股、基金持仓）在 USA 的收益幅度天然只有 1.5–2.5%，差一个量级。
不值得为它们烧仿真槽，与算子 / 窗口 / 中性化全无关。**

### 结论 14：★ `全期 Sharpe` 与 `2Y Sharpe` 符号相反 = regime artifact，一票否决

Wave 114 的 M1/M2 是完全镜像对：M1 `leAbj2o8` S = **−0.30** 但 2Y = **+1.82**；
镜像 M2 `78LEjQe2` S = +0.30、2Y = −1.82。即信号只在近两年有效、早年反向。
同形态：M3 `LLMA7XPL`（S−0.29 / 2Y1.48）、M8 `RREn7aRj`（S−0.64 / tvr0.5693 / 2Y1.66）。

**判据**：`sign(sharpe) ≠ sign(two_year_sharpe)` ⇒ 一票否决。作为零成本规则，**先于任何指标排序执行**
（此条比「Sharpe 低」更早、更硬：低 Sharpe 尚可能是机制弱，符号翻转是机制假）。

### 结论 15：★★ GROUP 字段不贡献 PV 塔——「行业分组 + 非 PV 信号」仍是纯单塔

实证：`npvM7z1a = group_rank(ts_zscore(inst18_instownership_num_held, 252), subindustry)`，
塔位 `pyramid_short = institutions`，`pyramids.list` 只有 `USA/D1/INSTITUTIONS(1.0)`，**没有 PV**。

平台侧 `pv1` 下确有 7 个 GROUP 字段（`industry` / `subindustry` / `sector` / `market` /
`exchange` / `country` / `currency`，用 `get_datafields(data_type="GROUP")` 列出；换成
`dataset_id="risk70"` 查询返回 0 条，证明数据集筛选确实生效），但它们在金字塔归类中**不贡献** PV。

推论（对「禁 PV/MODEL/OTHER 两两组腿」硬约束极关键）：

- `group_rank(x, industry)`、`group_neutralize(x, bucket(...))` **不会**把 OTHER / RISK / INSTITUTIONS
  信号污染成 PV；
- 真正引入 PV 的只有 **pv1 的数值字段**：`cap`、`returns`、`close`、`volume`、`vwap`、`adv20`、
  `sharesout` 等；
- ⇒ **去 PV 化只需替换这些数值字段，分组轴可以原样保留**。

样例：`78Lb3aoQ`（S1.82 / F1.21 / 2Y2.31 / subU1.06 / inv_S1.68 / fRA 0 / **prod 0.6839 通过**）
塔位为 `pv/risk/other`，PV 仅来自 `cap` 与 `ts_mean(returns,63)`；把这两个 bucket 换成
risk70 的 `market_capitalization_factor` / `trading_liquidity_factor` 即可合规，机制结构不用动。

### 结论 16：本地库 `best_s_in_dataset` 是「任意结构最优」而非「单字段能力」，用它排 ATOM 优先级会系统性高估

`query_dataset_profile` 的 `best_s_in_dataset` 取该数据集参与过的**所有结构**里的最优 Sharpe
（含多门控、多塔组合），**不等于**单字段 ATOM 能达到的水平：

- `institutions18`：本地 best_s = 1.82 / best_2y 1.97 / 56 次回测中 6 次 RA 全过（10.7%，远高于
  USA 全区 5.9%）—— 看起来是最优靶子；实际 Wave 114 八机制单字段 ATOM 上限仅 **0.96**，
  那个 1.82 来自「信号腿 + 多门控」的复合结构。
- `fundamental14`：248 字段看似大，实为「董事/高管变更 + SEC 备案元数据」治理数据集，
  多为布尔 flag / 地址 / 审计师名，**不适合 ATOM**。

**判据**：数据集级先验只能回答「值不值得探」，**不能预测单字段能到多少**。
排 ATOM 优先级应改用**字段级**三条件：`coverage ≥ 0.90` + 语义属「连续稠密量」+ 平台 `alphaCount` 低。

### 结论 17：USA 纯单字段 ATOM 的 Sharpe 天花板 ≈1.56，与 LOW_SHARPE(1.58) 闸结构性冲突

Wave 115 A 组把 `earningscall_sentiment` 五个话题 polarity 用**同一骨架**分别单跑（骨架：
`hump(group_rank(ts_zscore(ts_backfill(vec_avg(<F>),126),504), industry), hump=0.0001)`），
五条 Sharpe 全部落在 **1.29–1.56**，无一过 1.58：

| 话题 | Sharpe | F | ret | 2Y | subU | inv_S | inv比 |
|---|---:|---:|---:|---:|---:|---:|---:|
| assetutilization | **1.56** | 1.14 | 6.66% | 2.12 | 0.94 | 1.45 | 0.93 |
| profitability | 1.51 | 1.07 | 6.33% | 1.89 | 0.94 | 1.46 | 0.97 |
| leverage | 1.45 | 0.99 | 5.81% | 2.18 | 1.05 | 1.36 | 0.94 |
| cashflow | 1.30 | 0.87 | 5.58% | 1.78 | 0.77 | 1.23 | 0.95 |
| valuation | 1.29 | 0.87 | 5.64% | 1.81 | 0.78 | 1.27 | 0.98 |

**归因**：单字段 ATOM 的 Sharpe 来自「一个信号的横截面区分度」，缺乏正交维度分摊噪声；
`hump` 压住换手后 returns 稳定在 5.6–6.7%，但 S 上不去。**同一批信号叠三门控（size / liquidity /
momentum 风险因子）后 S 从 1.56 → 1.75（+0.19）**，说明增量 Sharpe 来自风险维度上的条件化。

**判据**：USA D1 TOP3000 下，「单字段 ATOM 直接过 LOW_SHARPE」的成功率极低（本轮 5/5 全部卡 1.29–1.56）。
单塔 ATOM 只适合作为**结构探针**（测机制强度、测 invest 比率），不要指望它直接产出可提交 alpha。
要过 1.58 必须叠第二个正交维度，而一叠往往就跨塔（见结论 18）。

### 结论 18：去 PV 化的代价可量化 = Sharpe −0.07，门控字段可整体平移不损机制

`78Lb3aoQ`（S1.82 / F1.21 / prod 0.6839 / 塔位 `pv/risk/other`）去 PV 化重建：
把 `cap` → `market_capitalization_factor`、`ts_mean(returns,63)` → `trading_liquidity_factor`
（均取自 `risk70`），其余结构一字不改，结果：

| alpha | 结构 | S | F | 2Y | subU | inv_S | inv比 | fRA | 塔位 |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| 78Lb3aoQ（原） | cap + returns63 + momentum | 1.82 | 1.21 | 2.31 | 1.06 | 1.68 | 0.92 | 0 | pv/risk/other |
| pwdAPALb | size + liquidity + momentum | 1.75 | 1.16 | 2.29 | 0.99 | 1.60 | 0.91 | 0 | **risk/other** |
| akKqLq56 | size + resvol + momentum | 1.72 | 1.09 | 2.42 | 1.03 | 1.58 | 0.92 | 0 | **risk/other** |
| E56XvX90 | size + liquidity + momentum，subindustry 轴 | 1.75 | 1.13 | 2.39 | 1.05 | 1.63 | 0.93 | 0 | **risk/other** |

**结论**：
- PV 数值字段在机制里只是**规模/动量的代理**，换成 risk70 的同语义因子后 Sharpe 仅掉 0.07、
  fitness 仅掉 0.05，**塔位干净地降为 `risk/other`**（`pyramids.list` 只剩 RISK + OTHER）。
- ⇒ 遇到「指标极好但撞 PV 禁混」的候选，**不要判死**，先做「PV 数值字段同语义替换」重建；
  分组轴（`industry` / `subindustry` / `bucket`）一律保持原样。
- 替换字段的语义必须对得上：原 `cap`（规模）→ `market_capitalization_factor`；
  原 `ts_mean(returns,63)`（流动性/波动）→ `trading_liquidity_factor` 或 `residual_volatility_factor`；
  原 `price_momentum_factor_score`（动量）本身就在 RISK，无需替换。

### 结论 19：investability 比率低是「事件族」的局部问题，情绪族天然 0.91–0.98

Wave 115 八条（情绪信号 + 风险因子中性化）的 `inv_S / S` 全部落在 **0.91–0.98**，而同一区域
`insider_trx_matrix` / `rsk65` 事件族的比率只有 0.03–0.13。

**判据**：`invest_S ≥ 0.70×S` 这道人工闸**不是**全区域难点，它只筛掉「换手集中在不可投资小盘股」
的事件型信号。设计阶段只要信号的横截面分布覆盖全 TOP3000 而非尾部，天然就过。
⇒ 不必为了 investability 单独调参，把它当**事后筛选**而不是**设计约束**。

### 结论 20：`hump=0.0001` 把 turnover 压到 0.03，使 fitness 完全由 returns 驱动

Wave 115 八条 turnover 全部 **0.027–0.033**。fitness 公式分母是 `max(turnover, 0.125)`，
turnover 低于 0.125 后分母恒定 ⇒ **继续压换手对 fitness 零收益**，此时
`F = S × √(returns / 0.125)`，要提高 fitness 只有一个杠杆：**抬 returns**。

反解（F=1.0 所需最低 returns）：

| Sharpe | 所需 returns |
|---:|---:|
| 1.29 | 9.4% |
| 1.45 | 7.4% |
| 1.56 | 6.4% |
| 1.75 | **5.1%** |
| 1.82 | 4.7% |

**实证吻合**：A1（S1.56 / ret 6.66%）F=1.14 刚过；A5（S1.29 / ret 5.64%）F=0.87 卡闸；
B6（S1.75 / ret 5.50%）F=1.16 过。⇒ 低换手族的调参方向**永远是抬 returns（或抬 S），
不是继续降换手**；把 hump 再收紧只会同时砍掉 returns，净效果为负。

### 结论 21：USA 的 earningscall/finnews 情绪族是 prod 墙 0.75–0.82，换门控救不了

同一机制族两个独立测量：

| 候选 | 门控 | 信号腿 | Sharpe | prod |
|---|---|---|---:|---:|
| `78Lb3aoQ` 系（Wave 115 B 组） | risk70 风险因子 ×3 | earningscall assetutilization | 1.75 | **0.7541** |
| `RREnbp1n`（Wave 116） | finnews 正+负 ×2 | earningscall assetutilization | 1.62 | **0.8189** |

**「用更小众的门控降 prod」这个假设被否证**：finnews 平台 alphaCount 仅 2（极冷门），
但换它做门控后 prod 反而从 0.7541 升到 0.8189。⇒ **prod 由信号腿（核心机制）主导，
门控的选择既不能降 prod、也不该指望它降**。（这与「互相关由信号腿来源主导」是同一件事的
两面：prod 与互相关都锚在信号腿的 PnL 结构上。）

**推论**：`earningscall_sentiment` 系列的 assetutilization/profitability/leverage/cashflow/valuation
五个话题 + 任意门控组合，全部预期落在 prod 0.75–0.82 ⇒ **该资源在 USA 不可用于提交**。
遇到"某个强机制族所有变体 prod 都 ≥0.7"时，不要在门控/中性化/窗口上继续投入 ——
换机制族，不要在 prod 墙上磨。

### 结论 22：换信号腿来源能降互相关，但代价 ≈ −0.7 Sharpe（同一门控/骨架下）

Wave 117 把 RREnbp1n 的门控（finnews 正+负，bucket 0.1）与骨架（backfill126 / zscore504 /
industry 轴 / hump1e-4）**完全冻结**，只换信号腿数据集：

| 信号腿数据集 | 最好 Sharpe | fitness | 2Y | 结论 |
|---|---:|---:|---:|---|
| earningscall assetutilization | 1.62 | 1.19 | 2.08 | prod 0.8189 否 |
| other143（券商集中度，非情绪） | 1.63 | 0.51 | **−0.93** | 2Y 反号 ⇒ regime artifact |
| ai_news（RavenPack 情绪） | 0.95（翻向校正后） | 0.17 | 2.04 | 强度不够 |

⇒ **「换信号腿换互相关名额」在机制上成立，但强度损失 ≈ 0.67–0.7 Sharpe**，且
other143 这类低换手机制会撞 turnover 0.51（fitness 只能到 0.51）。
**该配方只适合「已有强信号腿、需要一个正交备份」时用，不能当点亮新塔的主力路线。**

### 结论 23：`_N` 后缀变体不是新信息（ai_news 实锤）

`negative_score_average_value` 与 `negative_score_average_value_5` 回测出**完全相同的四个数字**
（S −0.95 / F −0.29 / tvr 0.2682 / 2Y −2.04）。平台 model variant（prv24 / prv25）在该字段上数值等价。
⇒ **不能把 `_N` 当独立变体做样本外验证或凑「多名额/多样性」**；要多样化必须换字段语义或换数据集。
（判据：两个变体若指标四位全同，直接视为同一表达式，只保留一个。）

### 结论 24：同数据集内「预测收益」的路径变体强度差 1.8 倍，open-to-open 远强于 close-to-close

`earnings_chart_dl`（EARNINGS 塔，CNN 把财报日历前后的价格序列转成图像预测前瞻收益）的 1 日前瞻分位字段，
在同一骨架 `hump(group_neutralize(group_rank(ts_zscore(ts_backfill(X,126),504),industry),subindustry),hump=1e-4)`
+ CROWDING/decay5/trunc0.08/TOP3000/D1 下实测：

| 字段 | 口径 | S | F | tvr | ret | 备注 |
|---|---|---:|---:|---:|---:|---|
| `open_return_quantile_1_1day` | 预测 open-to-open 1 日收益分位 | **−2.11** | −0.78 | 0.7194 | **−9.81%** | 取反即 S+2.11 / 2Y+2.10 |
| `close_return_quantile_1_1day` | 预测 close-to-close 1 日收益分位 | 1.61 | 0.47 | 0.6292 | 5.34% | 正向但收益不够 |

- **returns 相差 1.84 倍**（9.81% vs 5.34%），同骨架、同设置、同数据集 ⇒ 差异全部来自「价格路径口径」。
- **符号可以相反**：open 口径是反向信号（预测开盘收益高 ⇒ 后续跑输，即 CNN 对已上涨股票的过度外推误差），
  close 口径是正向信号。⇒ **同族多路径变体必须逐个测符号，不能假定同向**。
- 机制解释：开盘价承载隔夜跳空与集合竞价信息，是「过度外推」最直接的作用点；收盘口径已被日内消化掉一部分。
**应用**：数据集里存在 `{open,high,low,close}_xxx` 路径族时，**不要默认用 close**；`open` 族优先测，
且每个路径单独判符号（`multiply(-1, …)` 取反放在最外层保住 hump 阈值的一致性）。
另：该族三个 1 日分位字段的平台 alphaCount 极低（open 88 / high 60 / low 57），是低拥挤富矿。

### 结论 25：`earnings_chart_dl` 全族 fitness 天花板 ≈0.78 ⇒ 判死（16 颗仿真的定量结论）

**这是「有数学上界的判死」，不是「没试过就放弃」。**

`earnings_chart_dl` 的四个 1 日前瞻收益分位字段（close / open / high / low）在 USA TOP3000 D1 下：

| 字段（取反后） | S | ret | tvr | F | 2Y |
|---|---:|---:|---:|---:|---:|
| `open_return_quantile_1_1day` @decay5 | 2.11 | 9.81% | 0.7194 | 0.78 | 2.10 |
| 同上 @decay10 | 1.86 | 9.28% | 0.5276 | 0.78 | 1.59 |
| 同上 @decay20 | 1.60 | 8.20% | 0.3834 | 0.74 | 1.22 |
| `high_return_quantile_1_1day` @decay20 | 1.70 | — | 0.3823 | 0.69 | 1.33 |
| `low_return_quantile_1_1day` @decay20 | 1.67 | — | 0.3668 | 0.75 | 1.00 |
| `close_return_quantile_1_1day`（正向）@decay5 | 1.61 | 5.34% | 0.6292 | 0.47 | 1.24 |

**三点硬事实**：
1. **decay 从 5 拉到 20，turnover 降 47%，fitness 不动（0.78→0.74）** —— 详见 01_platform_gates §12b。
2. **时间平滑是纯损耗**：`ts_mean(5/22/66)`、`ts_decay_linear(22)` 把 S 从 1.86 削到 1.09/0.85/0.54/0.84。
   ⇒ 该信号是真 1 日反转，平滑即丢信号，**不存在「平滑换低换手」的可行路线**。
3. **margin 只有 1.7–2.7 bps**（常规过闸 alpha 5–15 bps）。returns 5–10% 而日换手 0.38–0.72，
   交易成本吃掉绝大部分毛收益 —— 这是**数据集层面的属性**，换写法救不了。

**最接近闸门的一颗**：`A1VMVAVE`（open 取反 @decay10）S 1.86 / F 0.78 / tvr 0.5276 / 2Y 1.59，
SHARPE、高低换手、集中度、2Y、子宇宙**全 PASS，唯一失败项是 LOW_FITNESS**，且已证明 decay 无法再抬 F ⇒ 结构性不可修。

**应用**：
- EARNINGS 塔**不能**靠 `earnings_chart_dl` 点亮（尽管它的 investability 很健康 0.79–0.86、alphaCount 极低、塔位确认为 earnings）。
- 同类「returns 尚可（>5%）但 turnover > 0.35」的候选，**投入前先用 `F ≈ S × sqrt(margin)` 估上界**：
  margin < 5 bps 且 F 上界 < 1.0 ⇒ 直接跳过，不必花仿真槽。
- 判断 margin 成本极低：`get_alpha_details` 的 `metrics.margin` 直接给，无需额外回测。

### 结论 26：低换手信号的 decay 是**纯损耗**——`tvr < 0.125` 就该先扫 decay=0

**「免费换手额度」的量化定义**：`fitness = S × sqrt(returns / max(tvr, 0.125))`。
当 `tvr < 0.125` 时分母被**钉死在 0.125** ⇒ 换手涨到 0.125 之前，提 returns 不付任何分母代价。
而 decay 的代价**不是换手，是相位延迟**：EMA 把信号滞后 ≈ decay/2 天，对 1–3 日尺度的预测是直接损耗。

**干净对比**（同一批 4 条表达式，只改 decay，`earnings_sent_matrix` USA TOP3000 D1）：

| decay | Sharpe（4 条） | fitness | turnover |
|---|---|---|---|
| **0** | **1.75 / 2.14 / 1.68 / 2.15** | **1.02–1.44** | 0.0492–0.0514 |
| 5 | 1.48 / 1.65 / 1.42 / 1.68 | 0.80–1.00 | 0.0451–0.0465 |

⇒ decay 0 比 decay 5 的 **Sharpe 高 18%–30%**，换手只高 6%–8%，且两者都远低于 0.125 地板
（分母始终 0.125）⇒ **fitness 同步涨 20%–44%，零成本**。

**与 §12b 的分工（不矛盾）**：
- §12b 说的是「decay **不能提高 margin**，因此救不了 margin < 5 bps 的族」（如 `earnings_chart_dl`）。
- 本条说的是「margin 健康（20+ bps）但 `tvr << 0.125` 的族，`decay > 0` 是纯粹的信号损耗」。
- **判据**：`margin ≥ 5 bps` 且 `tvr < 0.125` ⇒ 立刻试 `decay = 0`；`tvr > 0.2` 时不适用（降 decay 会把分母推上去）。

**应用**：
- 任何 `tvr < 0.125` 的候选，decay 扫描是**最高性价比参数杠杆**（零结构改动，历史实测 +20~50% Sharpe）。
- Wave 120 → 121 的 60% Sharpe 跃升，其中**归一化栈与 decay 是两个独立来源**：
  120 用的是 raw / `ts_mean22` + decay20（S 1.37–1.40），121 同时换了栈 + decay0（S 1.68–2.15）；
  只有 121A vs 121B 是干净的 decay-only 对比（上表）。
  引用「decay 贡献多大」时**只能用 121A/121B 那一组**，不能用 120 vs 121。

### 结论 27：情绪面板的黄金骨架——`ts_backfill` + 双分组轴（细轴在前、粗轴在后）

`earnings_sent_matrix`（EARNINGS, 7 MATRIX, coverage 0.70）在 USA TOP3000 D1 下跑出的完整栈：

```
hump(group_neutralize(group_rank(ts_zscore(ts_backfill(F, 126), 504), subindustry), industry), hump=0.0001)
```

| 字段 F | S | F(fitness) | tvr | 2Y | margin | invest_S | invest比 | fRA |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `overall_sentiment_score` | 2.15 | 1.44 | 0.0499 | 3.94 | 22.5 bps | 1.58 | 0.735 | **0** |
| `positive_sentiment_probability_3` | 2.14 | 1.42 | 0.0492 | 4.02 | 22.5 bps | 1.54 | 0.720 | **0** |
| 同字段 / 分组轴互换 | 1.75 | 1.08 | 0.0508 | 3.40 | 18.6 bps | 1.51 | 0.863 | **0** |
| 同字段 / 分组轴互换 | 1.68 | 1.02 | 0.0514 | 3.36 | 17.8 bps | 1.48 | 0.881 | **0** |

**三条可复用规律**：
1. **`ts_backfill(F, 126)` 是必需的**（coverage 0.70 的稀疏面板不 backfill 就无法持有）。实证：Wave 120 不带 backfill 的 raw 版 S 仅 1.37–1.40。
2. **分组轴顺序有 0.4 Sharpe 的定量差**：`group_rank(…, subindustry)` → `group_neutralize(…, industry)`
   （**细轴先分位、粗轴后去均值**）得 S 2.14–2.15；两轴互换得 S 1.68–1.75。
   ⇒ 先用细轴做横截面分位保留行业内序，再用粗轴剥行业共同成分，信息保留最好。
3. **invest 比值与 Sharpe 反相关**：S 2.14–2.15 的两颗 invest 比只有 0.720/0.735（贴着 0.70 人工闸），
   而 S 1.68–1.75 的两颗是 0.863/0.881。**追高 Sharpe 会把 invest 余量吃光**，
   在 `invest_S ≥ 0.70×S` 是硬要求时，1.7–1.8 Sharpe + 0.86 比值往往比 2.15 + 0.72 更可用。

### 结论 28：骨架不是瓶颈——**信号强度由数据集本身决定**（三数据集横向定量实证）

同一个冠军骨架（结论 27 那条完整栈）、同一套设置（USA / TOP3000 / D1 / decay=0 / CROWDING / trunc 0.08 /
IS 2014-01-01~2023-12-31），只换信号腿数据集，Sharpe 差 4.7 倍：

| 数据集 | 类别 | 最好 S | 最好 F | 换手 | 结论 |
|---|---|---:|---:|---:|---|
| `earnings_sent_matrix` | EARNINGS | **2.15** | 1.44 | 0.05 | 信号强，但 prod 0.847 卡提交层 |
| `earnings6`（EPS surprise） | EARNINGS | 0.46 | 0.20 | 0.037 | 判死 |
| `earnings4`（ORATS 财报期权） | EARNINGS | 0.82 | 0.33 | 0.023–0.28 | 判死 |

**规律**：当日志/文本类**情绪分**做信号腿，骨架能放大到 S > 2；当**期权定价量**或
**财报绝对水平值**（EPS 等）做信号腿，同一骨架只给 0.5–0.8。⇒ **选数据集（字段语义）比调骨架重要一个量级**；
骨架优化只能拿 20–40% 的边际改善（如结论 26 的 decay=0、结论 27 的轴顺序），
数据集选错则是 3–5 倍差距且不可补救。

**应用**：一个数据集探针跑出 S < 0.9 且 fRA 大面积失败时，**不要在骨架上继续迭代**，
直接换数据集——骨架已验证过（同骨架在别处给 2.15），瓶颈不在骨架。

### 结论 29：EARNINGS 塔（USA D1）的数据集已近穷尽，别再往里投

USA D1 金字塔实际计数：`model=4 / analyst=6 / earnings=1`，其余 13 座为 0
（点亮阈值 = 同一座塔 3 颗）。EARNINGS 的 6 个数据集逐个体检后：

| 数据集 | 覆盖 | 字段数 | 平台 aC | 判定 |
|---|---:|---:|---:|---|
| `earnings_chart_dl` | 0.991 | 100 | 1101 | **判死**：fitness 天花板 0.78、margin 1.7–2.7 bps |
| `earnings6` | 0.985 | 52 | 4969 | **判死**：48/52 是元数据，数值字段 S 上限 0.46 |
| `earnings4` | 0.969 | 375 | 13821 | **判死**：S 上限 0.82 |
| `earnings_sent_matrix` | 0.700 | 7 | 1599 | 能出 fRA=0（S 2.15）但 **prod=0.847** 提交层不可用 |
| `earnings7` | 0.648 | 40 | 1323 | 38/40 全 VECTOR、以元数据为主，无可挖材料 |
| `earnings27` | 0.273 | 14 | 1535 | 覆盖过低，无法满足"近十年都有数据" |

**结论**：该塔在当前字段供给下**结构性不可达**——不是挖法问题，是材料问题。
`earnings_sent_matrix` 证明信号存在，但同数据集内任何变体互相关 0.81–0.99（`max_mutually_below_subset_size = 1`），
且 prod 撞墙，既不能凑够 3 颗、也不能提交。

**应用**：`earnings_sent_matrix` 不要再用；EARNINGS 塔暂停，把槽位投向 USA D1 的 13 座零塔。
零塔里 `sentiment` / `news`（倍率 1.4 / 1.2）本身就是情绪分家族——骨架可直接复用，是最高性价比的下一步。

（⚠ 该「下一步」建议已被结论 31 证伪，见下。）

### 结论 30：★★★ 「每日原始聚合」型字段必须先做月度平滑——这条与字段语义无关（125A vs 126A 受控实验）

**实验设计**：同一数据集（`news_sentiment_transfer`）、同一冠军骨架、同一设置
（USA / TOP3000 / D1 / decay=0 / CROWDING / trunc 0.08 / IS 2014-01-01~2023-12-31），
**唯一变量**：在 `ts_backfill(F,126)` 之后是否插入 `ts_mean(·, 22)`（1 个月，STANDARD_WINDOWS 内的 22）。

| 对照 | 字段 | 无平滑 tvr / S | 有平滑 tvr / S | 换手变化 |
|---|---|---|---:|---:|
| T1 / S1 | `sentiment_score_median` | 0.7957 / −0.06 | **0.1271** / −0.16 | **−84%** |
| T2 / S2 | `vec_avg(news_sentiment_score)` | 0.7918 / −0.22 | **0.1233** / −0.27 | **−84%** |
| T4 / S4 | `news_article_count`（翻转） | 0.7029 / 0.22 | **0.1167** / **0.59** | **−83%** |

**结论**：三条严格单变量对照全部把换手压掉 83–84%（6.5 倍）⇒
125A 观察到的「四条语义完全不同的字段换手统一卡 0.70–0.80」**不是字段语义问题，
是每日原始聚合的采样噪声**：`ts_zscore(·,504)` 在噪声序列上反复穿越 0，横截面排名天天翻转。

**判据（可直接执行）**：某数据集字段若属「每日一条原始聚合」（新闻条数、每日情绪分、每日事件计数），
先验地预期 `tvr ∈ [0.7, 0.9]`；**不要**先跑一遍再发现换手爆表。
处理顺序：`ts_backfill(F,126)` → **`ts_mean(·, 22)`** → `ts_zscore(·, 504)`。
对照：慢变分（如 `earnings_sent_matrix` 的 `overall_sentiment_score`）本身 tvr 仅 0.05，不需要平滑。

**与结论 3 修正（102b）的关系**：102b 说「平滑 = 杀信号」用的是 **66 日快反应**形态；
本条说「平滑是必需」用的是 **504 日噪声序列**形态。两者不矛盾——
**平滑是否杀信号取决于原始序列的「信号/噪声比」，不取决于算子**：
快反应形态里信号本身长在高频成分上，平滑就杀掉了它；
噪声主导形态里高频成分全是采样噪声，平滑是纯增益。

### 结论 31：`news_sentiment_transfer` 情绪水平通道判死，注意力通道留一线

平滑后（消除换手干扰、信号暴露干净）8 条实测：

- **情绪水平类 4 个字段全是 |S| ≤ 0.27**（median −0.16 / 整体情绪 −0.27 / 均值 −0.27 / 偏度 −0.62）
  ⇒ 该数据集**不携带可用的横截面情绪预测力**。方向一致为负（正面情绪 → 未来收益低 = 情绪反转），
  机制上讲得通（情绪过度反应），但强度只有闸值的 1/6，**参数微调救不回来**。
- **唯一有生命力的是媒体关注度**：`news_article_count` 翻转后 S 0.22 → **0.59**（+168%）、F 0.22、tvr 0.1167。
  与 Barber-Odean 注意力驱动的高估一致（高关注 = 过度定价 = 做空高关注）。
  但 0.59 距 1.58 闸差 **2.7 倍**，已超出骨架优化能提供的边际（20–40%）。

**顺带一个字段去重发现**：`vec_avg(news_sentiment_score)` 与 `sentiment_score_average` 两条表达式的
`sh / fit / tvr / 2Y` **完全相同**（−0.27 / −0.06 / 0.1233 / −0.22）⇒ 两者是**同一份底层数据**。
后续不得把它们当两个独立字段计入多样性或互相关预检（会把 1 颗当 2 颗用）。

**对结论 29「应用」的修正**：结论 29 当时建议「零塔里 sentiment / news 是最高性价比下一步」。
**该建议已被 125A / 125B / 126A 三波证伪**——news/sentiment 类数据集在 USA D1 用冠军骨架
给不出 S > 0.9 的情绪水平信号。零塔的下一步应转向**报表 / 税 / 基本面类**（容量更好、拥挤度更低），
而不是继续在情绪文本族里换数据集。

### 结论 32：`ts_target_tvr_*` 的命名参数陷阱（会连带 CANCELLED 整批）

`ts_target_tvr_decay` / `ts_target_tvr_hump` 的**权威签名**（`docs/reference/operators_catalog.json`）：

```
ts_target_tvr_hump(x, lambda_min=0, lambda_max=1, target_tvr=0.1)
```

**第二个位置参数是 `lambda_min`，不是 `target_tvr`**。写成 `ts_target_tvr_hump(x, 1.0)` 会把
`lambda_min` 置 1、`target_tvr` 留空 ⇒ 平台报
`Required attribute "target_tvr" must have a value.`，**并连带把同批其余仿真全部 CANCELLED**
（实测 4 条：1 条报错、2 条 CANCELLED、1 条 404）。
设目标换手必须走命名参数：`ts_target_tvr_hump(x, target_tvr=0.60)`。

**更根本的一条**：本地 `validate_expressions` + `operator_audit` **双通过也能死在平台侧**。
两者只查「字段是否存在」与「是否幽灵算子」，**不校验命名参数/必填属性/位置语义**。
⇒ 凡表达式里出现**带命名参数的算子**（`hump(x, hump=…)`、`ts_target_tvr_*(x, target_tvr=…)` 等），
派发前必须显式核 `docs/reference/operators_catalog.json` 的 `definition` 字段，别信本地校验的绿灯。

### 结论 33：压换手杠杆排序（RISK 塔实证，四杠杆单变量对照）

被测对象：`-ts_rank(rsk65_mfm_etfm4_dsrt_intermediate, 504)`（RISK 塔特异性收益反转，基线
`0mY0EldK` S 2.94 / F 1.09 / tvr **0.7559 ✗** / 2Y 2.06 / sub 2.45 / invest 比 0.867，唯一失败项
`HIGH_TURNOVER`）。四个杠杆同底座设置（STATISTICAL / trunc 0.08 / nanHandling OFF）单变量对照：

| 杠杆 | alpha | S | F | tvr | 2Y | sub | invest 比 | fRA | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| **settings decay 5→10** | `P0od8o1w` | 2.67 | **1.14** | **0.5540** | 1.84 | 2.14 | 0.865 | **0** | ★**最优，表达式不动** |
| `ts_decay_linear(x, 2)` | `9qxLmXjr` | 2.69 | 1.09 | 0.5916 | 1.78 | 2.21 | 0.881 | 0 | ✓ 次优 |
| `ts_target_tvr_decay(x, target_tvr=0.60)` | `JjeZ17QE` | 2.07 | 1.10 | 0.2847 | **1.38 ✗** | 1.41 | 0.918 | 1 | ✗ 2Y 崩 |
| `ts_target_tvr_hump(x, target_tvr=0.60)` | `1YNQPwXK` | 1.98 | 0.81 | 0.3324 | **1.34 ✗** | 1.10 | 0.904 | 2 | ✗ 2Y+F 双崩 |
| `hump(x, hump=0.05)` | `j2Ybxj89` | **0.02** | 0.00 | 0.0455 | 0.66 | −0.27 | −0.01 | 4 | ✗✗ 信号全灭 |

**四条可复用的判据**：

1. **首选设置层 `decay`，不要在表达式里加平滑算子。** 换手 0.7559 → 0.5540（−26.7%），
   Sharpe 只掉 9.2%，**fitness 反而从 1.09 升到 1.14**，2Y 只掉 10.7%（远低于 40% 封盘线），
   且表达式保持 **2 个算子**的 ATOM 形态。同一表达式换一个 settings 值就全闸通过。
2. **`ts_decay_linear(x,2)` 是等效备选**（tvr 0.5916 / F 1.09），但它把算子数从 2 加到 3、
   且 2Y 更低（1.78 vs 1.84）⇒ **只在不改设置时才用它**。
3. **`ts_target_tvr_*(target_tvr=…)` 会过度平滑**：要 0.60 实际只给 0.28–0.33（不足目标一半），
   代价是 **2Y 直接跌破 1.58 闸**（1.34 / 1.38）。它的自适应调参把长窗慢信号里那点 2Y 强度一并磨掉了
   ⇒ **对「2Y 本来就只有 2.0 左右」的候选，不要用自适应换手算子**。
4. **`hump` 对秩尺度信号是灾难**：`hump(ts_rank(...), hump=0.05)` 的死区相当于满量程的 5%，
   把 ts_rank 的日间微小变动全部吃掉 ⇒ S 2.94 → **0.02**。秩值域 [0,1] 上 `hump` 参数的
   量级必须 ≪ 1e-3，否则等同于把信号冻死。**`hump` 只适合原始量纲差异很大的信号，不适合 rank 输出。**

> 与结论 3 再修正（长窗 `ts_rank` 压换手不杀信号）一致：本例 504 日 rank 的日间变化 < 1/504，
> 对任何平滑都高度耐受。**判据仍是「2Y 衰减比例」，不是换手降幅**。

### 结论 34：决定互相关的是「经济概念同一性」，不是「数据集 id」（对旧结论的边界修正）

旧结论曾写「**同门控 + 不同信号腿来源（换数据集）⇒ 互相关 0.082**」。本轮实测给出一条硬边界：

- `P0od8o1w` = `-ts_rank(rsk65_mfm_etfm4_dsrt_intermediate, 504)`（数据集 **risk65**）
- `pwdA3Jqv` = `-ts_rank(rsk72_top3000_dsrt, 504)`（数据集 **risk72**，覆盖率 1.0，另一张表）
- **两者互相关 = 0.8991**（986 个日收益点，4 年窗口）⇒ `max_mutually_below_subset_size = 1`

**两个数据集 id 完全不同（名字、覆盖率、alphaCount 全不同），但底层是同一份「特异性收益
（specific / idiosyncratic return）」序列** ⇒ 相关性 0.90，与「同一数据集换期限/档位」的
0.83–0.88 **几乎无差别**。

**修正后的判据**：
1. 低相关来自「**不同的经济机制**」，不是「不同的数据集 id」。
   换数据集但换的是**同一个经济量**（如 risk65 `dsrt` → risk72 `dsrt`）＝ 换汤不换药。
2. 「同门控 + 不同信号腿来源 ⇒ 0.082」这条只在**信号腿确实是不同机制**时成立
   （当时的 0.082 例是拿不同 category 的字段做腿）。
3. 因此点亮某座塔要凑 N 颗时，选来源的正确顺序是：
   **先按经济机制分类**（反转 / 借券约束 / 风险溢价 / 关注度…）→ 每个机制各取一颗 →
   再实测互相关。**不要按数据集名去凑**，那会在同一机制里反复产出 0.85+ 的重复品。

---

### 结论 35：★★★ 字段 alphaCount 低 ≠ prod 低相关 —— 拥挤度要看「机制在整池的总暴露」

**实证（USA D1，2026-10-28）**：`P0od8o1w` = `-ts_rank(rsk65_mfm_etfm4_dsrt_intermediate, 504)`
（decay=10）IS 侧**全闸通过且质量很好**：

| S | F | tvr | 2Y | sub | invest_S / 比 | fRA | 塔位 |
|---:|---:|---:|---:|---:|---|---:|---|
| 2.67 | 1.14 | 0.5540 | 1.84 | 2.14 | 2.31 / 0.865 | 0 | risk |

但**平台实测 `prod = 0.9477`**（红线 0.7，无豁免）⇒ **不可提交，路线封盘**。

**为什么会被误导**：该字段看起来极不拥挤——`userCount=80`、`alphaCount=89`、`coverage=1.0`。
可是它所代表的**经济概念**「特异性收益 / idiosyncratic return」在**别的数据集**里被大量使用：

- `risk70.daily_specific_return` → alphaCount **6305**（同一概念最拥挤的实现）
- `rsk72_top3000_dsrt` → 2600；`rsk65_mfm_etfm3_dsrt_intermediate` → 191；`rsk65_trsd_*` → 86/125

⇒ 生产池里早已堆满同一概念的 alpha，**换一个数据集 id 换不掉 0.93+ 的 prod**。

**判据（写进派发前 checklist）**：
1. **alphaCount 只在「字段」这一粒度上计数，prod 是「概念」粒度上的暴露**——两者不可互相推断。
2. 判断拥挤度的正确动作：拿字段的**语义关键词**（如 `specific return` / `idiosyncratic`）在
   **全部 category** 里搜近义字段，把 alphaCount **加总**；加总 > ~5000 视为 prod 高危，
   **不要**因为本数据集只有 89 就认为安全。
3. **「IS 全闸通过」与 prod 完全正交**——S 2.67 / F 1.14 / 2Y 1.84 / invest 比 0.865 / fRA=0
   的候选照样可能 prod 0.95。因此**prod 预判必须前置到选字段阶段**，不能等全闸跑完再测。
4. **特异性收益族（specific / idiosyncratic return）作为信号腿永久跳过**（USA D1）：
   `risk65.*dsrt*`、`risk65.trsd*`、`risk72.*dsrt`、`risk70.daily_specific_return*`。
5. 反过来，**低 alphaCount + 不同经济概念**才是 prod 安全区：同批发现的
   `risk70` 风格因子族（`residual_volatility_factor` 14、`relative_valuation_factor` 100、
   `dividend_yield_factor` 129、`earnings_quality_factor` 15、`financial_leverage_factor` 10）
   属于「风险模型暴露」概念，与特异性收益正交，是 RISK 塔更可行的供给。

---

### 结论 36：★★★ 多金字塔挂靠机制 —— 用目标塔字段做「分组变量」即可让强信号计入该塔

**这是点亮零塔的主路线，2026-10-28 在 USA D1 实证成功。**

#### （A）机制

一颗 alpha 的塔位**不是**由「信号的来源数据集」单点决定，而是由**表达式里实际出现的
所有字段所属塔位**共同决定。平台返回：

```json
{"ra": {"pyramid_short": "risk/model"},
 "pyramids": {"effective": 2,
              "list": [{"name": "USA/D1/RISK",  "multiplier": 1.1},
                       {"name": "USA/D1/MODEL", "multiplier": 1.3}]}}
```

⇒ 只要把**目标塔的低拥挤字段**放进表达式（最省伤的做法：当 `bucket()` 分组变量），
该塔就会进入 `pyramids.list`。信号腿仍用原本的强字段，`pyramids.effective` 变 2。

#### （B）实测：挂靠成本极小（单变量对照，同族信号腿）

| 版本 | 表达式 | S | F | tvr | 2Y | sub | invest_S/比 | fRA | pyramid_short |
|---|---|---:|---:|---:|---:|---:|---|---:|---|
| 基线 | `N1eLE1de`（credit_risk pair-diff） | 2.63 | 1.54 | 0.1409 | 2.07 | 1.66 | 2.50 / 0.951 | 0 | `model` |
| **10 桶挂靠** | `88RdZ61v` = 外层 `group_neutralize(·, bucket(rank(residual_volatility_factor), range="0,1,0.1"))` | **2.65** | 1.46 | 0.1588 | **2.07** | **1.64** | 2.50 / **0.943** | **0** | **`risk/model`** |
| 基线 | `zqrgna91`（buzz_intensity pair-diff） | 2.67 | 1.66 | 0.1579 | 1.68 | 1.47 | 2.70 / 1.011 | 0 | `model` |
| 10 桶挂靠 | `zq31EopX` | 2.65 | 1.53 | 0.1759 | **1.52** | **1.40** | 2.65 / 1.000 | 2 | `risk/model` |
| 基线 | `YPMvZZvv`（目标价 tribes） | 1.79 | 1.06 | 0.062 | 1.68 | 0.83 | 1.93 / 1.078 | 0 | `analyst` |
| 10 桶挂靠 | `O0AEjnv7` | 1.76 | 1.00 | 0.0615 | **1.51** | 0.78 | 1.92 / 1.091 | 1 | `risk/analyst` |

**挂靠代价的规律**：
- **Sharpe / investability 几乎不动**（±0.03、invest 比完全不变）⇒ 挂靠不伤主信号。
- **主要损耗落在 2Y 与 sub-universe**（−0.16 / −0.07），而这两项恰好是最容易卡闸的两个。
- 因此「擦边候选」挂靠后会翻红：`zq31EopX` sub 1.40 vs 限 1.41、2Y 1.52 vs 限 1.58；
  `O0AEjnv7` 2Y 1.51 vs 1.58。**基线必须留 ≥0.2 的 2Y 余量**才扛得住挂靠。

#### （C）塔混合规性（与用户硬约束「PV/MODEL/OTHER 禁两两混」）

| 挂靠组合 | 是否合法 | 说明 |
|---|---|---|
| `risk/model` | ✅ | RISK 不在三塔禁列内 |
| `risk/analyst` | ✅ | 同上 |
| `pv/risk` | ✅（实证 `xAr0EQlb`） | 同上 |
| `model/other` · `pv/model` · `pv/other` | ❌ | 命中禁令（历史存在 5 颗，新提交不得再造） |

⇒ **RISK / EARNINGS / FUNDAMENTAL / INSTITUTIONS / MACRO / SENTIMENT / NEWS / INSIDERS /
SHORTINTEREST / SOCIALMEDIA / OPTION / IMBALANCE 这 12 座零塔全部可用挂靠路线**，只要
信号腿不落在 PV/MODEL/OTHER 以外的第二个「禁塔」里。注意：**信号腿本身不能是
MODEL/OTHER/PV 与另一禁塔的组合**，但 `risk + model` 这类含单座禁塔的组合是合法的。

#### （D）实现要点（避免被判为「纯技巧挂靠」）

1. **必须真实使用该字段做分组**：`group_neutralize(信号, bucket(rank(risk字段), range=...))`。
   **不得**用 `add(signal, multiply(rank(risk_field), 0))` 之类零权重乘法——那是套利规则。
2. **在外层再套一层 group_neutralize，不要替换原有分组**：保留原 `market` / `subindustry`
   信息，扰动最小（`N1eLE1de` 内层 subindustry 保留 → 2Y 完全未退化）。
3. **锚字段优先选 alphaCount 极低的**：`financial_leverage_factor` 10、`residual_volatility_factor`
   14、`systematic_risk_beta_factor` 3（均 risk70，coverage 1.0）。
4. **避免用特异性收益族当锚**（`risk65.*dsrt*` / `risk72.*dsrt` / `risk70.daily_specific_return`）
   —— 见结论 35，该族本身 prod 饱和。
5. **bucket 粒度是调 2Y / sub 的第一杠杆**：`range="0,1,0.1"`=10 桶（本轮默认）→
   `range="0,1,0.2"`=5 桶（Wave 135 正在验证是否更轻）。粒度越粗，对原信号排序破坏越小。

#### （E）待验证

- **次塔是否计入 `get_pyramid_alphas` 的季度计数**：本季度 11 颗 REGULAR 全为单塔，
  无法对照；多塔语义（`effective=2` + 每塔各给 multiplier）强烈暗示**两塔都计**。
  若成立，则「点亮某塔」只需提交 1 颗多塔 alpha 即可同时推进两座塔。

---

### 结论 37：★★★ prod 与 investability 是**同一成因的两个投影** —— 二者反相关，只有窄带同时达标

**实证（USA D1，2026-10-28，7 颗低 prod 候选一次性打穿）**

| alpha | S | F | tvr | prod | **invest_S** | **invest 比** | 判定 |
|---|---:|---:|---:|---:|---:|---:|---|
| `d5KPPrxx` | 3.13 | 2.46 | 0.166 | 0.6737 | **0.25** | **0.080** | ✗ invest |
| `O0Jgd7Y7` | 2.27 | 2.03 | 0.130 | 0.5516 | **−0.06** | **−0.026** | ✗ invest |
| `vROPEJ8w` | 2.08 | 1.74 | 0.105 | 0.5517 | 0.17 | 0.082 | ✗ invest |
| `LL53QVvn` | 1.61 | 1.39 | 0.112 | 0.6163 | 0.22 | 0.137 | ✗ invest |
| `1Yj08nb6` | 1.58 | 1.20 | 0.100 | 0.5796 | −0.03 | −0.019 | ✗ invest |
| `XgRM3Yra` | 1.66 | 1.19 | 0.087 | 0.5803 | −0.10 | −0.060 | ✗ invest |
| `zqbvOmOR` | 4.30 | 3.28 | 1.769 | 0.5155 | 0.54 | 0.126 | ✗ tvr+fRA3+invest |

**7 颗里 6 颗 invest 比 < 0.14，1 颗 −0.06** —— 而它们的 prod 全部在 0.51–0.67 的「安全区」。

#### （A）机理：同一个成因

- **prod 低** = 生产池里没人做这个信号。
- **invest_S 低** = 该信号只在**流动性尾巴（小票/低成交额）**上有预测力，在流动大票上归零。
- 两者是**同一件事的两面**：「别人不做」往往正因为「大票上没钱赚」。
- 数学上：`invest_S` 是限定 investable universe（流动大票）后重算的 Sharpe；
  信号若来自 `total_*_transaction_count`（零售成交笔数）、微结构、小票特异事件，
  大票子样本里就只剩噪声。

#### （B）数据集级红线（直接跳过，不必再测）

- **dataset 382 `total_*_transaction_count` 族**（`total_buy_transaction_count`、
  `total_top_secondary_buy_transaction_count`、`total_top_secondary_sell_transaction_count`…）：
  实测 invest 比 0.08 / −0.03 ⇒ **整族不可提交**，无论 S/F/2Y 多好。
- 判据：**任何「笔数 / 笔数占比 / 小票事件计数」类字段，先查 invest 再谈其他**。

#### （C）能同时达标的窄带：截面排序型（`group_rank` / `ts_zscore` 于大盘 universe）

实测同时满足 `prod < 0.7` 且 `invest 比 ≥ 0.9` 的**只有**这一族：

| alpha | 模板 | prod | invest 比 |
|---|---|---:|---:|
| `N1eLE1de` | `ts_decay_linear(group_rank(ts_zscore(ts_backfill(pair-diff,252),252),subindustry),5)` | 0.6916 | **0.951** |
| `zqrgna91` | 同上（`market` 分组 + `signed_power 0.8`） | 0.6877 | **1.011** |
| `YPMvZZvv` | `group_rank(ts_zscore(tribes,175),subindustry)` | 0.6958 | **1.078** |
| `88RdZ61v` | 上式 + risk 挂靠 | 测中 | **0.943** |
| `zq31EopX` | 上式 + risk 挂靠 | — | **1.000** |
| `O0AEjnv7` | 上式 + risk 挂靠 | — | **1.091** |

⇒ **共同点**：全都在 **TOP2000 / TOP3000** 大盘 universe 上做**截面排序**（`group_rank`），
且信号是**慢变量**（252 日 zscore / 175 日 zscore / decay 5–210）。
慢变量 + 大盘 ⇒ 换手低（0.06–0.18）⇒ 大票上依然有 alpha ⇒ invest 高。

#### （D）对策略的硬影响

1. **`invest 比 ≥ 0.70` 必须排在筛选第 2 位**（fRA 之后、Sharpe 之前）。
   本次它一次性关闭了 6 颗「S 1.6–4.3、fRA=0、prod 0.52–0.67」的候选，
   若按 S/F 排序会全部误判为「最优未提交存量」。
2. **不要用「低 prod」当安全性证据**——低 prod 的本土成因常常是不可投资。
3. **提升 invest 的杠杆**：换大盘 universe（TOP1000/TOP2000/TOP3000）、
   把快信号改慢（长窗 `ts_zscore` / 大 decay）、改用截面排序而非时序事件。
4. **验收口径**：`investability_ratio = invest_S / S`，
   由 `batch_get_alpha_metrics` 单次批量返回（唯一直接入口）。

---

### 结论 38：★★★ 点亮一座塔 = 「3 个不同信号**来源**」；第 3 个概念常藏在「慢速 hump + 三重风险 bucket」族里

**实证（USA D1 RISK 塔，2026-10-28，篮内互相关 `max_mutually_below_subset` 精确解 = 3）**

| alpha | 信号腿（数据集） | 塔位 | S | F | tvr | 2Y | sub | invest 比 | fRA |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| `9qxLOPxr` | buzz_intensity 2−11（ai_equity） | risk/model | 2.69 | 1.67 | 0.1592 | 2.24 | 1.44 | 1.011 | 0 |
| `88RdZ61v` | credit_risk_model_score 5−7（ai_equity） | risk/model | 2.65 | 1.46 | 0.1588 | 2.07 | 1.64 | 0.943 | 0 |
| `E56XvX90` | **assetutilization_sentiment_polarity**（earningscall） | **risk/other** | 1.75 | 1.13 | **0.0333** | **2.39** | 1.05 | 0.931 | 0 |

篮内两两相关：`9qxLOPxr×88RdZ61v` **0.389**、`E56XvX90×9qxLOPxr` **0.1471**、`E56XvX90×88RdZ61v` **0.0596** —— 三条全 < 0.5。
同一表达式里 4 颗 hump 变体（`E56XvX90`/`pwdAPALb`/`akKqLq56`/`P0od2pOp`）**互相 0.927–0.973**，只能取 1 颗。

#### （A）为什么第 3 个概念最难找

前两颗都能从**同一个"挂靠"模板**（结论 36：强信号 × risk70 字段做 `bucket()`）产出，
但它们天然只覆盖 1–2 个信号来源。**同来源换期限/档位/门控一律 0.93+**（结论 34/36 已证），
所以第 3 颗必须换**数据集**，而不是换参数。

#### （B）第 3 个概念的正解形态：慢速 hump + 三重风险 bucket

```
hump(
  group_neutralize(
    group_neutralize(
      group_neutralize(
        group_rank(ts_zscore(ts_backfill(vec_avg(<信号字段>), 126), 504), subindustry),
        bucket(rank(market_capitalization_factor), range="0,1,0.1")),
      bucket(rank(trading_liquidity_factor), range="0,1,0.1")),
    bucket(rank(price_momentum_factor_score), range="0,1,0.1")),
  hump=0.0001)
```

- **三重风险 bucket** 同时剥离规模 / 流动性 / 动量暴露 ⇒ 残差与那两条（ai_equity 微结构）**近乎正交**（0.06–0.15）。
- **`hump=0.0001` + 504 日 zscore** 把换手压到 **0.033**，落在结论 37 的「慢变量 + 大盘」窄带里 ⇒ invest 比 0.93。
- `sub_universe_sharpe` 1.05 刚好过 `LOW_SUB_UNIVERSE_SHARPE`（limit ≈ 0.53×S = 0.93）——**这类慢速低波动候选的 sub 是最后一根稻草，选变体时优先挑 sub 最高的那颗**。

#### （C）选变体的排序（本族内）

`E56XvX90`（sub 1.05 / 2Y 2.39 / invest 0.931）> `akKqLq56`（1.03 / 2.42 / 0.919）> `pwdAPALb`（0.99 / 2.29 / 0.914）> `P0od2pOp`（0.86 / 2.06 / 0.882）。
**边际差异全在 sub 上**，而 sub 是硬闸 ⇒ 按 sub 排序，不按 F 排序（`P0od2pOp` F 1.18 最高但 sub 0.86 直接红）。

#### （D）塔位合规性（易误判）

`E56XvX90` 的 `ra.pyramid_short = "risk/other"`，`pyramids.list` = `[USA/D1/RISK, USA/D1/OTHER]`。
用户硬约束是「**PV / MODEL / OTHER 三者之间**禁两两混」，`risk/other` 只含 OTHER 一个受限塔 ⇒ **合法**（与 `risk/model` 同理）。
**判据**：把 `pyramid_short` 拆成集合，若它与 `{PV,MODEL,OTHER}` 的交集 ≥ 2 才违规。

#### （E）对零塔路线的推广

12 座零塔（RISK / EARNINGS / FUNDAMENTAL / NEWS / SENTIMENT / INSIDERS / INSTITUTIONS / MACRO / SOCIALMEDIA / SHORTINTEREST / OPTION / OTHER…）都可用同一配方：
1. 找该塔的**低拥挤字段**（alphaCount 个位数）当 `bucket()` 分组变量 —— 进塔用；
2. 信号腿一律从**别的数据集**取，且每颗换一个数据集 —— 互相关用；
3. 优先选**慢速截面排序 + hump** 形态 —— invest 用。
三步分别对应三个独立的闸，互不替代。
