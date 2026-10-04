# KOR × fundamental（组合分支）

> 回到 [KOR 区域流程](../SKILL.md) · [KOR profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/KOR.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region KOR --category fundamental`

<!-- profiles:cell-panel:start -->
**状态**：active（跟区域入场 active）　**分组**：Fundamental　**类别卡**：fundamental

**备注**：KOR 当前唯一活路（other466 财务比率族，平台类别 FUNDAMENTAL，fundamental 塔 1.6×）

**涉及数据集**：fundamental21、fundamental86、fundamental93、fundamental94、other466

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | KOR | 区域 settings.json |
| universe | TOP600 | 区域 settings.json |
| delay | 1 | 区域 settings.json |
| neutralization | STATISTICAL | 区域 settings.json |
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

- Mode B 主闸 sharpe / fitness：1.25 / 0.8（default；下限锁生效，实时值看 explain）
- 其余阈值跟区域 thresholds.json（本组合无覆盖）

### 证据（2026-10-04 只读汇总）

| 回测 | RA 全过 | prod 已测 | 其中低于上限 | 判死 | 胜绩 |
|---|---|---|---|---|---|
| 171 | 20 | 8 | 2 | 6 | 5 |

主要数据集（回测数）：other466（110）、fundamental94（25）、fundamental93（14）、fundamental21（12）、fundamental86（10）

### S1 字段理解

- 低频字段窗口取 66 / 252，补覆盖用 ts_backfill(·, 66)（季频）或 252（年频）（决策表 D5 / D6）
- 比率型信号的分母口径往往决定 self / prod 与 2Y——先看分母
- 窗口（类别卡，均在白名单内）：quarterly 66/252；annual 252/504

### S2 生成

- **用**：other466 财务比率：经营利润类分子 / 资产或市值类分母，group_rank 到 market 轴，再 ts_rank 504（RULES §G）
- **用**：分母是最大未测空间：已测 28 组合里分母 18 次集中在 bs_assets_tot_q（RULES §G）
- **避**：prod 饱和字段组合：oth466_bs_assets_tot_q 与 oth466_is_oper_inc_q 同时命中即拦，须换分子分母（RULES §G）
- **避**：慢变基本面族 fnd86 / 89 / 93 / f21 四连死；fundamental17 202 条天花板 1.30（RULES §G）
- **说明**：SUB / 2Y 二分：is_ptx_inc_norm_q 过 SUB 不过 2Y；is_consol_net_inc_q 过 2Y 不过 SUB（RULES §G）
- **说明**：分母口径决定 SELF / prod 与 2Y：资产侧 2Y 2.22，权益侧 1.12–1.18（KOR profile）
- **已验证骨架**（证据见每行注释；照抄前先按本组合当前 prod 复核）：

  ```text
  quantile(ts_rank(group_rank(divide(分子, 分母), market), 504))
  signed_power(ts_rank(group_rank(divide(分子, 分母), market), 504), 0.5)
  ```

  - quantile(ts_rank(group_rank(divide(分子, 分母), market), 504))… ← 外层包装用 quantile：在 signed_power 版基础上 2Y 1.51→1.56、prod 0.6544→0.6397，外层轴取 market 后 2Y 1.62 全闸过（KOR profile / WorkBuddy MEMORY §1.1）
  - signed_power(ts_rank(group_rank(divide(分子, 分母), market), 504… ← A1NXddRw S 2.11 / prod 0.6547 已 ACTIVE（历史版本，signed_power 制造了「假性不可能三角」）
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

1. [组合] 外层 signed_power(·, 0.5) 换成 quantile(·)，骨架其余冻结（证据：2Y 1.51→1.56、prod 0.6544→0.6397（WorkBuddy MEMORY §1.1）；禁外推（只在本区用）） <!-- lint:const-ok 证据原文 -->
2. [组合] 外层分组轴 sector → market（效果依赖包装算子，换了包装要重测）（证据：quantile 版换轴后 2Y 1.62 全闸过（WorkBuddy MEMORY §1.1）；禁外推（只在本区用）） <!-- lint:const-ok 证据原文 -->
3. [组合] self / prod 墙先换分母、不换分子（证据：同分子只换分母：self 0.7422→0.6244、prod 0.8061→0.6843；同分母扫 8 个分子无一过（WorkBuddy MEMORY §1.2）；禁外推（只在本区用）） <!-- lint:const-ok 证据原文 -->
4. [全局] 判「无解 / 天花板」前先扫等价算子替换：signed_power → quantile、ts_scale → quantile / normalize。数值路径不同，一次动多个闸（含 prod，要读全部闸）（KOR/GLB 复现：KOR other466 signed_power→quantile：2Y 1.51→1.56、prod 0.6544→0.6397；GLB quantile 替 ts_scale：S +0.20、F +0.06、prod 0.475→0.565（DEC-72）） <!-- lint:const-ok 证据原文 -->
   - 注意：效应量逐区实测，禁外推；quantile 只收 1 个参数
5. [全局] 强但撞 prod 墙的快信号：用一个经济子集门控（trade_when 进 >0.5 出 <0.4 的慢变量，或 rank(cap)>0.2 ∩ 子集）只在子集里持仓（GLB/ASI/IND 复现：GLB-DL20D-SUBSET-GATE-FAMILY-20260921（prod 0.82→0.60–0.67）；ASI LLNgdpw2 / 88jaV5lv；IND ZYbqREW1 / levk5JYN（prod 0.54–0.55）） <!-- lint:const-ok 证据原文 -->
   - 前提：未门控的基础信号 IS sharpe 不低于 2.5、fitness 不低于 1.5（GLB 2026-09-27 铁律：门控只修 prod / robust，不造强度）；慢信号门控后换手会升，只用于快信号
- **不要用**：同族兄弟连提：后来者的 prod 会被顶高（0.67→0.98），同族一次只提 1 颗（KOR profile 避坑） <!-- lint:const-ok 证据原文 -->
- **不要用**：add(卖, 买) 这类经济聚合当分母：闸 5 判 equal_weight_leg_add，改单字段分母或同源 subtract 价差（KOR 七约束 #3） <!-- lint:const-ok 证据原文 -->
- 提醒：prod 与 self 两个端点都取 max、都过线才可提；不改持仓的降 prod 杠杆（hump、加大 decay）会把 self 推爆（EUR wave274） <!-- lint:const-ok 证据原文 -->
- 提醒：设置是强度闸：nanHandling / maxTrade / decay / 中性化换档等于换信号，跨档结果不可比（IND 行为族 S 2.19→0.46） <!-- lint:const-ok 证据原文 -->
- 提醒：decay 匹配信号速度：快信号上 decay 越大越差；decay 0 与 1 逐位相同，只留一个 <!-- lint:const-ok 证据原文 -->
- 提醒：prod 墙先看直方图分单颗钉子 / 密墙 / 可破三型，再决定换分母、换设置档或分组轴（决策表 D0-P 诊断前置） <!-- lint:const-ok 证据原文 -->

### S5 提交前

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region KOR --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| KOR-FND21-ESG-DEAD | esg_sentiment | fnd27_allcategories_* 系列字段不再投任何变体 | fundamental21 | payload | <!-- lint:const-ok 证据原文 -->
| KOR-FND21-ESG-WEAK | esg-news-derived | Do not probe ESG/news-derived fundamental score datasets in KOR (fundamental21 fnd21/fnd27 families); governance quality | fundamental21 | payload | <!-- lint:const-ok 证据原文 -->
| KOR-FND86-SCORE-WEAK | slow_fundamental_score | KOR 慢变评分类基本面单独使用强度上限约 0.85，不要再投入打磨；仅作组合辅助腿参考 | fundamental86 | payload | <!-- lint:const-ok 证据原文 -->
| KOR-FND86-WEAK-SIGNAL |  | 评分类数据集（CapitalCube风格decile评分）在KOR信号强度不足，优先级降低，仅在组合腿慢腿候选池保留average_score | fundamental86 | payload | <!-- lint:const-ok 证据原文 -->
| KOR-FND93-TAXACCRUAL-WEAK | fundamental | Do not reinvest in fundamental93 in KOR unless combined with a confirmed stronger cross-dataset leg; US accrual anomaly  | fundamental93 | payload | <!-- lint:const-ok 证据原文 -->
| KOR-OTH466-QUANTILE-NETINC-FAMILY-DEAD-20261004 | other466 quantile 骨架 × 净利族分子（prod 墙） | 同骨架已有 2 颗 ACTIVE（0mrnWojG/gJZ7AvZO）；净利族分子（consol_net_inc/net_inc_basic_beft_xord/net_inc_dil/net_inc_basic）互相同义 ⇒ prod 必 | other466 | payload | <!-- lint:const-ok 证据原文 -->

### 胜绩

| 条目 | 机制 | 设置与骨架 | 数据集 | 归属 |
|---|---|---|---|---|
| KOR-OTHER466-CORE-EARN-YIELD-MKT-WIN | other466 核心盈利资产收益率价差 × market 轴 |  | other466 | payload | <!-- lint:const-ok 证据原文 -->
| KOR-OTHER466-WIN-A1NXddRw | other466 利润÷总资产 族 |  | other466 | payload | <!-- lint:const-ok 证据原文 -->
| KOR-OTHER466-WIN-wpZkk1Mp | other466 利润÷总资产 族 |  | other466 | payload | <!-- lint:const-ok 证据原文 -->
| KOR-WIN-OTH466-QUANTILE-NETINC-CURRASSET-20261003 | KOR other466 净利/流动资产比率的 quantile 包装形态——全闸通过并提交 ACTIVE，fundam | ★★ 分母是破 SELF 墙的真变量：同分子换分母使 self 0.7422→0.6244、prod 0.8061→0.6843。该族最优基准是『资产类』口径（bs_assets_curr_q 2Y2.22 / bs_eq_tot_q 2. | other466 | payload | <!-- lint:const-ok 证据原文 -->
| KOR-WIN-OTH466-QUANTILE-PTXINC-EQUITY-20261003 | KOR other466 财务比率族用 quantile 包装（非 signed_power）后全闸通过并提交 ACTI | OTHER466 利润/权益比率的 quantile 包装形态：内层 industry 去行业盈利水平 + 1008 日历史分位 + 外层 market 取秩 + 高斯分位变换。IS 四闸全清 + prod 0.6413 / self 0. | other466 | payload | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
<!-- profiles:manual:end -->
