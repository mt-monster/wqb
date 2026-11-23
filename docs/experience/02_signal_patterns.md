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

### 12.7 ★ 反向告诫：rank 壳内换「聚合算子」不是新探针（2026-10-31 KOR 实证）

`rank` / `group_rank` / `quantile` 都是**秩变换**，对入参的任何**严格单调变换**免疫 ⇒ 下列改写**逐位同信号**：

| 改写 | 关系 | 结论 |
|---|---|---|
| `ts_sum(x,d)` ↔ `ts_mean(x,d)` | 差一个正标量 d | 同信号 |
| `ts_std_dev(x,d)` ↔ `ts_var(x,d)` | 差一个单调 sqrt | 同信号 |
| `multiply(x,k>0)` ↔ `x` | 正标量 | 同信号 |

**战例**：KOR other496 wave 214 `group_rank(ts_sum(oth496_kor_mapped_limit_status,22), sector)` 与
wave 270 `group_rank(ts_mean(…,22), sector)` —— **S 都是 −0.64、TO 都是 .2104**，逐位相同，那一槽位等于白烧。

**判据（发批前先自问）**：把改写写成 `g(f2(x))` 与 `g(f1(x))`，若 `f2 = a·f1 + b`（a>0）或更一般 `f2 = h(f1)`
（h 严格单调）且 `g` 是秩算子 ⇒ **不是新探针**。真正的新探针只有换**壳**（分组轴 / 时间窗 / 事件条件 / 外层几何）
或换**字段 / 机制**。与 §12 不矛盾：§12 讲「换实现能改指标」（瓶颈在噪声或形状），
本条讲「换聚合不能改信号」（秩已把差异吸收）——**共同判据是先看外层是不是秩**。

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

### 结论 17b：外部文章的 4 条单字段 ATOM 模板只作候选（2026-11-17）

`docs/reference/atom_mining_playbook_20261117.md` §三⚠4 收录了 4 条单字段模板：

```
① group_rank(ts_mean(F,20) / ts_mean(F,120), subindustry)     // 长短均值比（边际变化）
② group_neutralize(ts_zscore(F,60), subindustry)              // 时序标准化 + 组内中性
③ ts_decay_linear(-ts_rank(F,252), 10)                        // 一年期分位反转（低换手）
④ group_rank(ts_delta(F,20) / ts_std_dev(F,60), sector)       // 差分÷自身波动（单字段 SNR）
```

本仓**只验证了方向**（单字段扫描 + 低 `alphaCount` + 新 onboard），**未逐条实测**；入批前必须过
`gate.py` / 证据闸 / 区内符号指纹校验。另：文章称 TO<30% 时 2Y 阈值 ×0.85，本仓判别件
`YP1ZvjWA`（USA/TOP3000/D1，ATOM 单数据集，TO 17.7%、2Y 1.57、`LOW_2Y_SHARPE` warning
`limit=1.58`、`ra_failed=true`）**未见折扣** ⇒ 近闸线按 **1.58**，不要用 1.34。

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

### 结论 32.5：批次失败的两种形态与处置（2026-11-20 实测校正 + 落地）

2026-11-20 在 EUR 侧复现并区分了两种此前混为一谈的失败形态：

| 形态 | 触发条件 | 平台表现 | 槽位损失 | 处置 |
|---|---|---|---|---|
| **A｜编译期连坐** | 幽灵算子 / 元数违规 / 命名参数违规 / 字段非法 | 父 multisim 状态 **ERROR**；出错条 ERROR、**其余全部 CANCELLED** | **整批**（实测 2 臂批中好臂被 CANCELLED、坏臂 ERROR：`Attempted to use inaccessible or unknown operator "ts_max"`） | 本地静态闸拦（形态 A 全部静态可判）；已成批则二分隔离 |
| **B｜运行期逐条** | 量纲（UNITS）/ 算子语义错 | 该条 WARNING/FAIL，**其余照常出 alpha** | 单条 | 读该条 error 修正表达式后重投 |

**落地（2026-11-20）**：
1. **MCP 静态闸补齐形态 A 三项**：`_toolkit_gate_check` 原只查语法 / inaccessible_ops / 毒模式，
   现并入 `wqb.expression.op_arity`（算子存在性 + 元数 + 命名参数 + 调用点数）。
   实测 `ts_max`（幽灵算子）、`ts_rank(x)`（元数）、`ts_rank(x,252,extra)`（位置参数过多）全部**本地拦下**，
   不再烧平台槽位。
2. **`ts_target_tvr_*` 的 `target_tvr` 平台必填**（catalog 名义有默认值但平台报
   `Required attribute "target_tvr" must have a value.`）：已在 `op_arity._REQUIRED_NAMED_ARGS` 显式登记，
   平台必填 ≠ catalog 默认。
3. **新工具 `tools/backtest/batch_isolate.py`**：批回来若含 CANCELLED ⇒ 二分重投定位坏臂，**只重投好臂**
   （坏臂写报告不再投）；派发受通道闸约束（CLI 默认禁，正常路径是本工具出计划 + MCP 派发）。

**派发纪律（新增）**：
- **首次出现的算子 / 字段 / 参数组合 ⇒ 单独 1~2 条一批先探**，探通才并入大批。
  这与「同类别算子全替换」天然冲突——全替换批**必然含未验证算子** ⇒ 该批应**分层小批**（每层 2–3 条），
  否则一条编译期错误会连坐整层。
- 收批后**必须核对每条子任务状态**：形态 B（逐条 WARNING）与形态 A（整批 CANCELLED）的处置完全不同。

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

---

## §17 ★★★ 探针等价性：哪些「变体」根本不构成新实验（2026-10-31 KOR 70 波复盘）

> 机器层对应规则：`rank_shell_aggregator_swap_is_not_new_probe_v1`（全局 `methodology_rules.json`）。
> 与 §12「等价算子替换」互补：§12 说**判死前必须扫替换**，本节说**哪些替换是 no-op、扫了也白烧配额**。
> 区域完整实证见 [`tracking/KOR/reference/kor_session_lessons_20261031.md`](../../tracking/KOR/reference/kor_session_lessons_20261031.md) §3。

### 17.1 rank 壳内的聚合算子互换 = 同一条探针（逐位相同，不是「接近」）

`rank` / `group_rank` 保序，**吸收任何严格单调变换**。因此在 rank 壳内换
`ts_sum` ↔ `ts_mean` ↔ `ts_av_diff`（同窗口、同字段）**不产生新信号**：

| 对 | 表达式差异 | 实测 |
|---|---|---|
| KOR wave214 #5 vs wave270 E1 | rank 壳内 `ts_sum` ↔ `ts_av_diff` | **S −0.64 / TO .2104 逐位相同** |

同类 no-op：`winsorize(rank(x), std=k)`（rank 输出已在 [0,1]，任何 std≥1 的截尾都不触发）、
`rank(rank(x))`、`ts_quantile(x,d,gaussian)` 外套 `rank`（逆 CDF 单调）。
⇒ **发波前按「rank 壳 + 字段 + 窗口 + 分组轴」四元组去重**，不要按表达式字符串去重。

### 17.2 `hump` ≠ `ts_decay_linear`：不可互替，也不可当冗余算子压掉

§9 与杠杆阶梯里「时序平滑在累积型信号上零和」的结论**只适用于 `ts_decay` / `ts_mean` 这类作用于信号均值的平滑**。
`hump` 作用于**换仓成本**（限制单日权重变动），是另一条轴：

| risk59 基线 | S | F | 2Y |
|---|---|---|---|
| 带 `hump=0.003`（`QPvr1vPM`） | 1.02 | 0.67 | 1.80 |
| 去掉 hump（`akKAY1g6`） | **0.90** | **0.53** | **1.60** |

⇒ **hump=0.003 值 +0.12 S**，属有用算子，压缩时不得删（删了会掉闸）。
推论：算子消融协议里「删除后崩 ⇒ 回滚」之后，仍可走**等效替换**（换实现保含义），但 hump 没有同义替代。

### 17.3 `reverse()` 不是精确反号；翻正**不改变** turnover

- `reverse(x)` 与 `-x` 的差 = **2×成本**（截断 × decay × 符号交互），所以铁律 B「方向正反各测一条」仍然必要；
- 但 **TO 由信号形态决定，不由符号决定**：KOR other496 RMW（wave271）正向与反向 **TO 同为 .0648**。
  ⇒ **反向变体不能当「降换手」杠杆**；它只能用来赌方向，不能用来修 `LOW_TURNOVER` / fitness。

### 17.4 fitness 的分母有 `.125` 换手地板

`fitness ≈ Sharpe × sqrt(margin)`，而 margin 的换手项被钳在 **0.125** 下限
⇒ **TO 低于 .125 后再降换手不再提 fitness**。这解释了为什么「极低 TO + 中等 S」的慢变量候选
fitness 反而好看，也解释了为什么在 TO 已 <.125 的候选上继续扫 decay 是零杠杆。

### 17.5 ★ 天花板代数：机制正交 ≠ 收益不相关（组合上限要先算再挖）

KOR 单塔单字段 ATOM 的实测上限 **S 1.04**（对 1.58 的闸缺 34%）。多腿组合的上限由**实测日收益相关系数**决定，
不由「机制看起来不同」决定：

| 形态 | 上限 S | 依据 |
|---|---|---|
| 单腿 ATOM | 1.04 | risk59 全字段普查最优 |
| 2 腿 | 1.238 | 实测 ρ |
| 3 腿 | **1.292** | 实测 **ρ=0.1978**（1023 个日收益点） |
| 达 1.58 所需 | 4 腿各 1.0，或 7 腿各 0.9 | 同上 ρ 外推 |

⇒ **开波前先算组合上限**：若当前攻击面的单腿上限 × 可达腿数仍低于平台闸，
继续铺量是结构性无效努力，应换攻击面（换塔 / 换区 / 请用户放宽约束），而不是再扫参数。
这条与 §11「多腿强度不可逆拆分」是同一枚硬币的两面：**存量多腿不能拆成单信号供给，新组合也不能靠机制命名凑强度**。

---

## §18 ★★ 时间轴回归族（`ts_step`）：`rettype` 选错等于白跑（2026-11-14 实证，21 条）

**触发场景**：拿到「趋势 / 斜率 / 去趋势」类配方，想用 `ts_regression(y, ts_step(1), d, rettype=k)` 落地。

### 18.1 核心判据：`rettype` 的选择比窗口重要一个数量级

同一骨架、同一批字段，只改 `rettype`：

| 族 | 表达式核心 | USA 实测 S |
|---|---|---:|
| 斜率（rettype=2） | `rank(ts_regression(ts_zscore(close,252), ts_step(1),252, rettype=2))` | **−0.05 ~ −0.08** |
| TM=β×R²（2 与 6 相乘） | `rank(multiply(β, R²))` | −0.08 |
| 趋势 t 值（2 / 8） | `rank(divide(β, SE_β))` | −0.07 |
| 趋势线性度（`ts_corr`） | `rank(ts_corr(ts_zscore(close,252), ts_step(1),252))` | −0.08 |
| **去趋势残差（rettype=0）** | `rank(-ts_regression(..., rettype=0))` | **IND 1.55 → STATISTICAL 1.76** |

