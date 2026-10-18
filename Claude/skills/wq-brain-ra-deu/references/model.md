# DEU × model（组合分支）

> 回到 [DEU 区域流程](../SKILL.md) · [DEU profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/DEU.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region DEU --category model`

<!-- profiles:cell-panel:start -->
**状态**：probe（跟区域入场 probe-only）　**分组**：MODEL　**类别卡**：model

**涉及数据集**：analyst_earnings_ibes、model106_probe_r54、model216、model238、model25、model250、model25_model216、model264、model28、model36、model53、predictive_starmine

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | DEU | 区域 settings.json |
| universe | TOP500 | 区域 settings.json |
| delay | 1 | 区域 settings.json |
| neutralization | SUBINDUSTRY | 区域 settings.json |
| decay | 4 | 区域 settings.json |
| truncation | 0.08 | 区域 settings.json |
| pasteurization | ON | 区域 settings.json |
| unitHandling | VERIFY | 区域 settings.json |
| nanHandling | OFF | 区域 settings.json |
| maxTrade | OFF | 区域 settings.json |
| language | FASTEXPR | 区域 settings.json |
| visualization | false | 区域 settings.json |
| startDate | 2013-01-01 | 区域 settings.json |
| endDate | 2023-12-31 | 区域 settings.json |

### 阈值

- Mode B 主闸 sharpe / fitness：1.25 / 0.8（thresholds_override:DEU；下限锁生效，实时值看 explain）
- 其余阈值跟区域 thresholds.json（本组合无覆盖）

### 证据（2026-10-04 只读汇总）

| 回测 | RA 全过 | prod 已测 | 其中低于上限 | 判死 | 胜绩 |
|---|---|---|---|---|---|
| 528 | 65 | 0 | 0 | 5 | 2 |

主要数据集（回测数）：predictive_starmine（154）、analyst_earnings_ibes（115）、model264（63）、model216（49）、model238（32）、model25（32）、model28（25）、model250（24）

### S1 字段理解

- 分清分数水平与分位 / 概率标签：标签类在 GBR 2Y 崩（GBR-DLRISKFREE-LABEL-DEAD）
- 看字段 description 判断是不是别人做好的成品因子；成品因子的热门字段 prod 墙最硬
- 窗口（类别卡，均在白名单内）：level 22/66/252；change 5/22

### S2 生成

- **类别通用原语**（类别卡，跨区）：
  - industry residual: group_zscore so the factor is not the sector bet
  - quality minus yield: a slow fundamental residual, not the raw score
  - invert only when the economic story is crowding or mean-reversion
  - never ship a lone rank(model_score) as a concept
  - model disagreement: ensemble variance across model outputs
  - regime conditional: model signal only in specific market regimes
- **跨区结论**（GLB/USA/EUR；negative）：成品模型分数的热门字段在多区撞 prod 墙（users 高的字段 prod 必超上限）（证据：GLB techindi_model predicted_first_quantile 系 qMNZX1o1 prod 0.7686（GLB profile）；USA mdl177 / book-value 145 颗同族 ACTIVE；EUR×model 62 条判死） <!-- lint:const-ok 证据原文 -->
- **禁止**（类别卡）：禁止使用裸 rank(model_score)（必须 group_neutralize 或 industry residual）
- **禁止**（全局锁定）：禁止两条独立信号腿相加：加权（0.4×A + 0.6×B）、等权 add(rank(A), rank(B))、中缀 + 都算；第二个数据集只以条件（trade_when / if_else）、分组（group_rank / bucket）或残差（regression_neut / vector_neut）入场
- **禁止**（全局锁定）：禁止 ts_event_* 系列（平台没有）与幽灵算子；字段名逐一经 get_datafields 验证

### S4 改进（按顺序试：组合 → 类别卡 → 全局）

1. [全局] 判「无解 / 天花板」前先扫等价算子替换：signed_power → quantile、ts_scale → quantile / normalize。数值路径不同，一次动多个闸（含 prod，要读全部闸）（KOR/GLB 复现：KOR other466 signed_power→quantile：2Y 1.51→1.56、prod 0.6544→0.6397；GLB quantile 替 ts_scale：S +0.20、F +0.06、prod 0.475→0.565（DEC-72）） <!-- lint:const-ok 证据原文 -->
   - 注意：效应量逐区实测，禁外推；quantile 只收 1 个参数
2. [全局] 强但撞 prod 墙的快信号：用一个经济子集门控（trade_when 进 >0.5 出 <0.4 的慢变量，或 rank(cap)>0.2 ∩ 子集）只在子集里持仓（GLB/ASI/IND 复现：GLB-DL20D-SUBSET-GATE-FAMILY-20260921（prod 0.82→0.60–0.67）；ASI LLNgdpw2 / 88jaV5lv；IND ZYbqREW1 / levk5JYN（prod 0.54–0.55）） <!-- lint:const-ok 证据原文 -->
   - 前提：未门控的基础信号 IS sharpe 不低于 2.5、fitness 不低于 1.5（GLB 2026-09-27 铁律：门控只修 prod / robust，不造强度）；慢信号门控后换手会升，只用于快信号
- 提醒：prod 与 self 两个端点都取 max、都过线才可提；不改持仓的降 prod 杠杆（hump、加大 decay）会把 self 推爆（EUR wave274） <!-- lint:const-ok 证据原文 -->
- 提醒：设置是强度闸：nanHandling / maxTrade / decay / 中性化换档等于换信号，跨档结果不可比（IND 行为族 S 2.19→0.46） <!-- lint:const-ok 证据原文 -->
- 提醒：decay 匹配信号速度：快信号上 decay 越大越差；decay 0 与 1 逐位相同，只留一个 <!-- lint:const-ok 证据原文 -->
- 提醒：prod 墙先看直方图分单颗钉子 / 密墙 / 可破三型，再决定换分母、换设置档或分组轴（决策表 D0-P 诊断前置） <!-- lint:const-ok 证据原文 -->

### S5 提交前

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region DEU --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| DEU-AEI-NONMOMENTUM-DEAD | analyst_earnings_ibes 反转/低波/量价/换手方向 |  | analyst_earnings_ibes | inferred | <!-- lint:const-ok 证据原文 -->
| DEU-AEI-PUREPOSITION-F-CEIL | analyst_earnings_ibes 纯位置线（52周位置+zscore 反转） |  | analyst_earnings_ibes | inferred | <!-- lint:const-ok 证据原文 -->
| DEU-MODEL216-COVERAGE-WEAK-2Y | model216（armpreferredrevisionscore 系） |  | model216 | inferred | <!-- lint:const-ok 证据原文 -->
| DEU-MODEL250-CLOSED | model250 |  | model250 | inferred | <!-- lint:const-ok 证据原文 -->
| DEU-MODEL53-CREDIT-DEAD | model53 |  | model53 | inferred | <!-- lint:const-ok 证据原文 -->

### 胜绩

| 条目 | 机制 | 设置与骨架 | 数据集 | 归属 |
|---|---|---|---|---|
| DEU-M238-FULLGATE-WIN | model238 |  | model238 | inferred | <!-- lint:const-ok 证据原文 -->
| DEU-M264-STARMINE-HYBRID-WIN | model264 × starmine hybrid（amihud 方向预测 × 修订腿） |  | model264 | inferred | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
### 字段画像结论（2026-10-08）

`UNUSABLE` 6498｜`UNTESTED` 1526｜`DEAD` 120｜**`WEAK` 15**｜`DEAD_STATIC` 8｜`DEAD_TURNOVER` 6（共 8173）

**★ 本类别有全 DEU 最多的 WEAK（15 个 = 全部 WEAK 的 58%）**：
`mean_estimate_change_pct_f12m_earnings_14d_4`（**S1.57 / 2Y1.44 / sub0.97**，即已提交 `58gkLAkk` 的字段）｜
`mdl216_armpreferredrevisionscore`（**S1.45**，VECTOR）｜
`mean_estimate_change_pct_f12m_ebitda_14d_4`（**S1.41 / 2Y1.22 / sub1.20**）｜
`mdl238_industry_rank`（1.33）｜`mdl250_malta_eq_score`（1.33）｜`mdl25_eq_v4_2_1_v6`（1.18）

**★ VECTOR 处理**：`model216`（45 个）**全为 VECTOR** ⇒ 必须 `vec_*` 聚合，且**聚合算子是搜索维度**（实测 `vec_max` 0.43 > `vec_avg` 0.35）。

**★ 已否证（按字段族判，不按数据集判）**：
- `model264`：单信号最高 0.74；历史 1.94 **全来自多腿** ⇒ 不建议投入。
- `model26` 的 **`mdl26_*`（模型因子）**：历史全崩 ⇒ 不建议。
- **★ 但 `model26` 的 `avg_estimate_change_pct_*` 族例外**（**唯一有效机制的载体**）：
  `avg_estimate_change_pct_year1_earnings_90d` → **S1.27 / 2Y1.33 / sub0.75 ⇒ 进 WEAK**（W170 实测，2026-10-08）。
  ⇒ **"数据集判死"必须落到字段族粒度** —— 同型错误此前在 `analyst93` 上犯过一次。
`model28/36/53`（信用/违约风险，67 字段）已实测**最高 S1.08**，核心字段换手 **0.022~0.028（静态）**。

**开批前**：优先 `mdl216_*`（用 `vec_max`）与 `predictive_starmine` 的 536 未测 —— 后者是**唯一产出过 alpha 的数据集**。

---

## ★★★ `model106`（晨星式评级）—— DEU 第二强机制（2026-10-13 WANL28–30）

**字段**（全 MATRIX，cov 1.0）：`mdl106_stars`(0-4星) / `global_evaluation`(−2~+2) / `rv`(估值 −2~+2) / `fnb`(坏消息因子，越高越差) / `fmb`(熊市敏感度) / `fmb/fnb/rv` 方向需实测定。

**实测（30 结构全谱）**：
| 机制 | 最好读数 | 判定 |
|---|---|---|
| **`rv` 估值评分水平量 × 框架(1/210)+桶轴** | **S0.90 / F0.64 / 2Y1.67 / TO0.142** | **强但差 0.68 够不到闸**；reverse 精确 −0.90（单调） |
| `ts_delta(stars,66)` 评级变化 | S0.77 / 2Y0.37 | 方向有效，2Y 弱 |
| `rv` × DEU核心 / industry / oth455 / MARKET中性化 | 0.31–0.70 | **全部更差** |

**四条铁律：**
1. **`rv` 的信号在「行业内相对估值」里**：换 MARKET 中性化 S 0.90→0.53（信号被市场中性化洗掉）；SUBINDUSTRY 是最优档。
2. **DEU 核心结构（quantile+decay）在 rv 上有害**（0.66 vs 0.90）⇒ **结构最优性三分实证**：框架赢（eps_y1）/ 核心赢（starmine）/ 都不赢（rv、残差动量）——**移植结构前必须逐字段实测**。
3. `winsorize(std=4)` 逐位不变（保序变换不改门槛指标，第 3 次实证）。
4. `fnb` 框架 0.05 / reverse −0.05 ⇒ 坏消息因子在 DEU 无信号。

**⇒ model106 判定：`rv` 是 DEU 第二强独立机制，但天花板 0.90 不可达闸；除非引入新结构范式，否则关闭。**

---

## ★★★ `model238` / `model264` / `analyst7` 判死（2026-10-14 WANL35–38）

| 数据集 | 机制 | 最好读数 | 判定 |
|---|---|---|---|
| **`model238`** | 偏好/筛选排名 0–100（`change_in_preference_rank`、`*_screening_rank`、`*_factor_alignment_rank`、`*_peer_investment_concentration_rank`） | **筛选排名族**（收口批 WANL39）：`global_screening_factor_alignment_rank` **S0.99 / F0.73 / TO0.10**；`mdl238_global_screening_rank` S0.97、`ts_delta(·,66)` S0.95/2Y0.95；**偏好变化族**：`ts_delta(global_chgpref,66)`+industry → **S0.81 / 2Y1.66 ✅**；水平量 S0.44；同业集中度族 −0.09~−0.14 | **两条子线剖面互补：一条 S0.99 但 2Y0.49，一条 2Y1.66 但 S0.81** ⇒ 跨不过双闸，不可达 |
| **`model264`** | 技术指标趋势概率（380 字段、78% α=0） | `mdl264_1l_ist` −0.22 / `mdl264_1l_lda` −0.11 | 与 `dl_riskfree_returns` **同族**（ML 概率），判死 |
| `analyst7` | 分析师估计水平/计数（355 可用） | `est_12m_bps_lowerednum_4wks` −0.53（反向 +0.53） | 弱 ⇒ 判死 |

**★ `model238` 的价值与教训**：
- 它是**唯一把 2Y 抬过闸**（1.66）的字段族——机制是「**偏好变化**」（`ts_delta` 构造，与 DEU 唯一有效机制「预期变化率」同源，都是**变化量**而非水平量）。
- 但 **S 封顶 0.81**；15 种窗（delta 22/66/126/252）/轴（sector/industry）/桶粒度变体全扫无效。
- **⇒ 再次实证「变化量 > 水平量」**（水平量 0.44 → 变化量 0.81，+0.37）。

**⇒ model 塔在 DEU 的可挖面：`predictive_starmine`（已挖，同腿）× `model106`（rv 0.90）× `model238`（0.81）——全部封顶，无可提交。**

---

## ★★★ 低覆盖大池判死（2026-10-14 WANL44）—— `model109` / `multifactor_return_pred`

**背景修正**：`coverage<0.6 剔除` 是**区域启发式，不是平台限制**（`preflight_expressions` 证明低覆盖字段可正常仿真）。据此复查发现两个**从未探测**的大池：

| 池 | 字段 | 覆盖分布 | 族数 | 语义 | 实测最好 |
|---|---|---|---|---|---|
| **`multifactor_return_pred`** | **648** | 0.3–0.6（492 个在 0.5–0.6） | 15 | ML 收益预测**置信度/分桶/对冲预测** | `short_term_20d_quantile5_confidence_score` **S0.48**（TO 0.450 偏高） |
| **`model109`** | **544** | 0.2–0.6（511 个在 0.5–0.6） | **87** | 基本面/流动性/杠杆/修订比/增长 | `mdl109_es_ebit_fy1_d1m`（修订上下比）**S0.45**；`mdl109_matrix_bookp` S0.24 / **2Y0.78** |
| `model262` / `model307` / `model144` | 159/11/2 | 0.2–0.5 | 2/3/1 | Compustat 预测 / 区域销售占比 / 预测分数 | 未出信号 |

**⇒ 判死**：双结构 × 跨 9 族，max |S| 0.48 ⇒ **model 塔在 DEU 无剩余可挖面**。

---

## ★★★ `model216` blended-revision 族 = **已占用腿**（2026-10-14 未采样族扫描发现）

**背景**：未采样族扫描（`scripts/sweep_unsampled.py`）在 `WANLS49` 出现**全程最佳读数**，且该批前 6 名全来自 `model216` 的 blended-revision 族（此前**从未测过**）：

| 字段 | 结构 | S | F | 2Y | corr(·, `2rjrMZ25`) |
|---|---|---|---|---|---|
| **`mdl216_preferredblendedrevisionfy1percent`** | A 级框架 | **1.45** | **1.21** | 1.12 | **0.8879 ⇒ 同腿** |
| `mdl216_armglobalcombinationscore` | 框架 | 0.68 | 0.40 | 0.87 | 0.7980 ⇒ 同腿 |
| `mdl216_armsector1rank` / `armregion1rank` | 核心/框架 | 0.69 / 0.63 | — | 0.93 / 0.79 | 0.7504 / 0.7450 ⇒ 同腿 |
| `mdl216_revenueblendedrevisionfy1percent` | 框架 | 0.60 | 0.32 | 1.22 | **0.6856（唯一未超线）** |

**⇒ 该族 = DEU 唯一那条「预期变化率」腿的另一种表达**（与已提交的 `2rjrMZ25` 相关 **0.89**）。
**即便把 S1.45 推到 1.58，也会被 self 相关（0.89 > 0.7）拦下**；唯一 <0.7 的 `Grg13NYP`（0.686）S 仅 0.60。
**⇒ `model216` 不可提交。这是「DEU 只有一条腿」的第 4 次独立验证**（前三次：eps_y1 全变体 0.999 / starmine 0.991 / model238 变体）。

**★ 方法论铁律**：**扫描出的强读数必须立即做 PnL 同腿判定**（`GET /alphas/{id}/recordsets/pnl` → Pearson，零配额）——只看 S 会把「同腿的另一表达」误判成新发现。

<!-- profiles:manual:end -->
