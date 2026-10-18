# IND × fundamental（组合分支）

> 回到 [IND 区域流程](../SKILL.md) · [IND profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/IND.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region IND --category fundamental`

<!-- profiles:cell-panel:start -->
**状态**：probe（跟区域入场 probe-only）　**分组**：Fundamental　**类别卡**：fundamental

**涉及数据集**：fnd94、fundamental1、fundamental17、fundamental23、fundamental44、fundamental86、fundamental90

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | IND | 区域 settings.json |
| universe | TOP500 | 区域 settings.json |
| delay | 1 | 区域 settings.json |
| neutralization | STATISTICAL | 区域 settings.json |
| decay | 4 | 区域 settings.json |
| truncation | 0.08 | 区域 settings.json |
| pasteurization | ON | 区域 settings.json |
| testPeriod | P0Y0M0D | 区域 settings.json |
| unitHandling | VERIFY | 区域 settings.json |
| nanHandling | OFF | 区域 settings.json |
| maxTrade | OFF | 区域 settings.json |
| language | FASTEXPR | 区域 settings.json |
| visualization | false | 区域 settings.json |

### 阈值

- Mode B 主闸 sharpe / fitness：1.5 / 1.0（thresholds_override:IND；下限锁生效，实时值看 explain）
- 其余阈值跟区域 thresholds.json（本组合无覆盖）

### 证据（2026-10-04 只读汇总）

| 回测 | RA 全过 | prod 已测 | 其中低于上限 | 判死 | 胜绩 |
|---|---|---|---|---|---|
| 0 | 0 | 1 | 1 | 9 | 2 |

### S1 字段理解

- 低频字段窗口取 66 / 252，补覆盖用 ts_backfill(·, 66)（季频）或 252（年频）（决策表 D5 / D6）
- 比率型信号的分母口径往往决定 self / prod 与 2Y——先看分母
- 窗口（类别卡，均在白名单内）：quarterly 66/252；annual 252/504

### S2 生成

- **类别通用原语**（类别卡，跨区）：
  - accrual / cash gap: earnings quality, not the earnings level
  - leverage change: delta of debt or interest burden
  - efficiency: turnover or incremental margin, not the stock of assets
  - invert value only as a residual after industry neutralization
  - asset growth: delta of total assets vs revenue growth (efficiency)
  - margin trajectory: gross margin change vs operating margin change
  - capital allocation: capex vs depreciation (growth vs maintenance)
- **跨区结论**（KOR/EUR；conflict）：换分母在 KOR 是破 self / prod 墙的主杠杆，在 EUR 是毒药——不作类别级规则，按组合取用（证据：KOR other466 只换分母 self 0.7422→0.6244、prod 0.8061→0.6843；EUR value_investment 换分母 S 0.10 全灭（WorkBuddy MEMORY §1.2 / §1.7）） <!-- lint:const-ok 证据原文 -->
- **跨区结论**（USA/KOR；negative）：慢变的经典基本面单因子（value / quality / book 及其线性变体）判死或 prod 饱和（证据：USA seed basics 全族死、book/value 145 颗同族 ACTIVE；KOR 慢变基本面族 fnd86/89/93/f21 四连死） <!-- lint:const-ok 证据原文 -->
- **禁止**（类别卡）：禁止使用裸 rank(fundamental_score)（必须 group_neutralize 或 group_zscore）
- **禁止**（类别卡）：禁止使用加权混合（0.4*rank(A) + 0.6*rank(B)）
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

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region IND --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| IND-FND17-ANNUAL-DEAD | fundamental17 annual tax/leverage | IND 区域避免使用 fundamental17 年度数据做 REGULAR alpha 主信号。年度频率不足以驱动 D1 回测。 | fundamental17 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-FND23-ANNUAL-BS-DEAD | fundamental23 annual balance sheet | IND 区域不再挖年度频率基本面科目数据集（fundamental17/23 已双证）；若需基本面暴露优先评分类/日频更新族（fnd86 win、model138 PDI 待探） | fundamental23 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-FND44-ACCOUNTING-QUALITY-DEAD | fundamental44 accounting quality | IND 区域避免挖会计质量/舞弊检测类信号（fundamental44, model192, fundamental90），转向其他方向。 | fundamental44 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-FND90-EARNINGS-QUALITY-DEAD | fundamental90 earnings quality/GAME score | IND 区域避免使用 fundamental90 盈利质量/GAME 评分数据集做 REGULAR alpha 主信号；该族信号与 IND 市场结构不匹配 | fundamental90 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-FND94-GROUPNEUT-FAIL | fnd94 group_neutralize | fnd94 在 IND-TOP500-D1 全面判死（robust 结构不可达 + group 系反向稀释），后续 IND 战役不再回 fnd94；momentum 反向腿 S 引擎可跨数据集复用（fnd94 上 S 1.60→2.02） | fnd94 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-FND94-ROBUST-CEILING-2RL5BVWY | fnd94 margin/cash/tax 三腿 margin 腿优化 | IND fnd94 三腿结构不再做同族参数优化；如需 robust≥1.0 必须换字段/换数据集或跨数据集混合 | fnd94 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-FND94-THIRD-LEG-DEAD | fundamental94 内部第三腿 | IND 区域 fnd94 数据集内部字段组合已穷尽，勿再尝试三腿组合 | fnd94 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-FUNDAMENTAL1-GOVERNANCE-SPARSE | fundamental1 governance | coverage 0.56 的治理/董事会字段在 IND TOP500 有效覆盖不足：先验验证字段实际持仓数（longCount 明显 <50 即无挖掘价值），勿再试 fundamental1 | fundamental1 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-OPMARGIN-PROD-SATURATED | Operating-Margin (fnd94_q_qpdaio / fnd94_q_saleq) | Do not submit Operating-Margin variants in IND. PROD pool saturated. | fnd94 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-FND93-TAX-DEAD | fundamental93 递延税比率 | IND 区域不再挖 fundamental93（Earnings Tax Data，32 字段 / alphaCount 14–173 白空间）：10 探针最高 \|S\|=0.63（F 0.33）、2Y 全部 ≤0.53。递延税比率族在 IND 无信号。 | fundamental93 | payload | <!-- lint:const-ok 证据原文 -->
| IND-FND89-ACCRUAL-DEAD | fundamental89 accrual / Jones model | IND 区域不再挖 fundamental89（195 字段）：10 探针最高 \|S\|=0.72（ts_delta）、水平型全部负值（−0.59~−0.06）。与已判死的 fundamental44/90「会计质量」同族，第三证。⚠ 另：`fnd89_other_d1_asset_change` / `major_d1_asset_change` / `asset_d1_asset_change` 三字段回测结果**逐位相同**，在 IND 是同一值的别名，勿当三个独立字段用。 | fundamental89 | payload | <!-- lint:const-ok 证据原文 -->
| IND-FND86-ROBUST-CEILING | fundamental86 综合评分（fnd86_earnings_score / average_score） | **fundamental86 是 IND fundamental 唯一活矿**（最强 S 2.70/F 2.62），但 `LOW_ROBUST_UNIVERSE_SHARPE`（limit 1.0）**天花板 0.80，已证明不可破**——单一字段/结构上不存在同时满足 S≥1.58 与 robust≥1.0 的点。后续 IND 战役若要再碰 fnd86，必须先有新的破 robust 维度（换 universe 不可，IND 只有 TOP500）。 | fundamental86 | payload | <!-- lint:const-ok 证据原文 -->
| IND-FND22-ESG-MICRO-DEAD | fundamental22 ESG KPI（2 个 VECTOR 字段，cov 0.395） | IND 区域不再挖 fundamental22：水平（vec_avg）与变化量（ts_delta 66）4 探针 |S|≤0.09、2Y ≤0.28。ESG 近静态第四证。 | fundamental22 | payload | <!-- lint:const-ok 证据原文 -->
| IND-FND25-METADATA-DEAD | fundamental25 operating metric（6 字段，5 个元数据码） | IND 区域不再挖 fundamental25：唯一真信号字段 fnd25_metricvalue cov 0.2984（<0.35 跳过线），探针 S 0.09。其余字段是 fiscalyear/periodcode 类毒药码。 | fundamental25 | payload | <!-- lint:const-ok 证据原文 -->
| IND-FND4-IDMAP-DEAD | fundamental4 内部 ID 映射 | IND fundamental4 唯一字段 fnd4_chinascope_secmap 是内部证券 ID（码类毒药字段，无语义）⇒ 按字段语义直接判死，勿烧波。 | fundamental4 | inferred | <!-- lint:const-ok 证据原文 -->

### 胜绩

| 条目 | 机制 | 设置与骨架 | 数据集 | 归属 |
|---|---|---|---|---|
| IND-FND86-EARNINGS-ROBUST-WIN | fundamental86 综合评分数据集（earnings_score/fundamental_score）在 IND | fundamental86 earnings_score 单信号 robust 突破配方：ts_zscore(fnd86_earnings_score, 252) 或 add(ts_zscore(fnd86_earnings_score,  | fundamental86 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-FND86-GROUPNEUT-ROBUST-BREAK | fnd86 group_neutralize | robust 破壁配方：前置多腿线性组合（earn+fnd−mom 等权）→ ts_zscore(315) → group_neutralize(industry)，backfill 66、decay 2、STATISTICAL。三个关键杠 | fundamental86 | inferred | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
## ★★★★ 2026-10-13 战役终局：fundamental86 是活矿，但 robust 闸不可破

**8 波 71 条实测**（wave176–183）。结论分三层。

### 1. 唯一活矿 = `fundamental86`（Stock Reports Plus）
7 个 MATRIX 字段，全是 **1–10 decile 综合评分**，cov 0.76–0.98。
- `fnd86_average_score`（综合总分）⇒ **S 最强**（2.60–2.70）
- `fnd86_earnings_score`（盈利分）⇒ **robust 最强**（0.80）
- `fnd86_price_momentum_score` ⇒ **反向**（S −0.48），该集内动量不可用
- `fnd86_insider_trading_score` ⇒ cov 0.0，不可用

### 2. ★★★ `LOW_ROBUST_UNIVERSE_SHARPE`（limit 1.0）是唯一卡点，天花板 0.80
**最优骨架（已穷尽）**：`group_zscore(ts_backfill(fnd86_earnings_score, 66), sector)`
⇒ S 2.11 / F 1.66 / TO 0.094 / sub 0.76✅ / 2Y 2.09✅ / **robust 0.80（差 0.20）**，挂 `IND/D1/FUNDAMENTAL` **单塔**（effective=1）。

**已试杠杆全表**（无一能把 robust 从 0.80 推到 1.0）：

| 杠杆 | Δrobust |
|---|---|
| 分组轴 industry→**sector** | **+0.20（唯一有效）** |
| 分组轴 →subindustry | −0.18 |
| `group_zscore` 替 `group_neutralize(rank())` | +0.03 |
| `winsorize` 前置 | **0（离散 decile 无尾部可截）** |
| `signed_power` | −0.08 |
| decay 4→2 / 4→8 | +0.03 / −0.03 |
| nanHandling OFF→ON | **0（逐位相同）** |
| neutralization →MARKET/NONE | −0.12 |
| neutralization →INDUSTRY | −0.35 |
| `ts_mean` 平滑 | −0.48 |
| `ts_delta` 换变化量 | +0.13（rob 0.93）但 S 掉到 1.46，主闸不保 |
| 同集残差 `subtract(rank,rank)` | −0.14 ~ −0.42 |
| 同集 `trade_when` 门控 | −0.49 |
| 反向 `−x` | 全闸反向失败 |
| **分组轴 sector→market / exchange（wave184）** | **0（0.76–0.77 ≈ sector 饱和；粗轴增益终点=sector）** |
| **DEU A 级框架（多窗 add + bucket 组，wave184）** | **+0.07（rob 0.87）但 S −0.26（1.83），仍 <1.0** |
| **子集门控 trade_when(rank(cap))（wave184）** | **0（0.80/0.64）** |
| **group_rank 替 group_zscore（wave184）** | **+0.01（等价，非独立杠杆）** |

### 3. ★★★ 两条可迁移铁律
1. **分组轴直接决定 robust，且是双赢不是权衡**：`subindustry` < `industry` < **`sector`**；轴越粗 robust 越高，**S 同步上升**。
   （修正旧认知「分组轴只决定 2Y 类型与塔数」——它同样决定 robust。）
2. **`LOW_SUB_UNIVERSE_SHARPE` 的 limit 随 S 动态浮动（≈0.29×S）**：S 2.70→限 0.80、S 2.09→限 0.62。
   ⇒ **选「刚好过主闸」的 S，不要追最高 S**——`average_score` 路线（S 2.70）正是因此挂 sub。
3. **离散评分型数据集禁用尾部处理算子**（winsorize / signed_power）：1–10 decile 无连续尾部可截，实测零效果。

### 4. 已判死
`fundamental93`（递延税，\|S\|≤0.63）、`fundamental89`（accrual/Jones，\|S\|≤0.72，且三个 asset_change 字段是同一值别名）。
剩余 `fundamental22`(2 字段)、`fundamental25`(6 字段)、`fundamental4`(1 字段) 覆盖 ≤0.40、字段过少，无挖掘价值。

### 5. ★★★★ robust+CW 联合破闸机理（wave186–204 实证，2026-10-14，限 0.99 差 0.01 终局）
上述「天花板 0.80」已被推翻。四级火箭链（全部在 `fnd86_earnings_score` 上实测）：
1. **裸 `ts_zscore(earn, 504)`**：rob 1.11 但 TO 0.399 ⇒ F 死（TO 由 NaN 覆盖进出驱动，decay/hump/winsorize 全无效）。
2. **对 z 输出做 `ts_backfill`（bf 悬崖）**：bf2→rob 1.50/TO 0.409；**bf5→TO 0.11 但 rob 0.70**（earnings 周更，5 天覆盖悬崖，二元无中间态）。
3. **`group_rank(·, sector)`**（连续族第一个正向杠杆）：rob 0.70→0.81；**z252**（窗口↓rob↑）：0.84。
4. **`signed_power(·, 3)`**（连续族最强杠杆）：0.84→**1.00 过闸**（power 1.5→0.92 / 2→0.96 / 3→1.0 单调）。
   注意：signed_power 加在 **z 输出/rank 输出**上有效（连续分布）；加在**裸 decile 分**上无效（上表第 3 条铁律只适用于裸分输入）。
5. **CW 闸（CONCENTRATED_WEIGHT）**：判据 = **每日分配权重股票数的覆盖持续性**（与权重分布形状无关——quantile uniform 全均匀仍 warning；与 truncation 无关——0.02/0.05/0.08 逐位同；与字段覆盖率无关——cov 0.974 的字段也 fail）。
   **由 ts_backfill 长度决定**：bf≥10 → PASS（bf9 warning），bf66 全覆盖。修复法：**同一字段 bf5 与 bf10 两窗版本的 filter=true 并集混合**（覆盖=并集；同字段多窗 add 判合规，正例同 `WjLEOqLP`）。
6. **终局**：CW（要缺口日有仓）与 rob 峰（要缺口日 bf5 风格）同谱互斥 ⇒ union 混合 rob 上限 **0.99**（权重比不敏感）。
   最优缺口：**同字段 bf5/bf10 两窗 group_rank³ 的 filter=true 并集混合**（完整式见台账 `IND_fnd86_ledger.md` §8.8，`6XA77p2L` 族；同字段多窗 add 判合规）
   S 1.87 / F 1.40 / TO 0.119 / CW✓ / sub 0.92 / 2Y 2.10 / **rob 0.99 差 0.01**。
   ⚠ `LOW_ROBUST_UNIVERSE_SHARPE` limit **固定 1.0 不随 S 浮动**（区别于 sub 闸 ≈0.29×S）；
   robust 由「缺口日行为」决定，STATISTICAL 是唯一可用 neut（CROWDING 0.58 / R&M 0.55）。
<!-- profiles:manual:end -->
