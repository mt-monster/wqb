# analyst25 数据集分析文档（KOR / TOP600 / D1）

> 字段分类**一律以平台 `description` 为准**，字段名仅作索引，禁作语义依据。
> 画像源：`reference/field_profile/kor_analyst25_profile.json`（207 字段）
> 区域 KOR（不换）｜universe TOP600（本区唯一合法）｜delay 1

---

## 一、分析思路

1. **先用 description 做零假设重分类**，不看字段名 —— 字段名会骗人（description 是唯一语义依据）。
2. 与「按字段名分类」对照，**记录差异**（差异往往就是被漏掉的资产）。
3. 每类映射到经济学机制：说清「收益从哪来」，说不出的不进骨架。
4. 机制 → 骨架 → 候选；**骨架形态由体检体征决定，壳层由经济机制决定**。
5. 双通道取证（论坛 + 论文）后本区实测，结论回写本文档。

## 二、数据集总览

| 指标 | 值 |
|---|---|
| 字段总数 | 207 |
| 类型分布 | VECTOR 207 |
| coverage ≥ 0.5 | 207 / 207 |
| 白空间（alphaCount ≤ 2） | 24 / 207 |
| 平均 coverage | 0.5000 |

## 三、字段分类（★ 以 description 为准）

| 类 | 经济学角色 | 条数 | 覆盖 | 类型 | 白空间 |
|---|---|---:|---:|---|---:|
| **未分类** | — | 190 | 190 | VECTOR190 | 24 |
| **家数/估计者数量** | 关注广度 | 13 | 13 | VECTOR13 | 0 |
| **年龄/时间戳** | 新鲜度 | 3 | 3 | VECTOR3 | 0 |
| **分散度/不确定度** | 观点分歧 | 1 | 1 | VECTOR1 | 0 |

### 与「按字段名分类」的差异

| 字段名前缀 | 条数 |
|---|---:|
| `anl_` | 207 |

> ⚠ 字段名分类**仅供参考**。凡名与 description 冲突的，一律以 description 为准；
> 差异条目须在下方逐条记录，因为差异往往指向被漏掉的信号结构。

### ★ 家数类的时间窗结构（字段名看不见，description 才揭示）

| 时间窗 | 条数 | 语义 | 代表字段 |
|---|---:|---|---|
| `unspecified` | 13 | — | `anl25_eps_down_cnt` (cov 0.500, αC 198) |

## 四、类别 → 经济学骨架映射

### 家数/估计者数量 → 骨架：**关注广度 / 覆盖变化**

- **收益来源**：分析师选择覆盖谁带信息，且覆盖存在羊群；水平含规模噪声，变化才干净
- **合规/工程注意**：VECTOR 必须 vec_avg；TO 低 ⇒ 禁扫窗口谱
- **字段数**：13｜代表：`anl25_eps_down_cnt`, `anl25_eps_even_cnt`, `anl25_eps_new_cnt`

### 年龄/时间戳 → 骨架：**预测新鲜度**

- **收益来源**：估计越旧信息越衰减；快照 vs 共识的差分刻画更新速度
- **合规/工程注意**：时间戳类字段（YYYYMMDD）禁作信号
- **字段数**：3｜代表：`anl25_12f_td_dts`, `anl25_est_dt_recent`, `anl25_td_dts`

### 分散度/不确定度 → 骨架：**分歧度 → 不确定性溢价**

- **收益来源**：分析师意见分歧大 = 信息环境差，风险溢价高
- **合规/工程注意**：离散评分型禁 winsorize/signed_power（无连续尾部）
- **字段数**：1｜代表：`anl25_target_prc_stddev`

### ⚠ 未分类 190 条（须逐条人工判读）

