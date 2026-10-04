# MEA × fundamental（组合分支）

> 回到 [MEA 区域流程](../SKILL.md) · [MEA profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/MEA.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region MEA --category fundamental`

<!-- profiles:cell-panel:start -->
**状态**：archived（跟区域入场 frozen）　**分组**：Fundamental　**类别卡**：fundamental

**涉及数据集**：fundamental、fundamental6、fundamental72

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | MEA | 区域 settings.json |
| universe | TOP400 | 区域 settings.json |
| delay | 1 | 区域 settings.json |
| neutralization | SECTOR | 区域 settings.json |
| decay | 4 | 区域 settings.json |
| truncation | 0.08 | 区域 settings.json |
| maxTrade | ON | 区域 settings.json |
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
| 25 | 1 | 6 | 1 | 8 | 2 |

主要数据集（回测数）：fundamental72（20）、fundamental6（5）

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

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region MEA --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| MEA-2DS-CURRENT-SKELETON-DEAD | fnd72+ern3 现有骨架（M+e3 及掺 cf） | 两数据集路线不可沿用 M+e3 骨架；analyst7 rev 腿是 2y 引擎唯一承载——若要两数据集必须换主腿经济逻辑 | fundamental72 | inferred | <!-- lint:const-ok 证据原文 -->
| MEA-FND-EARN-2DS-DEAD | fundamental72×earnings3 两数据集组合（M+e3 骨架变体与应计/盈余质量/SUE 新逻辑） | MEA 不再挖 fundamental72×earnings3 两数据集组合任何形态；e3 腿单独无法承载 2y 引擎，必须与 rev 腿共存 | fundamental72 | inferred | <!-- lint:const-ok 证据原文 -->
| MEA-FND6-EVENT-FIELDS-DEAD | fundamental6 全字段（VECTOR 元数据标错，实际 EVENT 类型） | MEA 不再挖 fundamental6 任何形态；fundamental 族（fundamental6 + fundamental72）全图关闭；EVENT 字段陷阱与 fundamental72 同款（元数据标 VECTOR 实际 EV | fundamental6 | inferred | <!-- lint:const-ok 证据原文 -->
| MEA-FND6-QLEVEL-ZSCORE-DEAD | fundamental6 质量流水平zscore骨架 | fundamental水平流单腿zscore在MEA无信号; 质量价差需比率化(分子/分母同除)而非双腿zscore相加; est_q_pre预告动量短窗无信号, 长窗(63d+)且限sal/eps族 | fundamental6 | inferred | <!-- lint:const-ok 证据原文 -->
| MEA-FND72-CF-SPARSE-DEAD | fundamental72 CF 家族 (CFO/asset、retain_earn/asset、income_unco | MEA TOP400 任何 VECTOR 字段挖前必须 longCount>=80 sanity check；f72 仅剩 is_q 已判死，f72 整集收官 | fundamental72 | inferred | <!-- lint:const-ok 证据原文 -->
| MEA-FND72-EPS-SURPRISE-DEAD | analyst×fundamental eps surprise/estimate momentum | 下次不要再用fnd72实际EPS与analyst7预估EPS做差/做比或预估水平动量; EPS方向改用修订计数广度腿(已验证有效) | fundamental72 | payload | <!-- lint:const-ok 证据原文 -->
| MEA-FND72-ISQ-LEVEL-PROD-SATURATED | fundamental72 is_q 水平场 zscore252 (oper_inc/EBITDA 族) | MEA 不再挖 fundamental 盈利水平场 (earnings LEVEL factor)；is_q 整族判死（wave50 per-share/tax/non-oper 无独立信号）；下一族 fundamental6 差异化信号或 | fundamental72 | inferred | <!-- lint:const-ok 证据原文 -->
| MEA-RATIO-ADDITIVE-SKELETON-DEAD | fundamental ratio additive | 比率族(rank(divide))不要用add加权加和; 改用multiply乘积结构(见MEA-FND6-RATIO-MULTIPLY-SKELETON win) | fundamental | inferred | <!-- lint:const-ok 证据原文 -->

### 胜绩

| 条目 | 机制 | 设置与骨架 | 数据集 | 归属 |
|---|---|---|---|---|
| MEA-DELEVERAGE-LEG-FIELD-PRIORITY | fundamental deleverage leg | multiply(ts_zscore(vec_avg(<liab_field>),252),-1) 作为0.4权重负腿; 窗口锁252(504塔崩); liab_field优先级: fundamental_other_liabilities | fundamental | inferred | <!-- lint:const-ok 证据原文 -->
| MEA-FND6-RATIO-MULTIPLY-SKELETON | fundamental ratio multiply | multiply(rank(divide(vec_avg(<quality_ratio>),vec_avg(<equity_base>))), rank(multiply(ts_zscore(vec_avg(<liab>),252),-1) | fundamental6 | inferred | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
<!-- profiles:manual:end -->
