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
<!-- profiles:manual:end -->