- `anl25_1_my_sg` ｜ Fiscal End
- `anl25_adj_eps_min` ｜ EPS(adj.) (Min)
- `anl25_adj_oper_p_max` ｜ Operating Income (Max)
- `anl25_adj_oper_p_med` ｜ Operating Income (Median)
- `anl25_adj_oper_p_min` ｜ Operating Income (Min)
- `anl25_adj_oper_profit` ｜ Operating Income
- `anl25_adj_oper_profit_12f` ｜ Operating Income, 12 Month Forward
- `anl25_adj_oper_profit_12t` ｜ Operating Income, Trailing 12 Months
- `anl25_adj_oper_profit_margin` ｜ Adjusted Operating Profit Margin
- `anl25_aor` ｜ ROA
- `anl25_asset_to_ratio` ｜ Asset Turnover Ratio
- `anl25_asset_tot` ｜ Assets
- `anl25_bf_tax_income` ｜ Pretax Continued Operation Income
- `anl25_bf_tax_income_growth` ｜ Pretax Continued Operation Income Growth (YoY)
- `anl25_bf_tax_income_growth_p` ｜ Pretax Continued Operation Income Growth (QoQ)
- `anl25_bf_tax_income_max` ｜ Pretax Continued Operation Income (Max)
- `anl25_bf_tax_income_med` ｜ Pretax Continued Operation Income (Median)
- `anl25_bf_tax_income_min` ｜ Pretax Continued Operation Income (Min)
- `anl25_bf_tax_profit` ｜ Net Income Before Taxes
- `anl25_borrow` ｜ Borrowings
- `anl25_borrow_rate` ｜ Interest-bearing Liabilities to Equity
- `anl25_bps_growth` ｜ BPS Growth (YoY)
- `anl25_bps_max` ｜ BPS (Max)
- `anl25_bps_min` ｜ BPS (Min)
- `anl25_cap` ｜ Capital Stock
- `anl25_cap_ratio` ｜ Stockholders' Equity to Total Assets
- `anl25_cap_tot` ｜ Stockholders' Equity
- `anl25_cap_tot_growth` ｜ Total Capital Growth (YoY)
- `anl25_cash_asset` ｜ Cash asset
- `anl25_cash_flow_tot_12f` ｜ Cash Flow, 12 month forward
- … 另有 160 条

## 四·补、字段质量先验（alphaCount TOP30 看轴）

> 依据 `brain-alpha-research-field-quality` §1：**高使用量字段揭示该数据集最强的经济轴**。
> 按 `alphaCount` 降序（同分按 `userCount`）取前 ~30 名看轴。**此步不可跳**。

| αC | users | cov | 字段 | description 摘要 |
|---:|---:|---:|---|---|
| 397 | 177 | 0.500 | `anl25_f21_spe` | EPS, 12 month forward |
| 337 | 176 | 0.500 | `anl25_adj_oper_profit_12f` | Operating Income, 12 Month Forward |
| 304 | 122 | 0.500 | `anl25_revert_net_profit_12f` | Net Income from Parent Company, 12 months forward |
| 198 | 91 | 0.500 | `anl25_eps_down_cnt` | Number ofEPS Estimates Down |
| 195 | 73 | 0.500 | `anl25_ebit_margin` | EBIT margin |
| 195 | 73 | 0.500 | `anl25_roe` | ROE |
| 183 | 67 | 0.500 | `anl25_ebit_max` | EBIT (Manuf. Max) |
| 149 | 72 | 0.500 | `anl25_net_profit_12f` | Net Income, 12 months forward |
| 146 | 64 | 0.500 | `anl25_sps_max` | SPS (Max) |
| 141 | 79 | 0.500 | `anl25_adj_oper_profit` | Operating Income |
| 140 | 60 | 0.500 | `anl25_oper_profit_margin` | Operating Profit Margin |
| 111 | 46 | 0.500 | `anl25_bf_tax_income_min` | Pretax Continued Operation Income (Min) |
| 104 | 78 | 0.500 | `anl25_eps_max` | EPS (Max) |
| 91 | 53 | 0.500 | `anl25_sales_growth` | Sales Growth |
| 88 | 59 | 0.500 | `anl25_adj_oper_p_med` | Operating Income (Median) |
| 86 | 61 | 0.500 | `anl25_ebitda_12f` | EBITDA, 12 months forward |
| 86 | 48 | 0.500 | `anl25_bps_growth` | BPS Growth (YoY) |
| 85 | 52 | 0.500 | `anl25_adj_oper_p_max` | Operating Income (Max) |
| 84 | 56 | 0.500 | `anl25_bf_tax_income` | Pretax Continued Operation Income |
| 76 | 51 | 0.500 | `anl25_roe_max` | ROE (Max) |
| 75 | 57 | 0.500 | `anl25_dem_aor` | ROA (Median) |
| 75 | 48 | 0.500 | `anl25_ebitdaps` | EBITDAPS |
| 74 | 39 | 0.500 | `anl25_net_profit_margin_con` | Parent Company's Net Profit Margin |
| 74 | 36 | 0.500 | `anl25_per_12f` | PER, 12 Months Forward |
| 73 | 48 | 0.500 | `anl25_tnc_pu_spe` | Number of EPS Estimates Up |
| 72 | 45 | 0.500 | `anl25_roa_max` | ROA (Max) |
| 71 | 55 | 0.500 | `anl25_spc` | CPS |
| 64 | 45 | 0.500 | `anl25_cps_max` | CPS (Max) |
| 64 | 39 | 0.500 | `anl25_bf_tax_income_med` | Pretax Continued Operation Income (Median) |
| 61 | 47 | 0.500 | `anl25_bf_tax_income_max` | Pretax Continued Operation Income (Max) |