⇒ **斜率族的幅度本身接近零，不是符号反了**（反向也只有 +0.08）。判"这个方向没信号"之前，先确认 `rettype` 是不是选错了。

### 18.2 载体必须零均值可判：去趋势只用在有水平漂移的变量上

| 载体 | 结果 |
|---|---|
| `ts_zscore(close, d)` | 可用（IND S 1.55） |
| 财务存量（revenue / operating_income / est_*） | 正但弱（S 0.45–0.57） |
| **`ts_zscore(returns, d)`** | **报废：TO 0.8433、F 0.34、4 项 FAIL** |

机理：returns 是零均值序列，其 z 分数在 0 附近反复穿越 ⇒ 残差符号剧烈翻转 ⇒ 换手爆炸。**判据一句话：载体是否零均值；零均值的 flow 变量不能做去趋势。**

### 18.3 有效性 ∝ 宇宙小市值程度（同一条骨架跨区）

| USA/TOP3000 | GBR/TOP700 | EUR/TOP2500 | IND/TOP500 |
|---:|---:|---:|---:|
| 0.60 | 1.20 | 1.39 | **1.55** |

⇒ 长期均值回复类信号**不在 USA 大盘磨**；USA 上 S 0.60 且 2Y 0.45，已属结构性无效。

### 18.4 `STATISTICAL` 是 `robust universe sharpe` 的专用杠杆

IND 同一表达式，只换中性化：

| 中性化 | S | F | robust universe sharpe |
|---|---:|---:|---:|
| SUBINDUSTRY | 1.55 | 1.30 | **0.51 FAIL** |
| **STATISTICAL** | **1.76** | **1.35** | **0.85**（仍差 0.15） |

对照：`truncation 0.08 → 0.04` **逐位相同，完全无效**。
⇒ 遇 `LOW_ROBUST_UNIVERSE_SHARPE` 卡点，先换 `STATISTICAL`（纯风险因子中性化把持仓从"行业内相对偏移"改成"风险暴露对齐"），不要调 truncation。

### 18.5 `REVERSION_COMPONENT` 按结构触发，不按字段

21/21 条全部命中，包括**纯基本面载体**（`revenue`）与**纯分析师载体**（`est_12m_ebt_mean`），完全不碰价格。

原文：`Alpha expression includes a reversion component so we may not accept these alphas in the future`。

判读：① 是 **WARNING 不是 ERROR**（21 条全有完整指标，不是拒付）；② 但整族背标记 ⇒ 即便调到 S 1.76 也有提交隐患；③ 检测依据是「对时间回归」结构在日频持仓上表现出的短期反转相关性。
⇒ 该族的最优解不是继续调参，而是**换机制**（见 `05_antipatterns.md`）。

### 18.6 已达上限的实证（供判死参照）

最强件 `2r5q1Kex`（IND/TOP500/STATISTICAL/decay4/trunc0.08）：
S 1.76 ✓ / F 1.35 ✓ / sub ✓ / CW ✓ / MATCHES_PYRAMID ✓，但 `LOW_ROBUST_UNIVERSE_SHARPE` **0.85 < 1.0** FAIL 且 `LOW_2Y_SHARPE` **1.14 < 1.58**（按铁律 WARNING 视同 FAIL）。
IND 只有 TOP500 一个 universe 档位（`get_platform_setting_options` 实测），无法换宇宙 ⇒ 剩余 0.15 无杠杆可推。

详见 `output_report/ts_step_templates_20261114.md`；模板骨架见 `docs/reference/economic_alpha_template_library.md` T13。

---

## §19 ★★ F 闸的定量可达界 + 两条对模型输出/符号翻转的实测律（USA news 族 14 臂，2026-11-15）

### 19.1 F 闸不能靠调参补：先把「可达界」算出来再决定要不要继续加臂

`F = S × sqrt(returns / max(TO, 0.125))`，`TO` 有 **0.125 下限**。于是：

- `TO ≥ 0.125` 时 `F` 随 `ret/TO`（≈ 单边 margin）线性开方，**降 TO 不改变 F**（ret 与 TO 同比例缩）；
- `TO ≤ 0.125` 时等价于 **`F = S × sqrt(ret/0.125)`**，判据塌缩成一条：**`S × sqrt(ret) ≥ 0.3536`**。

⇒ **开波前先算可达界**：拿该族已知最强臂的 `S` 与 `ret` 相乘开方，若离 0.3536 差 1.5 倍以上，
**换模板/换窗口/换 decay 全都无解**，必须换信息源。

USA news 族实测（14 臂 / 3 集 / 12 结构互异模板）：

| 臂 | S | ret | `S×sqrt(ret)` | 距 0.3536 |
|---|---|---|---|---|
| `88NrXV3a`（news48 注意力稀释） | 1.18 | 0.0325 | 0.213 | **差 1.66×** |
| `E5Qb2PKm`（event_return_model 三期限集成） | 0.77 | 0.0281 | 0.129 | **差 2.74×** |
| 交付对照 `vRAn3xkG` | 1.97 | 0.0383 | **0.386** | ✓ 过 |

该族需 **S ≈ 1.9–2.4** 才可能过闸，而 12 个模板最高 S 仅 1.18 ⇒ **F 闸结构性天花板**。
⚠ 这是 **PROVISIONAL**（D2 字段族 6/22·6/59·2/23、D4 单分组轴、D6 单配置，未满足判死六维），
**不得**作邻接 news 集先验、**不得**据此宣布 news 塔关闭。

### 19.2 ★ 四闸同号负值 ⇒ 先 `reverse()` 再判死，不要判「弱」

`58J92waN`（event_return_model 跨期限分歧 5d−20d）实测：
`S −0.54 / 2Y −0.55 / SUB −0.55 / invest_S −0.63` —— **四个独立度量同号同量级**。
加 `reverse()` 后 `omavk0Yn` = **+0.54**，精确镜像。

判据：**单看 S 为负可能是噪声；四个度量同时同号，是符号反了**。
这类臂的信息量与正 S 臂等价，丢弃它等于白烧一次配额。
（附带的判死反面：真正该判死的是 `9qlK2wAe` 那种 `S 0.15 / F 0.02 / 2Y −0.04`——S 近零且各闸方向不一致。）

### 19.3 ★ 模型输出类数据集：**水平值 ≫ 变化量**（与通用直觉相反）

同一 DL 收益预测字段族（`event_return_model`，category=news，59 字段、覆盖 0.999）：

| 构造 | 轴 | S |
|---|---|---|
| `ts_mean(ts_backfill(prob_rank_bin1_20d, 5), 10)` | **水平值** | **0.72** |
| `ts_mean(ts_delta(ts_backfill(prob_rank_bin1_10d,5),5), 5)` | **日间一阶差** | **0.15** |
| 5d+10d+20d 三 horizon 集成 | 同模型内 ensemble | 0.77（仅 +0.05） |
| 4 分位极差概率（label3−label0） | 分布形状 | 0.44 |

推理：模型**已经把时序信息消化进输出**，再对输出做差分等于对残差做差分，只放大噪声。
⇒ 模型/预测类字段（`predicted_*`、`prob_rank_*`、`*_model_score`）**先测水平值**，
"变化量优于水平值" 只适用于**原始观测字段**（情绪分、持仓量、财务科目）。

同批推论：**同模型内多 horizon 平均不是分散化**（0.77 vs 0.72，增益 0.05）——
要分散化必须**换信息源**，不是同模型多字段平均。

### 19.4 附：本轮两条工作清单纠错（不是新知识，是执行缺口）

1. **`CONCENTRATED_WEIGHT` 早在本文件 §14 有完整破局手册**，但我的开波闸清单漏了它。
   后果：`E56YX80G`（S2.91/F2.40/2Y3.87/SUB1.36）本地标签 `SUBMIT_LAYER_VERIFIED`，
   实测 `CONCENTRATED_WEIGHT` **0.1523 vs 0.1 FAIL** ⇒ BLOCKED。**闸清单必须固定为**
   `S / F / 2Y / SUB / TO / CW / invest_S·S / prod / self`。
2. **`submit_ready.gate='SUBMIT_LAYER_VERIFIED'` 不是放行依据**：平台 `GET /alphas/{id}/submit` **恒 404**，
   该标签只说明"查过并拿到 404"。同表 `towers` 列实测全为 `[]`，也不能用于塔位/ATOM 判定。
   任何候选一律以 `tools/submit_verdict.py` 实测为准（`E56YX80G` 即活证）。

---

## §20 ★★★ 收割池「一族一席」：IS-clean 行数 ≠ 候选数（USA 2026-11-15 全量聚类实证）

### 20.1 事实

`get_submit_ready(READY)` 的 38 条 `UNVERIFIABLE`（IS FAIL 0 / Failed-count 0）看起来是 38 个机会。
把 31 条剩余件做 `compute_mutual_correlation`（4y / 986 点，阈值 0.5）后：

| 互相关 | 组 | 说明 |
|---|---|---|
| **1.000** | `88R7JMxX` ≡ `78L0meRx` | 同一条，仅 `vector_neut` 参数序互换 |
| **0.9982** | `2rAQ5G0N` ≡ `QPvqzKjX` | 同一条，加/减一层 `vector_neut` |
| **0.9983** | `akKq92aO` ≡ `N1eLE1de`（已交付） | 同一条，加 `group_neutralize` |
| **0.9694** | `KPgYg8Nk` ≡ `MP6l68aa`（已交付） | 同一骨架，换 `group_rank` 轴 |
| 0.895 / 0.847 / 0.840 | `58EqmQEN`·`j2YdKN3Q`·`KPJwQzex` | institutions20 同族 |
| 0.734 / 0.621 / 0.588 | `ZYaweYl0`·`3q0YZPqg`·`mLaJ1Zq5` | earnings 语气反转族（与 ACTIVE `A1xJdOmg` 同骨架） |
| 0.762 / 0.658 | `gJezNxjg`·`gJevwxg0`·`MPYwqvLn` | shortinterest 贷款利率族 |
| 0.835 / 0.719 / 0.532 | `E56YodoJ`·`6Xd3lqnL` / `0mYopJ7r`·`P0oe533W` / `QPvex8G5`·`mLokaQJ5` | 三对同族 |

⇒ **31 条实际只有 6–8 个独立族**；扣除与已交付 6 颗重复后，
真正值得花 prod 槽的新增代表件**只有 6 条**（`Xg9Ymw1b`/`YP1ww82o`/`58EqmQEN`/
`MPYwqvLn`/`0mYopJ7r`/`QPvex8G5`）。

### 20.2 ★ 固化顺序（省 80% 平台单并发槽）

平台 prod 相关性是**账号级单并发**（`correlation_busy` 时 `retry_after` 可达 240s），
而 `compute_mutual_correlation` / `check_self_correlation` 是**本地计算、零配额**。

