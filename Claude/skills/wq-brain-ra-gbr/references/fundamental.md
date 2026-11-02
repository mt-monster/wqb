# GBR × fundamental（组合分支）

> 回到 [GBR 区域流程](../SKILL.md) · [GBR profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/GBR.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region GBR --category fundamental`

<!-- profiles:cell-panel:start -->
**状态**：active（跟区域入场 active）　**分组**：Fundamental　**类别卡**：fundamental

**涉及数据集**：fundamental17、fundamental6、fundamental72

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | GBR | 区域 settings.json |
| universe | TOP700 | 区域 settings.json |
| delay | 1 | 区域 settings.json |
| neutralization | SUBINDUSTRY | 区域 settings.json |
| decay | 4 | 区域 settings.json |
| truncation | 0.08 | 区域 settings.json |
| maxTrade | OFF | 区域 settings.json |
| pasteurization | ON | 区域 settings.json |
| unitHandling | VERIFY | 区域 settings.json |
| nanHandling | ON | 区域 settings.json |
| language | FASTEXPR | 区域 settings.json |
| visualization | false | 区域 settings.json |
| startDate | 2014-01-01 | 区域 settings.json |
| endDate | 2023-12-31 | 区域 settings.json |

### 阈值

- Mode B 主闸 sharpe / fitness：1.25 / 0.8（default；下限锁生效，实时值看 explain）
- 其余阈值跟区域 thresholds.json（本组合无覆盖）

### 证据（2026-10-04 只读汇总）

| 回测 | RA 全过 | prod 已测 | 其中低于上限 | 判死 | 胜绩 |
|---|---|---|---|---|---|
| 89 | 0 | 0 | 0 | 3 | 0 |

主要数据集（回测数）：fundamental72（46）、fundamental6（33）、fundamental17（10）

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
- **禁止**（全局锁定）：禁止两条独立信号腿相加：加权（0.4×A + 0.6×B）、等权 add(rank(A), rank(B))、中缀 + 都算；第二个数据集只以条件（trade_when / if_else）、分组（group_rank / bucket）或残差（ts_regression / group_neutralize / vector_neut）入场（★ 2026-10-20 更正：'vector_neut' **平台可用**——本地算子清单缺它是假阳性，EUR 平台已用它交付 JjQmx9nm；'regression_neut' 仍非平台算子名）
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

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region GBR --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| GBR-FND72-FASTKILL | fundamental72_statement_lines | fundamental72 报表行项族（IS/CF/BS 行项、日期差、days_from_last_change）不再生成；同域 fundamental17/analyst69 前需 prod-first 探针 | fundamental72 | payload | <!-- lint:const-ok 证据原文 -->
| GBR-FUNDAMENTAL17-DEAD | fundamental17_non_value | fundamental17 不再生成任何结构（运营利润率/人均效率/盈利质量/收入加速度全灭）；GBR fundamental域判死 | fundamental17 | payload | <!-- lint:const-ok 证据原文 -->
| GBR-FUNDAMENTAL6-CEILING | fundamental6_quality_value | fundamental6 质量/价值族（atq/revt/oancf/oiadp/gpy/capxy/dpy 等）不再生成——GBR TOP700/SUBINDUSTRY 下规模因子暴露主导，无超额信号；与 value 族 PROD 饱和判 | fundamental6 | payload | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
### 2026-10-31 · fundamental17 打开第二条通道 + ★「塔位杠杆」：`current_enterprise_value` 是集内市场量

本区此前认为 FUNDAMENTAL 只有 `fundamental6` 一个通道。本轮实测 **`fundamental17`（135 字段）是更干净的第二通道**：

**★ 塔位杠杆（最重要）**：`current_enterprise_value`（描述 "Current enterprise value (market capitalization plus net debt)"）
虽然**含市值**，但**数据集归属在 fundamental** ⇒
**`divide(<科目>, current_enterprise_value)` = 纯 FUNDAMENTAL 单塔**，完全不碰 PV 的 `cap`、**不吃任何 trio 配额**；
而分母用 `cap`（PV 集内）⇒ 变 PV+FUND 双塔，吃「单组合 ≤3 / trio×非trio ≤5」。
⇒ **要单塔就选集内市场量当分母。**

| 表达式核心 | S | F | 2Y | SUB | 塔位 | prod |
|---|---:|---:|---:|---:|---|---:|
| `rank(ts_quantile(ts_av_diff(divide(annual_ebitda_value, current_enterprise_value), 252), 22, gaussian))` | **2.48** | **2.22** | **2.69** | 1.68 | **FUND 单塔** | 0.5086 |
| `rank(ts_quantile(ts_zscore(divide(quarterly_ebit_value, current_enterprise_value), 504), 22, gaussian))` | 2.00 | 1.64 | 1.92 | 1.35 | FUND 单塔 | 0.6191 |
| `rank(ts_quantile(ts_av_diff(divide(quarterly_net_income_3, current_enterprise_value), 504), 22, gaussian))` | 1.99 | 1.57 | 2.10 | 1.50 | FUND 单塔 | 0.6460 |

⚠ **同族互相关**：前两条 0.9573、第二↔第三条 0.7203 ⇒ **三条最多取 1–2 条**。

★ **水平毛利率已被证伪（别再踩）**：`divide(fnd6_gpy, fnd6_revty)` = 水平毛利率，
本文件 §6 已记「`fnd6_M2_gross_profitability` 设计即被水平版证伪」；本轮补量波 **10 模板全灭的直接原因就是踩了它**
（F 主导 5 条 S 0.02–0.70，N 主导 3 条被它当权重稀释到 S 1.43–1.51 < 纯 N 腿 2.10）。
**⇒ `fnd6 ÷ cap` 族必须用「位移 + 自历史分位」形态**：`rank(ts_quantile(ts_av_diff(divide(fnd6_capxy, cap), 252), 84, gaussian))` S 2.21 / F 2.05 / 2Y 2.51。

★ **该族引擎 = 分母上价格的位移**（§9.1b）：纯会计增长安慰剂（不碰价格）S −0.12 判死 ⇒ **要出信号必须带价格腿**。
（提交前五道闸见 [`../rules/gate-and-submit-discipline.md`](../rules/gate-and-submit-discipline.md)。）

### ★ 2026-10-13 · GBR × Fundamental 全量清点与封闭（用户问「都试了吗」）

**结论：13 个 Fundamental 数据集现已全部覆盖。本回合补完最后 3 块处女集，全部无信号 ⇒ GBR Fundamental 域封闭。**

| 数据集 | GBR 平台字段 | 状态 | 证据 |
|---|---:|---|---|
| `fundamental6` | 197 | 已判死 | `GBR-FUNDAMENTAL6-CEILING` |
| `fundamental17` | 135 | 已判死（数据集级） | `GBR-FUNDAMENTAL17-DEAD` |
| `fundamental72` | 156 | 已判死 | `GBR-FND72-FASTKILL` |
| `fundamental90` | 63 | 已判死 | 会计质量经典库（Piotroski F / Ohlson O / Montier C / CHS 破产 / NOA / iCFROE）24 条 → **max S 0.28** |
| **`fundamental93`** | **17** | **本回合首次测 → 判死** | 递延税费用比率 / 应计比率 / 资产变化率：S **−0.22 ~ −0.37**，TO 0.022~0.046（近静态），2Y 0.43~0.89 |
| **`fundamental89`** | **42** | **本回合首次测 → 判死** | 资产翻倍/减半 0-1 指示器 + 应计观测数：S **−0.55 ~ 0.36**，TO 0.019~0.078 |
| **`fundamental86`** | **7** | **本回合首次测 → 判死** | 六维质量分位打分（1–10）：S **−0.40 ~ 0.01**，2Y 多为负 |
| `fundamental45` | 12 | 覆盖不足 | cov 0.27 ⇒ `UNUSABLE` |
| `fundamental1` / `alpha_factor_lib` / `digital_ad_spend` / `fundamental22` / `fundamental31` | **0** | **GBR 平台无字段** | `get_datafields` 实测 `count=0`（**本地 `fields` 表失真，勿信**）|

**★ 机制级结论**：GBR Fundamental 的**全部可用机制**（报表行项 / 质量价值 / 会计质量经典库 / 递延税·应计 / 质量打分）**均无横截面超额信号**——与原判死理由完全一致：**TOP700 / SUBINDUSTRY 下规模与价值因子暴露主导**。
**★ 结构特征**：3 块处女集的 TO 落 **0.019~0.078**（多数低于 `review.turnover_min=0.05`）⇒ 属「**近静态**」属性，**任何骨架都无用**（等价 `DEAD_STATIC` 语义）⇒ 以后见此区间直接跳过，别烧波次。

**本回合派发（3 波 24 条，全过五道发批闸 + 骨架审计）**

| 波 | sim | 目标 | 结果 |
|---|---|---|---|
| `gbr_fnd93_f1` | `xSvke64i5bYakKHhSEySq2` | fnd93（递延税/应计）× 5 骨架族 | S −0.22~−0.35（全负）|
| `gbr_fnd86_f2` | `2BUd21duW4POaMjowGOtBhD` | fnd86（六维质量分）× 5 骨架族 | S −0.40~0.01（全负）|
| `gbr_fnd89_f3` | `1peZQA6lZ4E79oc13gD5nCi2` | fnd89（资产波动指示器）+ fnd93 换量纲复核 | S −0.55~0.36（全弱）|

**★ 工程纪律（再次验证）**：本地 `fields` 表含 `fundamental1`(124) / `alpha_factor_lib`(82) / `digital_ad_spend`(6)，但 **GBR 平台 `get_datafields` 返回 0** ⇒ **开波前必须逐数据集用平台验存**；「本地有」≠「平台可用」。

### ★★★★★ 2026-10-30 · `fnd6_<科目> / cap` 是 GBR 唯一量产线（收窄上一节的「全机制封闭」）

**上一节「Fundamental 域封闭」的成立前提是「报表科目 ÷ 报表科目」同量纲比率** —— 全部证据都是 `atq/revt`、`oancf-oiadp/atq`、`ts_zscore(atq/revt,66)` 这类形式。
**分母换成 `cap`（市值）是另一条机制**：它给的是收益率形式（E/P、CF/P 类），带明确价值因子经济含义，不是纯会计比率。`GBR-FUNDAMENTAL6-CEILING` 的 payload 已按此收窄禁用范围（见该条 `scope_correction_20261030`）。

**骨架**：

```
rank/group_rank( ts_quantile( ts_av_diff( divide(fnd6_<科目>, cap), W ), Q, driver=gaussian ) )
W ∈ {168, 252} ／ Q ∈ {56, 84}
```

**★ 设置档是这条线的第二个必要条件**（与上一节的 SUBINDUSTRY/decay4 不同）：
`INDUSTRY` ／ decay **10** ／ truncation **0.05** ／ nanHandling **OFF** ／ maxTrade **OFF** ／ unitHandling VERIFY。

**10 条 `failed_ra_count=0`（`batch_get_alpha_metrics` 权威核出）**：

| alpha | 字段 / 骨架差异 | S | F | TO | 2Y | SUB | inv_ratio | margin(bp) | prod |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `rKRkL9QE` | `fnd6_capxy / cap` 基准 | **2.21** | **2.05** | 8.33% | 2.51 | 1.77 | 0.8733 | 25.94 | **0.6783 ✅** |
| `QPveQvOg` | 二阶差分 `av_diff(av_diff(capxy/cap,252),252)` | 2.06 | 1.78 | 7.49% | 2.47 | 1.68 | 0.8786 | 24.86 | 未测 ★首选 |
| `N1NM5WK8` | `capxy/cap` + `group_rank(·, industry)` | 2.05 | 1.80 | 8.98% | 2.26 | 1.68 | 0.8927 | 21.40 | 未测 ⚠ |
| `P0oerpjp` | `capxy/cap`，W/Q 换成 168/56 | 1.98 | 1.70 | 8.26% | 2.10 | 1.70 | 0.9495 | 22.31 | 未测 ⚠ |
| `0mYoANkv` | `cap / fnd6_newa2_re`（反向） | 1.89 | 1.54 | 11.66% | 2.08 | 1.12 | 0.7831 | 14.22 | **0.6932 ✅** |
| `6XdxzNb5` | `fnd6_newa2_re / cap` | 1.75 | 1.40 | 11.67% | 2.22 | 1.27 | 0.8114 | 13.64 | 未测 |
| `WjOkLGWx` | `fnd6_newq_cheq / cap` | 1.72 | 1.26 | 9.31% | 2.09 | 0.94 | 0.8488 | 14.53 | **0.6577 ✅** |
| `kqNRXm5k` | `capxy/cap` + `ts_zscore(·,168)` | 1.70 | 1.33 | 7.98% | 2.02 | 1.52 | 0.9647 | 19.05 | 未测 |
| `88RAnmAX` | `cap / fnd6_ewq_teqq` | 1.67 | 1.40 | 12.26% | 1.89 | 1.06 | 0.8982 | 14.39 | 未测 |
| `9qxoa3mx` | `cap / fnd6_cptnewq_ceqq` | 1.59 | 1.35 | 12.25% | 1.89 | 1.00 | 0.8679 | 14.78 | 未测 |

**★ 一鱼两塔（本族最有价值的属性）**：`divide(基本面科目, cap)` 同时具备 PV（价值）与 FUNDAMENTAL（基本面科目）属性，`pyramids.effective=2`，multiplier 1.4 + 1.6。
这不是平台巧合 —— `rKRkL9QE` / `0mYoANkv` / `WjOkLGWx` 三条提交后 **pv 1→4（点亮）+ fundamental 0→3（点亮）**，一次点两塔。**该骨架是可复用的双塔模式，值得在别区复用。**

**⚠ 薄余量族，扩招纪律**：三条已测 prod **0.6577–0.6932**，余量仅 **0.007–0.042**。第 4 条起撞墙概率不低：

1. **必须换财务科目，不许换窗口** —— 同科目换 W/Q 是伪多样性。`P0oerpjp` 与 `rKRkL9QE` 只差 168/56 vs 252/84，属**同一条腿**，别当两个候选数。
2. **以下两条不投 prod 时隙**（已有实测判据）：
   - `N1NM5WK8`：同骨架换 `group_rank(·, industry)` 在 INDUSTRY 中性化下已实测 **prod 0.9651**，本条目大概率同一死法。
   - `kqNRXm5k`：与 `rKRkL9QE` 同字段同窗口、只换外层（`ts_zscore` vs `ts_quantile`），大概率高相关；先 `compute_mutual_correlation` 再决定。
3. **扩招方向（真换科目）**：`fnd6_ewq_*` / `fnd6_cptnewq_*` / `fnd6_newa2_*` / `fnd6_newq_*`。
4. **先测族代表再量产**：本族已属「薄余量」状态，新科目首条就该测 prod，不要攒到 5 条再一起测（见 [`wq-prod-corr-read`](../../wq-prod-corr-read/SKILL.md) 族代表预判段）。

**字段池余量**：本地 `fields` 表 `fnd6_` 前缀共 **2233 个**（ds=368 → 838 / ds=1481 → 279 / ds=658 → 266 / ds=1189 → 258 / ds=172 → 197 / ds=858 → 197 / ds=1006 → 196），GBR 侧已用不到 10 个 ⇒ **放大器是换科目，不是换骨架**。

<!-- profiles:manual:end -->