**★ 轴判读**（头部字段指向的经济轴，供人工确认 / 修正）：

- 头部字段集中于：`anl25_f21_spe`(αC 397)；`anl25_adj_oper_profit_12f`(αC 337)；`anl25_revert_net_profit_12f`(αC 304)；`anl25_eps_down_cnt`(αC 198)；`anl25_ebit_margin`(αC 195)
- ⇒ **开波前须先确认本集「最强轴」是否与拟挖方向一致**；
  若头部字段指向的轴与拟挖方向不同，**方向本身可能已偏**（见 analyst_consensus 打样实例）。

## 四·补二、字段画像五问与预处理决策

> 五问 = 测的是什么？怎么测的？时间维度（瞬时/累计/变化率）？为何存在？可靠性如何？

| 类 | 测什么 | 怎么测 | 时间维度 | 为何存在 | 可靠性 |
|---|---|---|---|---|---|
| 家数/估计者数量 | — | — | — | — | cov≥0.5 13/13；类型 VECTOR |
| 年龄/时间戳 | — | — | — | — | cov≥0.5 3/3；类型 VECTOR |
| 分散度/不确定度 | — | — | — | — | cov≥0.5 1/1；类型 VECTOR |

**预处理决策（由画像推导，不由拍脑袋）**：

| 画像读数 | 预处理决策 | 依据 |
|---|---|---|
| VECTOR 占比高 | **必须 `vec_avg`/`vec_sum` 降维** | 裸用 `rank`/`ts_*` 秒拒；一条错整批 CANCELLED |
| cov < 0.4 的字段 | 先 `ts_backfill`/`group_backfill` | 体检硬门检查 1 |
| 季频更新（报告日） | 窗口下限 ≥ 63d | 窗口低于更新周期 = 噪声 |
| 单边恒正 | 改变化率 | 体检读数映射 |
| 离散评分型 | 禁 `winsorize`/`signed_power` | 无连续尾部，零效果 |

## 五、本区实测与死因

> **待回填**：本数据集在 KOR/TOP600/D1 的实测读数（S / TO / RN_S / 2Y）与死因归因。
> 死因判据三条：① TO 是否 <0.10（近静态）；② 有效持仓占比；③ risk_neutralized_S vs raw_S。
> ⚠ 预筛更严版：**TO < 0.03 的候选连差分都不要做**（差分只会更低）。

## 六、双通道取证（★ 已回填，2026-11-16）

- **通道 A（论坛）**：`search_forum_posts` 长中文 query 会炸，砍短关键词；`read_forum_post` 必传 `include_comments=false`（true 会 30s 超时）。
- **通道 B（论文）**：`domain_search`。

### ★★★★★ 通道 A 关键取证：ZZ43261「分析师盈利预期修正广度」（36 赞）

**帖子 ID**：`43250301270295`（顾问专属中文论坛，2026-09-04）

**核心主张**（与本集 13 个「家数/估计者数量」字段**直接对应**）：
> 「比起『单个分析师修正的幅度』（容易被一两个极端预测带偏），**『修正的广度』——有多少分析师在上调、有多少在下调——更能反映一致预期的方向性变化**。当上调的分析师数量压倒下调时，说明盈利动能（earnings momentum）在改善。」