```
① 表达式文本比对（含变量赋值版 vs 展开版、参数序互换）
② compute_mutual_correlation 全量聚类，按「一族一席」挑代表件
③ 每族只 1 条跑 self-corr（并核 pool_size 合理性）
④ 每族只 1 条跑 prod（缓存优先，不默认 refresh）
⑤ 代表件 + 已交付件再合成一次篮内矩阵
```

顺序反了会用宝贵平台槽去测一条已经重复的件。本轮 31 次 → 6 次。

### 20.3 为什么行数会虚高

平台按表达式文本去重**只对同一批 multisim 内**有效；跨批次、参数序互换、
`a=…; b=…` 变量赋值 vs 展开写法、同族换一个高度相关字段，都会各占一行。
`submit_ready` 是**行级清单**，不是**因子级清单**。

### 20.4 实测撞墙率（代表件也要过 prod）

6 条代表件中，已完成的两条全部 FAIL：
`YP1ww82o` **0.7754**（0.7–0.8 桶 n=8）、`Xg9Ymw1b` **0.9559**（0.9–1.0 桶 n=1）。
⇒ **一族一席之后，prod 墙依然是主瓶颈**；收割池不是"捡钱"。
`Xg9Ymw1b` 的 `get_alpha_details` 侧证 IS 面完全干净（checks.fail=[]、CW PASS、
pyramids.effective=1、S2.04/F1.08/2Y2.14/SUB0.95/TO0.072），仍被单个 prod alpha 打掉。

**直方图判据**：`0.9–1.0` 桶 `n=1` 且 `max>0.9` ⇒ 生产池里有一颗几乎同形的已上线 alpha。
这与 §14 的「同表达式母件上线后 IS 件失效」是同一现象的不同强度，
不一定要同表达式，**同 PnL 形状即可**（见 [[prod-reduction-and-corr]] PC=PnL 形状）。

---

## §21 ★★ 事件时间戳字段 + `nanHandling=ON` = 把「是否发生」当成「发生得多早」（USA shortinterest24 实测，2026-11-16）

### 21.1 现象（4 臂，一次设置对照就分离出根因）

字段 `shrt24_triggertime_2`（Reg SHO 短售熔断**触发时刻**，MATRIX，coverage 0.2573，aC 449）。
同一对表达式只改 `nanHandling`：

| 构造 | nanHandling=ON | nanHandling=OFF |
|---|---|---|
| `group_rank(ts_backfill(x,5), subindustry)` | S **−0.60** / DD **1.039** | S **+0.34** / DD 0.814 |
| `group_rank(ts_zscore(ts_backfill(x,22),252), subindustry)` | S −0.61 | S **+0.05** |

`get_alpha_details` 实测 ON 臂 **longCount=451 / shortCount=2171** ——
字段只覆盖 ~990 只，却持了 2622 只。**符号翻转 0.94、DD 打穿本金。**

### 21.2 机制

**时间戳是正数，`nanHandling=ON` 把 NaN 填成 0，而 0 是最小值** ⇒
`group_rank` / `rank` / `quantile` 把所有「当日未触发」的股票排到最底层**整片做空**。
于是信号从「触发得多早」退化成「**有没有触发**」（≈2100 只无记录 vs 451 只有记录的方向暴露）。

### 21.3 判据与纪律

- **凡字段语义是「时刻 / 日期 / 序号 / 持续时长」且覆盖稀疏**（coverage < ~0.5 或只在事件日有值），
  建 alpha 前必须先问：**缺失值会不会被当成有效最小值/最大值？**
- 正确做法（三选一，按成本排序）：
  1. **`nanHandling=OFF`** —— NaN 保留，`group_rank` 只在有效值内排序（本例一行设置就翻正）；
  2. **`trade_when(<事件是否发生>, <信号>, -1)`** 显式门控，只在事件态持仓；
  3. **把「是否发生」本身当主信号**（此时 ON 的填零反而是有意的，但必须写明这是 presence 信号，
     且要接受它天然是巨额单向暴露）。
- **看 `longCount`/`shortCount` 是否与字段覆盖对得上**，这是最快的体检：
  持仓数 ≫ 字段覆盖数 ⇒ 缺失值被当成了有效值参与排序。
- 本例最终判定：**PROVISIONAL 停投**（4 臂，最好 S 0.34 / DD 0.814 / TO 0.603，
  事件极端稀疏非可交付形态）；撤判条件 = 出现「触发事件条件化」的新用法。
  完整读数见 `tracking/USA/runs/usa_campaign_ledger_20261114.md` §15。

## §22 ★ 长窗平滑只对「存量」信号有效，对「流量/事件」信号是摧毁性的（USA shortinterest43 实测，2026-11-16）

同一骨架 `group_rank(ts_mean(divide(<场所做空股数>, Σ4场所做空股数), W), market)`，**只动窗口 W**：

| W | S | F | TO | 2Y |
|---|---|---|---|---|
| **22** | **+1.02** | 0.57 | 0.0947 | 0.99 |
| 252 | **−0.22** | −0.09 | 0.0132 | −0.78 |
| 504 | **−0.35** | −0.18 | 0.0112 | −0.88 |

**不是「提 2Y 的杠杆」，是把信号抹掉并翻负。**

判据：先问这个信号的经济机制是**存量**还是**流量**——

- **存量型**（做空余额、机构持仓、股本结构、覆盖率）→ 长窗有意义，平滑降噪、提稳定性；
- **流量型**（当日成交量、当日做空股数、订单流、事件触发）→ **长窗 = 换了一个问题**。
  venue-mix 测的是「今天谁在被做空」，252 日平滑等于问「过去一年平均谁在被做空」，机制消失。

**纪律**：几何移植（换窗口）之前，先用一句话写出信号的经济机制属于哪一类。
这一步花 10 秒，能省掉一整批仿真。同类前例：`ts_target_tvr_decay` 在单向事件族上无效（[[signal-type-fingerprints]]）。

## §23 ★ prod 墙的信息源级判定与「缺口-杠杆」算术（EUR sent_matrix / pv47，2026-11-19）

同一数据集换读数后 **IS 全闸、prod 同墙** ⇒ 判「信息源级拥挤」，不是形态问题：

| 读数（earnings_sent_matrix，同一份电话会转录本） | S | 2Y | prod |
|---|---:|---:|---:|
| prob_pos/neg + neutral 组合（wpQjEAPl） | 1.93 | 1.70 | 0.8713 |
| prob 比值（d5Wj0Nx2） | 1.90 | 1.81 | 0.8809 |
| **method1 取反（KPgNqaEk，首作方向信号）** | **1.99** | **1.98** | **0.9229** |
| **method2 取反（78YN09n5，首作方向信号）** | **1.91** | **1.82** | **0.8797** |

**数学判据（可复用）**：prod 有效杠杆实测量级——形状改造（中性化/几何）≈ **0.015/维**，换宇宙 ≈ **−0.03**（且族向依赖）。⇒ **缺口 >0.10 即结构性不可达**，别再烧算子配额；唯一出路 = 换信息源（换数据集）。

**配套两条**：
1. **宇宙的族向依赖再证**：TOPCS1600 对 pattern 形态族是 prod 解药（0.7422→0.7107，SOP #57），但对 pv47 特异收益反转族是**毒药**——2Y 1.06→0.47、S 1.94→1.60。宇宙选择必须逐族实测，不可跨族外推。
2. **2Y 时效闸在 pv47 复现**：六维闭合（12+ 结构 × 4 配置档）+ 十年满仓 + S/F/sub 全可过，2Y 仍封顶 1.05–1.27；逐年定位 2018（S0.35）/2022（S0.87）两个熊市年。与 pv37 同型，**2Y 是信号时效闸，窗口/平滑/设置全救不回**（SOP #4 跨数据集复现）。

## §24 ★ 符号不可跨区移植：残差动量在 EUR pv47 方向反了（2026-11-19）

Blitz/Huij/Martens (2011) 残差动量（特异收益长窗累加，**正向**）在 EUR `pv47` 上：

| 构造 | S | 说明 |
|---|---:|---|
| `ts_rank(ts_sum(pv47_spret,252),252)`（残差动量正向） | **−0.32** | 方向反了 |
| `-ts_rank(ts_sum(pv47_spret,11),252)`（短窗反转） | **+1.94** | 同字段最强档 |

⇒ **同一字段上「长窗动量」与「短窗反转」符号相反**；论文机制（美股）不能假设符号在 EUR 成立。纪律：**任何跨区/跨读数移植，第一批必须含方向对照臂（正/反号各一）**，不可只跑「论文方向」。

## §25 ★★★ 指标定向优化手册（官方口径 + 论坛实证，2026-11-19）

> 口径来源：官方文档 `parameters-simulation-results`（指标定义）、`alpha-submission`（提交测试与 sub-universe 公式）；论坛 `44888868944023`（投资性 Sharpe/流动性残差）、`44713280965527`（GLB 单区拖后腿）、`44734752518039`（降 TO 算子）、`44556201135127`（Fitness 闸）。
> 用途：**按缺口选策略**，不同指标用不同杠杆；先算数学关系，再决定「拿哪个余量换哪个缺口」。

### 25.1 指标定义与数学耦合（先算清楚，再动手）

| 指标 | 官方定义 | 耦合关系 |
|---|---|---|
| Sharpe / IR | `Sharpe = √252 × mean(PnL)/std(PnL)` | 提 S = 提「日均 PnL / PnL 波动」 |
| Fitness | `F = S × √(abs(Returns) / max(TO, 0.125))` | **S、ret、TO 三杠杆；TO<12.5% 时 TO 杠杆失效** |
| Returns | 年化 PnL / 半个 book size（$10M 基准） | 受信号幅度与换手共同决定 |
| Sub-Universe | `sub_S ≥ 0.75 × √(sub_size/univ_size) × S` | **EUR TOP2500→TOP1200 = 0.52×S**（√(1200/2500)×0.75=0.52，与实测 0.519 吻合） |
| Investability | `invest_S ≥ 0.70 × S` | 官方/论坛实测 0.70 倍线；保留比例不足先做流动性残差 |
| 2Y Sharpe | 近两年平均 IS Sharpe（ATOM 免 IS-Ladder 但**必须过 2Y**） | **时效闸**，非形态闸（见 §4 定律） |
| Margin | PnL / 总成交额 | 与 TO 反向；官方建议 ≥4bp（论坛口径 ≥10bp 更稳） |

**两条硬推论**：
1. **S 是双刃剑**：S↑ 同时抬 sub 闸限（0.52×S）与 investability 闸限（0.70×S）⇒ 不要盲目追最高 S，选「刚好过主闸且余量够」的 S。
2. **F 的可行域**：给定 ret/TO，`F≥1.0` 需要 `S ≥ 1/√(ret/max(TO,0.125))`。EUR 低波动族（ret≈3.3–4.5%、TO≈6.5%）该系数 0.54–0.60 ⇒ **需 S≥1.66–1.85**；S 达不到时，**F 缺口是结构性不可达**，不要在 F 上继续投入。

### 25.2 分指标策略表（缺什么补什么）

