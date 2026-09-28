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

**唯一有效解法 = 降 truncation**（0.08 → 0.04/0.02）+ 平滑（`ts_mean` / `ts_decay_linear`）。
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
