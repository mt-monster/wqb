# IND × other（组合分支）

> 回到 [IND 区域流程](../SKILL.md) · [IND profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/IND.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region IND --category other`

<!-- profiles:cell-panel:start -->
**状态**：probe（跟区域入场 probe-only）　**分组**：Other　**类别卡**：other

**备注**：other532 Barra 特质收益残差的短期反转（2026-10-03 突破，IND 唯一 S>3 活族）——可能满足 IND profile 写的升档条件「新的信息维度」，升不升档由人复核 prod 后定

**涉及数据集**：acquisition_model、ai_news_scores、mmp_nlp_sentiment、other128、other315、other545、other567

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
| 0 | 0 | 92 | 19 | 9 | 0 |

### S1 字段理解

- 数据集名会骗人：必读字段 description；稀疏高 valueScore 是陷阱
- 窗口（类别卡，均在白名单内）：daily 5/22；quarterly 66/252

### S2 生成

- **用**：累加腿 rank(-ts_sum(x, 5)) 比单期 rank(-x) 换手低 2.7 倍且 S 更高：既是最强腿，也是破 prod 墙的起点（WorkBuddy MEMORY §1.6）
- **用**：区域口径三选一：emerging / asia_ase2（亚洲除日本，与 IND 最贴）/ global
- **避**：股本收缩族（number_of_issued_shares、other323 esor 版）在 IND 判死（回购少、稀释多）
- **避**：analyst_base_ref 分歧度族判死（S ≤0.69、TO 1.235）
- **已验证骨架**（证据见每行注释；照抄前先按本组合当前 prod 复核）：

  ```text
  signed_power(rank(-ts_sum(oth532_emerging_daily_specificreturn, 5)), 0.4)
  ```

  - signed_power(rank(-ts_sum(oth532_emerging_daily_specificretu… ← gJZwVXVm S 3.66 / F 2.83 / TO 0.321，is.checks 无 FAIL（WorkBuddy MEMORY §1.6；prod 待测）
- **类别通用原语**（类别卡，跨区）：
  - name the priced risk first; the operator is secondary
  - 先按字段 description 判断经济含义，再套对应类别卡的思路（例：KOR other466 是财务比率 → fundamental；IND other532 是 Barra 特质收益 → 残差反转）
- **跨区结论**（KOR/EUR/DEU/GBR；negative）：other455 网络嵌入（n2v）族（证据：KOR RULES §G；EUR-W253-OTHER455-CUSTOMER-NETWORK-RETURNS；DEU-OTH455-PURECOMP-SUBUNIVERSE-WALL-20260923；GBR 红榜） <!-- lint:const-ok 证据原文 -->
- **禁止**（全局锁定）：禁止两条独立信号腿相加：加权（0.4×A + 0.6×B）、等权 add(rank(A), rank(B))、中缀 + 都算；第二个数据集只以条件（trade_when / if_else）、分组（group_rank / bucket）或残差（regression_neut / vector_neut）入场
- **禁止**（全局锁定）：禁止 ts_event_* 系列（平台没有）与幽灵算子；字段名逐一经 get_datafields 验证

### S4 改进（按顺序试：组合 → 类别卡 → 全局）

1. [组合] 深挖优先级：累加窗梯度 > 秩后裁剪 > quantile 等价替换（证据：WorkBuddy MEMORY §1.6） <!-- lint:const-ok 证据原文 -->
2. [全局] 判「无解 / 天花板」前先扫等价算子替换：signed_power → quantile、ts_scale → quantile / normalize。数值路径不同，一次动多个闸（含 prod，要读全部闸）（KOR/GLB 复现：KOR other466 signed_power→quantile：2Y 1.51→1.56、prod 0.6544→0.6397；GLB quantile 替 ts_scale：S +0.20、F +0.06、prod 0.475→0.565（DEC-72）） <!-- lint:const-ok 证据原文 -->
   - 注意：效应量逐区实测，禁外推；quantile 只收 1 个参数
3. [全局] 强但撞 prod 墙的快信号：用一个经济子集门控（trade_when 进 >0.5 出 <0.4 的慢变量，或 rank(cap)>0.2 ∩ 子集）只在子集里持仓（GLB/ASI/IND 复现：GLB-DL20D-SUBSET-GATE-FAMILY-20260921（prod 0.82→0.60–0.67）；ASI LLNgdpw2 / 88jaV5lv；IND ZYbqREW1 / levk5JYN（prod 0.54–0.55）） <!-- lint:const-ok 证据原文 -->
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
| IND-ACQMODEL-WEAK-NEG | acquisition_model | 并购目标概率百分位字段族在 IND TOP500 无 alpha 转化力；弱负向信号（／S／<1.0）不做反转波（对比 wave76 强负向才反转） | acquisition_model | inferred | <!-- lint:const-ok 证据原文 -->
| IND-AI-NEWS-DEAD | ai_news_scores sentiment | Avoid ai_news_scores in IND; news sentiment family exhausted (news_sentiment_nlp, news_sentiment_transfer, ai_news_score | ai_news_scores | inferred | <!-- lint:const-ok 证据原文 -->
| IND-AINEWS-SENTIMENT-DEAD | ai_news_scores sentiment | IND 区域回避新闻情感/NLP 类信号，该方向换手极高且无 alpha | ai_news_scores | inferred | <!-- lint:const-ok 证据原文 -->
| IND-MMPNLP-UNAVAILABLE | mmp_nlp_sentiment | IND 区域 mmp_nlp_sentiment 数据集不可用，勿再尝试 | mmp_nlp_sentiment | inferred | <!-- lint:const-ok 证据原文 -->
| IND-OTHER128-MANAGEMENT-QUALITY-DEAD | executive_performance |  | other128 | payload | <!-- lint:const-ok 证据原文 -->
| IND-OTHER315-SPARSE-DEAD | other315 equity swap | IND区域事件披露稀疏的other类数据集(other315型)首探批若>60%空持仓即止损，新鲜度机制窗口梯度递减即判死，勿恋战 | other315 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-OTHER545-NEMO-DEAD | other545 NEMO network momentum | IND 区域 other545 网络动量信号族判死，不再投入回测资源 | other545 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-OTHER567-DEAD | other567 glassdoor | Avoid other567 in IND; employee sentiment data does not translate to alpha in this market | other567 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-OTHER567-EMPLOYEE-SCORE-DEAD | other567 employee review | IND 区域 employee review 评分水平信号判死；变化/分歧类衍生信号（同源于水平）不必再烧配额。评分类字段适用 group_neutralize 配方的前提除行业可比外，信号本身必须有 alpha（fnd86 机构综合评分有 | other567 | inferred | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
### 2026-10-10 other532 prod 破墙战役（可携带经验）

**背景**：other532 Barra 特质收益短期反转 `signed_power(rank(-ts_sum(oth532_emerging_daily_specificreturn, 5)), 0.4)`（gJZwVXVm）IS 全闸 PASS（S 3.66 / F 2.83 / TO 0.321 / sub 1.94 / 2Y 2.85）但 **prod 0.8896**，被单颗钉子钉在 0.70 之上 ⇒ IND「唯一 S>3 活族」被 prod 墙封死。

**结论 1（破墙杠杆唯一性）**：约 20+ 变体后，**唯一有效的降 prod 杠杆 = 用慢变量把信号限制在一个经济子集里**（`trade_when(rank(慢变量), 进 >0.5 / 出 <0.4)`）：prod 0.8896 → **0.5487–0.5966**，且 2Y / robust / sub 仍在线上。
- **已排除（数值路径相同，不降 prod）**：区域口径置换（emerging / asia_ase2 / global → 0.86–0.88）、`quantile` 等价替换（0.8893）、`winsorize`（rank 已消尾，与基线逐位相同）。
- **已排除（换持仓但信号崩）**：monthly 频率（|S| ≤0.06）、小盘子集（sub 0.79 / rob 0.61 / 2Y 1.42 全跌破）、高波动子集（rob 0.70 / 2Y 1.48 跌破）。
- **有效门控矩阵**（4 个独立亚族，互相关 0.19–0.70 ⇒ 各自可出候选）：

  | 门控 | 字段类别 | 代表 alpha | S | prod |
  |---|---|---|---|---|
  | 大市值 | PV(`cap`) | akxzlYV6 | 3.04 | 0.5817 |
  | 低波动 | PV(`returns`) | E5Rza2AK | 2.79 | 0.5487 |
  | 窄带 0.6/0.5 | PV(`cap`) | WjezXxqd | 2.57 | 0.5508 |
  | 宽带 0.4/0.3 | PV(`cap`) | d51z7PVw | 3.26 | 0.5966 |
  | cap × 短窗 win3 | PV(`cap`) | 6XK0q2vp | 3.15 | 0.5730 |

**结论 2（★ 塔归属法则，跨区可携带）**：`MATCHES_PYRAMID` 的匹配塔数 = **表达式所用全部字段（含门控字段）的数据集类别的并集**。
- 纯 `other532`（other 类别）⇒ eff=1，单塔 `IND/D1/OTHER ×1.3`。
- `other532` + `cap`（**PV 类别**）⇒ eff=2（PV×1.1 + OTHER×1.3）⇒ 不满足「两两不同时选」。
- ⇒ **要造单塔候选，门控字段必须与信号字段同类别**。单 OTHER 塔用 `oth327_mktcap` / `oth327_sirc_lev` / `oth327_sirc_sl` / `oth424_divyld` / `dividend_growth_factor_score` / `oth424_mktcap`（均 other 类别）。
- 验证：wave160 用 other 门控重造 5 颗，全部 eff=1 单 OTHER 塔，prod 仍跌破上限。

**结论 3（族单位 = 门控信息源）**：「一条腿只出 1 颗」只在**同门控变体**内成立；**换门控字段可把同腿互相关压到 0.5–0.69** ⇒ 同一信号腿可产出多颗互相关低于上限的可提交候选。

**结论 4（入场未被推翻）**：other532 能破墙是**门控改变了持仓子集**，不是原信号本身脱离了 prod book ⇒ IND 20 批穷尽扫描的结论（8 颗 IS 全过候选 prod 全在 0.7161–0.8261）**依然成立**；升档须由人复核提报。

**结论 5（判死边界）**：other424（股息增长 GRID）在 IND TOP500 是**弱池**（8 探针 S 天花板 ~1.05，GRID 股息分数不为印度成长股定价）——标记弱池搁置（不深挖、不判死），但其字段可作 other 类别门控用。
<!-- profiles:manual:end -->