| 缺口 | 有效杠杆（按实测排序） | 无效/反向（别再试） |
|---|---|---|
| **S 不足** | ① **换信息源/读数**（最大杠杆）② **流动性残差化**（论坛实测 S 0.99→2.17；⚠ **前置判据：`risk_neutralized_sharpe ≫ S` 才做**——institutions6 实测 RN1.02<S1.35 时残差化反而 S−0.13，2026-11-20）③ **加正交快腿**（GLB 单区案例）④ 中性化换标准档（INDUSTRY 常优于 SUBINDUSTRY）⑤ **幅度保留形态**（`group_neutralize` 替代 `group_rank`，ret 7.5%→12.9%）⑥ 窗口/尺度结构梯度（族探针先行） | 幂次猛加（signed_power 2→3 单调恶化）；在单边 beta 暴露上做截面 rank（中性化后归零）；纯参数扫窗 |
| **F 不足** | ① **S 不足时先补 S**（F 与 S 线性）② ret 稀薄时用幅度保留 + 轻时序整形 ③ **TO>12.5% 时降 TO**（decay / `ts_target_tvr_decay` / `hump` / `jump`）④ 提高 ret/TO 比（找「低换手但厚收益」的读数） | TO 已 <12.5% 还继续降（floor 之下无增益）；只加 decay（S 与 ret 同步掉，F 不动）；在 ret 天花板 <4% 的族上硬磨 F |
| **2Y 不足** | ① **换信息源/读数**（时效问题只有换源能解）② 增加近期敏感成分（快腿权重、短窗）③ **降低长窗平滑**（长窗稀释近年信息）④ 降 decay（decay↑ 会伤 2Y）⑤ 事件门控（只在有效状态持仓） | 只拉窗口（66→252 实测 2Y 0.04→−0.04）；只做平滑（S 掉、2Y 不动）；靠换中性化档（只动 0.015–0.03 量级） |
| **sub 不足** | ① 内层分组轴换档（market 轴常抬 sub）② 流动性残差化（同时抬 sub 与 S）③ 幅度保留 + 去极值 ④ 先跑 TOP800 诊断（塌掉=信号住小盘=结构性） | 市值分桶（引入 CW）；外层中性化换档（EUR 实测反而更差） |
| **TO 异常** | 高 TO：`ts_target_tvr_decay(target_tvr=0.06–0.12)`、`hump`、`jump`、轻平滑；低 TO：缩短窗口/提快腿权重/降 decay | 用 hump 压到 1% 以下（TO 破 5% 内部下限且 S 崩）；把 TO 当唯一目标 |

### 25.3 ★ 指标间「换余量」矩阵（破闸的核心操作）

当某闸已过而另一闸不足时，**优先用余量换缺口**，而不是全面重做：

| 已有余量 | 不足 | 可换的动作 | 代价（实测） |
|---|---|---|---|
| **2Y 高（≥1.8）** | S | 缩短慢腿 / 提高快腿权重 / 降 decay / 减平滑 → S↑ 而 2Y↓ | S +0.2~0.4，2Y −0.2~0.4（pv37/risk70/pv47 族） |
| **S 高（≥1.7）** | 2Y | 加长慢腿 / 加平滑 / 换更近敏感读数 | 2Y +0.2~0.5，S −0.2~0.4；S 仍是余量 |
| S 高 | F | 若 TO>12.5%：降 TO（decay 档 / tvr_decay）；若 TO<12.5%：只能抬 ret（幅度保留） | F +0.1~0.3 |
| S 高 | sub | 内层轴换 market / 流动性残差 | sub +0.1~0.3，S −0.05~0.1 |
| 2Y 高且 S 高 | F | 先换 ret（幅度保留/缩短平滑），F 随 S 与 ret 双升 | F +0.1~0.2 |
| 任何 | prod | **只有换信息源/换持仓集合**（宇宙、罕见慢快窗）；保序形变只动 0.015–0.03 | 见 §16.3 三档决策 |

**操作纪律**：每次只换一个余量、只动一个杠杆；换完立刻回读**全部**闸（尤其 sub 与 investability——它们跟着 S 联动），不能只看目标闸。

### 25.4 官方/论坛原文锚点（可溯源）

- 官方 `parameters-simulation-results`：`Fitness = Sharpe × sqrt(abs(Returns)/max(Turnover,0.125))`；「increase Sharpe (or returns) and reduce turnover；improving one normally has an adverse impact on the other」。
- 官方 `alpha-submission`：D1 提交线 F>1、S>1.25、TO∈(1%,70%)、单股权重<10%、self<0.7 或 S 高 10%；sub-universe 公式 `0.75×sqrt(size比)×S`；**ATOM 免 IS-Ladder 但必须过 2Y**；sub 改进 tip：**不要用规模乘数**、**流动性/非流动性分开 decay**。
- 论坛 `44888868944023`：investability 线 = 0.70×S；**流动性残差（20 日 ADV 平方根）S 0.99→2.17**；诊断：`risk_neutralized_sharpe ≫ S` = 被风险暴露拖累，残差化后两者收敛。
- 论坛 `44713280965527`：单区拖后腿的修法是**加正交快腿**，不是扫参数；平滑 + 幂 2 会把稀薄区域的头寸压平/推晚。
- 论坛 `44734752518039`：降 TO 算子清单（tvr_decay / tvr_hump / tvr_delta_limit / hump / trade_when / jump）。

### 25.5 两条实践补充（2026-11-20 institutions6 实测）

1. **流动性残差的前置判据（可省配额）**：先读 `risk_neutralized_sharpe`。`RN ≫ S` ⇒ 信号被风险暴露拖累，流动性残差可能大增益（论坛 KOR 案例 S0.99→2.17）；`RN ≲ S` ⇒ 无可剥离拖累，残差化只加噪（institutions6 实测 S1.35→1.22，三臂全负）。**RN<S 时直接跳过**。
2. **慢变量（报告期/13F 类）没有窗口换档区**：`ts_zscore` 252→66/504、`ts_rank` 66/22 全部同时伤 S 与 2Y（1.35→0.70–1.03），不存在「短窗换 S」的交换区。**2Y↔S 交换只对「时效驱动型」信号成立，慢变量不成立。**
3. **工程坑**：`sqrt(volume*close)` 被 `unitHandling=VERIFY` 拒（量纲 `Unit[TSPrice:2,TSShare:1]`）⇒ 流动性代理用无量纲 `rank(ts_mean(volume*close,20))`。

## §26 ★ 同类别算子全替换闸（按需工具，用户 2026-11-20 裁定）

> 用户原话：「在回测的 alpha 表达式上，每加一个新的算子，就要把同类型的算子都要替换一遍回测，看是否对指标值有改善，比如加了 ts_rank，就要把平台提供给我能用的算子清单里关于截面的算子都替换一下」。
> **裁定**：按需工具（非默认硬闸——每算子触发 7–16 条，全默认会放大回测 5–10 倍）；范围 = 同 category 全替 + no-op 去重。

### 26.1 与 §12「等价替换」的区别

| | §12 等价替换 | §26 全替换 |
|---|---|---|
| 触发 | 判死前 / 近闸时 | 每次**新加一个算子**后（按需） |
| 范围 | 等价实现族（signed_power↔quantile 等） | 整个 category 的同 arity 算子 |
| 目的 | 防「实现路径误判为结构天花板」 | **看同类别里有没有别的算子能改善指标**——含语义变更族 |

### 26.2 工具

`tools/research/operator_swap_matrix.py`（已登记 tools/README.md；守护 `tests/unit/09_core/test_operator_swap_matrix.py`）：
```
python tools/research/operator_swap_matrix.py --list ts_zscore          # 看候选
python tools/research/operator_swap_matrix.py --expr "<基线>" --op ts_rank --out <json>
```
- 数据源：`docs/reference/operators_catalog.json`（MCP `get_operators` 刷出，103 算子）。
- **arity 过滤**：窗口类 `op(x,d)` ↔ 无窗类 `op(x)` ↔ 命名参类 `op(x,name=)` 三者不可互换（否则平台 ARITY 报错）。
- **no-op 去重**（§17.1）：rank 壳内 ts_sum/ts_mean/ts_av_diff 互换逐位相同 → 跳过；rank(rank(x)) 等恒等包装跳过。
  ⚠ **该 no-op 判定只对稠密字段成立**（2026-11-22 DEU news18 实测否证，见 §26.5）：稀疏 / NaN 密集字段
  （news18 声明 cov 0.80、实际有效日远低）窗口内有效天数不是常数 ⇒ `ts_sum = ts_mean × 有效天数` 不是常数倍，
  rank 壳内不再等价 —— 同骨架 `ts_sum` 版 S 0.25 / 2Y 0.85 vs `ts_mean` 版 S 0.31 / 2Y 0.13。
  **稀疏字段的 no-op 一律要实测，不得按 §17.1 直接跳过。**
- **两类标注**：「等价实现族」（如 ts_rank/ts_zscore/ts_quantile/ts_av_diff，相关≈1，Δ主要来自数值路径）vs「语义变更族」（如 ts_decay_linear/ts_delta/ts_arg_max，Δ按新机制解释）——后者往往是真破闸杠杆（§12 GBR news50 的 ts_decay_linear 一次同时抬 S/F/2Y）。

### 26.3 使用纪律

1. **只在"新加算子"时触发**，不是在每次改窗口/换字段时触发（否则组合爆炸）。
2. 生成的替换表达式**必须过 `mcp__wq-brain-http__preflight_expressions`** 才发（一条坏字段整批 kill）。
3. 派发只用 `create_multi_simulation`（用户硬约束），每批 2–10 条，超了拆批。
4. 输出对比表：每行 = `op | S | F | 2Y | sub | TO | Δ vs 基线 | 类别标注`，改善目标闸者进入下一轮定向挖掘。
5. 与三段式的关系：§26 是**表达式层的横向扫描**，与设置轴的纵向扫描（EUR skill `settings-axis-strategy.md`）正交——两者不要同时全跑，先 §26 找到最优算子实现，再进设置轴定档位。

### 26.4 实测样例（2026-11-20，pv20 骨架）

基线 `group_rank(ts_rank(subtract(0, adj_specific_return_crowding_top400),125),industry)`，替换 ts_rank：
- 16 个合法替换（Time Series 窗口类），6 个 arity/no-op 跳过；
- 其中 3 个等价实现族（ts_zscore/ts_quantile/ts_av_diff）、13 个语义变更族；
- 未全部派发（按需工具——本次只生成矩阵验证工具正确性，不是对该族继续投入）。

### 26.5 ★ 首份「单模板完整五层梯度」实测（2026-11-22，DEU news18 N1）

用户 2026-11-21 裁定「ATOM 并没有穷尽，只是对当时用的模板来说穷尽了；换模板后要做**完整的梯度流程**；
**每个模板**都要跑完整的梯度流程回测」。本节是该裁定的第一份执行样本（41 臂有效 + 6 臂作废）。

**模板**：`group_rank(ts_mean(vec_avg(nws18_multiple_comp_ssc),66),sector)`（DEU / TOP500 / D1 生产档）
基线 **S 0.31 / 2Y 0.13**。