**帖子给出的构造（三步，可直接落地）**：
| 步 | 做法 | 本集对应字段 |
|---|---|---|
| 1 | **广度比** = 「上调数 ÷ 下调数」或「上调数 ÷ 覆盖总数」 | `anl25_tnc_pu_spe` ÷ `anl25_eps_down_cnt` 或 ÷ `anl25_tot_eps_ests_num` |
| 2 | **向量聚合**：vec 级求和/均值压缩成单票标量 | **必须 `vec_sum`/`vec_avg`**（本集 207/207 全 VECTOR）|
| 3 | **去极值**：比值在「下调数≈0」时爆炸 ⇒ `winsorize` 截断 | `winsorize(..., std=2)` |

**帖子报告的 IS 读数（★ 关键）**：
> 「IS Sharpe 大致落在 **3.0~4.5** 区间，Turnover 约 **0.15~0.35**（信号较强，但换手需 decay 控制）。」

**帖子推荐的设置**（与本波设计的差异）：
> 「Neutralization = **STATISTICAL** / 行业中性化」「Decay 取**短档**」「Truncation 取适中值」「Universe = 宽基池」

⇒ ⚠ **本波（Wave18）用 SECTOR + decay4 是保守起点**；若结果不达 **S 3.0**，下一步应换 **STATISTICAL** + **decay 1–2** 复测。

**帖子的通用模板（可泛化接口）**：
```
revision_breadth(up_field, down_field, horizon, group) =
    signed_power(
        group_normalize( ts_smooth( vec_agg(up_field) / vec_agg(down_field), horizon ), group ),
        p
    )
```
- 换数据腿：上调/下调 → **目标价上调/下调**（本集有 `anl25_recom_val_up_cnt` / `anl25_recom_val_down_cnt`）
- 换聚合：**比值 vs 占比 vs 净占比**（`(up-down)/(up+down)`）—— 本波 Wave18 测了三种
- 换市场：「USA / EUR / ASI 都有分析师预期类数据，同一逻辑可直接迁移」

**★ 与本集其他字段的交叉**：
- `anl25_target_prc_stddev`（本集唯一「分散度」类）= 帖子所说「stddev 只告诉你分歧**大小**」
- 帖子未解决疑问：「覆盖分析师数很少的股票，广度信号是否可信？」⇒ 本集 `anl25_tot_eps_ests_num` 可作**质量过滤**（低覆盖降权）

### ★★★★ 通道 A 关键取证：WL27618「121 个字段里最值得做的 5 个信号」（30 赞）

**帖子 ID**：`42659792904343`

**第 1 名 = Estimate Revision Momentum（预期修正动量）**：
> 「分析师对 EPS 的一致预期**上升**时，股价出现持续正漂移；**修正方向反映增量信息，比预期绝对水平更强**。数据集通常**没有原生 revision 字段**，需要用 `ts_delta(anl14_mean_eps_fp1, d)` 自己构造。」

⇒ **★ 对本波的重要含义**：`analyst_factor_signals` 的 `eps_y1_estimate_change_3mo`（"Change in consensus FY1 EPS forecast over the past 3 months"）**正是"原生 revision 字段"** ⇒ 免去了自己 `ts_delta` 的噪声 ⇒ **理论上是比论坛更优的起点**（Wave16 A1 已证 2Y 1.69 过闸）。

**第 3 名 = Margin Scissor（边际剪刀差）—— 与合规禁令直接相关**：
> 「同时看 `mean_revenue_fp1` 与 `mean_eps_fp1` 的修正方向：**收入上修 + EPS 下修 = 隐含利润率压缩预期**，盈利质量恶化的领先信号。」

⇒ ⚠ 这是**跨字段**构造，但它是**两条独立信号腿**（收入修正 vs EPS 修正）⇒ **不能用 `add`**（撞 `POISON:equal_weight_leg_add`）。
⇒ **合规实现**：`subtract(rank(revenue修正), rank(eps修正))`（两腿**同源同集** + **单一经济含义**="利润率压缩"）—— **符合放行形态**。

**实现提醒（重要）**：
> 「数据集常见 coverage 只有 0.5 左右，记得用 `ts_backfill` 处理缺失」「`numofests`（估计人数）建议用作**质量过滤**」
> 「**`fp1` 与 `fp2` 的差本身就是「未来两个季度预期之差」，可作 revision 的廉价代理**」

⇒ ★ 最后一条给出**新合规构造**：`subtract(eps_y2_estimate_change_3mo, eps_y1_estimate_change_3mo)` = **修正的期限结构**（长端修正 − 短端修正），同源 + 单一经济含义 ⇒ **合规**。

