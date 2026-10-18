# DEU × analyst（组合分支）

> 回到 [DEU 区域流程](../SKILL.md) · [DEU profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/DEU.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region DEU --category analyst`

<!-- profiles:cell-panel:start -->
**状态**：probe（跟区域入场 probe-only）　**分组**：Analyst　**类别卡**：analyst

**涉及数据集**：analyst44、analyst47、analyst7、analyst9、analyst93、analyst_consensus、analyst_factor_signals

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
| 284 | 0 | 0 | 0 | 4 | 0 |

主要数据集（回测数）：analyst93（115）、analyst_factor_signals（94）、analyst7（48）、analyst44（8）、analyst9（8）、analyst47（8）、analyst_consensus（3）

### S1 字段理解

- 分清 actual_*（已实现、事后）与 mean_estimate_* / flash（预测、前瞻）：IND analyst_consensus 前 16 条全灭的真因是用了 actual（DEC-77）
- VECTOR 先 vec_avg / vec_count 聚合；JPN 下 vec_* 外再套 ts_* 会报错
- 窗口（类别卡，均在白名单内）：monthly 22/66；quarterly 66/252

### S2 生成

- **类别通用原语**（类别卡，跨区）：
  - revision surprise: change in FY1/FY2 vs the stale level
  - dispersion: disagreement across estimates, not the consensus mean
  - breadth vs magnitude: how many estimates moved, not how far the mean moved
  - horizon gap: FY2 minus FY1 as a growth-expectation residual
  - rating momentum: upgrade/downgrade frequency vs historical baseline
  - target price gap: current price vs consensus target (upside/downside)
  - estimate acceleration: second derivative of estimate revisions
- **跨区结论**（USA/GLB/HKG/KOR/EUR/DEU/GBR；negative）：flash / pretax 一致预期动量族只在 IND 有效，别的区 ／S／ 都在 1.07 以下（证据：waves probe_flash_eps_20260919 / probe_pretax_20260919：USA ≤0.09、GLB ≤0.08、HKG 0.64、KOR ≤1.07、EUR ≤0.96、DEU ≤0.72、GBR ≤0.54） <!-- lint:const-ok 证据原文 -->
- **跨区结论**（KOR/USA/DEU；negative）：分析师主信号族普遍撞 prod 墙（证据：KOR analyst10/16/44/consensus（RULES §G）；USA-ANALYST44-BREADTH-DEAD-EP-PRODWALL（E/P z prod 0.93）；DEU analyst93 prod 饱和） <!-- lint:const-ok 证据原文 -->
- **禁止**（类别卡）：禁止使用裸 rank(estimate)（必须 ts_delta 或 group_zscore）
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
| DEU-AN93-CROSS-COMPOSITE-DEAD | analyst93 cross-field/cross-dataset composite structures | analyst93（及 DEU 全域）不再尝试跨字段/跨集任何复合结构（含 bucket/group/价差）；只用单字段平滑与组内变换。 | analyst93 | inferred | <!-- lint:const-ok 证据原文 -->
| DEU-AN93-PROD-SATURATED | analyst93 recprofitabilityprev_profitability2 family (prod-s | DEU 该族停止打磨与提交尝试；任何 an93 变体在投入结构工作前先查 prod（prod-first 硬前置）。按拥挤族处理：不再投入 >2 条/波。 | analyst93 | inferred | <!-- lint:const-ok 证据原文 -->
| DEU-AN93-RELATIVE-DEAD | analyst93 relative_profitability series (rec/nonrec x analys | DEU an93 的 relative_profitability1-4 全系（16 字段）不再投回测槽位；relative 化方向判死。 | analyst93 | inferred | <!-- lint:const-ok 证据原文 -->
| DEU-CROSSSET-RESCUE-DEAD | cross-dataset rescue legs within DEU (analyst93 x fhp) | DEU 的 analyst93 主信号不要配 fhp/other455 辅助腿；DEU 内跨集正交腿不成立（跨集救援仅限跨区域组合时再评估）。 | analyst93 | inferred | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
### 字段画像结论（2026-10-08）

`UNUSABLE` 3655｜`UNTESTED` 550｜`DEAD` 81｜**`DEAD_STATIC` 11**｜`DEAD_TURNOVER` 5｜**`WEAK` 5**｜**`DEAD_COUNT` 4**｜**`ALIVE` 1**（共 4312）

**★ 全 DEU 唯一的 ALIVE 在本类别**：`eps_y1_estimate_change_3mo`（单信号 **S1.66 / 2Y2.14 / sub0.98 / n_sg 60**）。

**★ 两个已判死的失败模式高度集中**：
1. **`DEAD_STATIC` 11 个里 7 个是 `anl93_*`**（`{accuracy,consistency,correv,estimator}_*`，换手 **0.019~0.029**）⇒ 「分析师技能元数据」整类是**静态结构属性**。但注意 `anl93_recprofitabilityprev_*_profitability2` 族（换手 0.079、历史单信号 1.30）是**活的** —— **别把整个 analyst93 判死**。
2. **`DEAD_COUNT` 4 个全在 `analyst7`**（`rec_lowerednum_4wks` S0.01/2Y1.90 等）⇒ 「分析师数量」类 = 教科书级「2Y 有 S 无」。

**WEAK 池**：`netprofit_y1_estimate_change_3mo`（S1.32 / 2Y1.21 / **sub1.00**，仅 2 条样本 ⇒ 值得补测）｜`anl93_recprofitabilityprev_analyst_profitability2`（1.30）｜`eps_y2_estimate_coeff_var`（1.23 / **2Y1.49**）。

**开批前**：`analyst7` 的 395 未测里约 41% 是 `*num*` 计数类（`DEAD_COUNT` 形态）⇒ 先按名字过滤；`analyst44` / `analyst9` 属换手爆表族。
### ★★★★★ 决定性更新（2026-10-13 晚）：**2Y「墙」是结构问题，不是字段问题** —— 已产出全闸通过 alpha

**背景**：自造 40 条结构（`group_rank` / `ts_mean` / `ts_delta` 级联 / `ts_sum` 累积 / `group_zscore` / 各轴）**2Y 全部 ≤1.17**，一度误判「本集 2Y 不可破」。

**★ 转折**：检索仓库历史产物 → `output_report/DEU_gem_templates_after_skeleton_audit.md` 载有 **2026-10-07 已过闸的 DEU A 级框架**。
**同字段、同设置，只换结构**：

| 结构 | S | F | 2Y | 判定 |
|---|---|---|---|---|
| `group_rank(eps_y1_estimate_change_3mo, sector)` | 1.81 | 1.61 | 1.12 | 卡 2Y |
| 自造 40 条（ts_mean / 级联 / ts_sum / 各轴…） | ≤1.81 | ≤1.61 | **≤1.17** | 全卡 2Y |
| **A 级框架** | 1.65 | 1.47 | **1.69** | ✅ 全过（`9qWX78vV`） |
| **★ HYBRID（框架 × `group_rank`）** | **1.77** | **1.61** | **1.83** | ✅ **最强**（`WjLEOqLP`） |

**★★ A 级框架（三要素缺一不可）**：
```
bf(F) = ts_backfill(F, 1008)
group_neutralize(rank(add(ts_mean(bf,1), ts_mean(bf,210))),        # 双窗：短腿必须 = 1
                 bucket(rank(ts_mean(bf,252)), range="0,1,0.05"))  # 单桶轴：粒度 0.05
```
**★★ HYBRID 变体（当前最优形态）= 把框架的 `rank` 换成 `group_rank(..., sector)`**：
```
group_neutralize(group_rank(add(ts_mean(bf,1), ts_mean(bf,210)), sector),
                 bucket(rank(ts_mean(bf,252)), range="0,1,0.05"))
```
⇒ 同时拿到 S（group_rank 载重）与 2Y（双窗 + 桶轴）。

**★ 已到手的两颗（ANALYST 塔，DEU/D1，全闸 0 失败）**：
| Alpha | 结构 | S | F | 2Y | self | prod |
|---|---|---|---|---|---|---|
| **`WjLEOqLP`** | HYBRID | **1.77** | **1.61** | **1.83** | 0.3437 ✅ | 0.6510 ✅ |
| `9qWX78vV` | 框架 | 1.65 | 1.47 | 1.69 | 0.3014 ✅ | 0.6197 ✅ |

**⚠ 二者同腿（均为 `eps_y1_estimate_change_3mo`）⇒ 互相关系数 0.9372 ⇒ 只能提交其一**（平台 self 只算已提交 OS 池）。
**⚠ prod 余量小（0.651 vs 0.7）且逐日漂移 ⇒ 提交当日必须 `check_correlation(refresh=True)` 复核。**

**★ 框架 × 同族字段的可迁移性（批 W-ANL5/6，20 条）**：`eps_y1_change` 1.77 ✅；
`netprofit_y1` 最好 **1.36**、`eps_y2` **1.30**、`netprofit_y2` 1.08、`revenue_y1` 1.01、`revenue_y2` 0.75、
`*_q1_change_1mo` 0.23~0.60、`eps_revision_magnitude` 0.50 ⇒ **框架可迁移（2Y 都 ≥0.26）但 S 过不了 1.58**。
⇒ **`analyst_factor_signals` 的可提交上限 = 1 颗**（与 2026-10-07 战役「≈205 次测试 → 0 颗」相比，本轮靠框架首次过闸）。

**★★★ 方法论铁律（本轮最重要）**：
1. **墙常在「结构」不在「字段」** —— 开新战场前**必须先检索仓库内历史战役产物**（`output_report/DEU_*`、skill 的 `win_recipes`、`.workbuddy/memory/*`），不要从零自造结构。
2. **HYBRID（框架 2Y 机制 + `group_rank` S 载重）是本区最优形态模板**，可迁往其它数据集/类别先试。
3. `ts_delta` 双窗级联只对**水平量**有效；对**变化率**字段连续三次崩塌（本轮 0.91/0.83）；`ts_sum` 累积迁移同样失败。
4. `analyst7`（608 字段）实测无门槛候选（最优 S1.18/2Y0.28；高 2Y 全为计数类且 S≈0）；`analyst93` S 天花板 1.31；`analyst44/9/48/47` 属元数据/计数/时间戳族（DEAD）。

### ★★ 合规判据精确化 + 双窗 `add` 消融实验（2026-10-13 用户质疑后）

**质疑**：A 级框架里的 `add(ts_mean(bf,1), ts_mean(bf,210))` 是否属被禁的 `add(A,B)` 混信号？
**判定：不违规。** 规则禁的是「**两条独立信号腿**」= **不同字段/不同数据集/不同机制**相加。
本式两个腿是**同一字段**的 1 日窗 + 210 日窗 ⇒ **单信号结构化（多窗口平滑）**，不是混信号。
（真违规反例：`blRnKEk6` = 4 字段 / 3 数据集 add。）

**消融实验（批 W-ANL9，全部去掉 `add` 只留单窗口）**：

| 核心 | S | F | 2Y |
|---|---|---|---|
| **含 add：`add(ts_mean(bf,1),ts_mean(bf,210))`** | **1.77** | **1.61** | **1.83** |
| `bf` / `ts_mean(bf,1)`（短腿单窗） | 1.56 | 1.29 | 1.18 |
| `ts_decay_linear(bf,210)` | 1.40 | 1.13 | 1.20 |
| `ts_mean(bf,66)` | 1.37 | 1.07 | 1.22 |
| `ts_mean(bf,105)` | 1.26 | 0.95 | 0.78 |
| `ts_mean(bf,210)`（长腿单窗） | 0.97 | 0.65 | 0.29 |

**⇒ 去掉 `add` 后最好仅 S1.56 / 2Y1.22，全不过闸。**
**⇒ 长腿单用 0.97（几乎无效）、短腿单用 1.56、相加 1.77/1.83 ⇒ 真正的多窗口互补增益，不是两个独立信号叠加。**
**⇒ 双窗 `add` 是承重结构，合规且不可删。**

### ★★★ 跨类别 + 最后一片未测面实测（2026-10-13，批 W-ANL7/8/12）：**框架救不活其它类别**

**A 级框架 / HYBRID × 跨类别字段**（`HYBRID` = 把框架的 `rank` 换成 `group_rank(..., sector)`）：

| 字段（类别） | S | 2Y |
|---|---|---|
| `snl27_relpopularity1`（sentiment） | **0.64** | 0.96 |
| `credit_risk_leverage_score_d1`（model） | 0.53 | 0.59 |
| `snl27_totaldomains`（sentiment） | 0.46 | 0.77 |
| `stable_boundary_trade_count_21d_active`（institutions） | 0.44 | 0.75 |
| `mdl28_..._distance_to_default`（model） | 0.29 | 0.51 |
| `event_sentiment_score`（news） | 0.23 | 0.34 |
| `count_institutional_buyers_security`（institutions） | 0.02 | 0.45 |
| `rsk60_crowding` / `oth47_organic_traffic` / `annualized_pd_1_month_jc7` / `herfindahl_index_transactions` | −0.05 ~ −0.17 | −0.65~0.59 |
| `loaned_*` / `transaction_count_main` / `loan_rate_volatility_main`（shortinterest3） | **−0.18 ~ −0.44** | 负 |
| `lending_fee_bid_rate`（risk60） | **−0.52** | −0.24 |
| `count_institutional_sellers_security`（institutions） | −0.50 | 0.03 |

**★ 批 W-ANL12（最后一片未测面）**：`pattern_scores`（PV 未点亮塔，**504 个 MATRIX 字段、cov 1.0、alphaCount 0 全平台零竞争**，历史仅用自造结构测过 15 条 max S 0.42）在框架下 **全部 |S| ≤ 0.09**，且 TO 0.21–0.36（图表形态相似度天然高频）；
`insider_agg_matrix.directional_indicator` −0.10、`risk88.alternative_market_cap_usd` −0.03（均 cov 1.0）。

**⇒ 三条结论**：
1. **借券族（shortinterest3/risk60）在 DEU 无信号甚至反向**（−0.18~−0.52）—— 第三次确认族级否证。
2. **零售关注度（sentiment27）0.64 是跨类别最优，但仍远不及格**；「零竞争」≠ 有信号（`pattern_scores` 504 字段第二次实证）。
3. **A 级框架不是万能钥匙**：它只在**携带信号的字段**上把 2Y 从 1.1 抬到 1.8；对无信号字段（跨类别 29 + pattern_scores 10 = 39 个）毫无作用（框架改的是「结构」，信号的有无仍取决于「字段」）。

**★★ DEU 定案（本轮 12 批 / 103 条合规表达式）**：
- **可提交产出 = 1 颗**：`2rjrMZ25`（**10 算子**，S1.77/F1.61/2Y1.83/prod0.651/self0.3437/robustness PASS）；prod 漂移退路 `9qWX78vV`（prod 0.6197、稳健性更优、已审计）。
- **已穷尽**：`analyst_factor_signals` 全 6 类字段族、`analyst7`(608)/`analyst93`/`analyst44/9/48/47`、跨类别 29 字段、`pattern_scores` 10 字段。
- ⇒ **要凑 10 颗必须换区域或引入新数据源；DEU 已实证触顶。**

---

## ★★★ 第二轮重构（2026-10-13 晚，WANL21–25）：DEU 只有一条腿

### 1. DEU 核心结构 vs A 级框架：**逐字段不同**

「DEU 核心」= `group_neutralize(group_rank|group_zscore(ts_decay_linear(quantile(add(ts_mean(bf,5), ts_mean(bf,200))), 8), 轴), 桶轴)`（来自 `GrOWMGp0`，把 starmine 从 0.97 抬到 1.81）。

| 字段 | A 级框架 | DEU 核心 | 胜者 |
|---|---|---|---|
| `eps_y1_estimate_change_3mo` | **1.77 / 2Y1.83** | 1.55 / 2Y1.55 | **框架** |
| `netprofit_y1_estimate_change_3mo` | 1.36 | 1.27 | 框架 |
| `predictive_starmine` `mean_estimate_change_pct_f12m_earnings_14d_4` | 0.97 | **1.81** | **核心** |

**⇒ 结构最优性逐字段实测；「某个结构更强」是字段属性，不是普适规律。**

### 2. 三个新否证（本轮）

- **`oth455` 内轴 × analyst 全族：max S 1.46**（低于框架 1.77）⇒ starmine 上的高 S 增益**字段特异、不可迁移**。
- **`model30` StarMine 族**（`star_new_eps_smart_estimate_*` / `surprise_prediction_*`，cov 0.62–0.67、α=0 真空白）：框架/核心/`ts_delta` 共 10 结构 **max S 0.74** ⇒ **SmartEstimate「水平量」在 DEU 无信号**；只有「变化率」字段有效（水平量已被定价，变化量才含增量信息 —— 与 DEU fundamental 类同规律）。
- **未点亮类别 10 字段**（`sentiment27` 排名族 / `news17` 情绪 / `news50`，全部 `vec_avg` + DEU 核心）：**max S 0.59**，`snl27_topranking` −0.33、`mws50_ens` −0.49 ⇒ 未点亮类别在 DEU **无信号**，其「低竞争」源于**无数据/无信号**（约半数未点亮类别数据集在 DEU 覆盖率 = 0：earnings/option/macro/socialmedia/imbalance）。

### 3. ★★ 决定性实证：跨数据集同机制 = **同一条腿**

6 个候选逐日 PnL（2579 日）直算互相关：

| 对 | corr |
|---|---|
| `2rjrMZ25`(eps_y1·框架) ↔ `kqJqQL08`(eps_y1·bucket0.1) | **0.9992** |
| `2rjrMZ25` ↔ `9qWX78vV`(eps_y1·pure rank) | **0.9992** |
| `2rjrMZ25` ↔ `P0M0vX3p`(eps_y1·核心 w1=1) | 0.9989 |
| `2rjrMZ25` ↔ `e767nR9O`(eps_y1·核心 5/200 d8) | 0.9988 |
| **`2rjrMZ25` ↔ `npApoGRx`（predictive_starmine）** | **0.9910** |

**⇒ 三条铁律：**
1. **eps_y1 的一切结构/轴/算子变体互相关 0.9988–0.9992** ⇒ 改结构不产生新腿，**一条腿只能出 1 颗**。
2. **跨数据集同机制 = 同一条腿**（starmine 与 analyst 的「预期变化率」相关 **0.991**）⇒ **修正 2026-10-08 的推断**：「同机制跨数据集迁移**有效**」≠「迁移能出**新腿**」。迁移只换表达，不换因子。
3. `kqJqQL08` 全 IS 闸 PASS（S1.78/F1.62/2Y1.64），但与 `2rjrMZ25` 互相关 **0.9857** ⇒ **同腿二者只能取一**。

**★ 平台口径陷阱（务必记住）**：`self` 相关池**包含本人尚未提交的 alpha**（`POST /alphas/{id}/correlations/self` 可强制重算并返回逐条记录）。`kqJqQL08` 的 `self max = 0.9857` **不是**被已提交 alpha 占用，而是与**我们自己的** `2rjrMZ25` 相关；**对已提交池（`58gkLAkk`/`2rOe10qY`/`883Y3bAW`/`JjxrYjre`/`blRnKEk6`）的真实相关仅 0.3437 ✅** ⇒ **腿未被占用**。
**⇒ 判「是否被占用」必须看 `self` 记录里驱动 max 的那个 alpha 是不是自己创建的；不得只看 `max` 数值。**

**⇒ DEU 终局：可交易腿数 = 1（本轮新增可提交 = 1 颗 `2rjrMZ25`）；要凑 10 颗只能引入 DEU 未覆盖的新数据源或换区域。**

### 5. ★ 提交状态（2026-10-13）
- **`2rjrMZ25` 已由用户提交 → `ACTIVE` / `REGULAR`**（10 算子，S1.77/F1.61/2Y1.83/prod 0.651/self 0.3437，全 IS 闸 PASS）。**DEU `analyst` 塔由 0→1 即该颗点亮。**
- **该腿已被自己占用** ⇒ 同腿变体 `kqJqQL08` / `9qWX78vV` / `P0M0vX3p` / `e767nR9O` / `npApoGRx`（互相关 0.986–0.999）**永久不可再提交**；本区后续新候选的 `self` 池将含该颗。
- **DEU 剩余可挖空间**：仅「引入 DEU 未覆盖的新数据源」或换区域。

### 4. 工具沉淀

- `cache/verify_alpha.py`（本次新建）：**MCP 索引不可用时的替代通道** —— 直连 `api.worldquantbrain.com` 取 `alphas/{id}`（checks）+ `correlations/prod|self`（自动轮询 202）。用法 `python cache/verify_alpha.py <id> ...`。
- **PnL 直算互相关**：`GET /alphas/{id}/recordsets/pnl` → 两条 PnL 序列求 Pearson，**不占平台相关性配额**，是判「是否同一条腿」的零成本方法。

<!-- profiles:manual:end -->

---

## ★★★ `analyst83`（财报电话会可读性）判死（2026-10-14 WANL44）

**背景**：`analyst83`（345 字段，cov **0.343**，16 族）此前被 `coverage<0.6` 规则整体排除、**从未探测**——而该规则已被证明只是**区域启发式而非平台限制**（preflight 证明低覆盖字段可正常仿真）。

**机制语义（全新）**：**财报电话会的可读性/复杂度分数** —— `ARI`（Automated Readability Index）、`FRE`（Flesch Reading Ease）、`SMOG`，按发言角色分：CEO / 分析师 / 运营商 / 其他参会者 / 公司参会者；分 Presentation 与 Q&A 两段。

**实测（双结构 × vec_avg）**：

| 字段 | S |
|---|---|
| `anl83_ceo_smog_pres`（CEO 讲话 SMOG） | **0.40** |
| `other_participant_ari_score_presentation` | −0.43 |
| `anl83_analyst_ari_qa` | −0.02 |

**⇒ 判死（max \|S\| 0.43）**：可读性/叙事复杂度在 DEU 无 alpha。**analyst 塔全线封闭**（含全部低覆盖池）。