| 层 | 覆盖 | 结果 |
|---|---|---|
| L1 Time Series | **15 臂全类别替换** | 只有 4 个 sub 合规；`ts_decay_linear` 唯一四项可用（S0.56/2Y1.36/sub/S0.91/RA3） |
| L2 Group | **6 臂全类别替换** | 全灭（最好 group_scale S0.08） |
| L3 外层/非线性/同集算术 | 6 臂 | **双层中性化 +0.12**（S0.68/2Y1.49）；中轴 subindustry ≫ industry |
| L4 decay | 双基线 × 5 档 | K2@decay8 **2Y 1.61 首过闸** |
| L5 中性化/trunc | 4 臂 | SECTOR 最优 → **S0.54 / 2Y1.64 / TO13.4% / RA2** |

**三条可迁移规律（都在本节首证）**

1. **★ rank 壳的等价塌缩律**：`group_rank(ts_*(x,d), group)` 里只要 `ts_*` 对**当期值单调**
   （`ts_zscore` 是仿射、`ts_quantile`/`ts_rank` 是分位变换），在 rank 壳内**全部塌缩成 `group_rank(x)`**
   —— 实测三者 S 0.82 / 0.84 / 0.85、TO 均 ~58%，逐位接近。
   ⇒ 这类「替换无 Δ」不是巧合也不是等价实现族的巧合，是**信息塌缩**；把它们当三个候选会白烧配额。
   同族判据：**先问「该算子在 rank 壳内是否仍保留时间维度信息」**（均值/斜率/波动/极值位置保留了，
   对当期值的单调变换没有）。
2. **★ `group_rank` 的有界性本身就是换手抑制器**：把它换成输出原始量纲的 group 算子
   （neutralize / zscore / scale / backfill），TO 从 22.5% 跳到 55–62%，S 全崩到 ≤0.08。
   ⇒ 「削换手」与「保信号」在有界排名壳上是同一件事；**想靠换 group 算子降 TO 是反向操作**。
3. **★ decay 不是跨数据集通则的跷跷板**：risk68 上 decay 0→16 是 S −0.16 / 2Y +0.38 的严格单调交换；
   本模板上 S 与 2Y **都在中段同时取峰**（decay 4 S 峰 0.68、decay 8 2Y 峰 1.53），到 16 才双降。
   ⇒ **每次都要画自己那条 decay 曲线**，不要把别区的跷跷板结论套过来
   （与「跨区不外推」同源，这里是「跨数据集/跨信号族不外推」）。

**结论**：本模板天花板 S 0.68；闸口最平衡点 S0.54 / 2Y1.64 / TO13.4% / RA2，S 距闸 1.04、F 距闸 0.78
⇒ **信号强度层不足，模板不可交付**（记 PROVISIONAL，不写死键）。**但"不可交付"与"未穷尽"是两件事**：
本模板已完成五层全替换，可以写「该模板穷尽」；数据集层面还要逐个模板跑完才能写。

### 26.6 二轮补充：news 族 355 臂实测（2026-11-22，news18 十模板 + news20 三模板）

承 §26.5，继续把「每模板全层梯度」推到 news18 全部十模板与 news20 前三模板，累计约 **355 臂**。

**一、天花板必须用梯度后读数（口径纠正）**

| 集 | 首轮 max S | 梯度后 max S | 低估幅度 |
|---|---:|---:|---:|
| news18 | 0.31 | **0.73** | −0.42 |
| news20 | 0.68 | **0.74** | −0.06 |

⇒ 写「某集天花板」必须同时给 `模板数 × 层覆盖 × 臂数`。只写首轮模板读数会**系统性低估 1 个数量级**
（news18 是 −0.42，接近翻倍）。**「模板层穷尽」≠「数据集穷尽」**：news18 十模板可写前者；
news20 只跑 3/10、news104 只跑首轮 ⇒ 只能 PROVISIONAL。

**二、同算子跨模板反转（第 2–5 例，幅度可达 0.25）**

| 算子 | 在 A 模板 | 在 B 模板 | 结论 |
|---|---|---|---|
| `group_backfill` 内嵌 | `ssc` **+0.25**（0.46→0.71） | `bam` −0.19、`acb` −0.23 | 幅度最大的反转 |
| `ts_product` | N2/N3/N7 唯一正臂（0.27/0.65/0.25） | N1/N10 死臂（0.02/−0.01） | 只吃「带质量调节的事件核」 |
| `decay` 方向 | N1/N2/N3 升 decay → S 降 | N4 升 decay → S 升（0.58→0.69） | 不能跨模板套跷跷板 |
| `group_scale/zscore` | N4/M1 抬 S+F、砸 2Y | 其余模板普遍负 | 只在 kurtosis/level 核上有效 |

**三、分类器类字段的有效形态**

`bam`（并购）→ 基线 `ts_mean` 即最优（15/15 替换全劣）；
`acb`（财报发布）→ **`ts_ir`（收益÷波动）** 0.40→0.60；
`nip`（叙事影响力）→ **`ts_kurtosis`（尾部形状）** 0.45→（L2 group_scale 0.65）。
⇒ **分类器/打分型字段的有效信息常在「形状 / 信噪比」，不在均值水平**，先扫 `ts_ir`/`ts_kurtosis`。

**四、同集 add 是合法且能同时抬两维的机制（ATOM 内）**

两条各缺一维的最强腿（`bam` 2Y 1.50 / S 0.68；`ssc-backfill` S 0.71 / 2Y 0.91）
等权 add 后 → **S 0.74 / 2Y 1.19**，两个指标同时提升，RA 3、sub·S⁻¹ 0.83、TO 8.7%。
配比是 S↔2Y 的调参轴（bam×2 → S 0.69 / 2Y 1.30）。
**但门控 `trade_when` 在本族是负杠杆（0.25 / −0.07）**，与 KOR news 相反 ⇒ 机制也要逐集实测。

**五、355 臂后的结论**

NEWS 塔纯单集真实天花板 **S 0.74 / F 0.43 / 2Y 1.30**，距 S 闸（1.58）**0.84**。
已排除路径：10+10 模板 × 五层全替、同集 add（3 种配比 + 乘）、门控、backfill 双层包裹、
winsorize、双层中性化、decay 全档、4 种中性化。
⇒ **属信号强度层不足**（不是配置/机制/调参问题）。**判 NEWS 塔「不可达 S 闸」是安全的；
但不得据此写「news 数据集判死」**（判死要走 §7.6 六维 + 论坛取证，且判死是例外不是默认）。

### 26.7 三轮补充：news104 逐模板梯度（2026-11-22，D1–D4）

承 §26.5–26.6，把「每模板全层梯度」推到第三个新闻数据集 **news104**（11 字段，cov **0.963**，全 VECTOR）。
D1 sentiment / D2 概率差 / D3 confidence / D4 novelty，共 **122 臂**。

**一、★ 同一字段换统计形态可差 0.67 的 S（本轮最硬的一条）**

| 字段 | 最佳形态 | S | 基线 `ts_mean` 的 S | 差 |
|---|---|---:|---:|---:|
| `nws104_confidence` | **`ts_ir`（收益÷波动）** | **0.75** | **0.08** | **+0.67** |
| `nws104_sentiment` | `ts_sum` | 0.40 | 0.34 | +0.06 |
| `nws104_prob_pos−prob_neg` | `ts_sum` | 0.29 | 0.21 | +0.08 |
| `nws104_novelty` | `ts_kurtosis` | 0.50 | 0.41 | +0.09 |

`confidence` 同字段其他形态：`ts_sum` 0.19 / `ts_kurtosis` −0.19 / `ts_std_dev` −0.37 / `ts_arg_max` −0.73。
⇒ **只测 `ts_mean` 会把这个字段判成 0.08 的「死字段」，而它实际能到 S 0.80（配 decay 2）**。
**这是「逐模板 × 同 category 全算子替换」不可省的第一硬证据**（比 §26.5 的 rank 壳塌缩更极端）。

- 叠加设置后：`ts_ir` + decay 2 + SUBINDUSTRY → **S 0.80 / F 0.45 / 2Y 0.26 / TO 7.8% / sub·S⁻¹ 0.88 / RA 3**；
  + STATISTICAL → S 0.81 / 2Y 0.41 / sub 0.49。

**二、★「两个模板复现」不足以升级为数据集级规律（口径纪律，含自我更正）**

本轮曾据 D1（SECTOR 中性化 **+0.23**）与 D2（**+0.24**）判定「SECTOR 是 news104 数据集级杠杆」，
**第三个模板 D3 上 SECTOR 是 −0.27（0.80→0.53），结论当场作废**。
⇒ 升级路径必须是「**≥3 个互异模板复现 + 无同族反例**」，两模板只够写「候选规律」。
这与 §7.6 六维穷尽闸、跨族不外推是同一族纪律的不同层级。

**三、news104 的最高读数（全 NEWS 塔 660 臂内的新高）**

| 件 | S | F | 2Y | TO | sub·S⁻¹ | RA |
|---|---:|---:|---:|---:|---:|---:|
| `ts_ir(confidence)` @decay2 SUBIND | **0.80** | **0.45** | 0.26 | 7.8% | 0.88 | 3 |
| `ts_ir(confidence)` @STATISTICAL | **0.81** | 0.40 | **0.41** | 10.8% | 0.49 | 3 |
| `ts_sum(sentiment)` @SECTOR | 0.63 | 0.34 | 0.79 | 5.4% | 0.86 | 3 |
| `ts_sum(prob差)` @SECTOR | 0.53 | 0.27 | 0.44 | 5.3% | 0.98 | 3 |
| `ts_kurtosis(novelty)` @decay8 | 0.51 | 0.25 | 0.36 | 5.8% | 0.55 | 3 |

⇒ NEWS 塔天花板由 §26.6 的 **S 0.74 / F 0.43** 上修到 **S 0.81 / F 0.45**，距 S 闸（1.58）**0.77**。
**但注意**：`confidence` 是本轮唯一把 S 推到 0.8 档的字段，F 0.45 距闸仍差 0.55，2Y 0.26–0.41 距闸 1.2 以上
⇒ 仍属**信号强度层不足**，不改变「NEWS 塔不可达」的结论方向。

### 26.8 四轮补充：risk68 数据集完整穷尽（2026-11-23，八模板 × 五层，~150 臂）

用户 2026-11-23 新规：**「先把一个数据集的完整流程回测做完，再开下一个数据集」**。
据此把 risk68 的八套模板全部补到 L1–L5（此前只有 R5 一条线跑完五层）。

**一、★ 「一个数据集没做完就写天花板」的第二次实证代价**

| | 旧值（只测 R5 一条线） | 八模板全穷尽后的真值 | 低估 |
|---|---:|---:|---:|
| max S | 1.29 | **1.51**（R1 STAT×d0） | **−0.22** |
| max 2Y | 1.19 | **1.67**（R1 STAT×d0） | **−0.48** |
| max F | 0.78 | **1.37**（R1 NONE×d0） | **−0.59** |