### 通道 B（论文）已成形

- **Gleason & Lee (2003)**：创新性修正 > 羊群性修正
- **Jung (2019)**：未缩放修正有效、缩放后失效（Wave16 A3 实测佐证）
- **PEAD 文献族**（Schnaubelt & Seifert 等，见论坛「论文合集」帖 24897131810839）：财报意外后的反应不足

## 七、下一步

> **已回填（2026-11-16）**：

### 继承（来自其他集的判定）

| # | 判定 | 来源 |
|---|---|---|
| I1 | 「家数/覆盖广度」类机制在 `analyst_consensus` 已死（5 波 22 条最高 S 0.54）| Wave11–15 |
| I2 | ⚠ **但 Wave15 死的是「跨科目广度背离」+ 低覆盖 CW**，**不是**论坛所说的「上调/下调广度比」 | Wave15 复盘 |
| I3 | 论坛帖（36 赞）**明确报告「修正广度」可达 S 3.0–4.5** ⇒ 与 I1 的「家数类无信号」**冲突**，必须本区实测裁决 | 通道 A |

### 准入（本波凭什么值得测？）

| # | 依据 |
|---|---|
| A1 | **本集是 KOR 唯一有离线体检包的集** ⇒ 字段画像最完整 |
| A2 | **13 个「家数/估计者数量」字段**直接对应论坛首推的「修正广度」构造 |
| A3 | **论坛给出 S 3.0–4.5 的 IS 读数**（我方 A1 只有 1.31）⇒ 差距在构造不在方向，值得一测 |
| A4 | **`vec_sum` 降维路径明确**（207/207 VECTOR）⇒ 工程上无歧义 |
| A5 | 「上调数」`anl25_tnc_pu_spe` αC=73（本集头部），「下调数」`anl25_eps_down_cnt` αC=198（**本集第 4 强**）⇒ 两腿都是高使用量字段 |

### 收窄

Wave18 = **1 机制 × 5 聚合口径**（比值 / 占比 / 净占比 / 裸上调数 / 目标价口径）
⇒ 仍属「同骨架 × 字段笛卡尔积」探针批，非机制扩张。

### Wave18 候选（multisim `4tduUd8404vG9bd14Ij0oQhJ`）

| # | 聚合口径 | 表达式 |
|---|---|---|
| B1 | 上调/下调 **比值** | `winsorize(group_zscore(divide(vec_sum(anl25_tnc_pu_spe), add(vec_sum(anl25_eps_down_cnt), 0.0001)), sector), std=2)` |
| B2 | 上调/总数 **占比** | 同上，分母换 `anl25_tot_eps_ests_num` |
| B3 | **净占比** | `divide(subtract(up, down), add(total, 0.0001))` |
| B4 | 上调数 **裸** | `winsorize(group_zscore(vec_sum(anl25_tnc_pu_spe), sector), std=2)` |
| B5 | **目标价口径** | `up_cnt / down_cnt`（`anl25_recom_val_up_cnt` / `_down_cnt`）|

### ⚠ 已知风险

| 风险 | 说明 |
|---|---|
| **单位连坐** | `add(vec_sum(x), 0.0001)` 在 RULES §Q42 有 `Incompatible unit` 记载 ⇒ 若整批 FAIL，改用 `multiply(vec_sum(x), 0.0001)` 保单位，或省去 ε |
| **CW 死因** | ⚠ 本集 cov **全部 0.5**（207/207）⇒ 落在「危险区」边缘 ⇒ B 族**极可能触发 `CONCENTRATED_WEIGHT`** |
| **换手** | 论坛报告 TO 0.15–0.35 ⇒ 须 decay 控制 |
| **设置差异** | 论坛推荐 STATISTICAL + 短 decay；本波用 SECTOR + decay4 ⇒ 若 S 明显低于 3.0，**先查设置再查几何** |

### 若 Wave18 达标（S ≥ 1.58）

按论坛设置差异排查：SECTOR → **STATISTICAL**，decay 4 → **1/2**。

### 若 Wave18 全灭

⇒ 与 I1 一致 ⇒ 判定「家数/广度类机制在 **KOR** 死，即使论坛在 USA/EUR/ASI 有效」⇒ **又一个 R1 铁律（结构不可跨区迁移）实例**。