⇒ 与 §26.6 news18 的 0.31→0.73 同型。**「数据集天花板」必须等到八套模板 × 五层全部跑完才能写。**

**二、★ S ↔ sub 跷跷板的量化斜率（risk68 实测）**

R1（`group_rank(ts_zscore(rsk68_weight_edadv,252),sector)`）的中性化 × decay 全表给出：

| S | 1.51 | 1.48 | 1.44 | 1.38 | 1.27 | 1.16 | 1.04 |
|---|---:|---:|---:|---:|---:|---:|---:|
| sub·S⁻¹ | 0.344 | 0.419 | 0.437 | 0.457 | 0.472 | 0.543 | 0.49 |

⇒ **S 每 +0.1，sub/S 约 −0.02**（单调）。**风险线滑块（decay/中性化轴）在 S 与 sub 之间只有交换、没有交集**：
- 最高 S 1.51 时 sub·S⁻¹ 0.344（需 0.474）
- sub 合规（R8 0.543）时 S 只 1.16
**判据：若某配置的 sub·S⁻¹ 已 <0.40，再沿 S 方向推只会更差，应改换字段/机制而不是继续调轴。**

**三、★★ 两条新入册的「算子 no-op」**

| 算子 | 条件 | 证据 |
|---|---|---|
| `ts_target_tvr_decay(x, target_tvr=0.25)` | **实际 TO < target** | R7 与 R1 读数**逐位相同**（12 臂全对得上，含 6 种中性化 × 5 档 decay） |
| `truncation` 0.05 / 0.10 / 0.15 | 外层是 `group_rank`（输出有界 [0,1]） | R1 上 3 臂读数**逐位相同**（S1.44 / F1.11 / sub0.63） |

⇒ **tvr 类算子只在「实际 TO > target」时才有效**；给低换手信号套 tvr 是白烧一层。
**truncation 在 rank 壳核上通常不 binding**，不要拿它当「降集中度」的杠杆（与 GBR risk68 的「trunc 空杠杆」结论一致）。

**四、模板级判死清单（risk68）**

| 模板 | 判定 | 依据 |
|---|---|---|
| R2 `ts_delta(·,66)` | 死 | S 峰 0.84 时 2Y −0.08 / sub 0.24；sub 合规时 S 0.43 且 TO 72% / RA 5 |
| R3 `ts_std_dev(·,66)` | 死 | 峰 0.69（NONE）时 sub 0.45 ✗ / 2Y −0.15 / TO 1.1% |
| R4 `mean/std` 信噪比 | 死 | 峰 0.23，远低于闸 |
| R6 三层 group 嵌套 | 死 | 天花板 S 1.18，全部 sub·S⁻¹ ≤0.435，被 R1 完全支配 |
| R7 tvr | ≡ R1 | 算子 no-op |
| R1 / R5 / R8 | 活但不足 | S 1.51 / 1.29 / 1.16，均无同时过 S+sub 的点 |

⇒ **risk68 判死（模板层八套全穷尽）**，记 PROVISIONAL（未写死键）。

### 26.9 五轮补充：★★ `coverage = 0.0` 不是「无数据」（2026-11-23，risk71 实证）

**事件**：`get_datafields(risk71)` 返回 **10 个字段全部 `coverage = 0.0`**，
我据此判「数据层排除」并向用户报告。随后按「判死前必须实测」纪律跑了 2 臂探针 —— **当场推翻**：

| 字段 | alpha | S | F | 2Y | TO |
|---|---|---:|---:|---:|---:|
| `residualized_return_top2500` | `e7aZY2Ed` | **−1.12** | −0.31 | −0.37 | **90.5%** |
| `eur_minvol1m_specific_return_dsrt` | `pwae2z3j` | −0.44 | −0.13 | −0.04 | 30.6% |

两个字段**都产出了完整读数** ⇒ 数据真实存在，`cov=0.0` 只是**报告层假象**。
同型先例：DEU 的 GROUP 字段（`country`/`currency`/`exchange`/`market`）同样报 cov=0.0，实际完全可用。

**入册纪律（修正 §7.6 三档里的「数据层排除」前置条件）**

> **判「coverage=0 ⇒ 数据层排除」之前，必须先用 ≥2 臂探针实测。**
> `cov=0.0` 只在「探针也无读数」时才能作为排除依据，**不得单独作为排除/判死依据**。
> 探针形态用系列里最常用的字段 + 2 种互异统计形态（避免单一形态失败被误当成「字段无数据」）。

这条与「★轻易不要把数据集字段判死」「判死标记一律不得单独作为依据」是同一族纪律的**数据层版本**：
cov 是**平台元数据**，而判死需要**读数证据**。

**附带发现（risk71 的信号形态）**：`residualized_return_top2500` 裸 `ts_zscore(·,252)` 是
**S −1.12 的强反转 + TO 90.5%**。⇒ 方向清晰（取反 S≈+1.12），**换手是唯一硬敌**
（TO 闸 0.70 vs 实测 0.905）。这类「强反转高换手」面板的主线不是找信号，而是**压换手**：
长窗平滑（ts_mean 252）、`hump`/`tvr`、门控（trade_when）三条路径。

### 26.10 六轮补充：risk71「TO 属性死」+ tvr 有效性的完整判据（2026-11-23）

**一、★★ `tvr` 类算子的有效性判据（与 risk68 合成完整对照）**

| 数据集 | 实际 TO | `target_tvr` | 是否 binding | 证据 |
|---|---:|---:|---|---|
| risk68 R7 | ≈11% | 0.25 | **否（no-op）** | R7 与 R1 读数**逐位相同**（12 臂全对上） |
| risk71 | **90.4%** | 0.65 / 0.50 / 0.35 | **是** | TO 90.4% → **34.6% / 27.0% / 19.5%** |

> **判据：`ts_target_tvr_decay` 只在「实际 TO > target_tvr」时生效**。
> 实际 TO < target 时给低换手信号套 tvr 是**白烧一层**（risk68 实证）；
> 实际 TO > target 时它会把 TO 压到 target 附近（risk71 实证：target 0.65 → 实测 0.346，比 target 还低）。

**二、★★★ risk71 = 「TO 属性死」的结构性证据**

`residualized_return_top2500`（DEU 残差收益面板，aC=17）：

| 形态 | S | 2Y | TO | sub |
|---|---:|---:|---:|---:|
| 裸反转 `ts_zscore(−f,252)` | **+1.27** | **+0.58** | **90.4%** | **+0.37** |
| tvr 0.65 | 0.64 | −0.14 | 34.6% | −0.11 |
| tvr 0.50 | 0.54 | −0.22 | 27.0% | −0.06 |
| tvr 0.35 | 0.44 | −0.24 | 19.5% | −0.04 |
| `ts_decay_linear(·,5)` | 0.71 | 0.04 | 47.3% | **0.00** |
| `ts_decay_linear(·,22)` | 0.49 | −0.21 | 22.0% | −0.03 |
| `ts_mean(·,5)` | 0.50 | −0.14 | 41.0% | −0.18 |
| `ts_mean(·,252)` | **−0.23** | −0.01 | **8.9%** | −0.26 |

**规律：TO 从 90.4% 往下压的每一步，S / 2Y / sub 三项同时恶化；`ts_mean(252)` 直接把 S 从 +1.27 打到 −0.23（跨零翻转）。**
⇒ **信号的信息载体就是「日频反转」这个高换手属性本身**，不存在「压 TO 而保信号」的路径。

**三、入册判据（第一版，待更多样本校准）**

> **「TO 属性死」的机械判据**：
> ① 裸信号（最锐形态）TO > 0.85；
> ② 任意一种 TO 抑制手段（tvr / decay_linear / ts_mean / hump）使 **|S| 下降 > 0.4**；
> ③ 抑制后 **sub 仍 ≤ 0**（不是「不够 0.474S」，而是**转负**）。
> 三条同时命中 ⇒ 判 TO 属性死，**不必再调中性化 / 分组轴 / 配置档**（轴层救不了 TO 载体）。

⚠ 与本轮此前的印象相反：此前「TO 抑制是温和负杠杆」（如 news 族 decay 抬 2Y 压 S 一点点）。
**risk71 是「TO 就是信号」的极端案例** —— 必须逐集实测，不能按「TO 通常可以压」的先验去调。

**四、附加：`coverage = 0.0` 的数据层判据见 §26.9**（与本节独立，别混）

### 26.11 七轮补充：VECTOR/MATRIX 类型纪律必须机械化（2026-11-23，risk60 实证）

**同一 RISK 类目内，两个数据集的字段类型可以完全相反，且失败方式相反**：

| 数据集 | 字段类型 | 裸用（不降维） | 错误地包 `vec_avg` |
|---|---|---|---|
| risk68 | 全 **MATRIX** | 正常 | **整批静默失败**（返回 None，无报错） |
| risk60 | 全 **VECTOR** | **整批 ERROR**：`Operator ts_zscore does not support event inputs` | 正常 |

**事故经过**：我在 `tracking/DEU/reference/datasets/risk60.md` 建档时**已经写下**「5 字段全 VECTOR ⇒ 必须 `vec_avg`」，
但同一轮派批仍用裸字段，8 臂全废。⇒ **「记在档案里」不等于「派批时生效」**。

**处置（机械前置，不靠人记）**：
1. 派批前对**新数据集**必跑 `preflight_expressions(auto_fix_vector=True, dataset_id=<ds>)`
   或 `fix_vector_fields(dataset_id=<ds>)`，用返回的 `fixed_expressions` 派发；
2. `get_datafields` 的 `type` 列是唯一事实源 —— **同一 category 内必须逐集确认，禁止按类目推断**；
3. 失败指纹对照：**静默 None** ⇒ 错包了 `vec_*`（字段是 MATRIX）；**`does not support event inputs`** ⇒ 漏包了 `vec_*`（字段是 VECTOR）。

> 与 §26.9（`cov=0.0` 不是无数据）合起来看：**元数据两列（`type` / `coverage`）都各自有一个「反直觉」陷阱**，
> 且方向相反 —— `coverage` 会**误杀有数据的字段**，`type` 会**漏杀类型不匹配的表达式**。
> 两者的共同处置都是「**派批前的机械检查**」，不是文档纪律。

### 26.12 八轮补充：★★ `group_rank` 的「取反位置」决定结果（2026-11-23，risk60 T1 实证）

同一信号的三种写法，读数完全不同：

| 写法 | 表达式（risk60 `rsk60_offer`，窗 252） | S | F | sub |
|---|---|---:|---:|---:|
| 原向（不取反） | `group_rank(ts_zscore(vec_avg(f),252),sector)` | **−0.79** | −0.48 | −0.38 |
| **内层取反**（rank 之前） | `group_rank(ts_zscore(subtract(0,vec_avg(f)),252),sector)` | **+0.43** | 0.20 | +0.50 |
| 外层取反（rank 之后） | `subtract(0, group_rank(ts_zscore(vec_avg(f),252),sector))` | 预期 ≈+0.79 | — | 预期 ≈+0.38 |

**根因**：`group_rank` 把信号压到有界 [0,1]，因此**补集组合不是原组合的负向**（权重和不为零）。
- 内层取反 = 换了一条输入序列（`−f`），zscore 后再 rank，得到的是**第三种组合**；
- 外层取反 = 对原组合的权重整体变号，才是真正的多空翻转。

**纪律**
1. 任何「反向 / 取反 / 负向」实验，**必须写明取反位置**（rank 前 / rank 后 / 设置层的 reverse），否则 Δ 表不可比；
2. 想验证「论文说高费率跑输」这类**方向性假设**，正确写法是**保持原向读数看符号**（S −0.79 即假设成立），
   而不是改成内层取反去追正 S —— 后者会静默换成另一个组合，S 从 0.79 掉到 0.43 却看不出原因；
3. 若要交付「做空高费率」的 alpha，用**外层取反**保留原来的组合结构。

> 这条与 §26.5「rank 壳等价塌缩律」互补：那条讲「壳内什么算子会塌缩」，这条讲「壳外取反会改变组合结构」。
> 两条都指向同一个事实：**`group_rank` 不是恒等变换包装，它会改变信号的组合几何**。

### 26.13 九轮补充：★★ `CONCENTRATED_WEIGHT` 的解法是提高 decay，不是 trunc（2026-11-23，risk60 T1 实证）

**背景**：risk60 T1 的 `SECTOR × decay 4` 版本 RA 三项失败
（`LOW_SHARPE` / `LOW_FITNESS` / **`CONCENTRATED_WEIGHT`**）。按老经验先试 trunc —— **四档全 no-op**：

| trunc | alpha | S | F | 2Y | sub | RA |
|---|---|---:|---:|---:|---:|---:|
| 0.02 | `A1xX163Q` | 1.13 | 0.85 | 1.66 | 0.94 | 3（仍含 CW） |
| 0.04 | `58JK83E6` | 1.13 | 0.85 | 1.66 | 0.94 | 3 |
| 0.08 | `mLanPoMX` | 1.13 | 0.85 | 1.66 | 0.94 | 3（含 CW） |
| 0.10 | `9ql5qbdK` | 1.13 | 0.85 | 1.66 | 0.94 | 3 |

**四档读数逐位相同** ⇒ trunc 对 CW 与对 S/F 均**完全 no-op**（risk68 之后第 2 次独立复现）。

**真正有效的是提高 decay**：

| 配置 | S | F | 2Y | TO | sub | RA | CW |
|---|---:|---:|---:|---:|---:|---|---|
| SECTOR × **decay 4** | 1.13 | 0.85 | 1.66 | 6.3% | 0.94 | 3 | **有** |
| SECTOR × **decay 8** | **1.12** | **0.84** | **1.65** | **4.4%** | **0.95** | **2** | **无** |

⇒ **decay 4→8 只让 S/F/2Y 各掉 ≤0.02，却把 CW 彻底消掉**（尖峰持仓被平滑）。

**入册规律**

> **`CONCENTRATED_WEIGHT` 的处理顺序：① 提高 decay（首选，代价 ≤0.02）；② 换更平滑的信号形态
> （如 `ts_mean` 替 `ts_max_diff`）；③ 才考虑 trunc —— 但在 `group_rank` 壳上 trunc 通常已 no-op。**
> 判据：若 trunc 从 0.08 降到 0.02 读数逐位不变 ⇒ trunc 通道关闭，别再扫它。

**第二次复现的 trunc no-op**（risk68 三档 + risk60 四档，共 7 臂逐位相同）说明：
**`group_rank` 的有界输出让权重天然不触 trunc 上限**，所以 trunc 在 rank 壳上基本是死设置。

---

## §26.14 ★ 「只差一个指标」是假象：prod 必查 + PnL 三线归因（用户 2026-11-23 明令）

用户规则：**只要还有一个指标没过闸，就必须先查 prod 并做 PnL 归因，再判断有无办法推进。**

### 为什么 RA 读数不够

`get_alpha_details` 的 `is.checks`（→ `failed_ra_count`）**不含 prod correlation**。
所以「RA 只 1 项 LOW_SHARPE，只差 S 0.29」这种陈述**天然缺少两道信息**：prod 是否撞墙、
S 里有多少是风险因子 beta。前者决定这形状能不能交，后者决定 S 还有没有可挖的余量。

### 三步固定动作（只读，零仿真配额）

1. `check_correlation(alpha_id, correlation_type="production")`（缓存优先，48h 内不重触发）。
2. `get_alpha_pnl` → 三条曲线各自年化：`pnl`(raw) / `risk-neutralized-pnl` / `investability-constrained-pnl`，
   并算 `corr(raw, RN)`。
3. `get_alpha_yearly_stats` → 逐年 `S / TO / pnl / longCount / shortCount`。

### 判据

| 读数 | 含义 | 动作 |
|---|---|---|
| `RN 年化 S ≈ raw`（比值 >0.85） | 信号是特质 alpha | S 还有真实余量，可继续推 |
| **`RN 年化 S ≪ raw`（如 0.81 vs 1.32）** | **六成 S 是因子 beta** | 抬 raw S 要抬 beta，不是抬 alpha；优先级大幅下降 |
| `corr(raw, RN) < 0.70` | 同上，量化版 | 同上 |
| 逐年 S 集中在 2–3 个压力年 | 「压力年 alpha」 | 抬 S 需跨年广度（换信息源），不是加窗 |
| prod 高桶仅 1–2 对 | 近重复件指纹 | max 仍 FAIL ⇒ 换信息源，别在窗口上耗 |

### 实证：DEU risk60 T1（借券费率水平反转）

`LLKoVa5e` = `group_neutralize(ts_mean(subtract(0,vec_avg(rsk60_offer)),66),sector)` @SECTOR/d8：

| 项 | 读数 | 判读 |
|---|---|---|
| RA | 1（仅 LOW_SHARPE） | 看似「只差 S」 |
| **prod** | **0.844 FAIL**（高桶仅 2 对在 [0.8,0.9)） | 近重复件，**信息源级墙** |
| raw S | 1.32 | 与平台 1.29 一致 |
| **RN S** | **0.81** | **真 alpha 只有一半** |
| IC S | 1.27 | 可投资性不是瓶颈 |
| 逐年 | 2014 2.54 / 2018 2.53 / 2022 3.02 vs 2017 0.25 / 2020 0.25 / 2021 0.49 | 压力年 alpha |

⇒ 两条独立证据指向同一结论：**这个 PnL 形状已被生产池占据，且其强度主要来自风险因子暴露**。
**模板级终判：关闭，不再投入**（换窗/换轴/换外层都只是在同一形状上打转）。

### 与既有条目关系

- 补 `docs/experience/01_platform_gates.md` 的口径：**RA 清单 ≠ 提交闸全集**。
- 与 §26.5「rank 壳等价塌缩」互补：那条讲壳内算子会塌缩，这条讲**报告口径会漏项**。
- 关联 `[[alpha-attribution-must-include-pnl-and-yearly]]`：逐年零持仓/压力年集中同样是数据层判据。

## §27 ★★★ 梯度扫描纪律：按「层 × 类内全覆盖」判穷尽，不按臂数（2026-11-23，insiders1 45 臂实证）

### §27.1 事故：把参数层扫完就写了「全轴穷尽」

`insiders1`（EUR/TOPCS1600）在 11-06~11-08 跑了 30+ 臂——窗口 22/44/66/88/126/252、
幅度轴（quantile/winsorize std/signed_power）、设置轴（universe 3 档、中性化 2 档、decay 0/4/13/20）、
外层 `group_scale`——然后台账写下「天花板 1.14，全轴穷尽」。

复审核对**平台读回的真实表达式**、拆成 9 层后发现：**4 个算子类别轴一格未扫**
（L1 `vec_*` 折叠 / L4 `ts_*` / L5·L8 外层 `group_*` / 分组轴）。
补齐 45 臂（5 批）后：S 仍 1.14，但 **2Y 0.71→0.86、sub 0.94→0.99、robust 0.71→0.79**，
并证伪两条跨集外推律。

⇒ **根因不是「少跑几个臂」，是没有机制回答「缺哪几个臂」** —— 全靠人记。

### §27.2 层级杠杆实测（同一机制、单层单变量）

| 层 | 类内极差 ΔS | 性质 | 结论 |
|---|---|---|---|
| **L4 时序 `ts_*`** | **1.40**（−0.26~1.14） | 语义层 | 稀疏事件流 `ts_sum` 不可换（见 §27.4） |
| **L5/L8 外层 `group_*`** | **0.77**（0.37~1.14） | 语义层 | 两级 group 组合是结构要件，换 `group_rank` 双崩 |
| **L1 `vec_*` 折叠** | **0.40**（0.74~1.14） | 语义层 | 7 算子全扫；方向逐集不同（见 §27.5） |
| 窗口 | 0.37（0.77~1.14） | 半语义 | **S↔2Y 严格跷跷板**（44=S 峰 / 88=2Y 峰，中段无双峰解）|
| 分组轴 | 0.11（S）/ **0.20（2Y）** | 半语义 | sector > market > industry > subindustry > country ≡ exchange（EUR 该机制）|
| tail q / winsorize std | 0.01~0.02 | 参数层 | 一轮即可 |
| decay | 0.01 | 参数层 | 只改 TO（5.28%→4.38%），S/2Y 互抵 |
| **truncation** | **0.00** | **no-op** | 见 §27.4 |

**判据**：类内 ΔS > 0.30 ⇒ 语义层（必须全类替换）；ΔS < 0.05 ⇒ 参数层（**禁止精调**）。

### §27.3 六条纪律（已落代码，`src/wqb/config.py::GRADIENT_*` + `tools/research/gradient_coverage.py`）

| # | 纪律 | 落点 |
|---|---|---|
| A | **覆盖率审计**：每条表达式拆 L1…L13，逐层报 `tested/missing/coverage`；「穷尽」只能表述为「已测子集内穷尽」 | `gradient_coverage.py audit` |
| B | **settings 与算子臂分家**：`decay/truncation/universe/中性化/...` 是批级参数 ⇒ **一值一批**，绝不与表达式臂同批（2026-11-23 实测同批放同码臂白烧 1 臂位） | `GRADIENT_BATCH_LEVEL_SETTINGS` + `plan` 的 `settings_plan` |
| C | **扫描顺序固定 = 杠杆量级降序**：L1→L4→L5/L8→分组轴→窗口→参数层。历史上顺序是反的（先调参，最后才碰算子） | `GRADIENT_SCAN_ORDER` |
| D | **派批前离线 lint**：幽灵算子（`ts_weighted_decay`）/ 命名参数写成位置参数（`group_backfill(...,2.0)`）会 **CANCEL 整批**；本地可查 | `gradient_coverage.py lint`（委托 `wqb.expression.op_arity`）|
| E | **闸门导向验收**：每层给「类内最优 + Δ 表 + 离闸差多少」，limit 一律取平台下发值（不另立数字）；语义层全锁定、最优离闸仍差 >0.3 ⇒ 判 PROVISIONAL 停手 | `audit` 的 `gate_gaps` |
| F | **收割归属**：`harvest_multisim_alphas` 一次拿 code+metrics；同批 children 顺序 = 提交顺序（同码返回同一 alpha id，已实测） | `--exprs` 直接吃 harvest JSON |

**与 §26 的分工**：§26（`operator_swap_matrix`）管「**换哪一个算子**」；
本节管「**这一层还有哪几个没换、下一批该发什么、设置轴怎么排**」。
另：`tools/gates/operator_coverage_audit.py` 管**面**（全平台哪些算子从没用过），
本工具管**点**（每条表达式每层的同类可换子集）。

### §27.4 已确认的 no-op 律（换上去读数逐位相同，别再烧臂位）

1. **最终层是 `rank()`/`group_rank()`/`quantile()` 时，`truncation` 是结构性 no-op**
   ——insiders1 `trunc 0.05` 与 `0.08` 三臂读数逐位相同（`QP0RN5vX` ≡ `A1xXeJqW`）。
   机理：rank 已把权重摊平，单票权重远低于截断线。历史台账里的 `trunc 0.08` 从来不是调出来的值。
2. `group_rank` **之前**的任何单调变换（constant/quantile/signed_power/winsorize）。
3. **下游有 rank 吸收尺度时 `vec_sum ≡ vec_avg`**（risk60 + insiders1 两集复现）。
4. 内层已有 `ts_backfill` ⇒ 外层 `group_backfill` 不改变读数（risk60）。
5. **稀疏事件流的 L4 不能换 `ts_mean`/`ts_decay_linear`/`ts_rank`/`ts_ir`/`ts_av_diff`**：
   insiders1 同内核实测 1.14 → 0.24 / 0.07 / −0.26 / 0.04 / −0.24，三个伴 TO 145–147%。
   机理：`ts_sum` 保留事件频率，`ts_mean` 把它除掉；rank/decay 把稀疏脉冲打散成逐日跳变。

### §27.5 两条被证伪的跨集外推（第二次复现同一教训）

| 外推的「律」 | 来源集 | 反例 |
|---|---|---|
| `vec_max > vec_avg > vec_min`（尾部有定价力）| GBR risk60（借券费率）| **insiders1 反向**：avg≡sum(1.14) > max(1.13，且 robust 0.69 FAIL) > min(1.07) ≫ stddev/range(0.76/0.74)。申报金额的尾部=个别大额噪声，均值=典型规模才是信号 |
| 「换更小宇宙更好」（非流动小票留存超额）| USA FF56620（`ILLIQUID_MINVOL1M`）| insiders1 单调递差：TOPCS1600 0.93 > TOP2500 0.54 > TOP800 0.27。EUR 的 TOP*N* 是市值截断，**不等于流动性筛选** |

⇒ **折叠轴方向由「该字段的尾部是否有经济含义」决定**；**杠杆效应是（数据集 × 机制）级事实**。

### §27.6 用法

```bash
# 审计（覆盖率 + 平台闸门缺口）
python tools/research/gradient_coverage.py audit --alpha-id A1xXeJqW
# 缺臂计划（语义层优先、自动跳 no-op、settings 单独列）
python tools/research/gradient_coverage.py plan --alpha-id A1xXeJqW --max-arms 10 --out logs/_plan.json
# 派批前离线 lint（幽灵算子 / 命名参数）
python tools/research/gradient_coverage.py lint --exprs logs/_plan.json
```

三处数字口径：扫描顺序/参数层/no-op 律 = `src/wqb/config.py::GRADIENT_*`（唯一事实源）；
层归属 = 算子 `category` + 嵌套深度（结构近似，非经济语义判定）；闸门缺口 limit = 平台下发值。

---

## §26.15 ★★ 梯度测试的六条通用规律 + 八条优化落地（2026-11-23，~450 臂实证）

> 覆盖范围：risk60（5 机制族 ~261 臂）、risk88（10 臂）、insiders `insider_agg_matrix`（10 机制族 163 臂）、PV 探针（18 臂）。
> **产出诚实结论：0 颗可交付**，但留下 4 个「只差 S」的 RA-1/RA-2 件与本节六条规律。
> 机械落地：`tools/gates/gradient_stop_gate.py`（D1–D4）+ `src/wqb/config.py::GRADIENT_SCAN_ORDER/GRADIENT_NOOP_LAWS`
> + `tools/research/gradient_coverage.py`（覆盖率/缺臂/lint）。

### 规律 1：S 是三层结构，只有信息层决定天花板

| 层 | 实测可调幅度 | 杠杆 |
|---|---|---|
| 表达式层（算子/窗口/外层） | **±0.1–0.3** | 内层 16 全替、`signed_power`、`hump`、`vector_neut` |
| 配置层（中性化/decay/trunc） | **±0.2–0.5** | 轴 6 档、decay 6 档、trunc 4 档 |
| **信息层（机制 × 字段集）** | **不可调** | risk60 **1.25** / risk88 **0.54** / insiders **0.95** |

实证：risk60 上 40 个不同结构/配置全落 1.20–1.29；insiders 十个机制全落 0.49–0.95。
⇒ **判据（已机械化为 D1）**：L1 全替后 `max_S < 1.0` 且极差 `< 0.7` ⇒ 判「信息量不足」，**不投 L2–L5**。

### 规律 2：三条跷跷板，「单点最优」是幻觉

| 跷跷板 | 实证 | 读数 |
|---|---|---|
| **F ↔ 2Y** | 轴层 5 次复现 | NONE：F 1.09–1.49 / 2Y 0.00–0.14；SUBIND：2Y 1.65 / F 0.18–0.59 |
| **S ↔ 2Y** | risk60 T2 | STATISTICAL S 0.98 / 2Y 1.20 ↔ SECTOR S 0.77 / 2Y 1.62 |
| **S ↔ prod** | risk60 T4 **严格对立** | SECTOR S 1.29 / prod **0.87** ↔ SUBIND S 1.16 / prod **0.68** |

⇒ 判据（D3）：best S / best F / best 2Y 三点不重合 ⇒ `SWING` ⇒ **该模板不可交付、不必再调参**。

### 规律 3：杠杆跨核可移植性极低（本轮踩 4 次）

| 杠杆 | 核 A | 核 B |
|---|---|---|
| `signed_power(·,2)` | risk60 T2：**S +0.11 / F +0.36** | risk60 T3：sub 0.69→0.57 **纯损害**；insiders N1：**no-op** |
| `ts_mean` 平滑 | risk60 T4：S 1.25→1.24 几乎无损 | insiders N1：S **0.66→0.20** 杀 |
| 提高 decay | insiders N2：TO **−44pp**、S +0.01 | risk60 T2：**完全 no-op**（TO 已 1.3%） |
| trunc 调低 | risk60 T1/T3：no-op | risk60 T2：**反向**（RA 2→4） |

⇒ **纪律**：每个新核必须重测全部杠杆，**结论必须带「核指纹 + Δ」登记**，禁止跨核继承。

### ★ 规律 4：平滑是否杀 S 取决于**信号的时间分布类型**（本轮最重要的新规律）

| 类型 | 判型方法（L1 内即可判） | 平滑效果 | 实例 |
|---|---|---|---|
| **变动型**（人数、事件频率） | `ts_mean22` 相对裸核 **ΔS < −0.2** | **平滑即杀** | N1 0.66→0.20 |
| **水平型**（相对历史偏离、集中度） | ΔS ≥ 0 | **免费降 TO** | N2 TO −44pp 且 S +0.01；N4 裸核 0.17→`ts_mean66` 0.72 |

⇒ **先判型再平滑**：变动型 → 用长窗 `ts_sum`（保频次）压换手；水平型 → 直接用 `ts_mean`/decay。

### 规律 5：prod 只随 PnL **形状**移动，不随参数移动

- 有效自由度只有 **3 个**：**残差对象**（0.816→0.679，仅换字段）、**同集多腿 add**（0.60→0.54 且 S 升）、
  **中性化粒度**（与 S 严格对立）
- 换窗口 / decay / trunc 对 prod **零位移**（risk60 T1 五个窗口 prod 不动）
- **同集双残差 add 是唯一同时抬 S/F 并降 prod 的杠杆**（S 1.15→1.26、F 0.69→0.85、prod 0.60→0.54）
⇒ 纪律：**prod 只在形状上投入**，不要为窗口/参数测 prod（占全局单并发槽）。

### 规律 6：六个「结构型死因」—— 命中即停，别调参

| 死因 | 判据 | 实例 |
|---|---|---|
| TO 属性死 | 裸 TO >0.85 且任何压制使 \|S\| 掉 >0.4 | risk71 |
| 近常数信号 | 横截面差异小 ⇒ sub 崩 | insiders N3（买占比）/ N6（高管独占度） |
| **已标准化字段再 zscore** | **TO 0.00 / S 0.00** | insiders N7 `directional_indicator` |
| 聚合型 group 算子 | TO 70%+ / RA 5–6 | **10 次复现** |
| rank 壳内分位变换 | 塌缩成 `group_rank` | **4 次复现** |
| 有界变量的凸变换 | no-op（逐位相同） | insiders N1 `signed_power` |

### 八条优化的落地位置（可执行）

| # | 优化 | 落地 |
|---|---|---|
| 1 | **L1 极差止损闸** | `tools/gates/gradient_stop_gate.py --l1-range`（D1） |
| 2 | **杠杆登记表（核指纹 + Δ）** | `src/wqb/config.py::GRADIENT_NOOP_LAWS` + `gradient_coverage.py` 的 noop 告警；跨核结论必须带核指纹 |
| 3 | **字段类型/单位/标准化三查前置** | `gradient_stop_gate.py --lint-expr`（D4：裸常数 UNITS / 已标准化再 zscore / VECTOR 未降维） |
| 4 | **配置层先行（TO 带 5–20%）** | `gradient_stop_gate.py --to-band`（D2） |
| 5 | **三点检测** | `gradient_stop_gate.py --three-point`（D3） |
| 6 | **prod 只在形状上投入** | 本节规律 5（纪律）+ `gates/nemesis_prescreen.py`（判断是因子换皮还是新信息） |
| 7 | **同集多腿优先于换轴** | 本节规律 5 第 3 条（唯一三赢杠杆）+ ATOM 允许同集 add（`atom-pyramid-rules`） |
| 8 | **机制新颖 ≠ 信息量新** | 选区阶段先量化「字段携带多少可定价信息」（aC / 覆盖 / 更新频率 / 是否已聚合），见 `06_atom_mining.md` |

> **第 8 条的反例（本轮最贵的一课）**：insiders 十个机制**全部**取自论坛与论文（官方工作坊 T1–T9 +
> Heckmann 2026 / Lakshadweep-Lee 2001 / Cohen-Malloy-Pomorski 2012 等，论文闸 41 篇 / 33 作者 PASS），
> 结构互异、每条都跑过梯度，**仍无一破 S 1.0** —— 因为 `insider_agg_matrix` 的字段是**已聚合的均值/合计**
> （丢了逐笔申报细节）。**决定天花板的是字段的信息含量，不是模板的新颖度。**
